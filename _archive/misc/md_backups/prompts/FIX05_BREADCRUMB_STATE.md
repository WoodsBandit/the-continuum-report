# FIX05: Breadcrumb State Sync

## ISSUE
The breadcrumb bar shows `[CATEGORY]` placeholder instead of the actual selected category name when navigating via the side panel.

## ROOT CAUSE
In `updateLayerIndicator()` (line ~3690), the breadcrumb text is set based on `this.selectedCategory`:

```javascript
if (level === 'entities') {
    crumb.textContent = this.selectedCategory ? this.selectedCategory.toUpperCase() : '[CATEGORY]';
}
```

When `selectedCategory` is null (direct side panel navigation), it shows the placeholder.

## RELATIONSHIP TO FIX04
This issue is **directly related to FIX04**. If FIX04 is implemented correctly (defaulting to 'people' category when none selected), this issue will be resolved automatically.

## FILE
`/continuum/website/continuum.html`

## LOCATION
`updateLayerIndicator()` function, around line 3690-3714

## FIX (If FIX04 Not Applied)
If for some reason FIX04's approach isn't used, add a fallback in `updateLayerIndicator()`:

```javascript
updateLayerIndicator() {
    const indicator = document.getElementById('layerIndicator');
    if (indicator) {
        const crumbs = indicator.querySelectorAll('.layer-crumb');
        crumbs.forEach(crumb => {
            const level = crumb.dataset.level;
            crumb.classList.toggle('active', level === this.currentLevel);

            if (level === 'macro') {
                crumb.textContent = 'MACRO';
            } else if (level === 'entities') {
                // Default to 'PEOPLE' if no category selected but we're at entities level
                const categoryText = this.selectedCategory || 
                    (this.currentLevel === 'entities' ? 'people' : null);
                crumb.textContent = categoryText ? categoryText.toUpperCase() : '[CATEGORY]';
            } else if (level === 'web') {
                crumb.textContent = this.focusedEntity?.name || '[ENTITY]';
            }
        });
    }
    this.updateSideLevelIndicator();
}
```

## ADDITIONAL FIX: Clear Placeholder When Returning to Macro
Ensure when user returns to macro level, the placeholders reset properly:

In `navigateToLevel()` (line ~3673):
```javascript
navigateToLevel(level) {
    if (level === this.currentLevel) return;

    // Reset focused items when going up
    if (this.getLevelDepth(level) < this.getLevelDepth(this.currentLevel)) {
        if (level === 'macro' || level === 'entities') {
            this.focusedEntity = null;
        }
        if (level === 'macro') {
            this.focusedNetwork = null;
            this.selectedCategory = null;  // This already exists
        }
    }

    this.transitionToLevel(level);
}
```

This is already correct, so the main fix is ensuring FIX04 sets a default category.

## VERIFICATION
1. Apply FIX04 first
2. Open continuum.html
3. Click side panel "ENTITIES" from macro
4. Verify breadcrumb shows "PEOPLE" (or other default), NOT "[CATEGORY]"
5. Navigate to macro, click "FINANCIAL" box
6. Verify breadcrumb shows "FINANCIAL"
7. Return to macro
8. Verify breadcrumb resets properly

## BACKUP BEFORE CHANGES
```bash
cp /continuum/website/continuum.html /continuum/website/backups/continuum_pre-fix05.html
```
