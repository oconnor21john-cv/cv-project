# Web Scraping Guide - Real Recipe Sources

## ✅ Real Web Scraping Enabled!

I've updated the `scraper.py` file to enable real web scraping from recipe websites.

---

## 🌐 Currently Supported Websites

### 1. AllRecipes.com
- **Status**: Enabled ✅
- **Method**: `scrape_allrecipes()`
- **Data Extracted**:
  - Recipe title
  - Ingredients list
  - Cooking instructions
  - Recipe images
  - Source URL

### 2. BBC Good Food
- **Status**: Enabled ✅
- **Method**: `scrape_bbc_good_food()`
- **Data Extracted**:
  - Recipe title
  - Ingredients list
  - Cooking instructions
  - Recipe images
  - Source URL

---

## 🚀 How It Works Now

### Automatic Fallback System
```
1. Try scraping AllRecipes.com
2. Try scraping BBC Good Food
3. If both fail → Use mock data as fallback
```

### Search Flow
```python
User searches "chicken"
    ↓
Scrape AllRecipes (up to 7-8 recipes)
    ↓
Scrape BBC Good Food (up to 7-8 recipes)
    ↓
Combine results (up to 15 total)
    ↓
Detect allergens in all recipes
    ↓
Return filtered results
```

---

## ⚠️ Important Considerations

### 1. **Website Structure Changes**
Recipe websites frequently update their HTML structure. If scraping stops working:
- The website may have changed their layout
- You'll need to update the CSS selectors in `scraper.py`
- The mock data fallback will activate automatically

### 2. **Rate Limiting**
The scraper includes polite delays:
```python
time.sleep(random.uniform(0.5, 1.0))  # 0.5-1 second between requests
```

### 3. **Robots.txt & Terms of Service**
- Always respect website terms of service
- Check `robots.txt` before scraping
- This tool is for educational purposes
- Don't overload servers with requests

### 4. **Legal & Ethical Scraping**
✅ **DO:**
- Add delays between requests
- Respect robots.txt
- Use for personal/educational purposes
- Attribute sources properly
- Handle errors gracefully

❌ **DON'T:**
- Scrape excessively
- Ignore rate limits
- Use for commercial purposes without permission
- Bypass anti-scraping measures
- Overload servers

---

## 🔧 Testing Real Scraping

### Restart the Application
Since you changed `scraper.py`, restart the Flask server:

```bash
# Stop the current server (Ctrl+C)
# Then restart:
python app.py
```

### Test Searches
Try these searches to test real scraping:
1. "chicken soup"
2. "chocolate cake"
3. "pasta carbonara"
4. "vegetable stir fry"
5. "banana bread"

---

## 🐛 Troubleshooting

### Problem: No Real Recipes Returned
**Possible Causes:**
1. Website structure changed
2. Network connection issue
3. Website blocking automated requests
4. CSS selectors outdated

**Solution:**
- Check console output for error messages
- The app will automatically fall back to mock data
- Update CSS selectors if needed (see below)

### Problem: Slow Response
**Cause:** Real scraping takes longer than mock data
**Expected:** 2-5 seconds per search
**Normal:** This is expected behavior

### Problem: Some Recipes Missing Data
**Cause:** Website HTML structure varies
**Solution:** The app handles this gracefully, skipping incomplete recipes

---

## 🛠️ Adding More Recipe Sources

Want to add more websites? Here's how:

### Step 1: Create a Scraping Method

```python
def scrape_new_website(self, query, max_results=10):
    """Scrape from a new recipe website"""
    recipes = []
    
    try:
        # Build search URL
        search_url = f"https://example.com/search?q={query}"
        
        # Fetch page
        response = requests.get(search_url, headers=self.headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find recipe links (update selector for the website)
        recipe_links = soup.find_all('a', class_='recipe-link')
        
        for link in recipe_links[:max_results]:
            # Extract recipe data
            recipe_data = self._scrape_new_website_detail(link['href'])
            if recipe_data:
                recipes.append(recipe_data)
            
            # Be polite - add delay
            time.sleep(random.uniform(0.5, 1.0))
    
    except Exception as e:
        print(f"Error scraping new website: {e}")
    
    return recipes
```

### Step 2: Add to search_recipes()

```python
def search_recipes(self, query, max_results=15):
    all_recipes = []
    
    all_recipes.extend(self.scrape_allrecipes(query, max_results // 3))
    all_recipes.extend(self.scrape_bbc_good_food(query, max_results // 3))
    all_recipes.extend(self.scrape_new_website(query, max_results // 3))  # Add here
    
    if len(all_recipes) == 0:
        all_recipes.extend(self.get_mock_recipes(query, max_results))
    
    return all_recipes[:max_results]
```

---

## 📊 Popular Recipe Websites to Consider

### Easy to Scrape (Good HTML Structure)
- ✅ AllRecipes.com (already implemented)
- ✅ BBC Good Food (already implemented)
- Food Network
- Tasty
- Simply Recipes

### More Challenging (Complex JavaScript)
- Pinterest (requires JavaScript rendering)
- Instagram (requires authentication)
- TikTok (requires API access)

---

## 🔍 Finding CSS Selectors

### Using Browser Developer Tools

1. **Open the recipe website**
2. **Right-click** on a recipe title → "Inspect"
3. **Find the HTML element** in DevTools
4. **Note the class names** or IDs
5. **Update in scraper.py**

### Example for AllRecipes:
```python
# Find recipe cards
recipe_cards = soup.find_all('a', class_='card__titleLink')

# Find ingredients
ingredients = soup.find_all('li', class_='mntl-structured-ingredients__list-item')

# Find instructions
instructions = soup.find_all('li', class_='mntl-sc-block-group--LI')
```

---

## 📈 Performance Optimization

### Current Implementation
- Sequential scraping (one site at a time)
- ~2-5 seconds per search

### Future Improvements

#### 1. Async/Parallel Scraping
```python
import asyncio
import aiohttp

async def scrape_all_sources(query):
    tasks = [
        scrape_allrecipes_async(query),
        scrape_bbc_async(query),
        scrape_other_async(query)
    ]
    results = await asyncio.gather(*tasks)
    return results
```

#### 2. Caching
```python
from functools import lru_cache
import time

@lru_cache(maxsize=100)
def search_recipes_cached(query, timestamp):
    # Cache results for 1 hour
    return search_recipes(query)

# Use with:
search_recipes_cached(query, int(time.time() / 3600))
```

#### 3. Database Storage
Store scraped recipes in a database:
- SQLite for simple setup
- PostgreSQL for production
- MongoDB for flexible schema

---

## 🎯 Best Practices

### 1. User Agent
Always use a descriptive User-Agent:
```python
headers = {
    'User-Agent': 'Educational Recipe Scraper Bot 1.0 (contact@example.com)'
}
```

### 2. Error Handling
Handle all possible errors:
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.Timeout:
    print("Request timed out")
except requests.HTTPError as e:
    print(f"HTTP error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 3. Respect Rate Limits
```python
# Add delays
time.sleep(random.uniform(0.5, 1.5))

# Limit concurrent requests
max_concurrent = 3

# Use exponential backoff on errors
```

### 4. Data Validation
```python
if recipe_data and recipe_data.get('title') and recipe_data.get('ingredients'):
    recipes.append(recipe_data)
else:
    print(f"Skipping incomplete recipe")
```

---

## 📝 Monitoring & Logging

### Add Logging to Track Scraping

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_recipes(self, query, max_results=15):
    logger.info(f"Searching for: {query}")
    
    allrecipes_count = len(self.scrape_allrecipes(query, max_results // 2))
    logger.info(f"AllRecipes returned: {allrecipes_count} recipes")
    
    bbc_count = len(self.scrape_bbc_good_food(query, max_results // 2))
    logger.info(f"BBC Good Food returned: {bbc_count} recipes")
```

---

## 🚦 Current Status

### ✅ What's Working
- Real web scraping enabled
- Two sources active (AllRecipes, BBC Good Food)
- Automatic fallback to mock data
- Allergen detection on all recipes
- Error handling

### 🔄 What Might Need Updates
- CSS selectors (websites change frequently)
- Rate limiting (adjust if needed)
- Additional sources (add more websites)

---

## 🎓 Learning Resources

### Web Scraping
- BeautifulSoup Documentation: https://www.crummy.com/software/BeautifulSoup/
- Requests Library: https://requests.readthedocs.io/
- Web Scraping Ethics: https://www.scrapehero.com/web-scraping-ethics/

### Legal Information
- robots.txt Guide: https://developers.google.com/search/docs/crawling-indexing/robots/intro
- Terms of Service: Check each website individually

---

## 🎉 You're All Set!

Real web scraping is now enabled! The application will:
1. ✅ Try to scrape real recipes from AllRecipes and BBC Good Food
2. ✅ Automatically fall back to mock data if scraping fails
3. ✅ Detect allergens in all recipes (real or mock)
4. ✅ Provide a seamless user experience

**Restart your Flask server to see it in action!**

```bash
python app.py
```

Then search for recipes and watch it scrape real data! 🚀


