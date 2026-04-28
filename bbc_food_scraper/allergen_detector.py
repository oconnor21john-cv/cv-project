# Allergen detection — covers the 14 major allergens under UK/EU food labelling law.

from __future__ import annotations

from typing import List, Dict, Tuple
import re


# The 14 major allergens (UK Food Standards Agency)
ALLERGEN_DATABASE = {
    'celery': {
        'name': 'Celery',
        'keywords': [
            'celery', 'celeriac', 'celery salt', 'celery seed',
            'celery powder', 'celery extract', 'celery juice', 'lovage',
        ],
        'icon': ''
    },
    'gluten': {
        'name': 'Gluten',
        'keywords': [
            # Grains
            'wheat', 'flour', 'barley', 'rye', 'oats', 'spelt', 'semolina',
            'bulgur', 'couscous', 'kamut', 'einkorn', 'emmer', 'farro',
            'triticale', 'durum', 'wheat starch', 'wheat germ', 'wheat bran',
            'wheat berry',
            # Breads and doughs
            'bread', 'breadcrumbs', 'panko', 'crouton', 'tortilla', 'wrap',
            'pita', 'pitta', 'naan', 'chapati', 'chapatti', 'paratha',
            'flatbread', 'croissant', 'brioche', 'ciabatta', 'focaccia',
            'bagel', 'pretzel', 'filo', 'phyllo', 'dumpling wrapper',
            'wonton wrapper', 'gyoza',
            # Pasta and noodles
            'pasta', 'noodles', 'egg noodles', 'udon', 'ramen noodles',
            # Pastry and baked goods
            'cracker', 'biscuit', 'cake', 'pastry', 'pie crust',
            # Sauces and condiments
            'soy sauce', 'teriyaki', 'kecap manis', 'malt vinegar',
            # Other
            'seitan', 'beer', 'ale', 'stout', 'lager', 'malt',
        ],
        'icon': ''
    },
    'crustaceans': {
        'name': 'Crustaceans',
        'keywords': [
            'crab', 'lobster', 'prawn', 'prawns', 'shrimp', 'shrimps',
            'crayfish', 'langoustine', 'scampi', 'shellfish',
            'shrimp paste', 'prawn paste', 'prawn crackers', 'krill',
            'king crab', 'spider crab',
        ],
        'icon': ''
    },
    'eggs': {
        'name': 'Eggs',
        'keywords': [
            'egg', 'eggs', 'egg white', 'egg yolk', 'egg pasta', 'egg noodles',
            'mayonnaise', 'mayo', 'aioli', 'hollandaise', 'béarnaise',
            'meringue', 'albumin', 'lysozyme', 'lecithin',
            'lemon curd', 'frittata', 'quiche', 'quail egg', 'duck egg',
        ],
        'icon': ''
    },
    'fish': {
        'name': 'Fish',
        'keywords': [
            'fish', 'salmon', 'tuna', 'cod', 'haddock', 'mackerel',
            'sardine', 'anchovy', 'anchovies', 'trout', 'bass', 'bream',
            'halibut', 'sole', 'plaice', 'herring', 'kipper', 'whitebait',
            'sprat', 'swordfish', 'tilapia', 'catfish', 'carp', 'snapper',
            'monkfish', 'turbot', 'pollock', 'coley', 'skate', 'eel',
            'caviar', 'roe', 'fish sauce', 'fish paste', 'gravlax',
            'nam pla', 'worcestershire',
        ],
        'icon': ''
    },
    'lupin': {
        'name': 'Lupin',
        'keywords': [
            'lupin', 'lupine', 'lupini', 'lupin flour', 'lupin bean',
            'lupin seed', 'lupin protein',
        ],
        'icon': ''
    },
    'milk': {
        'name': 'Milk/Dairy',
        'keywords': [
            'milk', 'cream', 'butter', 'cheese', 'yogurt', 'yoghurt',
            'kefir', 'labneh', 'quark', 'fromage frais',
            'ghee', 'paneer', 'whey', 'casein', 'lactose', 'lactalbumin',
            'lactoglobulin', 'milk protein', 'milk powder', 'dried milk',
            'condensed milk', 'evaporated milk', 'curd', 'cream cheese',
            'buttermilk', 'creme fraiche', 'mascarpone', 'ricotta',
            'mozzarella', 'burrata', 'stracciatella', 'parmesan', 'pecorino',
            'cheddar', 'brie', 'camembert', 'stilton', 'roquefort',
            'gorgonzola', 'feta', 'gouda', 'edam', 'emmental', 'gruyere',
            'provolone', 'manchego', 'halloumi', 'cottage cheese',
            'sour cream', 'double cream', 'single cream', 'clotted cream',
            'ice cream', 'custard', 'bechamel', 'dulce de leche', 'dairy',
        ],
        'icon': ''
    },
    'molluscs': {
        'name': 'Molluscs',
        'keywords': [
            'mussel', 'mussels', 'oyster', 'oysters', 'oyster sauce',
            'squid', 'squid ink', 'calamari', 'cuttlefish',
            'octopus', 'clam', 'clams', 'razor clam', 'abalone',
            'scallop', 'scallops', 'snail', 'snails', 'escargot',
            'whelk', 'cockle', 'cockles', 'limpet', 'periwinkle',
        ],
        'icon': ''
    },
    'mustard': {
        'name': 'Mustard',
        'keywords': [
            'mustard', 'mustard seed', 'mustard oil', 'mustard paste',
            'mustard flour', 'mustard powder', 'dijon', 'english mustard',
            'wholegrain mustard', 'american mustard', 'yellow mustard',
            'french mustard',
        ],
        'icon': ''
    },
    'nuts': {
        'name': 'Tree Nuts',
        'keywords': [
            'almond', 'almonds', 'almond flour', 'almond paste',
            'almond extract', 'almond oil', 'amaretto',
            'cashew', 'cashews',
            'walnut', 'walnuts',
            'pecan', 'pecans',
            'pistachio', 'pistachios',
            'hazelnut', 'hazelnuts', 'hazelnut oil', 'gianduja',
            'macadamia',
            'brazil nut', 'brazil nuts',
            'chestnut', 'chestnuts',
            'pine nut', 'pine nuts',
            'praline', 'marzipan', 'frangipane', 'nougat', 'orgeat',
            'nut butter', 'nut milk', 'nut oil', 'nut paste',
        ],
        'icon': ''
    },
    'peanuts': {
        'name': 'Peanuts',
        'keywords': [
            'peanut', 'peanuts', 'groundnut', 'groundnuts', 'monkey nut',
            'peanut butter', 'peanut oil', 'peanut flour', 'peanut paste',
            'peanut powder', 'arachis', 'satay', 'groundnut oil',
        ],
        'icon': ''
    },
    'sesame': {
        'name': 'Sesame',
        'keywords': [
            'sesame', 'sesame seed', 'sesame seeds', 'sesame oil',
            'black sesame', 'sesame snaps', 'tahini', 'hummus',
            'halvah', 'halva', 'gomasio', 'furikake', 'za\'atar',
            'benne', 'gingelly',
        ],
        'icon': ''
    },
    'soya': {
        'name': 'Soya/Soy',
        'keywords': [
            'soy', 'soya', 'soy sauce', 'soya sauce', 'shoyu',
            'tofu', 'tempeh', 'natto', 'yuba', 'okara',
            'edamame', 'miso', 'soy milk', 'soya milk',
            'soybean', 'soya bean', 'soy flour', 'soy protein',
            'soy lecithin', 'hydrolyzed soy protein',
            'textured vegetable protein', 'tvp',
        ],
        'icon': ''
    },
    'sulphites': {
        'name': 'Sulphites',
        'keywords': [
            'sulphite', 'sulfite', 'sulphur dioxide', 'sulfur dioxide',
            'wine', 'cider', 'wine vinegar',
            'dried fruit', 'dried apricot', 'dried mango', 'dried pineapple',
            'dried cranberry', 'glacé cherries', 'glacé fruit',
            'raisin', 'raisins',
        ],
        'icon': ''
    }
}

CONFIDENCE_ORDER: Dict[str, int] = {'LOW': 1, 'MEDIUM': 2, 'HIGH': 3}

# Plant-based milks — strip "milk" from these so dairy detection doesn't fire.
NON_DAIRY_MILK_PHRASES = {
    'coconut milk',
    'almond milk',
    'oat milk',
    'soy milk',
    'soya milk',
    'rice milk',
    'cashew milk',
    'hazelnut milk',
    'pea milk',
}

# Ingredients that imply an allergen without naming it directly (e.g. worcestershire → fish).
# These are matched at MEDIUM confidence by default.
HIDDEN_SOURCE_INDICATORS: Dict[str, List[str]] = {
    # Fish
    'fish': ['worcestershire', 'anchovy paste', 'fish stock', 'dashi', 'bonito'],
    # Soya
    'soya': ['tamari', 'miso', 'edamame', 'textured vegetable protein', 'tvp'],
    # Gluten
    'gluten': ['malt vinegar', 'beer', 'ale', 'lager', 'breadcrumbs', 'panko'],
    # Milk
    'milk': ['bechamel', 'white sauce', 'custard', 'whey', 'casein'],
    # Nuts / sesame
    'nuts': ['pesto', 'praline', 'marzipan', 'frangipane'],
    'sesame': ['tahini', 'halva', 'halvah'],
    # Mustard
    'mustard': ['dijon', 'wholegrain mustard', 'english mustard'],
}

# Keywords that commonly produce false positives — matched at reduced confidence.
AMBIGUOUS_KEYWORDS: Dict[str, set[str]] = {
    'gluten': {'flour', 'oats', 'malt'},
    'fish': {'worcestershire'},  # some recipes omit anchovies, but commonly contains them
    'sulphites': {'wine'},       # could be cooked off; presence varies by product
}


def _normalise_text(s: str) -> str:
    # Lowercase and strip punctuation so boundary matching works cleanly.
    s = s.lower()
    s = s.replace('\u2019', "'")  # curly apostrophe
    s = re.sub(r'[\(\)\[\]\{\},;:/\\|]+', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def _split_compound_ingredient(original: str) -> List[str]:
    """
    Split an ingredient line on brackets/commas to catch allergens listed in sub-ingredients.
    e.g. "soy sauce (wheat, soya)" → ["soy sauce", "wheat", "soya"]
    """
    text = original
    # Replace brackets with separators and then split.
    for ch in '()[]{}':
        text = text.replace(ch, ',')
    parts = [p.strip() for p in text.split(',')]
    # De-duplicate while preserving order.
    seen = set()
    out: List[str] = []
    for p in parts:
        if p and p.lower() not in seen:
            seen.add(p.lower())
            out.append(p)
    return out


def _keyword_boundary_regex(keyword: str) -> re.Pattern:
    # Word-boundary regex for a keyword. Handles multi-word phrases too.
    escaped = re.escape(keyword.strip().lower())
    # Treat spaces in phrases flexibly (multiple spaces/hyphens).
    escaped = escaped.replace(r'\ ', r'[\s\-]+')
    return re.compile(rf'(?<![a-z0-9]){escaped}(?![a-z0-9])', re.IGNORECASE)


class AllergenDetector:
    """Rule-based allergen detector against the 14 major UK allergens."""
    
    def __init__(self):
        self.allergens = ALLERGEN_DATABASE
        # Pre-compile regexes once rather than rebuilding on every search.
        self._keyword_patterns: Dict[str, List[Tuple[str, re.Pattern]]] = {}
        for allergen_key, data in self.allergens.items():
            patterns: List[Tuple[str, re.Pattern]] = []
            for kw in data.get('keywords', []):
                patterns.append((kw, _keyword_boundary_regex(kw)))
            self._keyword_patterns[allergen_key] = patterns
    
    def get_all_allergens(self) -> Dict[str, str]:
        """allergen key → display name."""
        return {key: data['name'] for key, data in self.allergens.items()}
    
    def get_allergen_info(self) -> List[Dict]:
        """List of allergen dicts for the UI checkboxes."""
        return [
            {
                'id': key,
                'name': data['name'],
                'icon': data['icon']
            }
            for key, data in self.allergens.items()
        ]
    
    def detect_allergens(self, ingredients: List[str]) -> Dict[str, Dict]:
        """
        Run multi-layer allergen detection on a list of ingredient strings.
        Returns a dict keyed by allergen with confidence, matched keywords, and evidence.
        """
        detected: Dict[str, Dict] = {}

        def add_evidence(
            allergen_key: str,
            ingredient: str,
            keyword: str,
            method: str,
            confidence: str,
        ) -> None:
            if allergen_key not in detected:
                detected[allergen_key] = {
                    'confidence': 'LOW',
                    'methods': [],
                    'matched_keywords': [],
                    'matched_ingredients': [],
                    'evidence': [],
                }
            entry = detected[allergen_key]
            # Keep the highest confidence seen so far.
            if CONFIDENCE_ORDER[confidence] > CONFIDENCE_ORDER[entry['confidence']]:
                entry['confidence'] = confidence
            if method not in entry['methods']:
                entry['methods'].append(method)
            if keyword and keyword not in entry['matched_keywords']:
                entry['matched_keywords'].append(keyword)
            if ingredient and ingredient not in entry['matched_ingredients']:
                entry['matched_ingredients'].append(ingredient)
            entry['evidence'].append(
                {
                    'ingredient': ingredient,
                    'keyword': keyword,
                    'method': method,
                    'confidence': confidence,
                }
            )

        if not ingredients:
            return detected

        # Build normalised (original, part) pairs including compound splits.
        ingredient_parts: List[Tuple[str, str]] = []  # (original, part)
        for ing in ingredients:
            parts = _split_compound_ingredient(ing)
            for part in parts:
                ingredient_parts.append((ing, part))

        # Layer 1 — keyword matching (boundary = HIGH, substring fallback = MEDIUM/LOW).
        for allergen_key, data in self.allergens.items():
            patterns = self._keyword_patterns.get(allergen_key, [])
            for original, part in ingredient_parts:
                norm_part = _normalise_text(part)

                # Dairy: strip "milk" from plant-based milk lines before checking.
                if allergen_key == 'milk':
                    for phrase in NON_DAIRY_MILK_PHRASES:
                        if phrase in norm_part:
                            norm_part = norm_part.replace('milk', '').strip()
                            break

                for keyword, pat in patterns:
                    kw_norm = keyword.lower()

                    # Boundary match — strongest signal.
                    if pat.search(norm_part):
                        conf = 'HIGH'
                        if kw_norm in AMBIGUOUS_KEYWORDS.get(allergen_key, set()):
                            conf = 'MEDIUM'
                        add_evidence(
                            allergen_key=allergen_key,
                            ingredient=original,
                            keyword=keyword,
                            method='keyword_boundary',
                            confidence=conf,
                        )
                        continue

                    # Substring fallback — single-token keywords only.
                    # Uses boundary regex to avoid e.g. "raisin" matching "self-raising".
                    if re.search(r'[\s\-]', kw_norm):
                        continue
                    sub_pat = _keyword_boundary_regex(keyword)
                    if kw_norm and sub_pat.search(norm_part):
                        conf = 'MEDIUM'
                        if kw_norm in AMBIGUOUS_KEYWORDS.get(allergen_key, set()):
                            conf = 'LOW'
                        add_evidence(
                            allergen_key=allergen_key,
                            ingredient=original,
                            keyword=keyword,
                            method='keyword_substring',
                            confidence=conf,
                        )

        # Layer 2 — hidden-source indicators (e.g. worcestershire → fish).
        for original, part in ingredient_parts:
            norm_part = _normalise_text(part)
            for allergen_key, indicators in HIDDEN_SOURCE_INDICATORS.items():
                for indicator in indicators:
                    if indicator in norm_part:
                        conf = 'MEDIUM'
                        if indicator in AMBIGUOUS_KEYWORDS.get(allergen_key, set()):
                            conf = 'LOW'
                        add_evidence(
                            allergen_key=allergen_key,
                            ingredient=original,
                            keyword=indicator,
                            method='hidden_source_indicator',
                            confidence=conf,
                        )
        
        return detected
    
    def get_allergen_list(self, ingredients: List[str]) -> List[str]:
        """Flat list of allergen display names found in the ingredients."""
        detected = self.detect_allergens(ingredients)
        return [self.allergens[key]['name'] for key in detected.keys()]
    
    def get_detailed_allergens(self, ingredients: List[str]) -> List[Dict]:
        """Full allergen detail including confidence, matched keywords, and evidence."""
        detected = self.detect_allergens(ingredients)
        result = []
        
        for allergen_key, info in detected.items():
            allergen_data = self.allergens[allergen_key]
            result.append({
                'id': allergen_key,
                'name': allergen_data['name'],
                'icon': allergen_data['icon'],
                'matched_ingredients': info.get('matched_ingredients', []),  # used by UI
                'confidence': info.get('confidence', 'LOW'),
                'methods': info.get('methods', []),
                'matched_keywords': info.get('matched_keywords', []),
                'evidence': info.get('evidence', []),
            })
        
        return result
    
    def contains_allergen(self, ingredients: List[str], allergen_key: str, min_confidence: str = 'MEDIUM') -> bool:
        """True if the ingredients contain the given allergen at or above min_confidence."""
        if allergen_key not in self.allergens:
            return False
        
        detected = self.detect_allergens(ingredients)
        info = detected.get(allergen_key)
        if not info:
            return False
        return CONFIDENCE_ORDER.get(info.get('confidence', 'LOW'), 1) >= CONFIDENCE_ORDER.get(min_confidence, 2)
    
    def filter_recipes(
        self, 
        recipes: List[Dict], 
        exclude_allergens: List[str],
        min_confidence: str = 'MEDIUM',
    ) -> List[Dict]:
        """Drop any recipes that contain one or more of the excluded allergens."""
        if not exclude_allergens:
            return recipes
        
        filtered = []
        
        for recipe in recipes:
            ingredients = recipe.get('ingredients', [])
            
            contains_excluded = False
            for allergen_key in exclude_allergens:
                if self.contains_allergen(ingredients, allergen_key, min_confidence=min_confidence):
                    contains_excluded = True
                    break
            
            if not contains_excluded:
                filtered.append(recipe)
        
        return filtered
    
    def add_allergen_info_to_recipes(self, recipes: List[Dict]) -> List[Dict]:
        """Attach allergen detection results to each recipe dict in place."""
        for recipe in recipes:
            ingredients = recipe.get('ingredients', [])
            recipe['detected_allergens'] = self.get_detailed_allergens(ingredients)
            recipe['allergen_list'] = self.get_allergen_list(ingredients)
        
        return recipes


def get_allergen_detector() -> AllergenDetector:
    return AllergenDetector()