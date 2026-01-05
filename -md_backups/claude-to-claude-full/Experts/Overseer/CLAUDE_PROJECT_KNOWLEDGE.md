# THE CONTINUUM REPORT — Project Knowledge

## Overview

The Continuum Report is an independent investigative journalism platform that documents and visualizes connections within the Epstein network through an interactive web-based knowledge graph. The platform operates under the tagline "Another Node in the Decentralized Intelligence Agency."

**Live Site:** thecontinuumreport.com  
**Core Interface:** continuum.html — Interactive network visualization

---

## Architecture: Three-Layer Navigation

The visualization uses a hierarchical zoom model where users progressively drill down from broad categories to specific entities and their connections.

```
┌─────────────────────────────────────────────────────────────────┐
│                         MACRO LAYER                              │
│   Four category boxes connected to central "THE CONTINUUM"       │
│   Click a category → Navigate to Entities Layer                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       ENTITIES LAYER                             │
│   Zoomable/pannable card grid showing all entities in category   │
│   Filter search bar for name/tag searching                       │
│   Click a card → Navigate to Web Layer with that entity focal    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                         WEB LAYER                                │
│   Progressive web building — start with single focal node        │
│   Click connections in panel → Nodes appear and link             │
│   "Show All Connections" button for full reveal                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Macro Layer Design

Four category boxes at cardinal positions, connected to center circle via gold lines:

```
                 ╔═══════════════╗
                 ║    PEOPLE     ║  ← Yellow border (#FFD54F)
                 ╚═══════════════╝
                        │ (gold)
    ╔════════════╗      ◉      ╔════════════╗
    ║ GOVERNMENT ║──────────────║ FINANCIAL  ║
    ╚════════════╝  THE        ╚════════════╝
      ↑ Blue       CONTINUUM     ↑ Green
      (#5C6BC0)    (gold)        (#81C784)
                        │ (gold)
                 ╔═══════════════╗
                 ║     MEDIA     ║  ← Pink border (#F48FB1)
                 ╚═══════════════╝
```

**Design Rules:**
- Category box borders use entity type colors (see Color Schema below)
- Center circle and connecting lines are gold (#c9a227)
- Box backgrounds are dark/transparent
- NO subtitles in boxes — just category name
- NO color legend at bottom

---

## Entity Color Schema (8 Types)

| Entity Type | Color Name | Hex Code | Usage |
|-------------|------------|----------|-------|
| Person: Gov Employee | Reddish | `#E57373` | Documented government employment |
| Person: CEO/Board | Tealish | `#4DD0E1` | CEO or Board Member role |
| Person: Other | Yellow | `#FFD54F` | Default for people |
| Org: Banking/Financial | Green | `#81C784` | Banks, financial institutions |
| Org: Media | Pink | `#F48FB1` | Media companies |
| Org: Government | Dark Blue | `#5C6BC0` | Government agencies |
| Org: Other | Purple | `#9575CD` | Other organizations |
| Case | Orange | `#FFB74D` | Legal proceedings |

**Multi-Tag Entities:** Entities with 2+ category tags may display gradient between those colors.

**Node Sizing:** All nodes of the same type should be the SAME SIZE. No special treatment for any entity (including Jeffrey Epstein). The focal/selected node is distinguished by a gold ring, not by size.

---

## Progressive Web Building (Core UX Concept)

**Philosophy:** Users discover the network through exploration, not by seeing everything at once. They build their own mental map of connections.

**Flow:**
1. User clicks entity card from Entities Layer
2. **ONLY that single node appears** (centered, gold selection ring)
3. Detail panel shows connections list on right side
4. User clicks a connection in the panel → That node **animates in** with link to focal node
5. User progressively builds their exploration web
6. "Show All Connections" button reveals all connected nodes at once (staggered animation)

**Visual Indicators:**
- Revealed connections show checkmark (✓) in panel
- Counter shows "5/12 connections revealed"
- Unrevealed connections can still be clicked to reveal

---

## Entities Layer (Card Grid)

- **Zoomable/pannable grid** of entity cards
- **Filter search bar** (separate from top global search) — filters by name, tags
- Cards show: Avatar with initials, Name, Type badge, Connection count
- Click-hold to pan, scroll to zoom
- Cards sorted by connection count (most connected first)
- Clicking a card navigates to Web Layer with that entity as focal

---

## Connections Panel (Detail Panel)

When viewing an entity in Web Layer, the right panel shows:

**Header:**
- Entity type badge (colored)
- Entity name
- Status/description line
- Summary paragraph

**Sections:**
- "View Full Brief" button → Opens entity analytical brief
- "Connections (N)" header with "View Brief" button
- "Show All" button + revealed count
- Expandable connection list

**Each Connection Item:**
- Click to reveal node in graph + expand dropdown
- Dropdown shows: Connection summary, Source documents list
- Double-click to navigate and make that entity focal

---

## UI Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ TCR              [  Filter entities...  ]        37 entities    │ ← Header
├─────────────────────────────────────────────────────────────────┤
│ MACRO › PEOPLE › ENTITY NAME                                    │ ← Breadcrumb
├───────────────────────────────────────────┬─────────────────────┤
│                                           │ PERSON              │
│                                           │ Entity Name         │
│           [Main Graph/Grid Area]          │ Status line         │
│                                           │                     │
│                                           │ [Summary...]        │
│                                           │                     │
│                                           │ Connections (9)     │
│                                           │ • Connection 1  ✓   │
│                                           │ • Connection 2      │
├───────────────────────────────────────────┴─────────────────────┤
│ [+][-][⟲]                                                       │ ← Controls (left)
│ [Legend]                                                        │
│                    ●────●────○  100%                            │ ← Level indicator (center)
│                  MACRO ENTITIES WEB                             │
└─────────────────────────────────────────────────────────────────┘
```

**Key Positions:**
- Zoom controls (+, -, reset): Bottom LEFT
- Level indicator (MACRO—ENTITIES—WEB + zoom %): Bottom CENTER, horizontal
- Legend: Bottom left, above controls
- Detail panel: Right side, slides in when entity selected

---

## File Structure

```
/continuum/
├── website/
│   ├── continuum.html      ← Main visualization (single-file app)
│   ├── index.html          ← Landing page
│   └── backups/            ← Pre-change backups
├── data/
│   ├── entities.json       ← Entity data with tags, connections
│   └── connections.json    ← Connection links between entities
├── briefs/
│   ├── analytical/         ← Entity analytical briefs (legal-protected)
│   └── connections/        ← Connection briefs ({entityId}_connections.md)
├── Prompts/
│   └── 12.21 fix/          ← Implementation prompts for Claude Code
├── sources/                ← Primary source documents (PDFs)
├── scripts/                ← Python utilities
└── CLAUDE.md               ← This file (for Claude Code)
```

---

## Data Structure

### entities.json
```json
{
  "entities": [
    {
      "id": "jeffrey-epstein",
      "name": "Jeffrey Epstein",
      "type": "person",
      "tags": ["convicted", "deceased", "financier"],
      "description": "...",
      "connections": [
        {
          "targetId": "ghislaine-maxwell",
          "summary": "Long-term associate and alleged co-conspirator...",
          "sources": [
            { "id": "ecf-1331-12", "title": "Sarah Ransome Affidavit", "date": "2017-04-15" }
          ]
        }
      ]
    }
  ]
}
```

### connections.json
```json
{
  "connections": [
    {
      "source": "jeffrey-epstein",
      "target": "ghislaine-maxwell",
      "type": "documented",
      "strength": 0.95,
      "bidirectional": true
    }
  ]
}
```

---

## Legal Framework

All analytical content follows First Amendment opinion protections under Milkovich v. Lorain Journal precedent:

- Content labeled as "ANALYTICAL BRIEF — EDITORIAL COMMENTARY"
- Clear separation of documented facts from editorial analysis
- "Alternative Interpretations" sections as liability shields
- Opinion-signaling language throughout
- Source citations with clickable links to primary documents

---

## Search Behavior

**Two Search Systems:**

| Search | Location | Scope | Behavior |
|--------|----------|-------|----------|
| Global | Top header | All entities | Click result → Jump to Web with entity as focal |
| Filter | Entities Layer | Current category | Filters visible cards in real-time |

---

## Technical Notes for Claude Code

### Large File Handling
continuum.html exceeds 50k tokens. DO NOT read the full file.

```bash
# Find code locations
grep -n "SEARCH_TERM" /continuum/website/continuum.html | head -20

# Read specific sections
sed -n 'START,ENDp' /continuum/website/continuum.html

# Make targeted edits
sed -i 's/OLD/NEW/g' /continuum/website/continuum.html
```

### Before Any Changes
```bash
# Always create backup first
cp /continuum/website/continuum.html /continuum/website/backups/continuum_$(date +%Y%m%d_%H%M%S).html
```

### Key Code Locations (approximate line numbers)
- CSS Variables: ~20-80
- Header CSS: ~86-130
- Detail Panel CSS: ~176-230
- Entities Layer CSS: ~1067-1220
- Level Indicator CSS: ~1403-1450
- Controls CSS: ~1353-1375
- Graph Object: ~4183+
- Entity Colors: ~4201-4210
- Category Filters: ~3814-3822
- Navigation Handlers: ~5175+

---

## Brand Guidelines

**Colors:**
- Gold (primary accent): `#c9a227`
- Purple (secondary): `#8b6fc0`
- Void (background): `#0a0a0b`
- Pure (text): `#ffffff`
- Smoke (muted text): `#a8a8a8`
- Mist (light text): `#d4d4d4`

**Fonts:**
- Headlines: Cinzel (serif)
- Body: Source Sans 3
- Code/Data: JetBrains Mono
- Accent: Cormorant Garamond (italic quotes)

---

## Current Implementation Status

### Completed
- [x] Three-layer architecture (Macro → Entities → Web)
- [x] Macro view with 4 category boxes + center circle
- [x] Gold connecting lines on macro
- [x] Entity card grid in Entities layer
- [x] Force-directed graph in Web layer
- [x] Detail panel with connections list
- [x] Breadcrumb navigation
- [x] Progressive web building (single node → reveal connections)
- [x] Level indicator repositioned (bottom center)
- [x] Zoom controls repositioned (bottom left)

### In Progress / To Verify
- [ ] Category-specific border colors on macro boxes
- [ ] Connection summaries populated in data
- [ ] Connection briefs generated and accessible
- [ ] Source documents linked in connection dropdowns
- [ ] Equal node sizing (no Epstein special treatment)

---

## Key Principles

1. **Progressive Disclosure:** Don't overwhelm users with all information at once
2. **Exploration Over Display:** Users build their own understanding through interaction
3. **Source Verification:** Every claim links to primary source documents
4. **Legal Protection:** All editorial content follows First Amendment framework
5. **Equal Treatment:** No entity receives special visual treatment; the data speaks for itself
6. **Clean Aesthetic:** Minimal UI, dark theme, gold accents, no visual clutter

---

*Last Updated: December 21, 2024*
