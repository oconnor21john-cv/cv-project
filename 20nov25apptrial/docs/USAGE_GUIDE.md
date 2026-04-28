# Allergen-Filtered Recipe Search - Usage Guide

## Quick Start

### 1. Installation

First, install the required Python packages:

```bash
pip install -r requirements.txt
```

### 2. Run the Application

Start the Flask server:

```bash
python app.py
```

The application will start on `http://localhost:5000`

### 3. Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## How to Use

### Searching for Recipes

1. **Enter a Search Term**: Type what you're looking for in the search box (e.g., "chicken", "pasta", "salad", "soup")

2. **Select Allergens to Exclude**: Check the boxes for any allergens you want to avoid:
   - Cereals containing gluten (wheat, rye, barley, oats)
   - Crustaceans
   - Eggs
   - Fish
   - Peanuts
   - Soybeans
   - Milk (Dairy)
   - Tree Nuts
   - Celery
   - Mustard
   - Sesame seeds
   - Sulphur dioxide and sulphites
   - Lupin
   - Molluscs

3. **Click "Search Recipes"**: The application will search and filter recipes based on your criteria

4. **Browse Results**: Scroll through the recipe cards to see what's available

5. **View Recipe Details**: Click on any recipe card to see:
   - Full ingredient list
   - Step-by-step instructions
   - Detailed allergen information
   - Source and original recipe link (when available)

## Features Explained

### Allergen Detection

The application automatically analyzes recipe ingredients and detects the presence of the 14 major allergen groups. Each recipe card shows:

- ✓ **Green checkmark**: No major allergens detected
- ⚠️ **Warning tags**: Lists specific allergens found in the recipe

### Filtering

When you select allergens to exclude:
- Recipes containing those allergens are automatically removed from results
- The results count shows how many recipes were filtered
- You can adjust filters and search again at any time

### Recipe Details

Click any recipe to see:
- **Full ingredient list**: All ingredients needed
- **Step-by-step instructions**: Detailed cooking directions
- **Allergen warnings**: Comprehensive list of detected allergens
- **Source information**: Where the recipe came from
- **Original recipe link**: Visit the source website (when available)

## Example Searches

### Example 1: Dairy-Free Chicken Recipes
1. Enter "chicken" in the search box
2. Check the "Milk (Dairy)" allergen box
3. Click "Search Recipes"
4. Browse dairy-free chicken recipes

### Example 2: Gluten and Egg-Free Salads
1. Enter "salad" in the search box
2. Check both "Cereals containing gluten" and "Eggs"
3. Click "Search Recipes"
4. View salads without gluten or eggs

### Example 3: Nut-Free Desserts
1. Enter "dessert" or "cake" in the search box
2. Check "Tree Nuts" and "Peanuts"
3. Click "Search Recipes"
4. Find nut-free dessert options

## Technical Details

### Web Scraping

The application uses web scraping to gather recipe data from various sources:
- **BeautifulSoup4**: Parses HTML content
- **Requests**: Fetches web pages
- **Mock Data**: Provides demo recipes when scraping is unavailable

### Allergen Detection Algorithm

The system uses keyword-based detection:
1. Analyzes all ingredients in a recipe
2. Searches for allergen-related keywords
3. Categorizes findings into the 14 major allergen groups
4. Provides comprehensive allergen information

### API Endpoints

The backend provides these REST API endpoints:

- `GET /api/allergens`: Get all allergen groups
- `POST /api/search`: Search and filter recipes
  ```json
  {
    "query": "chicken",
    "excluded_allergens": ["milk", "gluten"]
  }
  ```
- `GET /health`: Health check endpoint

## Important Notes

### ⚠️ Allergen Detection Accuracy

**IMPORTANT**: The allergen detection is automated and based on ingredient analysis. It may not be 100% accurate. 

- Always verify ingredients if you have severe allergies
- Check the original recipe source for complete allergen information
- Consult with healthcare professionals for dietary restrictions
- Cross-contamination is not accounted for in this tool

### Web Scraping Considerations

- Respect website terms of service
- The application includes rate limiting and delays
- Some websites may block automated access
- Recipe availability depends on source websites
- Mock data is used for demonstration purposes

## Troubleshooting

### Application Won't Start

**Error**: `ModuleNotFoundError`
- **Solution**: Install dependencies with `pip install -r requirements.txt`

**Error**: `Port already in use`
- **Solution**: Stop other applications using port 5000, or change the port in `app.py`

### No Results Found

**Issue**: Search returns no results
- **Solution**: Try different search terms
- **Solution**: Reduce the number of excluded allergens
- **Solution**: Check your internet connection (for real scraping)

### Recipes Not Loading

**Issue**: Recipes don't appear or images are broken
- **Solution**: This is normal - the app uses mock data by default
- **Solution**: To enable real scraping, uncomment the scraping lines in `scraper.py`

### Modal Won't Close

**Issue**: Recipe detail modal stuck open
- **Solution**: Press the Escape key
- **Solution**: Click outside the modal
- **Solution**: Refresh the page

## Customization

### Adding More Recipe Sources

To add more recipe sources, edit `scraper.py`:

1. Create a new scraping method:
```python
def scrape_new_source(self, query, max_results=10):
    # Your scraping logic here
    pass
```

2. Add it to the `search_recipes` method:
```python
all_recipes.extend(self.scrape_new_source(query, max_results // 3))
```

### Modifying Allergen Keywords

To improve allergen detection, edit `allergen_detector.py`:

1. Find the `ALLERGEN_GROUPS` dictionary
2. Add keywords to the relevant allergen group:
```python
'milk': {
    'name': 'Milk (Dairy)',
    'keywords': [
        'milk', 'dairy', 'cream', 'butter',
        # Add your keywords here
        'your_new_keyword'
    ]
}
```

### Styling Changes

To customize the appearance, edit `static/css/style.css`:
- Change colors, fonts, layouts
- Modify the gradient backgrounds
- Adjust card styles and spacing

## Performance Tips

1. **Limit Results**: Reduce `max_results` in search requests for faster loading
2. **Cache Results**: Implement caching for frequently searched terms
3. **Database**: Store scraped recipes in a database for better performance
4. **Async Scraping**: Use async/await for parallel scraping

## Future Enhancements

Potential improvements for this application:

- [ ] Database integration for storing recipes
- [ ] User accounts and saved recipes
- [ ] Recipe ratings and reviews
- [ ] Nutritional information
- [ ] Meal planning features
- [ ] Shopping list generation
- [ ] More recipe sources
- [ ] Advanced search filters (cuisine, cooking time, difficulty)
- [ ] Recipe recommendations
- [ ] Mobile app version

## Support

For issues, questions, or contributions:
- Check the README.md file
- Review the code documentation
- Test with different search terms
- Verify your Python environment

## License

This project is for educational purposes. Always respect the terms of service of websites you scrape from.

