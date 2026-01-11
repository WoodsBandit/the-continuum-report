# File Structure — Complete Reference

**The Continuum Report**
**Last Updated:** 2025-12-25

---

## Directory Structure

```
/continuum/
├── CLAUDE.md                    # Main context file (LEAN VERSION)
├── CONTEXT_INDEX.md             # Additional context & archived file index
├── connection_brief_reference.md # Entity/connection JSON schemas
├── source_link_audit.md         # ECF citation standards
├── entities_index.md            # Master entity index (2,008+ entities)
├── ENTITIES_README.md           # How to use the entity index
├── index.md                     # Quick reference navigation
├── log.md                       # Session activity log
│
├── config/                      # ⭐ REFERENCE DOCUMENTATION
│   ├── legal_framework.md       # Detailed legal guidelines
│   ├── document_corpus.md       # Complete document inventory
│   ├── technical_infrastructure.md # Server, containers, API config
│   ├── file_structure.md        # This file - directory reference
│   ├── CLAUDE_CODE_CONTINUUM_TASK.md # Dynamic system specs
│   └── CLAUDE_PROJECT_KNOWLEDGE.md   # UI/UX spec for continuum.html
│
├── agents/                      # 14 custom agent definitions
│   ├── REFERENCE.md             # Agent system reference
│   ├── overseer.md              # Meta-coordination agent
│   ├── [12 specialized agents]  # Brief generator, legal auditor, etc.
│   ├── logs/                    # 📊 SESSION LOGS
│   │   ├── index.md             # Project dashboard & activity tracker
│   │   └── overseer-log.md      # Session-by-session work log
│   ├── tasks/                   # ⚡ ACTIVE TASK TRACKING
│   │   └── sources-archive/     # Sources Archive project
│   │       ├── index.md         # Project tracker + active research tasks
│   │       ├── log.md           # Append-only session work log
│   │       ├── BUILD_INSTRUCTIONS.md
│   │       └── TASK_BRIEF.md
│   ├── themes/                  # Theme-based research system
│   │   ├── THEMES_INDEX.md      # Theme overview
│   │   └── [THEME]_THEME_RESEARCH_AGENT.md
│   └── epstein-extraction/      # Document extraction agent
│       ├── index.md             # Agent index
│       ├── log.md               # Activity log
│       ├── findings/            # Extraction results
│       └── synthesis/           # Consolidated findings
│
├── briefs/                      # Working brief copies (markdown)
│   ├── entity/                  # 37 entity briefs
│   ├── connections/             # 86 connection briefs
│   ├── backup/                  # Original brief versions
│   └── INDEX.md                 # Brief index
│
├── data/                        # Canonical JSON data files
│   ├── entities.json            # 37 entities with full metadata
│   ├── connections.json         # Connection graph data
│   ├── connection_briefs.json   # Per-entity connection summaries
│   └── hierarchy.json           # Entity categorization
│
├── templates/                   # ✅ Standardized document templates
│   ├── README.md                # Template usage guide
│   ├── analytical-brief.md      # Full entity brief template
│   ├── connection-brief.md      # Connection documentation template
│   ├── opinion-narrative-short.md  # Short-form opinion piece (500-1000 words)
│   └── opinion-narrative-long.md   # Long-form opinion piece (2000-5000 words)
│
├── website/                     # Live website files
│   ├── index.html, about.html, legal.html, continuum.html
│   ├── sources/
│   │   └── index.html           # Source archive page
│   ├── data/                    # Symlink → /continuum/data/
│   │   ├── entities.json
│   │   ├── connections.json
│   │   └── hierarchy.json
│   ├── briefs/                  # Web-accessible briefs (HTML)
│   │   ├── entity/              # 37 entity briefs
│   │   └── connections/         # 86 connection briefs
│   └── sources/                 # 33,745+ hosted PDFs
│       ├── house-oversight-2025/  # 33,572 DOJ files
│       ├── giuffre-v-maxwell/     # 96 court filings
│       ├── financial-enablers/    # 15 documents
│       ├── florida-case/          # 6 documents
│       ├── maxwell-criminal/      # 4 documents
│       ├── regulatory-actions/    # 3 documents
│       ├── cia-history/           # 18 documents
│       ├── fbi-history/           # 14 documents
│       ├── fbi-vault/             # 8 FBI parts
│       ├── doj-transparency-2025/ # 8 documents
│       ├── palm-beach-investigation/ # 1 document
│       ├── epstein-sdny/          # Placeholder
│       └── epstein-estate/        # Placeholder
│
├── reports/                     # Generated reports
│   ├── MASTER_DOCUMENT_ACQUISITION_LIST.md # 249 prioritized documents
│   ├── epstein-financial-master-timeline.md # $1.4B+ financial impact
│   ├── LEGAL_AUDIT_REPORT.md    # Legal compliance audit
│   └── session_history.md       # Historical session states
│
├── work/                        # Working files and logs
│   └── claude_md_optimization_log.md # This optimization project
│
├── audits/                      # Audit logs and reports
│   ├── legal-compliance-2025-12-24/
│   ├── source-citation-audit-2025-12-24/
│   └── connection-brief-audit/
│
├── scripts/                     # Python automation (WIP)
│   ├── continuum_pipeline.py    # Main pipeline
│   ├── parse_brief.py           # Brief parser
│   ├── build_graph.py           # Graph builder
│   ├── mount-woodsden.sh        # WoodsDen mount script
│   └── check-woodsden-mount.sh  # Mount verification
│
├── documents/inbox/             # Paperless consumption directory
│
├── downloads/                   # Large file drops
│   ├── house-oversight/         # DOJ 33k files (original)
│   │   └── extracted/epstein-pdf/ # 33,564 PDFs
│   ├── doj-combined/            # DataSets 1-7 (3.2GB)
│   └── fbi-vault/               # FBI Parts 1-8
│
├── research/                    # Research files
│   ├── prince-andrew/           # 4 deep dive reports
│   ├── meeting-notes/           # Design meeting notes
│   ├── outreach/                # Collaboration outreach drafts
│   └── cia-history/             # 5 historical analysis files
│
├── _archive/                    # Archived versions
│   └── reports_analytical_briefs/ # Old brief versions
│
└── -md_backups/                 # Archived .md files
    ├── prompts/                 # 34 implementation prompts
    ├── claude-desktop/          # Old context files
    ├── claude-to-claude-original/ # Expert hierarchy files
    ├── misc/                    # Miscellaneous archived files
    └── woodsden-source/         # WoodsDen backup files
```

---

## Key Reference Documents

| Document | Purpose | Location |
|----------|---------|----------|
| CLAUDE.md | Main context (LEAN VERSION) | `/continuum/` |
| CONTEXT_INDEX.md | Additional context index | `/continuum/` |
| connection_brief_reference.md | Entity/connection schemas | `/continuum/` |
| source_link_audit.md | ECF citation standards | `/continuum/` |
| entities_index.md | Master entity index (2,008+) | `/continuum/` |
| index.md | Quick reference navigation | `/continuum/` |
| log.md | Session activity log | `/continuum/` |
| legal_framework.md | Detailed legal guidelines | `/continuum/config/` |
| document_corpus.md | Complete document inventory | `/continuum/config/` |
| technical_infrastructure.md | Server/API configuration | `/continuum/config/` |
| file_structure.md | This document | `/continuum/config/` |
| briefs/INDEX.md | Brief index | `/continuum/briefs/` |
| agents/REFERENCE.md | Agent system reference | `/continuum/agents/` |
| templates/README.md | Template usage guide | `/continuum/templates/` |

---

## Data Files (Canonical Locations)

| File | Location | Purpose |
|------|----------|---------|
| entities.json | `/continuum/data/` | Primary entity store (37 entities) |
| connections.json | `/continuum/data/` | Connection graph data |
| connection_briefs.json | `/continuum/data/` | Per-entity connection summaries |
| hierarchy.json | `/continuum/data/` | Entity categorization |

**Note:** Website data files in `/continuum/website/data/` are symlinked to `/continuum/data/`.

---

## Brief Files

| Type | Working Location | Web Location | Count |
|------|------------------|--------------|-------|
| Entity briefs (MD) | `/continuum/briefs/entity/` | — | 37 |
| Connection briefs (MD) | `/continuum/briefs/connections/` | — | 86 |
| Entity briefs (HTML) | — | `/continuum/website/briefs/entity/` | 37 |
| Connection briefs (HTML) | — | `/continuum/website/briefs/connections/` | 86 |

---

## Agent System Files

| Component | Location | Purpose |
|-----------|----------|---------|
| Agent definitions | `/continuum/agents/` | 14 custom agent .md files |
| Agent logs | `/continuum/agents/logs/` | Session activity tracking |
| Active tasks | `/continuum/agents/tasks/` | Task-specific project tracking |
| Theme research | `/continuum/agents/themes/` | Theme-based research agents |
| Document extraction | `/continuum/agents/epstein-extraction/` | Extraction agent + findings |

---

## Source Documents

| Category | Location | Files |
|----------|----------|-------|
| All sources | `/continuum/website/sources/` | 33,745 PDFs |
| DOJ 33k (web) | `/continuum/website/sources/house-oversight-2025/` | 33,572 |
| DOJ 33k (original) | `/continuum/downloads/house-oversight/extracted/epstein-pdf/` | 33,564 |
| Giuffre v Maxwell | `/continuum/website/sources/giuffre-v-maxwell/` | 96 |
| Financial enablers | `/continuum/website/sources/financial-enablers/` | 15 |
| Florida case | `/continuum/website/sources/florida-case/` | 6 |

---

## Archived Files

| Location | Contents |
|----------|----------|
| `/continuum/_archive/` | Old analytical brief versions |
| `/continuum/-md_backups/prompts/` | 34 implementation prompts |
| `/continuum/-md_backups/claude-desktop/` | Deprecated context files |
| `/continuum/-md_backups/woodsden-source/` | WoodsDen backup files |

---

*For CLAUDE.md summary, see: Section 10 (File Locations)*
