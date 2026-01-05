# FIX04: Side Panel Navigation - Entities Level Direct Access

## ISSUE
Clicking "ENTITIES" on the side level indicator (right side dots) shows the D3 graph view (all nodes visible) instead of the card grid. The side indicator stays on "ENTITIES" (correct) but displays wrong content.

## ROOT CAUSE
In `renderEntitiesView()` (line ~3524), there's a conditional:

```javascript
async renderEntitiesView() {
    // ...
    // If coming from macro (has selected category), show card grid
    if (this.selectedCategory) {
        EntitiesLayer.show(this.selectedCategory);
        return;
    }
    
    // Otherwise show standard graph view
    // ... shows D3 graph ...
}
```

When clicking the side panel's "ENTITIES" level:
1. If user previously selected a category (e.g., clicked "PEOPLE" box), `selectedCategory` is set → card grid shows ✓
2. If user navigates directly via side panel without selecting category, `selectedCategory` is null → falls through to graph view ✗

## FILE
`/continuum/website/continuum.html`

## LOCATION
`renderEntitiesView()` function, around line 3524-3570

## FIX

### Option A: Always Show Card Grid with Default Category (Recommended)
When no category is selected, default to "people" (the most common use case):

```javascript
async renderEntitiesView() {
    // Remove any network/layer/document nodes
    Graph.g.selectAll('.network-clusters').remove();
    Graph.g.selectAll('.layer-nodes').remove();
    Graph.g.selectAll('.document-nodes').remove();

    // Always show card grid - default to 'people' if no category selected
    const category = this.selectedCategory || 'people';
    this.selectedCategory = category;  // Store it for breadcrumb
    EntitiesLayer.show(category);
}
```

### Option B: Force User Through Macro Selection
Prevent direct navigation to entities without a category:

In the side panel click handler (line ~5186):
```javascript
document.querySelectorAll('#levelIndicator .level-node').forEach(node => {
    node.addEventListener('click', () => {
        const level = node.dataset.level;
        if (level && !node.classList.contains('disabled')) {
            // Don't navigate to web layer without a focused entity
            if (level === 'web' && !HierarchyManager.focusedEntity) {
                return;
            }
            // Don't navigate to entities without a category - go to macro instead
            if (level === 'entities' && !HierarchyManager.selectedCategory) {
                HierarchyManager.navigateToLevel('macro');
                return;
            }
            HierarchyManager.navigateToLevel(level);
        }
    });
});
```

### Option C: Show Category Picker Modal
Create a quick category selection when no category is set:

```javascript
async renderEntitiesView() {
    Graph.g.selectAll('.network-clusters').remove();
    Graph.g.selectAll('.layer-nodes').remove();
    Graph.g.selectAll('.document-nodes').remove();

    if (this.selectedCategory) {
        EntitiesLayer.show(this.selectedCategory);
        return;
    }
    
    // No category selected - show category picker or default
    // For simplicity, default to 'people'
    this.selectedCategory = 'people';
    EntitiesLayer.show('people');
}
```

## RECOMMENDED APPROACH
Use **Option A** - it's the simplest and provides good UX. Users expect to see content when clicking "ENTITIES", not a blank or wrong view.

## VERIFICATION
1. Open continuum.html
2. From macro view, click "ENTITIES" on the side panel (without clicking a category box first)
3. Verify the card grid appears (not the D3 graph)
4. Verify the default category "PEOPLE" is shown
5. Verify breadcrumb updates to show "PEOPLE" (not [CATEGORY])

## BACKUP BEFORE CHANGES
```bash
cp /continuum/website/continuum.html /continuum/website/backups/continuum_pre-fix04.html
```
