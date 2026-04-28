# Allergen-Filtered Recipe Search - Enhanced Safety Implementation

## 🎓 Academic Project - MSc Web Development

**Based on comprehensive literature review analyzing web scraping ethics and digital food allergen management systems.**

---

## ⚠️ CRITICAL SAFETY NOTICE

**This system implements automated allergen detection which is NOT 100% accurate.**

This implementation embodies the literature review's core argument:
> "Such systems should be built, but only if they are designed from the ground up to acknowledge their limitations loudly and persistently."

**Key Safety Features:**
- ✅ Prominent safety warnings (impossible to miss)
- ✅ Confidence scoring (transparency about accuracy)
- ✅ User verification required (active engagement)
- ✅ Conservative filtering (safety over convenience)
- ✅ Data transparency (full attribution and metadata)

---

## 📚 Literature Review Implementation

This project directly implements recommendations from:

- **Roither et al. (2022)** - Multi-layered allergen detection
- **Sharma et al. (2025)** - Hierarchical allergen taxonomy
- **Suwalka et al. (2023)** - Ingredient normalization
- **Brown et al. (2024)** - Ethical web scraping practices
- **Anaphylaxis UK (2023)** - 14 major allergen groups
- **Kelly (2024)** - Rising food allergy prevalence

---

## 🚀 Quick Start

### Installation

```bash
# Navigate to project directory
cd "c:\Users\John\Documents\Comp Sci Msc\web\it3\20nov25apptrial"

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Access
Open browser to: `http://localhost:5000`

---

## ✨ Enhanced Features

### 1. Multi-Layered Allergen Detection

Four detection layers for comprehensive allergen identification:

**Layer 1: Lexical Analysis (90% confidence)**
- Direct keyword matching
- Example: "milk" → Dairy allergen

**Layer 2: Compound Ingredients (70% confidence)**
- Detects allergens in composite foods
- Example: "pesto" → Contains tree nuts (pine nuts)

**Layer 3: Hidden Sources (60% confidence)**
- Identifies allergens in processing aids
- Example: "whey protein" → Contains milk

**Layer 4: Specific Types (85% confidence)**
- Recognizes specific varieties
- Example: "parmesan" → Dairy (milk) allergen

### 2. Confidence Scoring System

Every allergen detection includes:
- **Confidence Level:** HIGH / MEDIUM / LOW
- **Confidence Percentage:** Numerical accuracy (0-100%)
- **Detection Method:** How allergen was identified
- **Matched Keywords:** What triggered the detection

**Visual Indicators:**
- 🔴 RED badges = HIGH confidence (90%+)
- 🟠 ORANGE badges = MEDIUM confidence (60-90%)
- 🟡 YELLOW badges = LOW confidence (<60%)

### 3. Safety Verification Gate

**Before viewing ANY recipe, users must:**
1. Read safety limitations
2. Check verification box acknowledging:
   - Automated detection is NOT 100% accurate
   - They will manually verify ALL ingredients
   - Tool does not replace medical advice
   - They accept responsibility for verification

**Cannot be bypassed or skipped.**

### 4. Ingredient Normalization

Automatically handles variations in ingredient descriptions:
- Removes measurements: "2 cups milk" → "milk"
- Removes preparation: "chopped walnuts" → "walnuts"
- Removes descriptors: "fresh parmesan" → "parmesan"

Improves detection accuracy across different recipe formats.

### 5. Hierarchical Allergen Taxonomy

Enhanced allergen database structure:

```python
{
    'keywords': [...],           # Basic allergen terms
    'compound_ingredients': [...], # Foods containing allergen
    'hidden_sources': [...],      # Processing aids
    'specific_types': [...]       # Specific varieties
}
```

**Benefits:**
- Detects "pesto" as containing nuts (pine nuts)
- Identifies "soy sauce" may contain gluten (wheat)
- Recognizes "parmesan" contains milk (dairy)

### 6. Data Transparency & Attribution

Every recipe includes comprehensive metadata:
- **Source:** Where data came from (BBC, AllRecipes, etc.)
- **Timestamp:** When data was collected
- **Method:** How data was collected (scraping technique)
- **Quality:** Live scraped vs. demonstration data
- **Link:** Attribution to original recipe

### 7. Enhanced Error Handling

**Robust fallback mechanisms:**
- Individual error handling per source
- Graceful degradation to demo data
- Clear error messages
- System continues working even if scraping fails

**User Communication:**
- Transparent about when using demo data
- Explains why scraping may have failed
- Distinguishes live vs. mock data

### 8. Prominent Safety Warnings

**Multiple warning locations:**

**A. Critical Safety Banner (Top of Page)**
- Red gradient background
- Animated warning icon
- Cannot be dismissed
- States limitations clearly

**B. Recipe Card Warnings**
- Confidence-coded allergen badges
- "Verify manually" reminders
- Data quality indicators

**C. Modal Warnings**
- Detailed allergen breakdown
- Repeated verification reminders
- Confidence percentages
- Detection method transparency

---

## 🎯 Design Philosophy

### Safety Over Convenience

**Traditional Approach:**
- Disclaimers buried in terms of service
- Assumes accuracy is sufficient
- Focuses on user convenience
- Hides uncertainty

**Our Approach (Literature Review-Informed):**
- Warnings impossible to miss
- Acknowledges accuracy limitations
- Requires active user engagement
- Makes uncertainty visible

### Conservative Filtering

**Philosophy:** Better to exclude a safe recipe than include an unsafe one.

**Implementation:**
- Defaults to excluding even LOW confidence detections
- False positives preferred over false negatives
- Users can adjust confidence threshold if desired
- System errs on side of caution

---

## 📊 Technical Architecture

### Backend (`app.py`)
- Flask REST API
- Enhanced error handling
- Comprehensive logging
- Safety-aware responses

### Scraper (`scraper.py`)
- Ethical web scraping (robots.txt compliance)
- Rate limiting (0.5-1s delays)
- Multiple source support
- Fallback mechanisms
- Metadata tracking

### Allergen Detector (`allergen_detector.py`)
- Multi-layered detection
- Confidence scoring
- Ingredient normalization
- Hierarchical taxonomy
- Safety warning generation

### Frontend
- **HTML:** Safety banners, verification gates
- **JavaScript:** Confidence display, modal logic
- **CSS:** Color-coded badges, responsive warnings

---

## 🧪 Testing

See `TESTING_NEW_FEATURES.md` for comprehensive testing guide.

**Quick Test:**
1. Start application: `python app.py`
2. Notice red safety banner at top
3. Search for "pasta carbonara"
4. Click recipe → verify safety gate appears
5. Check box → view detailed allergen breakdown
6. Notice confidence scores and detection methods

---

## 📖 Documentation

### Main Documents
- **`LITERATURE_REVIEW_IMPLEMENTATION.md`** - Detailed implementation guide
- **`CHANGES_SUMMARY.md`** - Quick overview of changes
- **`TESTING_NEW_FEATURES.md`** - Comprehensive testing guide
- **`README_ENHANCED.md`** - This file

### Original Documents
- **`LITERATURE_REVIEW_FINAL.md`** - Complete literature review
- **`README.md`** - Original project documentation
- **`ETHICAL_COMPLIANCE_SUMMARY.md`** - Ethics documentation

---

## 🎓 For Your Dissertation

### Key Discussion Points

**1. Ethical Implementation**
- System embodies literature review arguments
- Prioritizes safety over convenience
- Makes limitations visible, not hidden

**2. Technical Innovation**
- Multi-layered detection approach
- Confidence scoring system
- Hierarchical allergen taxonomy
- Conservative filtering strategy

**3. User Experience Trade-offs**
- Safety warnings vs. usability
- Verification requirements vs. convenience
- Transparency vs. simplicity

**4. Research Contributions**
- Bridges gap between technical and ethical literature
- Demonstrates responsible health technology design
- Provides framework for similar systems

### Strengths to Highlight

✅ **Research-Informed:** Directly implements academic recommendations  
✅ **Safety-First:** Prioritizes user safety over convenience  
✅ **Transparent:** Makes uncertainty and limitations visible  
✅ **Conservative:** Errs on side of caution  
✅ **Ethical:** Respects data sources and end users  

### Limitations to Discuss

⚠️ **Accuracy:** Not 100% accurate (acknowledged throughout)  
⚠️ **Usability:** Safety features may reduce convenience  
⚠️ **Scraping:** Dependent on website structure (may break)  
⚠️ **Coverage:** Limited to 14 major allergens  
⚠️ **Verification:** Relies on user compliance  

---

## 🔬 Future Enhancements

### Potential Improvements

**1. Machine Learning Integration**
- Train models on annotated datasets
- Improve semantic understanding
- Better ambiguity handling

**2. User Feedback Loop**
- Report incorrect detections
- Build verified recipe database
- Improve algorithms based on feedback

**3. Cross-Contamination Detection**
- Detect "may contain" warnings
- Identify shared equipment risks
- Warn about preparation methods

**4. API Integration**
- Use official recipe APIs
- Reduce scraping dependency
- Improve data quality

**5. Additional Dietary Restrictions**
- Vegetarian/vegan filtering
- Religious dietary laws
- Low-sodium, low-sugar, etc.

---

## 📚 References

### Key Academic Sources

**Allergen Detection:**
- Roither, A., Kurz, M. and Sonnleitner, E. (2022) 'The Chef's Choice: system for allergen and style classification in recipes', Applied Sciences, 12(5), p. 2590.

**Web Scraping:**
- Brown, M.A. et al. (2024) Web Scraping for research: legal, ethical, institutional, and scientific considerations.
- Suwalka, N. et al. (2023) 'Food Genie, Recipe Search Algorithm Using Web Scraping', ASIANCON.

**Public Health:**
- Kelly, M. (2024) Rising Trends in Food Allergies: A 20-Year Study from England.
- Anaphylaxis UK (2023) The 14 Major Food Allergens.

**System Design:**
- Sharma, P. et al. (2025) 'Food allergen detection and recommendation', SSRN Electronic Journal.

---

## 🛡️ Safety Disclaimer

**CRITICAL NOTICE:**

This system is an academic research project demonstrating ethical web scraping and allergen detection. It is NOT intended for production use without extensive testing and validation.

**Limitations:**
- Automated detection is NOT 100% accurate
- May miss allergens or incorrectly identify safe foods
- Dependent on website structure (scraping may fail)
- Limited to 14 major allergen groups
- Does not detect cross-contamination
- Cannot replace medical advice

**Users with severe food allergies should:**
- Always verify ingredients manually
- Consult with healthcare providers
- Read original recipe sources
- Never rely solely on automated detection
- Understand the risks of false negatives

---

## 📞 Contact & Attribution

**Project:** MSc Web Development - Allergen-Filtered Recipe Search  
**Institution:** [Your Institution]  
**Purpose:** Academic Research & Educational Demonstration  
**License:** Educational Use Only

**Data Sources:**
- AllRecipes.com (with robots.txt compliance)
- BBC Good Food (with robots.txt compliance)
- Mock data for demonstration purposes

**Attribution:**
All scraped recipes include links to original sources and clear attribution to content creators.

---

## 🎯 Core Principle

This project embodies the literature review's central argument:

> "The question is whether a system designed with these limitations in mind, that makes uncertainty visible and demands active user engagement, can still provide value while minimising harm."

**Answer:** Yes, through:
- Transparent design
- Conservative filtering
- Visible confidence scoring
- Mandatory user verification
- Persistent safety warnings

**The gap between what we can build and what we should build is bridged by honest acknowledgment of limitations and safety-first design.**

---

**Version:** 2.0 (Enhanced Safety Implementation)  
**Date:** December 1, 2025  
**Status:** Academic Research Project

