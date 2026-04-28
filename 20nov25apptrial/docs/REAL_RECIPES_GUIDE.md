# Getting Real Recipes - Complete Guide

## The Problem

You're currently seeing mock/fake data because modern recipe websites like AllRecipes use **JavaScript** to load their content. Our basic scraper (using `requests` + `BeautifulSoup`) can't execute JavaScript, so it only sees empty HTML.

## Your Options

### 🌟 OPTION 1: Use Selenium (RECOMMENDED)

**What it does:** Opens a real browser and executes JavaScript

**Steps to implement:**

1. **Install Selenium:**
   ```powershell
   .venv\Scripts\activate
   pip install -r requirements_selenium.txt
   ```

2. **Test it works:**
   ```powershell
   python scraper_selenium.py
   ```

3. **Integrate into your app:**
   Edit `app.py` line 6:
   ```python
   # Change this:
   from scraper import RecipeScraper
   
   # To this:
   from scraper_selenium import RecipeScraperSelenium as RecipeScraper
   ```

4. **Restart your Flask server:**
   ```powershell
   python app.py
   ```

**Pros:**
- ✅ Gets REAL recipes from AllRecipes, BBC Good Food, etc.
- ✅ Works with modern JavaScript websites
- ✅ Still respects robots.txt and ethical scraping
- ✅ Great for your MSc project (shows technical depth)

**Cons:**
- ⏱️ Slower (2-5 seconds per recipe vs 0.5 seconds)
- 💾 Uses more resources (opens a browser)
- 🔧 Requires Chrome browser installed

---

### OPTION 2: Use Recipe APIs

**What it does:** Uses official APIs from recipe websites

**Examples:**
- Spoonacular API (https://spoonacular.com/food-api)
- Edamam Recipe API (https://www.edamam.com/)
- TheMealDB API (https://www.themealdb.com/api.php) - FREE!

**Steps for TheMealDB (Free):**

1. **Test the API:**
   ```powershell
   curl "https://www.themealdb.com/api/json/v1/1/search.php?s=chicken"
   ```

2. **I can create a new scraper** that uses this API instead of web scraping

**Pros:**
- ✅ Very fast
- ✅ Reliable and legal
- ✅ Structured data (easy to parse)
- ✅ No robots.txt concerns

**Cons:**
- ❌ Limited free recipes (TheMealDB has ~600 recipes)
- ❌ May require API keys
- ❌ Usage limits on free tiers

---

### OPTION 3: Find Simpler Recipe Sites

**What it does:** Scrapes websites that don't use heavy JavaScript

**Examples:**
- Food.com (older structure)
- Recipe blogs (many use simple HTML)
- Archive.org cached versions

**Pros:**
- ✅ Works with current scraper (no changes needed)
- ✅ Fast

**Cons:**
- ❌ Harder to find reliable sources
- ❌ Sites may change or go offline
- ❌ Less variety

---

### OPTION 4: Keep Mock Data

**What it does:** Use the generated recipes for demonstration

**Pros:**
- ✅ Always works
- ✅ Fast and reliable
- ✅ Good for testing allergen detection
- ✅ Can customize recipes to showcase features

**Cons:**
- ❌ Not real recipes
- ❌ Less impressive for your project

---

## My Recommendation

For your **MSc Web Development Project**, I strongly recommend **OPTION 1 (Selenium)** because:

1. **Academic Value**: Demonstrates understanding of:
   - Modern web technologies (JavaScript rendering)
   - Browser automation
   - Complex problem-solving

2. **Real Data**: Shows your allergen detection working with actual recipes

3. **Industry Relevant**: Selenium is widely used professionally

4. **Ethical Compliance**: You can still implement all ethical scraping practices

5. **Dissertation Content**: Provides rich material for your technical discussion

---

## Quick Start: Selenium Implementation

### 1. Install Requirements
```powershell
cd "C:\Users\John\Documents\Comp Sci Msc\web\it3\20nov25apptrial"
.venv\Scripts\activate
pip install -r requirements_selenium.txt
```

### 2. Test Selenium Scraper
```powershell
python scraper_selenium.py
```

You should see:
```
✓ Selenium WebDriver initialized successfully
Loading AllRecipes search page...
Found X potential recipe links
✓ Scraped: [Recipe Name]
...
```

### 3. Integrate into Flask App
```powershell
# Edit app.py (I can do this for you)
# Then restart:
python app.py
```

### 4. Test in Browser
```
http://localhost:5000
Search for "chicken" or "lasagne"
```

You should now see REAL recipes! 🎉

---

## Need Help?

Let me know if you want me to:
1. ✅ **Install and test Selenium** (RECOMMENDED)
2. ✅ **Implement a Recipe API** instead
3. ✅ **Find simpler websites** to scrape
4. ✅ **Improve the mock data** generator

Just tell me which option you prefer!

