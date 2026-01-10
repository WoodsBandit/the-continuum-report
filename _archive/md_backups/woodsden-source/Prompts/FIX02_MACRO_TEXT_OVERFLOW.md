# FIX02: Macro Box Text Overflow

## ISSUE
The GOV category box on the macro layer has its subtitle text ("Government agencies, employees, foreign intelligence") overflowing outside the box boundaries. The text extends beyond the 220px box width.

## ROOT CAUSE
SVG `<text>` elements do not automatically wrap. The code at line ~3334 simply sets:
```javascript
node.append('text')
    .attr('class', 'layer-node-desc')
    .text(category.subtitle);
```

There's no width constraint or text wrapping mechanism.

## FILE
`/continuum/website/continuum.html`

## SOLUTION OPTIONS

### Option A: Shorten Subtitles (Data Change - Recommended)
Change the subtitle text in `getDefaultHierarchy()` around line 2906-2914 and `renderMacroView()` around line 3251-3256:

```javascript
categories: [
    { id: 'people', name: 'PEOPLE', subtitle: 'Every person in The Continuum', position: 'top', color: '#c9a227' },
    { id: 'gov', name: 'GOV', subtitle: 'Government & intelligence', position: 'left', color: '#c9a227' },  // Shortened
    { id: 'media', name: 'MEDIA', subtitle: 'Media companies & personalities', position: 'bottom', color: '#c9a227' },
    { id: 'financial', name: 'FINANCIAL', subtitle: 'Banks & financial entities', position: 'right', color: '#c9a227' }
]
```

### Option B: Multi-line Text (Code Change)
Replace single text element with multiple tspans. In `renderMacroView()` around line 3332-3339, replace:

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

With:
```javascript
// Subtitle (smaller description) - wrap long text
const subtitleText = node.append('text')
    .attr('class', 'layer-node-desc')
    .attr('x', 0)
    .attr('text-anchor', 'middle');

// Split subtitle if too long (max ~25 chars per line)
const subtitle = category.subtitle || '';
const maxChars = 28;
if (subtitle.length > maxChars) {
    // Find a good break point near the middle
    const mid = Math.floor(subtitle.length / 2);
    let breakPoint = subtitle.lastIndexOf(' ', mid + 5);
    if (breakPoint < mid - 10) breakPoint = subtitle.indexOf(' ', mid);
    if (breakPoint === -1) breakPoint = maxChars;
    
    const line1 = subtitle.substring(0, breakPoint).trim();
    const line2 = subtitle.substring(breakPoint).trim();
    
    subtitleText.append('tspan')
        .attr('x', 0)
        .attr('dy', '10')
        .text(line1);
    subtitleText.append('tspan')
        .attr('x', 0)
        .attr('dy', '14')
        .text(line2);
} else {
    subtitleText.append('tspan')
        .attr('x', 0)
        .attr('dy', '15')
        .text(subtitle);
}
```

### Option C: CSS Text Overflow (Limited SVG Support)
Add to `.layer-node-desc` CSS:
```css
.layer-node-desc {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 10px;  /* Reduced from 11px */
    fill: var(--smoke);
    text-anchor: middle;
}
```

## RECOMMENDED APPROACH
Use **Option A** (shorten subtitles) as it's simplest and maintains visual consistency. The box is 220px wide; subtitles should be ~25-28 characters max.

## VERIFICATION
1. Open continuum.html
2. View macro layer
3. Verify all four category boxes have text fully contained within borders
4. Check GOV box specifically

## BACKUP BEFORE CHANGES
```bash
cp /continuum/website/continuum.html /continuum/website/backups/continuum_pre-fix02.html
```
