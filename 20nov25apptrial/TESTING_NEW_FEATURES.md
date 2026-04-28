# Testing Guide: Enhanced Safety Features

## Quick Start

### 1. Start the Application
```bash
cd "c:\Users\John\Documents\Comp Sci Msc\web\it3\20nov25apptrial"
python app.py
```

The app will start on: `http://localhost:5000`

---

## Feature Testing Checklist

### ✅ Test 1: Critical Safety Banner

**What to look for:**
- [ ] Red banner at the very top of the page
- [ ] Animated warning icon (⚠️)
- [ ] Text: "CRITICAL SAFETY NOTICE"
- [ ] Clear warning about automated detection not being 100% accurate
- [ ] Banner is impossible to dismiss or hide

**Expected Result:** Banner should be highly visible and attention-grabbing.

---

### ✅ Test 2: Confidence Scoring

**Steps:**
1. Search for: "chicken pasta"
2. Look at the recipe cards

**What to look for:**
- [ ] Allergen badges have different colors:
  - 🔴 Red = HIGH confidence
  - 🟠 Orange = MEDIUM confidence
  - 🟡 Yellow = LOW confidence
- [ ] Hover over badges to see confidence percentage
- [ ] Each recipe shows which allergens were detected

**Expected Result:** Different allergens should show different confidence levels.

---

### ✅ Test 3: Safety Verification Gate

**Steps:**
1. Click on any recipe card

**What to look for:**
- [ ] Modal opens with yellow warning box
- [ ] Title: "⚠️ Safety Verification Required"
- [ ] 4 bullet points about limitations
- [ ] Checkbox: "I understand and accept these limitations"
- [ ] "View Recipe" button is DISABLED initially
- [ ] Checking the box ENABLES the button
- [ ] Cannot view recipe without checking box

**Expected Result:** Users must actively acknowledge safety limitations.

---

### ✅ Test 4: Detailed Allergen Information

**Steps:**
1. Search for: "pasta carbonara" (contains eggs, milk, gluten)
2. Click on a recipe
3. Check the safety verification box
4. Click "View Recipe"

**What to look for:**
- [ ] Allergen warning section with detailed breakdown
- [ ] Each allergen shows:
  - Name (e.g., "Milk (Dairy)")
  - Confidence level (HIGH/MEDIUM/LOW)
  - Confidence percentage (e.g., "90%")
  - Detection method (e.g., "lexical, compound")
  - Matched keywords (e.g., "parmesan (specific type)")
- [ ] Color-coded boxes for each allergen
- [ ] Critical reminder: "Even HIGH confidence detections may be incorrect"

**Expected Result:** Transparent breakdown of how allergens were detected.

---

### ✅ Test 5: Ingredient Normalization

**Steps:**
1. Look at recipe ingredients in the modal
2. Notice how ingredients are displayed

**What to look for:**
- [ ] Original ingredients shown as-is
- [ ] Allergen detection works even with:
  - Measurements: "2 cups milk" → detects milk
  - Preparation: "chopped walnuts" → detects nuts
  - Descriptors: "fresh parmesan cheese" → detects dairy

**Expected Result:** System detects allergens regardless of how ingredients are written.

---

### ✅ Test 6: Compound Ingredient Detection

**Test Cases:**

#### Test 6a: Pesto (contains pine nuts)
1. Search for: "pesto pasta"
2. Check if "Tree Nuts" is detected
3. In recipe details, verify it shows "pesto (compound)" as matched keyword

#### Test 6b: Soy Sauce (may contain wheat/gluten)
1. Search for: "stir fry"
2. Check if "Cereals containing gluten" is detected
3. Verify "soy sauce" is listed as matched keyword

#### Test 6c: Parmesan (contains milk)
1. Search for: "caesar salad"
2. Check if "Milk (Dairy)" is detected
3. Verify "parmesan (specific type)" is shown

**Expected Result:** System detects hidden allergens in compound ingredients.

---

### ✅ Test 7: Data Transparency

**Steps:**
1. View any recipe details

**What to look for:**
- [ ] Source clearly shown (e.g., "BBC Good Food")
- [ ] Data Retrieved timestamp
- [ ] Collection Method (e.g., "BeautifulSoup HTML parsing")
- [ ] Data Type (Live Scraped Data or Demonstration Data)
- [ ] Link to original recipe (if available)

**Expected Result:** Complete transparency about data source and collection.

---

### ✅ Test 8: Data Quality Indicators

**What to look for on recipe cards:**
- [ ] 🌐 "Live" badge for scraped recipes
- [ ] 📋 "Demo" badge for mock data

**Expected Result:** Users can distinguish real data from demonstration data.

---

### ✅ Test 9: Allergen Filtering

**Steps:**
1. Check "Milk (Dairy)" in the allergen filters
2. Search for: "pasta"
3. Look at results

**What to look for:**
- [ ] Results count shows: "Found X recipes (filtered from Y total)"
- [ ] Recipes with milk allergens are excluded
- [ ] Even LOW confidence milk detections are excluded (conservative approach)

**Expected Result:** Filtering works conservatively (excludes even uncertain detections).

---

### ✅ Test 10: Error Handling

**Steps:**
1. Disconnect from internet (or wait for scraping to fail)
2. Search for anything

**What to look for:**
- [ ] System doesn't crash
- [ ] Falls back to demonstration data
- [ ] Shows warning: "⚠️ Real scraping returned no results, using mock data"
- [ ] Shows warning: "⚠️ IMPORTANT: Mock data is for demonstration only!"
- [ ] Recipes are marked with 📋 "Demo" badge

**Expected Result:** Graceful degradation with clear user communication.

---

### ✅ Test 11: No Allergens Detected

**Steps:**
1. Search for: "salad" (simple recipes)
2. Find a recipe with no detected allergens
3. View details

**What to look for:**
- [ ] Info box (blue, not red)
- [ ] Message: "No major allergens detected by automated system"
- [ ] **Critical reminder:** "This does NOT guarantee the recipe is safe"
- [ ] Warning: "Always verify ingredients manually"

**Expected Result:** Even "safe" recipes have warnings about verification.

---

### ✅ Test 12: Multiple Confidence Levels

**Steps:**
1. Search for: "chocolate cake" (milk, eggs, gluten)
2. View a recipe with multiple allergens

**What to look for:**
- [ ] Different allergens show different confidence levels
- [ ] HIGH confidence allergens listed first
- [ ] Each has its own color-coded box
- [ ] Detection methods vary (lexical, compound, specific type)

**Expected Result:** System provides nuanced confidence assessment.

---

### ✅ Test 13: Mobile Responsiveness

**Steps:**
1. Resize browser window to mobile size (or use mobile device)

**What to look for:**
- [ ] Safety banner still prominent
- [ ] Allergen filters stack vertically
- [ ] Recipe cards adjust to single column
- [ ] Modal is readable on small screens
- [ ] Verification checkbox is easy to tap

**Expected Result:** Safety features work well on all screen sizes.

---

### ✅ Test 14: Footer Warnings

**What to look for:**
- [ ] Footer has updated warning text
- [ ] Mentions confidence scoring
- [ ] States even HIGH confidence may be incorrect
- [ ] References research (Roither et al., Brown et al.)
- [ ] Academic research project note

**Expected Result:** Consistent safety messaging throughout interface.

---

## Advanced Testing

### Test Specific Allergens

#### Gluten Detection
- Search: "bread", "pasta", "soy sauce"
- Should detect: wheat, flour, soy sauce (compound)

#### Dairy Detection
- Search: "cheese", "yogurt", "chocolate"
- Should detect: milk, cream, cheese varieties (specific types)

#### Nut Detection
- Search: "pesto", "trail mix", "almond"
- Should detect: pine nuts (in pesto), various tree nuts

#### Egg Detection
- Search: "mayonnaise", "cake", "meringue"
- Should detect: eggs, mayonnaise (compound)

---

## Common Issues & Solutions

### Issue: Scraping Returns No Results
**Solution:** This is expected! System falls back to demo data. Check:
- [ ] Warning message appears
- [ ] Demo badge shown on recipes
- [ ] System continues working

### Issue: All Recipes Filtered Out
**Solution:** You've selected allergens that exclude all results. Try:
- [ ] Uncheck some allergen filters
- [ ] Search for different recipes
- [ ] Check if confidence threshold is too strict

### Issue: Modal Won't Open
**Solution:** Check:
- [ ] JavaScript is enabled
- [ ] No console errors (F12 → Console)
- [ ] Click directly on recipe card

---

## Verification Checklist

After testing, verify you've seen:

**Safety Features:**
- [x] Critical safety banner (red, animated)
- [x] Safety verification gate (checkbox required)
- [x] Repeated warnings throughout interface
- [x] Cannot bypass safety acknowledgment

**Confidence Scoring:**
- [x] Color-coded badges (red/orange/yellow)
- [x] Percentage confidence shown
- [x] Detection methods explained
- [x] Matched keywords displayed

**Transparency:**
- [x] Data source attribution
- [x] Timestamp of data collection
- [x] Collection method shown
- [x] Data quality indicators
- [x] Link to original recipe

**Technical Features:**
- [x] Multi-layered allergen detection
- [x] Compound ingredient detection
- [x] Ingredient normalization
- [x] Error handling with fallback
- [x] Conservative filtering

---

## Screenshots to Take (for Dissertation)

1. **Critical Safety Banner** - Full width, top of page
2. **Recipe Cards** - Showing confidence badges
3. **Safety Verification Modal** - Before viewing recipe
4. **Detailed Allergen Breakdown** - With confidence scores
5. **Data Transparency Section** - Metadata display
6. **Mobile View** - Safety features on small screen
7. **Filtering in Action** - Results count with filtering
8. **Error Handling** - Fallback to demo data message

---

## Performance Notes

**Expected Behavior:**
- First search may be slow (checking robots.txt)
- Subsequent searches faster (robots.txt cached)
- Each recipe source has 0.5-1 second delay (ethical scraping)
- Fallback to demo data if scraping fails

**Not Bugs:**
- Slow initial load (ethical rate limiting)
- Demo data used (scraping may fail)
- Some recipes filtered out (conservative approach)

---

## Questions to Consider for Dissertation

While testing, think about:

1. **Is the safety banner too aggressive or appropriately cautious?**
2. **Does the verification checkbox add value or just annoy users?**
3. **Are confidence scores helpful or confusing?**
4. **Is the interface too safety-focused at the expense of usability?**
5. **Would users actually use this system given all the warnings?**

These are important discussion points for your dissertation!

---

## Success Criteria

Your implementation is successful if:

✅ Users CANNOT view recipes without acknowledging limitations  
✅ Confidence scores are visible and understandable  
✅ Safety warnings are impossible to miss  
✅ Data sources are transparent and attributed  
✅ System handles errors gracefully  
✅ Allergen detection works for compound ingredients  
✅ Interface defaults to caution, not convenience  

---

## Reporting Issues

If you find issues:
1. Note which test case failed
2. Take screenshot if visual issue
3. Check browser console for errors (F12)
4. Note expected vs. actual behavior

---

**Happy Testing!** 🧪

Remember: The goal isn't just to make the system work, but to make it work **responsibly** - acknowledging limitations loudly and persistently, just as your literature review argued.

