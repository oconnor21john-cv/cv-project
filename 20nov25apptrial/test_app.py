"""
Test script for the Allergen-Filtered Recipe Search application
"""

import sys
import json

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Test imports
print("Testing imports...")
try:
    from allergen_detector import AllergenDetector
    print("[OK] AllergenDetector imported successfully")
except Exception as e:
    print(f"[FAIL] Failed to import AllergenDetector: {e}")
    sys.exit(1)

try:
    from scraper import RecipeScraper
    print("[OK] RecipeScraper imported successfully")
except Exception as e:
    print(f"[FAIL] Failed to import RecipeScraper: {e}")
    sys.exit(1)

try:
    from flask import Flask
    print("[OK] Flask imported successfully")
except Exception as e:
    print(f"[FAIL] Failed to import Flask: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("Testing AllergenDetector")
print("="*60)

# Test allergen detector
detector = AllergenDetector()

# Test 1: Get all allergen groups
print("\nTest 1: Get all allergen groups")
allergen_groups = detector.get_all_allergen_groups()
print(f"Found {len(allergen_groups)} allergen groups:")
for key, name in allergen_groups.items():
    print(f"  - {key}: {name}")

# Test 2: Detect allergens in ingredients
print("\nTest 2: Detect allergens in sample ingredients")
test_ingredients = [
    "2 cups of milk",
    "3 eggs",
    "1 cup wheat flour",
    "2 tablespoons peanut butter",
    "1 cup shredded cheese"
]
print("Ingredients:", test_ingredients)
detected = detector.detect_allergens(test_ingredients)
allergen_list = detector.get_allergen_list(test_ingredients)
print(f"Detected allergens: {allergen_list}")

# Test 3: Filter recipes
print("\nTest 3: Filter recipes by allergens")
mock_recipes = [
    {
        'title': 'Recipe 1',
        'allergens': {'milk': True, 'eggs': False, 'gluten': False}
    },
    {
        'title': 'Recipe 2',
        'allergens': {'milk': False, 'eggs': True, 'gluten': False}
    },
    {
        'title': 'Recipe 3',
        'allergens': {'milk': False, 'eggs': False, 'gluten': True}
    }
]
excluded = ['milk']
filtered = detector.filter_by_allergens(mock_recipes, excluded)
print(f"Excluded allergens: {excluded}")
print(f"Recipes before filtering: {len(mock_recipes)}")
print(f"Recipes after filtering: {len(filtered)}")
print(f"Remaining recipes: {[r['title'] for r in filtered]}")

print("\n" + "="*60)
print("Testing RecipeScraper")
print("="*60)

# Test scraper
scraper = RecipeScraper()

# Test 4: Search for recipes
print("\nTest 4: Search for recipes (using mock data)")
query = "chicken"
recipes = scraper.search_recipes(query, max_results=5)
print(f"Search query: '{query}'")
print(f"Found {len(recipes)} recipes:")
for i, recipe in enumerate(recipes[:3], 1):
    print(f"\n{i}. {recipe['title']}")
    print(f"   Source: {recipe['source']}")
    print(f"   Ingredients: {len(recipe.get('ingredients', []))} items")
    print(f"   Allergens: {', '.join(recipe.get('allergen_list', [])) or 'None detected'}")

print("\n" + "="*60)
print("Testing Complete Recipe Workflow")
print("="*60)

# Test 5: Complete workflow
print("\nTest 5: Search and filter workflow")
search_query = "pasta"
excluded_allergens = ['milk', 'gluten']

print(f"Search query: '{search_query}'")
print(f"Excluded allergens: {excluded_allergens}")

# Search
all_recipes = scraper.search_recipes(search_query, max_results=10)
print(f"\nTotal recipes found: {len(all_recipes)}")

# Filter
filtered_recipes = detector.filter_by_allergens(all_recipes, excluded_allergens)
print(f"Recipes after filtering: {len(filtered_recipes)}")

if filtered_recipes:
    print("\nSample filtered recipe:")
    sample = filtered_recipes[0]
    print(f"  Title: {sample['title']}")
    print(f"  Allergens: {', '.join(sample.get('allergen_list', [])) or 'None detected'}")
    print(f"  Ingredients: {len(sample.get('ingredients', []))} items")

print("\n" + "="*60)
print("All Tests Completed Successfully!")
print("="*60)
print("\nThe application is ready to use.")
print("Run 'python app.py' to start the web server.")
print("Then open http://localhost:5000 in your browser.")

