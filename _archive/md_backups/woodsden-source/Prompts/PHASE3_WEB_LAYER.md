# PHASE 3: Web Layer Updates
## Continuum.html Implementation - Phase 3 of 5

---

## PHASE DETECTION CHECK (RUN FIRST)

**BEFORE DOING ANYTHING ELSE, verify prerequisites and current state:**

### Prerequisite Check - Phases 1 & 2 Complete?

Read `/continuum/website/continuum.html` and verify:

**Phase 1 indicators:**
- Macro boxes labeled "PEOPLE", "GOV", "MEDIA", "FINANCIAL" ✓
- Gold connecting lines exist ✓

**Phase 2 indicators:**
- Entities layer with `.entities-card-grid` exists ✓
- Filter search bar (`.entities-filter-search`) exists ✓
- Pan/zoom handlers for entities layer exist ✓

**If Phases 1 or 2 NOT complete, STOP and output:**
```
═══════════════════════════════════════════════════════════════
PREREQUISITES NOT MET - Cannot proceed with Phase 3
═══════════════════════════════════════════════════════════════
Phase 1 and Phase 2 must be completed before Phase 3.

MISSING: Phase [1 or 2]
PROMPT: /continuum/prompts/PHASE[X]_[NAME].md
═══════════════════════════════════════════════════════════════
```

### Phase 3 Already Complete Check

Look for these indicators:
1. **Gradient Colors:** CSS with `linear-gradient` for multi-tag entities OR a `gradient` class on entity nodes
2. **Entity Color Schema:** CSS variables or classes for: `--entity-gov-employee`, `--entity-ceo`, `--entity-banking`, `--entity-media`, `--entity-gov-org`
3. **Top-Down Gravity:** Force simulation with Y-axis bias OR `forceY` configuration pushing nodes downward from focal
4. **Focal Node Emphasis:** Larger node size and enhanced styling for `.focal-node` class

**If ALL FOUR exist, STOP and output:**
```
═══════════════════════════════════════════════════════════════
PHASE 3 ALREADY COMPLETE
═══════════════════════════════════════════════════════════════
This phase has already been implemented. No changes made.

READY FOR: Phase 4 - Connections Panel Updates
NEXT PROMPT: /continuum/prompts/PHASE4_CONNECTIONS_PANEL.md

To proceed, run Phase 4.
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
BACKUP_FILE="${BACKUP_DIR}/continuum_v${NEXT}_${TIMESTAMP}_pre-phase3.html"
cp /continuum/website/continuum.html "$BACKUP_FILE"

echo "✓ Backup created: $BACKUP_FILE"
```

---

## TASK SCOPE - PHASE 3 ONLY

### ✅ DO THESE THINGS:
1. Implement new entity color schema (8 distinct types)
2. Add gradient coloring for multi-tag entities
3. Modify force-directed graph for top-down gravity flow
4. Style focal node with emphasis (larger, brighter)
5. Update entity node rendering to use new colors

### ❌ DO NOT TOUCH:
- Macro layer (Phase 1)
- Entities layer cards/grid (Phase 2)
- Connections panel behavior (Phase 4)
- Search bars (either global or filter)
- Document/brief display

---

## DETAILED IMPLEMENTATION

### 1. ENTITY COLOR SCHEMA

**Define CSS custom properties for all entity types:**

```css
/* ═══════════════════════════════════════════════════════════
   ENTITY COLOR SCHEMA - Phase 3
   ═══════════════════════════════════════════════════════════ */

:root {
    /* PERSON TYPES */
    --entity-person-gov-employee: #E57373;    /* Reddish - Government employees */
    --entity-person-ceo-board: #4DD0E1;       /* Tealish - CEO/Board members */
    --entity-person-other: #FFD54F;           /* Yellow - Everyone else */
    
    /* ORGANIZATION TYPES */
    --entity-org-banking: #81C784;            /* Green - Banking/Financial */
    --entity-org-media: #F48FB1;              /* Pink - Media */
    --entity-org-government: #5C6BC0;         /* Dark Blue - Government orgs */
    --entity-org-other: #9575CD;              /* Purple - All other orgs */
    
    /* CASE TYPE */
    --entity-case: #FFB74D;                   /* Orange/Amber - Cases */
    
    /* NODE STYLING */
    --node-border-width: 2px;
    --node-focal-border-width: 4px;
    --node-focal-scale: 1.3;
    --node-glow-spread: 8px;
}
```

### 2. ENTITY TYPE CLASSIFICATION LOGIC

```javascript
/* ═══════════════════════════════════════════════════════════
   ENTITY TYPE CLASSIFICATION
   ═══════════════════════════════════════════════════════════ */

/**
 * Determine the primary color(s) for an entity based on type and tags
 * Returns single color or array for gradient
 */
function getEntityColors(entity) {
    const type = entity.type || entity.tp;
    const tags = entity.tags || [];
    const subtype = entity.subtype || entity.role || '';
    
    // Normalize tags to lowercase for comparison
    const normalizedTags = tags.map(t => t.toLowerCase());
    
    if (type === 'case') {
        return ['#FFB74D']; // Orange - always single color
    }
    
    if (type === 'organization' || type === 'org') {
        return getOrganizationColors(normalizedTags, subtype);
    }
    
    if (type === 'person' || type === 'per') {
        return getPersonColors(entity, normalizedTags);
    }
    
    // Default fallback
    return ['#9575CD']; // Purple
}

function getOrganizationColors(tags, subtype) {
    const colors = [];
    
    // Check for banking/financial
    if (tags.includes('banking') || tags.includes('financial') || 
        tags.includes('bank') || subtype.includes('bank') || subtype.includes('financial')) {
        colors.push('#81C784'); // Green
    }
    
    // Check for media
    if (tags.includes('media') || tags.includes('news') || 
        subtype.includes('media')) {
        colors.push('#F48FB1'); // Pink
    }
    
    // Check for government
    if (tags.includes('government') || tags.includes('gov') || 
        tags.includes('agency') || tags.includes('intelligence') ||
        subtype.includes('gov')) {
        colors.push('#5C6BC0'); // Dark Blue
    }
    
    // If no specific tags, default to "other org"
    if (colors.length === 0) {
        colors.push('#9575CD'); // Purple
    }
    
    return colors;
}

function getPersonColors(entity, tags) {
    const colors = [];
    
    // Check for government employment
    const hasGovEmployment = tags.includes('government') || 
                             tags.includes('gov-employee') ||
                             tags.includes('politician') ||
                             tags.includes('intelligence') ||
                             tags.includes('cia') || tags.includes('fbi') ||
                             tags.includes('mossad') ||
                             entity.roles?.some(r => r.toLowerCase().includes('government')) ||
                             entity.employment?.some(e => isGovernmentRole(e));
    
    // Check for CEO/Board membership
    const hasCeoBoard = tags.includes('ceo') || 
                        tags.includes('board') ||
                        tags.includes('executive') ||
                        tags.includes('chairman') ||
                        entity.roles?.some(r => isCeoBoardRole(r));
    
    if (hasGovEmployment) {
        colors.push('#E57373'); // Reddish
    }
    
    if (hasCeoBoard) {
        colors.push('#4DD0E1'); // Tealish
    }
    
    // If neither, they're "everyone else"
    if (colors.length === 0) {
        colors.push('#FFD54F'); // Yellow
    }
    
    return colors;
}

function isGovernmentRole(employment) {
    if (!employment) return false;
    const role = (employment.role || employment.title || '').toLowerCase();
    const org = (employment.organization || employment.org || '').toLowerCase();
    
    const govKeywords = ['president', 'senator', 'congressman', 'secretary', 
                         'director', 'agent', 'officer', 'cia', 'fbi', 'nsa',
                         'doj', 'department', 'administration', 'government'];
    
    return govKeywords.some(kw => role.includes(kw) || org.includes(kw));
}

function isCeoBoardRole(role) {
    if (!role) return false;
    const r = role.toLowerCase();
    return r.includes('ceo') || r.includes('chief executive') ||
           r.includes('board') || r.includes('chairman') ||
           r.includes('director') || r.includes('president');
}
```

### 3. GRADIENT COLOR RENDERING

```javascript
/* ═══════════════════════════════════════════════════════════
   GRADIENT NODE RENDERING
   ═══════════════════════════════════════════════════════════ */

/**
 * Generate CSS background for entity node
 * Single color = solid, multiple = gradient
 */
function getEntityNodeBackground(entity) {
    const colors = getEntityColors(entity);
    
    if (colors.length === 1) {
        return colors[0];
    }
    
    // Create gradient for multi-tag entities
    // Using conic gradient for circular nodes, or linear for other shapes
    if (colors.length === 2) {
        return `linear-gradient(135deg, ${colors[0]} 0%, ${colors[0]} 50%, ${colors[1]} 50%, ${colors[1]} 100%)`;
    }
    
    if (colors.length === 3) {
        return `linear-gradient(135deg, ${colors[0]} 0%, ${colors[0]} 33%, ${colors[1]} 33%, ${colors[1]} 66%, ${colors[2]} 66%, ${colors[2]} 100%)`;
    }
    
    // 4+ colors (rare)
    const stops = colors.map((color, i) => {
        const start = (i / colors.length) * 100;
        const end = ((i + 1) / colors.length) * 100;
        return `${color} ${start}%, ${color} ${end}%`;
    }).join(', ');
    
    return `linear-gradient(135deg, ${stops})`;
}

/**
 * For SVG circles, we need a different approach using defs
 */
function createSVGGradient(svgDefs, entityId, colors) {
    if (colors.length === 1) return colors[0];
    
    const gradientId = `gradient-${entityId}`;
    
    // Check if gradient already exists
    if (document.getElementById(gradientId)) {
        return `url(#${gradientId})`;
    }
    
    const gradient = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
    gradient.setAttribute('id', gradientId);
    gradient.setAttribute('x1', '0%');
    gradient.setAttribute('y1', '0%');
    gradient.setAttribute('x2', '100%');
    gradient.setAttribute('y2', '100%');
    
    colors.forEach((color, i) => {
        const stop = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
        stop.setAttribute('offset', `${(i / (colors.length - 1)) * 100}%`);
        stop.setAttribute('stop-color', color);
        gradient.appendChild(stop);
    });
    
    svgDefs.appendChild(gradient);
    return `url(#${gradientId})`;
}
```

### 4. FOCAL NODE EMPHASIS

```css
/* ═══════════════════════════════════════════════════════════
   FOCAL NODE STYLING
   ═══════════════════════════════════════════════════════════ */

/* Base node styling */
.entity-node {
    transition: all 0.3s ease;
}

/* Focal node - the starting/center entity */
.entity-node.focal-node {
    transform: scale(var(--node-focal-scale, 1.3));
    z-index: 100;
}

.entity-node.focal-node circle,
.entity-node.focal-node .node-circle {
    stroke-width: var(--node-focal-border-width, 4px);
    stroke: var(--ancient-gold, #c9a227);
    filter: drop-shadow(0 0 var(--node-glow-spread, 8px) rgba(201, 162, 39, 0.6));
}

.entity-node.focal-node text,
.entity-node.focal-node .node-label {
    font-weight: 600;
    fill: var(--pure, #f8f8f8);
}

/* For HTML-based nodes */
.node-element.focal-node {
    transform: scale(1.3);
    z-index: 100;
    box-shadow: 0 0 20px rgba(201, 162, 39, 0.5),
                0 0 40px rgba(201, 162, 39, 0.3);
    border-width: 3px;
    border-color: var(--ancient-gold, #c9a227);
}
```

```javascript
/* ═══════════════════════════════════════════════════════════
   FOCAL NODE LOGIC
   ═══════════════════════════════════════════════════════════ */

let currentFocalEntityId = null;

function setFocalNode(entityId) {
    // Remove focal class from previous
    document.querySelectorAll('.focal-node').forEach(el => {
        el.classList.remove('focal-node');
    });
    
    currentFocalEntityId = entityId;
    
    // Add focal class to new focal node
    const focalNode = document.querySelector(`[data-entity-id="${entityId}"]`);
    if (focalNode) {
        focalNode.classList.add('focal-node');
    }
    
    // If using D3, also update the simulation
    if (typeof simulation !== 'undefined' && simulation) {
        // Re-run layout to position focal at top
        applyTopDownGravity(entityId);
    }
}
```

### 5. TOP-DOWN GRAVITY (FORCE-DIRECTED LAYOUT)

```javascript
/* ═══════════════════════════════════════════════════════════
   TOP-DOWN FORCE-DIRECTED LAYOUT
   ═══════════════════════════════════════════════════════════ */

/**
 * Configure D3 force simulation for top-down flow
 * Focal node at top, connections flow downward
 */
function configureTopDownSimulation(simulation, nodes, links, focalEntityId, width, height) {
    // Find focal node
    const focalNode = nodes.find(n => n.id === focalEntityId);
    
    if (focalNode) {
        // Pin focal node near top center
        focalNode.fx = width / 2;
        focalNode.fy = 100; // Near top
    }
    
    // Calculate depth/distance from focal for each node
    const nodeDepths = calculateNodeDepths(nodes, links, focalEntityId);
    
    simulation
        .force('link', d3.forceLink(links)
            .id(d => d.id)
            .distance(100)
            .strength(0.5))
        .force('charge', d3.forceManyBody()
            .strength(-300))
        .force('center', null) // Remove center force
        .force('x', d3.forceX(width / 2).strength(0.05)) // Weak horizontal centering
        .force('y', d3.forceY()
            .y(d => {
                // Position based on depth from focal
                const depth = nodeDepths.get(d.id) || 0;
                const baseY = 100; // Focal node Y position
                const levelSpacing = 150; // Vertical space between levels
                return baseY + (depth * levelSpacing);
            })
            .strength(0.3)) // Moderate vertical pull
        .force('collision', d3.forceCollide().radius(50));
    
    return simulation;
}

/**
 * Calculate graph distance from focal node using BFS
 */
function calculateNodeDepths(nodes, links, focalEntityId) {
    const depths = new Map();
    const adjacency = new Map();
    
    // Build adjacency list
    nodes.forEach(n => adjacency.set(n.id, []));
    links.forEach(link => {
        const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
        const targetId = typeof link.target === 'object' ? link.target.id : link.target;
        adjacency.get(sourceId)?.push(targetId);
        adjacency.get(targetId)?.push(sourceId);
    });
    
    // BFS from focal
    const queue = [focalEntityId];
    depths.set(focalEntityId, 0);
    
    while (queue.length > 0) {
        const current = queue.shift();
        const currentDepth = depths.get(current);
        
        const neighbors = adjacency.get(current) || [];
        neighbors.forEach(neighbor => {
            if (!depths.has(neighbor)) {
                depths.set(neighbor, currentDepth + 1);
                queue.push(neighbor);
            }
        });
    }
    
    // Assign max depth to disconnected nodes
    const maxDepth = Math.max(...depths.values(), 0);
    nodes.forEach(n => {
        if (!depths.has(n.id)) {
            depths.set(n.id, maxDepth + 1);
        }
    });
    
    return depths;
}

/**
 * Apply top-down gravity when focal node changes
 */
function applyTopDownGravity(focalEntityId) {
    if (!simulation) return;
    
    const nodes = simulation.nodes();
    const links = simulation.force('link')?.links() || [];
    const width = window.innerWidth;
    const height = window.innerHeight;
    
    // Unpin all nodes first
    nodes.forEach(n => {
        n.fx = null;
        n.fy = null;
    });
    
    // Reconfigure with new focal
    configureTopDownSimulation(simulation, nodes, links, focalEntityId, width, height);
    
    // Reheat simulation
    simulation.alpha(0.8).restart();
}
```

### 6. UPDATE NODE RENDERING

```javascript
/* ═══════════════════════════════════════════════════════════
   UPDATED NODE RENDERING WITH NEW COLORS
   ═══════════════════════════════════════════════════════════ */

/**
 * Render or update entity nodes with new color scheme
 */
function renderEntityNodes(container, entities, focalEntityId) {
    // Ensure SVG defs exists for gradients
    let svg = container.querySelector('svg') || container;
    let defs = svg.querySelector('defs');
    if (!defs && svg.tagName === 'svg') {
        defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        svg.insertBefore(defs, svg.firstChild);
    }
    
    entities.forEach(entity => {
        const entityId = entity.id;
        const colors = getEntityColors(entity);
        const isFocal = entityId === focalEntityId;
        
        // Get or create node element
        let node = container.querySelector(`[data-entity-id="${entityId}"]`);
        
        if (!node) {
            // Create new node (implementation depends on your current structure)
            node = createEntityNode(entity);
            container.appendChild(node);
        }
        
        // Apply colors
        const fill = colors.length === 1 
            ? colors[0] 
            : createSVGGradient(defs, entityId, colors);
        
        const circle = node.querySelector('circle') || node.querySelector('.node-circle');
        if (circle) {
            circle.setAttribute('fill', fill);
        }
        
        // Apply focal styling
        if (isFocal) {
            node.classList.add('focal-node');
        } else {
            node.classList.remove('focal-node');
        }
        
        // Store colors for reference
        node.dataset.colors = JSON.stringify(colors);
        node.dataset.entityType = entity.type;
    });
}

/**
 * Get human-readable type label for entity
 */
function getEntityTypeLabel(entity) {
    const colors = getEntityColors(entity);
    
    if (entity.type === 'case') return 'CASE';
    
    if (entity.type === 'organization' || entity.type === 'org') {
        if (colors.includes('#81C784')) return 'ORG: BANKING';
        if (colors.includes('#F48FB1')) return 'ORG: MEDIA';
        if (colors.includes('#5C6BC0')) return 'ORG: GOV';
        return 'ORG';
    }
    
    if (entity.type === 'person' || entity.type === 'per') {
        if (colors.includes('#E57373') && colors.includes('#4DD0E1')) return 'PER: GOV + CEO';
        if (colors.includes('#E57373')) return 'PER: GOV';
        if (colors.includes('#4DD0E1')) return 'PER: CEO';
        return 'PER';
    }
    
    return entity.type?.toUpperCase() || 'ENTITY';
}
```

---

## VERIFICATION CHECKLIST

After implementation, verify each item:

- [ ] CSS variables for all 8 entity colors defined
- [ ] Government employees render with reddish color
- [ ] CEO/Board members render with tealish color
- [ ] "Other" people render with yellow color
- [ ] Banking orgs render with green color
- [ ] Media orgs render with pink color
- [ ] Government orgs render with dark blue color
- [ ] Other orgs render with purple color
- [ ] Cases render with orange color
- [ ] Multi-tag entities show gradient (e.g., Bill Clinton: red→teal)
- [ ] Focal node is visibly larger than other nodes
- [ ] Focal node has gold border/glow emphasis
- [ ] Focal node positioned near top of viewport
- [ ] Connected nodes flow downward from focal
- [ ] Force simulation reheat works when changing focal
- [ ] Dragging nodes still works
- [ ] No console errors
- [ ] Mobile responsive maintained

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
✓ PHASE 3 COMPLETE: Web Layer Updates
═══════════════════════════════════════════════════════════════

CHANGES MADE:
  • Implemented 8-type entity color schema
  • Added gradient coloring for multi-tag entities
  • Configured top-down gravity (focal at top, flows down)
  • Added focal node emphasis (larger, gold glow)
  • Updated node rendering to use new color logic

COLOR SCHEMA:
  • Gov Employee (Person): #E57373 (Reddish)
  • CEO/Board (Person): #4DD0E1 (Tealish)
  • Other (Person): #FFD54F (Yellow)
  • Banking (Org): #81C784 (Green)
  • Media (Org): #F48FB1 (Pink)
  • Government (Org): #5C6BC0 (Dark Blue)
  • Other (Org): #9575CD (Purple)
  • Case: #FFB74D (Orange)

BACKUP CREATED:
  /continuum/website/backups/continuum_v[X]_[timestamp]_pre-phase3.html

VERIFICATION:
  • All 18 checklist items passing

═══════════════════════════════════════════════════════════════
READY FOR: Phase 4 - Connections Panel Updates
NEXT PROMPT: /continuum/prompts/PHASE4_CONNECTIONS_PANEL.md
═══════════════════════════════════════════════════════════════
```

---

## TROUBLESHOOTING

**Gradients not appearing:**
- Verify SVG `<defs>` element exists
- Check gradient ID uniqueness
- Ensure `url(#gradient-id)` syntax correct

**Colors not matching expected:**
- Console.log `getEntityColors(entity)` output
- Check entity tags array format
- Verify classification logic conditions

**Top-down layout not working:**
- Check simulation forces configured correctly
- Verify `forceY` strength is sufficient
- Ensure focal node `fy` is pinned

**Focal node not emphasized:**
- Verify `.focal-node` class being added
- Check CSS specificity of focal styles
- Inspect computed styles in browser
