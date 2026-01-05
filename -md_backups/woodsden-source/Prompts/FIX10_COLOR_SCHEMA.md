# FIX10: Entity Type Color Schema Alignment

## ISSUE
The entity colors in the web layer (D3 graph) don't match the specification. Claude Code implemented its own schema instead of the designed colors.

## CURRENT (Wrong) vs SPECIFIED (Correct)

### Current Implementation (line 4201-4210)
```javascript
entityColors: {
    'gov-employee': '#dc2626',   // Red
    'ceo': '#2563eb',            // Blue
    'politician': '#7c3aed',     // Purple
    'celebrity': '#f59e0b',      // Amber
    'royal': '#be185d',          // Magenta
    'financier': '#059669',      // Emerald
    'operator': '#dc2626',       // Red
    'general': '#6b7280'         // Gray
}
```

### Specified Schema
| Entity Type | Color Name | Hex Code |
|-------------|------------|----------|
| Person: Gov Employee | Reddish | #E57373 |
| Person: CEO/Board | Tealish | #4DD0E1 |
| Person: Other | Yellow | #FFD54F |
| Org: Banking | Green | #81C784 |
| Org: Media | Pink | #F48FB1 |
| Org: Government | Dark Blue | #5C6BC0 |
| Org: Other | Purple | #9575CD |
| Case | Orange | #FFB74D |

## FILE
`/continuum/website/continuum.html`

## LOCATIONS TO UPDATE

### 1. Entity Colors Object (line ~4201)
```javascript
entityColors: {
    // Person types
    'person-gov': '#E57373',      // Government Employee - Reddish
    'person-ceo': '#4DD0E1',      // CEO/Board Member - Tealish
    'person-other': '#FFD54F',    // Other Person - Yellow
    
    // Organization types
    'org-banking': '#81C784',     // Banking/Financial - Green
    'org-media': '#F48FB1',       // Media - Pink
    'org-gov': '#5C6BC0',         // Government Agency - Dark Blue
    'org-other': '#9575CD',       // Other Organization - Purple
    
    // Case type
    'case': '#FFB74D',            // Legal Case - Orange
    
    // Fallback
    'general': '#9E9E9E'          // Unknown - Gray
}
```

### 2. getEntityColors() Function (line ~4213)
Replace the entire function:

```javascript
getEntityColors(entity) {
    const tags = entity.tags || [];
    const type = (entity.type || '').toLowerCase();
    const tagStr = tags.join(' ').toLowerCase();
    
    // Case entities
    if (type === 'case') {
        return [this.entityColors['case']];
    }
    
    // Organization entities
    if (type === 'organization') {
        if (tagStr.includes('banking') || tagStr.includes('bank') || 
            tagStr.includes('finance') || tagStr.includes('financial')) {
            return [this.entityColors['org-banking']];
        }
        if (tagStr.includes('media') || tagStr.includes('news') || 
            tagStr.includes('journalist')) {
            return [this.entityColors['org-media']];
        }
        if (tagStr.includes('government') || tagStr.includes('agency') ||
            tagStr.includes('cia') || tagStr.includes('fbi') ||
            tagStr.includes('intelligence')) {
            return [this.entityColors['org-gov']];
        }
        return [this.entityColors['org-other']];
    }
    
    // Person entities
    if (type === 'person') {
        // Check for government/official tags
        if (tagStr.includes('government') || tagStr.includes('official') ||
            tagStr.includes('prosecutor') || tagStr.includes('agent') ||
            tagStr.includes('cia') || tagStr.includes('fbi')) {
            return [this.entityColors['person-gov']];
        }
        
        // Check for CEO/executive tags
        if (tagStr.includes('ceo') || tagStr.includes('executive') ||
            tagStr.includes('chairman') || tagStr.includes('director') ||
            tagStr.includes('board') || tagStr.includes('founder') ||
            tagStr.includes('ceo-board')) {
            return [this.entityColors['person-ceo']];
        }
        
        // Check for finance-related person (should still use person color)
        if (tagStr.includes('finance') || tagStr.includes('financier') ||
            tagStr.includes('banker') || tagStr.includes('investor')) {
            return [this.entityColors['person-ceo']];  // Use CEO color for finance people
        }
        
        // Default person
        return [this.entityColors['person-other']];
    }
    
    // Unknown type
    return [this.entityColors['general']];
}
```

### 3. CSS Variables (line ~26-40)
Update the root CSS variables:

```css
:root {
    /* ... existing variables ... */
    
    /* Entity Type Colors - Aligned with spec */
    --entity-person-gov: #E57373;      /* Person: Gov Employee - Reddish */
    --entity-person-ceo: #4DD0E1;      /* Person: CEO/Board - Tealish */
    --entity-person-other: #FFD54F;    /* Person: Other - Yellow */
    --entity-org-banking: #81C784;     /* Org: Banking - Green */
    --entity-org-media: #F48FB1;       /* Org: Media - Pink */
    --entity-org-gov: #5C6BC0;         /* Org: Government - Dark Blue */
    --entity-org-other: #9575CD;       /* Org: Other - Purple */
    --entity-case: #FFB74D;            /* Case - Orange */
}
```

### 4. Legend Colors (if legend exists)
Update the legend to show new color categories.

### 5. Card Avatar Colors (line ~1201-1212)
Update entity card avatar colors in EntitiesLayer:

```css
.entity-card[data-type="person"] .entity-card-avatar {
    background: var(--entity-person-other, #FFD54F);
}

.entity-card[data-type="organization"] .entity-card-avatar {
    background: var(--entity-org-other, #9575CD);
}

.entity-card[data-type="case"] .entity-card-avatar {
    background: var(--entity-case, #FFB74D);
}
```

## MULTI-COLOR GRADIENT SUPPORT
If an entity has multiple classifications (e.g., a CEO who is also a government official), the gradient system should still work. The `getEntityColors()` function can return multiple colors:

```javascript
getEntityColors(entity) {
    const colors = [];
    const tags = entity.tags || [];
    const type = (entity.type || '').toLowerCase();
    const tagStr = tags.join(' ').toLowerCase();
    
    if (type === 'person') {
        if (tagStr.includes('government')) colors.push(this.entityColors['person-gov']);
        if (tagStr.includes('ceo') || tagStr.includes('executive')) colors.push(this.entityColors['person-ceo']);
        if (colors.length === 0) colors.push(this.entityColors['person-other']);
    }
    // ... etc
    
    return colors.length > 0 ? colors : [this.entityColors['general']];
}
```

## VERIFICATION
1. Open continuum.html
2. Navigate to web layer with entities visible
3. Verify color coding:
   - Persons with gov tags: Reddish (#E57373)
   - Persons with CEO/exec tags: Tealish (#4DD0E1)
   - Regular persons: Yellow (#FFD54F)
   - Banking orgs: Green (#81C784)
   - Media orgs: Pink (#F48FB1)
   - Gov orgs: Dark Blue (#5C6BC0)
   - Other orgs: Purple (#9575CD)
   - Cases: Orange (#FFB74D)
4. Check entity cards have matching avatar colors
5. Verify multi-tag entities show gradient if implemented

## BACKUP BEFORE CHANGES
```bash
cp /continuum/website/continuum.html /continuum/website/backups/continuum_pre-fix10.html
```
