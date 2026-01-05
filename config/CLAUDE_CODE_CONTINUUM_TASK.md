# CLAUDE CODE TASK: Build Dynamic Continuum System

## Overview

Transform the static, hardcoded `continuum.html` page into a dynamic knowledge graph system that automatically populates from analytical brief markdown files. When a new analytical brief is dropped into the `/continuum/briefs/` folder, a script should:

1. Parse the markdown file for entities and connections
2. Update a central JSON data file
3. The Continuum webpage reads from this JSON to display the knowledge graph

This should work like Obsidian - connections are automatically detected based on mentions of other entities in the documents.

---

## Current State

- **Website location:** `/continuum/website/`
- **Current page:** `continuum.html` (formerly zoom.html) has hardcoded sample data
- **Analytical briefs:** 15 completed, stored as markdown files
- **Server:** Unraid at 192.168.1.139
- **Paperless API:** http://192.168.1.139:8040 (token: da99fe6aa0b8d021689126cf72b91986abbbd283)

---

## What to Build

### 1. Directory Structure

Create this structure:
```
/continuum/
├── briefs/                    # Drop analytical briefs here (markdown)
│   ├── analytical_brief_jeffrey_epstein.md
│   ├── analytical_brief_ghislaine_maxwell.md
│   └── ...
├── data/
│   ├── entities.json          # Auto-generated from briefs
│   ├── connections.json       # Auto-generated relationships
│   └── manifest.json          # List of all processed briefs
├── scripts/
│   ├── parse_brief.py         # Parse single brief → extract entities
│   ├── build_graph.py         # Rebuild entire graph from all briefs
│   ├── watch_briefs.py        # Watch folder for new files
│   └── utils.py               # Shared utilities
├── website/
│   ├── continuum.html         # Updated to read from JSON
│   ├── index.html
│   └── about.html
└── CLAUDE.md
```

### 2. Brief Parser Script (`parse_brief.py`)

Parse an analytical brief markdown file and extract:

**From the Document Classification table:**
- Subject name
- Status (Never charged, Convicted, etc.)
- Document type
- Sources

**Entity detection:**
- Subject is primary entity (type: person, organization, or case based on filename)
- Scan document for mentions of other known entities

**Connection Architecture (Updated Jan 2026):**
- **CONNECTION BRIEFS ARE THE SOURCE OF TRUTH**
- No connection exists without a corresponding pairwise connection brief
- `connections.json` is DERIVED from briefs via `build_connections_from_briefs.py`
- Each connection has: quote + source + summary (binary model - exists or doesn't)
- No subjective "strength" scoring - the source speaks for itself

**Output format per entity:**
```json
{
  "id": "jeffrey-epstein",
  "name": "Jeffrey Epstein",
  "type": "person",
  "status": "Convicted sex offender, deceased",
  "summary": "[First paragraph of Executive Summary]",
  "brief_url": "/briefs/analytical_brief_jeffrey_epstein.html",
  "sources": [
    {"ecf": "1328-44", "description": "Deposition", "url": "/sources/ecf-1328-44.pdf"}
  ],
  "mentions": ["ghislaine-maxwell", "bill-clinton", "prince-andrew", ...],
  "last_updated": "2025-12-15T22:30:00Z"
}
```

### 3. Graph Builder Script (`build_graph.py`)

Scan all briefs in `/continuum/briefs/` and:

1. Parse each brief using `parse_brief.py`
2. Build connections by cross-referencing mentions:
   - If Entity A mentions Entity B AND Entity B mentions Entity A → strong connection
   - If only one mentions the other → weak connection
3. Generate `entities.json` with all entities
4. Generate `connections.json` with all relationships:

```json
{
  "connections": [
    {
      "source": "jeffrey-epstein",
      "target": "ghislaine-maxwell",
      "type": "documented",
      "evidence": ["ECF 1328-44", "ECF 1331-12"],
      "summary": "Maxwell described as present at Epstein properties...",
      "brief_file": "epstein_maxwell_connection.md"
    },
    {
      "source": "jeffrey-epstein",
      "target": "bill-clinton",
      "type": "documented",
      "evidence": ["Flight logs", "ECF 1320-28"],
      "summary": "Flight logs show Clinton traveled on Epstein aircraft...",
      "brief_file": "epstein_clinton_connection.md"
    }
  ]
}
```

5. Generate `manifest.json` listing all processed briefs with timestamps

### 4. File Watcher Script (`watch_briefs.py`)

Use `watchdog` library to monitor `/continuum/briefs/` folder:

```python
# When new .md file is added:
1. Wait 2 seconds (ensure file is fully written)
2. Run parse_brief.py on the new file
3. Run build_graph.py to rebuild connections
4. Log the update

# When .md file is modified:
1. Re-parse that specific brief
2. Rebuild graph

# When .md file is deleted:
1. Remove entity from graph
2. Rebuild connections
```

Create a systemd service or cron job to keep this running.

### 5. Update `continuum.html`

Modify the JavaScript to:

1. **Remove hardcoded data** - Delete the `const DATA = {...}` block
2. **Fetch from JSON files:**
```javascript
async function loadData() {
    const [entities, connections] = await Promise.all([
        fetch('/data/entities.json').then(r => r.json()),
        fetch('/data/connections.json').then(r => r.json())
    ]);
    return { entities, connections };
}
```

3. **Dynamic entity rendering** - Build entity cards from JSON
4. **Dynamic connection lines** - Draw SVG connections from connections.json
5. **Search across all entities** - Filter from loaded JSON
6. **Click entity → show detail panel** with:
   - Summary from brief
   - Connections (each links to pairwise connection brief)
   - Link to full analytical brief
   - Source documents

### 6. Entity Linking System

When parsing briefs, detect mentions of other entities using:

**Known entity list** (built from existing briefs):
```python
KNOWN_ENTITIES = {
    "Jeffrey Epstein": "jeffrey-epstein",
    "Epstein": "jeffrey-epstein",
    "Ghislaine Maxwell": "ghislaine-maxwell",
    "Maxwell": "ghislaine-maxwell",
    "Bill Clinton": "bill-clinton",
    "Clinton": "bill-clinton",
    # ... etc
}
```

**Fuzzy matching** for variations:
- "President Clinton" → bill-clinton
- "Prince Andrew, Duke of York" → prince-andrew
- "the Maxwell trial" → giuffre-v-maxwell-case

**Section weighting:**
- Mentions in "The Public Record" → weight 3 (documented fact)
- Mentions in "Editorial Analysis" → weight 2 (interpreted connection)
- Mentions in other sections → weight 1 (referenced)

### 7. Brief → HTML Conversion

Create `convert_briefs.py` to:
1. Convert markdown briefs to styled HTML pages
2. Apply the purple/black/gold theme
3. Auto-link entity mentions to their Continuum pages
4. Save to `/continuum/website/briefs/`

Example: `analytical_brief_jeffrey_epstein.md` → `/briefs/jeffrey-epstein.html`

---

## Implementation Order

1. **Create directory structure**
2. **Build `parse_brief.py`** - Test on one brief
3. **Build `build_graph.py`** - Generate JSON from all 15 briefs
4. **Update `continuum.html`** - Read from JSON instead of hardcoded
5. **Test the system** - Verify entities and connections display correctly
6. **Build `watch_briefs.py`** - Auto-update on new files
7. **Build `convert_briefs.py`** - HTML versions of briefs
8. **Set up auto-run** - Systemd service or cron

---

## Entity Type Detection

Based on filename pattern:
- `analytical_brief_[name].md` where name is a person → type: "person"
- `analytical_brief_[name]_case.md` → type: "case"
- `analytical_brief_terramar_project.md` → type: "organization"

Or parse the Document Classification table for explicit type.

---

## Connection Visualization

In `continuum.html`, the Systems level should show:
- Nodes for each entity (sized by number of connections)
- Lines between connected entities (click to view connection brief)
- Color coding by entity type:
  - Person: gold
  - Organization: purple
  - Case: blue

The Events level should show:
- Cards for each case/event
- Entity chips showing who's involved
- Source type indicators (court, leaked, news, book)

---

## Sample Entity JSON Output

After processing `analytical_brief_ghislaine_maxwell.md`:

```json
{
  "id": "ghislaine-maxwell",
  "name": "Ghislaine Maxwell",
  "type": "person",
  "status": "Convicted December 2021, 20-year sentence",
  "summary": "British socialite convicted of sex trafficking charges in connection with Jeffrey Epstein. Central figure in recruitment and facilitation of victims.",
  "brief_url": "/briefs/ghislaine-maxwell.html",
  "zoom_level": "events",
  "sources": [
    {"ecf": "1328-44", "description": "Marcinkova Deposition", "case": "Giuffre v. Maxwell"},
    {"ecf": "1331-12", "description": "Ransome Affidavit", "case": "Giuffre v. Maxwell"}
  ],
  "mentions": [
    "jeffrey-epstein",
    "virginia-giuffre", 
    "prince-andrew",
    "bill-clinton",
    "alan-dershowitz",
    "terramar-project"
  ],
  "mentioned_by": [
    "jeffrey-epstein",
    "virginia-giuffre",
    "prince-andrew",
    "sarah-kellen",
    "nadia-marcinkova"
  ],
  "last_updated": "2025-12-15T22:30:00Z"
}
```

---

## Nginx Configuration

Ensure `/data/` and `/briefs/` are served:

```nginx
location /data/ {
    alias /continuum/data/;
    add_header Access-Control-Allow-Origin *;
}

location /briefs/ {
    alias /continuum/website/briefs/;
}
```

---

## Testing Checklist

- [ ] Drop new .md file in `/continuum/briefs/` → appears in Continuum within 10 seconds
- [ ] Connections auto-detected between entities
- [ ] Click entity → shows detail panel with correct info
- [ ] Search finds entities by name
- [ ] Zoom levels navigate correctly
- [ ] Mobile responsive still works
- [ ] Source links point to correct documents

---

## Files to Create

1. `/continuum/scripts/parse_brief.py`
2. `/continuum/scripts/build_graph.py`
3. `/continuum/scripts/watch_briefs.py`
4. `/continuum/scripts/convert_briefs.py`
5. `/continuum/scripts/utils.py`
6. `/continuum/data/entities.json` (generated)
7. `/continuum/data/connections.json` (generated)
8. `/continuum/data/manifest.json` (generated)
9. Updated `/continuum/website/continuum.html`

---

## Reference: Current Analytical Briefs

These 15 briefs should be processed:

| File | Entity Type | Key Connections |
|------|-------------|-----------------|
| analytical_brief_jeffrey_epstein.md | person | maxwell, giuffre, clinton, trump, andrew, dershowitz |
| analytical_brief_ghislaine_maxwell.md | person | epstein, giuffre, andrew, kellen, taylor, marcinkova |
| analytical_brief_virginia_giuffre.md | person | epstein, maxwell, andrew, dershowitz, clinton |
| analytical_brief_bill_clinton.md | person | epstein, maxwell |
| analytical_brief_donald_trump.md | person | epstein |
| analytical_brief_prince_andrew.md | person | epstein, maxwell, giuffre |
| analytical_brief_alan_dershowitz.md | person | epstein, giuffre |
| analytical_brief_glenn_dubin.md | person | epstein, maxwell |
| analytical_brief_sarah_kellen.md | person | epstein, maxwell |
| analytical_brief_nadia_marcinkova.md | person | epstein, maxwell |
| analytical_brief_lesley_groff.md | person | epstein |
| analytical_brief_emmy_taylor.md | person | epstein, maxwell |
| analytical_brief_terramar_project.md | organization | maxwell |
| analytical_brief_epstein_florida_case.md | case | epstein |
| analytical_brief_giuffre_v_maxwell_case.md | case | giuffre, maxwell, epstein |

---

## Start Here

Begin by creating `parse_brief.py` and testing it on `analytical_brief_jeffrey_epstein.md`. Show me the extracted JSON output before proceeding.
