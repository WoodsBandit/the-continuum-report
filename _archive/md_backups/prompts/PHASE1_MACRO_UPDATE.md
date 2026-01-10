# PHASE 1: Macro Tab Update + Layer Restructure
## Continuum.html Implementation - Phase 1 of 5

---

## PHASE DETECTION CHECK (RUN FIRST)

**BEFORE DOING ANYTHING ELSE, check if this phase is already complete:**

Read `/continuum/website/continuum.html` and check for these indicators:

1. **Box Labels Check:** Look for the macro category boxes. If they contain:
   - "PEOPLE" (not "Intelligence Networks")
   - "GOV" (not "Political Networks")
   - "MEDIA" (not "Media Networks")
   - "FINANCIAL" (not "Financial Networks")
   → PHASE 1 ALREADY COMPLETE

2. **Gold Lines Check:** Look for SVG lines or CSS borders connecting macro boxes to center circle with color `#c9a227`
   → PHASE 1 ALREADY COMPLETE

3. **Layer Names Check:** Search for the string "sources" as a layer/level name. If NOT found and layers are named "macro", "entities", "web"
   → PHASE 1 ALREADY COMPLETE

**If ANY TWO of these indicators exist, STOP IMMEDIATELY and output:**
```
═══════════════════════════════════════════════════════════════
PHASE 1 ALREADY COMPLETE
═══════════════════════════════════════════════════════════════
This phase has already been implemented. No changes made.

READY FOR: Phase 2 - Entities Layer Implementation
NEXT PROMPT: /continuum/prompts/PHASE2_ENTITIES_LAYER.md

To proceed, run Phase 2.
═══════════════════════════════════════════════════════════════
```

---

## BACKUP PROTOCOL (REQUIRED)

```bash
# Create backup directory if it doesn't exist
mkdir -p /continuum/website/backups

# Determine version number
BACKUP_DIR="/continuum/website/backups"
LATEST=$(ls "$BACKUP_DIR" 2>/dev/null | grep -oP 'continuum_v\K[0-9]+' | sort -n | tail -1)
if [ -z "$LATEST" ]; then
    NEXT=1
else
    NEXT=$((LATEST + 1))
fi

# Create backup with version and timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/continuum_v${NEXT}_${TIMESTAMP}_pre-phase1.html"
cp /continuum/website/continuum.html "$BACKUP_FILE"

echo "✓ Backup created: $BACKUP_FILE"
```

---

## TASK SCOPE - PHASE 1 ONLY

### ✅ DO THESE THINGS:
1. Change Macro tab box labels to: PEOPLE, GOV, MEDIA, FINANCIAL
2. Add gold connecting lines between boxes and center circle
3. Remove color legend from bottom of Macro view
4. Rename/restructure layer references (remove "Sources" layer)
5. Update breadcrumb format to: `MACRO > [CATEGORY] > [ENTITY]`
6. Ensure navigation targets Entities layer when clicking macro boxes

### ❌ DO NOT TOUCH:
- Entity node colors or styling
- Search bar functionality
- Connections panel behavior
- Force-directed graph physics
- Any Web layer functionality
- Entity card grid (that's Phase 2)

---

## DETAILED IMPLEMENTATION

### 1. MACRO BOX LABEL CHANGES

Locate the macro view rendering code and update:

| Old Label | New Label | Position |
|-----------|-----------|----------|
| Intelligence Networks | **PEOPLE** | Top |
| Political Networks | **GOV** | Left |
| Media Networks | **MEDIA** | Bottom |
| Financial Networks | **FINANCIAL** | Right |

**Subtitle text for each box:**

```javascript
const MACRO_CATEGORIES = {
    people: {
        label: 'PEOPLE',
        subtitle: 'Every person in The Continuum',
        position: 'top'
    },
    gov: {
        label: 'GOV', 
        subtitle: 'Government agencies, employees, foreign intelligence',
        position: 'left'
    },
    media: {
        label: 'MEDIA',
        subtitle: 'Media companies and personalities', 
        position: 'bottom'
    },
    financial: {
        label: 'FINANCIAL',
        subtitle: 'Banks and financial entities',
        position: 'right'
    }
};
```

### 2. GOLD CONNECTING LINES

Add visual connections between each category box and "THE CONTINUUM" center circle.

**Specifications:**
- Color: `#c9a227` (existing ancient-gold CSS variable)
- Stroke width: 2px
- Style: Solid line
- Z-index: Behind boxes, above background
- Must recalculate on window resize

**SVG Implementation:**

```html
<!-- Add this SVG container to the macro view, positioned absolutely -->
<svg class="macro-connections-svg" 
     style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
            pointer-events: none; z-index: 1;">
    <line class="macro-connection-line" id="line-people" stroke="#c9a227" stroke-width="2"/>
    <line class="macro-connection-line" id="line-gov" stroke="#c9a227" stroke-width="2"/>
    <line class="macro-connection-line" id="line-media" stroke="#c9a227" stroke-width="2"/>
    <line class="macro-connection-line" id="line-financial" stroke="#c9a227" stroke-width="2"/>
</svg>
```

**JavaScript to position lines:**

```javascript
function updateMacroConnectionLines() {
    const centerCircle = document.querySelector('.macro-center-circle'); // Adjust selector
    const boxes = {
        people: document.querySelector('[data-category="people"]'),
        gov: document.querySelector('[data-category="gov"]'),
        media: document.querySelector('[data-category="media"]'),
        financial: document.querySelector('[data-category="financial"]')
    };
    
    if (!centerCircle) return;
    
    const centerRect = centerCircle.getBoundingClientRect();
    const containerRect = document.querySelector('.macro-container').getBoundingClientRect();
    
    const centerX = centerRect.left + centerRect.width/2 - containerRect.left;
    const centerY = centerRect.top + centerRect.height/2 - containerRect.top;
    
    Object.entries(boxes).forEach(([key, box]) => {
        if (!box) return;
        const boxRect = box.getBoundingClientRect();
        const boxCenterX = boxRect.left + boxRect.width/2 - containerRect.left;
        const boxCenterY = boxRect.top + boxRect.height/2 - containerRect.top;
        
        const line = document.getElementById(`line-${key}`);
        if (line) {
            line.setAttribute('x1', centerX);
            line.setAttribute('y1', centerY);
            line.setAttribute('x2', boxCenterX);
            line.setAttribute('y2', boxCenterY);
        }
    });
}

// Call on load and resize
window.addEventListener('resize', updateMacroConnectionLines);
// Call after macro view renders
```

### 3. REMOVE COLOR LEGEND

Locate and remove/hide the bottom filter bar from Macro view. Look for elements like:
- Filter toggles: "All | Person | Organization | Case"
- Color key/legend explaining node colors
- Any `.filter-bar`, `.legend`, `.color-key` elements

**Keep these elements for Web layer** - only hide on Macro view:

```css
/* When in macro view, hide the filter legend */
.view-macro .filter-bar,
.view-macro .color-legend {
    display: none;
}
```

Or conditionally render based on current layer:

```javascript
function updateFilterBarVisibility(currentLayer) {
    const filterBar = document.querySelector('.filter-bar');
    if (filterBar) {
        filterBar.style.display = currentLayer === 'macro' ? 'none' : 'flex';
    }
}
```

### 4. LAYER RESTRUCTURE

**Remove all "Sources" layer references:**

Search for and remove/update:
- `'sources'` as a layer name
- Layer 4 references
- Source-level zoom thresholds
- Source view rendering code
- Breadcrumb "sources" handling

**New layer constants:**

```javascript
// OLD - Remove these patterns:
// const LAYERS = ['macro', 'networks', 'entities', 'sources'];
// case 'sources': ...
// zoomLevel === 4 ...

// NEW - Use this structure:
const LAYERS = {
    MACRO: 'macro',      // Level 1 - Category overview
    ENTITIES: 'entities', // Level 2 - Entity index/cards
    WEB: 'web'           // Level 3 - Connection graph
};

// Layer order for navigation
const LAYER_ORDER = ['macro', 'entities', 'web'];
```

### 5. BREADCRUMB FORMAT UPDATE

**Old format:** `THE CONTINUUM > EPSTEIN NETWORK > 19 ENTITIES`

**New format:** `MACRO > [CATEGORY] > [FOCAL ENTITY]`

**Update breadcrumb rendering:**

```javascript
function updateBreadcrumb(currentLayer, category, focalEntity) {
    const breadcrumb = document.querySelector('.breadcrumb');
    if (!breadcrumb) return;
    
    let parts = [];
    
    // Always show MACRO as first crumb (clickable unless current)
    if (currentLayer === 'macro') {
        parts.push('<span class="breadcrumb-current">MACRO</span>');
    } else {
        parts.push('<span class="breadcrumb-link" data-navigate="macro">MACRO</span>');
    }
    
    // Show category if in entities or web layer
    if (category && (currentLayer === 'entities' || currentLayer === 'web')) {
        if (currentLayer === 'entities') {
            parts.push('<span class="breadcrumb-current">' + category.toUpperCase() + '</span>');
        } else {
            parts.push('<span class="breadcrumb-link" data-navigate="entities" data-category="' + category + '">' + category.toUpperCase() + '</span>');
        }
    }
    
    // Show focal entity if in web layer
    if (focalEntity && currentLayer === 'web') {
        parts.push('<span class="breadcrumb-current">' + focalEntity.name + '</span>');
    }
    
    breadcrumb.innerHTML = parts.join(' <span class="breadcrumb-separator">›</span> ');
}
```

**Add click handlers for navigation:**

```javascript
document.querySelector('.breadcrumb').addEventListener('click', (e) => {
    const link = e.target.closest('.breadcrumb-link');
    if (!link) return;
    
    const target = link.dataset.navigate;
    const category = link.dataset.category;
    
    navigateToLayer(target, { category });
});
```

### 6. NAVIGATION FLOW UPDATE

When user clicks a Macro category box, navigate to Entities layer:

```javascript
function handleMacroCategoryClick(category) {
    // Store selected category for entities layer
    currentState.selectedCategory = category;
    
    // Navigate to entities layer
    navigateToLayer('entities', { category });
    
    // Update breadcrumb
    updateBreadcrumb('entities', category, null);
}

// Attach to category boxes
document.querySelectorAll('.macro-category-box').forEach(box => {
    box.addEventListener('click', () => {
        const category = box.dataset.category;
        handleMacroCategoryClick(category);
    });
});
```

**Note:** The actual Entities layer UI will be built in Phase 2. For now, ensure:
- Navigation state is set correctly
- No JavaScript errors occur
- Some placeholder or existing view displays

---

## VERIFICATION CHECKLIST

After implementation, verify each item:

- [ ] Macro view shows "PEOPLE" box at top position
- [ ] Macro view shows "GOV" box at left position
- [ ] Macro view shows "MEDIA" box at bottom position
- [ ] Macro view shows "FINANCIAL" box at right position
- [ ] Each box has correct subtitle text
- [ ] Gold lines visibly connect each box to center circle
- [ ] Gold lines are color `#c9a227`
- [ ] Gold lines render behind boxes
- [ ] No color legend/filter bar visible in Macro view
- [ ] Breadcrumb shows "MACRO" when at macro level
- [ ] Clicking a macro box triggers navigation (no errors)
- [ ] No console errors related to "sources" layer
- [ ] Search for "sources" in code returns 0 layer-related results
- [ ] Window resize recalculates gold line positions
- [ ] Mobile responsive layout intact

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
✓ PHASE 1 COMPLETE: Macro Tab Update + Layer Restructure
═══════════════════════════════════════════════════════════════

CHANGES MADE:
  • Box labels updated to: PEOPLE, GOV, MEDIA, FINANCIAL
  • Gold connecting lines added between boxes and center circle
  • Color legend removed from Macro view
  • Layer structure simplified to 3 levels (Sources removed)
  • Breadcrumb format updated to: MACRO > [CATEGORY] > [ENTITY]
  • Navigation wired from Macro → Entities layer

BACKUP CREATED:
  /continuum/website/backups/continuum_v[X]_[timestamp]_pre-phase1.html

VERIFICATION:
  • All 15 checklist items passing

═══════════════════════════════════════════════════════════════
READY FOR: Phase 2 - Entities Layer Implementation
NEXT PROMPT: /continuum/prompts/PHASE2_ENTITIES_LAYER.md
═══════════════════════════════════════════════════════════════
```

---

## TROUBLESHOOTING

**Gold lines not appearing:**
- Verify SVG container has `position: absolute` and correct dimensions
- Check z-index ordering (lines behind boxes)
- Confirm line coordinates are being calculated after DOM ready
- Test `updateMacroConnectionLines()` in console

**Navigation not working:**
- Check `navigateToLayer` function exists and handles 'entities'
- Verify click handlers attached after DOM ready
- Look for JavaScript errors in console

**Breadcrumb not updating:**
- Confirm `updateBreadcrumb` called after navigation
- Check selector for `.breadcrumb` element exists
- Verify innerHTML assignment not blocked by CSP
