# File Structure & Execution Summary

## 🎯 Main Takeaway

**You only need to run ONE file: `app.py`**

Everything else is automatically handled!

---

## 📂 File Structure

```
20nov25apptrial/
│
├── 🚀 STARTUP FILES (Choose One)
│   ├── run_app.bat          ← Double-click this (Windows)
│   └── app.py               ← Or run this with: python app.py
│
├── 🔧 CORE APPLICATION FILES (Auto-imported by app.py)
│   ├── scraper_api.py       ← Gets real recipes from TheMealDB
│   ├── allergen_detector.py ← Detects allergens in ingredients
│   │
│   ├── templates/
│   │   └── index.html       ← Frontend HTML
│   │
│   └── static/
│       ├── css/
│       │   └── style.css    ← Styling
│       └── js/
│           └── app.js       ← Frontend JavaScript
│
├── 📦 CONFIGURATION FILES
│   ├── requirements.txt     ← Python packages (use with: pip install -r)
│   └── requirements_selenium.txt ← Alternative packages (not needed)
│
├── 🧪 TESTING FILES (Optional - for development)
│   ├── test_app.py          ← Test core functionality
│   └── test_real_recipes.py ← Test API connection
│
├── 📚 DOCUMENTATION FILES (Read these for help)
│   ├── START_HERE.txt       ← Quick start (read this first!)
│   ├── QUICK_RUN.md         ← Fastest way to run
│   ├── RUN_ORDER.md         ← Detailed execution order
│   ├── README.md            ← Full project documentation
│   ├── USAGE_GUIDE.md       ← How to use the app
│   ├── QUICK_START.md       ← Setup guide
│   ├── PROJECT_SUMMARY.md   ← Technical overview
│   ├── FEATURES.md          ← Feature specifications
│   ├── TROUBLESHOOTING.md   ← Common issues & solutions
│   ├── WEB_SCRAPING_GUIDE.md ← Scraping documentation
│   ├── ROBOTS_TXT_IMPLEMENTATION.md ← Ethics documentation
│   ├── ETHICAL_COMPLIANCE_SUMMARY.md ← Compliance overview
│   ├── SCRAPING_ISSUE_EXPLANATION.md ← Why we use API
│   ├── SELENIUM_SETUP_GUIDE.md ← Alternative approach
│   ├── REAL_RECIPES_GUIDE.md ← Recipe sources explained
│   └── INDEX.md             ← Documentation index
│
└── 🔄 ALTERNATIVE SCRAPERS (Not currently used)
    ├── scraper.py           ← Original scraper (mock data)
    └── scraper_selenium.py  ← Browser-based scraper (optional)
```

---

## ⚡ Execution Flow

```
User Action: run_app.bat  OR  python app.py
                    ↓
            app.py starts
                    ↓
    ┌───────────────┴───────────────┐
    ↓                               ↓
Imports scraper_api.py      Imports allergen_detector.py
    ↓                               ↓
scraper_api.py imports      allergen_detector.py
allergen_detector.py        loads allergen database
    ↓                               ↓
    └───────────────┬───────────────┘
                    ↓
        Flask server starts
                    ↓
    ┌───────────────┴───────────────┐
    ↓                               ↓
Serves templates/index.html    Serves static files
    ↓                               ↓
index.html loads               CSS & JS loaded
    ↓                               ↓
    └───────────────┬───────────────┘
                    ↓
        Application Ready!
    Browser: http://localhost:5000
```

---

## 🎬 What Happens When You Run app.py

1. **Line 1-9**: Import statements
   - Imports Flask framework
   - Imports `scraper_api.py` (which imports `allergen_detector.py`)
   - Imports `allergen_detector.py` directly

2. **Line 11-16**: Initialize application
   - Creates Flask app
   - Creates scraper instance
   - Creates allergen detector instance

3. **Line 19-130**: Define routes
   - `/` - Serves the main page (index.html)
   - `/api/search` - Searches for recipes
   - `/api/filter` - Filters recipes by allergens

4. **Line 132-137**: Start server
   - Runs on http://localhost:5000
   - Debug mode enabled for development

---

## 📋 File Dependencies

```
app.py
├── Requires: flask, flask_cors
├── Imports: scraper_api.py
│   └── Requires: requests
│       └── Imports: allergen_detector.py
│           └── Requires: (no external packages)
└── Imports: allergen_detector.py
    └── Requires: (no external packages)

templates/index.html
├── Loads: static/css/style.css
└── Loads: static/js/app.js
    └── Makes API calls to app.py routes
```

---

## 🚦 Run Order (Simple Version)

### For Daily Use:
```
1. python app.py
2. Open browser to http://localhost:5000
3. Done!
```

### For First Time Setup:
```
1. pip install -r requirements.txt
2. python app.py
3. Open browser to http://localhost:5000
4. Done!
```

---

## ❌ What NOT to Run

Don't run these files directly (they're imported automatically):
- ❌ scraper_api.py
- ❌ allergen_detector.py
- ❌ Any HTML/CSS/JS files

Don't use these files (they're alternatives):
- ❌ scraper.py (old version with mock data)
- ❌ scraper_selenium.py (browser-based, has compatibility issues)

---

## ✅ Files You CAN Run (Optional)

These are for testing only:
- ✅ test_app.py - Tests the application
- ✅ test_real_recipes.py - Tests API connection

---

## 🎓 For Your Dissertation

When explaining your project structure, highlight:

1. **Single Entry Point**: `app.py` is the main entry point
2. **Modular Design**: Separate concerns (scraping, allergen detection, web interface)
3. **Automatic Dependencies**: Flask handles all imports and file serving
4. **Clean Architecture**: Clear separation between backend (Python) and frontend (HTML/CSS/JS)
5. **Easy Deployment**: One command starts everything

This demonstrates professional software engineering practices!

---

## 📞 Quick Reference

| What You Want | What To Do |
|---------------|------------|
| Start the app | `python app.py` or `run_app.bat` |
| Stop the app | Press `Ctrl+C` |
| View the app | Open `http://localhost:5000` |
| Install packages | `pip install -r requirements.txt` |
| Test the app | `python test_app.py` |
| Read docs | Start with `START_HERE.txt` |

---

## 🎉 Summary

**To run your application:**
1. Open terminal
2. Type: `python app.py`
3. Open browser: http://localhost:5000
4. Search for recipes!

**That's it!** All other files work automatically in the background.

