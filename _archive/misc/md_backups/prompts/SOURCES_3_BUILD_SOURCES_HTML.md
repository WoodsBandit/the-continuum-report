# TASK: Build Interactive Sources Page (sources.html)

Create the Sources page for The Continuum Report — an interactive document library matching the continuum.html aesthetic.

---

## OUTPUT FILE

Save to: `/continuum/website/sources.html`

---

## DATA SOURCE

Read from: `/continuum/website/data/sources-manifest.json`

---

## DESIGN REQUIREMENTS

### Color Palette (match continuum.html):
- Background: #0a0a0a (near black)
- Card background: #1a1a1a
- Card hover: #2a2a2a
- Primary accent: #c9a227 (gold)
- Secondary accent: #d4af37 (lighter gold)
- Text primary: #e0e0e0
- Text secondary: #888888
- Border: #333333

### Typography:
- Headers: 'Georgia', serif
- Body: 'Inter', -apple-system, sans-serif
- Monospace (citations): 'Consolas', monospace

### Layout:
- Full viewport height
- Fixed header with search/filters
- Scrollable content area
- Responsive (works on mobile)

---

## PAGE STRUCTURE

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Source Documents | The Continuum Report</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        /* CSS here */
    </style>
</head>
<body>
    <!-- Header -->
    <header>
        <div class="header-left">
            <a href="/" class="logo">TCR</a>
            <h1>Source Documents</h1>
        </div>
        <div class="header-right">
            <span class="doc-count">0 documents</span>
        </div>
    </header>

    <!-- Search & Filters Bar -->
    <div class="filter-bar">
        <div class="search-container">
            <input type="text" id="search" placeholder="Search documents...">
        </div>
        <div class="filters">
            <select id="collection-filter">
                <option value="all">All Collections</option>
            </select>
            <select id="type-filter">
                <option value="all">All Types</option>
                <option value="court-opinion">Court Opinions</option>
                <option value="legislation">Legislation</option>
                <option value="executive-order">Executive Orders</option>
                <option value="congressional">Congressional</option>
            </select>
            <select id="year-filter">
                <option value="all">All Years</option>
            </select>
        </div>
    </div>

    <!-- Main Content -->
    <main>
        <!-- Collection Cards (default view) -->
        <div id="collections-view" class="collections-grid">
            <!-- Populated by JS -->
        </div>

        <!-- Document List (when filtered/searching) -->
        <div id="documents-view" class="documents-list" style="display: none;">
            <!-- Populated by JS -->
        </div>
    </main>

    <!-- Footer -->
    <footer>
        <p>The Continuum Report — Another Node in the Decentralized Intelligence Agency</p>
        <p class="disclaimer">Public domain and fair use documents for journalism and research.</p>
    </footer>

    <script>
        /* JavaScript here */
    </script>
</body>
</html>
```

---

## CSS STYLING

### Base Styles:
```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #0a0a0a;
    color: #e0e0e0;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

a {
    color: #c9a227;
    text-decoration: none;
}

a:hover {
    color: #d4af37;
}
```

### Header:
```css
header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 40px;
    background: #0a0a0a;
    border-bottom: 1px solid #333;
    position: sticky;
    top: 0;
    z-index: 100;
}

.logo {
    font-family: 'Georgia', serif;
    font-size: 24px;
    font-weight: bold;
    color: #c9a227;
    letter-spacing: 3px;
    margin-right: 30px;
}

header h1 {
    font-family: 'Georgia', serif;
    font-size: 18px;
    font-weight: normal;
    color: #888;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.doc-count {
    font-size: 14px;
    color: #888;
}
```

### Filter Bar:
```css
.filter-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 40px;
    background: #1a1a1a;
    border-bottom: 1px solid #333;
    flex-wrap: wrap;
    gap: 15px;
}

.search-container {
    flex: 1;
    max-width: 400px;
}

.search-container input {
    width: 100%;
    padding: 12px 20px;
    background: #0a0a0a;
    border: 1px solid #333;
    border-radius: 4px;
    color: #e0e0e0;
    font-size: 14px;
}

.search-container input:focus {
    outline: none;
    border-color: #c9a227;
}

.search-container input::placeholder {
    color: #666;
}

.filters {
    display: flex;
    gap: 15px;
}

.filters select {
    padding: 10px 15px;
    background: #0a0a0a;
    border: 1px solid #333;
    border-radius: 4px;
    color: #e0e0e0;
    font-size: 14px;
    cursor: pointer;
}

.filters select:focus {
    outline: none;
    border-color: #c9a227;
}
```

### Collection Cards:
```css
main {
    flex: 1;
    padding: 40px;
}

.collections-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 25px;
    max-width: 1400px;
    margin: 0 auto;
}

.collection-card {
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 8px;
    padding: 30px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.collection-card:hover {
    background: #2a2a2a;
    border-color: #c9a227;
    transform: translateY(-2px);
}

.collection-card h2 {
    font-family: 'Georgia', serif;
    font-size: 22px;
    color: #c9a227;
    margin-bottom: 10px;
}

.collection-card .meta {
    font-size: 13px;
    color: #888;
    margin-bottom: 15px;
}

.collection-card .description {
    font-size: 14px;
    color: #aaa;
    line-height: 1.6;
    margin-bottom: 20px;
}

.collection-card .stats {
    display: flex;
    gap: 20px;
    font-size: 13px;
    color: #666;
}

.collection-card .stats span {
    display: flex;
    align-items: center;
    gap: 5px;
}
```

### Document List:
```css
.documents-list {
    max-width: 1000px;
    margin: 0 auto;
}

.category-header {
    font-family: 'Georgia', serif;
    font-size: 16px;
    color: #c9a227;
    padding: 15px 0;
    border-bottom: 1px solid #333;
    margin-top: 30px;
    margin-bottom: 15px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.document-item {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 20px;
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 6px;
    margin-bottom: 10px;
    transition: all 0.2s ease;
}

.document-item:hover {
    background: #2a2a2a;
    border-color: #444;
}

.document-info {
    flex: 1;
}

.document-info h3 {
    font-family: 'Georgia', serif;
    font-size: 16px;
    color: #e0e0e0;
    margin-bottom: 5px;
}

.document-info .citation {
    font-family: 'Consolas', monospace;
    font-size: 12px;
    color: #c9a227;
    margin-bottom: 8px;
}

.document-info .description {
    font-size: 13px;
    color: #888;
    line-height: 1.5;
}

.document-actions {
    display: flex;
    gap: 10px;
    margin-left: 20px;
}

.document-actions a {
    padding: 8px 16px;
    background: #2a2a2a;
    border: 1px solid #444;
    border-radius: 4px;
    font-size: 12px;
    color: #e0e0e0;
    transition: all 0.2s ease;
}

.document-actions a:hover {
    background: #c9a227;
    color: #0a0a0a;
    border-color: #c9a227;
}

.document-actions a.primary {
    background: #c9a227;
    color: #0a0a0a;
    border-color: #c9a227;
}

.document-actions a.primary:hover {
    background: #d4af37;
}
```

### Back Button:
```css
.back-button {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    background: #2a2a2a;
    border: 1px solid #444;
    border-radius: 4px;
    color: #e0e0e0;
    font-size: 14px;
    cursor: pointer;
    margin-bottom: 30px;
    transition: all 0.2s ease;
}

.back-button:hover {
    background: #3a3a3a;
    border-color: #c9a227;
}
```

### Footer:
```css
footer {
    padding: 30px 40px;
    background: #0a0a0a;
    border-top: 1px solid #333;
    text-align: center;
}

footer p {
    font-size: 13px;
    color: #666;
    margin-bottom: 5px;
}

footer .disclaimer {
    font-size: 11px;
    color: #444;
}
```

### Responsive:
```css
@media (max-width: 768px) {
    header {
        padding: 15px 20px;
        flex-direction: column;
        gap: 10px;
    }
    
    .filter-bar {
        padding: 15px 20px;
        flex-direction: column;
    }
    
    .search-container {
        max-width: 100%;
    }
    
    .filters {
        width: 100%;
        flex-wrap: wrap;
    }
    
    .filters select {
        flex: 1;
        min-width: 120px;
    }
    
    main {
        padding: 20px;
    }
    
    .collections-grid {
        grid-template-columns: 1fr;
    }
    
    .document-item {
        flex-direction: column;
    }
    
    .document-actions {
        margin-left: 0;
        margin-top: 15px;
    }
}
```

---

## JAVASCRIPT FUNCTIONALITY

### Load Data:
```javascript
let manifest = null;
let currentView = 'collections';
let currentCollection = null;

async function loadManifest() {
    const response = await fetch('/data/sources-manifest.json');
    manifest = await response.json();
    updateDocCount();
    renderCollections();
    populateFilters();
}
```

### Render Collections:
```javascript
function renderCollections() {
    const container = document.getElementById('collections-view');
    container.innerHTML = manifest.collections.map(collection => `
        <div class="collection-card" onclick="openCollection('${collection.id}')">
            <h2>${collection.title}</h2>
            <div class="meta">${collection.dateRange}</div>
            <div class="description">${collection.description}</div>
            <div class="stats">
                <span>${collection.documentCount} documents</span>
                <span>${collection.categories.length} categories</span>
            </div>
        </div>
    `).join('');
}
```

### Open Collection:
```javascript
function openCollection(collectionId) {
    currentCollection = manifest.collections.find(c => c.id === collectionId);
    currentView = 'documents';
    
    document.getElementById('collections-view').style.display = 'none';
    document.getElementById('documents-view').style.display = 'block';
    
    renderDocuments(currentCollection);
}
```

### Render Documents:
```javascript
function renderDocuments(collection) {
    const container = document.getElementById('documents-view');
    
    let html = `
        <button class="back-button" onclick="backToCollections()">
            ← Back to Collections
        </button>
        <h2 style="font-family: Georgia; color: #c9a227; margin-bottom: 30px;">
            ${collection.title}
        </h2>
    `;
    
    collection.categories.forEach(category => {
        if (category.documents.length === 0) return;
        
        html += `<div class="category-header">${category.name}</div>`;
        
        category.documents.forEach(doc => {
            html += `
                <div class="document-item">
                    <div class="document-info">
                        <h3>${doc.title}</h3>
                        ${doc.citation ? `<div class="citation">${doc.citation}</div>` : ''}
                        <div class="description">${doc.description || ''}</div>
                    </div>
                    <div class="document-actions">
                        <a href="${doc.pdfPath}" target="_blank" class="primary">View PDF</a>
                        ${doc.hasText ? `<a href="${doc.textPath}" target="_blank">View Text</a>` : ''}
                    </div>
                </div>
            `;
        });
    });
    
    container.innerHTML = html;
}
```

### Back to Collections:
```javascript
function backToCollections() {
    currentView = 'collections';
    currentCollection = null;
    
    document.getElementById('collections-view').style.display = 'grid';
    document.getElementById('documents-view').style.display = 'none';
    
    // Reset filters
    document.getElementById('search').value = '';
    document.getElementById('collection-filter').value = 'all';
}
```

### Search:
```javascript
document.getElementById('search').addEventListener('input', function(e) {
    const query = e.target.value.toLowerCase().trim();
    
    if (query.length < 2) {
        if (currentView === 'collections') {
            renderCollections();
        }
        return;
    }
    
    // Search across all documents
    const results = [];
    manifest.collections.forEach(collection => {
        collection.categories.forEach(category => {
            category.documents.forEach(doc => {
                const searchText = `${doc.title} ${doc.description || ''} ${doc.citation || ''}`.toLowerCase();
                if (searchText.includes(query)) {
                    results.push({ ...doc, collectionTitle: collection.title });
                }
            });
        });
    });
    
    renderSearchResults(results, query);
});
```

### Render Search Results:
```javascript
function renderSearchResults(results, query) {
    document.getElementById('collections-view').style.display = 'none';
    document.getElementById('documents-view').style.display = 'block';
    
    const container = document.getElementById('documents-view');
    
    let html = `
        <button class="back-button" onclick="backToCollections()">
            ← Clear Search
        </button>
        <h2 style="font-family: Georgia; color: #888; margin-bottom: 30px;">
            ${results.length} results for "${query}"
        </h2>
    `;
    
    results.forEach(doc => {
        html += `
            <div class="document-item">
                <div class="document-info">
                    <h3>${doc.title}</h3>
                    ${doc.citation ? `<div class="citation">${doc.citation}</div>` : ''}
                    <div class="description">
                        <span style="color: #666;">${doc.collectionTitle}</span>
                        ${doc.description ? ` — ${doc.description}` : ''}
                    </div>
                </div>
                <div class="document-actions">
                    <a href="${doc.pdfPath}" target="_blank" class="primary">View PDF</a>
                    ${doc.hasText ? `<a href="${doc.textPath}" target="_blank">View Text</a>` : ''}
                </div>
            </div>
        `;
    });
    
    if (results.length === 0) {
        html += `<p style="color: #666; text-align: center; padding: 40px;">No documents found.</p>`;
    }
    
    container.innerHTML = html;
}
```

### Filter Functions:
```javascript
function populateFilters() {
    // Populate collection filter
    const collectionFilter = document.getElementById('collection-filter');
    manifest.collections.forEach(c => {
        const option = document.createElement('option');
        option.value = c.id;
        option.textContent = c.title;
        collectionFilter.appendChild(option);
    });
    
    // Populate year filter
    const years = new Set();
    manifest.collections.forEach(c => {
        c.categories.forEach(cat => {
            cat.documents.forEach(doc => {
                if (doc.year) years.add(doc.year);
            });
        });
    });
    
    const yearFilter = document.getElementById('year-filter');
    [...years].sort((a, b) => b - a).forEach(year => {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        yearFilter.appendChild(option);
    });
}

function updateDocCount() {
    document.querySelector('.doc-count').textContent = 
        `${manifest.totalDocuments} documents`;
}
```

### Initialize:
```javascript
document.addEventListener('DOMContentLoaded', loadManifest);
```

---

## FINAL CHECKLIST

- [ ] Page loads and displays collection cards
- [ ] Clicking collection shows documents
- [ ] Back button returns to collections
- [ ] Search filters documents in real-time
- [ ] Collection dropdown filters work
- [ ] PDF links open in new tab
- [ ] Text links open in new tab (if available)
- [ ] Mobile responsive
- [ ] Matches continuum.html aesthetic

---

## POST-TASK: PERMISSIONS (Run from root@Tower AFTER Claude Code completes)

```bash
chmod 666 /mnt/user/continuum/website/sources.html
chown nobody:users /mnt/user/continuum/website/sources.html
```

---

*The Continuum Report — Another Node in the Decentralized Intelligence Agency*
