"""
Recipe scraper for allergen-filtered recipe search
MSc Web Development Project

Ethical scraping practices:
- Respects robots.txt
- Rate limiting
- Clear user agent
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import json
from datetime import datetime
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from allergen_detector import AllergenDetector
from typing import List, Dict, Optional


class RecipeScraper:
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Educational Recipe Scraper/1.0 (MSc Web Development Project; Allergen Filter Tool; Educational Purpose)'
        }
        self.allergen_detector = AllergenDetector()
        self.robots_cache = {}
    
    def check_robots_txt(self, url):
        # Check robots.txt before scraping
        try:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            if base_url in self.robots_cache:
                rp = self.robots_cache[base_url]
            else:
                rp = RobotFileParser()
                robots_url = f"{base_url}/robots.txt"
                rp.set_url(robots_url)
                
                try:
                    rp.read()
                    self.robots_cache[base_url] = rp
                    print(f"✓ Checked robots.txt for {base_url}")
                except Exception:
                    print(f"⚠ No robots.txt found for {base_url}, proceeding cautiously")
                    return True
            
            user_agent = self.headers.get('User-Agent', '*')
            can_fetch = rp.can_fetch(user_agent, url)
            
            if not can_fetch:
                print(f"✗ robots.txt disallows scraping: {url}")
            
            return can_fetch
            
        except Exception as e:
            print(f"⚠ Error checking robots.txt: {e}")
            return True
    
    def get_crawl_delay(self, url):
        # Get crawl delay from robots.txt or use default
        try:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            if base_url in self.robots_cache:
                rp = self.robots_cache[base_url]
                crawl_delay = rp.crawl_delay(self.headers.get('User-Agent', '*'))
                if crawl_delay:
                    return float(crawl_delay)
            
            return 0.5  # Default minimum delay
            
        except Exception as e:
            print(f"⚠ Error getting crawl delay: {e}")
            return 0.5
    
    def _assess_quality(self, title, ingredients, instructions):
        # Score data completeness (0-1)
        score = 0.0
        
        if title and title != 'Unknown Recipe' and len(title) > 5:
            score += 0.2
        
        if ingredients and len(ingredients) >= 3:
            score += 0.3
            # Bonus for measurements
            if any(any(c.isdigit() for c in ing) for ing in ingredients):
                score += 0.1
        
        if instructions and len(instructions) >= 2:
            score += 0.2
            if any(len(inst) > 20 for inst in instructions):
                score += 0.1
        
        if ingredients:
            avg_len = sum(len(ing) for ing in ingredients) / len(ingredients)
            if avg_len > 10:
                score += 0.1
        
        return min(score, 1.0)
    
    def _try_structured_data(self, soup):
        # Try Schema.org JSON-LD first (more reliable)
        try:
            scripts = soup.find_all('script', type='application/ld+json')
            
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    
                    # Handle both single objects and arrays
                    if isinstance(data, list):
                        data = next((d for d in data if d.get('@type') == 'Recipe'), None)
                    
                    if data and data.get('@type') == 'Recipe':
                        instructions = []
                        raw_instructions = data.get('recipeInstructions', [])
                        
                        if isinstance(raw_instructions, str):
                            instructions = [raw_instructions]
                        elif isinstance(raw_instructions, list):
                            for inst in raw_instructions:
                                if isinstance(inst, str):
                                    instructions.append(inst)
                                elif isinstance(inst, dict):
                                    instructions.append(inst.get('text', ''))
                        
                        image = ''
                        img_data = data.get('image')
                        if isinstance(img_data, str):
                            image = img_data
                        elif isinstance(img_data, dict):
                            image = img_data.get('url', '')
                        elif isinstance(img_data, list) and img_data:
                            if isinstance(img_data[0], str):
                                image = img_data[0]
                            elif isinstance(img_data[0], dict):
                                image = img_data[0].get('url', '')
                        
                        return {
                            'title': data.get('name', ''),
                            'ingredients': data.get('recipeIngredient', []),
                            'instructions': instructions,
                            'image': image,
                            'from_structured': True
                        }
                except (json.JSONDecodeError, AttributeError):
                    continue
        except Exception as e:
            pass
        
        return None
    
    def scrape_allrecipes(self, query, max_results=10):
        recipes = []
        
        try:
            search_url = f"https://www.allrecipes.com/search?q={query.replace(' ', '+')}"
            
            if not self.check_robots_txt(search_url):
                print("⚠ AllRecipes scraping blocked by robots.txt")
                return recipes
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            recipe_cards = soup.find_all('a', class_='card__titleLink', limit=max_results)
            
            for card in recipe_cards[:max_results]:
                try:
                    title = card.get_text(strip=True)
                    url = card.get('href', '')
                    
                    if url and title:
                        if self.check_robots_txt(url):
                            recipe_data = self._scrape_allrecipes_detail(url)
                            if recipe_data:
                                recipes.append(recipe_data)
                        else:
                            print(f"⚠ Skipping {title} - blocked by robots.txt")
                    
                    delay = max(self.get_crawl_delay(url), random.uniform(0.5, 1.0))
                    time.sleep(delay)
                    
                except Exception as e:
                    print(f"Error scraping recipe card: {e}")
                    continue
        
        except Exception as e:
            print(f"Error scraping AllRecipes: {e}")
        
        return recipes
    
    def _scrape_allrecipes_detail(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try structured data first
            structured = self._try_structured_data(soup)
            
            if structured and structured.get('ingredients'):
                title = structured['title']
                ingredients = structured['ingredients']
                instructions = structured['instructions']
                image_url = structured['image']
                method = 'Schema.org structured data'
            else:
                # Fall back to HTML
                title_elem = soup.find('h1', class_='article-heading')
                title = title_elem.get_text(strip=True) if title_elem else 'Unknown Recipe'
                
                ingredients = []
                ingredient_elems = soup.find_all('li', class_='mntl-structured-ingredients__list-item')
                for ing in ingredient_elems:
                    ingredient_text = ing.get_text(strip=True)
                    if ingredient_text:
                        ingredients.append(ingredient_text)
                
                instructions = []
                instruction_elems = soup.find_all('li', class_='mntl-sc-block-group--LI')
                for inst in instruction_elems:
                    instruction_text = inst.get_text(strip=True)
                    if instruction_text:
                        instructions.append(instruction_text)
                
                image_url = ''
                image_elem = soup.find('img', class_='primary-image__image')
                if image_elem:
                    image_url = image_elem.get('src', '')
                
                method = 'HTML parsing'
            
            quality = self._assess_quality(title, ingredients, instructions)
            
            # Skip low quality or missing ingredients
            if quality < 0.5 or not ingredients or len(ingredients) < 2:
                print(f"⚠ Skipping low quality recipe: {title} (quality: {quality:.2f})")
                return None
            
            allergens = self.allergen_detector.detect_allergens(ingredients)
            allergen_list = self.allergen_detector.get_allergen_list(ingredients)
            allergen_details = self.allergen_detector.get_allergen_list_with_confidence(ingredients)
            
            return {
                'title': title,
                'url': url,
                'source': 'AllRecipes',
                'ingredients': ingredients,
                'instructions': instructions,
                'image': image_url,
                'allergens': allergens,
                'allergen_list': allergen_list,
                'allergen_details': allergen_details,
                'scraped_at': datetime.now().isoformat(),
                'data_quality': 'live_scrape',
                'quality_score': quality,
                'scraping_method': method
            }
        
        except Exception as e:
            print(f"Error scraping recipe detail: {e}")
            return None
    
    def scrape_bbc_good_food(self, query, max_results=10):
        recipes = []
        
        try:
            search_url = f"https://www.bbcgoodfood.com/search?q={query.replace(' ', '+')}"
            
            if not self.check_robots_txt(search_url):
                print("⚠ BBC Good Food scraping blocked by robots.txt")
                return recipes
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            recipe_links = soup.find_all('a', class_='link', limit=max_results * 2)
            
            count = 0
            for link in recipe_links:
                if count >= max_results:
                    break
                
                try:
                    url = link.get('href', '')
                    if url and '/recipes/' in url:
                        if not url.startswith('http'):
                            url = 'https://www.bbcgoodfood.com' + url
                        
                        if self.check_robots_txt(url):
                            recipe_data = self._scrape_bbc_detail(url)
                            if recipe_data:
                                recipes.append(recipe_data)
                                count += 1
                        else:
                            print(f"⚠ Skipping recipe - blocked by robots.txt")
                        
                        delay = max(self.get_crawl_delay(url), random.uniform(0.5, 1.0))
                        time.sleep(delay)
                
                except Exception as e:
                    print(f"Error scraping BBC recipe: {e}")
                    continue
        
        except Exception as e:
            print(f"Error scraping BBC Good Food: {e}")
        
        return recipes
    
    def _scrape_bbc_detail(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try structured data first
            structured = self._try_structured_data(soup)
            
            if structured and structured.get('ingredients'):
                title = structured['title']
                ingredients = structured['ingredients']
                instructions = structured['instructions']
                image_url = structured['image']
                method = 'Schema.org structured data'
            else:
                # Fall back to HTML
                title_elem = soup.find('h1', class_='heading-1')
                title = title_elem.get_text(strip=True) if title_elem else 'Unknown Recipe'
                
                ingredients = []
                ingredient_elems = soup.find_all('li', class_='pb-xxs')
                for ing in ingredient_elems:
                    ingredient_text = ing.get_text(strip=True)
                    if ingredient_text:
                        ingredients.append(ingredient_text)
                
                instructions = []
                instruction_elems = soup.find_all('li', class_='grouped-list__item')
                for inst in instruction_elems:
                    instruction_text = inst.get_text(strip=True)
                    if instruction_text and len(instruction_text) > 20:
                        instructions.append(instruction_text)
                
                image_url = ''
                image_elem = soup.find('img', class_='image__img')
                if image_elem:
                    image_url = image_elem.get('src', '')
                
                method = 'HTML parsing'
            
            quality = self._assess_quality(title, ingredients, instructions)
            
            if quality < 0.5 or not ingredients or len(ingredients) < 2:
                print(f"⚠ Skipping low quality recipe: {title} (quality: {quality:.2f})")
                return None
            
            allergens = self.allergen_detector.detect_allergens(ingredients)
            allergen_list = self.allergen_detector.get_allergen_list(ingredients)
            allergen_details = self.allergen_detector.get_allergen_list_with_confidence(ingredients)
            
            return {
                'title': title,
                'url': url,
                'source': 'BBC Good Food',
                'ingredients': ingredients,
                'instructions': instructions,
                'image': image_url,
                'allergens': allergens,
                'allergen_list': allergen_list,
                'allergen_details': allergen_details,
                'scraped_at': datetime.now().isoformat(),
                'data_quality': 'live_scrape',
                'quality_score': quality,
                'scraping_method': method
            }
        
        except Exception as e:
            print(f"Error scraping BBC recipe detail: {e}")
            return None
    
    def get_mock_recipes(self, query, max_results=15):
        # Fallback data for testing/demo
        mock_recipes_data = [
            {
                'title': f'Grilled {query.title()} Salad',
                'ingredients': ['lettuce', 'tomatoes', 'cucumber', 'olive oil', 'lemon juice', 'salt', 'pepper', query.lower()],
                'instructions': [
                    f'Wash and chop all vegetables',
                    f'Grill the {query.lower()} until cooked through',
                    'Mix vegetables in a large bowl',
                    'Drizzle with olive oil and lemon juice',
                    'Season with salt and pepper',
                    'Serve fresh'
                ],
                'image': 'https://placehold.co/400x300/e8f5e9/2e7d32?text=Grilled+Salad',
                'source': 'Demo Recipe',
                'data_quality': 'mock_data',
                'quality_score': 0.85
            },
            {
                'title': f'Creamy {query.title()} Pasta',
                'ingredients': ['pasta', 'cream', 'butter', 'garlic', 'parmesan cheese', 'salt', 'pepper', query.lower()],
                'instructions': [
                    'Cook pasta according to package directions',
                    f'Sauté {query.lower()} with garlic in butter',
                    'Add cream and simmer',
                    'Toss with cooked pasta',
                    'Top with parmesan cheese',
                    'Serve hot'
                ],
                'image': 'https://placehold.co/400x300/fff3e0/e65100?text=Creamy+Pasta',
                'source': 'Demo Recipe',
                'quality_score': 0.85
            },
            {
                'title': f'Spicy {query.title()} Stir-Fry',
                'ingredients': ['bell peppers', 'onions', 'soy sauce', 'ginger', 'garlic', 'chili flakes', 'rice', query.lower()],
                'instructions': [
                    'Cook rice according to package directions',
                    'Heat oil in a wok or large pan',
                    f'Stir-fry {query.lower()} until cooked',
                    'Add vegetables and stir-fry',
                    'Add soy sauce and seasonings',
                    'Serve over rice'
                ],
                'image': 'https://placehold.co/400x300/ffebee/c62828?text=Spicy+Stir-Fry',
                'source': 'Demo Recipe',
                'quality_score': 0.85
            },
            {
                'title': f'Baked {query.title()} with Herbs',
                'ingredients': ['olive oil', 'rosemary', 'thyme', 'garlic', 'lemon', 'salt', 'pepper', query.lower()],
                'instructions': [
                    'Preheat oven to 375°F (190°C)',
                    f'Season {query.lower()} with herbs and spices',
                    'Drizzle with olive oil',
                    'Bake for 25-30 minutes',
                    'Squeeze lemon juice over top',
                    'Serve with your favorite sides'
                ],
                'image': 'https://placehold.co/400x300/f1f8e9/558b2f?text=Baked+Herbs',
                'source': 'Demo Recipe',
                'quality_score': 0.85
            },
            {
                'title': f'{query.title()} Soup',
                'ingredients': ['vegetable broth', 'carrots', 'celery', 'onions', 'potatoes', 'bay leaves', 'salt', 'pepper', query.lower()],
                'instructions': [
                    'Sauté onions, carrots, and celery',
                    f'Add {query.lower()} and cook briefly',
                    'Pour in vegetable broth',
                    'Add potatoes and bay leaves',
                    'Simmer for 30 minutes',
                    'Season and serve hot'
                ],
                'image': 'https://placehold.co/400x300/e3f2fd/1565c0?text=Soup',
                'source': 'Demo Recipe',
                'quality_score': 0.85
            },
            {
                'title': f'{query.title()} Tacos',
                'ingredients': ['corn tortillas', 'avocado', 'cilantro', 'lime', 'onions', 'salsa', 'salt', query.lower()],
                'instructions': [
                    f'Cook {query.lower()} with your favorite seasonings',
                    'Warm tortillas',
                    'Fill tortillas with cooked ingredients',
                    'Top with avocado, cilantro, and onions',
                    'Squeeze lime juice over top',
                    'Serve with salsa'
                ],
                'image': 'https://placehold.co/400x300/fff8e1/f57f17?text=Tacos',
                'source': 'Demo Recipe',
                'quality_score': 0.85
            },
            {
                'title': f'Roasted {query.title()} Bowl',
                'ingredients': ['quinoa', 'sweet potatoes', 'kale', 'chickpeas', 'tahini', 'lemon', 'olive oil', query.lower()],
                'instructions': [
                    'Cook quinoa according to package directions',
                    'Roast sweet potatoes and chickpeas',
                    f'Cook {query.lower()} to preference',
                    'Massage kale with olive oil',
                    'Assemble bowl with all ingredients',
                    'Drizzle with tahini dressing'
                ],
                'image': 'https://placehold.co/400x300/fce4ec/880e4f?text=Bowl',
                'source': 'Demo Recipe',
                'quality_score': 0.85
            },
            {
                'title': f'{query.title()} Curry',
                'ingredients': ['coconut milk', 'curry paste', 'onions', 'garlic', 'ginger', 'vegetables', 'rice', query.lower()],
                'instructions': [
                    'Cook rice according to package directions',
                    'Sauté onions, garlic, and ginger',
                    'Add curry paste and cook',
                    f'Add {query.lower()} and vegetables',
                    'Pour in coconut milk and simmer',
                    'Serve over rice'
                ],
                'image': 'https://placehold.co/400x300/fff9c4/f9a825?text=Curry',
                'source': 'Demo Recipe',
                'quality_score': 0.85
            },
            {
                'title': f'Mediterranean {query.title()}',
                'ingredients': ['olives', 'feta cheese', 'tomatoes', 'cucumbers', 'red onion', 'olive oil', 'oregano', query.lower()],
                'instructions': [
                    f'Prepare {query.lower()} as desired',
                    'Chop all vegetables',
                    'Combine in a bowl',
                    'Crumble feta cheese on top',
                    'Drizzle with olive oil',
                    'Sprinkle with oregano and serve'
                ],
                'image': 'https://placehold.co/400x300/e0f2f1/00695c?text=Mediterranean',
                'source': 'Demo Recipe',
                'quality_score': 0.85
            },
            {
                'title': f'{query.title()} Sandwich',
                'ingredients': ['bread', 'lettuce', 'tomatoes', 'mayonnaise', 'mustard', 'cheese', 'pickles', query.lower()],
                'instructions': [
                    f'Cook {query.lower()} to preference',
                    'Toast bread slices',
                    'Spread mayonnaise and mustard',
                    'Layer with lettuce, tomatoes, and cheese',
                    f'Add {query.lower()}',
                    'Top with second bread slice and serve'
                ],
                'image': 'https://placehold.co/400x300/efebe9/5d4037?text=Sandwich',
                'source': 'Demo Recipe',
                'quality_score': 0.85
            },
            {
                'title': f'BBQ {query.title()}',
                'ingredients': ['bbq sauce', 'brown sugar', 'garlic powder', 'onion powder', 'paprika', 'salt', 'pepper', query.lower()],
                'instructions': [
                    'Mix dry seasonings together',
                    f'Season {query.lower()} with spice mix',
                    'Grill or bake until nearly done',
                    'Brush with BBQ sauce',
                    'Continue cooking until caramelized',
                    'Serve with coleslaw'
                ],
                'image': 'https://placehold.co/400x300/fbe9e7/bf360c?text=BBQ',
                'source': 'Demo Recipe',
                'quality_score': 0.85
            },
            {
                'title': f'{query.title()} Fried Rice',
                'ingredients': ['rice', 'eggs', 'peas', 'carrots', 'soy sauce', 'sesame oil', 'green onions', query.lower()],
                'instructions': [
                    'Cook rice and let cool',
                    'Scramble eggs and set aside',
                    f'Stir-fry {query.lower()} until cooked',
                    'Add vegetables and cook',
                    'Add rice and soy sauce',
                    'Mix in eggs and green onions'
                ],
                'image': 'https://placehold.co/400x300/fffde7/f57f17?text=Fried+Rice',
                'source': 'Demo Recipe',
                'quality_score': 0.85
            },
            {
                'title': f'Stuffed {query.title()}',
                'ingredients': ['bell peppers', 'rice', 'tomato sauce', 'onions', 'garlic', 'cheese', 'herbs', query.lower()],
                'instructions': [
                    'Preheat oven to 375°F (190°C)',
                    'Cut tops off bell peppers and remove seeds',
                    f'Mix cooked rice with {query.lower()} and seasonings',
                    'Stuff peppers with mixture',
                    'Top with cheese and tomato sauce',
                    'Bake for 30-35 minutes'
                ],
                'image': 'https://placehold.co/400x300/e8eaf6/3f51b5?text=Stuffed',
                'source': 'Demo Recipe',
                'quality_score': 0.85
            },
            {
                'title': f'{query.title()} Casserole',
                'ingredients': ['pasta', 'cream of mushroom soup', 'milk', 'cheese', 'breadcrumbs', 'butter', 'vegetables', query.lower()],
                'instructions': [
                    'Preheat oven to 350°F (175°C)',
                    'Cook pasta according to package directions',
                    f'Mix pasta with {query.lower()}, soup, and milk',
                    'Pour into baking dish',
                    'Top with cheese and breadcrumbs',
                    'Bake for 25-30 minutes until bubbly'
                ],
                'image': 'https://placehold.co/400x300/f3e5f5/7b1fa2?text=Casserole',
                'source': 'Demo Recipe',
                'quality_score': 0.85
            },
            {
                'title': f'Grilled {query.title()} Skewers',
                'ingredients': ['bell peppers', 'onions', 'cherry tomatoes', 'olive oil', 'lemon juice', 'herbs', 'salt', query.lower()],
                'instructions': [
                    f'Cut {query.lower()} and vegetables into chunks',
                    'Thread onto skewers alternating ingredients',
                    'Brush with olive oil and lemon juice',
                    'Season with herbs and salt',
                    'Grill until cooked through',
                    'Serve hot with rice or salad'
                ],
                'image': 'https://placehold.co/400x300/fce4ec/c2185b?text=Skewers',
                'source': 'Demo Recipe',
                'quality_score': 0.85
            }
        ]
        
        recipes = []
        for recipe_data in mock_recipes_data[:max_results]:
            allergens = self.allergen_detector.detect_allergens(recipe_data['ingredients'])
            allergen_list = self.allergen_detector.get_allergen_list(recipe_data['ingredients'])
            allergen_details = self.allergen_detector.get_allergen_list_with_confidence(recipe_data['ingredients'])
            
            recipe_data['allergens'] = allergens
            recipe_data['allergen_list'] = allergen_list
            recipe_data['allergen_details'] = allergen_details
            recipe_data['url'] = '#'
            recipe_data['scraped_at'] = datetime.now().isoformat()
            recipe_data['scraping_method'] = 'Mock data (fallback)'
            recipe_data['data_quality'] = 'mock_data'
            
            recipes.append(recipe_data)
        
        return recipes
    
    def search_recipes(self, query, max_results=15):
        all_recipes = []
        scraping_errors = []
        
        print(f"🔍 Searching for '{query}'...")
        
        try:
            allrecipes_results = self.scrape_allrecipes(query, max_results // 2)
            all_recipes.extend(allrecipes_results)
            print(f"✓ AllRecipes: Found {len(allrecipes_results)} recipes")
        except Exception as e:
            error_msg = f"AllRecipes scraping failed: {str(e)}"
            print(f"✗ {error_msg}")
            scraping_errors.append(error_msg)
        
        try:
            bbc_results = self.scrape_bbc_good_food(query, max_results // 2)
            all_recipes.extend(bbc_results)
            print(f"✓ BBC Good Food: Found {len(bbc_results)} recipes")
        except Exception as e:
            error_msg = f"BBC Good Food scraping failed: {str(e)}"
            print(f"✗ {error_msg}")
            scraping_errors.append(error_msg)
        
        if len(all_recipes) == 0:
            print("⚠️ Real scraping returned no results, using mock data as fallback...")
            print("⚠️ IMPORTANT: Mock data is for demonstration only - not real recipes!")
            all_recipes.extend(self.get_mock_recipes(query, max_results))
        
        for recipe in all_recipes:
            if 'scraping_errors' not in recipe:
                recipe['scraping_errors'] = scraping_errors
            recipe['total_sources_attempted'] = 2
            recipe['successful_sources'] = 2 - len(scraping_errors)
        
        return all_recipes[:max_results]

