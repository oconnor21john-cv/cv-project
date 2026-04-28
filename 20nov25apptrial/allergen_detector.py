"""
Allergen Detection System
Detects allergens in recipe ingredients based on the 14 major allergen groups

- Multi-layered detection (lexical, semantic, rule-based) - Roither et al. (2022)
- Hierarchical allergen taxonomy - Sharma et al. (2025)
- Ingredient normalization - Suwalka et al. (2023)
- Confidence scoring - addressing safety concerns from literature review
- Conservative error handling - prioritizing false positives over false negatives
"""

import re
from typing import List, Dict, Tuple, Set

class AllergenDetector:
    """
    Enhanced allergen detector implementing multi-layered detection approach
    Based on research by Roither et al. (2022) and Sharma et al. (2025)
    
    CRITICAL SAFETY NOTE:
    This system is designed to err on the side of caution. A 'low confidence' detection
    should be treated as seriously as a 'high confidence' detection when making dietary
    decisions. As noted in the literature review, even 90% accuracy means 1 in 10 recipes
    could be incorrectly classified - potentially fatal for severe allergies.
    """
    
    # D14 major allergen groups with keyword lists hierarchies
    ALLERGEN_GROUPS = {
        'gluten': {
            'name': 'Cereals containing gluten',
            'keywords': [
                'wheat', 'rye', 'barley', 'oats', 'spelt', 'kamut',
                'flour', 'bread', 'pasta', 'couscous', 'semolina',
                'bulgur', 'farro', 'durum', 'bran', 'cereal',
                'breadcrumbs', 'croutons', 'noodles', 'soy sauce',
                'seitan', 'udon', 'ramen', 'wheat flour', 'all-purpose flour',
                'self-raising flour', 'plain flour', 'whole wheat', 'wholemeal'
            ],
            'compound_ingredients': [
                'soy sauce', 'teriyaki sauce', 'hoisin sauce', 'bread',
                'pasta', 'noodles', 'crackers', 'cookies', 'cake', 'pastry'
            ],
            'hidden_sources': [
                'malt', 'modified food starch', 'hydrolyzed vegetable protein'
            ]
        },
        'crustaceans': {
            'name': 'Crustaceans',
            'keywords': [
                'crab', 'lobster', 'prawns', 'shrimp', 'crayfish',
                'langoustine', 'scampi', 'krill', 'barnacle'
            ]
        },
        'eggs': {
            'name': 'Eggs',
            'keywords': [
                'egg', 'eggs', 'mayonnaise', 'mayo', 'meringue',
                'albumin', 'lecithin', 'lysozyme', 'ovalbumin'
            ]
        },
        'fish': {
            'name': 'Fish',
            'keywords': [
                'fish', 'salmon', 'tuna', 'cod', 'haddock', 'anchovy',
                'anchovies', 'sardine', 'sardines', 'trout', 'bass',
                'mackerel', 'halibut', 'tilapia', 'worcestershire'
            ]
        },
        'peanuts': {
            'name': 'Peanuts',
            'keywords': [
                'peanut', 'peanuts', 'groundnut', 'groundnuts',
                'monkey nut', 'peanut butter', 'peanut oil'
            ]
        },
        'soybeans': {
            'name': 'Soybeans',
            'keywords': [
                'soy', 'soya', 'soybean', 'soybeans', 'tofu',
                'tempeh', 'edamame', 'miso', 'soy sauce',
                'soy milk', 'soy protein', 'textured vegetable protein',
                'tvp', 'lecithin'
            ]
        },
        'milk': {
            'name': 'Milk (Dairy)',
            'keywords': [
                'milk', 'dairy', 'cream', 'butter', 'cheese', 'yogurt',
                'yoghurt', 'whey', 'casein', 'lactose', 'ghee',
                'buttermilk', 'sour cream', 'creme fraiche',
                'parmesan', 'mozzarella', 'cheddar', 'ricotta',
                'mascarpone', 'paneer', 'custard', 'condensed milk',
                'evaporated milk', 'powdered milk', 'milk powder',
                'half and half', 'heavy cream', 'double cream',
                'single cream', 'clotted cream'
            ],
            'compound_ingredients': [
                'cheese', 'yogurt', 'ice cream', 'chocolate', 'butter',
                'custard', 'pudding', 'white sauce', 'bechamel', 'alfredo'
            ],
            'hidden_sources': [
                'whey protein', 'casein', 'lactose', 'milk solids',
                'milk powder', 'curds', 'lactalbumin', 'lactoglobulin'
            ],
            'specific_types': [
                'parmesan', 'mozzarella', 'cheddar', 'brie', 'camembert',
                'gouda', 'feta', 'ricotta', 'mascarpone', 'gruyere',
                'swiss cheese', 'blue cheese', 'goat cheese', 'cream cheese'
            ]
        },
        'nuts': {
            'name': 'Tree Nuts',
            'keywords': [
                'almond', 'almonds', 'hazelnut', 'hazelnuts', 'walnut',
                'walnuts', 'cashew', 'cashews', 'pecan', 'pecans',
                'brazil nut', 'brazil nuts', 'pistachio', 'pistachios',
                'macadamia', 'macadamias', 'pine nut', 'pine nuts',
                'chestnut', 'chestnuts', 'nut', 'nuts', 'marzipan',
                'praline', 'nougat', 'pesto', 'almond milk', 'almond flour',
                'nut butter', 'nutella', 'gianduja'
            ],
            'compound_ingredients': [
                'pesto', 'marzipan', 'praline', 'nougat', 'baklava',
                'nut butter', 'trail mix', 'granola', 'nutella'
            ],
            'hidden_sources': [
                'natural flavoring', 'artificial flavoring', 'nut oils'
            ],
            'specific_types': [
                'almond', 'hazelnut', 'walnut', 'cashew', 'pecan',
                'brazil nut', 'pistachio', 'macadamia', 'pine nut', 'chestnut'
            ]
        },
        'celery': {
            'name': 'Celery',
            'keywords': [
                'celery', 'celeriac', 'celery seed', 'celery salt'
            ]
        },
        'mustard': {
            'name': 'Mustard',
            'keywords': [
                'mustard', 'mustard seed', 'mustard powder',
                'dijon', 'wholegrain mustard'
            ]
        },
        'sesame': {
            'name': 'Sesame seeds',
            'keywords': [
                'sesame', 'tahini', 'sesame seed', 'sesame seeds',
                'sesame oil', 'hummus', 'halva'
            ]
        },
        'sulphites': {
            'name': 'Sulphur dioxide and sulphites',
            'keywords': [
                'sulphite', 'sulphites', 'sulfite', 'sulfites',
                'sulphur dioxide', 'sulfur dioxide', 'dried fruit',
                'wine', 'vinegar', 'pickled'
            ]
        },
        'lupin': {
            'name': 'Lupin',
            'keywords': [
                'lupin', 'lupine', 'lupin flour', 'lupin seeds'
            ]
        },
        'molluscs': {
            'name': 'Molluscs',
            'keywords': [
                'mussel', 'mussels', 'oyster', 'oysters', 'snail',
                'snails', 'squid', 'octopus', 'cuttlefish', 'clam',
                'clams', 'scallop', 'scallops', 'whelk', 'abalone'
            ]
        }
    }
    
    # Ingredient normalization patterns
    MEASUREMENT_PATTERNS = [
        r'\d+\s*(?:cup|cups|tablespoon|tablespoons|tbsp|teaspoon|teaspoons|tsp|ounce|ounces|oz|pound|pounds|lb|gram|grams|g|kilogram|kilograms|kg|milliliter|milliliters|ml|liter|liters|l)',
        r'\d+/\d+',  # Fractions
        r'\d+\.\d+',  # Decimals
        r'\d+',  # Plain numbers
    ]
    
    PREPARATION_PATTERNS = [
        r'\b(chopped|diced|sliced|minced|grated|shredded|crushed|ground|whole|fresh|dried|frozen|canned|cooked|raw|toasted|roasted|blanched|peeled)\b',
        r'\b(finely|coarsely|roughly|thinly|thickly)\b',
        r'\(.*?\)',  # Remove parenthetical notes
    ]
    
    @classmethod
    def normalize_ingredient(cls, ingredient: str) -> str:
        """
        Normalize ingredient text by removing measurements and preparation methods
        Implements approach from Suwalka et al. (2023)
        
        Args:
            ingredient: Raw ingredient string
            
        Returns:
            Normalized ingredient string
        """
        normalized = ingredient.lower().strip()
        
        # Remove measurements
        for pattern in cls.MEASUREMENT_PATTERNS:
            normalized = re.sub(pattern, '', normalized, flags=re.IGNORECASE)
        
        # Remove preparation methods
        for pattern in cls.PREPARATION_PATTERNS:
            normalized = re.sub(pattern, '', normalized, flags=re.IGNORECASE)
        
        # Remove extra whitespace
        normalized = ' '.join(normalized.split())
        
        # Remove common non-ingredient words
        stop_words = ['of', 'to', 'for', 'or', 'and', 'the', 'a', 'an', 'plus']
        words = normalized.split()
        words = [w for w in words if w not in stop_words]
        normalized = ' '.join(words)
        
        return normalized.strip()
    
    @classmethod
    def detect_allergens_with_confidence(cls, ingredients: List[str]) -> Dict[str, Dict]:
        """
        Enhanced allergen detection with confidence scoring
        Implements multi-layered approach from Roither et al. (2022)
        
        CRITICAL: Even 'low' confidence detections should be taken seriously.
        False positives are preferable to false negatives in health applications.
        
        Args:
            ingredients: List of ingredient strings
            
        Returns:
            Dictionary with allergen detection results and confidence scores
            Format: {
                'allergen_key': {
                    'detected': bool,
                    'confidence': str ('high', 'medium', 'low'),
                    'confidence_score': float (0-1),
                    'matched_keywords': list,
                    'detection_method': str
                }
            }
        """
        results = {}
        
        # Normalize all ingredients
        normalized_ingredients = [cls.normalize_ingredient(ing) for ing in ingredients]
        ingredients_text = ' '.join(normalized_ingredients).lower()
        raw_ingredients_text = ' '.join(ingredients).lower()
        
        for allergen_key, allergen_data in cls.ALLERGEN_GROUPS.items():
            matched_keywords = []
            detection_methods = []
            confidence_score = 0.0
            
            # Layer 1: Lexical Analysis - Direct keyword matching
            for keyword in allergen_data['keywords']:
                if keyword in ingredients_text or keyword in raw_ingredients_text:
                    matched_keywords.append(keyword)
                    detection_methods.append('lexical')
                    confidence_score = max(confidence_score, 0.9)  # High confidence
            
            # Layer 2: Compound Ingredient Detection
            if 'compound_ingredients' in allergen_data:
                for compound in allergen_data['compound_ingredients']:
                    if compound in ingredients_text or compound in raw_ingredients_text:
                        matched_keywords.append(f"{compound} (compound)")
                        detection_methods.append('compound')
                        confidence_score = max(confidence_score, 0.7)  # Medium confidence
            
            # Layer 3: Hidden Source Detection
            if 'hidden_sources' in allergen_data:
                for hidden in allergen_data['hidden_sources']:
                    if hidden in ingredients_text or hidden in raw_ingredients_text:
                        matched_keywords.append(f"{hidden} (hidden source)")
                        detection_methods.append('hidden_source')
                        confidence_score = max(confidence_score, 0.6)  # Medium-low confidence
            
            # Layer 4: Specific Type Detection (e.g., specific cheese types)
            if 'specific_types' in allergen_data:
                for specific in allergen_data['specific_types']:
                    if specific in ingredients_text or specific in raw_ingredients_text:
                        matched_keywords.append(f"{specific} (specific type)")
                        detection_methods.append('specific_type')
                        confidence_score = max(confidence_score, 0.85)  # High confidence
            
            # Determine confidence level
            detected = len(matched_keywords) > 0
            
            if confidence_score >= 0.8:
                confidence_level = 'high'
            elif confidence_score >= 0.6:
                confidence_level = 'medium'
            elif confidence_score > 0:
                confidence_level = 'low'
            else:
                confidence_level = 'none'
            
            results[allergen_key] = {
                'detected': detected,
                'confidence': confidence_level,
                'confidence_score': confidence_score,
                'matched_keywords': matched_keywords,
                'detection_method': ', '.join(set(detection_methods)) if detection_methods else 'none'
            }
        
        return results
    
    @classmethod
    def detect_allergens(cls, ingredients):
        """
        Detect allergens in a list of ingredients (backward compatible)
        
        Args:
            ingredients (list): List of ingredient strings
            
        Returns:
            dict: Dictionary with allergen groups as keys and boolean values
        """
        detailed_results = cls.detect_allergens_with_confidence(ingredients)
        
        # Convert to simple boolean format for backward compatibility
        return {key: result['detected'] for key, result in detailed_results.items()}
    
    @classmethod
    def get_allergen_list(cls, ingredients):
        """
        Get a list of allergen names present in ingredients
        
        Args:
            ingredients (list): List of ingredient strings
            
        Returns:
            list: List of allergen names detected
        """
        detected = cls.detect_allergens(ingredients)
        allergen_names = []
        
        for allergen_key, is_present in detected.items():
            if is_present:
                allergen_names.append(cls.ALLERGEN_GROUPS[allergen_key]['name'])
        
        return allergen_names
    
    @classmethod
    def get_allergen_list_with_confidence(cls, ingredients: List[str]) -> List[Dict]:
        """
        Get detailed allergen information with confidence scores
        
        Args:
            ingredients: List of ingredient strings
            
        Returns:
            List of dictionaries with allergen details
        """
        detailed_results = cls.detect_allergens_with_confidence(ingredients)
        allergen_details = []
        
        for allergen_key, result in detailed_results.items():
            if result['detected']:
                allergen_details.append({
                    'name': cls.ALLERGEN_GROUPS[allergen_key]['name'],
                    'key': allergen_key,
                    'confidence': result['confidence'],
                    'confidence_score': result['confidence_score'],
                    'matched_keywords': result['matched_keywords'],
                    'detection_method': result['detection_method']
                })
        
        # Sort by confidence score (highest first)
        allergen_details.sort(key=lambda x: x['confidence_score'], reverse=True)
        
        return allergen_details
    
    @classmethod
    def filter_by_allergens(cls, recipes, excluded_allergens, min_confidence='low'):
        """
        Filter recipes by excluding those with specified allergens
        
        CONSERVATIVE APPROACH: By default, excludes recipes even with 'low' confidence
        allergen detection, as recommended in the literature review.
        
        Args:
            recipes (list): List of recipe dictionaries
            excluded_allergens (list): List of allergen keys to exclude
            min_confidence (str): Minimum confidence level to trigger exclusion
                                 ('low', 'medium', 'high')
            
        Returns:
            list: Filtered list of recipes
        """
        filtered_recipes = []
        confidence_threshold = {'low': 0.0, 'medium': 0.6, 'high': 0.8}
        threshold = confidence_threshold.get(min_confidence, 0.0)
        
        for recipe in recipes:
            has_excluded = False
            
            # Check with confidence scores if available
            if 'allergen_details' in recipe:
                for allergen_detail in recipe['allergen_details']:
                    if allergen_detail['key'] in excluded_allergens:
                        if allergen_detail['confidence_score'] >= threshold:
                            has_excluded = True
                            break
            # Fallback to simple boolean check
            elif 'allergens' in recipe:
                for allergen in excluded_allergens:
                    if recipe['allergens'].get(allergen, False):
                        has_excluded = True
                        break
            
            if not has_excluded:
                filtered_recipes.append(recipe)
        
        return filtered_recipes
    
    @classmethod
    def get_safety_warning(cls, allergen_details: List[Dict]) -> str:
        """
        Generate appropriate safety warning based on allergen detections
        
        Args:
            allergen_details: List of detected allergens with confidence
            
        Returns:
            Safety warning string
        """
        if not allergen_details:
            return " CAUTION: No major allergens detected by automated system. Always verify ingredients manually."
        
        high_confidence = [a for a in allergen_details if a['confidence'] == 'high']
        medium_confidence = [a for a in allergen_details if a['confidence'] == 'medium']
        low_confidence = [a for a in allergen_details if a['confidence'] == 'low']
        
        warning = " ALLERGEN WARNING:\n"
        
        if high_confidence:
            warning += f"• HIGH CONFIDENCE: {', '.join([a['name'] for a in high_confidence])}\n"
        if medium_confidence:
            warning += f"• MEDIUM CONFIDENCE: {', '.join([a['name'] for a in medium_confidence])}\n"
        if low_confidence:
            warning += f"• LOW CONFIDENCE (verify manually): {', '.join([a['name'] for a in low_confidence])}\n"
        
        warning += "\n CRITICAL: Automated detection is NOT 100% accurate. "
        warning += "Always read ingredient labels carefully if you have severe allergies."
        
        return warning
    
    @classmethod
    def get_all_allergen_groups(cls):
        """
        Get all allergen groups with their display names
        
        Returns:
            dict: Dictionary of allergen keys and names
        """
        return {key: data['name'] for key, data in cls.ALLERGEN_GROUPS.items()}

