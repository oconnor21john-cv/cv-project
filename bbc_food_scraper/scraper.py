"""
Multi-source recipe scraper. Handles robots.txt, rate limiting, and
fallback strategies for each supported site.
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import json
import re
from datetime import datetime
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse, urljoin, quote_plus, parse_qs, unquote
from typing import List, Dict, Optional
import concurrent.futures
import xml.etree.ElementTree as ET


class BaseScraper:
    """Shared base for all source scrapers — handles requests, robots.txt, and fallbacks."""
    
    def __init__(self):
        # Standard browser headers to avoid unnecessary bot blocks.
        self.headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/123.0.0.0 Safari/537.36'
            ),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.robots_parser = None
        self.robots_base_netloc = None
        self.fast_mode = False  # set True by analysis pipeline to skip delays/retries
        self.query_normalization = {
            'lasagne': 'lasagna',
            'courgette': 'zucchini',
            'aubergine': 'eggplant',
            'coriander': 'cilantro',
            'mince': 'ground',
        }
        self.reset_diagnostics()

    def reset_diagnostics(self):
        """Clear per-search state used for source health reporting."""
        self.last_http_status_codes = set()
        self.last_blocked_by_robots = False
        self.used_external_fallback = False
        self.used_mirror_fallback = False
    
    def _init_robots_parser(self, base_url: str):
        """Fetch and parse robots.txt for this source."""
        try:
            robots_url = f"{base_url.rstrip('/')}/robots.txt"
            robots_response = self.session.get(robots_url, timeout=15)
            if robots_response.status_code >= 400 or not robots_response.text.strip():
                # Can't load robots.txt — don't assume everything is blocked.
                self.robots_parser = None
                self.robots_base_netloc = None
                print(f"[WARN] robots.txt unavailable for {base_url} (status {robots_response.status_code})")
                return

            parser = RobotFileParser()
            parser.parse(robots_response.text.splitlines())
            self.robots_parser = parser
            self.robots_base_netloc = urlparse(base_url).netloc
            print(f"[OK] robots.txt loaded for {base_url}")
        except Exception as e:
            print(f"[WARN] Could not load robots.txt for {base_url}: {e}")
            self.robots_parser = None
            self.robots_base_netloc = None
    
    def can_fetch(self, url: str) -> bool:
        """Check whether robots.txt permits this URL."""
        if self.robots_parser:
            # Only enforce this site's rules — don't block off-site fallbacks.
            url_netloc = urlparse(url).netloc
            if self.robots_base_netloc and url_netloc != self.robots_base_netloc:
                return True
            return self.robots_parser.can_fetch('*', url)
        return True
    
    def get_crawl_delay(self) -> float:
        """Crawl delay from robots.txt, or 1 second if not specified."""
        if self.fast_mode:
            return 0.0
        if self.robots_parser:
            delay = self.robots_parser.crawl_delay(self.headers['User-Agent'])
            if delay:
                return float(delay)
        return 1.0
    
    def _make_request(self, url: str, max_retries: int = 2) -> Optional[requests.Response]:
        """Rate-limited GET with retry logic."""
        if not self.can_fetch(url):
            print(f"[BLOCKED] robots.txt disallows: {url}")
            self.last_blocked_by_robots = True
            return None

        if self.fast_mode:
            max_retries = 0

        for attempt in range(max_retries + 1):
            try:
                delay = self.get_crawl_delay()
                if not self.fast_mode:
                    delay += random.uniform(0.5, 1.5)
                if attempt > 0:
                    delay += attempt * 0.75
                time.sleep(delay)

                request_headers = {
                    'Referer': f"{urlparse(url).scheme}://{urlparse(url).netloc}/",
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                }

                response = self.session.get(url, timeout=20, headers=request_headers)

                # Back off and retry on anti-bot throttle responses.
                self.last_http_status_codes.add(response.status_code)
                if response.status_code in (403, 429) and attempt < max_retries:
                    print(f"[RETRY] HTTP {response.status_code} for {url} (attempt {attempt + 1})")
                    continue

                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if attempt >= max_retries:
                    print(f"[ERROR] Request failed for {url}: {e}")
                    return None

        return None

    def _extract_duckduckgo_result_url(self, href: str) -> str:
        """Resolve a DuckDuckGo result link to its actual destination URL."""
        if not href:
            return ''

        if href.startswith('http'):
            return href

        # DuckDuckGo often uses redirect links such as /l/?uddg=<encoded-url>
        parsed = urlparse(href)
        if parsed.path.startswith('/l/'):
            encoded = parse_qs(parsed.query).get('uddg', [''])[0]
            if encoded:
                return unquote(encoded)
        return ''

    def _fallback_site_search(self, query: str, site_domain: str, max_results: int = 12) -> List[str]:
        """DuckDuckGo site: search, used when the site's own search is blocked."""
        if self.fast_mode:
            return []
        self.used_external_fallback = True
        search_query = f"site:{site_domain} {query} recipe"
        ddg_url = f"https://duckduckgo.com/html/?q={quote_plus(search_query)}"
        print(f"[FALLBACK] DuckDuckGo site search: {ddg_url}")

        response = self._make_request(ddg_url, max_retries=1)
        if not response:
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        links = []

        for anchor in soup.select('a.result__a, .result a[href], a[href]'):
            href = anchor.get('href', '')
            resolved = self._extract_duckduckgo_result_url(href) or href

            if not resolved.startswith('http'):
                continue

            parsed = urlparse(resolved)
            if site_domain not in parsed.netloc:
                continue

            if resolved not in links:
                links.append(resolved)

            if len(links) >= max_results:
                break

        print(f"[FALLBACK] Found {len(links)} fallback links for {site_domain}")
        return links

    def _fetch_markdown_via_mirror(self, url: str) -> Optional[str]:
        """Fetch a page through the Jina reader mirror as plain markdown."""
        self.used_mirror_fallback = True
        mirror_url = f"https://r.jina.ai/http://{url.lstrip('/')}".replace('http://https://', 'http://')
        print(f"[FALLBACK] Mirror fetch: {mirror_url}")

        for attempt in range(2):
            try:
                response = self.session.get(mirror_url, timeout=70)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                if attempt == 1:
                    print(f"[ERROR] Mirror fetch failed for {url}: {e}")
                    return None
                print(f"[RETRY] Mirror fetch retry for {url}")
                time.sleep(1.5)

        return None

    def _extract_urls_from_markdown(self, markdown: str, site_domain: str, max_results: int = 20) -> List[str]:
        """Pull unique same-domain URLs out of mirrored markdown."""
        urls = re.findall(rf'https://(?:www\.)?{re.escape(site_domain)}/[^\s\)"]+', markdown)
        deduped = []
        for url in urls:
            clean = url.rstrip('.,;:')
            if clean not in deduped:
                deduped.append(clean)
            if len(deduped) >= max_results:
                break
        return deduped

    def _clean_markdown_text(self, text: str) -> str:
        """Strip markdown/link noise from mirrored content."""
        if not text:
            return ''

        cleaned = text
        cleaned = re.sub(r'!\[[^\]]*\]\([^)]+\)', ' ', cleaned)
        cleaned = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'\1', cleaned)
        cleaned = re.sub(r'https?://\S+', ' ', cleaned)
        cleaned = cleaned.replace('**', '').replace('__', '')
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        cleaned = cleaned.strip(' -•|')
        return cleaned

    def _is_noise_markdown_line(self, line: str) -> bool:
        """True if this line is navigation/image noise rather than recipe content."""
        if not line:
            return True

        stripped = line.strip()
        lowered = stripped.lower()

        if stripped.startswith('![') or stripped.startswith('[!['):
            return True
        if stripped.startswith('[') and '](' in stripped and stripped.endswith(')'):
            return True
        if lowered.startswith('skip to content'):
            return True
        if lowered.startswith('keep screen awake'):
            return True
        if lowered.startswith('image ') or lowered.startswith('image:'):
            return True
        if re.match(r'^(serious eats|simply recipes|bbc(?: food)?)\s*/\s*', stripped, flags=re.IGNORECASE):
            return True

        return False

    def _extract_recipe_from_markdown(self, markdown: str, source: str, url: str) -> Optional[Dict]:
        """Extract recipe data from a Jina-mirrored markdown page."""
        lines = [line.strip() for line in markdown.splitlines()]
        lines = [line for line in lines if line]

        if not lines:
            return None

        # Title
        title = 'Unknown Recipe'
        title_match = re.search(r'^Title:\s*(.+)$', markdown, flags=re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
        elif lines:
            title = lines[0]

        # Description: first plain sentence-like line after content header.
        description = ''
        for line in lines:
            if line.startswith('URL Source:') or line.startswith('Markdown Content:'):
                continue
            if self._is_noise_markdown_line(line):
                continue
            cleaned_line = self._clean_markdown_text(line)
            if len(cleaned_line) > 40 and '|' not in cleaned_line:
                description = cleaned_line
                break

        # Image
        image_match = re.search(r'!\[[^\]]*\]\((https?://[^)]+)\)', markdown)
        image = image_match.group(1) if image_match else ''

        # Ingredients: strongest marker in mirrored recipes.
        ingredients = []
        start_idx = 0
        for i, line in enumerate(lines):
            if line.lower() == 'keep screen awake':
                start_idx = i + 1
                break

        first_step_idx = None
        for i in range(start_idx, len(lines)):
            if re.match(r'^\d+\.\s+', lines[i]):
                first_step_idx = i
                break

        if first_step_idx is not None:
            for line in lines[start_idx:first_step_idx]:
                bullet = re.match(r'^\*\s+(.*)$', line)
                if bullet:
                    item = self._clean_markdown_text(bullet.group(1).strip())
                    if item:
                        ingredients.append(item)

        # Instructions: parse numbered steps and continuation lines.
        instructions = []
        current_step = ''
        if first_step_idx is not None:
            for line in lines[first_step_idx:]:
                step_match = re.match(r'^\d+\.\s+(.*)$', line)
                if step_match:
                    if current_step:
                        instructions.append(current_step.strip())
                    current_step = self._clean_markdown_text(step_match.group(1).strip())
                    continue

                if current_step:
                    # Stop if we reached nutrition/table/footer content.
                    if line.startswith('|') or line.startswith('Nutrition') or line.startswith('©'):
                        break
                    if line.startswith('**Love the recipe'):
                        break
                    if self._is_noise_markdown_line(line):
                        continue
                    continuation = self._clean_markdown_text(line)
                    if not continuation:
                        continue
                    current_step += f" {continuation}"

            if current_step:
                instructions.append(current_step.strip())

        if len(ingredients) < 2:
            return None

        return {
            'title': title,
            'description': description,
            'ingredients': ingredients,
            'instructions': instructions,
            'image': image,
            'url': url,
            'scraped_at': datetime.now().isoformat(),
            'source': source,
            'extraction_method': 'Mirror markdown parsing',
            'prep_time': '',
            'cook_time': '',
            'total_time': '',
            'servings': '',
            'author': '',
            'cuisine': '',
            'category': '',
        }

    def _query_variants(self, query: str) -> List[str]:
        """Generate UK/US spelling variants for a query."""
        base = query.strip()
        if not base:
            return []

        variants = [base]
        lowered = base.lower()
        for uk, us in self.query_normalization.items():
            if uk in lowered:
                variants.append(lowered.replace(uk, us))

        # De-duplicate while preserving order.
        return list(dict.fromkeys(variants))

    def _is_probable_recipe_url(self, url: str, query_tokens: set) -> bool:
        """Best-guess check for whether a URL looks like a recipe page."""
        parsed = urlparse(url)
        path = parsed.path.strip('/').lower()
        if not path:
            return False

        # Reject obvious non-recipe routes.
        non_recipe_patterns = (
            path.startswith('search'),
            path.startswith('tag/'),
            path.startswith('topics/'),
            path.startswith('about'),
            path.startswith('contact'),
            'all-recipes' in path,
            'recipes-by-' in path,
            path.startswith('what-is-'),
            path.startswith('what-are-'),
            path.startswith('how-to-'),
        )
        if any(non_recipe_patterns):
            return False

        # Ensure some relation to the user's query when possible.
        if query_tokens and not any(tok in path for tok in query_tokens):
            return False

        recipe_markers = (
            '-recipe' in path,
            '/recipes/' in url.lower(),
            bool(re.search(r'-\d{6,}$', path)),
        )
        if any(recipe_markers):
            return True

        # Older article slugs can still be recipes without explicit "-recipe".
        return path.count('-') >= 3
    
    def _parse_duration(self, duration: str) -> str:
        """Convert ISO 8601 duration (e.g. PT1H30M) to a readable string."""
        if not duration:
            return ''
        
        try:
            import re
            match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?', duration)
            if match:
                hours = int(match.group(1) or 0)
                minutes = int(match.group(2) or 0)
                parts = []
                if hours:
                    parts.append(f"{hours}h")
                if minutes:
                    parts.append(f"{minutes}m")
                return ' '.join(parts) if parts else ''
        except:
            pass
        
        return duration
    
    def _extract_author(self, author_data) -> str:
        """Pull author name from string, dict, or list formats."""
        if not author_data:
            return ''
        if isinstance(author_data, str):
            return author_data
        if isinstance(author_data, dict):
            return author_data.get('name', '')
        if isinstance(author_data, list) and author_data:
            first = author_data[0]
            return first if isinstance(first, str) else first.get('name', '')
        return ''
    
    def _is_recipe_type(self, type_value) -> bool:
        """True if the JSON-LD @type value is or includes Recipe."""
        if isinstance(type_value, str):
            return type_value == 'Recipe'
        if isinstance(type_value, list):
            return 'Recipe' in type_value
        return False
    
    def _extract_json_ld(self, soup: BeautifulSoup, source: str) -> Optional[Dict]:
        """Parse Schema.org Recipe from JSON-LD script tags."""
        scripts = soup.find_all('script', type='application/ld+json')
        
        for script in scripts:
            try:
                data = json.loads(script.string)
                
                # Handle @graph format
                if isinstance(data, dict) and '@graph' in data:
                    data = data['@graph']
                
                # Handle array format
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and self._is_recipe_type(item.get('@type')):
                            data = item
                            break
                    else:
                        continue
                
                if not isinstance(data, dict) or not self._is_recipe_type(data.get('@type')):
                    continue
                
                # Extract ingredients
                ingredients = data.get('recipeIngredient', [])
                if isinstance(ingredients, str):
                    ingredients = [ingredients]
                
                # Extract instructions
                instructions = []
                raw_instructions = data.get('recipeInstructions', [])
                if isinstance(raw_instructions, str):
                    instructions = [raw_instructions]
                elif isinstance(raw_instructions, list):
                    for inst in raw_instructions:
                        if isinstance(inst, str):
                            instructions.append(inst)
                        elif isinstance(inst, dict):
                            # Handle HowToStep directly
                            text = inst.get('text', '')
                            if text:
                                instructions.append(text)
                            # Handle HowToSection with nested steps
                            elif inst.get('@type') == 'HowToSection':
                                section_name = inst.get('name', '')
                                if section_name:
                                    instructions.append(f"**{section_name}**")
                                for step in inst.get('itemListElement', []):
                                    if isinstance(step, str):
                                        instructions.append(step)
                                    elif isinstance(step, dict):
                                        step_text = step.get('text', '')
                                        if step_text:
                                            instructions.append(step_text)
                
                # Extract image
                image = ''
                img_data = data.get('image')
                if isinstance(img_data, str):
                    image = img_data
                elif isinstance(img_data, dict):
                    image = img_data.get('url', '')
                elif isinstance(img_data, list) and img_data:
                    first = img_data[0]
                    image = first if isinstance(first, str) else first.get('url', '')
                
                # Extract timing
                prep_time = self._parse_duration(data.get('prepTime', ''))
                cook_time = self._parse_duration(data.get('cookTime', ''))
                total_time = self._parse_duration(data.get('totalTime', ''))
                
                return {
                    'title': data.get('name', 'Unknown Recipe'),
                    'description': data.get('description', ''),
                    'ingredients': ingredients,
                    'instructions': instructions,
                    'image': image,
                    'prep_time': prep_time,
                    'cook_time': cook_time,
                    'total_time': total_time,
                    'servings': str(data.get('recipeYield', '')),
                    'author': self._extract_author(data.get('author')),
                    'cuisine': data.get('recipeCuisine', ''),
                    'category': data.get('recipeCategory', ''),
                    'source': source,
                }
                
            except (json.JSONDecodeError, AttributeError, TypeError):
                continue
        
        return None


class BBCFoodScraper(BaseScraper):
    """BBC Food (bbc.co.uk/food)."""
    
    BASE_URL = "https://www.bbc.co.uk/food"
    SOURCE_NAME = "BBC Food"
    
    def __init__(self):
        super().__init__()
        self._init_robots_parser(self.BASE_URL)
    
    def search_recipes(self, query: str, max_results: int = 12) -> List[Dict]:
        """Search BBC Food and return recipe dicts."""
        self.reset_diagnostics()
        recipes = []
        
        search_url = f"{self.BASE_URL}/search?q={query.replace(' ', '+')}"
        print(f"[SEARCH] {search_url}")
        
        response = self._make_request(search_url)
        if not response:
            return recipes
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try a few different selectors since BBC Food card markup has changed over time.
        recipe_links = []
        
        selectors = [
            'a[href*="/food/recipes/"]',
            '.promo a[href*="/recipes/"]',
            '.gel-layout__item a[href*="/recipes/"]',
        ]
        
        for selector in selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href', '')
                if '/recipes/' in href and href not in recipe_links:
                    if not href.startswith('http'):
                        href = urljoin(self.BASE_URL, href)
                    recipe_links.append(href)
        
        recipe_links = list(dict.fromkeys(recipe_links))[:max_results]
        
        print(f"[FOUND] {len(recipe_links)} recipe links")
        
        for url in recipe_links:
            recipe_data = self.scrape_recipe(url)
            if recipe_data:
                recipes.append(recipe_data)
                print(f"[OK] Scraped: {recipe_data['title']}")
        
        return recipes
    
    def scrape_recipe(self, url: str) -> Optional[Dict]:
        """Fetch and parse a single recipe URL."""
        response = self._make_request(url)
        if not response:
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        recipe_data = self._extract_json_ld(soup, self.SOURCE_NAME)
        
        if recipe_data:
            recipe_data['url'] = url
            recipe_data['scraped_at'] = datetime.now().isoformat()
            recipe_data['extraction_method'] = 'Schema.org JSON-LD'
            return recipe_data
        
        return self._extract_from_html(soup, url)
    
    def _extract_from_html(self, soup: BeautifulSoup, url: str) -> Optional[Dict]:
        """HTML fallback when JSON-LD is absent."""
        try:
            # Title
            title_elem = soup.find('h1')
            title = title_elem.get_text(strip=True) if title_elem else 'Unknown Recipe'
            
            # Description
            desc_elem = soup.find('p', class_=lambda x: x and 'description' in x.lower()) or \
                       soup.find('meta', {'name': 'description'})
            description = ''
            if desc_elem:
                description = desc_elem.get('content', '') or desc_elem.get_text(strip=True)
            
            # Ingredients - look for common patterns
            ingredients = []
            ingredient_sections = soup.find_all(['ul', 'ol'], class_=lambda x: x and 'ingredient' in str(x).lower())
            if not ingredient_sections:
                ingredient_sections = soup.find_all('section', class_=lambda x: x and 'ingredient' in str(x).lower())
            
            for section in ingredient_sections:
                for li in section.find_all('li'):
                    text = li.get_text(strip=True)
                    if text and len(text) > 2:
                        ingredients.append(text)
            
            # Instructions
            instructions = []
            method_sections = soup.find_all(['ol', 'div'], class_=lambda x: x and ('method' in str(x).lower() or 'instruction' in str(x).lower()))
            
            for section in method_sections:
                for item in section.find_all(['li', 'p']):
                    text = item.get_text(strip=True)
                    if text and len(text) > 10:
                        instructions.append(text)
            
            # Image
            image = ''
            img_elem = soup.find('img', class_=lambda x: x and 'recipe' in str(x).lower()) or \
                      soup.find('img', {'itemprop': 'image'}) or \
                      soup.select_one('picture img')
            if img_elem:
                image = img_elem.get('src', '') or img_elem.get('data-src', '')
            
            # Only return if we got meaningful data
            if not ingredients or len(ingredients) < 2:
                return None
            
            return {
                'title': title,
                'description': description,
                'ingredients': ingredients,
                'instructions': instructions,
                'image': image,
                'url': url,
                'scraped_at': datetime.now().isoformat(),
                'source': self.SOURCE_NAME,
                'extraction_method': 'HTML parsing',
                'prep_time': '',
                'cook_time': '',
                'total_time': '',
                'servings': '',
                'author': '',
                'cuisine': '',
                'category': '',
            }
            
        except Exception as e:
            print(f"[ERROR] HTML extraction failed: {e}")
            return None
    
    def get_featured_recipes(self, max_results: int = 8) -> List[Dict]:
        """Pull recipe links from the BBC Food homepage."""
        recipes = []
        
        print(f"[HOME] Fetching featured recipes from homepage...")
        
        response = self._make_request(self.BASE_URL)
        if not response:
            return recipes
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find recipe links on homepage
        recipe_links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            if '/recipes/' in href:
                if not href.startswith('http'):
                    href = urljoin(self.BASE_URL, href)
                if href not in recipe_links:
                    recipe_links.append(href)
        
        recipe_links = recipe_links[:max_results]
        
        for url in recipe_links:
            recipe_data = self.scrape_recipe(url)
            if recipe_data:
                recipes.append(recipe_data)
                print(f"[OK] Scraped: {recipe_data['title']}")
        
        return recipes


class BBCGoodFoodScraper(BaseScraper):
    """BBC Good Food (bbcgoodfood.com)."""

    BASE_URL = "https://www.bbcgoodfood.com"
    SOURCE_NAME = "BBC Good Food"

    def __init__(self):
        super().__init__()
        self._init_robots_parser(self.BASE_URL)

    def search_recipes(self, query: str, max_results: int = 12) -> List[Dict]:
        self.reset_diagnostics()
        recipes = []

        search_url = f"{self.BASE_URL}/search?q={quote_plus(query)}"
        print(f"[SEARCH] BBC Good Food: {search_url}")

        response = self._make_request(search_url)
        if not response:
            return recipes

        soup = BeautifulSoup(response.content, 'html.parser')
        recipe_links = []

        for link in soup.select('a[href]'):
            href = link.get('href', '')
            if not href:
                continue
            full_url = urljoin(self.BASE_URL, href)
            lowered = full_url.lower()
            if '/recipes/' not in lowered:
                continue
            if any(skip in lowered for skip in (
                '/recipes/collection/',
                '/recipes/category/',
                '/recipes/guide/',
                '/recipes/cookbook/',
                '/recipes/skill/',
            )):
                continue
            if full_url not in recipe_links:
                recipe_links.append(full_url)
            if len(recipe_links) >= max_results:
                break

        print(f"[FOUND] BBC Good Food: {len(recipe_links)} recipe links")

        for url in recipe_links:
            recipe_data = self.scrape_recipe(url)
            if recipe_data:
                recipes.append(recipe_data)
                print(f"[OK] BBC Good Food: {recipe_data['title']}")

        return recipes

    def scrape_recipe(self, url: str) -> Optional[Dict]:
        response = self._make_request(url)
        if not response:
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        recipe_data = self._extract_json_ld(soup, self.SOURCE_NAME)
        if recipe_data:
            recipe_data['url'] = url
            recipe_data['scraped_at'] = datetime.now().isoformat()
            recipe_data['extraction_method'] = 'Schema.org JSON-LD'
            return recipe_data

        return None


class TomKerridgeScraper(BaseScraper):
    """Tom Kerridge (tomkerridge.com) — uses sitemap for discovery."""

    BASE_URL = "https://tomkerridge.com"
    SOURCE_NAME = "Tom Kerridge"
    SITEMAP_URL = "https://tomkerridge.com/recipes-sitemap.xml"

    def __init__(self):
        super().__init__()
        self._init_robots_parser(self.BASE_URL)

    def _recipe_urls_from_sitemap(self, max_candidates: int = 250) -> List[str]:
        response = self._make_request(self.SITEMAP_URL)
        if not response:
            return []

        try:
            root = ET.fromstring(response.content)
        except ET.ParseError:
            return []

        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = []
        for loc in root.findall('.//sm:loc', ns):
            candidate = (loc.text or '').strip()
            if not candidate or '/recipes/' not in candidate:
                continue
            if candidate not in urls:
                urls.append(candidate)
            if len(urls) >= max_candidates:
                break
        return urls

    def search_recipes(self, query: str, max_results: int = 12) -> List[Dict]:
        self.reset_diagnostics()
        recipes = []

        query_tokens = [t for t in re.findall(r'[a-z]+', query.lower()) if len(t) >= 3]
        candidates = self._recipe_urls_from_sitemap(max_candidates=350)
        if query_tokens:
            recipe_links = [
                url for url in candidates
                if any(token in url.lower() for token in query_tokens)
            ][:max_results]
        else:
            recipe_links = candidates[:max_results]

        print(f"[FOUND] Tom Kerridge: {len(recipe_links)} recipe links")

        for url in recipe_links:
            recipe_data = self.scrape_recipe(url)
            if recipe_data:
                recipes.append(recipe_data)
                print(f"[OK] Tom Kerridge: {recipe_data['title']}")

        return recipes

    def scrape_recipe(self, url: str) -> Optional[Dict]:
        response = self._make_request(url)
        if not response:
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        recipe_data = self._extract_json_ld(soup, self.SOURCE_NAME)
        if recipe_data:
            recipe_data['url'] = url
            recipe_data['scraped_at'] = datetime.now().isoformat()
            recipe_data['extraction_method'] = 'Schema.org JSON-LD'
            return recipe_data
        return self._extract_from_html(soup, url)

    def _extract_from_html(self, soup: BeautifulSoup, url: str) -> Optional[Dict]:
        """HTML fallback for Tom Kerridge pages that lack JSON-LD."""
        title_elem = soup.find('h1')
        title = title_elem.get_text(' ', strip=True) if title_elem else 'Unknown Recipe'

        description = ''
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc:
            description = meta_desc.get('content', '').strip()

        ingredients = []
        instructions = []
        servings = ''

        container = soup.select_one('.recipe-details-box')
        if not container:
            return None

        for section in container.select('.ingredients'):
            heading = section.find('p', class_=lambda cls: cls and 'title' in cls)
            section_name = heading.get_text(' ', strip=True).lower() if heading else ''
            content = section.select_one('.grey-box-cust-searve')
            if not content:
                continue

            for p_tag in content.find_all('p'):
                text = p_tag.get_text(' ', strip=True)
                if not text:
                    continue

                upper_text = text.upper()
                if upper_text.startswith('SERVES:'):
                    servings = text.split(':', 1)[-1].strip()
                    continue
                if text in ('Share this Recipe', 'Print'):
                    continue

                if 'ingredient' in section_name:
                    ingredients.append(text)
                elif 'method' in section_name:
                    # Keep numbered methods but remove decorative spacing.
                    instructions.append(re.sub(r'\s+', ' ', text).strip())

        # Desktop and mobile blocks can duplicate — deduplicate before returning.
        ingredients = list(dict.fromkeys(ingredients))
        instructions = list(dict.fromkeys(instructions))

        if len(ingredients) < 2:
            return None

        return {
            'title': title,
            'description': description,
            'ingredients': ingredients,
            'instructions': instructions,
            'image': '',
            'url': url,
            'scraped_at': datetime.now().isoformat(),
            'source': self.SOURCE_NAME,
            'extraction_method': 'Tom Kerridge HTML parsing',
            'prep_time': '',
            'cook_time': '',
            'total_time': '',
            'servings': servings,
            'author': 'Tom Kerridge',
            'cuisine': '',
            'category': '',
        }


class FoodAFactOfLifeScraper(BaseScraper):
    """Food - a Fact of Life (foodafactoflife.org.uk)."""

    BASE_URL = "https://www.foodafactoflife.org.uk"
    SOURCE_NAME = "Food - a Fact of Life"
    RECIPES_URL = "https://www.foodafactoflife.org.uk/recipes/"

    def __init__(self):
        super().__init__()
        self._init_robots_parser(self.BASE_URL)

    def search_recipes(self, query: str, max_results: int = 12) -> List[Dict]:
        self.reset_diagnostics()
        recipes = []
        query_tokens = [t for t in re.findall(r'[a-z]+', query.lower()) if len(t) >= 3]

        response = self._make_request(self.RECIPES_URL)
        if not response:
            return recipes

        soup = BeautifulSoup(response.content, 'html.parser')
        recipe_links = []
        for link in soup.select('a[href]'):
            href = link.get('href', '')
            if not href:
                continue
            full_url = urljoin(self.RECIPES_URL, href)
            if '/recipes/' not in full_url.lower():
                continue
            if full_url.rstrip('/') == self.RECIPES_URL.rstrip('/'):
                continue
            path = urlparse(full_url).path.lower()
            if path.count('/') < 3:
                continue
            if query_tokens and not any(token in path for token in query_tokens):
                continue
            if full_url not in recipe_links:
                recipe_links.append(full_url)
            if len(recipe_links) >= max_results:
                break

        # If strict token filtering found nothing, fall back to first recipe pages.
        if not recipe_links:
            for link in soup.select('a[href]'):
                href = link.get('href', '')
                full_url = urljoin(self.RECIPES_URL, href)
                path = urlparse(full_url).path.lower()
                if '/recipes/' in full_url.lower() and path.count('/') >= 3 and full_url not in recipe_links:
                    if full_url.rstrip('/') != self.RECIPES_URL.rstrip('/'):
                        recipe_links.append(full_url)
                if len(recipe_links) >= max_results:
                    break

        print(f"[FOUND] Food - a Fact of Life: {len(recipe_links)} recipe links")

        for url in recipe_links:
            recipe_data = self.scrape_recipe(url)
            if recipe_data:
                recipes.append(recipe_data)
                print(f"[OK] Food - a Fact of Life: {recipe_data['title']}")

        return recipes

    def scrape_recipe(self, url: str) -> Optional[Dict]:
        response = self._make_request(url)
        if not response:
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        title_elem = soup.find('h1')
        title = title_elem.get_text(strip=True) if title_elem else 'Unknown Recipe'

        description = ''
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc:
            description = meta_desc.get('content', '').strip()

        ingredients = []
        instructions = []
        equipment = ''

        for block in soup.select('.content-block'):
            heading = block.find(['h2', 'h3', 'h4'])
            if not heading:
                continue
            section_title = heading.get_text(' ', strip=True).lower()
            text_parts = []
            for paragraph in block.find_all('p'):
                raw = paragraph.get_text('\n', strip=True)
                if raw:
                    text_parts.extend([part.strip() for part in raw.split('\n') if part.strip()])

            if 'ingredient' in section_title:
                ingredients.extend(text_parts)
            elif 'method' in section_title:
                for li in block.find_all('li'):
                    step = li.get_text(' ', strip=True)
                    if step:
                        instructions.append(step)
                if not instructions:
                    instructions.extend(text_parts)
            elif 'equipment' in section_title:
                equipment = ' '.join(text_parts).strip()

        if len(ingredients) < 2:
            return None

        author = 'Food - a Fact of Life'
        if equipment:
            author = f"{author} | Equipment: {equipment}"

        return {
            'title': title,
            'description': description,
            'ingredients': ingredients,
            'instructions': instructions,
            'image': '',
            'url': url,
            'scraped_at': datetime.now().isoformat(),
            'source': self.SOURCE_NAME,
            'extraction_method': 'Sectioned HTML parsing',
            'prep_time': '',
            'cook_time': '',
            'total_time': '',
            'servings': '',
            'author': author,
            'cuisine': '',
            'category': '',
        }


class RealFoodDietitiansScraper(BaseScraper):
    """The Real Food Dietitians (therealfooddietitians.com)."""

    BASE_URL = "https://therealfooddietitians.com"
    SOURCE_NAME = "The Real Food Dietitians"
    POST_SITEMAP_URL = "https://therealfooddietitians.com/post-sitemap.xml"

    def __init__(self):
        super().__init__()
        self._init_robots_parser(self.BASE_URL)

    def _post_urls_from_sitemap(self, max_candidates: int = 300) -> List[str]:
        response = self._make_request(self.POST_SITEMAP_URL)
        if not response:
            return []
        try:
            root = ET.fromstring(response.content)
        except ET.ParseError:
            return []

        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = []
        for loc in root.findall('.//sm:loc', ns):
            candidate = (loc.text or '').strip()
            if not candidate or '/wp-' in candidate:
                continue
            # Exclude obvious non-content routes.
            if candidate.rstrip('/') == f"{self.BASE_URL}/blog":
                continue
            if candidate not in urls:
                urls.append(candidate)
            if len(urls) >= max_candidates:
                break
        return urls

    def search_recipes(self, query: str, max_results: int = 12) -> List[Dict]:
        self.reset_diagnostics()
        recipes = []
        query_tokens = [t for t in re.findall(r'[a-z]+', query.lower()) if len(t) >= 3]

        candidates = self._post_urls_from_sitemap(max_candidates=300)
        if query_tokens:
            prioritized = [
                url for url in candidates
                if any(token in url.lower() for token in query_tokens)
            ]
            fallback_pool = [url for url in candidates if url not in prioritized]
            candidate_pool = prioritized + fallback_pool[:40]
        else:
            candidate_pool = candidates

        print(f"[FOUND] The Real Food Dietitians: {len(candidate_pool)} candidate post links")

        for url in candidate_pool:
            if len(recipes) >= max_results:
                break
            recipe_data = self.scrape_recipe(url)
            if recipe_data:
                recipes.append(recipe_data)
                print(f"[OK] The Real Food Dietitians: {recipe_data['title']}")

        return recipes

    def scrape_recipe(self, url: str) -> Optional[Dict]:
        response = self._make_request(url)
        if not response:
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        recipe_data = self._extract_json_ld(soup, self.SOURCE_NAME)
        if recipe_data:
            recipe_data['url'] = url
            recipe_data['scraped_at'] = datetime.now().isoformat()
            recipe_data['extraction_method'] = 'Schema.org JSON-LD'
            return recipe_data
        return None


class OcadoScraper(BaseScraper):
    """Ocado (ocado.com) — uses sitemap for discovery."""

    BASE_URL = "https://www.ocado.com"
    SOURCE_NAME = "Ocado"
    RECIPES_URL = "https://www.ocado.com/recipes"
    RECIPE_SITEMAP_URL = "https://www.ocado.com/sitemaps/sitemap-recipes-part1.xml"

    def __init__(self):
        super().__init__()
        self._init_robots_parser(self.BASE_URL)

    def search_recipes(self, query: str, max_results: int = 12) -> List[Dict]:
        self.reset_diagnostics()
        recipes = []
        query_tokens = [t for t in re.findall(r'[a-z]+', query.lower()) if len(t) >= 3]
        recipe_links = self._recipe_urls_from_sitemap(query_tokens, max_results=max_results)
        if not recipe_links:
            recipe_links = self._recipe_urls_from_homepage(query_tokens, max_results=max_results)

        print(f"[FOUND] Ocado: {len(recipe_links)} recipe links")

        for url in recipe_links:
            recipe_data = self.scrape_recipe(url)
            if recipe_data:
                recipes.append(recipe_data)
                safe_title = recipe_data.get('title', '').encode('ascii', errors='ignore').decode('ascii')
                print(f"[OK] Ocado: {safe_title}")

        return recipes

    def _recipe_urls_from_sitemap(self, query_tokens: List[str], max_results: int = 12) -> List[str]:
        response = self._make_request(self.RECIPE_SITEMAP_URL)
        if not response:
            return []

        try:
            root = ET.fromstring(response.content)
        except ET.ParseError:
            return []

        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        all_urls = []
        for loc in root.findall('.//sm:loc', ns):
            candidate = (loc.text or '').strip()
            if not candidate or '/recipes/' not in candidate.lower():
                continue
            if '/recipes/collections/' in candidate.lower():
                continue
            all_urls.append(candidate)

        if not all_urls:
            return []

        if query_tokens:
            matched = [
                url for url in all_urls
                if any(token in url.lower() for token in query_tokens)
            ]
            if matched:
                return matched[:max_results]

        return all_urls[:max_results]

    def _recipe_urls_from_homepage(self, query_tokens: List[str], max_results: int = 12) -> List[str]:
        response = self._make_request(self.RECIPES_URL)
        if not response:
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        recipe_links = []
        for link in soup.select('a[href]'):
            href = link.get('href', '')
            if not href:
                continue
            full_url = urljoin(self.RECIPES_URL, href)
            lowered = full_url.lower()
            if '/recipes/' not in lowered or '/recipes/collections/' in lowered:
                continue
            path_parts = [part for part in urlparse(full_url).path.split('/') if part]
            if len(path_parts) < 3:
                continue
            if query_tokens and not any(token in lowered for token in query_tokens):
                continue
            if full_url not in recipe_links:
                recipe_links.append(full_url)
            if len(recipe_links) >= max_results:
                break
        return recipe_links

    def scrape_recipe(self, url: str) -> Optional[Dict]:
        response = self._make_request(url)
        if not response:
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        recipe_data = self._extract_json_ld(soup, self.SOURCE_NAME)
        if recipe_data:
            recipe_data['url'] = url
            recipe_data['scraped_at'] = datetime.now().isoformat()
            recipe_data['extraction_method'] = 'Schema.org JSON-LD'
            return recipe_data
        return None


class MultiSourceScraper:
    """Runs searches across all configured sources and merges results."""
    
    def __init__(self):
        self.scrapers = {
            'bbc': BBCFoodScraper(),
            'bbcgoodfood': BBCGoodFoodScraper(),
            'tomkerridge': TomKerridgeScraper(),
            'foodafactoflife': FoodAFactOfLifeScraper(),
            'realfooddietitians': RealFoodDietitiansScraper(),
            'ocado': OcadoScraper(),
        }
        self.source_names = {
            'bbc': 'BBC Food',
            'bbcgoodfood': 'BBC Good Food',
            'tomkerridge': 'Tom Kerridge',
            'foodafactoflife': 'Food - a Fact of Life',
            'realfooddietitians': 'The Real Food Dietitians',
            'ocado': 'Ocado',
        }
        self.last_source_status = {}

    def _build_source_status(self, source_key: str, scraper: BaseScraper, recipe_count: int) -> Dict:
        """Build the status dict for one source, used by the UI to show availability."""
        blocked_statuses = {403, 429}
        had_anti_bot_block = bool(scraper.last_http_status_codes.intersection(blocked_statuses))

        if recipe_count > 0 and not had_anti_bot_block:
            status = 'ok'
            message = 'Source available'
        elif recipe_count > 0 and had_anti_bot_block:
            status = 'partial'
            message = 'Source partially available; some requests were blocked'
        elif scraper.last_blocked_by_robots:
            status = 'unavailable'
            message = 'Source blocked by robots.txt policy'
        elif had_anti_bot_block:
            status = 'temporarily_unavailable'
            message = 'Source temporarily unavailable (anti-bot protection)'
        else:
            status = 'no_results'
            message = 'No matching recipes found from this source'

        return {
            'id': source_key,
            'name': self.source_names.get(source_key, source_key),
            'status': status,
            'message': message,
            'recipes_found': recipe_count,
            'http_statuses': sorted(scraper.last_http_status_codes),
            'fallbacks_used': {
                'external_search': scraper.used_external_fallback,
                'mirror': scraper.used_mirror_fallback,
            }
        }
    
    def search_recipes(self, query: str, max_results: int = 12, sources: List[str] = None) -> List[Dict]:
        """Search all configured sources and return a merged, interleaved recipe list."""
        if sources is None:
            sources = list(self.scrapers.keys())
        
        self.last_source_status = {}
        all_recipes = []
        results_per_source = max(4, max_results // len(sources))
        
        for source_key in sources:
            if source_key in self.scrapers:
                scraper = self.scrapers[source_key]
                print(f"\n[MULTI] Searching {self.source_names[source_key]}...")
                
                try:
                    recipes = scraper.search_recipes(query, max_results=results_per_source)
                    all_recipes.extend(recipes)
                    self.last_source_status[source_key] = self._build_source_status(
                        source_key, scraper, len(recipes)
                    )
                    print(f"[MULTI] Got {len(recipes)} recipes from {self.source_names[source_key]}")
                except Exception as e:
                    print(f"[ERROR] {self.source_names[source_key]} search failed: {e}")
                    self.last_source_status[source_key] = {
                        'id': source_key,
                        'name': self.source_names.get(source_key, source_key),
                        'status': 'error',
                        'message': f"Search failed: {e}",
                        'recipes_found': 0,
                        'http_statuses': [],
                        'fallbacks_used': {
                            'external_search': False,
                            'mirror': False,
                        }
                    }
        
        # Interleave results from different sources for variety
        return self._interleave_results(all_recipes, max_results)

    def get_last_source_status(self) -> Dict:
        """Source status data from the most recent search."""
        return self.last_source_status
    
    def _interleave_results(self, recipes: List[Dict], max_results: int) -> List[Dict]:
        """Interleave results so no single source dominates the top of the list."""
        if not recipes:
            return []
        
        # Group by source
        by_source = {}
        for recipe in recipes:
            source = recipe.get('source', 'Unknown')
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(recipe)
        
        # Interleave
        result = []
        source_lists = list(by_source.values())
        max_len = max(len(lst) for lst in source_lists) if source_lists else 0
        
        for i in range(max_len):
            for source_list in source_lists:
                if i < len(source_list) and len(result) < max_results:
                    result.append(source_list[i])
        
        return result
    
    def get_featured_recipes(self, max_results: int = 8) -> List[Dict]:
        """Homepage recipes from BBC Food."""
        return self.scrapers['bbc'].get_featured_recipes(max_results)
    
    def scrape_recipe(self, url: str) -> Optional[Dict]:
        """Route a recipe URL to the right scraper."""
        if 'bbc.co.uk' in url:
            return self.scrapers['bbc'].scrape_recipe(url)
        elif 'bbcgoodfood.com' in url:
            return self.scrapers['bbcgoodfood'].scrape_recipe(url)
        elif 'tomkerridge.com' in url:
            return self.scrapers['tomkerridge'].scrape_recipe(url)
        elif 'foodafactoflife.org.uk' in url:
            return self.scrapers['foodafactoflife'].scrape_recipe(url)
        elif 'therealfooddietitians.com' in url:
            return self.scrapers['realfooddietitians'].scrape_recipe(url)
        elif 'ocado.com' in url:
            return self.scrapers['ocado'].scrape_recipe(url)
        else:
            return self.scrapers['bbc'].scrape_recipe(url)


