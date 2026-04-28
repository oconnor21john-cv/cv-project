# Allergen-Filtered Recipe Search Tool

A web-based application that allows users to search for recipes and filter them by the 14 major allergen groups using web scraping techniques.

## Features

- **Recipe Search**: Search for recipes by name or ingredients
- **Allergen Filtering**: Filter recipes by 14 major allergen groups:
  1. Cereals containing gluten (wheat, rye, barley, oats)
  2. Crustaceans
  3. Eggs
  4. Fish
  5. Peanuts
  6. Soybeans
  7. Milk (dairy)
  8. Nuts (tree nuts)
  9. Celery
  10. Mustard
  11. Sesame seeds
  12. Sulphur dioxide and sulphites
  13. Lupin
  14. Molluscs

- **Web Scraping**: Automatically scrapes recipes from multiple sources
- **Modern UI**: Clean, responsive interface for easy recipe browsing
- **Recipe Details**: View full recipe information including ingredients, instructions, and allergen warnings

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Enter a search term (e.g., "chicken", "pasta", "salad")
2. Select allergens you want to exclude from the checkboxes
3. Click "Search Recipes"
4. Browse the filtered results
5. Click on any recipe to view full details

## Technical Details

- **Backend**: Flask (Python)
- **Web Scraping**: BeautifulSoup4 with requests
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Allergen Detection**: Keyword-based ingredient analysis

## Project Structure

```
.
├── app.py                 # Flask backend server
├── scraper.py            # Web scraping logic
├── allergen_detector.py  # Allergen detection system
├── static/
│   ├── css/
│   │   └── style.css    # Styling
│   └── js/
│       └── app.js       # Frontend logic
├── templates/
│   └── index.html       # Main HTML template
└── requirements.txt     # Python dependencies
```

## Notes

- This application scrapes publicly available recipe data
- Allergen detection is based on ingredient analysis and may not be 100% accurate
- Always verify allergen information before consuming if you have severe allergies
- Respect the robots.txt and terms of service of scraped websites

