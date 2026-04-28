# Quick Start Guide - Allergen-Filtered Recipe Search

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install flask flask-cors requests beautifulsoup4 python-dotenv
```

### Step 2: Run the Application

**Option A: Using Python directly**
```bash
python app.py
```

**Option B: Using the batch file (Windows)**
```bash
start_app.bat
```

### Step 3: Open Your Browser
Navigate to: **http://localhost:5000**

---

## 📖 How to Use

### 1. Search for Recipes
- Type a food item in the search box (e.g., "chicken", "pasta", "salad")
- Click "Search Recipes"

### 2. Filter by Allergens
Before searching, check the boxes for allergens you want to avoid:
- ☑ Milk (Dairy)
- ☑ Cereals containing gluten
- ☑ Eggs
- etc.

### 3. View Results
- Browse recipe cards with images and allergen information
- Click any recipe to see full details

### 4. Recipe Details
The modal shows:
- Complete ingredient list
- Step-by-step instructions
- Allergen warnings
- Source information

---

## 🧪 Test the Application

Run the test script to verify everything works:
```bash
python test_app.py
```

Expected output:
```
[OK] AllergenDetector imported successfully
[OK] RecipeScraper imported successfully
[OK] Flask imported successfully
...
All Tests Completed Successfully!
```

---

## 📋 Example Searches

### Example 1: Dairy-Free Recipes
1. Enter "chicken" in search
2. Check "Milk (Dairy)" box
3. Search
4. See only dairy-free chicken recipes

### Example 2: Gluten and Nut-Free
1. Enter "salad"
2. Check "Cereals containing gluten" and "Tree Nuts"
3. Search
4. Get safe salad recipes

### Example 3: Multiple Allergens
1. Enter "pasta"
2. Check multiple allergen boxes
3. Search
4. View highly filtered results

---

## 🎯 Key Features

✅ **14 Allergen Groups** - Complete EU allergen list
✅ **Real-time Filtering** - Instant results
✅ **Recipe Details** - Full ingredients and instructions
✅ **Responsive Design** - Works on all devices
✅ **Allergen Warnings** - Clear visual indicators
✅ **Mock Data** - Works without internet scraping

---

## 🔧 Troubleshooting

### Problem: "Module not found"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Problem: "Port 5000 already in use"
**Solution**: Change port in app.py (line 135)
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Problem: No recipes found
**Solution**: 
- Try different search terms
- Reduce number of excluded allergens
- Check internet connection

### Problem: Images not loading
**Solution**: This is normal - mock data uses placeholder images

---

## 📁 Project Structure

```
.
├── app.py                 # Flask server (START HERE)
├── allergen_detector.py   # Allergen detection logic
├── scraper.py            # Recipe scraping
├── test_app.py           # Test script
├── requirements.txt      # Dependencies
├── templates/
│   └── index.html        # Main page
└── static/
    ├── css/
    │   └── style.css     # Styling
    └── js/
        └── app.js        # Frontend logic
```

---

## 🌐 API Endpoints

### Get Allergens
```
GET /api/allergens
```
Returns list of all 14 allergen groups

### Search Recipes
```
POST /api/search
Content-Type: application/json

{
  "query": "chicken",
  "excluded_allergens": ["milk", "gluten"]
}
```
Returns filtered recipes

### Health Check
```
GET /health
```
Verifies server is running

---

## 💡 Tips

1. **Start Simple** - Try searching without filters first
2. **Be Specific** - Use specific food names ("grilled chicken" vs "chicken")
3. **Check Allergens** - Always verify allergen information
4. **Mobile Friendly** - Works great on phones and tablets
5. **Bookmark Favorites** - Save recipes you like

---

## ⚠️ Important Notice

**Allergen Detection Disclaimer**:
- Automated detection may not be 100% accurate
- Always verify ingredients if you have severe allergies
- Cross-contamination is not accounted for
- Consult healthcare professionals for dietary advice

---

## 📚 Additional Resources

- **README.md** - Comprehensive project documentation
- **USAGE_GUIDE.md** - Detailed usage instructions
- **PROJECT_SUMMARY.md** - Technical overview
- **test_app.py** - Test and validation script

---

## 🎓 Learning Outcomes

This project demonstrates:
- Web scraping with Python
- Flask backend development
- RESTful API design
- Frontend JavaScript
- Responsive CSS design
- Data filtering algorithms
- User interface design

---

## 🚀 Next Steps

After getting familiar with the application:

1. **Customize** - Modify allergen keywords in `allergen_detector.py`
2. **Extend** - Add new recipe sources in `scraper.py`
3. **Style** - Change colors and design in `static/css/style.css`
4. **Deploy** - Host on Heroku, AWS, or other platforms
5. **Enhance** - Add features like user accounts, ratings, etc.

---

## ✅ Checklist

Before using the application:
- [ ] Python 3.7+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Port 5000 available
- [ ] Browser ready (Chrome, Firefox, Safari, Edge)

---

## 🎉 You're Ready!

Run `python app.py` and start exploring allergen-friendly recipes!

**Enjoy cooking safely! 👨‍🍳👩‍🍳**

