# Theme-Based Research System — Index

> **The Continuum Report — Modular Research Architecture**
>
> Version: 1.0 | Created: 2025-12-25

---

## What Are Themes?

Themes are self-contained research modules that exhaust a specific topic before connecting to the broader Continuum. Each theme produces:

- **Analytical Briefs** — Opinion-protected documentation
- **Entity Extractions** — Named persons, organizations, events
- **Connection Maps** — Relationships between entities
- **Source Documents** — Verified primary sources
- **Cross-References** — Links to other themes

---

## Active Themes

| Theme | Status | Agent File | Task File | Brief Status |
|-------|--------|------------|-----------|--------------|
| **FBI** | 🟢 COMPLETE | `FBI_THEME_RESEARCH_AGENT.md` | — | **Complete (1 entity + 3 connection briefs)** |
| **CIA/Intelligence History** | 🟡 IN PROGRESS | — | `tasks/CIA_HISTORY_ACQUISITION_PLAN.md` | Partial (18/150+ docs) |

### FBI Theme Completion Summary (2025-12-25)

**Outputs Created:**
- `briefs/entity/analytical_brief_fbi.md` — Main FBI entity brief
- `briefs/connections/fbi_epstein_investigation.md` — FBI-Epstein connection
- `briefs/connections/fbi_wexner_coconspirator.md` — FBI-Wexner co-conspirator
- `briefs/connections/fbi_maxwell_arrest.md` — FBI-Maxwell arrest
- `website/data/fbi-personnel.json` — 3 FBI personnel documented
- `website/data/fbi-theme-connections.json` — Cross-theme mapping
- `reports/fbi-investigation-timeline.md` — 1924-2022 timeline
- `research/foia/FBI_FOIA_REQUESTS.md` — 8 FOIA request templates

**Documented Gaps (for future work):**
- FBI Vault PDFs require OCR (8 files)
- Church Committee Book V too large to process
- FBI 302 reports require FOIA
- Entity brief updates needed: Wexner (CRITICAL), Epstein, Maxwell

---

## Planned Themes

| Theme | Priority | Dependencies | Notes |
|-------|----------|--------------|-------|
| **DOJ** | HIGH | FBI Theme | Institutional parent of FBI |
| **Intelligence Community** | HIGH | CIA, Mossad briefs exist | Consolidation needed |
| **Financial Enablers** | HIGH | JPMorgan, Deutsche Bank briefs exist | Consolidation needed |
| **Florida Case** | MEDIUM | FBI Theme | NPA, state prosecution |
| **NXIVM** | MEDIUM | Raniere, Bronfman, Mack briefs exist | Consolidation needed |
| **Maxwell Network** | MEDIUM | Robert Maxwell, Ghislaine briefs exist | Family connections |
| **Wexner** | HIGH | FBI Theme (co-conspirator) | Extensive documentation |

---

## Theme Lifecycle

```
1. PLANNING
   └── Identify scope, existing materials, gaps

2. CONSOLIDATION
   └── Gather all existing materials into theme folder

3. EXTRACTION
   └── Process documents, extract entities, build timelines

4. ANALYSIS
   └── Generate analytical briefs, map connections

5. INTEGRATION
   └── Cross-reference with other themes, update website

6. MAINTENANCE
   └── Add new documents as obtained (FOIA, etc.)
```

---

## Theme File Structure

Each theme creates outputs in standard locations:

```
/continuum/
├── agents/themes/
│   └── [THEME]_THEME_RESEARCH_AGENT.md   # Agent instructions
├── briefs/entity/
│   └── analytical_brief_[theme].md        # Main brief
├── briefs/connections/
│   └── [theme]_[entity].md                # Connection briefs
├── reports/
│   └── [theme]-*.md                       # Working reports
├── data/
│   └── [theme]-*.json                     # Structured data
└── website/sources/[theme]/
    └── *.pdf                              # Source documents
```

---

## How to Start a New Theme

1. **Create Agent Instructions:**
   ```
   Copy FBI_THEME_RESEARCH_AGENT.md as template
   Modify for new theme's scope and materials
   Save as [THEME]_THEME_RESEARCH_AGENT.md
   ```

2. **Update This Index:**
   ```
   Add theme to Active Themes table
   Remove from Planned Themes if applicable
   ```

3. **Execute Theme Phases:**
   ```
   Follow agent instructions
   Spawn parallel agents where indicated
   Log all progress
   ```

4. **Complete Theme:**
   ```
   Verify all checklists passed
   Update entity/connection counts in CLAUDE.md
   Mark theme as COMPLETE in index
   ```

---

## Cross-Theme Connections

Themes connect through shared entities. Example:

```
FBI Theme ←→ DOJ Theme
    └── Shared: NPA negotiations, prosecution decisions

FBI Theme ←→ Epstein Theme
    └── Shared: Investigations 2005-2007, 2019

FBI Theme ←→ Wexner Theme
    └── Shared: Co-conspirator identification July 2019
```

The `theme-connections.json` file (created during Phase 5 of each theme) maps these relationships.

---

## Quality Standards

All theme outputs must:

1. Follow Milkovich opinion-protection framework
2. Include mandatory brief sections
3. Cite primary sources with verification links
4. Acknowledge alternative interpretations
5. Pass legal-auditor agent review

---

**END OF THEMES INDEX**
