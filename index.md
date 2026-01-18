# THE CONTINUUM REPORT — Quick Reference Index

> Fast navigation to all project resources. For full documentation, see [CLAUDE.md](CLAUDE.md).

**Last Updated:** 2026-01-18 (Session 27)
**Related:** [log.md](log.md) | [CLAUDE.md](CLAUDE.md) | [BUGS.md](BUGS.md)

---

## Directory Structure

```
T:/ (\\192.168.1.139\continuum\)
├── CLAUDE.md              ← Full project briefing (START HERE)
├── index.md               ← This file (quick reference)
├── log.md                 ← Session activity log
├── MASTER_TODO_LIST.md    ← Outstanding tasks and priorities
├── BUGS.md                ← Bug tracking (25 issues)
├── CONTRIBUTING.md        ← Contribution guidelines
├── README.md              ← Project README
│
├── _archive/              ← ALL historical/archived content
│   ├── backups/           ← Date-based .bak files
│   ├── briefs/            ← Old brief snapshots
│   ├── data/              ← Archived data files
│   ├── misc/              ← Miscellaneous archived items
│   ├── pipeline_v1_2025/  ← Archived pipeline v1
│   ├── reports/           ← Old reports
│   └── work/              ← Archived work sessions
│
├── briefs/                ← WORKING briefs (research, not public)
│   ├── agencies/          ← 83+ agency research briefs
│   ├── connections/       ← 131 connection briefs
│   ├── entity/            ← 314 entity briefs
│   ├── narratives/        ← Narrative briefs
│   └── templates/         ← Brief templates
│
├── downloads/             ← Source document collections (LOCAL ONLY)
│   ├── doj-combined/      ← DOJ DataSets 1-8
│   ├── fbi-vault/         ← FBI FOIA releases
│   ├── house-oversight/   ← DOJ 33k Congressional release
│   └── misc/              ← Other sources
│
├── meeting-notes/         ← Meeting documentation
│
├── paperless/             ← Paperless-ngx integration
│   ├── data/              ← Paperless database (don't touch)
│   ├── export/            ← Exported documents
│   ├── inbox/             ← Documents awaiting OCR
│   └── media/             ← Paperless media files
│
└── website/               ← LIVE PUBLIC WEBSITE
    ├── briefs/            ← PUBLISHED briefs (curated subset)
    │   ├── agencies/
    │   ├── connections/
    │   └── entity/
    ├── data/              ← JSON data files
    │   ├── entities.json
    │   ├── connections.json
    │   └── manifest.json
    ├── sources/           ← Cited PDFs (PUBLIC)
    ├── about.html
    ├── continuum.html
    ├── index.html
    └── legal.html
```

---

## Key Files

### Project Documentation
| File | Purpose |
|------|---------|
| [CLAUDE.md](CLAUDE.md) | Complete project briefing — read first |
| [log.md](log.md) | Chronological session activity log |
| [index.md](index.md) | This quick reference index |
| [MASTER_TODO_LIST.md](MASTER_TODO_LIST.md) | Outstanding tasks and priorities |
| [BUGS.md](BUGS.md) | Master bug tracking (25 issues, 4 phases) |

### GitHub Repository
| Resource | URL |
|----------|-----|
| **Repository** | https://github.com/WoodsBandit/the-continuum-report |
| **Clone URL** | `git clone https://github.com/WoodsBandit/the-continuum-report.git` |

### Working Briefs
| Location | Count | Purpose |
|----------|-------|---------|
| `briefs/entity/` | 314 | Entity research briefs |
| `briefs/connections/` | 131 | Connection briefs |
| `briefs/agencies/` | 83+ | Federal agency research |
| `briefs/templates/` | 7 | Brief templates |

### Published Data (website/)
| File | Purpose |
|------|---------|
| `website/data/entities.json` | Published entities (285) |
| `website/data/connections.json` | Published connections (103) |
| `website/data/manifest.json` | Entity manifest (source of truth for UI) |

### Source Documents (website/sources/)
| Location | Contents |
|----------|----------|
| `giuffre-v-maxwell/` | 96 unsealed court documents |
| `financial-enablers/` | Banking/financial documents |
| `florida-case/` | NPA, indictment, OPR report |
| `congressional/` | Congressional reports |
| `intelligence/` | Intelligence documents |
| `regulatory-actions/` | Regulatory filings |

---

## Current Statistics

### Data Counts
| Category | Count |
|----------|-------|
| **Published Entities** | 285 |
| **Published Connections** | 103 |
| **Working Entity Briefs** | 314 |
| **Working Connection Briefs** | 131 |
| **Agency Research Briefs** | 83+ |
| **Public Source PDFs** | 121 |
| **Paperless Docs** | ~372 |

### Pending Processing
- **DOJ 33k PDFs:** 33,564 files requiring OCR
- **Paperless Inbox:** Documents awaiting processing

---

## Quick Commands

### Start a Session
```
Read T:\CLAUDE.md
```

### Check Session History
```
Read T:\log.md
```

### Check TODO List
```
Read T:\MASTER_TODO_LIST.md
```

### Access Source Documents
```
List T:\website\sources\[category]\
```

---

## Recent Sessions

| Session | Date | Summary |
|---------|------|---------|
| 27 | 2026-01-18 | Directory structure documentation |
| 26 | 2026-01-17 | Vietnam War research + primary source acquisition |
| 25d | 2026-01-15 | Major brief processing — 40 → 285 entities |
| 25 | 2026-01-14 | Archive consolidation, pipeline v1 archival |
| 24 | 2026-01-11 | Directory cleanup, git tracking fix |

**Full history:** [log.md](log.md)

---

## Current Priorities

| Priority | Task | Status |
|----------|------|--------|
| **CRITICAL** | DOJ 33k OCR processing | 33,564 files pending |
| **CRITICAL** | Wexner brief FBI co-conspirator update | Pending |
| **HIGH** | Pipeline v2 rebuild | Planned |
| **HIGH** | Cloudflare tunnel stability | Known issue |

**Full TODO list:** [MASTER_TODO_LIST.md](MASTER_TODO_LIST.md)

---

## Contact & Resources

| Resource | Location |
|----------|----------|
| Website | https://thecontinuumreport.com |
| Paperless-ngx | http://192.168.1.139:8040 |
| SMB Share | `\\192.168.1.139\continuum\` |
| Contact | contact@thecontinuumreport.com |

---

*For detailed information on any topic, consult [CLAUDE.md](CLAUDE.md).*
