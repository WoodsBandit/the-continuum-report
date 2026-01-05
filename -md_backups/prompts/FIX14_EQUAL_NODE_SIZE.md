# FIX14: Remove Jeffrey Epstein Special Styling

## ISSUE
Jeffrey Epstein's node appears larger and bolder than other person nodes. He should be styled the same as every other person - no special treatment.

## LIKELY CAUSE
There's probably hardcoded logic that makes Epstein's node larger, either:
1. A special check for his ID/name
2. A "focal node" style that persists
3. A connection count-based sizing that inflates his node

## FILE
`/continuum/website/continuum.html`

## FIND THE PROBLEM

Search for any Epstein-specific code:
```bash
grep -ni "epstein" /continuum/website/continuum.html | head -20
```

Search for node sizing logic:
```bash
grep -ni "nodeSize\|node-size\|radius\|getRadius\|focal" /continuum/website/continuum.html | head -30
```

## LIKELY LOCATIONS

### 1. Node Radius Calculation (around line 4500-4600)

Look for code like:
```javascript
// BAD - gives Epstein special treatment
const radius = d.id === 'jeffrey-epstein' ? 40 : 25;

// BAD - scales by connection count (Epstein has most)
const radius = 15 + Math.sqrt(d.connections?.length || 0) * 3;
```

Should be:
```javascript
// GOOD - same size for all nodes of same type
const radius = 25;  // Fixed size for all
```

### 2. Node Creation in buildGraph() (around line 4480-4520)

Find where nodes are created and check for size variations:
```javascript
this.nodeElements = this.g.selectAll('.node')
    .data(this.nodes)
    .join('g')
    .attr('class', 'node')
    // Look for radius or size calculations here
```

### 3. CSS Classes

Check if there's a special class:
```bash
grep -ni "epstein\|focal-node\|primary-node\|main-node" /continuum/website/continuum.html | head -20
```

## FIX

### Option A: Remove Size Variation Entirely

Find the node circle creation and set fixed radius:

```javascript
// Find this pattern:
nodeGroup.append('circle')
    .attr('class', 'node-circle')
    .attr('r', d => /* some calculation */)

// Replace with fixed size:
nodeGroup.append('circle')
    .attr('class', 'node-circle')
    .attr('r', 25)  // Same for everyone
```

### Option B: Remove ID-Based Special Cases

Find and remove any Epstein-specific checks:

```javascript
// DELETE any code like this:
if (d.id === 'jeffrey-epstein' || d.name.includes('Epstein')) {
    // special styling
}
```

### Option C: Fix Connection-Based Scaling

If nodes scale by connection count, cap or remove it:

```javascript
// BEFORE (problematic - Epstein has most connections)
const radius = 15 + Math.min(d.connectionCount, 30) * 0.5;

// AFTER (equal treatment)
const radius = 25;
```

## FOCAL NODE RING (Keep This)

The gold ring around the selected/focal node is FINE - that's UI feedback showing which node is selected. Just make sure the base node size is equal.

```javascript
// This is OK - it's just a visual indicator for selection
.classed('active', d => d.id === this.activeNode?.id)

// The ring style in CSS is fine:
.node.active circle {
    stroke: var(--gold);
    stroke-width: 3;
}
```

## WHAT TO KEEP vs REMOVE

**KEEP:**
- Gold ring on selected/active node (selection indicator)
- Different colors for different entity types
- Hover effects

**REMOVE:**
- Any size differences based on ID
- Any size differences based on connection count
- Any "importance" or "centrality" scaling
- Any Epstein-specific styling

## VERIFICATION

1. Open continuum.html
2. Navigate to web view with multiple nodes visible
3. Verify Jeffrey Epstein's node is the SAME SIZE as other person nodes
4. Verify all person nodes are equal size
5. Verify organization nodes are equal size to each other
6. Verify the gold selection ring still works on active node
7. Compare: Epstein, Ghislaine Maxwell, Prince Andrew - all should be identical size

## BACKUP BEFORE CHANGES
```bash
cp /continuum/website/continuum.html /continuum/website/backups/continuum_pre-fix14.html
```
