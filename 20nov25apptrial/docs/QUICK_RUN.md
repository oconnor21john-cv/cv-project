# Quick Run Guide

## 🚀 Fastest Way to Start

### Method 1: Double-click the batch file
```
run_app.bat
```

### Method 2: One command
```powershell
python app.py
```

Then open: **http://localhost:5000**

---

## 📋 That's It!

You only need to run **ONE file**: `app.py`

All other files are automatically loaded:
- ✅ `scraper_api.py` - Imported automatically
- ✅ `allergen_detector.py` - Imported automatically  
- ✅ HTML/CSS/JS files - Served automatically

---

## 🛑 To Stop

Press `Ctrl+C` in the terminal

---

## 🔧 If You Get Errors

### "Module not found"
```powershell
pip install -r requirements.txt
```

### "Port already in use"
Stop the other Flask instance or restart your computer

---

## 📁 File Order (For Reference)

```
START HERE → app.py
                ↓
                ├─→ scraper_api.py
                │      ↓
                │      └─→ allergen_detector.py
                │
                └─→ templates/index.html
                       ↓
                       ├─→ static/css/style.css
                       └─→ static/js/app.js
```

**You only run the first file!** Everything else is automatic.

