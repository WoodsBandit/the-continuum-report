# THE CONTINUUM REPORT — Quick Reference Index

> Fast navigation to all project resources. For full documentation, see [CLAUDE.md](CLAUDE.md).

**Last Updated:** 2026-01-05 (Session 18)
**Related:** [log.md](log.md) | [CLAUDE.md](CLAUDE.md) | [BUGS.md](BUGS.md)

---

## Directory Structure

```
T:\continuum\
├── CLAUDE.md              ← Full project briefing (START HERE)
├── index.md               ← This file (quick reference)
├── log.md                 ← Session activity log
├── entities_index.md      ← Master entity index (2,008+ entities)
├── ENTITIES_README.md     ← Entity index usage guide
│
├── agents/                ← Custom agent definitions
│   ├── tasks/             ← Task-specific agents
│   ├── themes/            ← Theme-based research agents
│   └── epstein-extraction/← Extraction pipeline & findings
│
├── briefs/                ← Analytical briefs (local copies)
│   ├── entity/            ← 38 entity profiles
│   └── agencies/          ← 73+ federal agency research briefs (NEW)
│
├── website/               ← Web-hosted content
│   ├── sources/           ← 33,745 source PDFs
│   ├── briefs/            ← Published briefs
│   │   ├── entity/        ← 37 entity briefs
│   │   └── connections/   ← 86 connection briefs
│   └── data/              ← JSON data files
│
├── downloads/             ← Raw document downloads
├── reports/               ← Generated reports
├── research/              ← Research notes & outreach
├── templates/             ← Document templates
├── config/                ← Configuration files
└── logs/                  ← System logs
```

---

## Key Files

### Project Documentation
| File | Purpose |
|------|---------|
| [CLAUDE.md](CLAUDE.md) | Complete project briefing — read first |
| [log.md](log.md) | Chronological session activity log |
| [index.md](index.md) | This quick reference index |
| [BUGS.md](BUGS.md) | Master bug tracking (25 issues, 4 phases) |
| [SESSION_START_PROMPT.md](SESSION_START_PROMPT.md) | Session initialization instructions |
| [CONTEXT_INDEX.md](CONTEXT_INDEX.md) | Context loading guide |

### GitHub Repository
| Resource | URL |
|----------|-----|
| **Repository** | https://github.com/WoodsBandit/the-continuum-report |
| **Clone URL** | `git clone https://github.com/WoodsBandit/the-continuum-report.git` |

### Bug Fix Agent Tasks
| Phase | File | Priority | Issues |
|-------|------|----------|--------|
| 1 | [BUGFIX_PHASE1_INFRASTRUCTURE.md](agents/tasks/BUGFIX_PHASE1_INFRASTRUCTURE.md) | P0 Critical | 3 |
| 2 | [BUGFIX_PHASE2_NAVIGATION.md](agents/tasks/BUGFIX_PHASE2_NAVIGATION.md) | P1 High | 8 |
| 3 | [BUGFIX_PHASE3_DATA.md](agents/tasks/BUGFIX_PHASE3_DATA.md) | P2 Medium | 8 |
| 4 | [BUGFIX_PHASE4_POLISH.md](agents/tasks/BUGFIX_PHASE4_POLISH.md) | P3 Low | 6 |

### Entity Reference
| File | Purpose |
|------|---------|
| [entities_index.md](entities_index.md) | Master entity index (2,008+ entities with citations) |
| [ENTITIES_README.md](ENTITIES_README.md) | How to use the entity index |
| [website/data/entities-master.json](website/data/entities-master.json) | JSON version for programmatic access |
| [connection_brief_reference.md](connection_brief_reference.md) | Connection documentation reference |

### Source Documents
| Location | Contents |
|----------|----------|
| `website/sources/house-oversight-2025/` | 33,572 DOJ Congressional release PDFs |
| `website/sources/giuffre-v-maxwell/` | 97 unsealed court documents |
| `website/sources/financial-enablers/` | 27 banking/financial documents |
| `website/sources/maxwell-criminal/` | 8 criminal case documents |
| `website/sources/fbi-vault/` | 8 FBI FOIA release parts |

---

## Current Statistics

### Documents
- **Total Source PDFs:** 33,745
- **Extracted & Indexed:** 100 (Phase 1)
- **Requiring OCR:** ~33,580 (DOJ 33k + FBI Vault)

### Entities
- **Unique Entities Extracted:** 2,008 - 2,428
- **Entity Briefs Created:** 38
- **Connection Briefs Created:** 86

### Top Entities by Mention Count
| Entity | Mentions |
|--------|----------|
| Ghislaine Maxwell | 76-85 |
| Jeffrey Epstein | 62-66 |
| Virginia Giuffre | 58-66 |
| Sarah Kellen | 36 |
| Alan Dershowitz | 31-33 |
| Prince Andrew | 29-31 |

---

## Quick Commands

### Start a Session
```
Read T:\continuum\CLAUDE.md
```

### Find an Entity
```
Search T:\continuum\entities_index.md for "[NAME]"
```

### Check Session History
```
Read T:\continuum\log.md
```

### Access Source Documents
```
List T:\continuum\website\sources\[category]\
```

---

## Active Research Themes

| Theme | Status | Agent Location |
|-------|--------|----------------|
| FBI | COMPLETE | `agents/themes/FBI_THEME_RESEARCH_AGENT.md` |
| Entity Indexing | COMPLETE | `agents/tasks/ENTITY_INDEX_MANAGER.md` |
| DOJ | PLANNED | — |
| Financial Enablers | PLANNED | — |
| Intelligence Community | PLANNED | — |

## Infrastructure Modernization (Session 4 - COMPLETE)

| Component | Status | Details |
|-----------|--------|---------|
| Security Hardening | COMPLETE | All Python scripts use env vars |
| Shared Library | COMPLETE | scripts/lib/ with config, logging, API clients |
| Test Infrastructure | COMPLETE | 116 tests passing, 83% coverage |
| Docker Setup | COMPLETE | Multi-stage builds, compose files verified |
| CI/CD Pipelines | COMPLETE | 6 workflows fixed and verified |
| Frontend Analysis | COMPLETE | FRONTEND_MODERNIZATION_PLAN.md created |

## Frontend Modernization (Session 5 - IN PROGRESS)

| Component | Status | Details |
|-----------|--------|---------|
| SRI Hashes | COMPLETE | D3.js, Marked.js, PDF.js secured |
| Copyright Years | COMPLETE | All HTML files updated to 2025 |
| CSS Tokens | COMPLETE | `website/styles/tokens.css` created |
| JS Modularization | 3/7 DONE | data-loader, brief-viewer, pdf-viewer extracted |
| CSS Extraction | PENDING | Link shared tokens.css to HTML files |

### Session 5 Key Deliverables

| File | Purpose |
|------|---------|
| `website/styles/tokens.css` | Shared CSS design tokens |
| `website/scripts/data-loader.js` | Data fetching utility |
| `website/scripts/brief-viewer.js` | Brief rendering module |
| `website/scripts/pdf-viewer.js` | PDF.js integration |
| `website/scripts/README.md` | Module architecture docs |
| `website/continuum.html` | SRI hashes added |
| `website/about.html` | Copyright year fixed |
| `website/legal.html` | Copyright year fixed |

### Security Status

**API Token Rotated** - New token configured in `.env` files (2025-12-26)

## Autonomous Pipeline (Session 6 - IN PROGRESS)

| Component | Status | Details |
|-----------|--------|---------|
| Pipeline Scripts | COMPLETE | 8 scripts (~130KB) in scripts/ |
| Docker Config | COMPLETE | continuum-python with Docker socket |
| Webhook Endpoint | RUNNING | Port 5000 on Tower |
| File Watchers | RUNNING | entity_registry, connection_contexts, approved/ |
| Paperless Hook | PENDING | Post-consume script needed |

### Session 6 Key Deliverables

| File | Purpose |
|------|---------|
| `scripts/invoke_claude.py` | Claude CLI wrapper via docker exec |
| `scripts/webhook_listener.py` | Flask webhook for Paperless |
| `scripts/run_stage1.py` | Entity extraction |
| `scripts/run_stage2.py` | Context extraction |
| `scripts/run_stage3.py` | Brief generation |
| `scripts/run_stage4.py` | Publication |
| `scripts/pipeline_watcher.py` | File system watchers |
| `scripts/pipeline_daemon.py` | Master orchestrator |
| `scripts/PIPELINE_DEPLOYMENT.md` | Deployment guide |

### Pipeline Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `http://192.168.1.139:5000/health` | GET | Health check |
| `http://192.168.1.139:5000/api/continuum/ingest` | POST | Trigger Stage 1 |
| `http://192.168.1.139:5000/api/continuum/status` | GET | Queue status |

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
