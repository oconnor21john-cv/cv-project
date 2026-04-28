"""
Recipe Scraper - Flask Web Application
Focused live scraping from multiple recipe websites
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from scraper import MultiSourceScraper
from allergen_detector import AllergenDetector
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize multi-source scraper and allergen detector
scraper = MultiSourceScraper()
allergen_detector = AllergenDetector()

# Available sources for filtering
AVAILABLE_SOURCES = {
    'bbc': 'BBC Food',
    'bbcgoodfood': 'BBC Good Food',
    'tomkerridge': 'Tom Kerridge',
    'foodafactoflife': 'Food - a Fact of Life',
    'realfooddietitians': 'The Real Food Dietitians',
    'ocado': 'Ocado',
}


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/allergens', methods=['GET'])
def get_allergens():
    """Get list of allergens for filtering"""
    return jsonify({
        'success': True,
        'allergens': allergen_detector.get_allergen_info()
    })


@app.route('/api/sources', methods=['GET'])
def get_sources():
    """Get available recipe sources"""
    return jsonify({
        'success': True,
        'sources': [
            {'id': key, 'name': name}
            for key, name in AVAILABLE_SOURCES.items()
        ]
    })


@app.route('/api/search', methods=['POST'])
def search_recipes():
    """Search for recipes by query with optional allergen and source filtering"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        query = data.get('query', '').strip()
        exclude_allergens = data.get('exclude_allergens', [])
        sources = data.get('sources', None)  # None means all sources
        
        if not query:
            return jsonify({'success': False, 'error': 'Search query required'}), 400
        
        if len(query) < 2:
            return jsonify({'success': False, 'error': 'Query too short'}), 400
        
        logger.info(f"Searching for: {query} | Sources: {sources or 'all'} | Excluding allergens: {exclude_allergens}")
        
        # Try to scrape real recipes from selected sources
        recipes = scraper.search_recipes(query, max_results=15, sources=sources)
        source_status = scraper.get_last_source_status()

        unavailable_sources = [
            status['name']
            for status in source_status.values()
            if status.get('status') in ('temporarily_unavailable', 'unavailable', 'error')
        ]
        unavailable_details = [
            f"{status.get('name')}: {status.get('message')}"
            for status in source_status.values()
            if status.get('status') in ('temporarily_unavailable', 'unavailable', 'error')
        ]
        
        # Add allergen info to all recipes
        recipes = allergen_detector.add_allergen_info_to_recipes(recipes)
        total_before_filter = len(recipes)
        
        # Filter out recipes with excluded allergens
        if exclude_allergens:
            # Safety-first default: filter on MEDIUM+ confidence matches.
            # LOW confidence matches are still displayed in the UI as "possible".
            recipes = allergen_detector.filter_recipes(recipes, exclude_allergens, min_confidence='MEDIUM')
            filtered_count = total_before_filter - len(recipes)
            logger.info(f"Filtered out {filtered_count} recipes containing excluded allergens")
        
        # Count recipes by source
        source_counts = {}
        for recipe in recipes:
            src = recipe.get('source', 'Unknown')
            source_counts[src] = source_counts.get(src, 0) + 1
        
        return jsonify({
            'success': True,
            'query': query,
            'count': len(recipes),
            'total_found': total_before_filter,
            'filtered_out': total_before_filter - len(recipes),
            'exclude_allergens': exclude_allergens,
            'source_counts': source_counts,
            'source_status': source_status,
            'unavailable_sources': unavailable_sources,
            'unavailable_details': unavailable_details,
            'recipes': recipes,
            'message': (
                f"Some sources are unavailable: {'; '.join(unavailable_details)}"
                if unavailable_details else None
            )
        })
        
    except Exception as e:
        logger.error(f"Search error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Search failed. Please try again.'
        }), 500


@app.route('/api/featured', methods=['GET'])
def get_featured():
    """Get featured recipes (BBC Food fallback)"""
    try:
        logger.info("Fetching featured recipes")
        
        recipes = scraper.get_featured_recipes(max_results=6)
        
        return jsonify({
            'success': True,
            'count': len(recipes),
            'recipes': recipes or []
        })
        
    except Exception as e:
        logger.error(f"Featured recipes error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Could not fetch featured recipes'
        }), 500


@app.route('/api/recipe', methods=['POST'])
def get_recipe():
    """Get a specific recipe by URL"""
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        if not url:
            return jsonify({'success': False, 'error': 'Invalid recipe URL'}), 400
        
        recipe = scraper.scrape_recipe(url)
        
        if recipe:
            return jsonify({
                'success': True,
                'recipe': recipe
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Could not fetch recipe'
            }), 404
            
    except Exception as e:
        logger.error(f"Recipe fetch error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Could not fetch recipe'
        }), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Multi-Source Recipe Scraper',
        'sources': list(AVAILABLE_SOURCES.values())
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

