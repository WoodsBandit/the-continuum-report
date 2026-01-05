# FIX03: Entities Card Grid Responsive Layout

## ISSUE
When the browser window is not fullscreen, the entity cards on the left edge get cut off. Cards are clipped by the viewport edge.

## ROOT CAUSE
The `.entities-card-grid` has:
```css
position: absolute;
top: 50%;
left: 50%;
transform: translate(-50%, -50%) scale(1);
width: max-content;
max-width: 1400px;
min-width: 700px;
```

Combined with `.entities-viewport` having `overflow: hidden`, when the browser is narrower than the grid's min-width (700px), content gets clipped.

## FILE
`/continuum/website/continuum.html`

## LOCATION
CSS section, around lines 1130-1159

## FIX
Change the viewport to allow scrolling and adjust the grid positioning:

### Step 1: Update `.entities-viewport` (around line 1130)
```css
.entities-viewport {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: auto;  /* Changed from 'hidden' to 'auto' */
    cursor: grab;
}
```

### Step 2: Update `.entities-card-grid` (around line 1146)
```css
.entities-card-grid {
    /* Remove absolute centering, use margin-based centering */
    position: relative;
    margin: 160px auto 60px auto;  /* Top margin for search bar clearance */
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 220px));
    gap: 20px;
    padding: 0 60px 60px 60px;
    width: fit-content;
    max-width: 1400px;
    min-width: min(700px, 100vw - 120px);  /* Responsive min-width */
}
```

### Step 3: Update pan/zoom JavaScript (around line 3770-3773)
The current pan/zoom implementation assumes fixed positioning. After changing to scrollable:

```javascript
// In EntitiesLayer.init(), update or remove the pan/zoom handlers
// if they conflict with native scroll behavior
initPanZoom() {
    // Keep zoom functionality but let native scroll handle panning
    const viewport = document.getElementById('entitiesViewport');
    if (!viewport) return;
    
    // Remove or simplify pan handlers since we now use native scroll
    // Keep only zoom if desired
}
```

## ALTERNATIVE SIMPLER FIX
If maintaining the current centered layout is preferred, just allow overflow:

```css
.entities-viewport {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: auto;  /* Allow scroll */
    cursor: grab;
}

.entities-card-grid {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) scale(1);
    transform-origin: center center;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 220px));
    gap: 20px;
    padding: 160px 60px 60px 60px;
    width: max-content;
    max-width: calc(100vw - 60px);  /* Constrain to viewport */
    min-width: min(700px, calc(100vw - 60px));  /* Responsive */
}
```

## VERIFICATION
1. Open continuum.html in a non-maximized browser window (~800px wide)
2. Navigate to PEOPLE category
3. Verify cards on left edge are NOT cut off
4. Verify horizontal scroll appears if content is wider than viewport
5. Test at various window widths (600px, 800px, 1024px, fullscreen)

## BACKUP BEFORE CHANGES
```bash
cp /continuum/website/continuum.html /continuum/website/backups/continuum_pre-fix03.html
```
