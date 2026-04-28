/**
 * Frontend JavaScript for Allergen-Filtered Recipe Search
 */

// Global state
let currentRecipes = [];
let allergenGroups = {};
let currentRecipeIndex = null;

// DOM Elements
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const allergenFilters = document.getElementById('allergenFilters');
const resultsSection = document.getElementById('resultsSection');
const recipeGrid = document.getElementById('recipeGrid');
const resultsTitle = document.getElementById('resultsTitle');
const resultsCount = document.getElementById('resultsCount');
const noResults = document.getElementById('noResults');
const loadingIndicator = document.getElementById('loadingIndicator');
const recipeModal = document.getElementById('recipeModal');
const modalBody = document.getElementById('modalBody');
const safetyVerification = document.getElementById('safetyVerification');
const safetyAcknowledge = document.getElementById('safetyAcknowledge');
const proceedToRecipe = document.getElementById('proceedToRecipe');

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    loadAllergenFilters();
    setupEventListeners();
});

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Search button click
    searchBtn.addEventListener('click', performSearch);
    
    // Enter key in search input
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    // Modal close button
    const modalClose = document.querySelector('.modal-close');
    if (modalClose) {
        modalClose.addEventListener('click', closeModal);
    }
    
    // Close modal when clicking outside
    recipeModal.addEventListener('click', (e) => {
        if (e.target === recipeModal) {
            closeModal();
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && recipeModal.style.display === 'flex') {
            closeModal();
        }
    });
    
    // Safety acknowledgment checkbox
    if (safetyAcknowledge) {
        safetyAcknowledge.addEventListener('change', (e) => {
            proceedToRecipe.disabled = !e.target.checked;
        });
    }
    
    // Proceed to recipe button
    if (proceedToRecipe) {
        proceedToRecipe.addEventListener('click', () => {
            safetyVerification.style.display = 'none';
            modalBody.style.display = 'block';
            loadRecipeDetails(currentRecipeIndex);
        });
    }
}

/**
 * Load allergen filter checkboxes
 */
async function loadAllergenFilters() {
    try {
        const response = await fetch('/api/allergens');
        const data = await response.json();
        
        if (data.success) {
            allergenGroups = data.allergens;
            renderAllergenFilters(allergenGroups);
        }
    } catch (error) {
        console.error('Error loading allergens:', error);
        showError('Failed to load allergen filters');
    }
}

/**
 * Render allergen filter checkboxes
 */
function renderAllergenFilters(allergens) {
    allergenFilters.innerHTML = '';
    
    Object.entries(allergens).forEach(([key, name]) => {
        const allergenItem = document.createElement('div');
        allergenItem.className = 'allergen-item';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = `allergen-${key}`;
        checkbox.value = key;
        
        const label = document.createElement('label');
        label.htmlFor = `allergen-${key}`;
        label.textContent = name;
        
        allergenItem.appendChild(checkbox);
        allergenItem.appendChild(label);
        
        // Make the whole item clickable
        allergenItem.addEventListener('click', (e) => {
            if (e.target !== checkbox) {
                checkbox.checked = !checkbox.checked;
            }
        });
        
        allergenFilters.appendChild(allergenItem);
    });
}

/**
 * Get selected allergens
 */
function getSelectedAllergens() {
    const checkboxes = allergenFilters.querySelectorAll('input[type="checkbox"]:checked');
    return Array.from(checkboxes).map(cb => cb.value);
}

/**
 * Perform recipe search
 */
async function performSearch() {
    const query = searchInput.value.trim();
    
    if (!query) {
        showError('Please enter a search term');
        return;
    }
    
    // Get excluded allergens
    const excludedAllergens = getSelectedAllergens();
    
    // Show loading state
    showLoading();
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                excluded_allergens: excludedAllergens
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentRecipes = data.recipes;
            displayResults(data);
        } else {
            showError(data.error || 'Search failed');
        }
    } catch (error) {
        console.error('Search error:', error);
        showError('Failed to search recipes. Please try again.');
    } finally {
        hideLoading();
    }
}

/**
 * Display search results
 */
function displayResults(data) {
    // Hide no results message
    noResults.style.display = 'none';
    
    if (data.recipes.length === 0) {
        // Show no results message
        resultsSection.style.display = 'none';
        noResults.style.display = 'block';
        return;
    }
    
    // Update results header
    resultsTitle.textContent = `Results for "${data.query}"`;
    
    let countText = `Found ${data.filtered_results} recipe${data.filtered_results !== 1 ? 's' : ''}`;
    if (data.excluded_allergens.length > 0) {
        countText += ` (filtered from ${data.total_results} total)`;
    }
    resultsCount.textContent = countText;
    
    // Render recipe cards
    renderRecipeCards(data.recipes);
    
    // Show results section
    resultsSection.style.display = 'block';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Render recipe cards
 */
function renderRecipeCards(recipes) {
    recipeGrid.innerHTML = '';
    
    recipes.forEach((recipe, index) => {
        const card = createRecipeCard(recipe, index);
        recipeGrid.appendChild(card);
    });
}

/**
 * Create a recipe card element with confidence indicators
 */
function createRecipeCard(recipe, index) {
    const card = document.createElement('div');
    card.className = 'recipe-card';
    card.onclick = () => showRecipeDetail(index);
    
    // Recipe image
    const img = document.createElement('img');
    img.className = 'recipe-image';
    img.src = recipe.image || 'https://placehold.co/400x300/e0e0e0/757575?text=Recipe';
    img.alt = recipe.title;
    img.onerror = () => {
        img.src = 'https://placehold.co/400x300/e0e0e0/757575?text=Recipe';
    };
    
    // Recipe content
    const content = document.createElement('div');
    content.className = 'recipe-content';
    
    // Title
    const title = document.createElement('h3');
    title.className = 'recipe-title';
    title.textContent = recipe.title;
    
    // Source and data quality indicator
    const sourceDiv = document.createElement('div');
    sourceDiv.className = 'recipe-metadata';
    
    const source = document.createElement('span');
    source.className = 'recipe-source';
    source.textContent = recipe.source || 'Unknown Source';
    sourceDiv.appendChild(source);
    
    // Data quality badge
    if (recipe.data_quality) {
        const qualityBadge = document.createElement('span');
        qualityBadge.className = `data-quality-badge ${recipe.data_quality}`;
        qualityBadge.textContent = recipe.data_quality === 'mock_data' ? '📋 Demo' : '🌐 Live';
        qualityBadge.title = recipe.data_quality === 'mock_data' ? 
            'Demonstration data' : 'Scraped from live website';
        sourceDiv.appendChild(qualityBadge);
    }
    
    // Allergens section with confidence indicators
    const allergensDiv = document.createElement('div');
    allergensDiv.className = 'recipe-allergens';
    
    if (recipe.allergen_details && recipe.allergen_details.length > 0) {
        const warning = document.createElement('div');
        warning.className = 'allergen-warning';
        warning.textContent = '⚠️ Contains Allergens:';
        
        const tags = document.createElement('div');
        tags.className = 'allergen-tags';
        
        recipe.allergen_details.forEach(allergen => {
            const tag = document.createElement('span');
            tag.className = `allergen-tag confidence-${allergen.confidence}`;
            tag.textContent = allergen.name;
            tag.title = `Confidence: ${allergen.confidence.toUpperCase()} (${Math.round(allergen.confidence_score * 100)}%)`;
            tags.appendChild(tag);
        });
        
        allergensDiv.appendChild(warning);
        allergensDiv.appendChild(tags);
    } else if (recipe.allergen_list && recipe.allergen_list.length > 0) {
        // Fallback for recipes without detailed confidence data
        const warning = document.createElement('div');
        warning.className = 'allergen-warning';
        warning.textContent = '⚠️ Contains:';
        
        const tags = document.createElement('div');
        tags.className = 'allergen-tags';
        
        recipe.allergen_list.forEach(allergen => {
            const tag = document.createElement('span');
            tag.className = 'allergen-tag';
            tag.textContent = allergen;
            tags.appendChild(tag);
        });
        
        allergensDiv.appendChild(warning);
        allergensDiv.appendChild(tags);
    } else {
        const noAllergens = document.createElement('div');
        noAllergens.className = 'no-allergens-detected';
        noAllergens.innerHTML = '⚠️ No major allergens detected<br><small>(Always verify manually)</small>';
        allergensDiv.appendChild(noAllergens);
    }
    
    // Assemble card
    content.appendChild(title);
    content.appendChild(sourceDiv);
    content.appendChild(allergensDiv);
    
    card.appendChild(img);
    card.appendChild(content);
    
    return card;
}

/**
 * Show recipe detail modal with safety verification
 */
function showRecipeDetail(index) {
    currentRecipeIndex = index;
    
    // Reset modal state
    safetyVerification.style.display = 'block';
    modalBody.style.display = 'none';
    safetyAcknowledge.checked = false;
    proceedToRecipe.disabled = true;
    
    // Show modal
    recipeModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

/**
 * Load recipe details after safety acknowledgment
 */
function loadRecipeDetails(index) {
    const recipe = currentRecipes[index];
    
    if (!recipe) return;
    
    // Build modal content with enhanced safety information
    let modalHTML = `
        <h2 class="modal-recipe-title">${recipe.title}</h2>
        
        ${recipe.image ? `<img src="${recipe.image}" alt="${recipe.title}" class="modal-recipe-image" onerror="this.style.display='none'">` : ''}
        
        <div class="modal-section modal-metadata">
            <p><strong>Source:</strong> ${recipe.source || 'Unknown'}</p>
            ${recipe.scraped_at ? `<p><strong>Data Retrieved:</strong> ${new Date(recipe.scraped_at).toLocaleString()}</p>` : ''}
            ${recipe.scraping_method ? `<p><strong>Collection Method:</strong> ${recipe.scraping_method}</p>` : ''}
            ${recipe.data_quality ? `<p><strong>Data Type:</strong> ${recipe.data_quality === 'mock_data' ? 'Demonstration Data' : 'Live Scraped Data'}</p>` : ''}
            ${recipe.url && recipe.url !== '#' ? `<p><a href="${recipe.url}" target="_blank" rel="noopener noreferrer" class="original-link">View Original Recipe →</a></p>` : ''}
        </div>
    `;
    
    // Enhanced allergen warning with confidence scores
    if (recipe.allergen_details && recipe.allergen_details.length > 0) {
        modalHTML += `
            <div class="modal-allergen-warning critical">
                <h4>⚠️ ALLERGEN WARNING</h4>
                <p><strong>This recipe contains the following detected allergens:</strong></p>
                <div class="modal-allergen-detailed-list">
        `;
        
        recipe.allergen_details.forEach(allergen => {
            const confidenceClass = `confidence-${allergen.confidence}`;
            const confidencePercent = Math.round(allergen.confidence_score * 100);
            modalHTML += `
                <div class="allergen-detail-item ${confidenceClass}">
                    <div class="allergen-detail-header">
                        <span class="allergen-name">${allergen.name}</span>
                        <span class="confidence-badge ${confidenceClass}">
                            ${allergen.confidence.toUpperCase()} (${confidencePercent}%)
                        </span>
                    </div>
                    <div class="allergen-detail-info">
                        <small>Detected via: ${allergen.detection_method}</small>
                        ${allergen.matched_keywords && allergen.matched_keywords.length > 0 ? 
                            `<br><small>Matched: ${allergen.matched_keywords.slice(0, 3).join(', ')}</small>` : ''}
                    </div>
                </div>
            `;
        });
        
        modalHTML += `
                </div>
                <p class="critical-reminder">⚠️ <strong>REMINDER:</strong> Even HIGH confidence detections may be incorrect. 
                Verify all ingredients before consuming.</p>
            </div>
        `;
    } else if (recipe.allergen_list && recipe.allergen_list.length > 0) {
        // Fallback for recipes without detailed data
        modalHTML += `
            <div class="modal-allergen-warning">
                <h4>⚠️ Allergen Warning</h4>
                <p>This recipe contains the following allergens:</p>
                <div class="modal-allergen-list">
                    ${recipe.allergen_list.map(allergen => 
                        `<span class="modal-allergen-tag">${allergen}</span>`
                    ).join('')}
                </div>
            </div>
        `;
    } else {
        modalHTML += `
            <div class="modal-allergen-warning info">
                <h4>ℹ️ Allergen Detection Result</h4>
                <p>No major allergens detected by automated system.</p>
                <p class="critical-reminder">⚠️ <strong>IMPORTANT:</strong> This does NOT guarantee the recipe is safe. 
                Always verify ingredients manually.</p>
            </div>
        `;
    }
    
    // Ingredients
    if (recipe.ingredients && recipe.ingredients.length > 0) {
        modalHTML += `
            <div class="modal-section">
                <h3>📝 Ingredients</h3>
                <p class="verify-reminder">⚠️ <strong>Verify each ingredient carefully</strong></p>
                <ul class="ingredient-list">
                    ${recipe.ingredients.map(ingredient => 
                        `<li>${escapeHtml(ingredient)}</li>`
                    ).join('')}
                </ul>
            </div>
        `;
    }
    
    // Instructions
    if (recipe.instructions && recipe.instructions.length > 0) {
        modalHTML += `
            <div class="modal-section">
                <h3>👨‍🍳 Instructions</h3>
                <ol class="instruction-list">
                    ${recipe.instructions.map(instruction => 
                        `<li>${escapeHtml(instruction)}</li>`
                    ).join('')}
                </ol>
            </div>
        `;
    }
    
    modalBody.innerHTML = modalHTML;
}

/**
 * Close recipe modal
 */
function closeModal() {
    recipeModal.style.display = 'none';
    document.body.style.overflow = 'auto';
    
    // Reset modal state
    safetyVerification.style.display = 'block';
    modalBody.style.display = 'none';
    safetyAcknowledge.checked = false;
    proceedToRecipe.disabled = true;
    currentRecipeIndex = null;
}

/**
 * Show loading indicator
 */
function showLoading() {
    loadingIndicator.style.display = 'block';
    resultsSection.style.display = 'none';
    noResults.style.display = 'none';
    searchBtn.disabled = true;
    
    const btnText = searchBtn.querySelector('.btn-text');
    const btnLoader = searchBtn.querySelector('.btn-loader');
    if (btnText) btnText.style.display = 'none';
    if (btnLoader) btnLoader.style.display = 'inline';
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    loadingIndicator.style.display = 'none';
    searchBtn.disabled = false;
    
    const btnText = searchBtn.querySelector('.btn-text');
    const btnLoader = searchBtn.querySelector('.btn-loader');
    if (btnText) btnText.style.display = 'inline';
    if (btnLoader) btnLoader.style.display = 'none';
}

/**
 * Show error message
 */
function showError(message) {
    alert(message);
}

/**
 * Utility function to escape HTML
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

