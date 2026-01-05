# FIX01: Detail Panel Top Offset

## ISSUE
The detail panel (right side panel showing entity info when clicked) has its content cut off by the header/breadcrumb bar. The "PERSON" type label and top portion of content are hidden behind the navigation elements.

## ROOT CAUSE
- Header: `position: fixed; top: 0; z-index: 1000;` (padding ~24px + content)
- Layer Indicator (breadcrumb): `position: fixed; top: 52px; z-index: 999;` (~30-40px tall)
- Detail Panel: `position: fixed; top: 60px;` ← **This is too high**

The detail panel starts at 60px but the breadcrumb extends to approximately 85-90px.

## FILE
`/continuum/website/continuum.html`

## LOCATION
CSS section, around line 177-190:
```css
#detailPanel {
    position: fixed;
    right: -420px; top: 60px;  /* ← CHANGE THIS */
    ...
}
```

## FIX
Change `top: 60px` to `top: 90px` to clear both the header and breadcrumb.

Also update `max-height` calculation:
```css
#detailPanel {
    position: fixed;
    right: -420px; 
    top: 90px;  /* Updated from 60px */
    width: 400px;
    max-height: calc(100vh - 110px);  /* Updated from 80px */
    ...
}
```

## VERIFICATION
1. Open continuum.html
2. Navigate to any entity (click a card)
3. Verify the "PERSON" type label is fully visible at top of panel
4. Verify content is not cut off
5. Test on different viewport heights

## BACKUP BEFORE CHANGES
```bash
cp /continuum/website/continuum.html /continuum/website/backups/continuum_pre-fix01.html
```
