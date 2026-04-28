# Selenium Setup Guide

## What is Selenium?

Selenium is a browser automation tool that:
- Opens a real browser (Chrome, Firefox, etc.)
- Executes JavaScript just like a human user
- Can scrape content from modern, JavaScript-heavy websites

## Installation Steps

### Step 1: Install Chrome Browser
Make sure you have Google Chrome installed on your computer.
- Download from: https://www.google.com/chrome/

### Step 2: Install Selenium Packages

```powershell
# Activate your virtual environment first
.venv\Scripts\activate

# Install Selenium and WebDriver Manager
pip install -r requirements_selenium.txt
```

### Step 3: Test the Installation

```powershell
python scraper_selenium.py
```

This will:
1. Automatically download the correct ChromeDriver
2. Open Chrome in headless mode (invisible)
3. Scrape 3 real recipes from AllRecipes
4. Display the results

## Using Selenium in Your App

### Option A: Replace the Current Scraper

Edit `app.py` and change the import:

```python
# OLD:
from scraper import RecipeScraper

# NEW:
from scraper_selenium import RecipeScraperSelenium as RecipeScraper
```

### Option B: Add as an Alternative

Keep both scrapers and let users choose, or use Selenium as a fallback.

## Troubleshooting

### Error: "Chrome not found"
- **Solution**: Install Google Chrome browser

### Error: "ChromeDriver version mismatch"
- **Solution**: The `webdriver-manager` package should handle this automatically
- If it persists, try: `pip install --upgrade webdriver-manager`

### Error: "Timeout waiting for page"
- **Solution**: Increase the wait time in `scraper_selenium.py`
- Some websites load slowly; this is normal

### Scraping is Slow
- **Expected**: Selenium is slower than requests (it loads a full browser)
- **Typical speed**: 2-5 seconds per recipe vs 0.5 seconds with requests
- **Trade-off**: Slower but gets real data from JavaScript sites

## Ethical Considerations

The Selenium scraper still implements:
- ✅ robots.txt compliance
- ✅ Crawl delay respect
- ✅ Educational User-Agent
- ✅ Rate limiting
- ✅ Error handling

## Performance Tips

1. **Headless Mode**: Keep `--headless` flag (browser runs in background)
2. **Disable Images**: Add `chrome_options.add_argument('--blink-settings=imagesEnabled=false')` to load faster
3. **Reuse Driver**: The driver is reused across multiple recipes in one search
4. **Limit Results**: Start with fewer results (5-10) for faster responses

## When to Use Selenium vs Regular Scraping

**Use Selenium when:**
- Website uses heavy JavaScript (React, Vue, Angular)
- Content loads dynamically after page load
- You need to interact with the page (click, scroll, etc.)

**Use Regular Scraping (requests + BeautifulSoup) when:**
- Website has traditional HTML
- Speed is critical
- Content is in the initial HTML response

## Next Steps

1. Test the Selenium scraper: `python scraper_selenium.py`
2. If it works, integrate it into your Flask app
3. Restart your Flask server to see real recipes!

