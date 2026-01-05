# Additional Context Index

> Reference document for supplementary context files. Main project context is in `CLAUDE.md`.

**Last Updated:** 2025-12-24

---

## Active Reference Documents

These files provide detailed specifications referenced by CLAUDE.md:

| Document | Purpose | Location |
|----------|---------|----------|
| **connection_brief_reference.md** | Entity/connection JSON schemas, taxonomy, brief specifications | `/continuum/` |
| **source_link_audit.md** | ECF citation standards, URL patterns, verification methods | `/continuum/` |
| **CLAUDE_CODE_CONTINUUM_TASK.md** | Dynamic Continuum system specs (parse_brief.py, build_graph.py) | `/continuum/config/` |

---

## Reports Directory

Generated analysis reports in `/continuum/reports/`:

| Report | Description |
|--------|-------------|
| `MASTER_DOCUMENT_ACQUISITION_LIST.md` | 249 prioritized documents with URLs |
| `epstein-financial-master-timeline.md` | $1.4B+ financial impact timeline |
| `wexner_document_gap_analysis_2025-12-23.md` | Document gaps for Wexner research |
| `wexner_document_gaps_executive_summary.md` | Executive summary of Wexner gaps |
| `citation_gap_audit_2025-12-23.md` | Citation verification audit |
| `document_inventory_2025-12-23.md` | Full document inventory |
| `audit_operational_enabler_source_gaps.md` | Operational enabler analysis |
| `data_consolidation_analysis_2025-12-23.md` | Data merge analysis |

---

## Archived Materials

Archived context files are stored in `/continuum/-md_backups/` for reference:

### `/prompts/` — Completed Bug Fix Prompts (Dec 2024)
14 fix prompts for continuum.html bugs. All fixes completed and verified.
- `FIX_INDEX.md` — Master index of all fixes
- `FIX01` through `FIX14` — Individual fix prompts

### `/claude-desktop/` — Outdated Claude Desktop Context
Earlier version of CLAUDE.md using deprecated "DOSSIER" terminology.
- `CLAUDE.md` — Old project briefing (uses "dossier" not "analytical brief")
- `CLAUDE_PROJECT_KNOWLEDGE.md` — Old project knowledge file

### `/claude-to-claude-original/` — Expert Communication System (Dec 2025)
Historical Claude-to-Claude communication protocol used Dec 22-24, 2025.

**Key files preserved:**
- `MASTER_Claude_To_Claude.md` — Bridge protocol, accomplishments log, CC status
- `MASTER_ClaudeCode_Overseer_Start.md` — CC initialization protocol
- `Expert_to_Overseer.md` — Expert hierarchy communication

**Expert folders archived:**
- `Experts/Overseer/` — Overseer expert context
- `Experts/Connection Brief/` — Connection brief methodology
- `Experts/Infrastructure/` — Infrastructure expert tasks
- `Experts/Legal Framework/` — Legal compliance tasks
- `Experts/File Organization/Completed 12.22.25/` — Completed org tasks
- `Experts/Continuum Visualization/` — Visualization expert
- `Experts/Landing Page/` — Landing page expert
- `Experts/MISC/` — Miscellaneous chat

**Session files archived:**
- `CC1_Start.md`, `CC1_Work.md` — CC1 instance files
- `CC2_Start.md`, `CC2_Work.md` — CC2 instance files
- `CC3_Start.md`, `CC3_Work.md` — CC3 instance files
- `TASK_*.md` — Task assignments
- `URGENT_*.md` — Urgent directives

### `/misc/` — Miscellaneous Archived Files
- `test.md` — Test file (junk)
- `claude-smb-write-access-fix.md` — Completed SMB fix documentation

---

## Prince Andrew Deep Dive Reports

Located in `/continuum/documents/inbox/Epstein Docs/`:

| File | Description |
|------|-------------|
| `Prince_Andrew_Analysis_Abstract.md` | Executive summary of 70+ document mentions |
| `Prince_Andrew_Deep_Dive_Report.md` | Part 1 of comprehensive analysis |
| `Prince_Andrew_Deep_Dive_Report_COMPLETE.md` | Full consolidated report |
| `Prince_Andrew_Report_Part2.md` | Continued analysis (legal proceedings, investigation branches) |

---

## When to Use Archived Materials

**Use archived files when:**
- Researching how a past task was completed
- Understanding the Expert hierarchy system if it's reactivated
- Referencing completed bug fixes if similar issues arise
- Understanding historical project decisions

**Don't use archived files when:**
- Following current project standards (use CLAUDE.md)
- Looking for current data schemas (use connection_brief_reference.md)
- Checking citation standards (use source_link_audit.md)

---

## Directory Structure (Post-Organization)

```
/continuum/
├── CLAUDE.md                      # Main project context
├── CONTEXT_INDEX.md               # This file
├── connection_brief_reference.md  # Schema reference
├── source_link_audit.md           # Citation standards
├── config/
│   └── CLAUDE_CODE_CONTINUUM_TASK.md  # Dynamic system specs
├── reports/                       # Generated reports
├── -md_backups/                   # Archived .md files
│   ├── prompts/                   # Completed fix prompts
│   ├── claude-desktop/            # Old Claude Desktop context
│   ├── claude-to-claude-original/ # Expert system files
│   └── misc/                      # Miscellaneous
└── [protected directories not touched]
    ├── agents/
    ├── briefs/
    ├── data_archive/
    ├── database/
    ├── research/
    ├── sources/
    └── website/
```

---

*This index provides navigation to supplementary context. Primary context is always CLAUDE.md.*
