# THE CONTINUUM REPORT — Project Briefing

> "For there is nothing hidden that will not be disclosed, and nothing concealed that will not be known or brought out into the open." — Luke 8:17

**Last Updated:** 2026-01-05
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
| **[entities_index.md](entities_index.md)** | Master entity index — 2,008+ entities with source citations |
| **[agents/memos/index.md](agents/memos/index.md)** | Strategic memos — foundational directives for all sessions |

> **New Claude Sessions:** Start with this file, then check [log.md](log.md) for recent activity, [agents/memos/](agents/memos/) for strategic directives, and [index.md](index.md) for quick navigation.

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

**📄 For complete legal guidelines, see: [/config/legal_framework.md](/config/legal_framework.md)**

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

When foundational documents change (CLAUDE.md, REFERENCE.md), changes must cascade:
1. Check `/agents/memos/` for current strategic directives
2. All downstream agents and instructions inherit changes
3. No orphaned instructions — the bottom follows the top

**📄 For current strategic memos, see: [/agents/memos/index.md](/agents/memos/index.md)**

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
3. Run `python scripts/rebuild_entities_from_manifest.py`
4. Update `connections.json` if adding connections

**Build Scripts:**
- `rebuild_entities_from_manifest.py` — Rebuilds entities.json from manifest (USE THIS)
- `build_graph.py` — Auto-filters to manifest, won't overwrite curated manifest.json
- `build_connections_from_briefs.py` — Builds connections from connection briefs

**NEVER:**
- ❌ Add entities directly to entities.json without manifest entry
- ❌ Run build scripts that bypass manifest filtering
- ❌ Assume all briefs should become visible entities

---

## Current State

### Data Overview

| Category | Count | Status |
|----------|-------|--------|
| **Source Documents (Public)** | 121 PDFs | ✅ Cited sources at thecontinuumreport.com/sources |
| **Manifest Entities** | 40 | ✅ Curated for UI display |
| **Total Briefs** | 288+ | ✅ Research corpus (not all displayed) |
| **Master Entity Index** | 2,008+ | ✅ See entities_index.md |
| **Connections** | 70 | ✅ Between manifest entities only |
| **Paperless Docs** | ~372 | ✅ OCR processed, growing |

### Major Document Collections

- **House Oversight DOJ 33k:** Being uploaded to Paperless for OCR (not public until processed)
- **Giuffre v. Maxwell:** 96 court documents (public, cited in briefs)
- **Financial Enablers:** Court complaints and regulatory filings (public)
- **Florida Case:** NPA, indictment, OPR report (public)
- **Archived Collections:** FBI vault, congressional investigations, historical docs (in `/archive/`, not public)

**📄 For complete inventory, see: [/config/document_corpus.md](/config/document_corpus.md)**

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

**Timeline:** `/reports/epstein-financial-master-timeline.md`

---

## The Zoom Framework

Four-level hierarchical model for understanding how events connect across scales:

1. **Macro — Theological Framework:** The eternal context between truth and deception
2. **Systems — Power Structures:** Intelligence agencies, financial systems, recurring methods
3. **Events — Specific Cases:** Named individuals, timestamped communications, court filings (WHERE CLAIMS MUST BE SUBSTANTIATED)
4. **Ground — Breaking News:** Current developments connecting upward into patterns

**Interactive Implementation:** continuum.html (3-layer navigation: MACRO → ENTITIES → WEB)

---

## Directory Structure — MANDATORY REFERENCE

⚠️ **All Claude sessions MUST understand this structure before making changes.**

### Root Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | **This file** — Primary context for all Claude sessions |
| `index.md` | Quick navigation index to all resources |
| `log.md` | Chronological session log — UPDATE AFTER EVERY SESSION |
| `MASTER_TODO_LIST.md` | Single source of truth for all outstanding tasks |
| `BUGS.md` | Bug tracking with priority levels |
| `README.md` | Public GitHub readme |

### Directory Reference

| Directory | Purpose | Key Contents |
|-----------|---------|--------------|
| **`_archive/`** | 📦 **Consolidated archive for ALL old/backup content** | `briefs_backups/`, `indexes_backup/`, `published/`, `work_logs_dec2025/` — Move old files HERE, not scattered backups |
| **`agents/`** | 🤖 **Custom AI agent definitions** | `REFERENCE.md` (agent system overview), `tasks/` (active task specs), `themes/` (research themes), `memos/` (strategic directives) |
| **`audits/`** | 📋 **Completed audit reports** | Legal compliance audits, source citation audits — Historical record of verification work |
| **`briefs/`** | 📝 **Working analytical briefs (Markdown)** | `entity/` (708 entity briefs), `connections/` (connection briefs), `agencies/` (83 federal agency briefs) — SOURCE OF TRUTH for brief content |
| **`config/`** | ⚙️ **Configuration and reference documentation** | `legal_framework.md`, `document_corpus.md`, `technical_infrastructure.md`, `CLAUDE_PROJECT_KNOWLEDGE.md` |
| **`database/`** | 💾 **Database files** | Paperless database mount point |
| **`docker/`** | 🐳 **Docker configuration** | Container definitions, compose overrides |
| **`docs/`** | 📚 **Documentation organized by topic** | `docker/`, `github/`, `infrastructure/`, `session/`, `status/` — Reference docs moved from root |
| **`documents/`** | 📄 **Document staging area** | `inbox/` (PDFs awaiting Paperless processing ~494MB), `working/` (active processing), `public/` (reviewed for publication) |
| **`downloads/`** | ⬇️ **Downloaded source collections** | `doj-combined/` (3GB), `house-oversight/`, `fbi-vault/`, `executive-power/`, `legacy-root-files/` — Large file storage |
| **`indexes/`** | 🗂️ **Pipeline index files** | `entity_registry.json`, `co_occurrence.json`, `source_mentions.json`, `tag_map.json` — Machine-generated indexes |
| **`logs/`** | 📊 **Application logs** | Pipeline execution logs, error logs, progress tracking |
| **`pending_approval/`** | ⏳ **Briefs awaiting review** | Briefs created but not yet approved for publication — NEVER approve in same session that created them |
| **`reports/`** | 📈 **Generated analysis reports** | Gap analyses, acquisition lists, timelines, security scans, frontend assessments |
| **`research/`** | 🔬 **Active research materials** | `cia-history/`, `foia/` (FOIA templates), `prince-andrew/`, `meeting-notes/`, `outreach/` |
| **`scripts/`** | 🔧 **All Python and shell scripts** | Pipeline scripts, build scripts, upload helpers, utility scripts — ALL executable code goes here |
| **`sops/`** | 📋 **Standard Operating Procedures** | `SOP-002` through `SOP-005` — Mandatory procedures for document handling, brief generation, etc. |
| **`src/`** | 💻 **Python package source** | `continuum_report/` package with `lib/` — Importable Python modules |
| **`templates/`** | 📋 **Brief templates** | `analytical-brief.md`, `connection-brief.md` — Standard formats for new briefs |
| **`tests/`** | 🧪 **Test files** | pytest test suite for Python code |
| **`website/`** | 🌐 **LIVE WEBSITE FILES** | `continuum.html` (main UI), `briefs/` (HTML versions), `sources/` (121 cited PDFs), `data/` (entities.json, connections.json, manifest.json) |
| **`work/`** | 🔨 **Active working directory** | Scratch files, gap analyses, processing queues — Temporary work in progress |

### Critical Rules

1. **`_archive/`** — ALL archived content goes here. No scattered `backup/`, `old/`, or dated folders elsewhere.
2. **`scripts/`** — ALL executable scripts go here. Never leave `.py` or `.sh` files in other directories.
3. **`pending_approval/`** — Briefs MUST go here before publication. Never approve in the same session.
4. **`website/`** — This is LIVE. Changes here are PUBLIC immediately.
5. **`briefs/`** vs **`website/briefs/`** — Working markdown in `briefs/`, published HTML in `website/briefs/`.

### Workflow Paths

```
Document Acquisition:
  Download → documents/inbox/ → Paperless OCR → website/sources/ (if cited)

Brief Creation:
  Research → briefs/entity/ or briefs/connections/ → pending_approval/ → (new session) → website/briefs/

Archive:
  Old files → _archive/{descriptive_folder}/
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

**📄 For complete technical details, see: [/config/technical_infrastructure.md](/config/technical_infrastructure.md)**

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

**⚠️ ANY Claude session tasked with acquiring documents MUST read and follow:**

**📄 [/sops/SOP-005-document-acquisition-standard.md](/sops/SOP-005-document-acquisition-standard.md)**

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

**Architecture:** Single Claude Code session acts as Overseer; 14 specialized agents spawned via Task tool for parallel work.

### 14 Custom Agents

| Agent | Purpose |
|-------|---------|
| overseer | Meta-coordination |
| legal-auditor | First Amendment compliance |
| brief-generator | Full analytical briefs |
| connection-brief-generator | Relationship documentation |
| citation-mapper | ECF → PDF linking |
| entity-extractor | Extract entities from docs |
| financial-analyst | Money flow analysis |
| document-acquisition | Download sources |
| paperless-integrator | Paperless API integration |
| [+5 more] | See /agents/REFERENCE.md |

**Agent Definitions:** `/continuum/agents/`
**Active Tasks:** `/continuum/agents/tasks/`

---

## Session State (2025-12-25)

### Recently Completed

- ✅ Entity Index Manager (2,008+ entities extracted)
- ✅ Connection Brief Template Audit (70 briefs standardized)
- ✅ FBI Theme Complete (brief + 3 connections + timeline + FOIA templates)
- ✅ Legal Compliance Audit (116 files fixed, liability risk VERY LOW)
- ✅ Source Citation Audit (23 files, ~333 hyperlinks, 100% compliance)
- ✅ Sources Archive (thecontinuumreport.com/sources LIVE)

### Active Work

- [ ] Connection Brief Overseer Phase 2 (88 briefs queued)
- [ ] DOJ 33k OCR processing
- [ ] Cycle 2 document extraction

**📄 For complete session history, see: [/reports/session_history.md](/reports/session_history.md)**

---

## Reference Documents Quick Links

| Document | Purpose |
|----------|---------|
| [/config/legal_framework.md](/config/legal_framework.md) | Complete legal guidelines and templates |
| [/config/document_corpus.md](/config/document_corpus.md) | Full document inventory and acquisition list |
| [/config/technical_infrastructure.md](/config/technical_infrastructure.md) | Server, API, container configuration |
| [/config/file_structure.md](/config/file_structure.md) | Complete directory structure |
| [connection_brief_reference.md](connection_brief_reference.md) | Entity/connection JSON schemas |
| [/agents/REFERENCE.md](/agents/REFERENCE.md) | Agent system reference |
| [/templates/README.md](/templates/README.md) | Template usage guide |
| [/reports/session_history.md](/reports/session_history.md) | Historical session states |

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
   grep -rln "TASK_KEYWORDS" T:/*.md T:/config/*.md
   ```
2. **Update ALL matching files** - mark `[x]`, remove from pinned lists, add dates
3. **Update MASTER_TODO_LIST.md** (T:\ is canonical):
   - Mark item `[x]` with completion date
   - Move to COMPLETED ITEMS section
   - Update statistics
4. **Sync** T:\MASTER_TODO_LIST.md → local copy

### Files to Check
| File | Location | Priority |
|------|----------|----------|
| MASTER_TODO_LIST.md | T:\ | **Canonical** |
| MASTER_TODO_LIST.md | Local | Sync from T:\ |
| CLAUDE.md | T:\ and Local | Update if contains item |

**This prevents TODO drift between files.**
