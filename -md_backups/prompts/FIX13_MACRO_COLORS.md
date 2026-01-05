# FIX13: Macro Box Styling - Color Theory & Cleanup

## CHANGES
1. Remove subtitle text from macro boxes (just category name)
2. Change "GOV" to "GOVERNMENT"
3. Apply entity type colors to box borders:
   - PEOPLE → Yellow (#FFD54F)
   - GOVERNMENT → Dark Blue (#5C6BC0)
   - MEDIA → Pink (#F48FB1)
   - FINANCIAL → Green (#81C784)
4. Keep center circle and connecting lines gold

## FILE
`/continuum/website/continuum.html`

## FIND THE MACRO CATEGORIES DATA

Search for the categories definition (two locations):

```bash
grep -n "categories:" /continuum/website/continuum.html | head -5
grep -n "id: 'people'" /continuum/website/continuum.html | head -5
```

### Location 1: getDefaultHierarchy() (around line 2906)
### Location 2: renderMacroView() fallback (around line 3251)

## CHANGES TO MAKE

### 1. Update Category Definitions

Replace the categories array in BOTH locations with:

```javascript
categories: [
    { id: 'people', name: 'PEOPLE', position: 'top', color: '#FFD54F' },
    { id: 'gov', name: 'GOVERNMENT', position: 'left', color: '#5C6BC0' },
    { id: 'media', name: 'MEDIA', position: 'bottom', color: '#F48FB1' },
    { id: 'financial', name: 'FINANCIAL', position: 'right', color: '#81C784' }
]
```

Note: 
- Removed `subtitle` property entirely
- Changed `name: 'GOV'` to `name: 'GOVERNMENT'`
- Changed colors from all gold to entity-type specific colors

### 2. Update renderMacroView() Box Rendering

Find the section that renders macro boxes (around line 3306-3340).

**Remove the subtitle text element.** Find and DELETE this block:

```javascript
// Subtitle (smaller description)
node.append('text')
    .attr('class', 'layer-node-desc')
    .attr('x', 0)
    .attr('y', 15)
    .attr('dominant-baseline', 'middle')
    .attr('text-anchor', 'middle')
    .text(category.subtitle);
```

**Update the box stroke to use category color:**

Find:
```javascript
.attr('class', 'layer-node-bg')
.attr('stroke', 'var(--gold)')
```

Change to:
```javascript
.attr('class', 'layer-node-bg')
.attr('stroke', category.color)
```

### 3. Keep Center Circle and Lines Gold

The center "THE CONTINUUM" circle should remain gold. Verify this line exists:
```javascript
.attr('stroke', 'var(--gold)')  // For center circle
```

The connecting lines should remain gold. Verify:
```javascript
.attr('stroke', 'var(--gold)')  // For lines
```

### 4. Adjust Title Position (Since No Subtitle)

Without the subtitle, center the title vertically in the box:

Find:
```javascript
node.append('text')
    .attr('class', 'layer-node-title')
    .attr('x', 0)
    .attr('y', -5)  // or similar negative value
```

Change to:
```javascript
node.append('text')
    .attr('class', 'layer-node-title')
    .attr('x', 0)
    .attr('y', 0)  // Centered vertically
    .attr('dominant-baseline', 'middle')
```

## COMPLETE UPDATED renderMacroView BOXES SECTION

Replace the category box rendering section with:

```javascript
// Category boxes at cardinal positions
categories.forEach(category => {
    const pos = positions[category.position];
    
    const node = layerGroup.append('g')
        .attr('class', 'layer-node macro-category-box')
        .attr('transform', `translate(${pos.x}, ${pos.y})`)
        .attr('data-category', category.id)
        .style('cursor', 'pointer');
    
    // Box background - use category-specific border color
    node.append('rect')
        .attr('class', 'layer-node-bg')
        .attr('x', -110)
        .attr('y', -40)
        .attr('width', 220)
        .attr('height', 80)
        .attr('rx', 8)
        .attr('stroke', category.color)  // Category-specific color
        .attr('stroke-width', 2)
        .attr('fill', 'rgba(10, 10, 11, 0.9)');
    
    // Category title only (no subtitle)
    node.append('text')
        .attr('class', 'layer-node-title')
        .attr('x', 0)
        .attr('y', 0)
        .attr('dominant-baseline', 'middle')
        .attr('text-anchor', 'middle')
        .attr('fill', 'var(--pure)')
        .text(category.name);
    
    // Click handler
    node.on('click', () => {
        HierarchyManager.selectedCategory = category.id;
        HierarchyManager.transitionToLevel('entities');
    });
});
```

## VISUAL RESULT

```
                    ┌─────────────────┐
                    │     PEOPLE      │  ← Yellow border (#FFD54F)
                    └─────────────────┘
                           │
                           │ (gold line)
                           │
    ┌──────────────┐       ◉       ┌──────────────┐
    │  GOVERNMENT  │───────────────│  FINANCIAL   │
    └──────────────┘  (gold lines) └──────────────┘
     ↑ Blue border                  ↑ Green border
       (#5C6BC0)                      (#81C784)
                           │
                           │ (gold line)
                           │
                    ┌─────────────────┐
                    │      MEDIA      │  ← Pink border (#F48FB1)
                    └─────────────────┘
```

## CSS COLORS REFERENCE (For Consistency)

Add these CSS variables if not present (around line 26):

```css
:root {
    /* ... existing vars ... */
    
    /* Macro Category Border Colors */
    --macro-people: #FFD54F;
    --macro-gov: #5C6BC0;
    --macro-media: #F48FB1;
    --macro-financial: #81C784;
}
```

## VERIFICATION

1. Open continuum.html
2. View macro layer
3. Verify:
   - PEOPLE box has yellow border (#FFD54F)
   - GOVERNMENT box has dark blue border (#5C6BC0) - NOT "GOV"
   - MEDIA box has pink border (#F48FB1)
   - FINANCIAL box has green border (#81C784)
   - Center circle is gold
   - Connecting lines are gold
   - NO subtitle text in any box
   - Category names are centered vertically

## BACKUP BEFORE CHANGES
```bash
cp /continuum/website/continuum.html /continuum/website/backups/continuum_pre-fix13.html
```
