"""
Flask app for allergen-filtered recipe search
MSc Web Development Project - Allergen Management System
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from scraper import RecipeScraper
from allergen_detector import AllergenDetector
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

scraper = RecipeScraper()
allergen_detector = AllergenDetector()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/allergens', methods=['GET'])
def get_allergens():
    # Return the 14 major allergen groups for the filter UI
    allergen_groups = allergen_detector.get_all_allergen_groups()
    return jsonify({
        'success': True,
        'allergens': allergen_groups
    })


@app.route('/api/search', methods=['POST'])
def search_recipes():
    # Main search endpoint - handles recipe queries with allergen filtering
    try:
        data = request.get_json()
        
        if not data:
            logger.warning("Empty request received")
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        query = data.get('query', '').strip()
        excluded_allergens = data.get('excluded_allergens', [])
        min_confidence = data.get('min_confidence', 'low')
        
        if not query:
            return jsonify({'success': False, 'error': 'Search query is required'}), 400
        
        logger.info(f"Search: '{query}' | Excluding: {excluded_allergens}")
        
        # Get recipes from scraper
        recipes = scraper.search_recipes(query, max_results=20)
        
        # Add safety warnings based on detected allergens
        for recipe in recipes:
            if 'allergen_details' in recipe:
                recipe['safety_warning'] = allergen_detector.get_safety_warning(
                    recipe['allergen_details']
                )
        
        # Apply allergen filtering if user selected any exclusions
        if excluded_allergens:
            filtered_recipes = allergen_detector.filter_by_allergens(
                recipes, excluded_allergens, min_confidence=min_confidence
            )
        else:
            filtered_recipes = recipes
        
        logger.info(f"Results: {len(recipes)} total, {len(filtered_recipes)} after filtering")
        
        # Build response with safety information
        # This disclaimer is critical - automated detection isn't perfect
        response_data = {
            'success': True,
            'query': query,
            'total_results': len(recipes),
            'filtered_results': len(filtered_recipes),
            'excluded_allergens': excluded_allergens,
            'recipes': filtered_recipes,
            'safety_disclaimer': (
                "CRITICAL SAFETY NOTICE: Automated allergen detection is NOT 100% accurate. "
                "This system may miss allergens or incorrectly identify safe foods as containing allergens. "
                "ALWAYS verify ingredients manually if you have severe food allergies. "
                "This tool is for informational purposes only and should not replace professional "
                "medical advice or careful ingredient verification."
            ),
            'detection_confidence_note': (
                "Confidence levels indicate detection reliability: "
                "HIGH (90%+), MEDIUM (60-90%), LOW (<60%). "
                "Even LOW confidence detections should be taken seriously."
            )
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        logger.error(f"Search failed: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e),
            'safety_note': 'An error occurred. Please try again or verify ingredients manually.'
        }), 500


@app.route('/api/recipe/<int:recipe_id>', methods=['GET'])
def get_recipe_detail(recipe_id):
    # Placeholder for future database implementation
    # Currently recipes are fetched fresh each search
    return jsonify({
        'success': True,
        'message': 'Recipe detail endpoint - implement with database'
    })


@app.route('/health', methods=['GET'])
def health_check():
    # Simple health check for monitoring
    return jsonify({
        'status': 'healthy',
        'service': 'Allergen-Filtered Recipe Search API'
    })


if __name__ == '__main__':
    # Make sure required directories exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

