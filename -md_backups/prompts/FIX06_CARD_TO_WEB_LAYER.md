# FIX06: Card Click → Web Layer (Blank Main Area)

## ISSUE
When clicking an entity card from the PEOPLE (or other category) grid, the detail panel opens on the right but the main area (left side) is blank. The D3 graph with the focal node and connections should appear.

## ROOT CAUSE
In `navigateToWebWithEntity()` (line ~3927), the transition logic is:

```javascript
navigateToWebWithEntity(entityId) {
    const entity = Graph.nodes.find(n => n.id === entityId);
    if (!entity) return;

    HierarchyManager.focusedEntity = entity;
    this.hide();  // Hides entities layer
    
    HierarchyManager.currentLevel = 'web';
    HierarchyManager.updateLayerIndicator();
    HierarchyManager.updateSideLevelIndicator();

    // Show and select the entity in the graph
    if (Graph.nodeElements) {
        Graph.nodeElements.style('display', null);
    }
    if (Graph.linkElements) {
        Graph.linkElements.style('display', null);
    }

    Graph.selectNode(entity);
    // ...
}
```

Issues:
1. The nodes may have `display: none` from the initial macro view
2. Node positions might not be valid (x, y could be NaN or undefined)
3. The simulation might not have run to calculate positions
4. The graph container might not be visible

## FILE
`/continuum/website/continuum.html`

## LOCATION
`EntitiesLayer.navigateToWebWithEntity()` function, around line 3926-3972

## FIX

### Step 1: Ensure Graph Container is Visible
```javascript
navigateToWebWithEntity(entityId) {
    const entity = Graph.nodes.find(n => n.id === entityId);
    if (!entity) {
        console.warn('Entity not found:', entityId);
        return;
    }

    // Store focal entity
    HierarchyManager.focusedEntity = entity;

    // Hide entities layer
    this.hide();
    
    // IMPORTANT: Show graph container
    document.getElementById('graphContainer').style.display = 'block';

    // Transition to web layer
    HierarchyManager.currentLevel = 'web';
    HierarchyManager.updateLayerIndicator();
    HierarchyManager.updateSideLevelIndicator();

    // Show entity nodes and links
    if (Graph.nodeElements) {
        Graph.nodeElements.style('display', null)
            .style('opacity', 1);
    }
    if (Graph.linkElements) {
        Graph.linkElements.style('display', null)
            .style('opacity', d => d.bidirectional || d.type === 'documented' ? 0.7 : 0.4);
    }

    // Show legend
    const legend = document.getElementById('legend');
    if (legend) legend.style.display = 'flex';

    // Select the entity (this opens detail panel)
    Graph.selectNode(entity);

    // Ensure positions are valid before zooming
    if (entity.x === undefined || entity.y === undefined || isNaN(entity.x) || isNaN(entity.y)) {
        // Run simulation briefly to get positions
        Graph.simulation.alpha(0.3).restart();
        setTimeout(() => {
            this.zoomToEntity(entity);
        }, 500);
    } else {
        // Zoom to entity
        setTimeout(() => {
            this.zoomToEntity(entity);
        }, 100);
    }
},

// Add helper function
zoomToEntity(entity) {
    if (!entity.x || !entity.y) {
        Graph.resetView();
        return;
    }
    
    const transform = d3.zoomIdentity
        .translate(window.innerWidth / 2, window.innerHeight / 2)
        .scale(1.5)
        .translate(-entity.x, -entity.y);
    Graph.svg.transition().duration(500)
        .call(Graph.zoom.transform, transform);
}
```

### Step 2: Verify Node Positions Are Calculated
In `Graph.buildGraph()` (line ~4383), ensure the simulation runs to completion:

```javascript
// After creating simulation, run 300 iterations
for (let i = 0; i < 300; i++) {
    this.simulation.tick();
}
// Now all nodes have valid x, y positions
```

This is already in the code at line ~4475, so verify it's working.

### Step 3: Debug Logging (Temporary)
Add logging to understand what's happening:

```javascript
navigateToWebWithEntity(entityId) {
    console.log('navigateToWebWithEntity called with:', entityId);
    const entity = Graph.nodes.find(n => n.id === entityId);
    console.log('Found entity:', entity);
    console.log('Entity position:', entity?.x, entity?.y);
    console.log('Graph.nodeElements:', Graph.nodeElements);
    // ... rest of function
}
```

## VERIFICATION
1. Open continuum.html
2. Navigate to PEOPLE category
3. Click on "Prince Andrew" card
4. Verify the D3 graph appears in the main area with Prince Andrew highlighted
5. Verify connected nodes are visible
6. Verify zoom/pan works
7. Test with multiple entities

## BACKUP BEFORE CHANGES
```bash
cp /continuum/website/continuum.html /continuum/website/backups/continuum_pre-fix06.html
```
