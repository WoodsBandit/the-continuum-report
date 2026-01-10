# FIX12: Reposition Level Indicator and Zoom Controls

## ISSUES
1. Side level indicator (MACRO dots + zoom %) overlaps the detail panel when open
2. Zoom controls (+, -, reset) at bottom-right are hidden behind detail panel

## SOLUTION
1. Move level indicator to **bottom center** (horizontal layout)
2. Move zoom controls to **bottom left**

## FILE
`/continuum/website/continuum.html`

## CHANGES

### 1. Level Indicator CSS (around line 1700-1780)

Find the `#levelIndicator` CSS and replace with:

```css
/* LEVEL INDICATOR - Bottom Center (Horizontal) */
#levelIndicator {
    position: fixed;
    bottom: 1.5rem;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 1.2rem;
    background: rgba(18, 16, 26, 0.95);
    border: 1px solid rgba(139, 111, 192, 0.3);
    border-radius: 30px;
    z-index: 100;
    backdrop-filter: blur(10px);
}

.level-track {
    display: flex;
    flex-direction: row;  /* Horizontal layout */
    align-items: center;
    gap: 0.25rem;
}

.level-node {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    cursor: pointer;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    transition: all 0.2s;
}

.level-node:hover {
    background: rgba(201, 162, 39, 0.1);
}

.level-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: rgba(139, 111, 192, 0.4);
    border: 2px solid rgba(139, 111, 192, 0.6);
    transition: all 0.3s;
}

.level-node:hover .level-dot {
    border-color: var(--gold);
}

.level-node.active .level-dot {
    background: var(--gold);
    border-color: var(--gold);
    box-shadow: 0 0 10px rgba(201, 162, 39, 0.5);
}

.level-node.visited .level-dot {
    background: rgba(139, 111, 192, 0.6);
    border-color: rgba(139, 111, 192, 0.8);
}

.level-node.disabled {
    opacity: 0.4;
    cursor: not-allowed;
    pointer-events: none;
}

.level-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--smoke);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: color 0.2s;
}

.level-node:hover .level-label,
.level-node.active .level-label {
    color: var(--gold);
}

.level-connector {
    width: 20px;
    height: 2px;
    background: rgba(139, 111, 192, 0.3);
    transition: background 0.3s;
}

.level-connector.active {
    background: var(--gold);
}

.zoom-percentage {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--smoke);
    padding-left: 0.75rem;
    border-left: 1px solid rgba(139, 111, 192, 0.3);
    margin-left: 0.5rem;
}
```

### 2. Zoom Controls CSS (around line 1353-1374)

Find the `#controls` CSS and update:

```css
/* CONTROLS - Bottom Left */
#controls {
    position: fixed;
    bottom: 1.5rem;
    left: 1.5rem;  /* Changed from right: 1.5rem */
    display: flex;
    gap: 0.5rem;
    z-index: 100;
}

.control-btn {
    width: 36px;
    height: 36px;
    background: rgba(18, 16, 26, 0.95);
    border: 1px solid rgba(139, 111, 192, 0.3);
    border-radius: 8px;
    color: var(--mist);
    font-size: 1rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
    backdrop-filter: blur(10px);
}

.control-btn:hover {
    border-color: var(--gold);
    color: var(--gold);
    background: rgba(201, 162, 39, 0.1);
}
```

### 3. Legend Position Adjustment

The legend is also at bottom-left. Move it up slightly or reposition:

```css
/* LEGEND - Bottom Left, above controls */
#legend {
    position: fixed;
    bottom: 4.5rem;  /* Increased from 1.5rem to clear controls */
    left: 1.5rem;
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    padding: 0.6rem 1rem;
    background: rgba(18, 16, 26, 0.9);
    border: 1px solid rgba(139, 111, 192, 0.3);
    border-radius: 8px;
    z-index: 50;
    max-width: 300px;
}
```

### 4. Mobile Responsive (around line 1890-1950)

Update mobile styles:

```css
@media (max-width: 768px) {
    #levelIndicator {
        bottom: 1rem;
        padding: 0.5rem 1rem;
        gap: 0.25rem;
    }
    
    .level-label {
        font-size: 0.55rem;
    }
    
    .level-connector {
        width: 12px;
    }
    
    .zoom-percentage {
        display: none;  /* Hide on mobile to save space */
    }
    
    #controls {
        bottom: 1rem;
        left: 1rem;
    }
    
    .control-btn {
        width: 32px;
        height: 32px;
        font-size: 0.9rem;
    }
    
    #legend {
        bottom: 3.5rem;
        left: 1rem;
        max-width: 250px;
    }
}
```

## VISUAL RESULT

```
┌─────────────────────────────────────────────────────┐
│ THE CONTINUUM          [search]           47 entities│  ← Header
├─────────────────────────────────────────────────────┤
│ MACRO > PEOPLE > Glenn Dubin                        │  ← Breadcrumb
├───────────────────────────────────┬─────────────────┤
│                                   │ PERSON          │
│                                   │ Glenn Dubin     │
│       [Graph Area]                │ Never charged   │
│                                   │                 │
│                                   │ Connections (9) │
│                                   │ • Emmy Taylor   │
│                                   │ • Ghislaine...  │
├───────────────────────────────────┴─────────────────┤
│ [+][-][⟲]     [Legend items...]                     │  ← Controls left
│                                                     │
│              ●─────●─────○  100%                    │  ← Level indicator center
│             MACRO  ENTITIES  WEB                    │
└─────────────────────────────────────────────────────┘
```

## VERIFICATION

1. Open continuum.html
2. Navigate to an entity (Glenn Dubin or any)
3. Verify level indicator is at **bottom center** (horizontal dots: MACRO — ENTITIES — WEB)
4. Verify zoom controls (+, -, reset) are at **bottom left**
5. Verify neither overlaps the detail panel on the right
6. Verify legend doesn't overlap controls
7. Test on narrow viewport / mobile

## BACKUP BEFORE CHANGES
```bash
cp /continuum/website/continuum.html /continuum/website/backups/continuum_pre-fix12.html
```
