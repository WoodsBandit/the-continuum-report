# THE CONTINUUM REPORT

> *"For there is nothing hidden that will not be disclosed..."* — Luke 8:17

---

## SESSION START PROTOCOL

**Every session reads these files in order:**

1. **This file** (CLAUDE.md) — Project overview and rules
2. **[STATE.md](STATE.md)** — Current state, what's in progress
3. **[TODO.md](TODO.md)** — Prioritized task list
4. **[SESSION_LOG.md](SESSION_LOG.md)** — Recent session history

**Before ending any session:**
- Update STATE.md with current progress
- Append to SESSION_LOG.md
- Update TODO.md if priorities changed

---

## INFRASTRUCTURE (WoodsDen Local)

**All infrastructure runs locally on WoodsDen. There is no server.**

| Resource | Location |
|----------|----------|
| **Project Root** | `C:\Users\Xx LilMan xX\Documents\Claude Docs\Continuum\` |
| **Website** | https://thecontinuumreport.com |
| **Local Dev** | http://localhost:8081 |
| **Paperless OCR** | http://localhost:8040 |
| **Data Storage** | Z:\ drive (1.9TB) |
| **GitHub** | WoodsBandit/the-continuum-report |

### Docker Services

```bash
cd docker
docker-compose -f docker-compose.woodsden.yml up -d
```

| Service | Port | Credentials |
|---------|------|-------------|
| Paperless | 8040 | admin / continuum2026 |
| Website | 8081 | — |

### Key Paths

| Purpose | Path |
|---------|------|
| Drop PDFs for OCR | Z:\paperless\consume\ |
| OCR'd documents | Z:\paperless\media\ |
| Source archives | Z:\continuum-sources\ |
| Backups | Z:\backups\ |

---

## THE MISSION

Independent intelligence analysis mapping connections between power structures, documented events, and the people involved. We build a comprehensive, well-sourced repository of analytical briefs based on primary source documents.

**Core Principles:**
- Document what the evidence shows
- Cite everything to primary sources
- Acknowledge what we don't know
- Invite verification

---

## LEGAL FRAMEWORK (CRITICAL)

All content operates under **Milkovich v. Lorain Journal (1990)** opinion protection.

### Required in Every Brief

1. Opinion-protection header
2. **The Public Record** — Quotes + citations only, NO interpretation
3. **Editorial Analysis** — Clearly labeled opinion
4. **Alternative Interpretations** — 5-7 minimum (STRONGEST LIABILITY SHIELD)
5. Right of Response invitation

### Never Do

- Assert as fact anything not directly quoted from sources
- Use loaded characterizations ("inner circle," "network")
- Treat Fifth Amendment as evidence of guilt
- Publish without Alternative Interpretations section

---

## DIRECTORY STRUCTURE

```
Continuum/
├── CLAUDE.md           # YOU ARE HERE - read first
├── STATE.md            # Current state - read second
├── TODO.md             # Prioritized tasks
├── SESSION_LOG.md      # Session history (append-only)
│
├── _active/            # Work in progress
├── _archive/           # Completed/historical
│
├── bnis/               # Breaking News Intelligence System
│   ├── run_bnis.py     # Main entry point
│   ├── config/         # News source configuration
│   ├── data/           # Pipeline data and output
│   └── scripts/        # Processing scripts
│
├── config/             # Project configuration
│   └── voice_guide.md  # Editorial voice guide
│
├── docker/             # Infrastructure
│   ├── docker-compose.woodsden.yml
│   └── nginx.conf
│
├── docs/               # Documentation
│   ├── config/         # Configuration reference
│   ├── sops/           # Standard Operating Procedures
│   └── infrastructure/ # Infrastructure docs
│
├── pending_approval/   # Briefs awaiting review
├── pipeline/           # Processing pipeline scripts
├── tests/              # Test suite
│
└── website/            # PUBLIC SITE
    ├── briefs/         # All briefs (entity/, connections/)
    ├── data/           # JSON data files
    └── sources/        # Cited PDFs
```

---

## BRIEF WORKFLOW

### Creating Briefs

1. Research in `_active/`
2. Draft brief using template
3. Save to `pending_approval/` (NEVER approve same session)
4. Different session reviews and approves
5. Move to `website/briefs/`

### Data Architecture

```
manifest.json = SOURCE OF TRUTH
↓
entities.json (generated from manifest)
↓
connections.json (between manifest entities only)
```

**To add entity:** Create brief → Add to manifest.json → Run rebuild script

---

## BNIS (Breaking News Intelligence System)

Automated pipeline: News fetch → Entity match → Claude Code narrative → Approval → Publish

| Component | Purpose |
|-----------|---------|
| Fetchers | GDELT, RSS, NewsAPI |
| Matcher | 2,008+ entities |
| Generator | Claude Code CLI |
| Approver | Different session |

---

## GIT WORKFLOW

```bash
git config user.email "thecontinuumreport@gmail.com"
git add [files]
git commit -m "Description

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push
```

---

## SESSION END CHECKLIST

Before ending session:

- [ ] Updated STATE.md with current progress
- [ ] Appended to SESSION_LOG.md
- [ ] Updated TODO.md if priorities changed
- [ ] Committed changes to git (if code modified)
- [ ] No work left in ambiguous state

---

*Another Node in the Decentralized Intelligence Agency*
