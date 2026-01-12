# PHASE 4: Connections Panel Updates
## Continuum.html Implementation - Phase 4 of 5

---

## PHASE DETECTION CHECK (RUN FIRST)

**BEFORE DOING ANYTHING ELSE, verify prerequisites and current state:**

### Prerequisite Check - Phases 1, 2 & 3 Complete?

Read `/continuum/website/continuum.html` and verify:

**Phase 1:** Macro boxes labeled "PEOPLE", "GOV", "MEDIA", "FINANCIAL" ✓  
**Phase 2:** Entities layer with `.entities-card-grid` exists ✓  
**Phase 3:** Entity color schema with 8 colors AND gradient support exists ✓

**If any prerequisite NOT complete, STOP and output:**
```
═══════════════════════════════════════════════════════════════
PREREQUISITES NOT MET - Cannot proceed with Phase 4
═══════════════════════════════════════════════════════════════
Phases 1, 2, and 3 must be completed before Phase 4.

MISSING: Phase [X]
PROMPT: /continuum/prompts/PHASE[X]_[NAME].md
═══════════════════════════════════════════════════════════════
```

### Phase 4 Already Complete Check

Look for these indicators in `continuum.html`:

1. **Connection Dropdown:** CSS class `.connection-dropdown` or `.connection-expandable` with expandable content
2. **Summary + Sources Structure:** Elements for `.connection-summary` AND `.connection-sources` within each connection item
3. **View Connections Brief Button:** A button with text "View Connections Brief" or class `.view-connections-brief-btn`
4. **No Badge Labels:** The words "DOCUMENTED", "ASSOCIATED", "REFERENCED" do NOT appear as visible badge text in the connections panel

**If ALL FOUR indicators present, STOP and output:**
```
═══════════════════════════════════════════════════════════════
PHASE 4 ALREADY COMPLETE
═══════════════════════════════════════════════════════════════
This phase has already been implemented. No changes made.

READY FOR: Phase 5 - Connection Brief Generator
NEXT PROMPT: /continuum/prompts/PHASE5_CONNECTION_BRIEFS.md

To proceed, run Phase 5.
═══════════════════════════════════════════════════════════════
```

---

## BACKUP PROTOCOL (REQUIRED)

```bash
mkdir -p /continuum/website/backups

BACKUP_DIR="/continuum/website/backups"
LATEST=$(ls "$BACKUP_DIR" 2>/dev/null | grep -oP 'continuum_v\K[0-9]+' | sort -n | tail -1)
NEXT=$((LATEST + 1))

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/continuum_v${NEXT}_${TIMESTAMP}_pre-phase4.html"
cp /continuum/website/continuum.html "$BACKUP_FILE"

echo "✓ Backup created: $BACKUP_FILE"
```

---

## TASK SCOPE - PHASE 4 ONLY

### ✅ DO THESE THINGS:
1. Add dropdown expansion to connection items in the panel
2. Display connection summary text when expanded
3. Display clickable source links when expanded
4. Add "View Connections Brief" button to panel header
5. Remove "DOCUMENTED", "ASSOCIATED", "REFERENCED" badge labels

### ❌ DO NOT TOUCH:
- Macro layer
- Entities layer
- Web layer graph rendering or physics
- Entity colors or gradients
- Brief view modal (that displays when clicking "View Full Brief")

---

## CURRENT STATE REFERENCE

Based on the screenshots, the current connections panel shows:

```
┌─────────────────────────────────────────────┐
│ CONNECTIONS (21)                            │
├─────────────────────────────────────────────┤
│ ● Alan Dershowitz          [DOCUMENTED]     │
│   PERSON                                    │
├─────────────────────────────────────────────┤
│ ● Bill Clinton             [DOCUMENTED]     │
│   PERSON                   [ENTITIES]       │
├─────────────────────────────────────────────┤
│ ● Donald Trump             [DOCUMENTED]     │
│   PERSON                                    │
├─────────────────────────────────────────────┤
│ ...                                         │
└─────────────────────────────────────────────┘
```

**Target state after Phase 4:**

```
┌─────────────────────────────────────────────┐
│ CONNECTIONS (21)    [View Connections Brief]│
├─────────────────────────────────────────────┤
│ ▶ Alan Dershowitz                           │
│   PERSON                                    │
├─────────────────────────────────────────────┤
│ ▼ Bill Clinton                      [click] │
│   PERSON                                    │
│   ┌─────────────────────────────────────┐   │
│   │ Epstein and Clinton connected via   │   │
│   │ multiple documented flights on      │   │
│   │ Epstein's private aircraft...       │   │
│   │                                     │   │
│   │ SOURCES:                            │   │
│   │ • ECF Doc. 1331-32 (01/05/24)      │   │
│   │ • Flight Logs Exhibit A            │   │
│   │ • Maxwell Trial Testimony          │   │
│   └─────────────────────────────────────┘   │
├─────────────────────────────────────────────┤
│ ▶ Donald Trump                              │
│   PERSON                                    │
├─────────────────────────────────────────────┤
```

---

## DETAILED IMPLEMENTATION

### 1. HTML STRUCTURE FOR CONNECTION ITEMS

Update the connection item template:

```html
<!-- Connection item with expandable dropdown -->
<div class="connection-item" data-connection-id="[connection-id]" data-target-entity="[entity-id]">
    <div class="connection-header">
        <span class="connection-expand-icon">▶</span>
        <div class="connection-avatar">[initials]</div>
        <div class="connection-info">
            <div class="connection-name">[Entity Name]</div>
            <div class="connection-type">[PERSON/ORG/CASE]</div>
        </div>
    </div>
    
    <!-- Expandable dropdown content (hidden by default) -->
    <div class="connection-dropdown" style="display: none;">
        <div class="connection-summary">
            <!-- Summary text loaded from connection data -->
            Loading connection details...
        </div>
        <div class="connection-sources">
            <div class="connection-sources-header">SOURCES:</div>
            <ul class="connection-sources-list">
                <!-- Source links populated dynamically -->
            </ul>
        </div>
    </div>
</div>
```

### 2. CSS STYLING

```css
/* ═══════════════════════════════════════════════════════════
   CONNECTIONS PANEL - PHASE 4 UPDATES
   ═══════════════════════════════════════════════════════════ */

/* Connection item header - clickable to expand */
.connection-header {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px;
    cursor: pointer;
    transition: background 0.2s;
}

.connection-header:hover {
    background: rgba(45, 31, 61, 0.5);
}

/* Expand/collapse icon */
.connection-expand-icon {
    font-size: 10px;
    color: var(--smoke, #a8a8a8);
    transition: transform 0.2s;
    width: 12px;
    text-align: center;
}

.connection-item.expanded .connection-expand-icon {
    transform: rotate(90deg);
}

/* Remove old badge styling - hide if still present */
.connection-badge,
.connection-item [class*="badge"],
.connection-item .documented-badge,
.connection-item .associated-badge,
.connection-item .referenced-badge {
    display: none !important;
}

/* Dropdown container */
.connection-dropdown {
    padding: 0 12px 12px 34px; /* Indent to align with name */
    border-bottom: 1px solid rgba(107, 82, 128, 0.2);
    animation: dropdownExpand 0.2s ease-out;
}

@keyframes dropdownExpand {
    from {
        opacity: 0;
        max-height: 0;
    }
    to {
        opacity: 1;
        max-height: 500px;
    }
}

/* Summary text */
.connection-summary {
    font-size: 13px;
    line-height: 1.6;
    color: var(--mist, #d4d4d4);
    padding: 12px;
    background: rgba(26, 16, 37, 0.6);
    border: 1px solid rgba(107, 82, 128, 0.3);
    border-radius: 6px;
    margin-bottom: 12px;
}

/* Sources section */
.connection-sources {
    padding-top: 8px;
}

.connection-sources-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.1em;
    color: var(--ancient-gold, #c9a227);
    margin-bottom: 8px;
}

.connection-sources-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.connection-source-link {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    background: rgba(45, 31, 61, 0.4);
    border: 1px solid rgba(107, 82, 128, 0.2);
    border-radius: 4px;
    color: var(--light-gold, #e8d48b);
    text-decoration: none;
    font-size: 12px;
    transition: all 0.2s;
    cursor: pointer;
}

.connection-source-link:hover {
    background: rgba(45, 31, 61, 0.7);
    border-color: var(--ancient-gold, #c9a227);
}

.connection-source-link .source-icon {
    font-size: 14px;
}

.connection-source-link .source-title {
    flex: 1;
}

.connection-source-link .source-date {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--smoke, #a8a8a8);
}

/* View Connections Brief button */
.view-connections-brief-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    background: rgba(201, 162, 39, 0.15);
    border: 1px solid rgba(201, 162, 39, 0.4);
    border-radius: 4px;
    color: var(--ancient-gold, #c9a227);
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.2s;
}

.view-connections-brief-btn:hover {
    background: rgba(201, 162, 39, 0.25);
    border-color: var(--ancient-gold, #c9a227);
}

/* Connections panel header update */
.connections-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px;
    border-bottom: 1px solid rgba(201, 162, 39, 0.2);
}

.connections-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--ancient-gold, #c9a227);
}

.connections-count {
    font-size: 12px;
    color: var(--smoke, #a8a8a8);
}
```

### 3. JAVASCRIPT - DROPDOWN EXPANSION

```javascript
/* ═══════════════════════════════════════════════════════════
   CONNECTION DROPDOWN EXPANSION
   ═══════════════════════════════════════════════════════════ */

/**
 * Initialize connection dropdown functionality
 */
function initConnectionDropdowns() {
    const connectionsContainer = document.querySelector('.connections-list');
    if (!connectionsContainer) return;
    
    // Event delegation for connection clicks
    connectionsContainer.addEventListener('click', (e) => {
        const header = e.target.closest('.connection-header');
        if (!header) return;
        
        const connectionItem = header.closest('.connection-item');
        if (!connectionItem) return;
        
        // Don't expand if clicking on something that navigates
        if (e.target.closest('.connection-navigate-btn')) return;
        
        toggleConnectionDropdown(connectionItem);
    });
}

/**
 * Toggle dropdown expansion for a connection item
 */
function toggleConnectionDropdown(connectionItem) {
    const dropdown = connectionItem.querySelector('.connection-dropdown');
    const isExpanded = connectionItem.classList.contains('expanded');
    
    if (isExpanded) {
        // Collapse
        connectionItem.classList.remove('expanded');
        dropdown.style.display = 'none';
    } else {
        // Expand
        connectionItem.classList.add('expanded');
        dropdown.style.display = 'block';
        
        // Load connection details if not already loaded
        if (dropdown.dataset.loaded !== 'true') {
            loadConnectionDetails(connectionItem);
        }
    }
}

/**
 * Load connection summary and sources for dropdown
 */
async function loadConnectionDetails(connectionItem) {
    const targetEntityId = connectionItem.dataset.targetEntity;
    const currentEntityId = currentFocalEntityId; // From Phase 3
    const dropdown = connectionItem.querySelector('.connection-dropdown');
    const summaryEl = dropdown.querySelector('.connection-summary');
    const sourcesList = dropdown.querySelector('.connection-sources-list');
    
    // Get connection data
    const connectionData = getConnectionData(currentEntityId, targetEntityId);
    
    if (!connectionData) {
        summaryEl.textContent = 'Connection details not available.';
        sourcesList.innerHTML = '';
        dropdown.dataset.loaded = 'true';
        return;
    }
    
    // Populate summary
    summaryEl.textContent = connectionData.summary || 'Connection documented in source materials.';
    
    // Populate sources
    if (connectionData.sources && connectionData.sources.length > 0) {
        sourcesList.innerHTML = connectionData.sources.map(source => `
            <li>
                <a class="connection-source-link" 
                   href="#" 
                   data-source-id="${source.id}"
                   data-source-type="${source.type}"
                   onclick="openSourceDocument('${source.id}'); return false;">
                    <span class="source-icon">📄</span>
                    <span class="source-title">${source.title}</span>
                    ${source.date ? `<span class="source-date">${source.date}</span>` : ''}
                </a>
            </li>
        `).join('');
    } else {
        sourcesList.innerHTML = '<li class="no-sources">No source documents linked</li>';
    }
    
    dropdown.dataset.loaded = 'true';
}

/**
 * Get connection data between two entities
 * This pulls from your connections data structure
 */
function getConnectionData(entityId1, entityId2) {
    // Check if connection briefs data exists
    if (typeof connectionBriefs !== 'undefined' && connectionBriefs[entityId1]) {
        const brief = connectionBriefs[entityId1];
        const connection = brief.connections?.find(c => c.entityId === entityId2);
        if (connection) return connection;
    }
    
    // Fallback to entity connection data
    const entity = D.ent?.[entityId1] || window.entitiesData?.[entityId1];
    if (!entity || !entity.connections) return null;
    
    const conn = entity.connections.find(c => 
        c.targetId === entityId2 || c.id === entityId2 || c.entityId === entityId2
    );
    
    if (!conn) return null;
    
    return {
        summary: conn.summary || conn.description || conn.notes || null,
        sources: conn.sources || conn.documents || []
    };
}

/**
 * Open source document in viewer
 * Reuses existing document modal from brief view
 */
function openSourceDocument(sourceId) {
    // Check if document viewer modal exists
    const modal = document.getElementById('documentModal') || document.querySelector('.document-modal');
    
    if (modal && typeof showDocumentModal === 'function') {
        showDocumentModal(sourceId);
    } else {
        // Fallback: try to navigate to document
        const source = findSourceById(sourceId);
        if (source && source.url) {
            window.open(source.url, '_blank');
        } else {
            console.warn('Document viewer not available for:', sourceId);
        }
    }
}

function findSourceById(sourceId) {
    // Search through all entities for the source
    const entities = Object.values(D.ent || window.entitiesData || {});
    for (const entity of entities) {
        const doc = entity.documents?.find(d => d.id === sourceId);
        if (doc) return doc;
    }
    return null;
}
```

### 4. VIEW CONNECTIONS BRIEF BUTTON

```javascript
/* ═══════════════════════════════════════════════════════════
   VIEW CONNECTIONS BRIEF BUTTON
   ═══════════════════════════════════════════════════════════ */

/**
 * Add "View Connections Brief" button to panel header
 */
function addConnectionsBriefButton() {
    const header = document.querySelector('.connections-header') || 
                   document.querySelector('.entity-section-title:contains("Connections")');
    
    if (!header) return;
    
    // Check if button already exists
    if (header.querySelector('.view-connections-brief-btn')) return;
    
    // Restructure header if needed
    const headerContent = header.innerHTML;
    header.innerHTML = `
        <div class="connections-header-left">
            <span class="connections-title">Connections</span>
            <span class="connections-count"></span>
        </div>
        <button class="view-connections-brief-btn" onclick="openConnectionsBrief()">
            📋 View Connections Brief
        </button>
    `;
}

/**
 * Open the full Connections Brief document
 */
function openConnectionsBrief() {
    const entityId = currentFocalEntityId;
    if (!entityId) {
        console.warn('No focal entity selected');
        return;
    }
    
    // Check for connections brief file/data
    const briefPath = `/continuum/briefs/connections/${entityId}_connections.md`;
    
    // Try to load in existing brief modal
    if (typeof showBriefModal === 'function') {
        showBriefModal(briefPath, 'connections');
    } else if (typeof openDocumentModal === 'function') {
        openDocumentModal(briefPath);
    } else {
        // Fallback: fetch and display inline
        loadAndDisplayConnectionsBrief(entityId);
    }
}

/**
 * Fallback: Load and display connections brief inline
 */
async function loadAndDisplayConnectionsBrief(entityId) {
    const briefPath = `/continuum/briefs/connections/${entityId}_connections.md`;
    
    try {
        const response = await fetch(briefPath);
        if (!response.ok) throw new Error('Brief not found');
        
        const markdown = await response.text();
        const html = marked ? marked.parse(markdown) : `<pre>${markdown}</pre>`;
        
        // Create modal
        const modal = document.createElement('div');
        modal.className = 'connections-brief-modal';
        modal.innerHTML = `
            <div class="connections-brief-backdrop" onclick="this.parentElement.remove()"></div>
            <div class="connections-brief-content">
                <div class="connections-brief-header">
                    <h2>Connections Brief</h2>
                    <button class="close-btn" onclick="this.closest('.connections-brief-modal').remove()">✕</button>
                </div>
                <div class="connections-brief-body">
                    ${html}
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
    } catch (error) {
        console.warn('Connections brief not available:', error);
        alert('Connections brief not yet generated for this entity.\n\nRun Phase 5 to generate connection briefs.');
    }
}
```

### 5. REMOVE OLD BADGE LABELS

```javascript
/* ═══════════════════════════════════════════════════════════
   REMOVE "DOCUMENTED/ASSOCIATED/REFERENCED" BADGES
   ═══════════════════════════════════════════════════════════ */

/**
 * Clean up old badge elements from connections panel
 */
function removeOldConnectionBadges() {
    // Find and remove all badge elements
    const badgeSelectors = [
        '.connection-badge',
        '.documented-badge',
        '.associated-badge', 
        '.referenced-badge',
        '[class*="DOCUMENT"]',
        '[class*="ASSOCIAT"]',
        '[class*="REFERENC"]'
    ];
    
    badgeSelectors.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            // Only remove if it's in the connections area
            if (el.closest('.connections-list, .connection-item')) {
                el.remove();
            }
        });
    });
    
    // Also search for text content and remove
    document.querySelectorAll('.connection-item').forEach(item => {
        // Remove any span containing these exact texts
        item.querySelectorAll('span').forEach(span => {
            const text = span.textContent.trim().toUpperCase();
            if (text === 'DOCUMENTED' || text === 'ASSOCIATED' || text === 'REFERENCED') {
                span.remove();
            }
        });
    });
}

// Run cleanup on page load and after rendering connections
document.addEventListener('DOMContentLoaded', removeOldConnectionBadges);
```

### 6. UPDATE CONNECTION RENDERING

```javascript
/* ═══════════════════════════════════════════════════════════
   UPDATED CONNECTION ITEM RENDERING
   ═══════════════════════════════════════════════════════════ */

/**
 * Render connection item with new structure (no badges, with dropdown)
 */
function renderConnectionItem(connection, index) {
    const targetEntity = D.ent?.[connection.targetId] || 
                        window.entitiesData?.[connection.targetId] ||
                        { name: connection.name || connection.targetId, type: 'unknown' };
    
    const name = targetEntity.name || targetEntity.nm || connection.name;
    const type = targetEntity.type || connection.type || 'entity';
    const initials = getInitials(name);
    
    // Get entity colors for avatar
    const colors = getEntityColors(targetEntity);
    const avatarBg = colors.length === 1 ? colors[0] : 
                     `linear-gradient(135deg, ${colors.join(', ')})`;
    
    return `
        <div class="connection-item" 
             data-connection-id="${connection.id || index}"
             data-target-entity="${connection.targetId || connection.id}">
            <div class="connection-header">
                <span class="connection-expand-icon">▶</span>
                <div class="connection-avatar" style="background: ${avatarBg}">
                    ${initials}
                </div>
                <div class="connection-info">
                    <div class="connection-name">${name}</div>
                    <div class="connection-type">${type.toUpperCase()}</div>
                </div>
            </div>
            <div class="connection-dropdown" style="display: none;" data-loaded="false">
                <div class="connection-summary">Loading connection details...</div>
                <div class="connection-sources">
                    <div class="connection-sources-header">SOURCES:</div>
                    <ul class="connection-sources-list"></ul>
                </div>
            </div>
        </div>
    `;
}

/**
 * Render full connections list with new structure
 */
function renderConnectionsList(entity) {
    const container = document.querySelector('.connections-list');
    if (!container) return;
    
    const connections = entity.connections || [];
    
    // Update count in header
    const countEl = document.querySelector('.connections-count');
    if (countEl) countEl.textContent = `(${connections.length})`;
    
    // Render items
    container.innerHTML = connections.map((conn, i) => 
        renderConnectionItem(conn, i)
    ).join('');
    
    // Clean up any old badges that might have been added
    removeOldConnectionBadges();
    
    // Initialize dropdown handlers
    initConnectionDropdowns();
}
```

### 7. INTEGRATION

```javascript
/* ═══════════════════════════════════════════════════════════
   INTEGRATE WITH EXISTING PANEL RENDERING
   ═══════════════════════════════════════════════════════════ */

// Hook into existing entity selection
const originalShowEnt = typeof showEnt === 'function' ? showEnt : null;

if (originalShowEnt) {
    window.showEnt = function(entityId) {
        // Call original
        originalShowEnt(entityId);
        
        // Add connections brief button
        setTimeout(() => {
            addConnectionsBriefButton();
            removeOldConnectionBadges();
        }, 100);
    };
}

// Also hook into panel rendering if different function
const originalRenderPanel = typeof renderEntityPanel === 'function' ? renderEntityPanel : null;

if (originalRenderPanel) {
    window.renderEntityPanel = function(entity) {
        originalRenderPanel(entity);
        
        setTimeout(() => {
            addConnectionsBriefButton();
            removeOldConnectionBadges();
            initConnectionDropdowns();
        }, 100);
    };
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initConnectionDropdowns();
    addConnectionsBriefButton();
    removeOldConnectionBadges();
});
```

---

## VERIFICATION CHECKLIST

After implementation, verify each item:

- [ ] "DOCUMENTED" badges no longer visible in connections panel
- [ ] "ASSOCIATED" badges no longer visible
- [ ] "REFERENCED" badges no longer visible
- [ ] Connection items show expand icon (▶)
- [ ] Clicking connection header expands dropdown
- [ ] Expand icon rotates to ▼ when expanded
- [ ] Dropdown shows summary text
- [ ] Dropdown shows "SOURCES:" header
- [ ] Source links are clickable
- [ ] Clicking source link opens document viewer
- [ ] "View Connections Brief" button visible in panel header
- [ ] Clicking "View Connections Brief" attempts to load brief
- [ ] Graceful handling when brief not yet generated
- [ ] Multiple dropdowns can be expanded simultaneously
- [ ] Clicking same header again collapses dropdown
- [ ] No console errors
- [ ] Mobile touch works for expansion

---

## FILE PERMISSIONS

```bash
chmod 666 /continuum/website/continuum.html
chown nobody:users /continuum/website/continuum.html
```

---

## COMPLETION OUTPUT

**When finished, output EXACTLY this format:**

```
═══════════════════════════════════════════════════════════════
✓ PHASE 4 COMPLETE: Connections Panel Updates
═══════════════════════════════════════════════════════════════

CHANGES MADE:
  • Added expandable dropdown to connection items
  • Dropdown displays summary text
  • Dropdown displays clickable source links
  • Added "View Connections Brief" button to panel header
  • Removed DOCUMENTED/ASSOCIATED/REFERENCED badge labels

NEW UI ELEMENTS:
  • .connection-dropdown - expandable content area
  • .connection-summary - brief explanation of connection
  • .connection-sources-list - clickable source document links
  • .view-connections-brief-btn - opens full connections brief

BACKUP CREATED:
  /continuum/website/backups/continuum_v[X]_[timestamp]_pre-phase4.html

VERIFICATION:
  • All 17 checklist items passing

═══════════════════════════════════════════════════════════════
READY FOR: Phase 5 - Connection Brief Generator
NEXT PROMPT: /continuum/prompts/PHASE5_CONNECTION_BRIEFS.md
═══════════════════════════════════════════════════════════════
```

---

## TROUBLESHOOTING

**Dropdown not expanding:**
- Check click event listener attached
- Verify `.connection-header` selector matches HTML
- Console.log in toggle function to debug

**Old badges still showing:**
- Run `removeOldConnectionBadges()` manually in console
- Check if badges are being re-added by other code
- Add `!important` to CSS `display: none`

**Sources not loading:**
- Check `getConnectionData` function returns data
- Verify entity data structure has `connections` array
- Console.log connection object to inspect structure

**Brief button not appearing:**
- Check header element selector
- Verify function runs after DOM ready
- Look for conflicting styles hiding button
