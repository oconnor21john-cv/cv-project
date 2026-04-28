# Application Run Order Guide

## Quick Start (Easiest Method)

### Option 1: Use the Master Script (RECOMMENDED)

Simply double-click or run:
```bash
run_app.bat
```

This will automatically:
1. Check Python installation
2. Install missing dependencies
3. Start the Flask server
4. Open at http://localhost:5000

---

## File Execution Order (What Happens Behind the Scenes)

### Core Files (Run in This Order):

1. **`app.py`** - Main Flask application (START HERE)
   - This is the ONLY file you need to run
   - It automatically imports and uses all other files

2. **Files imported by app.py** (automatically loaded):
   - `scraper_api.py` - Gets real recipes from TheMealDB API
   - `allergen_detector.py` - Detects allergens in ingredients
   - `templates/index.html` - Frontend HTML
   - `static/css/style.css` - Styling
   - `static/js/app.js` - Frontend JavaScript

### You DON'T need to run these separately:
- ❌ `scraper_api.py` - Imported by app.py
- ❌ `allergen_detector.py` - Imported by app.py
- ❌ Any HTML/CSS/JS files - Served by Flask

---

## Manual Start (If You Prefer)

### Step 1: Open Terminal/PowerShell
```powershell
cd "C:\Users\John\Documents\Comp Sci Msc\web\it3\20nov25apptrial"
```

### Step 2: Run the Flask App
```powershell
python app.py
```

### Step 3: Open Browser
Go to: `http://localhost:5000`

### Step 4: Stop the Server
Press `Ctrl+C` in the terminal

---

## File Dependencies (Visual)

```
run_app.bat  (Master Script - Optional)
    ↓
app.py  (Main Application - START HERE)
    ↓
    ├── scraper_api.py
    │       ↓
    │       └── allergen_detector.py
    │
    ├── allergen_detector.py
    │
    ├── templates/index.html
    │       ↓
    │       ├── static/css/style.css
    │       └── static/js/app.js
    │
    └── Flask Routes:
            ├── GET  /              → Serves index.html
            ├── POST /api/search    → Searches recipes
            └── POST /api/filter    → Filters by allergens
```

---

## Testing Files (Optional - For Development)

These are for testing only, NOT needed to run the app:

- `test_app.py` - Tests core functionality
- `test_real_recipes.py` - Tests API connection
- `scraper_selenium.py` - Alternative scraper (not used)

To run tests:
```powershell
python test_app.py
python test_real_recipes.py
```

---

## Common Scenarios

### Scenario 1: First Time Setup
```powershell
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

### Scenario 2: Daily Use
```powershell
# Just run the app
python app.py
```

### Scenario 3: After Making Changes
```powershell
# Stop the server (Ctrl+C)
# Make your changes
# Restart the server
python app.py
```

---

## What Each File Does

| File | Purpose | Run It? |
|------|---------|---------|
| `run_app.bat` | Master startup script | ✅ YES (easiest) |
| `app.py` | Main Flask application | ✅ YES (or use bat) |
| `scraper_api.py` | Gets recipes from API | ❌ Auto-imported |
| `allergen_detector.py` | Detects allergens | ❌ Auto-imported |
| `templates/index.html` | Frontend page | ❌ Auto-served |
| `static/css/style.css` | Styling | ❌ Auto-served |
| `static/js/app.js` | Frontend logic | ❌ Auto-served |
| `requirements.txt` | Package list | ❌ Use with pip |
| `test_*.py` | Testing scripts | ⚠️ Optional |

---

## Summary

**To run your application, you only need ONE command:**

```powershell
python app.py
```

**Or even simpler:**

```powershell
run_app.bat
```

Everything else is automatically handled by Flask! 🎉

---

## Troubleshooting

### "Module not found" error
```powershell
pip install -r requirements.txt
```

### "Port already in use"
```powershell
# Find and stop the other Flask instance
# Or change the port in app.py (last line)
```

### "Can't connect to localhost"
- Make sure `python app.py` is running
- Check the terminal for error messages
- Try: http://127.0.0.1:5000 instead

---

## For Your Dissertation

When documenting your project, you can explain:

1. **Single Entry Point**: `app.py` is the main entry point
2. **Modular Design**: Separate files for different concerns
3. **Automatic Dependencies**: Flask handles imports and serving
4. **Easy Deployment**: One command to start everything

This demonstrates good software engineering practices! 👍

