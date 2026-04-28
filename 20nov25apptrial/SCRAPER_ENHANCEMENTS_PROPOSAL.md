# Scraper Enhancement Proposals Based on Chaudhari et al. (2020)

## Key Insight from Chaudhari et al.

> "Different websites employ varying structures and formats for presenting recipe information"

This observation suggests several improvements to make your scraper more **robust, maintainable, and scalable** while maintaining safety-first principles.

---

## Current Architecture Issues

### Problem 1: **Hard-Coded Selectors**
```python
# Current approach - brittle
recipe_cards = soup.find_all('a', class_='card__titleLink')
ingredient_elems = soup.find_all('li', class_='mntl-structured-ingredients__list-item')
```

**Issue:** If website changes CSS classes, scraper breaks completely.

### Problem 2: **Duplicate Logic**
```python
def scrape_allrecipes(self, query, max_results=10):
    # robots.txt check
    # request handling
    # error handling
    
def scrape_bbc_good_food(self, query, max_results=10):
    # robots.txt check (duplicated)
    # request handling (duplicated)
    # error handling (duplicated)
```

**Issue:** Same logic repeated for each source.

### Problem 3: **Limited Adaptability**
- Adding new sources requires writing entire new methods
- No fallback if primary selectors fail
- No validation of extracted data quality

---

## Proposed Enhancements (Chaudhari-Inspired)

## Enhancement 1: **Abstract Source Configuration**

### Concept
Instead of hard-coding selectors in methods, define them in a configuration structure.

### Implementation

```python
class RecipeSourceConfig:
    """Configuration for a recipe website source"""
    
    def __init__(self, name, base_url, search_pattern, selectors):
        self.name = name
        self.base_url = base_url
        self.search_pattern = search_pattern
        self.selectors = selectors

# Define sources as configurations
RECIPE_SOURCES = {
    'allrecipes': RecipeSourceConfig(
        name='AllRecipes',
        base_url='https://www.allrecipes.com',
        search_pattern='/search?q={query}',
        selectors={
            'search_results': [
                {'type': 'a', 'class': 'card__titleLink'},  # Primary
                {'type': 'a', 'class': 'card-link'},        # Fallback 1
                {'type': 'div', 'class': 'card__content'}   # Fallback 2
            ],
            'recipe_title': [
                {'type': 'h1', 'class': 'article-heading'},
                {'type': 'h1', 'class': 'headline'},
                {'type': 'h1', 'id': 'article-heading'}
            ],
            'ingredients': [
                {'type': 'li', 'class': 'mntl-structured-ingredients__list-item'},
                {'type': 'span', 'class': 'ingredients-item-name'},
                {'type': 'li', 'class': 'ingredient'}
            ],
            'instructions': [
                {'type': 'li', 'class': 'mntl-sc-block-group--LI'},
                {'type': 'div', 'class': 'recipe-directions__list--item'},
                {'type': 'p', 'class': 'instruction-text'}
            ],
            'image': [
                {'type': 'img', 'class': 'primary-image__image'},
                {'type': 'img', 'class': 'recipe-image'},
                {'type': 'img', 'property': 'og:image'}
            ]
        }
    ),
    
    'bbc_good_food': RecipeSourceConfig(
        name='BBC Good Food',
        base_url='https://www.bbcgoodfood.com',
        search_pattern='/search?q={query}',
        selectors={
            'search_results': [
                {'type': 'a', 'class': 'link'},
                {'type': 'a', 'class': 'standard-card-new__article-link'}
            ],
            'recipe_title': [
                {'type': 'h1', 'class': 'heading-1'},
                {'type': 'h1', 'class': 'post-header__title'}
            ],
            'ingredients': [
                {'type': 'li', 'class': 'pb-xxs'},
                {'type': 'li', 'class': 'recipe-ingredients__list-item'}
            ],
            'instructions': [
                {'type': 'li', 'class': 'grouped-list__item'},
                {'type': 'li', 'class': 'recipe-method__list-item'}
            ],
            'image': [
                {'type': 'img', 'class': 'image__img'},
                {'type': 'img', 'class': 'img-responsive'}
            ]
        }
    )
}
```

### Benefits
✅ **Easy to update** - Change selectors without touching code  
✅ **Fallback selectors** - Try multiple patterns if first fails  
✅ **Easy to add sources** - Just add new config  
✅ **Maintainable** - Selectors in one place  

---

## Enhancement 2: **Generic Scraping Method with Fallbacks**

### Implementation

```python
def _extract_with_fallback(self, soup, selectors, extract_type='text'):
    """
    Extract data using multiple fallback selectors
    Implements Chaudhari et al.'s approach to handling varying structures
    
    Args:
        soup: BeautifulSoup object
        selectors: List of selector dictionaries to try
        extract_type: 'text', 'attribute', or 'list'
    
    Returns:
        Extracted data or None
    """
    for selector in selectors:
        try:
            if extract_type == 'text':
                elem = soup.find(selector['type'], 
                               class_=selector.get('class'),
                               id=selector.get('id'),
                               attrs=selector.get('attrs', {}))
                if elem:
                    return elem.get_text(strip=True)
                    
            elif extract_type == 'list':
                elems = soup.find_all(selector['type'],
                                     class_=selector.get('class'),
                                     id=selector.get('id'),
                                     attrs=selector.get('attrs', {}))
                if elems:
                    return [elem.get_text(strip=True) for elem in elems if elem.get_text(strip=True)]
                    
            elif extract_type == 'attribute':
                elem = soup.find(selector['type'],
                               class_=selector.get('class'),
                               id=selector.get('id'),
                               attrs=selector.get('attrs', {}))
                if elem:
                    attr_name = selector.get('attribute', 'src')
                    return elem.get(attr_name, '')
                    
        except Exception as e:
            # Try next selector
            continue
    
    return None  # All selectors failed

def _scrape_recipe_generic(self, url, source_config):
    """
    Generic recipe scraper that works with any configured source
    Implements Chaudhari et al.'s multi-stage approach
    """
    try:
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract with fallbacks
        title = self._extract_with_fallback(
            soup, 
            source_config.selectors['recipe_title'],
            'text'
        ) or 'Unknown Recipe'
        
        ingredients = self._extract_with_fallback(
            soup,
            source_config.selectors['ingredients'],
            'list'
        ) or []
        
        instructions = self._extract_with_fallback(
            soup,
            source_config.selectors['instructions'],
            'list'
        ) or []
        
        image_url = self._extract_with_fallback(
            soup,
            source_config.selectors['image'],
            'attribute'
        ) or ''
        
        # Data quality check (Chaudhari's "data cleaning" stage)
        quality_score = self._assess_data_quality(
            title, ingredients, instructions
        )
        
        # Enhanced allergen detection with confidence scoring
        allergens = self.allergen_detector.detect_allergens(ingredients)
        allergen_list = self.allergen_detector.get_allergen_list(ingredients)
        allergen_details = self.allergen_detector.get_allergen_list_with_confidence(ingredients)
        
        return {
            'title': title,
            'url': url,
            'source': source_config.name,
            'ingredients': ingredients,
            'instructions': instructions,
            'image': image_url,
            'allergens': allergens,
            'allergen_list': allergen_list,
            'allergen_details': allergen_details,
            'scraped_at': datetime.now().isoformat(),
            'data_quality': 'live_scrape',
            'data_quality_score': quality_score,  # NEW
            'scraping_method': 'Generic multi-fallback scraper'
        }
        
    except Exception as e:
        print(f"Error scraping recipe detail: {e}")
        return None
```

### Benefits
✅ **Single method for all sources** - No duplication  
✅ **Automatic fallbacks** - Tries multiple selectors  
✅ **Easier to maintain** - Fix once, works everywhere  
✅ **Data quality tracking** - Know which extractions succeeded  

---

## Enhancement 3: **Data Quality Assessment**

### Concept
Chaudhari et al. emphasize "data cleaning to standardise extracted information." We should **assess quality** of scraped data.

### Implementation

```python
def _assess_data_quality(self, title, ingredients, instructions):
    """
    Assess quality of scraped data
    Returns score 0-1 indicating completeness and reliability
    
    Implements Chaudhari et al.'s data cleaning stage concept
    """
    score = 0.0
    max_score = 5.0
    
    # Title check
    if title and title != 'Unknown Recipe' and len(title) > 5:
        score += 1.0
    
    # Ingredients check
    if ingredients and len(ingredients) >= 3:
        score += 1.5
        # Bonus for detailed ingredients
        if any(any(char.isdigit() for char in ing) for ing in ingredients):
            score += 0.5  # Has measurements
    
    # Instructions check
    if instructions and len(instructions) >= 2:
        score += 1.0
        # Bonus for detailed instructions
        if any(len(inst) > 20 for inst in instructions):
            score += 0.5  # Has detailed steps
    
    # Ingredient quality check
    if ingredients:
        avg_length = sum(len(ing) for ing in ingredients) / len(ingredients)
        if avg_length > 10:  # Detailed ingredients
            score += 0.5
    
    return min(score / max_score, 1.0)

def _should_include_recipe(self, recipe_data, min_quality=0.6):
    """
    Decide if scraped recipe meets quality threshold
    Conservative approach for safety
    """
    if not recipe_data:
        return False
    
    quality = recipe_data.get('data_quality_score', 0)
    
    # Require minimum quality
    if quality < min_quality:
        print(f"⚠️ Recipe quality too low ({quality:.2f}): {recipe_data['title']}")
        return False
    
    # Require ingredients for allergen detection
    if not recipe_data.get('ingredients'):
        print(f"⚠️ No ingredients found: {recipe_data['title']}")
        return False
    
    # Require minimum number of ingredients
    if len(recipe_data.get('ingredients', [])) < 2:
        print(f"⚠️ Too few ingredients: {recipe_data['title']}")
        return False
    
    return True
```

### Benefits
✅ **Filter poor quality data** - Don't show incomplete recipes  
✅ **Safety-focused** - Require ingredients for allergen detection  
✅ **Transparent** - Users see quality scores  
✅ **Conservative** - Exclude uncertain data  

---

## Enhancement 4: **Structured Data Extraction (Schema.org)**

### Concept
Many recipe sites use Schema.org structured data. This is **more reliable** than HTML scraping.

### Implementation

```python
def _extract_structured_data(self, soup):
    """
    Extract recipe data from Schema.org JSON-LD
    More reliable than HTML parsing (Chaudhari et al.'s standardization)
    
    Returns:
        dict or None
    """
    try:
        # Find JSON-LD script tags
        scripts = soup.find_all('script', type='application/ld+json')
        
        for script in scripts:
            try:
                data = json.loads(script.string)
                
                # Handle single object or array
                if isinstance(data, list):
                    data = next((d for d in data if d.get('@type') == 'Recipe'), None)
                
                if data and data.get('@type') == 'Recipe':
                    return {
                        'title': data.get('name', ''),
                        'ingredients': data.get('recipeIngredient', []),
                        'instructions': self._parse_instructions(data.get('recipeInstructions', [])),
                        'image': self._get_image_url(data.get('image')),
                        'source_type': 'structured_data',
                        'data_quality_score': 0.95  # Structured data is high quality
                    }
            except json.JSONDecodeError:
                continue
                
    except Exception as e:
        print(f"Error extracting structured data: {e}")
    
    return None

def _parse_instructions(self, instructions):
    """Parse instructions from various Schema.org formats"""
    if isinstance(instructions, str):
        return [instructions]
    elif isinstance(instructions, list):
        result = []
        for inst in instructions:
            if isinstance(inst, str):
                result.append(inst)
            elif isinstance(inst, dict):
                result.append(inst.get('text', ''))
        return result
    return []

def _get_image_url(self, image_data):
    """Extract image URL from various Schema.org formats"""
    if isinstance(image_data, str):
        return image_data
    elif isinstance(image_data, dict):
        return image_data.get('url', '')
    elif isinstance(image_data, list) and image_data:
        return self._get_image_url(image_data[0])
    return ''

def _scrape_recipe_enhanced(self, url, source_config):
    """
    Enhanced scraper that tries structured data first, then HTML
    Implements Chaudhari et al.'s approach to handling varying formats
    """
    try:
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try structured data first (most reliable)
        structured = self._extract_structured_data(soup)
        
        if structured and structured.get('ingredients'):
            recipe_data = structured
            recipe_data['scraping_method'] = 'Schema.org structured data (high reliability)'
        else:
            # Fall back to HTML scraping
            recipe_data = self._scrape_recipe_generic(url, source_config)
            if recipe_data:
                recipe_data['scraping_method'] = 'HTML parsing with fallbacks (medium reliability)'
        
        # Add allergen detection
        if recipe_data and recipe_data.get('ingredients'):
            ingredients = recipe_data['ingredients']
            recipe_data['allergens'] = self.allergen_detector.detect_allergens(ingredients)
            recipe_data['allergen_list'] = self.allergen_detector.get_allergen_list(ingredients)
            recipe_data['allergen_details'] = self.allergen_detector.get_allergen_list_with_confidence(ingredients)
            recipe_data['source'] = source_config.name
            recipe_data['scraped_at'] = datetime.now().isoformat()
        
        return recipe_data
        
    except Exception as e:
        print(f"Error in enhanced scraper: {e}")
        return None
```

### Benefits
✅ **More reliable** - Structured data less likely to change  
✅ **Better quality** - Standardized format  
✅ **Automatic fallback** - HTML scraping if structured data unavailable  
✅ **Transparency** - Users know data source type  

---

## Enhancement 5: **Intelligent Source Selection**

### Concept
Track which sources provide best quality data and prioritize them.

### Implementation

```python
class RecipeScraper:
    def __init__(self):
        self.headers = {...}
        self.allergen_detector = AllergenDetector()
        self.robots_cache = {}
        
        # NEW: Track source performance
        self.source_stats = {
            'allrecipes': {'success': 0, 'failure': 0, 'avg_quality': 0.0},
            'bbc_good_food': {'success': 0, 'failure': 0, 'avg_quality': 0.0}
        }
    
    def _update_source_stats(self, source_name, success, quality_score=None):
        """Track source performance over time"""
        if source_name not in self.source_stats:
            self.source_stats[source_name] = {
                'success': 0, 'failure': 0, 'avg_quality': 0.0, 'total_quality': 0.0
            }
        
        stats = self.source_stats[source_name]
        
        if success:
            stats['success'] += 1
            if quality_score:
                stats['total_quality'] += quality_score
                stats['avg_quality'] = stats['total_quality'] / stats['success']
        else:
            stats['failure'] += 1
    
    def _get_source_priority(self):
        """
        Get sources ordered by reliability
        Implements adaptive scraping based on performance
        """
        sources = []
        for name, stats in self.source_stats.items():
            total = stats['success'] + stats['failure']
            if total > 0:
                success_rate = stats['success'] / total
                score = (success_rate * 0.6) + (stats['avg_quality'] * 0.4)
                sources.append((name, score))
        
        # Sort by score (highest first)
        sources.sort(key=lambda x: x[1], reverse=True)
        return [name for name, score in sources]
    
    def search_recipes_adaptive(self, query, max_results=15):
        """
        Adaptive scraping that prioritizes reliable sources
        Implements Chaudhari et al.'s insight about varying quality
        """
        all_recipes = []
        scraping_errors = []
        
        # Get sources ordered by reliability
        source_priority = self._get_source_priority() or ['allrecipes', 'bbc_good_food']
        
        print(f"🔍 Searching '{query}' (source priority: {source_priority})")
        
        for source_name in source_priority:
            if len(all_recipes) >= max_results:
                break
            
            try:
                source_config = RECIPE_SOURCES.get(source_name)
                if not source_config:
                    continue
                
                recipes = self._scrape_source(query, source_config, max_results - len(all_recipes))
                
                # Track performance
                for recipe in recipes:
                    quality = recipe.get('data_quality_score', 0)
                    self._update_source_stats(source_name, True, quality)
                
                all_recipes.extend(recipes)
                print(f"✓ {source_config.name}: Found {len(recipes)} recipes (avg quality: {sum(r.get('data_quality_score', 0) for r in recipes) / len(recipes) if recipes else 0:.2f})")
                
            except Exception as e:
                error_msg = f"{source_name} scraping failed: {str(e)}"
                print(f"✗ {error_msg}")
                scraping_errors.append(error_msg)
                self._update_source_stats(source_name, False)
        
        # Fallback to mock data if needed
        if len(all_recipes) == 0:
            print("⚠️ All sources failed, using mock data...")
            all_recipes.extend(self.get_mock_recipes(query, max_results))
        
        return all_recipes[:max_results]
```

### Benefits
✅ **Learns over time** - Prioritizes reliable sources  
✅ **Adaptive** - Adjusts to source availability  
✅ **Efficient** - Tries best sources first  
✅ **Transparent** - Reports source performance  

---

## Enhancement 6: **Parallel Scraping with Timeouts**

### Concept
Scrape multiple sources simultaneously to improve speed.

### Implementation

```python
import concurrent.futures
import threading

def _scrape_source_with_timeout(self, query, source_config, max_results, timeout=10):
    """Scrape a single source with timeout"""
    try:
        return self._scrape_source(query, source_config, max_results)
    except Exception as e:
        print(f"✗ {source_config.name} failed: {e}")
        return []

def search_recipes_parallel(self, query, max_results=15, timeout=15):
    """
    Scrape multiple sources in parallel
    Faster response time while maintaining safety
    """
    all_recipes = []
    
    # Create thread pool
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit scraping tasks
        futures = {}
        for source_name, source_config in RECIPE_SOURCES.items():
            future = executor.submit(
                self._scrape_source_with_timeout,
                query,
                source_config,
                max_results // len(RECIPE_SOURCES),
                timeout
            )
            futures[future] = source_name
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(futures, timeout=timeout):
            source_name = futures[future]
            try:
                recipes = future.result()
                all_recipes.extend(recipes)
                print(f"✓ {source_name}: {len(recipes)} recipes")
            except Exception as e:
                print(f"✗ {source_name} failed: {e}")
    
    return all_recipes[:max_results]
```

### Benefits
✅ **Faster** - Parallel execution  
✅ **Timeout protection** - Don't wait forever  
✅ **Maintains safety** - Each source isolated  
✅ **Better UX** - Quicker results  

---

## Enhancement 7: **Caching Layer**

### Concept
Cache scraped recipes to reduce load on source websites and improve speed.

### Implementation

```python
import hashlib
import pickle
from pathlib import Path

class RecipeCache:
    """Simple file-based cache for scraped recipes"""
    
    def __init__(self, cache_dir='recipe_cache', max_age_hours=24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.max_age = max_age_hours * 3600  # Convert to seconds
    
    def _get_cache_key(self, url):
        """Generate cache key from URL"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def get(self, url):
        """Retrieve cached recipe if available and fresh"""
        cache_key = self._get_cache_key(url)
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        if not cache_file.exists():
            return None
        
        # Check age
        age = time.time() - cache_file.stat().st_mtime
        if age > self.max_age:
            cache_file.unlink()  # Delete stale cache
            return None
        
        try:
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        except Exception:
            return None
    
    def set(self, url, recipe_data):
        """Cache recipe data"""
        cache_key = self._get_cache_key(url)
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(recipe_data, f)
        except Exception as e:
            print(f"Cache write failed: {e}")

# In RecipeScraper.__init__:
self.cache = RecipeCache(max_age_hours=24)

# In scraping methods:
def _scrape_recipe_cached(self, url, source_config):
    """Scrape with caching"""
    # Check cache first
    cached = self.cache.get(url)
    if cached:
        print(f"✓ Using cached data for {url}")
        cached['data_quality'] = 'cached'
        return cached
    
    # Scrape if not cached
    recipe_data = self._scrape_recipe_enhanced(url, source_config)
    
    # Cache successful scrapes
    if recipe_data and self._should_include_recipe(recipe_data):
        self.cache.set(url, recipe_data)
    
    return recipe_data
```

### Benefits
✅ **Faster** - No repeated scraping  
✅ **Ethical** - Reduces load on source websites  
✅ **Reliable** - Works even if source is down  
✅ **Configurable** - Adjustable cache duration  

---

## Summary of Enhancements

### Inspired by Chaudhari et al. (2020):

| Enhancement | Chaudhari Principle | Benefit |
|-------------|-------------------|---------|
| **1. Source Configuration** | Varying structures | Easy maintenance, fallbacks |
| **2. Generic Scraping** | Standardization | Single method, no duplication |
| **3. Quality Assessment** | Data cleaning | Filter poor data, safety-first |
| **4. Structured Data** | Standardization | More reliable extraction |
| **5. Adaptive Selection** | Source reliability | Learn over time, prioritize best |
| **6. Parallel Scraping** | Efficiency | Faster results, better UX |
| **7. Caching** | Efficiency | Reduce load, improve speed |

---

## Implementation Priority

### HIGH PRIORITY (Safety & Reliability):
1. ✅ **Quality Assessment** - Filter poor data
2. ✅ **Structured Data Extraction** - More reliable
3. ✅ **Generic Scraping with Fallbacks** - Robust extraction

### MEDIUM PRIORITY (Maintainability):
4. ✅ **Source Configuration** - Easier updates
5. ✅ **Adaptive Selection** - Learn from performance

### LOWER PRIORITY (Performance):
6. ✅ **Caching** - Speed improvement
7. ✅ **Parallel Scraping** - Faster results

---

## Next Steps

1. **Start with Quality Assessment** - Add data quality scoring
2. **Implement Structured Data** - Try Schema.org first
3. **Refactor to Generic Method** - Reduce code duplication
4. **Add Source Configuration** - Make selectors configurable
5. **Test thoroughly** - Ensure safety not compromised

Would you like me to implement any of these enhancements?

