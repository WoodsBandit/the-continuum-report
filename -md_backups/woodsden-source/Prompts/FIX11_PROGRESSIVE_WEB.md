# FEATURE: Progressive Web Building

## OVERVIEW
Change the Web layer from "show all nodes" to "build your own web through exploration."

## CURRENT BEHAVIOR (Wrong)
1. Click macro category → See entity cards ✓
2. Click entity card → Detail panel opens, BUT all 70+ nodes visible in graph ✗

## DESIRED BEHAVIOR
1. Click macro category → See entity cards ✓
2. Click entity card → **ONLY that single node appears** (focal node, centered, gold ring)
3. Detail panel shows connections list
4. Click a connection in the panel → That connected node **appears and links to focal node**
5. User progressively builds their own exploration web
6. "Show All Connections" button reveals all connected nodes at once

## VISUAL FLOW

```
Step 1: User clicks "Prince Andrew" card
┌─────────────────────────────────────┐
│                                     │
│                                     │
│            ◉ Prince Andrew          │  ← Only this node visible
│              (gold ring)            │
│                                     │
│                                     │
└─────────────────────────────────────┘

Step 2: User clicks "Alan Dershowitz" in connections panel
┌─────────────────────────────────────┐
│                                     │
│     ○ Alan Dershowitz               │  ← New node appears
│         \                           │
│          \────────◉ Prince Andrew   │  ← Link drawn between them
│                                     │
│                                     │
└─────────────────────────────────────┘

Step 3: User clicks "Show All Connections"
┌─────────────────────────────────────┐
│  ○ Ghislaine    ○ Virginia         │
│      \           /                  │
│       \         /                   │
│        ◉ Prince Andrew              │  ← All connections revealed
│       /         \                   │
│      /           \                  │
│  ○ Epstein    ○ Dershowitz         │
└─────────────────────────────────────┘
```

## IMPLEMENTATION

### File: `/continuum/website/continuum.html`

### Step 1: Track Revealed Nodes

Add state tracking to Graph object (around line 4183):

```javascript
const Graph = {
    // ... existing properties ...
    
    // NEW: Track which nodes are revealed in progressive web
    revealedNodes: new Set(),
    focalNodeId: null,
    
    // ... rest of object ...
};
```

### Step 2: Modify Node Display on Entity Selection

In `EntitiesLayer.navigateToWebWithEntity()` (around line 3926):

```javascript
navigateToWebWithEntity(entityId) {
    const entity = Graph.nodes.find(n => n.id === entityId);
    if (!entity) {
        console.warn('Entity not found:', entityId);
        return;
    }

    // Store focal entity
    HierarchyManager.focusedEntity = entity;
    
    // NEW: Reset revealed nodes and set focal
    Graph.revealedNodes.clear();
    Graph.revealedNodes.add(entityId);
    Graph.focalNodeId = entityId;

    // Hide entities layer
    this.hide();
    
    // Show graph container
    document.getElementById('graphContainer').style.display = 'block';

    // Transition to web layer
    HierarchyManager.currentLevel = 'web';
    HierarchyManager.updateLayerIndicator();
    HierarchyManager.updateSideLevelIndicator();

    // NEW: Apply progressive visibility
    Graph.applyProgressiveVisibility();

    // Show legend
    const legend = document.getElementById('legend');
    if (legend) legend.style.display = 'flex';

    // Select the entity (opens detail panel)
    Graph.selectNode(entity);

    // Center on focal node
    setTimeout(() => {
        Graph.centerOnNode(entity);
    }, 100);
}
```

### Step 3: Add Progressive Visibility Function

Add to Graph object (after line ~4600):

```javascript
// Apply progressive visibility - only show revealed nodes
applyProgressiveVisibility() {
    // Hide all nodes except revealed ones
    this.nodeElements
        .style('display', d => this.revealedNodes.has(d.id) ? null : 'none')
        .style('opacity', d => this.revealedNodes.has(d.id) ? 1 : 0);
    
    // Hide all links except those between revealed nodes
    this.linkElements
        .style('display', d => {
            const sourceId = typeof d.source === 'object' ? d.source.id : d.source;
            const targetId = typeof d.target === 'object' ? d.target.id : d.target;
            return this.revealedNodes.has(sourceId) && this.revealedNodes.has(targetId) ? null : 'none';
        })
        .style('opacity', d => {
            const sourceId = typeof d.source === 'object' ? d.source.id : d.source;
            const targetId = typeof d.target === 'object' ? d.target.id : d.target;
            if (this.revealedNodes.has(sourceId) && this.revealedNodes.has(targetId)) {
                return d.bidirectional || d.type === 'documented' ? 0.7 : 0.4;
            }
            return 0;
        });
},

// Reveal a single node and its link to focal node
revealNode(nodeId) {
    if (this.revealedNodes.has(nodeId)) return; // Already revealed
    
    this.revealedNodes.add(nodeId);
    
    // Animate the reveal
    const node = this.nodeElements.filter(d => d.id === nodeId);
    node
        .style('display', null)
        .style('opacity', 0)
        .transition()
        .duration(400)
        .style('opacity', 1);
    
    // Show links connecting this node to other revealed nodes
    this.linkElements
        .filter(d => {
            const sourceId = typeof d.source === 'object' ? d.source.id : d.source;
            const targetId = typeof d.target === 'object' ? d.target.id : d.target;
            const involvesNewNode = sourceId === nodeId || targetId === nodeId;
            const otherNodeRevealed = this.revealedNodes.has(sourceId) && this.revealedNodes.has(targetId);
            return involvesNewNode && otherNodeRevealed;
        })
        .style('display', null)
        .style('opacity', 0)
        .transition()
        .duration(400)
        .style('opacity', d => d.bidirectional || d.type === 'documented' ? 0.7 : 0.4);
    
    // Update detail panel connection count if open
    this.updateRevealedCount();
},

// Reveal all connections to focal node at once
revealAllConnections() {
    if (!this.focalNodeId) return;
    
    // Find all nodes connected to focal node
    const connectedIds = new Set();
    this.links.forEach(link => {
        const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
        const targetId = typeof link.target === 'object' ? link.target.id : link.target;
        if (sourceId === this.focalNodeId) connectedIds.add(targetId);
        if (targetId === this.focalNodeId) connectedIds.add(sourceId);
    });
    
    // Reveal each with staggered animation
    let delay = 0;
    connectedIds.forEach(nodeId => {
        if (!this.revealedNodes.has(nodeId)) {
            setTimeout(() => this.revealNode(nodeId), delay);
            delay += 50; // 50ms stagger between reveals
        }
    });
},

// Center view on a specific node
centerOnNode(node) {
    if (!node.x || !node.y) {
        this.resetView();
        return;
    }
    
    const transform = d3.zoomIdentity
        .translate(window.innerWidth / 2, window.innerHeight / 2)
        .scale(1.5)
        .translate(-node.x, -node.y);
    
    this.svg.transition().duration(500)
        .call(this.zoom.transform, transform);
},

// Update count display
updateRevealedCount() {
    const countEl = document.getElementById('revealedCount');
    if (countEl) {
        const total = this.getConnectedCount(this.focalNodeId);
        const revealed = this.revealedNodes.size - 1; // Minus focal node
        countEl.textContent = `${revealed}/${total} connections revealed`;
    }
},

// Get count of connections to a node
getConnectedCount(nodeId) {
    let count = 0;
    this.links.forEach(link => {
        const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
        const targetId = typeof link.target === 'object' ? link.target.id : link.target;
        if (sourceId === nodeId || targetId === nodeId) count++;
    });
    return count;
}
```

### Step 4: Add "Show All Connections" Button

In the detail panel HTML (around line 2029), add button:

```html
<!-- Add after the connections section header -->
<div class="connections-controls">
    <button id="showAllConnectionsBtn" class="show-all-btn" onclick="Graph.revealAllConnections()">
        ⊕ Show All Connections
    </button>
    <span id="revealedCount" class="revealed-count">0/0 connections revealed</span>
</div>
```

### Step 5: Style the Button

Add CSS (around line 300):

```css
/* Progressive Web Controls */
.connections-controls {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 0;
    border-bottom: 1px solid rgba(139, 111, 192, 0.2);
    margin-bottom: 0.75rem;
}

.show-all-btn {
    background: linear-gradient(135deg, rgba(201, 162, 39, 0.2), rgba(201, 162, 39, 0.1));
    border: 1px solid var(--gold-dim);
    border-radius: 6px;
    padding: 0.5rem 1rem;
    color: var(--gold);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    cursor: pointer;
    transition: all 0.2s;
}

.show-all-btn:hover {
    background: linear-gradient(135deg, rgba(201, 162, 39, 0.3), rgba(201, 162, 39, 0.2));
    border-color: var(--gold);
    box-shadow: 0 0 10px rgba(201, 162, 39, 0.3);
}

.revealed-count {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--smoke);
}
```

### Step 6: Make Connection List Items Clickable to Reveal

Modify the connection click handler in `showDetail()` (around line 4873):

```javascript
// Connection item click - reveal node in graph
document.querySelectorAll('.connection-header').forEach(header => {
    header.addEventListener('click', (e) => {
        const item = header.closest('.connection-item');
        if (!item) return;
        
        const targetEntityId = item.dataset.targetEntity;
        
        // NEW: Reveal this node in the graph
        if (targetEntityId && !Graph.revealedNodes.has(targetEntityId)) {
            Graph.revealNode(targetEntityId);
        }
        
        // Toggle dropdown (existing behavior)
        const isExpanded = item.classList.contains('expanded');
        const dropdown = item.querySelector('.connection-dropdown');
        
        if (isExpanded) {
            item.classList.remove('expanded');
            dropdown.style.display = 'none';
        } else {
            item.classList.add('expanded');
            dropdown.style.display = 'block';
        }
    });
});
```

### Step 7: Visual Indicator for Revealed/Unrevealed Connections

Add CSS to show which connections are already revealed:

```css
.connection-item[data-revealed="true"] .connection-header {
    border-left: 3px solid var(--gold);
    padding-left: 0.5rem;
}

.connection-item[data-revealed="true"] .connection-name::after {
    content: " ✓";
    color: var(--gold);
    font-size: 0.8em;
}
```

Update connection list rendering to include revealed state:

```javascript
// In showDetail(), when creating connection items:
const isRevealed = Graph.revealedNodes.has(conn.id);
html += `<li class="connection-item" data-entity="${conn.id}" data-target-entity="${conn.id}" data-revealed="${isRevealed}">
    // ... rest of HTML
</li>`;
```

## VERIFICATION

1. Open continuum.html
2. Click PEOPLE → Select "Jeffrey Epstein"
3. Verify ONLY Jeffrey Epstein node appears (centered, gold ring)
4. Verify detail panel shows connections list
5. Click "Ghislaine Maxwell" in connections → Verify her node appears with link
6. Click "Show All Connections" → Verify all connected nodes appear with staggered animation
7. Verify revealed connections show checkmark in list
8. Verify count updates (e.g., "5/12 connections revealed")

## NOTES

- This fundamentally changes UX from "view everything" to "discover through exploration"
- Users build their own mental map of connections
- More engaging and less overwhelming than 70+ nodes at once
- Maintains all existing functionality, just changes initial visibility

## BACKUP BEFORE CHANGES
```bash
cp /continuum/website/continuum.html /continuum/website/backups/continuum_pre-progressive-web.html
```
