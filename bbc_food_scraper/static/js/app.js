/**
 * Multi-Source Recipe Scraper - Frontend Application
 */

// State
let currentRecipes = [];
let lastQuery = '';
let allergenData = [];
let selectedAllergens = new Set();
let selectedSource = 'all'; // 'all' or one configured source key

// DOM Elements
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const resultsSection = document.getElementById('resultsSection');
const resultsTitle = document.getElementById('resultsTitle');
const resultsCount = document.getElementById('resultsCount');
const recipeGrid = document.getElementById('recipeGrid');
const loadingSection = document.getElementById('loadingSection');
const noResults = document.getElementById('noResults');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const retryBtn = document.getElementById('retryBtn');
const recipeModal = document.getElementById('recipeModal');
const modalContent = document.getElementById('modalContent');
const allergenToggle = document.getElementById('allergenToggle');
const allergenPanel = document.getElementById('allergenPanel');
const allergenGrid = document.getElementById('allergenGrid');
const clearAllergens = document.getElementById('clearAllergens');
const selectedCount = document.getElementById('selectedCount');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadAllergens();
    searchInput.focus();
});

/**
 * Setup all event listeners
 */
function setupEventListeners() {
    // Search
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch();
    });
    
    // Quick search buttons
    document.querySelectorAll('.quick-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            searchInput.value = btn.dataset.query;
            performSearch();
        });
    });
    
    // Retry button
    retryBtn.addEventListener('click', performSearch);
    
    // Modal close
    document.querySelector('.modal-close').addEventListener('click', closeModal);
    document.querySelector('.modal-backdrop').addEventListener('click', closeModal);
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
    });
    
    // Nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });
    
    // Allergen toggle
    allergenToggle.addEventListener('click', toggleAllergenPanel);
    
    // Clear allergens button
    clearAllergens.addEventListener('click', clearAllAllergens);
    
    // Source selection buttons
    document.querySelectorAll('.source-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.source-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            selectedSource = btn.dataset.source;
        });
    });
}

/**
 * Load allergens from API
 */
async function loadAllergens() {
    try {
        const response = await fetch('/api/allergens');
        const data = await response.json();
        
        if (data.success) {
            allergenData = data.allergens;
            renderAllergenFilters();
        }
    } catch (error) {
        console.error('Failed to load allergens:', error);
    }
}

/**
 * Render allergen filter checkboxes
 */
function renderAllergenFilters() {
    allergenGrid.innerHTML = '';
    
    allergenData.forEach(allergen => {
        const item = document.createElement('div');
        item.className = 'allergen-item';
        
        item.innerHTML = `
            <input type="checkbox" id="allergen-${allergen.id}" value="${allergen.id}">
            <label class="allergen-label" for="allergen-${allergen.id}">
                <span class="allergen-name">${allergen.name}</span>
            </label>
        `;
        
        const checkbox = item.querySelector('input');
        checkbox.addEventListener('change', () => {
            if (checkbox.checked) {
                selectedAllergens.add(allergen.id);
            } else {
                selectedAllergens.delete(allergen.id);
            }
            updateSelectedCount();
        });
        
        allergenGrid.appendChild(item);
    });
}

/**
 * Toggle allergen panel visibility
 */
function toggleAllergenPanel() {
    const isVisible = allergenPanel.style.display !== 'none';
    allergenPanel.style.display = isVisible ? 'none' : 'block';
    allergenToggle.classList.toggle('active', !isVisible);
}

/**
 * Clear all selected allergens
 */
function clearAllAllergens() {
    selectedAllergens.clear();
    allergenGrid.querySelectorAll('input').forEach(cb => cb.checked = false);
    updateSelectedCount();
}

/**
 * Update selected count display
 */
function updateSelectedCount() {
    const count = selectedAllergens.size;
    selectedCount.textContent = `${count} selected`;
    selectedCount.classList.toggle('has-selection', count > 0);
}

/**
 * Perform recipe search
 */
async function performSearch() {
    const query = searchInput.value.trim();
    
    if (!query) {
        searchInput.focus();
        return;
    }
    
    if (query.length < 2) {
        showError('Please enter at least 2 characters');
        return;
    }
    
    lastQuery = query;
    showLoading();
    
    try {
        // Build sources array based on selection
        let sources = null;
        if (selectedSource !== 'all') {
            sources = [selectedSource];
        }
        
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                query,
                exclude_allergens: Array.from(selectedAllergens),
                sources: sources
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Search failed');
        }
        
        if (data.success) {
            currentRecipes = data.recipes;
            displayResults(data);
        } else {
            throw new Error(data.error || 'Unknown error');
        }
        
    } catch (error) {
        console.error('Search error:', error);
        showError(error.message);
    }
}

/**
 * Display search results
 */
function displayResults(data) {
    hideAllSections();
    
    if (!data.recipes || data.recipes.length === 0) {
        noResults.style.display = 'block';
        return;
    }
    
    // Update header
    resultsTitle.textContent = `Results for "${data.query}"`;
    
    // Build count text with filter info and source counts
    let countText = `Found ${data.count} recipe${data.count !== 1 ? 's' : ''}`;
    
    // Add source breakdown
    if (data.source_counts && Object.keys(data.source_counts).length > 1) {
        const sourceParts = Object.entries(data.source_counts)
            .map(([source, count]) => `${count} from ${source}`)
            .join(', ');
        countText += ` (${sourceParts})`;
    }
    
    // Add filter info
    if (data.filtered_out > 0) {
        countText += ` • ${data.filtered_out} filtered out due to allergens`;
    }
    resultsCount.textContent = countText;
    
    // Render recipe cards
    renderRecipes(data.recipes);
    
    // Show results
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Render recipe cards
 */
function renderRecipes(recipes) {
    recipeGrid.innerHTML = '';
    
    recipes.forEach((recipe, index) => {
        const card = createRecipeCard(recipe, index);
        recipeGrid.appendChild(card);
    });
}

/**
 * Create a recipe card element
 */
function createRecipeCard(recipe, index) {
    const card = document.createElement('article');
    card.className = 'recipe-card';
    card.onclick = () => openRecipeModal(index);
    
    const imageUrl = recipe.image || `https://placehold.co/600x400/1f2937/c9a227?text=${encodeURIComponent(recipe.title.slice(0, 20))}`;
    
    // Build allergen tags HTML
    let allergenHtml = '';
    if (recipe.detected_allergens && recipe.detected_allergens.length > 0) {
        const confBadge = (a) => {
            const c = (a.confidence || '').toUpperCase();
            if (!c) return '';
            const cls = c === 'HIGH' ? 'high' : c === 'MEDIUM' ? 'medium' : 'low';
            return `<span class="allergen-confidence ${cls}">${c}</span>`;
        };
        allergenHtml = `
            <div class="recipe-allergens">
                ${recipe.detected_allergens.slice(0, 4).map(a => 
                    `<span class="allergen-tag">${a.name}${confBadge(a)}</span>`
                ).join('')}
                ${recipe.detected_allergens.length > 4 ? `<span class="allergen-tag">+${recipe.detected_allergens.length - 4}</span>` : ''}
            </div>
        `;
    } else {
        allergenHtml = `<div class="recipe-allergens"><span class="no-allergens-badge">No major allergens detected</span></div>`;
    }
    
    // Source badge with styling
    const source = recipe.source || 'Unknown';
    const sourceClass = source.toLowerCase().includes('bbc') ? 'bbc' : 
                        source.toLowerCase().includes('simply') ? 'simply' : 
                        source.toLowerCase().includes('serious') ? 'serious' : '';
    
    card.innerHTML = `
        <div class="recipe-image-container">
            <img 
                src="${escapeHtml(imageUrl)}" 
                alt="${escapeHtml(recipe.title)}" 
                class="recipe-image"
                onerror="this.src='https://placehold.co/600x400/1f2937/c9a227?text=Recipe'"
            >
            ${recipe.total_time ? `<span class="recipe-badge">${escapeHtml(recipe.total_time)}</span>` : ''}
        </div>
        <div class="recipe-content">
            <h3 class="recipe-title">${escapeHtml(recipe.title)}</h3>
            <div class="recipe-meta">
                ${recipe.servings ? `<span class="recipe-meta-item">${escapeHtml(recipe.servings)}</span>` : ''}
                ${recipe.author ? `<span class="recipe-meta-item">By ${escapeHtml(recipe.author)}</span>` : ''}
            </div>
            ${allergenHtml}
            ${recipe.description ? `<p class="recipe-description">${escapeHtml(recipe.description)}</p>` : ''}
        </div>
        <div class="recipe-footer">
            <span class="recipe-source-badge ${sourceClass}">${escapeHtml(source)}</span>
            <span class="view-recipe">View Recipe</span>
        </div>
    `;
    
    return card;
}

/**
 * Open recipe modal
 */
function openRecipeModal(index) {
    const recipe = currentRecipes[index];
    if (!recipe) return;
    
    const imageUrl = recipe.image || `https://placehold.co/800x400/1f2937/c9a227?text=${encodeURIComponent(recipe.title.slice(0, 20))}`;
    
    // Build allergen warning HTML
    let allergenWarningHtml = '';
    if (recipe.detected_allergens && recipe.detected_allergens.length > 0) {
        const formatEvidence = (a) => {
            // Prefer the most actionable evidence for display.
            const methods = Array.isArray(a.methods) ? a.methods : [];
            const keywords = Array.isArray(a.matched_keywords) ? a.matched_keywords : [];
            const ing = Array.isArray(a.matched_ingredients) ? a.matched_ingredients : [];

            const methodText = methods.length ? `Method: ${methods.join(', ')}` : '';
            const kwText = keywords.length ? `Matched: ${keywords.slice(0, 6).join(', ')}${keywords.length > 6 ? '…' : ''}` : '';
            const ingText = ing.length ? `From: ${ing.slice(0, 2).join(', ')}${ing.length > 2 ? '…' : ''}` : '';

            const bits = [ingText, kwText].filter(Boolean);
            return bits.length ? `<div class="modal-allergen-evidence">${bits.join(' • ')}</div>` : '';
        };

        const confLabel = (a) => {
            const c = (a.confidence || '').toUpperCase();
            if (!c) return '';
            const cls = c === 'HIGH' ? 'high' : c === 'MEDIUM' ? 'medium' : 'low';
            return `<span class="modal-allergen-confidence ${cls}">${c}</span>`;
        };

        allergenWarningHtml = `
            <div class="modal-allergen-warning">
                <h4>Allergen Information</h4>
                <p>This recipe may contain (automated detection):</p>
                <div class="modal-allergen-list">
                    ${recipe.detected_allergens.map(a => `
                        <div class="modal-allergen-item">
                            <div class="modal-allergen-row">
                                <span class="modal-allergen-name">${a.name}</span>
                                ${confLabel(a)}
                            </div>
                            ${formatEvidence(a)}
                        </div>
                    `).join('')}
                </div>
                <p class="allergen-disclaimer">Always check ingredient labels to confirm allergen information.</p>
            </div>
        `;
    }
    
    modalContent.innerHTML = `
        <img 
            src="${escapeHtml(imageUrl)}" 
            alt="${escapeHtml(recipe.title)}" 
            class="modal-image"
            onerror="this.src='https://placehold.co/800x400/1f2937/c9a227?text=Recipe'"
        >
        <div class="modal-body">
            <h2 class="modal-title">${escapeHtml(recipe.title)}</h2>
            
            <div class="modal-meta">
                ${recipe.prep_time ? `
                    <div class="modal-meta-item">
                        <span>Prep: ${escapeHtml(recipe.prep_time)}</span>
                    </div>
                ` : ''}
                ${recipe.cook_time ? `
                    <div class="modal-meta-item">
                        <span>Cook: ${escapeHtml(recipe.cook_time)}</span>
                    </div>
                ` : ''}
                ${recipe.servings ? `
                    <div class="modal-meta-item">
                        <span>Serves: ${escapeHtml(recipe.servings)}</span>
                    </div>
                ` : ''}
                ${recipe.author ? `
                    <div class="modal-meta-item">
                        <span>By ${escapeHtml(recipe.author)}</span>
                    </div>
                ` : ''}
            </div>
            
            ${allergenWarningHtml}
            
            ${recipe.description ? `
                <p class="modal-description">${escapeHtml(recipe.description)}</p>
            ` : ''}
            
            ${recipe.ingredients && recipe.ingredients.length > 0 ? `
                <div class="modal-section">
                    <h3>Ingredients</h3>
                    <ul class="ingredients-list">
                        ${recipe.ingredients.map(ing => `<li>${escapeHtml(ing)}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            
            ${recipe.instructions && recipe.instructions.length > 0 ? `
                <div class="modal-section">
                    <h3>Method</h3>
                    <ol class="instructions-list">
                        ${recipe.instructions.map(step => `<li>${escapeHtml(step)}</li>`).join('')}
                    </ol>
                </div>
            ` : ''}
        </div>
        
        <div class="modal-footer">
            <span class="modal-source">
                Source: ${escapeHtml(recipe.source || 'BBC Food')}
                ${recipe.extraction_method ? ` • ${escapeHtml(recipe.extraction_method)}` : ''}
            </span>
            ${recipe.url ? `
                <a href="${escapeHtml(recipe.url)}" target="_blank" rel="noopener noreferrer" class="modal-link">
                    View Original
                </a>
            ` : ''}
        </div>
    `;
    
    recipeModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

/**
 * Close recipe modal
 */
function closeModal() {
    recipeModal.style.display = 'none';
    document.body.style.overflow = '';
}

/**
 * Show loading state
 */
function showLoading() {
    hideAllSections();
    loadingSection.style.display = 'block';
    searchBtn.disabled = true;
    searchBtn.querySelector('.btn-text').style.display = 'none';
    searchBtn.querySelector('.btn-loading').style.display = 'flex';
}

/**
 * Show error state
 */
function showError(message) {
    hideAllSections();
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    resetSearchButton();
}

/**
 * Hide all content sections
 */
function hideAllSections() {
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'none';
    noResults.style.display = 'none';
    errorSection.style.display = 'none';
    resetSearchButton();
}

/**
 * Reset search button state
 */
function resetSearchButton() {
    searchBtn.disabled = false;
    searchBtn.querySelector('.btn-text').style.display = 'inline';
    searchBtn.querySelector('.btn-loading').style.display = 'none';
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = String(text);
    return div.innerHTML;
}

