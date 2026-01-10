# THE CONTINUUM REPORT — Session Continuity Guide
**Purpose:** Ensure consistent context across Claude Code sessions
**Created:** 2026-01-04

---

## FOR NEW CLAUDE SESSIONS

### Step 1: Read Core Context (3 minutes)
```
1. Read this file (SESSION_CONTINUITY_GUIDE.md)
2. Read MASTER_PROJECT_STATUS.md (comprehensive status)
3. Check T:\log.md for recent activity
```

### Step 2: Understand the Project (30 seconds)
- **What:** Open source intelligence project mapping power structures
- **How:** Primary source documents → entity extraction → analytical briefs
- **Legal:** All content under Milkovich v. Lorain Journal opinion protection
- **Spiritual:** Truth vs. deception - this is the frame

### Step 3: Check Current Work
```
1. Review MASTER_TODO_LIST.md for outstanding tasks
2. Check T:\agents\tasks\ for active agent work
3. Look at PROJECT_CONSOLIDATION_2026-01-04.md if reorganizing
```

---

## KEY FILE LOCATIONS

| What You Need | Where It Is |
|---------------|-------------|
| **Main Project Context** | T:\CLAUDE.md (network - canonical) |
| **Comprehensive Status** | T:\MASTER_PROJECT_STATUS.md |
| **Task List** | T:\MASTER_TODO_LIST.md |
| **Session Log** | T:\log.md |
| **Entity Briefs** | T:\website\briefs\entity\ |
| **Source Documents** | T:\website\sources\ |
| **Prompts/Templates** | Local\Prompts\ |
| **Website HTML** | T:\website\ |

**Local Path:** `C:\Users\Xx LilMan xX\Documents\Claude Docs\The Continuum Report\`
**Network Path:** `T:\` or `\\192.168.1.139\continuum\`

---

## TOWER SERVER ACCESS (CRITICAL)

**Tower** is the Unraid server at 192.168.1.139 running all Continuum infrastructure.

### Browser Access (via Chrome MCP)
1. Navigate to: `http://192.168.1.139/login`
2. Login: `root` / `2569`
3. Click **Terminal** button for web terminal access

### Claude Code on Tower
A persistent Claude Code container runs on Tower:
```bash
docker exec -it claude-code-persistent bash -c "cd /continuum && claude --dangerously-skip-permissions"
```

Use this to coordinate WoodsDen (local PC) Claude with Tower Claude for:
- Direct file access to /continuum
- Paperless integration
- Heavy processing offloaded to server

---

## CRITICAL RULES

### 1. Brief Approval Separation
**NEVER approve a brief in the same session that created it.**
- Session 1 creates → saves to pending
- Session 2 reviews → approves → moves to production

### 2. Legal Framework
Every analytical brief MUST have:
- Opinion-protection header
- The Public Record (quotes + citations ONLY)
- Editorial Analysis (clearly labeled)
- Alternative Interpretations (5-7 minimum)
- Right of Response

### 3. Source Hosting
- `/website/sources/` is PUBLIC
- Only add files that are cited in published briefs
- All new docs go to Paperless first for OCR

### 4. SMB Write Access
Claude has FULL access to T:\ (fixed 2026-01-04).
- Can read from T:\ ✓
- Can write to T:\ ✓
- T:\ is mapped to `\\192.168.1.139\continuum\`

---

## CURRENT PRIORITIES (Jan 2026)

### Critical
1. Update Wexner brief with FBI co-conspirator info
2. ~~Fix SMB write access~~ DONE (2026-01-04)
3. OCR DOJ 33k files
4. Download remaining Epstein Estate files

### High
1. Maxwell Proffer manual download
2. Website stability (Cloudflare tunnel)
3. Website fixes (FIX01-FIX14)

### In Progress
1. Entity synthesis
2. Connection briefs Phase 2
3. CIA/Intelligence History theme

---

## KNOWN BLOCKERS

| Task | Blocker | Solution |
|------|---------|----------|
| Maxwell Proffer | DOJ auth | Manual browser download from justice.gov |
| Church Committee Book V | Too large | Split PDF or chunk processing |
| Epstein Estate | Rate limit | Use Dropbox backup or wait |

---

## AGENT SYSTEM

14 specialized agents available via Task tool:
- overseer, legal-auditor, brief-generator
- connection-brief-generator, citation-mapper
- entity-extractor, financial-analyst
- document-acquisition, paperless-integrator
- [see T:\agents\REFERENCE.md for full list]

**Spawn agents for parallel work** - don't do everything sequentially.

---

## THE ZOOM FRAMEWORK

Understanding the hierarchy:
1. **Macro (Theological)** - Truth vs. deception
2. **Systems (Power)** - Intelligence, finance, methods
3. **Events (Cases)** - Named people, court filings
4. **Ground (News)** - Current developments

Content flows from Events (substantiated) up to Systems (patterns) within Macro (frame).

---

## PAPERLESS API

```bash
URL="http://192.168.1.139:8040"
TOKEN="da99fe6aa0b8d021689126cf72b91986abbbd283"

# Search documents
curl -H "Authorization: Token $TOKEN" "$URL/api/documents/?query=Epstein"
```

---

## IF CONTEXT BREAKS

1. Re-read MASTER_PROJECT_STATUS.md
2. Check PROJECT_CONSOLIDATION_2026-01-04.md for audit notes
3. Review T:\log.md for what was happening
4. Ask user for clarification if needed

---

## QUICK COMMANDS

```bash
# List T:\ root
ls -la T:/

# Find recent markdown files
find "T:/" -name "*.md" -mtime -7

# Check website status
curl -I https://thecontinuumreport.com
```

---

*Another Node in the Decentralized Intelligence Agency*
