# SOURCES ARCHIVE — Build Instructions

**Project Lead Agent:** sources-archive-lead
**Authority:** May spawn sub-agents for parallel work
**Output:** `/continuum/website/sources/index.html`

---

## Mission Statement

Build a world-class source document archive page that:
- Establishes credibility through professional presentation
- Makes verification easy for journalists and researchers
- Matches The Continuum Report's visual identity perfectly
- Organizes 72+ documents into intuitive categories

**This page is where our credibility is proven. Build it like your reputation depends on it.**

---

## Phase 1: Research & Design Extraction

### 1.1 Extract Design System

**Read:** `/continuum/website/index.html`

Extract and document:
```
CSS VARIABLES:
- All color definitions (--void-black, --ancient-gold, etc.)
- All typography settings
- All spacing/sizing variables

COMPONENTS:
- Navigation bar HTML structure
- Footer HTML structure
- Button styles
- Card patterns
- Animation keyframes

PATTERNS:
- How sections are structured
- How responsive breakpoints work
- How hover effects are implemented
```

**Deliverable:** Design system notes in `log.md`

### 1.2 Inventory Source Documents

**Read:** `/continuum/website/sources/index.json`

Current inventory:
- 72 Giuffre v. Maxwell ECF documents
- Case citation: "Giuffre v. Maxwell, No. 15-cv-07433-LAP (S.D.N.Y.)"

**Check directories:**
- `/sources/bop-footage/` — BOP footage, DOJ memos
- `/sources/cia-history/` — CIA historical documents
- `/sources/epstein-estate/` — House Oversight images

**Deliverable:** Complete document count in `index.md`

---

## Phase 2: Data Architecture

### 2.1 Expand sources.json Schema

Current schema only has Giuffre v. Maxwell. Expand to:

```json
{
  "generated": "2025-12-25T00:00:00Z",
  "total_documents": 0,
  "categories": [
    {
      "id": "court-filings",
      "name": "Court Filings",
      "description": "Official court documents from federal cases",
      "icon": "gavel",
      "count": 0
    },
    {
      "id": "foia",
      "name": "FOIA Releases",
      "description": "Documents obtained through Freedom of Information Act requests",
      "icon": "document",
      "count": 0
    },
    {
      "id": "regulatory",
      "name": "Regulatory Actions",
      "description": "Consent orders, enforcement actions, and regulatory findings",
      "icon": "shield",
      "count": 0
    },
    {
      "id": "estate",
      "name": "Estate Materials",
      "description": "Documents from Epstein estate and House Oversight releases",
      "icon": "folder",
      "count": 0
    }
  ],
  "cases": {
    "giuffre-v-maxwell": {
      "name": "Giuffre v. Maxwell",
      "citation": "No. 15-cv-07433-LAP (S.D.N.Y.)",
      "category": "court-filings",
      "documents": []
    }
  },
  "standalone_documents": []
}
```

**Option:** Keep existing index.json as-is and create new `sources-full.json` for the landing page.

### 2.2 Document Card Data Structure

Each document needs:
```json
{
  "id": "unique-id",
  "title": "Human readable title",
  "filename": "actual-file.pdf",
  "path": "/sources/category/file.pdf",
  "category": "court-filings",
  "case": "Giuffre v. Maxwell",
  "type": "Deposition | Exhibit | Motion | Order | Transcript",
  "date": "2024-01-05",
  "size_kb": 2456,
  "pages": 45,
  "description": "Brief description of contents",
  "ecf": "1328-44",
  "verification_url": "https://pacer.uscourts.gov/..."
}
```

---

## Phase 3: HTML Structure

### 3.1 Page Skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Meta tags (copy pattern from index.html) -->
    <!-- Google Fonts preconnect -->
    <!-- Inline CSS -->
</head>
<body>
    <!-- Navigation (exact copy from index.html) -->
    <nav>...</nav>

    <!-- Hero Section -->
    <section class="archive-hero">
        <h1>Source Archive</h1>
        <p class="hero-subtitle">Primary documents. Independently verifiable. Open to all.</p>
        <p class="hero-description">Every claim we make is backed by source documents.
           Browse our complete archive of court filings, FOIA releases, and regulatory actions.</p>
    </section>

    <!-- Filter Controls -->
    <section class="archive-controls">
        <div class="category-filters">
            <button class="filter-btn active" data-category="all">All Documents</button>
            <button class="filter-btn" data-category="court-filings">Court Filings</button>
            <button class="filter-btn" data-category="foia">FOIA</button>
            <button class="filter-btn" data-category="regulatory">Regulatory</button>
            <button class="filter-btn" data-category="estate">Estate</button>
        </div>
        <div class="search-container">
            <input type="text" id="searchInput" placeholder="Search documents...">
            <span class="result-count">72 documents</span>
        </div>
    </section>

    <!-- Document Grid -->
    <section class="archive-grid">
        <div id="documentsContainer">
            <!-- Cards populated by JavaScript -->
        </div>
    </section>

    <!-- Case Sections (grouped by case) -->
    <section class="case-section" id="giuffre-v-maxwell">
        <h2>Giuffre v. Maxwell</h2>
        <p class="case-citation">No. 15-cv-07433-LAP (S.D.N.Y.)</p>
        <div class="case-documents">
            <!-- Document cards for this case -->
        </div>
    </section>

    <!-- Methodology Section -->
    <section class="methodology">
        <h2>Our Sourcing Standards</h2>
        <div class="methodology-grid">
            <div class="method-card">
                <h3>Primary Sources Only</h3>
                <p>We prioritize official court filings, government documents, and verified records.</p>
            </div>
            <div class="method-card">
                <h3>Verification Links</h3>
                <p>Where possible, we provide PACER links for independent verification.</p>
            </div>
            <div class="method-card">
                <h3>Complete Context</h3>
                <p>Documents are presented in full, not selectively quoted.</p>
            </div>
        </div>
    </section>

    <!-- Footer (exact copy from index.html) -->
    <footer>...</footer>

    <!-- Inline JavaScript -->
    <script>
        // Load sources.json
        // Render document cards
        // Handle filtering
        // Handle search
    </script>
</body>
</html>
```

### 3.2 Document Card Component

```html
<div class="doc-card" data-category="court-filings" data-case="giuffre-v-maxwell">
    <div class="doc-badge">Court Filing</div>
    <h3 class="doc-title">ECF 1328-44</h3>
    <p class="doc-case">Giuffre v. Maxwell</p>
    <p class="doc-description">Exhibit 44 — Deposition excerpts</p>
    <div class="doc-meta">
        <span class="doc-size">2.4 MB</span>
        <span class="doc-pages">45 pages</span>
    </div>
    <a href="/sources/giuffre-v-maxwell/ecf-1328-44.pdf" class="doc-download" target="_blank">
        <span>Download PDF</span>
        <svg><!-- download icon --></svg>
    </a>
</div>
```

---

## Phase 4: CSS Styling

### 4.1 Required Styles

**Hero Section:**
```css
.archive-hero {
    background: linear-gradient(180deg, var(--void-black) 0%, var(--deep-purple) 100%);
    padding: 8rem 2rem 4rem;
    text-align: center;
}

.archive-hero h1 {
    font-family: 'Cinzel', serif;
    font-size: clamp(2rem, 5vw, 3.5rem);
    color: var(--ancient-gold);
    margin-bottom: 1rem;
}

.hero-subtitle {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(1.2rem, 3vw, 1.6rem);
    color: var(--mist);
    font-style: italic;
}
```

**Filter Controls:**
```css
.archive-controls {
    background: var(--deep-purple);
    padding: 2rem;
    position: sticky;
    top: 60px; /* Below nav */
    z-index: 100;
    border-bottom: 1px solid var(--ancient-gold);
}

.filter-btn {
    background: transparent;
    border: 1px solid var(--mystic-purple);
    color: var(--mist);
    padding: 0.5rem 1rem;
    font-family: 'Source Sans 3', sans-serif;
    cursor: pointer;
    transition: all 0.3s ease;
}

.filter-btn:hover,
.filter-btn.active {
    border-color: var(--ancient-gold);
    color: var(--ancient-gold);
    background: rgba(201, 162, 39, 0.1);
}
```

**Document Cards:**
```css
.doc-card {
    background: var(--royal-purple);
    border: 1px solid var(--mystic-purple);
    border-radius: 8px;
    padding: 1.5rem;
    transition: all 0.3s ease;
}

.doc-card:hover {
    border-color: var(--ancient-gold);
    transform: translateY(-4px);
    box-shadow: 0 8px 32px rgba(201, 162, 39, 0.15);
}

.doc-badge {
    display: inline-block;
    background: rgba(201, 162, 39, 0.2);
    color: var(--ancient-gold);
    font-size: 0.75rem;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.doc-download {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    background: var(--ancient-gold);
    color: var(--void-black);
    padding: 0.75rem 1rem;
    border-radius: 4px;
    text-decoration: none;
    font-weight: 600;
    margin-top: 1rem;
    transition: all 0.3s ease;
}

.doc-download:hover {
    background: var(--light-gold);
    transform: scale(1.02);
}
```

**Responsive Grid:**
```css
.archive-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    padding: 2rem;
    max-width: 1400px;
    margin: 0 auto;
}

@media (max-width: 768px) {
    .archive-grid {
        grid-template-columns: 1fr;
        padding: 1rem;
    }
}
```

---

## Phase 5: JavaScript Functionality

### 5.1 Data Loading

```javascript
let allDocuments = [];
let currentFilter = 'all';
let searchTerm = '';

async function loadDocuments() {
    try {
        const response = await fetch('/sources/index.json');
        const data = await response.json();

        // Flatten documents from all cases
        allDocuments = [];
        for (const [caseId, caseData] of Object.entries(data.cases)) {
            caseData.documents.forEach(doc => {
                allDocuments.push({
                    ...doc,
                    case: caseData.case_citation,
                    caseId: caseId,
                    category: 'court-filings',
                    path: `/sources/${caseId}/${doc.filename}`
                });
            });
        }

        renderDocuments();
        updateCount();
    } catch (error) {
        console.error('Failed to load documents:', error);
        showError('Unable to load document archive');
    }
}
```

### 5.2 Filtering & Search

```javascript
function filterDocuments() {
    let filtered = allDocuments;

    // Category filter
    if (currentFilter !== 'all') {
        filtered = filtered.filter(doc => doc.category === currentFilter);
    }

    // Search filter
    if (searchTerm) {
        const term = searchTerm.toLowerCase();
        filtered = filtered.filter(doc =>
            doc.ecf?.toLowerCase().includes(term) ||
            doc.title?.toLowerCase().includes(term) ||
            doc.case?.toLowerCase().includes(term) ||
            doc.description?.toLowerCase().includes(term)
        );
    }

    return filtered;
}

function renderDocuments() {
    const container = document.getElementById('documentsContainer');
    const docs = filterDocuments();

    container.innerHTML = docs.map(doc => `
        <div class="doc-card" data-category="${doc.category}">
            <div class="doc-badge">${doc.category.replace('-', ' ')}</div>
            <h3 class="doc-title">ECF ${doc.ecf}</h3>
            <p class="doc-case">${doc.case}</p>
            <a href="${doc.path}" class="doc-download" target="_blank">
                Download PDF
            </a>
        </div>
    `).join('');

    updateCount(docs.length);
}
```

### 5.3 Event Handlers

```javascript
// Filter buttons
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilter = btn.dataset.category;
        renderDocuments();
    });
});

// Search input with debounce
let searchTimeout;
document.getElementById('searchInput').addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        searchTerm = e.target.value;
        renderDocuments();
    }, 200);
});

// Initialize on load
document.addEventListener('DOMContentLoaded', loadDocuments);
```

---

## Phase 6: Testing & Refinement

### 6.1 Checklist

- [ ] All 72+ documents display correctly
- [ ] Category filters work
- [ ] Search filters in real-time
- [ ] Download links work (open PDF in new tab)
- [ ] Mobile responsive at all breakpoints
- [ ] Navigation matches main site exactly
- [ ] Footer matches main site exactly
- [ ] Colors match design system
- [ ] Typography matches design system
- [ ] Hover effects work smoothly
- [ ] Page loads under 2 seconds
- [ ] No console errors
- [ ] WCAG 2.1 AA accessible

### 6.2 Browser Testing

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Mobile Chrome
- [ ] Mobile Safari

---

## Sub-Agent Assignments

The lead agent MAY spawn these sub-agents for parallel work:

### Sub-Agent 1: Design Extractor
**Task:** Read index.html, extract all CSS variables, components, and patterns
**Output:** Update `log.md` with design system documentation

### Sub-Agent 2: Data Architect
**Task:** Expand index.json schema, add metadata for all documents
**Output:** Updated `/sources/index.json` or new `/sources/sources-full.json`

### Sub-Agent 3: Component Builder
**Task:** Build individual HTML/CSS components (cards, filters, hero)
**Output:** Component code snippets in `log.md`

### Sub-Agent 4: JavaScript Developer
**Task:** Write filtering, search, and rendering logic
**Output:** JavaScript code in `log.md`

### Sub-Agent 5: QA Tester
**Task:** Test completed page across devices and browsers
**Output:** Test results in `log.md`

---

## File Management

### Update Frequency

**log.md:** Update after EVERY significant action
- Starting a phase
- Completing a component
- Encountering an issue
- Making a decision

**index.md:** Update when:
- File is created/modified
- Status changes
- Dependencies identified

### Log Format

```markdown
## [YYYY-MM-DD HH:MM] — Action Title

**Agent:** [agent name]
**Phase:** [1-6]
**Task:** What was done
**Files:** Files affected
**Notes:** Any important observations
**Status:** Complete / In Progress / Blocked
**Next:** What happens next
```

---

## Success Criteria

The page is COMPLETE when:

1. **Visual Match:** Indistinguishable from main site design language
2. **Full Inventory:** All 72+ documents accessible
3. **Functional:** Filter/search work perfectly
4. **Fast:** Loads under 2 seconds
5. **Responsive:** Works on all devices
6. **Accessible:** WCAG 2.1 AA compliant
7. **Professional:** Feels like a serious research archive

---

## Emergency Contacts

If blocked, the lead agent should:
1. Document the blocker in `log.md`
2. Return to main session with status report
3. Request human intervention if needed

---

*Build instructions created: 2025-12-25*
*These instructions should enable any capable agent to complete this project.*
