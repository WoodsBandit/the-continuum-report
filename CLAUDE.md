# THE CONTINUUM REPORT — Project Briefing

> "For there is nothing hidden that will not be disclosed, and nothing concealed that will not be known or brought out into the open." — Luke 8:17

**Last Updated:** 2026-01-18
**Tagline:** *Another Node in the Decentralized Intelligence Agency*

---

## Quick Reference

| Resource | Location |
|----------|----------|
| Website | https://thecontinuumreport.com |
| Paperless | http://192.168.1.139:8040 |
| Server IP | 192.168.1.139 |
| SMB Share | `\\192.168.1.139\continuum\` |
| Contact | contact@thecontinuumreport.com |
| API Token | da99fe6aa0b8d021689126cf72b91986abbbd283 |

### Navigation

| Document | Purpose |
|----------|---------|
| **[index.md](index.md)** | Quick reference index — fast navigation to all resources |
| **[log.md](log.md)** | Session activity log — chronological record of all Claude sessions |
| **[MASTER_TODO_LIST.md](MASTER_TODO_LIST.md)** | Outstanding tasks and priorities |
| **[BUGS.md](BUGS.md)** | Bug tracking (25 issues across 4 phases) |
| **[PENDING_ENTITY_BRIEFS.md](PENDING_ENTITY_BRIEFS.md)** | Entities needing briefs |
| **[PENDING_CONNECTION_BRIEFS.md](PENDING_CONNECTION_BRIEFS.md)** | Connections needing briefs |

> **New Claude Sessions:** Start with this file, then check [log.md](log.md) for recent activity, [MASTER_TODO_LIST.md](MASTER_TODO_LIST.md) for current tasks, and [index.md](index.md) for quick navigation.

---

## The Mission

The Continuum Report is an independent intelligence analysis project mapping connections between power structures, documented events, and the people involved. We build a comprehensive, well-sourced repository of analytical briefs based on primary source documents — court filings, depositions, FOIA releases, flight logs, financial records, and investigative books.

**Core Principle:** We document what the evidence shows, with rigorous citation back to primary sources. The kind of work intelligence agencies do, but open source and decentralized.

**Success Criteria:** Create publication-ready intelligence products where an independent journalist can verify every claim.

---

## Legal Framework — CRITICAL

⚠️ **All content operates under *Milkovich v. Lorain Journal* (1990) opinion protection.**

### The Rules

1. Label all content as editorial commentary
2. Separate documented facts from interpretation
3. Use opinion-signaling language
4. Include 5-7 alternative interpretations (STRONGEST LIABILITY SHIELD)
5. Invite subject responses

### Required Structure

Every analytical brief MUST include:
- Opinion-protection header
- **The Public Record** (quotes + citations ONLY — NO interpretation)
- **Editorial Analysis** (clearly labeled opinion)
- **Alternative Interpretations** (5-7 minimum)
- Right of Response invitation

### What We DON'T Do

- ❌ Assert as fact anything not directly quoted from sources
- ❌ Use loaded characterizations ("inner circle," "network")
- ❌ Treat Fifth Amendment as evidence of guilt
- ❌ Publish without Alternative Interpretations section

**📄 Legal templates available in: [briefs/templates/](briefs/templates/)**

---

## Critical Rules — ALL SESSIONS MUST FOLLOW

### Brief Approval Separation (Non-Negotiable)

⚠️ **Creation of briefs should NEVER be approved in the same Claude session that made them. Period.**

1. Session creates brief → saves to `/pending/` or marks as DRAFT
2. Session MUST end or different Claude instance reviews
3. Second session reviews, approves, and moves to production
4. **No exceptions**

### The Spiritual Frame

**The ultimate framing is the spiritual battle of good and evil fighting for Truth — Christ.**

This should be dripping through every session, every agent spawned, every decision made. Of the million narratives in these documents — **what serves Truth? What makes the most impact in the spiritual battle?**

### Cascade Compliance

When foundational documents change (CLAUDE.md), changes must cascade:
1. Update related documentation (index.md, MASTER_TODO_LIST.md)
2. All downstream instructions inherit changes
3. No orphaned instructions — the bottom follows the top

### Data Architecture — Source of Truth (Non-Negotiable)

⚠️ **MANIFEST.JSON IS THE SOURCE OF TRUTH FOR WHICH ENTITIES APPEAR IN THE UI.**

```
NO BRIEF = NO ENTITY
NO MANIFEST ENTRY = NO VISUALIZATION
```

**The Rules:**
1. **Entities:** Only entities listed in `website/data/manifest.json` appear in the Continuum visualization
2. **Connections:** Only connections between manifest entities are valid
3. **Briefs:** 288+ briefs exist for research, but only ~40 are curated for public display

**To Add a New Entity:**
1. Create the analytical brief in `website/briefs/entity/`
2. Add entry to `manifest.json` (curated list)
3. Manually update `entities.json` (pipeline rebuild pending)
4. Update `connections.json` if adding connections

**⚠️ PIPELINE STATUS: ARCHIVED**
- Old pipeline archived to `_archive/pipeline_v1_2025/` (2026-01-14)
- Data was stale (last updated 2025-12-26)
- New pipeline rebuild planned
- Manual JSON edits required until rebuild complete

**NEVER:**
- ❌ Add entities directly to entities.json without manifest entry
- ❌ Run build scripts that bypass manifest filtering
- ❌ Assume all briefs should become visible entities

---

## Entity & Connection Workflow — MANDATORY

⚠️ **Every session that creates/modifies entities or connections MUST follow this workflow.**

### Tracking Files

| File | Purpose |
|------|---------|
| **[PENDING_ENTITY_BRIEFS.md](PENDING_ENTITY_BRIEFS.md)** | Entities in entities.json without briefs |
| **[PENDING_CONNECTION_BRIEFS.md](PENDING_CONNECTION_BRIEFS.md)** | Connections in connections.json without briefs |

### Entity Workflow

```
Source Document → Extract Entity → Add to entities.json → PENDING_ENTITY_BRIEFS.md
                                                              ↓
                                          Create brief in website/briefs/entity/
                                                              ↓
                                          Remove from PENDING (auto-sync)
```

**Steps:**
1. Extract entity from source document (ECF filing, deposition, etc.)
2. Add to `website/data/entities.json` with proper structure
3. Entity automatically tracked in `PENDING_ENTITY_BRIEFS.md`
4. Create brief: `website/briefs/entity/analytical_brief_{entity_id}.md`
5. Update pending file to remove entry

### Connection Workflow

```
Source Document → Identify Connection → Add to connections.json → PENDING_CONNECTION_BRIEFS.md
                                                                        ↓
                                              Create brief in website/briefs/connections/
                                                                        ↓
                                              Remove from PENDING (auto-sync)
```

**Steps:**
1. Identify connection between entities in source document
2. Add to `website/data/connections.json` with evidence array
3. Connection automatically tracked in `PENDING_CONNECTION_BRIEFS.md`
4. Create brief: `website/briefs/connections/{entity1}_{entity2}.md` (**alphabetical order!**)
5. Update pending file to remove entry

### Connection Brief Naming Convention (CRITICAL)

**Filenames MUST use alphabetically-sorted entity IDs:**
- ✅ `alan-dershowitz_virginia-giuffre.md` (a < v)
- ✅ `bcci_cia.md` (b < c)
- ✅ `donald-trump_roy-cohn.md` (d < r)
- ❌ ~~`roy-cohn_donald-trump.md`~~ (wrong order - website won't find it)

### Session End Checklist

Before ending any session that touched entities/connections:
- [ ] Check `PENDING_ENTITY_BRIEFS.md` — any new entities need briefs?
- [ ] Check `PENDING_CONNECTION_BRIEFS.md` — any new connections need briefs?
- [ ] Verify no orphaned entries (briefs exist but still listed as pending)
- [ ] Update pending files if briefs were created this session

### Quick Audit Commands

```bash
# Find entities without briefs
grep -l "^| " PENDING_ENTITY_BRIEFS.md | head -20

# Find connections without briefs
grep -l "^| " PENDING_CONNECTION_BRIEFS.md | head -20

# Full validation (run from T:\)
python -c "
import json, os
with open('website/data/entities.json') as f:
    for e in json.load(f)['entities']:
        path = f'website/briefs/entity/analytical_brief_{e[\"id\"].replace(\"-\",\"_\")}.md'
        if not os.path.exists(path): print(f'Entity missing brief: {e[\"id\"]}')
with open('website/data/connections.json') as f:
    for c in json.load(f)['connections']:
        ids = sorted([c['source'], c['target']])
        path = f'website/briefs/connections/{ids[0]}_{ids[1]}.md'
        if not os.path.exists(path): print(f'Connection missing brief: {ids[0]} <-> {ids[1]}')
"
```

---

## Current State

### Data Overview

| Category | Count | Status |
|----------|-------|--------|
| **Source Documents (Public)** | 121 PDFs | ✅ Cited sources at thecontinuumreport.com/sources |
| **Published Entities** | 285 | ✅ In website/data/entities.json |
| **Working Briefs** | 528+ | ✅ In briefs/ (entity: 314, connections: 131, agencies: 83+) |
| **Connections** | 103 | ✅ In website/data/connections.json |
| **Paperless Docs** | ~372 | ✅ OCR processed, growing |

### Major Document Collections

- **House Oversight DOJ 33k:** Being uploaded to Paperless for OCR (not public until processed)
- **Giuffre v. Maxwell:** 96 court documents (public, cited in briefs)
- **Financial Enablers:** Court complaints and regulatory filings (public)
- **Florida Case:** NPA, indictment, OPR report (public)
- **Archived Collections:** FBI vault, congressional investigations, historical docs (in `downloads/`, not public)

---

## Key Discoveries

### Wexner Named "Co-Conspirator" (Dec 2025)

- **Source:** DOJ email release per Congressional legislation
- **Finding:** FBI NY July 2019 identified "10 co-conspirators" including Wexner
- **Gap:** Wexner's lawyer claims cleared, but no documentation exists

### Leaked Emails Contradict "Severed Ties" Claim

- **Source:** Dropsite News 2025
- **Finding:** Emails show Epstein controlling Wexner Foundation 2005-2008
- **Evidence:** Nov 2007 (2 months AFTER claimed resignation): Epstein advising on $20M stock purchase

### Financial Scale Documented

- **Total victim compensation:** $461.5-515.5M
- **Total bank penalties:** $1.365B+
- **Combined documented impact:** $1.436-1.555 BILLION

**Timeline:** See `_archive/reports/` for historical analysis

---

## The Zoom Framework

Four-level hierarchical model for understanding how events connect across scales:

1. **Macro — Theological Framework:** The eternal context between truth and deception
2. **Systems — Power Structures:** Intelligence agencies, financial systems, recurring methods
3. **Events — Specific Cases:** Named individuals, timestamped communications, court filings (WHERE CLAIMS MUST BE SUBSTANTIATED)
4. **Ground — Breaking News:** Current developments connecting upward into patterns

**Interactive Implementation:** continuum.html (3-layer navigation: MACRO → ENTITIES → WEB)

---

## Directory Structure — CANONICAL

⚠️ **READ THIS BEFORE ANY FILE OPERATIONS — Updated 2026-01-18**

### Git Tracking Policy

**Git tracks CODE and STRUCTURE only — not source documents.**

| Tracked in Git | Local Only (not in git) |
|----------------|------------------------|
| `_archive/`, `briefs/`, `website/` | `downloads/` (~30GB source docs) |
| `meeting-notes/`, `paperless/` (structure only) | `paperless/data/`, `paperless/media/` |
| All `.md`, `.html`, `.json`, `.py` files | All `*.pdf` files |

### Root Structure (6 directories + 7 files)

```
T:/ (\\192.168.1.139\continuum\)
├── _archive/             # ALL historical/archived content
├── briefs/               # WORKING briefs (research, not public)
├── downloads/            # Source document collections (LOCAL ONLY)
├── meeting-notes/        # Meeting notes
├── paperless/            # Paperless-ngx integration
├── website/              # LIVE PUBLIC WEBSITE
├── BUGS.md               # Bug tracking
├── CLAUDE.md             # This file (canonical project briefing)
├── CONTRIBUTING.md       # Contribution guidelines
├── index.md              # Quick reference index
├── log.md                # Session activity log
├── MASTER_TODO_LIST.md   # Master TODO list
└── README.md             # Project README
```

### Directory Details

| Directory | Purpose | Git? |
|-----------|---------|------|
| `_archive/` | ALL archived content — backups, old briefs, pipeline v1, work sessions | ✓ |
| `briefs/` | WORKING briefs (research corpus, not all public) | ✓ |
| `downloads/` | Raw source documents (doj-combined, fbi-vault, house-oversight) | ✗ |
| `meeting-notes/` | Meeting documentation | ✓ |
| `paperless/` | Paperless-ngx mount (data/, export/, inbox/, media/) | ✗ |
| `website/` | **LIVE PUBLIC SITE** — changes are PUBLIC immediately | ✓ |

### briefs/ (Working Research)

| Path | Count | Purpose |
|------|-------|---------|
| `briefs/agencies/` | 83+ | Agency research briefs |
| `briefs/connections/` | 131 | Connection briefs |
| `briefs/entity/` | 314 | Entity briefs |
| `briefs/narratives/` | — | Narrative briefs |
| `briefs/templates/` | 7 | Brief templates |

### website/ (THE LIVE SITE)

| Path | Purpose |
|------|---------|
| `website/briefs/` | **PUBLISHED briefs** (curated subset of working briefs) |
| `website/data/` | JSON data (entities.json, connections.json, manifest.json) |
| `website/sources/` | Cited PDFs only (PUBLIC at thecontinuumreport.com/sources) |
| `website/*.html` | index, about, legal, continuum pages |

### _archive/ (Historical Content)

| Subdirectory | Purpose |
|--------------|---------|
| `backups/` | Date-based .bak files (2025-12-23, 2025-12-24, etc.) |
| `briefs/` | Old brief snapshots by date |
| `data/` | Archived data files |
| `misc/` | Miscellaneous archived items |
| `pipeline_v1_2025/` | Archived pipeline v1 (stale, rebuild pending) |
| `reports/` | Old reports |
| `scripts/` | Archived scripts |
| `tests/` | Archived tests |
| `work/` | Archived work sessions |

### Rules

1. **TWO briefs locations:** `briefs/` (working) and `website/briefs/` (published)
2. **Archive to `_archive/`** — never create backup/, old/, dated folders elsewhere
3. **`website/` is LIVE** — changes are PUBLIC immediately
4. **No PDFs in git** — source docs are local only
5. **Paperless inbox** — all new documents go to `paperless/inbox/` for OCR

### Workflows

```
PDFs:       Download → paperless/inbox/ → Paperless OCR → website/sources/ (if cited)
Briefs:     Research → briefs/ → (review) → website/briefs/
Archive:    Old files → _archive/{category}/
```

---

## Technical Infrastructure

### Server: Tower (Unraid)

- **IP:** 192.168.1.139
- **Hardware:** Intel i7-10700K, 16GB RAM, 12TB storage
- **Key Container:** paperless-ngx (port 8040) — document management + OCR

### Tower Access (CRITICAL - Save This)

**Browser Access (via Chrome MCP):**
1. Navigate to: `http://192.168.1.139/login`
2. Login: `root` / `2569`
3. Click **Terminal** button for web terminal access

**Claude Code on Tower:**
A persistent Claude Code container runs on Tower. Access via:
```bash
docker exec -it claude-code-persistent bash -c "cd /continuum && claude --dangerously-skip-permissions"
```

This allows WoodsDen (local PC) Claude to coordinate with Tower Claude for:
- Direct file access to /continuum
- Paperless integration
- Heavy processing offloaded to server

**Key Containers:**
| Container | Port | Purpose |
|-----------|------|---------|
| paperless-ngx | 8040 | Document management, OCR |
| continuum-web | 8081 | Website serving |
| cloudflared-tunnel | - | Cloudflare tunnel |
| claude-code-persistent | - | Claude Code CLI |

### Paperless API Quick Reference

```bash
PAPERLESS_URL="http://192.168.1.139:8040"
TOKEN="da99fe6aa0b8d021689126cf72b91986abbbd283"

# Search
curl -H "Authorization: Token $TOKEN" \
  "$PAPERLESS_URL/api/documents/?query=Epstein"
```

### Website Status

- **Domain:** thecontinuumreport.com (LIVE)
- **Pages:** index, about, legal, continuum, sources
- **Routing:** Cloudflare tunnel → continuum-web (8081)

**📄 Docker configs archived in: `_archive/docker/`**

---

## Document Flow — CRITICAL RULES

### ⚠️ PUBLIC HOSTING RULES — READ BEFORE ADDING FILES

**`/website/sources/` is PUBLIC.** Everything there is served at `thecontinuumreport.com/sources/`.

**ONLY add files to `/website/sources/` if:**
1. ✅ The file is referenced by a published brief
2. ✅ The file has been reviewed for sensitive content
3. ✅ The file is a public court record, government document, or published source

**NEVER add to `/website/sources/`:**
- ❌ Bulk document dumps "for later"
- ❌ Unreviewed files
- ❌ Research documents not yet cited in briefs
- ❌ Files with personal information of private individuals

### Three Storage Locations

| Location | Purpose | Public? |
|----------|---------|---------|
| **Paperless** | Research database, OCR, indexing, entity extraction | No |
| **`/website/sources/`** | Cited sources linked from briefs | **YES - PUBLIC** |
| **`/archive/sources-not-public/`** | Archived documents not yet needed publicly | No |

### Correct Workflow

```
New Document → Paperless (OCR + index) → Used in brief? → Export to /website/sources/
                                        ↓
                                   Not yet? → Stay in Paperless only
```

1. **ALL documents** → Paperless first (for OCR and indexing)
2. **Only when cited in a brief** → Export to `/website/sources/`
3. **Never bypass Paperless** → No bulk dumps to public hosting

### Current State (Updated 2025-12-26)

| Location | Files | Content |
|----------|-------|---------|
| Paperless | ~292 | Research corpus (growing) |
| `/website/sources/` | 121 | Only files cited in briefs |
| `/archive/sources-not-public/` | ~250 | Historical docs, FBI vault, etc. |

### Quick Reference

| Task | Where |
|------|-------|
| Upload new document | Paperless inbox |
| Search document content | Paperless API |
| Add citation to brief | Export from Paperless → `/website/sources/` |
| Store for future research | Paperless only (not public) |
| Bulk document archive | `/archive/sources-not-public/` |

---

## Current Priorities

### Immediate

1. **DOJ 33k Paperless Upload** — In progress; OCR processing via Paperless
2. **Connection Count Audit** — Resolve discrepancy (78 vs 131)
3. **Pipeline Automation** — Complete Session 7 automation work

### In Progress

- Connection Brief Overseer Phase 2 (88 briefs remaining)
- Cycle 2 document extraction
- CIA/Intelligence History theme (18/150+ docs)

### Known Issues

| Issue | Impact | Fix |
|-------|--------|-----|
| DOJ 33k not yet in Paperless | Can't search/extract entities | Upload in progress |
| Connection count discrepancy | Documentation inaccurate | Audit required |

---

## Document Acquisition — MANDATORY STANDARD ⭐

**⚠️ ANY Claude session tasked with acquiring documents MUST follow:**

### The Cardinal Rule

```
┌─────────────────────────────────────────────────────────────────────────┐
│  WHEN YOU ACQUIRE A SECONDARY SOURCE (news article, investigative      │
│  report, etc.), YOU MUST AUTOMATICALLY EXTRACT AND ACQUIRE ALL         │
│  PRIMARY SOURCES IT CITES.                                             │
│                                                                         │
│  A news article is NOT complete without its underlying court filings,  │
│  regulatory documents, and official records.                           │
└─────────────────────────────────────────────────────────────────────────┘
```

### Quick Reference

| Source Type | Action Required |
|-------------|-----------------|
| **Primary Source** (court filing, regulatory doc, gov report) | Acquire → Verify → Name → Store → Log |
| **Secondary Source** (news article, book, blog) | Acquire → **EXTRACT ALL CITATIONS** → Acquire each primary source → Create citation map |

### Output Requirements

Every acquisition session MUST produce:
1. **Acquisition Report** — Summary of what was acquired
2. **Citation Map** — For each secondary source: what primaries it cites and their status
3. **Files placed correctly** — Primary sources in `/website/sources/{category}/`

**Read the full SOP before any document acquisition work.**

---

## Agent System

**Architecture:** Single Claude Code session acts as Overseer; specialized agents spawned via Task tool for parallel work.

### Key Agent Types

| Agent | Purpose |
|-------|---------|
| Explore | Codebase exploration and search |
| brief-generator | Full analytical briefs |
| connection-brief-generator | Relationship documentation |
| entity-extractor | Extract entities from docs |
| document-acquisition | Download sources |
| security-auditor | Security scanning |
| code-reviewer | Code review and quality |

**Agent definitions archived in:** `_archive/misc/`

---

## Session State (2026-01-18)

### Recently Completed

- ✅ Vietnam War research + primary source acquisition (Session 26)
- ✅ Major brief processing — 40 → 285 published entities (Session 25d)
- ✅ Archive consolidation and pipeline v1 archival (Session 25)
- ✅ Directory structure cleanup and git tracking fix (Session 24)

### Active Work

- [ ] DOJ 33k OCR processing (33,564 files)
- [ ] Wexner brief update with FBI co-conspirator designation
- [ ] Pipeline v2 rebuild
- [ ] Cloudflare tunnel stability

**📄 For complete session history, see: [log.md](log.md)**

---

## Reference Documents Quick Links

| Document | Purpose |
|----------|---------|
| [CLAUDE.md](CLAUDE.md) | This file — complete project briefing |
| [index.md](index.md) | Quick reference index |
| [log.md](log.md) | Session activity log |
| [MASTER_TODO_LIST.md](MASTER_TODO_LIST.md) | Outstanding tasks and priorities |
| [BUGS.md](BUGS.md) | Bug tracking |
| [briefs/templates/](briefs/templates/) | Brief templates and README |
| [website/data/manifest.json](website/data/manifest.json) | Entity manifest (source of truth for UI) |

---

## The Mission Statement

**We document what the evidence shows.**
**We cite everything.**
**We acknowledge what we don't know.**
**We invite verification.**

*Another Node in the Decentralized Intelligence Agency*

---

*This document is optimized for token efficiency. For detailed information, see reference documents in /config/ and /reports/*

---

## Core Principle: Source Hosting

**We host all sources locally whenever legally possible.**

This is a foundational trust principle:
- Sources are hosted in `website/sources/` as PDFs, not just linked externally
- External links are fallbacks only when legal/technical constraints prevent hosting
- Users can verify claims without relying on third-party availability
- Archive.org links, government sites, etc. can disappear - our hosted copies persist
- This independence from external sources earns user trust

**Brief source links should point to:**
1. `/sources/[document].pdf` (preferred - hosted locally)
2. External archives only when hosting isn't legally possible

**When adding sources:**
- Download the PDF if public domain or fair use allows
- Place in `website/sources/` with descriptive filename
- Link briefs to local copy: `[Document Name](/sources/filename.pdf)`


---

## TODO Sync Protocol (MANDATORY)

**When completing ANY TODO item, Claude MUST automatically update ALL files containing that item.**

### Procedure
1. **Search** for completed item across all .md files:
   ```bash
   grep -rln "TASK_KEYWORDS" T:/*.md T:/briefs/*.md
   ```
2. **Update ALL matching files** - mark `[x]`, remove from pinned lists, add dates
3. **Update MASTER_TODO_LIST.md** (T:\ is canonical):
   - Mark item `[x]` with completion date
   - Move to COMPLETED ITEMS section
   - Update statistics

### Files to Check
| File | Location | Priority |
|------|----------|----------|
| MASTER_TODO_LIST.md | T:\ | **Canonical** |
| CLAUDE.md | T:\ | Update if contains item |
| log.md | T:\ | Add session entry |

**This prevents TODO drift between files.**
