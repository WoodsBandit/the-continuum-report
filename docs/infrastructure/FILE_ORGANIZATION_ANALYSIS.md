# THE CONTINUUM REPORT — File Organization Analysis & Recommendations

**Analysis Date:** 2025-12-24
**Project Status:** Active development with 33,745 source documents, 38 entity briefs, 86 connection briefs
**Analyst:** Claude Sonnet 4.5 (Documentation Architect)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current Structure Analysis](#current-structure-analysis)
3. [Naming Convention Audit](#naming-convention-audit)
4. [Directory Hierarchy Evaluation](#directory-hierarchy-evaluation)
5. [Configuration Management Assessment](#configuration-management-assessment)
6. [Problem Areas Identified](#problem-areas-identified)
7. [Proposed Reorganization](#proposed-reorganization)
8. [Migration Strategy](#migration-strategy)
9. [Maintenance Recommendations](#maintenance-recommendations)

---

## Executive Summary

### Project Overview

The Continuum Report is an intelligence analysis project mapping power structures through primary source documentation. The project has evolved organically from initial research into a complex multi-component system with:

- **33,745 source PDFs** (court documents, FOIA releases, financial records)
- **2,008+ extracted entities** with citation tracking
- **38 entity briefs** and **86 connection briefs**
- **13 Python automation scripts**
- **Multiple agent-based extraction systems**
- **Static website generation** pipeline

### Current State Assessment

**Overall Rating:** 6/10 — Functional but showing signs of organic growth without systematic architecture

**Strengths:**
- Clear separation of source documents from generated content
- Comprehensive documentation in root-level markdown files
- Template-based standardization for briefs
- Agent-based modular approach to research tasks

**Critical Issues:**
- **95 backup files** (.bak) scattered across briefs directories
- **10+ backup directories** with inconsistent naming (Backups/ backups/ backup/ briefs_backup_20251223_075731/)
- **Root directory pollution:** 17 markdown files in project root
- **Configuration scattered** across multiple locations
- **Duplicate content** between /briefs/ and /website/briefs/
- **Orphaned directories:** briefs_backup_20251223_075731, data_archive_20251223, -md_backups

### Key Recommendations

1. **Implement proper version control** (Git) to eliminate .bak files
2. **Consolidate documentation** into /docs/ directory
3. **Centralize configuration** into single /config/ hierarchy
4. **Establish clear build artifacts** vs source separation
5. **Create systematic backup strategy** outside project directory

---

## Current Structure Analysis

### Root Directory Organization

**Current Layout:**
```
/t/
├── CLAUDE.md                           ← Main project briefing (44 KB, 1,367 lines)
├── index.md                            ← Quick reference index
├── log.md                              ← Session activity log
├── entities_index.md                   ← Master entity index (322 KB!)
├── ENTITIES_README.md                  ← Entity index usage guide
├── CONTEXT_INDEX.md                    ← Context loading guide
├── SESSION_START_PROMPT.md             ← Session initialization
├── connection_brief_reference.md       ← Connection documentation
├── source_link_audit.md                ← Audit report
├── CONTINUUM_REPORT_INFRASTRUCTURE_ASSESSMENT.md
├── EXECUTIVE_SUMMARY.md
├── IMPLEMENTATION_ROADMAP.md
├── QUICK_START_GUIDE.md
├── README.md
├── setup-claude-config.sh              ← Setup scripts (3)
├── setup-claude-full.sh
├── setup-claude-plugins.sh
└── NDH6SA~M                            ← Orphaned temp file
```

**Analysis:**

**Positive Aspects:**
- Core navigation files (CLAUDE.md, index.md, log.md) are immediately accessible
- Naming is descriptive and consistent (ALL_CAPS for major docs, lowercase for operational)
- Session-oriented documentation supports AI agent continuity

**Issues:**
1. **Too many root-level files** (17 markdown + 3 shell scripts = 20 files)
2. **No clear categorization** — documentation, guides, infrastructure docs, and operational logs all mixed
3. **Orphaned temp file** (NDH6SA~M) suggests incomplete cleanup
4. **Large data file in root** (entities_index.md at 322 KB should be in /data/)

**Impact:** New contributors or AI agents face cognitive overload determining which file to read first.

---

### Scripts Directory Structure

**Current State:**
```
/t/scripts/
├── brief_watcher.py                    ← Real-time brief monitoring
├── build_epstein_dossier.py            ← Legacy dossier builder (deprecated?)
├── build_graph.py                      ← Graph visualization
├── continuum_pipeline.py               ← Main AI pipeline (v3.1)
├── entity_discovery.py                 ← Entity extraction
├── export_sources.py                   ← Source export utility
├── fix_sources.py                      ← Source data repair
├── generate_connection_briefs.py       ← Connection brief generator
├── generate_dossiers.py                ← Multi-entity dossier generator
├── generate_epstein_dossier.py         ← Specific entity dossier
├── inject_ecf_links.py                 ← Court document link injection
├── parse_brief.py                      ← Brief parser utility
├── redaction_extractor.py              ← Redaction analysis
├── check-woodsden-mount.sh             ← Server mount check
└── mount-woodsden.sh                   ← Server mounting

Total: 13 Python scripts (~4,970 lines), 2 shell scripts
```

**Analysis:**

**Positive Aspects:**
- Descriptive naming with clear verbs (generate_, build_, parse_, fix_)
- Separation of concerns (extraction vs generation vs utilities)
- Shell scripts properly separated from Python automation

**Issues:**
1. **No subdirectory organization** — all scripts flat in one directory
2. **Legacy scripts retained** (build_epstein_dossier.py vs generate_epstein_dossier.py)
3. **No requirements.txt** or dependency documentation in /scripts/
4. **Python cache pollution** (__pycache__/ directories)

**Functional Categories Identified:**
- **Generation:** continuum_pipeline.py, generate_*.py, build_*.py (6 scripts)
- **Extraction:** entity_discovery.py, redaction_extractor.py, parse_brief.py (3 scripts)
- **Utilities:** fix_sources.py, export_sources.py, inject_ecf_links.py (3 scripts)
- **Monitoring:** brief_watcher.py (1 script)
- **Infrastructure:** *.sh scripts (2 scripts)

---

### Briefs Organization

**Current State:**
```
/t/briefs/
├── backup/                             ← Empty backup directory
├── connections/
│   ├── alan-dershowitz_connections.md  ← Aggregated connection index
│   ├── alan-dershowitz_epstein-florida-case.md
│   ├── alan-dershowitz_ghislaine-maxwell.md
│   ├── [... 86 total connection briefs]
│   ├── *.bak                           ← 73 backup files!!!
│   ├── manifest.json
│   └── CONNECTION_BRIEF_INDEX.md
└── entity/
    ├── analytical_brief_alan_dershowitz.md
    ├── analytical_brief_jeffrey_epstein.md
    ├── [... 38 total entity briefs]
    ├── *.bak                           ← 22 backup files!!!
    └── .tmp                            ← Empty temp file

Parallel structure:
/t/website/briefs/                      ← Duplicate hierarchy (122 files)
├── connections/
│   └── manifest.json
└── entity/
```

**Analysis:**

**Positive Aspects:**
- Clear semantic separation (entity/ vs connections/)
- Consistent naming: `analytical_brief_[entity].md` for entities
- Logical naming for connections: `[entity-a]_[entity-b].md`
- Manifest files for programmatic access

**Critical Issues:**
1. **95 .bak files** (73 + 22) across briefs directories — version control anti-pattern
2. **Duplicate content** between /briefs/ and /website/briefs/ (122 files)
3. **Inconsistent entity naming:**
   - `analytical_brief_alan_dershowitz.md` (entity brief)
   - `alan-dershowitz_connections.md` (connection index)
   - `alan-dershowitz_jeffrey-epstein.md` (pairwise connection)
4. **Mixed formats:** Entity names use underscores in filenames, hyphens in connection briefs
5. **Empty/orphaned files:** backup/, .tmp

**Naming Convention Analysis:**

| File Type | Convention | Example | Issues |
|-----------|------------|---------|--------|
| Entity Brief | `analytical_brief_[slug].md` | `analytical_brief_alan_dershowitz.md` | Verbose prefix |
| Connection Index | `[slug]_connections.md` | `alan-dershowitz_connections.md` | Hyphenated |
| Pairwise Connection | `[slug-a]_[slug-b].md` | `alan-dershowitz_jeffrey-epstein.md` | Hyphenated |

**Observations:**
- Entity briefs use underscores in slugs: `alan_dershowitz`
- Connection briefs use hyphens in slugs: `alan-dershowitz`
- No consistent slug standard across project

---

### Website Structure

**Current State:**
```
/t/website/
├── index.html                          ← Landing page (58 KB)
├── about.html                          ← About page (34 KB)
├── continuum.html                      ← Visualization page (236 KB)
├── legal.html                          ← Legal framework (24 KB)
├── og-image.jpg                        ← Open Graph image
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
├── briefs/                             ← Published briefs (122 files)
│   ├── entity/
│   └── connections/
│       └── manifest.json
├── sources/                            ← 33,745 source PDFs
│   ├── giuffre-v-maxwell/              ← 97 documents
│   ├── maxwell-criminal/               ← 8 documents
│   ├── house-oversight-2025/           ← 33,572 documents
│   ├── financial-enablers/             ← 27 documents
│   ├── fbi-vault/                      ← 8 documents
│   ├── [... additional categories]
├── data/                               ← JSON data exports
│   ├── entities.json
│   ├── entities-master.json            ← 516 KB
│   ├── connections.json
│   ├── hierarchy.json
│   ├── manifest.json
│   ├── fbi-personnel.json
│   └── fbi-theme-connections.json
├── theology/                           ← Theological commentary
├── backups/                            ← 15 backup HTML files
└── Backups/                            ← 15 backup HTML files (duplicate!)
```

**Analysis:**

**Positive Aspects:**
- Clean public-facing structure (HTML files in root)
- Logical organization of assets, sources, data
- JSON data files enable dynamic frontend features
- Sources organized by document category

**Critical Issues:**
1. **Duplicate backup directories** (`backups/` and `Backups/`) — 30 identical files
2. **Case sensitivity problem** on Windows — these would merge on Unix systems
3. **Briefs duplication** with /t/briefs/ — unclear which is source of truth
4. **Large HTML files** (continuum.html at 236 KB) — should be generated from data
5. **No clear build pipeline** — static HTML appears hand-edited

**Directory Depth:** Appropriate (max 3 levels for sources)

---

### Documentation Distribution

**Current Locations:**

```
Root-level documentation (17 files):
- CLAUDE.md, index.md, log.md          ← Core navigation
- ENTITIES_README.md, entities_index.md ← Entity system
- SESSION_START_PROMPT.md, CONTEXT_INDEX.md ← Session management
- connection_brief_reference.md        ← Template reference
- source_link_audit.md                 ← Audit reports
- CONTINUUM_REPORT_INFRASTRUCTURE_ASSESSMENT.md
- EXECUTIVE_SUMMARY.md
- IMPLEMENTATION_ROADMAP.md
- QUICK_START_GUIDE.md
- README.md

Agent documentation:
/t/agents/tasks/ENTITY_INDEX_MANAGER.md
/t/agents/themes/FBI_THEME_RESEARCH_AGENT.md
[... additional agent specs]

Template documentation:
/t/templates/README.md
/t/templates/*.md (4 templates)

Historical documentation:
/t/-md_backups/claude-to-claude-full/Experts/[...]
/t/-md_backups/claude-desktop/

Reports:
/t/reports/*.md (20+ report files)

Audits:
/t/audits/legal-compliance-2025-12-24/
/t/audits/source-citation-audit-2025-12-24/
```

**Analysis:**

**Issues:**
1. **No centralized documentation directory** — docs scattered across 6+ locations
2. **Unclear documentation lifecycle** — when does a report become archival?
3. **Redundant guides** (QUICK_START_GUIDE.md + SESSION_START_PROMPT.md + index.md)
4. **Historical clutter** (-md_backups/ contains 50+ obsolete documents)

**Impact:** Difficulty maintaining documentation consistency; new agents may read outdated information.

---

## Naming Convention Audit

### File Naming Patterns

**Entity Brief Naming:**
```
Format: analytical_brief_[entity_slug].md
Examples:
  analytical_brief_alan_dershowitz.md
  analytical_brief_jeffrey_epstein.md
  analytical_brief_cia.md
  analytical_brief_iran_contra.md

Slug convention: lowercase with underscores
Special cases: multi-word entities use underscores (alan_dershowitz, jean_luc_brunel)
```

**Assessment:** ✅ Consistent within category
**Issue:** Verbose `analytical_brief_` prefix adds 18 characters to every filename

---

**Connection Brief Naming:**

```
Format (Pairwise): [entity-a-slug]_[entity-b-slug].md
Examples:
  alan-dershowitz_jeffrey-epstein.md
  bill-clinton_ghislaine-maxwell.md
  deutsche-bank_jeffrey-epstein.md

Format (Index): [entity-slug]_connections.md
Examples:
  alan-dershowitz_connections.md
  bill-clinton_connections.md
  virginia-giuffre_connections.md

Slug convention: lowercase with hyphens (NOT underscores!)
Ordering: Alphabetical by last name (dershowitz before epstein)
```

**Assessment:** ⚠️ Inconsistent with entity brief slugs
**Issue:** Entity briefs use underscores (`alan_dershowitz`), connections use hyphens (`alan-dershowitz`)

---

**Script Naming:**
```
Python scripts: verb_noun.py pattern
Examples:
  generate_connection_briefs.py
  build_graph.py
  parse_brief.py
  fix_sources.py

Shell scripts: verb-noun.sh pattern (hyphenated)
Examples:
  mount-woodsden.sh
  check-woodsden-mount.sh
  setup-claude-config.sh
```

**Assessment:** ✅ Consistent verb-first imperative naming
**Issue:** Inconsistent delimiter (underscores in Python, hyphens in shell)

---

**Data File Naming:**
```
JSON files: noun-description.json (hyphenated)
Examples:
  entities-master.json
  fbi-theme-connections.json
  fbi-personnel.json

Manifests: manifest.json (generic, context from directory)
```

**Assessment:** ✅ Consistent hyphenated convention
**Issue:** Generic `manifest.json` requires directory context for meaning

---

**Backup File Naming:**

**Current Chaos:**
```
Individual file backups:
  analytical_brief_alan_dershowitz.md.bak
  alan-dershowitz_jeffrey-epstein.md.bak
  [95 total .bak files]

Directory backups:
  briefs_backup_20251223_075731/
  data_archive_20251223/

Website backups:
  backups/about.html
  backups/continuum - backup.html
  Backups/about.html           ← Duplicate with different case!
  Backups/index - Copy.html
```

**Assessment:** ❌ No systematic naming, case conflicts, redundancy
**Issue:**
- .bak files should not exist with proper version control
- Timestamp format inconsistent (YYYYMMDD_HHMMSS vs YYYYMMDD)
- Case-sensitivity issues (backups/ vs Backups/)
- Descriptive suffixes mixed with timestamps ("continuum - backup.html")

---

### Slug Standardization Analysis

**Entity Slug Variants Found:**

| Entity | Entity Brief Slug | Connection Brief Slug | Inconsistent? |
|--------|-------------------|-----------------------|---------------|
| Alan Dershowitz | `alan_dershowitz` | `alan-dershowitz` | ✅ YES |
| Jeffrey Epstein | `jeffrey_epstein` | `jeffrey-epstein` | ✅ YES |
| Ghislaine Maxwell | `ghislaine_maxwell` | `ghislaine-maxwell` | ✅ YES |
| Bill Clinton | `bill_clinton` | `bill-clinton` | ✅ YES |
| CIA | `cia` | `cia` | ❌ No |
| BCCI | `bcci` | `bcci` | ❌ No |
| Iran-Contra | `iran_contra` | `iran-contra` | ✅ YES |

**Recommendation:** Standardize on **hyphenated slugs** (more web-friendly, URL-compatible)

---

### Directory Naming Patterns

**Consistency Check:**

| Directory | Convention | Consistent? |
|-----------|------------|-------------|
| `/briefs/entity/` | lowercase, no delimiter | ✅ |
| `/briefs/connections/` | lowercase, no delimiter | ✅ |
| `/website/sources/` | lowercase, no delimiter | ✅ |
| `/agents/tasks/` | lowercase, no delimiter | ✅ |
| `/-md_backups/` | prefix hyphen, underscore delimiter | ⚠️ |
| `/briefs_backup_20251223_075731/` | underscore delimiter, timestamp | ⚠️ |
| `/data_archive_20251223/` | underscore delimiter, timestamp | ⚠️ |
| `/woodsden-docs/` | hyphen delimiter | ⚠️ |

**Issue:** Mix of hyphens, underscores, and no delimiters with no clear pattern

---

## Directory Hierarchy Evaluation

### Depth Analysis

**Maximum Depth:** 6 levels (reasonable)

```
Example deepest path:
/t/agents/epstein-extraction/findings/court-filings/[document-id]/[file].md
│  │      │                  │        │             │            └─ File
│  │      │                  │        │             └─ Document ID
│  │      │                  │        └─ Category
│  │      │                  └─ Output type
│  │      └─ Agent name
│  └─ Agent type
└─ Project root

Depth: 6 levels
```

**Assessment:** ✅ Acceptable — not overly nested

---

### Separation of Concerns

**Source Documents vs Generated Output:**

```
Source documents (read-only primary sources):
✅ /t/website/sources/[category]/[document].pdf
✅ /t/documents/inbox/Epstein Docs/

Generated output (AI-created content):
✅ /t/briefs/entity/
✅ /t/briefs/connections/
✅ /t/reports/
✅ /t/agents/[agent]/findings/

Configuration (human-edited):
⚠️ /t/config/ — exists but underutilized
⚠️ /t/.claude/settings.json
⚠️ Setup scripts in root directory

Working directories (temporary/intermediate):
⚠️ /t/work/ — purpose unclear
⚠️ /t/cache/ — 7 JSON files
⚠️ /t/downloads/ — raw downloads vs /documents/inbox/?
```

**Assessment:** ✅ Good separation of sources vs output
**Issue:** Configuration scattered, unclear working directory purpose

---

### Orphaned and Misplaced Files

**Orphaned Directories:**

```
❌ /t/briefs_backup_20251223_075731/
   - Timestamped backup should be in dedicated /backups/ or archived externally
   - 95 backup files consuming space

❌ /t/data_archive_20251223/
   - Should be archived outside active project directory
   - Contains obsolete JSON: connections.json, connection_briefs.json, entities.json

❌ /t/-md_backups/
   - Leading hyphen is non-standard
   - Contains 50+ obsolete markdown files from previous agent iterations
   - Should be git history, not filesystem clutter

❌ /t/website/backups/ and /t/website/Backups/
   - Duplicate directories differing only in case
   - 30 redundant HTML backup files
   - Will conflict on case-sensitive filesystems

❌ /t/briefs/backup/
   - Empty directory serving no purpose
```

---

**Misplaced Files:**

```
❌ /t/entities_index.md (322 KB)
   - Data file in project root
   - Should be: /t/data/entities_index.md or /t/docs/reference/entities_index.md

❌ /t/setup-claude-*.sh (3 scripts)
   - Installation/setup scripts in root
   - Should be: /t/scripts/setup/ or /t/bin/

❌ /t/NDH6SA~M
   - Orphaned temporary file (Windows short name format)
   - Should be deleted

⚠️ /t/website/data/entities-master.json (516 KB)
   - Duplicate of data in entities_index.md
   - Intentional for website consumption, but relationship unclear
```

---

**Unclear Purpose Directories:**

```
? /t/work/connections/
  - Contains what? Working drafts? Temporary files?
  - No README explaining purpose

? /t/downloads/
  - vs /t/documents/inbox/ — overlapping purposes?
  - Should have clear delineation

? /t/database/paperless/
  - Empty directory
  - Paperless-ngx runs locally via Docker (http://localhost:8040)
  - Data stored in data/paperless/ directory
  - Why does this directory exist?

? /t/cache/timeline_events/
  - Only 7 JSON files numbered: 5, 6, 24, 68, 174, 177, 193
  - Sparse cache suggests incomplete feature or abandoned implementation
```

---

## Configuration Management Assessment

### Configuration File Locations

**Current Distribution:**

```
1. Claude-specific config:
   /t/.claude/settings.json

2. Project knowledge base:
   /t/config/CLAUDE_PROJECT_KNOWLEDGE.md
   /t/config/CLAUDE_CODE_CONTINUUM_TASK.md
   /t/config/ollama/ (subdirectory for Ollama configs)

3. Setup scripts:
   /t/setup-claude-config.sh
   /t/setup-claude-full.sh
   /t/setup-claude-plugins.sh

4. Agent configurations (embedded in agent specs):
   /t/agents/tasks/ENTITY_INDEX_MANAGER.md
   /t/agents/themes/FBI_THEME_RESEARCH_AGENT.md

5. Template configurations:
   /t/templates/README.md (contains quality checklist, naming conventions)

6. Data manifests (pseudo-configuration):
   /t/website/data/manifest.json
   /t/briefs/connections/manifest.json
   /t/website/briefs/connections/manifest.json
```

**Assessment:**

**Issues:**
1. **No central configuration registry** — configs scattered across 6 locations
2. **Setup scripts in root** instead of /scripts/setup/ or /bin/
3. **Configuration embedded in documentation** (templates/README.md)
4. **Duplicate manifests** (briefs/connections/ vs website/briefs/connections/)
5. **No .env file** or environment variable management (API keys hardcoded in CLAUDE.md!)

---

### Environment Variable Handling

**Current State:**

```
From CLAUDE.md:
| API Token | da99fe6aa0b8d021689126cf72b91986abbbd283 |
```

**CRITICAL SECURITY ISSUE:**
❌ API token hardcoded in documentation file
❌ No .env or secrets management
❌ Token visible in all backups, git history (if versioned)

**Recommendation:**
Immediately rotate this token and implement proper secrets management.

---

### Secrets Placement

**Current Exposure:**

```
Files containing sensitive information:
❌ /t/CLAUDE.md — Paperless-ngx API token
❌ /t/CLAUDE.md — Local service URLs (localhost ports)

Backup exposure:
❌ /-md_backups/claude-desktop/CLAUDE.md
❌ /-md_backups/claude-to-claude-full/[multiple files]

If this project is in git:
❌ All historical commits contain these secrets
```

**Required Actions:**
1. Create `/t/.env` with secrets
2. Add `.env` to `.gitignore`
3. Update CLAUDE.md to reference environment variables
4. Rotate exposed API token
5. Document secrets setup in `/t/config/SECRETS.md.example`

---

## Problem Areas Identified

### Critical (Fix Immediately)

1. **Security: Exposed API Credentials**
   - **File:** /t/CLAUDE.md
   - **Issue:** Paperless-ngx API token hardcoded in documentation
   - **Impact:** Unauthorized access to document management system
   - **Fix:** Rotate token, implement .env, update references

2. **Data Integrity: Duplicate Backup Directories**
   - **Locations:** /t/website/backups/ and /t/website/Backups/
   - **Issue:** Case-insensitive Windows filesystem creates duplicates; will conflict on Unix
   - **Impact:** Wasted storage, deployment failures on Linux servers
   - **Fix:** Consolidate to single /t/backups/ at root level

3. **Version Control: 95 .bak Files**
   - **Locations:** /t/briefs/entity/ (22), /t/briefs/connections/ (73)
   - **Issue:** Manual backup anti-pattern; no systematic versioning
   - **Impact:** Confusion about canonical versions, storage waste
   - **Fix:** Initialize git repository, delete all .bak files

---

### High Priority (Fix This Sprint)

4. **Clarity: Slug Inconsistency**
   - **Issue:** Entity briefs use underscores, connection briefs use hyphens
   - **Examples:** `alan_dershowitz` vs `alan-dershowitz`
   - **Impact:** Programmatic cross-referencing failures, developer confusion
   - **Fix:** Standardize on hyphenated slugs, rename files

5. **Organization: Root Directory Pollution**
   - **Issue:** 17 markdown files + 3 shell scripts in project root
   - **Impact:** Cognitive overload for new contributors
   - **Fix:** Consolidate into /docs/, /scripts/setup/, /data/

6. **Maintenance: Orphaned Archive Directories**
   - **Locations:** /t/briefs_backup_20251223_075731/, /t/data_archive_20251223/, /t/-md_backups/
   - **Issue:** 150+ obsolete files consuming space
   - **Impact:** Confusion about which data is current
   - **Fix:** Archive to external storage, remove from project

---

### Medium Priority (Next Sprint)

7. **Build Pipeline: Static HTML vs Generated**
   - **Issue:** No clear distinction between hand-edited HTML and generated output
   - **Impact:** Risk of overwriting manual edits during regeneration
   - **Fix:** Create /website/src/ for templates, /website/public/ for output

8. **Documentation: Scattered Locations**
   - **Locations:** Root (17 files), /reports/, /audits/, /-md_backups/, /agents/
   - **Issue:** No single source of truth for documentation
   - **Impact:** Outdated information may mislead agents
   - **Fix:** Consolidate into /docs/ with clear hierarchy

9. **Clarity: Unclear Working Directories**
   - **Directories:** /t/work/, /t/downloads/, /t/cache/
   - **Issue:** No README explaining purpose or lifecycle
   - **Impact:** Uncertain whether contents are safe to delete
   - **Fix:** Add README to each, or eliminate if unused

---

### Low Priority (Backlog)

10. **Scripts: Flat Directory**
    - **Issue:** All 13 Python scripts in single /scripts/ directory
    - **Impact:** Harder to navigate as project scales
    - **Fix:** Organize into /scripts/generation/, /scripts/extraction/, /scripts/utils/

11. **Data: Duplicate Entity Data**
    - **Files:** /t/entities_index.md (322 KB) vs /t/website/data/entities-master.json (516 KB)
    - **Issue:** Same data in two formats with no clear build relationship
    - **Impact:** Risk of desynchronization
    - **Fix:** Document which is source of truth, establish build pipeline

12. **Templates: Configuration in README**
    - **File:** /t/templates/README.md
    - **Issue:** Quality checklist, naming conventions buried in template docs
    - **Impact:** Not discoverable as project-wide standards
    - **Fix:** Extract to /docs/standards/ or /config/quality-standards.md

---

## Proposed Reorganization

### Design Principles

1. **Separation of Concerns**
   - Source documents (read-only)
   - Configuration (human-edited)
   - Generated output (machine-created)
   - Documentation (explanatory)
   - Build artifacts (publishable)

2. **Clear Hierarchy**
   - Max 4 levels deep for common paths
   - Descriptive directory names
   - Consistent naming conventions

3. **Version Control Readiness**
   - No backup files (.bak)
   - .gitignore for generated content
   - Secrets in .env (not tracked)

4. **Discoverability**
   - README.md in each major directory
   - Index files for large collections
   - Consistent slug format

---

### Proposed Directory Structure

```
/t/
├── .env                                # Environment variables (NOT in git)
├── .gitignore                          # Git exclusions
├── README.md                           # Project overview (brief)
├── CHANGELOG.md                        # Version history
│
├── bin/                                # Executable scripts
│   ├── setup-environment.sh            # Environment setup
│   ├── setup-claude.sh                 # Claude configuration
│   └── mount-server.sh                 # Server mounting
│
├── config/                             # Configuration files
│   ├── README.md                       # Configuration guide
│   ├── SECRETS.md.example              # Secrets template (for onboarding)
│   ├── claude/                         # Claude-specific config
│   │   ├── project-knowledge.md
│   │   └── settings.json
│   ├── ollama/                         # Ollama LLM config
│   │   └── modelfile
│   ├── agents/                         # Agent configurations
│   │   ├── entity-index-manager.yaml
│   │   └── fbi-theme-researcher.yaml
│   ├── templates/                      # Document templates
│   │   ├── analytical-brief.md
│   │   ├── connection-brief.md
│   │   ├── opinion-narrative-short.md
│   │   └── opinion-narrative-long.md
│   └── quality-standards.md            # Editorial standards checklist
│
├── docs/                               # Project documentation
│   ├── README.md                       # Documentation index
│   ├── getting-started.md              # Quickstart guide
│   ├── architecture.md                 # System architecture
│   ├── session-guide.md                # Claude session workflow
│   ├── api/                            # API documentation
│   │   └── briefs-api.md
│   ├── reference/                      # Reference materials
│   │   ├── entities-index.md           # Master entity index
│   │   ├── entities-guide.md           # How to use entity index
│   │   ├── connection-guide.md         # Connection documentation
│   │   └── legal-framework.md          # Legal compliance guide
│   ├── guides/                         # How-to guides
│   │   ├── creating-briefs.md
│   │   ├── running-extractions.md
│   │   └── deploying-website.md
│   └── standards/                      # Project standards
│       ├── naming-conventions.md
│       ├── citation-requirements.md
│       └── quality-checklist.md
│
├── src/                                # Source code
│   ├── README.md                       # Code documentation
│   ├── extraction/                     # Entity/data extraction
│   │   ├── __init__.py
│   │   ├── entity_discovery.py
│   │   ├── redaction_extractor.py
│   │   └── parse_brief.py
│   ├── generation/                     # Content generation
│   │   ├── __init__.py
│   │   ├── continuum_pipeline.py
│   │   ├── generate_connection_briefs.py
│   │   ├── generate_dossiers.py
│   │   └── build_graph.py
│   ├── utilities/                      # Utility scripts
│   │   ├── __init__.py
│   │   ├── fix_sources.py
│   │   ├── export_sources.py
│   │   └── inject_ecf_links.py
│   ├── monitoring/                     # Monitoring/watching
│   │   ├── __init__.py
│   │   └── brief_watcher.py
│   ├── lib/                            # Shared libraries
│   │   ├── __init__.py
│   │   ├── slug.py                     # Slug standardization
│   │   ├── citation.py                 # Citation formatting
│   │   └── validation.py               # Data validation
│   └── requirements.txt                # Python dependencies
│
├── data/                               # Data files (source of truth)
│   ├── README.md                       # Data dictionary
│   ├── entities/                       # Entity data
│   │   ├── entities-master.json        # Master entity list
│   │   └── entities-index.md           # Human-readable index
│   ├── connections/                    # Connection data
│   │   ├── connections.json
│   │   └── manifest.json
│   ├── sources/                        # Source metadata
│   │   ├── source-catalog.json
│   │   └── citation-index.json
│   └── cache/                          # Cached computations
│       └── .gitkeep
│
├── sources/                            # Primary source documents (read-only)
│   ├── README.md                       # Source catalog
│   ├── giuffre-v-maxwell/              # 97 unsealed docs
│   ├── maxwell-criminal/               # 8 criminal case docs
│   ├── house-oversight-2025/           # 33,572 DOJ release
│   ├── financial-enablers/             # 27 banking docs
│   ├── fbi-vault/                      # 8 FBI FOIA releases
│   ├── florida-case/                   # 7 Florida case docs
│   ├── doj-transparency-2025/          # 9 DOJ docs
│   └── [additional categories]/
│
├── content/                            # Generated content (build artifacts)
│   ├── README.md                       # Content organization
│   ├── briefs/                         # Published briefs
│   │   ├── entity/                     # Entity profiles
│   │   │   ├── alan-dershowitz.md
│   │   │   ├── jeffrey-epstein.md
│   │   │   └── [38 total]
│   │   └── connections/                # Connection analyses
│   │       ├── alan-dershowitz_jeffrey-epstein.md
│   │       ├── manifest.json
│   │       └── [86 total]
│   ├── reports/                        # Research reports
│   │   ├── fbi-investigation-timeline.md
│   │   ├── epstein-financial-timeline.md
│   │   └── [20+ reports]
│   └── audits/                         # Audit reports
│       ├── 2025-12-24-legal-compliance/
│       └── 2025-12-24-source-citation/
│
├── website/                            # Website build
│   ├── README.md                       # Build instructions
│   ├── src/                            # Website source templates
│   │   ├── index.html
│   │   ├── about.html
│   │   ├── continuum.html
│   │   ├── legal.html
│   │   └── templates/
│   │       ├── brief-template.html
│   │       └── entity-template.html
│   ├── public/                         # Built website (deploy this)
│   │   ├── index.html
│   │   ├── about.html
│   │   ├── assets/
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── images/
│   │   ├── briefs/                     # Symlink to /t/content/briefs/
│   │   ├── sources/                    # Symlink to /t/sources/
│   │   └── data/                       # Symlink to /t/data/
│   └── build.sh                        # Website build script
│
├── agents/                             # AI agent specifications
│   ├── README.md                       # Agent system overview
│   ├── tasks/                          # Task-specific agents
│   │   ├── entity-extractor.md
│   │   ├── connection-builder.md
│   │   └── citation-validator.md
│   ├── themes/                         # Theme research agents
│   │   ├── fbi-theme-researcher.md
│   │   └── cia-history-researcher.md
│   ├── managers/                       # Orchestration agents
│   │   └── entity-index-manager.md
│   └── outputs/                        # Agent-generated findings
│       ├── epstein-extraction/
│       │   ├── findings/
│       │   └── synthesis/
│       └── [other agent outputs]/
│
├── logs/                               # Operational logs
│   ├── session-log.md                  # Claude session history
│   ├── progress.json                   # Pipeline progress tracking
│   └── errors/                         # Error logs
│       └── .gitkeep
│
├── research/                           # Research materials
│   ├── README.md                       # Research tracking
│   ├── foia/                           # FOIA requests/responses
│   ├── outreach/                       # Outreach correspondence
│   ├── meeting-notes/                  # Interview notes
│   └── topics/                         # Topic-specific research
│       ├── cia-history/
│       └── prince-andrew/
│
├── tmp/                                # Temporary working files
│   ├── .gitignore                      # Ignore all contents
│   └── README.md                       # Usage guidelines
│
└── archive/                            # Historical materials
    ├── README.md                       # Archive index
    ├── 2025-12-23-briefs-backup/
    ├── 2025-12-23-data-archive/
    └── legacy-docs/
```

---

### Key Changes Explained

#### 1. Root Directory Cleanup

**Before:** 17 markdown files + 3 shell scripts (20 files)
**After:** 4 markdown files + 11 directories

```
Root files retained:
- README.md                  # Brief project overview, points to /docs/
- CHANGELOG.md               # Version history
- .env                       # Environment variables (gitignored)
- .gitignore                 # Git exclusions

Everything else moved into logical directories.
```

**Rationale:** Clean root directory improves first impressions and reduces cognitive load.

---

#### 2. Configuration Consolidation

**All configuration in `/config/`:**

```
/config/
├── claude/                  # Claude-specific
├── ollama/                  # LLM configs
├── agents/                  # Agent specifications (YAML)
├── templates/               # Document templates
└── quality-standards.md     # Editorial standards
```

**No more scattered configs** across root, /t/.claude/, /templates/, etc.

---

#### 3. Documentation Hierarchy

**All documentation in `/docs/`:**

```
/docs/
├── getting-started.md       # New user onboarding
├── session-guide.md         # Replaces SESSION_START_PROMPT.md
├── architecture.md          # System design
├── reference/               # Reference materials
│   ├── entities-index.md    # Moved from root
│   └── legal-framework.md   # Extracted from CLAUDE.md
├── guides/                  # How-to documentation
└── standards/               # Project standards
```

**Session workflow:**
1. Claude reads `/docs/getting-started.md`
2. Checks `/logs/session-log.md` for recent activity
3. Consults `/docs/reference/` for entity lookups

---

#### 4. Code Organization (`/src/`)

**Before:** Flat `/scripts/` directory (13 files)
**After:** Organized by function

```
/src/
├── extraction/              # Data extraction scripts
├── generation/              # Content generation
├── utilities/               # Utility functions
├── monitoring/              # Watchers
└── lib/                     # Shared libraries
```

**Benefits:**
- Clear categorization
- Easier to find relevant script
- Shared libraries prevent code duplication
- Python package structure (with `__init__.py`)

---

#### 5. Data Management (`/data/`)

**Single source of truth for all data:**

```
/data/
├── entities/
│   ├── entities-master.json     # Canonical entity data
│   └── entities-index.md        # Human-readable (generated from JSON)
├── connections/
│   └── connections.json
├── sources/
│   └── source-catalog.json
└── cache/                       # Ephemeral cached data
```

**Build pipeline:**
```
entities-master.json → (generate) → entities-index.md
                                 → (generate) → website/public/data/entities.json
```

**No more uncertainty** about which file is authoritative.

---

#### 6. Content vs Source Separation

**Primary sources (immutable):**
```
/sources/                        # Original PDFs (33,745 documents)
```

**Generated content (mutable):**
```
/content/
├── briefs/                      # AI-generated analytical briefs
├── reports/                     # Research reports
└── audits/                      # Audit reports
```

**Publishing workflow:**
```
/content/briefs/ → (build) → /website/public/briefs/ (via symlink)
```

---

#### 7. Website Build Pipeline

**Before:** Unclear if HTML is hand-edited or generated
**After:** Clear source vs build separation

```
/website/
├── src/                         # Source templates (hand-edited)
│   ├── index.html
│   ├── about.html
│   └── templates/
├── public/                      # Built output (deploy this)
│   ├── [generated HTML]
│   ├── briefs/   → symlink to /t/content/briefs/
│   ├── sources/  → symlink to /t/sources/
│   └── data/     → symlink to /t/data/
└── build.sh                     # Build script
```

**Workflow:**
1. Edit templates in `/website/src/`
2. Run `./website/build.sh`
3. Outputs to `/website/public/`
4. Deploy `/website/public/` to web server

**Safeguards:** Never edit `/website/public/` directly (will be overwritten)

---

#### 8. Backup Strategy

**Before:** Scattered backups in 10+ locations
**After:** Systematic archival

```
/archive/                        # Historical snapshots
├── 2025-12-23-briefs-backup/
├── 2025-12-23-data-archive/
└── legacy-docs/

External backups (not in project):
/mnt/backups/continuum/          # Separate backup volume
├── daily/
├── weekly/
└── monthly/
```

**No .bak files** — version control handles this
**No duplicate backup directories** — single archive location
**Timestamped archives** moved outside active project

---

#### 9. Temporary Files

**Before:** Unclear if /cache/, /work/, /downloads/ are safe to delete
**After:** Clear temporary location

```
/tmp/
├── .gitignore                   # Ignores all contents
└── README.md                    # "Safe to delete anytime"
```

**All temporary work** goes here
**Git ignores** entire directory
**Can be cleared** without checking

---

#### 10. Slug Standardization

**Standardize all entity slugs to hyphenated format:**

```
Before:
  Entity briefs:     alan_dershowitz
  Connection briefs: alan-dershowitz

After:
  All files:         alan-dershowitz

Rename plan:
  analytical_brief_alan_dershowitz.md → alan-dershowitz.md
  analytical_brief_jeffrey_epstein.md → jeffrey-epstein.md
  [all 38 entity briefs]
```

**Benefits:**
- URL-friendly (hyphens preferred in URLs)
- Cross-platform compatibility
- Consistent programmatic access
- Aligns with web standards

---

### Naming Convention Standards

#### File Naming

**Markdown Documents:**
```
Format: lowercase-hyphenated-slug.md
Examples:
  getting-started.md
  entity-index-guide.md
  fbi-investigation-timeline.md

NOT:
  Getting_Started.md
  entity_index_guide.md
  FBI-Investigation-Timeline.md
```

---

**Entity Briefs:**
```
Format: [entity-slug].md
Location: /content/briefs/entity/

Examples:
  alan-dershowitz.md
  jeffrey-epstein.md
  ghislaine-maxwell.md
  jpmorgan-chase.md
  giuffre-v-maxwell.md

NOT:
  analytical_brief_alan_dershowitz.md  (verbose prefix)
  Alan-Dershowitz.md                   (capitalized)
  alan_dershowitz.md                   (underscores)
```

---

**Connection Briefs:**
```
Format: [entity-a-slug]_[entity-b-slug].md
Location: /content/briefs/connections/

Ordering: Alphabetical by slug (not by importance)

Examples:
  alan-dershowitz_jeffrey-epstein.md
  bill-clinton_ghislaine-maxwell.md
  deutsche-bank_jeffrey-epstein.md

NOT:
  jeffrey-epstein_alan-dershowitz.md   (wrong order)
  AlanDershowitz_JeffreyEpstein.md     (capitalized)
  alan-dershowitz-jeffrey-epstein.md   (single hyphen, ambiguous)
```

**Connection Index:**
```
Format: [entity-slug]_connections.md

Examples:
  alan-dershowitz_connections.md
  bill-clinton_connections.md
```

---

**Python Scripts:**
```
Format: verb_noun.py (underscores for Python convention)
Location: /src/[category]/

Examples:
  extract_entities.py
  generate_briefs.py
  validate_citations.py

NOT:
  ExtractEntities.py                   (PascalCase)
  extract-entities.py                  (hyphens not Pythonic)
```

---

**Shell Scripts:**
```
Format: verb-noun.sh (hyphens)
Location: /bin/

Examples:
  setup-environment.sh
  mount-server.sh
  deploy-website.sh

NOT:
  setup_environment.sh                 (underscores less common in shell)
  SetupEnvironment.sh                  (PascalCase)
```

---

**JSON Data Files:**
```
Format: noun-description.json (hyphens)
Location: /data/[category]/

Examples:
  entities-master.json
  connections-index.json
  source-catalog.json

NOT:
  entities_master.json                 (underscores)
  EntitiesMaster.json                  (PascalCase)
  manifest.json                        (too generic without directory context)
```

---

**Configuration Files:**
```
Format: noun-description.yaml or config-name.json
Location: /config/[category]/

Examples:
  project-knowledge.md
  quality-standards.md
  entity-extractor.yaml

NOT:
  CLAUDE_PROJECT_KNOWLEDGE.md          (SCREAMING_SNAKE_CASE)
```

---

#### Directory Naming

**Standard:**
```
Format: lowercase-hyphenated
Examples:
  entity-briefs/
  connection-analyses/
  source-documents/

NOT:
  Entity_Briefs/
  connectionAnalyses/
  source_documents/
```

**Exception:** Python package directories use underscores (Python convention)
```
Acceptable:
  /src/entity_discovery/
  /src/citation_validator/
```

---

#### Entity Slug Creation Rules

**For Persons:**
```
Format: firstname-lastname

Examples:
  alan-dershowitz
  jeffrey-epstein
  virginia-giuffre
  jean-luc-brunel           (preserve hyphenated first names)
  prince-andrew             (titles become part of name)

Edge cases:
  virginia-roberts-giuffre  (maiden-married name, use most recent)
  → Standardize on: virginia-giuffre
```

---

**For Organizations:**
```
Format: organization-name-acronym (if applicable)

Examples:
  jpmorgan-chase
  deutsche-bank
  fbi
  cia
  bank-of-credit-and-commerce-international-bcci

Prefer acronym for well-known entities:
  bcci (not bank-of-credit-and-commerce-international)
  fbi  (not federal-bureau-of-investigation)
```

---

**For Legal Cases:**
```
Format: plaintiff-v-defendant-case

Examples:
  giuffre-v-maxwell
  giuffre-v-dershowitz
  epstein-florida-case
  us-v-maxwell
```

---

**For Events/Concepts:**
```
Format: descriptive-slug

Examples:
  iran-contra
  intelligence-financial-nexus
  epstein-florida-plea-deal
```

---

### Manifest File Standards

**Instead of generic `manifest.json` in every directory:**

```
Before:
  /data/manifest.json
  /briefs/connections/manifest.json
  /website/data/manifest.json

After:
  /data/data-catalog.json
  /content/briefs/connections/connections-manifest.json
  /website/public/data/website-manifest.json
```

**Each manifest has descriptive name** indicating its purpose.

---

## Migration Strategy

### Phase 1: Preparation (Week 1)

**Goal:** Set up version control and backup current state

#### Tasks:

1. **Initialize Git Repository**
   ```bash
   cd /t/
   git init
   git add .
   git commit -m "Initial commit: Pre-reorganization snapshot"
   ```

2. **Create External Backup**
   ```bash
   # Backup to external drive/server
   robocopy /t/ /mnt/backups/continuum/2025-12-24-pre-reorg/ /E /ZB /MT:8
   ```

3. **Rotate Exposed API Token**
   - Log into Paperless-ngx (http://localhost:8040)
   - Generate new API token
   - Update scripts that reference token
   - Revoke old token `da99fe6aa0b8d021689126cf72b91986abbbd283`

4. **Create .env File**
   ```bash
   # /t/.env
   PAPERLESS_API_TOKEN=<new-token>
   PAPERLESS_BASE_URL=http://localhost:8040
   # All services run locally on WoodsDen via Docker
   # No network shares or remote servers needed
   ```

5. **Create .gitignore**
   ```bash
   # /t/.gitignore
   .env
   *.bak
   __pycache__/
   *.pyc
   /tmp/
   /data/cache/
   /logs/errors/
   /archive/
   /website/public/
   ```

---

### Phase 2: Directory Structure (Week 2)

**Goal:** Create new directory structure without breaking existing functionality

#### Tasks:

1. **Create New Directories**
   ```bash
   mkdir -p /t/bin
   mkdir -p /t/config/{claude,ollama,agents,templates}
   mkdir -p /t/docs/{reference,guides,standards,api}
   mkdir -p /t/src/{extraction,generation,utilities,monitoring,lib}
   mkdir -p /t/data/{entities,connections,sources,cache}
   mkdir -p /t/content/{briefs/entity,briefs/connections,reports,audits}
   mkdir -p /t/website/{src,public}
   mkdir -p /t/agents/{tasks,themes,managers,outputs}
   mkdir -p /t/logs/errors
   mkdir -p /t/tmp
   mkdir -p /t/archive
   ```

2. **Create README Files**
   - Write README.md in each major directory explaining its purpose
   - Include file naming conventions
   - Document what belongs in each location

---

### Phase 3: Content Migration (Week 3)

**Goal:** Move files to new locations systematically

#### Move Root Documentation:

```bash
# Documentation → /docs/
mv /t/CLAUDE.md /t/docs/session-guide.md
mv /t/index.md /t/docs/getting-started.md
mv /t/ENTITIES_README.md /t/docs/reference/entity-index-guide.md
mv /t/entities_index.md /t/data/entities/entities-index.md
mv /t/SESSION_START_PROMPT.md /t/docs/reference/session-start-prompt.md
mv /t/CONTEXT_INDEX.md /t/docs/reference/context-index.md
mv /t/connection_brief_reference.md /t/docs/reference/connection-guide.md

# Infrastructure docs → /docs/
mv /t/CONTINUUM_REPORT_INFRASTRUCTURE_ASSESSMENT.md /t/docs/architecture.md
mv /t/IMPLEMENTATION_ROADMAP.md /t/docs/roadmap.md
mv /t/QUICK_START_GUIDE.md /t/docs/quick-start.md

# Audit/report docs → /content/audits/ or /archive/
mv /t/source_link_audit.md /t/content/audits/source-citation-audit-2025-12-21.md
```

---

#### Move Scripts:

```bash
# Setup scripts → /bin/
mv /t/setup-claude-config.sh /t/bin/setup-claude.sh
mv /t/setup-claude-full.sh /t/bin/setup-environment.sh
mv /t/setup-claude-plugins.sh /t/bin/setup-plugins.sh

# Python scripts → /src/[category]/
mv /t/scripts/entity_discovery.py /t/src/extraction/
mv /t/scripts/redaction_extractor.py /t/src/extraction/
mv /t/scripts/parse_brief.py /t/src/extraction/

mv /t/scripts/continuum_pipeline.py /t/src/generation/
mv /t/scripts/generate_connection_briefs.py /t/src/generation/
mv /t/scripts/generate_dossiers.py /t/src/generation/
mv /t/scripts/generate_epstein_dossier.py /t/src/generation/
mv /t/scripts/build_graph.py /t/src/generation/

mv /t/scripts/fix_sources.py /t/src/utilities/
mv /t/scripts/export_sources.py /t/src/utilities/
mv /t/scripts/inject_ecf_links.py /t/src/utilities/

mv /t/scripts/brief_watcher.py /t/src/monitoring/

mv /t/scripts/check-woodsden-mount.sh /t/bin/
mv /t/scripts/mount-woodsden.sh /t/bin/

# Remove old scripts directory
rmdir /t/scripts
```

---

#### Move Configuration:

```bash
# Templates → /config/templates/
mv /t/templates/* /t/config/templates/

# Claude config → /config/claude/
mv /t/config/CLAUDE_PROJECT_KNOWLEDGE.md /t/config/claude/project-knowledge.md
mv /t/config/CLAUDE_CODE_CONTINUUM_TASK.md /t/config/claude/task-definition.md
mv /t/.claude/settings.json /t/config/claude/settings.json

# Ollama config
mv /t/config/ollama/* /t/config/ollama/
```

---

#### Move Briefs:

```bash
# Entity briefs → /content/briefs/entity/
# (Also rename to remove 'analytical_brief_' prefix)
cd /t/briefs/entity/
for file in analytical_brief_*.md; do
  newname=$(echo "$file" | sed 's/analytical_brief_//' | sed 's/_/-/g')
  mv "$file" "/t/content/briefs/entity/$newname"
done

# Connection briefs → /content/briefs/connections/
mv /t/briefs/connections/*.md /t/content/briefs/connections/
mv /t/briefs/connections/*.json /t/content/briefs/connections/

# Remove old briefs directory
rm -rf /t/briefs/
```

---

#### Move Reports & Audits:

```bash
# Reports → /content/reports/
mv /t/reports/*.md /t/content/reports/

# Audits → /content/audits/
mv /t/audits/* /t/content/audits/
```

---

#### Move Agent Files:

```bash
# Agent tasks
mv /t/agents/tasks/*.md /t/agents/tasks/

# Agent themes
mv /t/agents/themes/*.md /t/agents/themes/

# Agent outputs (extraction findings)
mv /t/agents/epstein-extraction/ /t/agents/outputs/epstein-extraction/
mv /t/agents/cia-history/ /t/agents/outputs/cia-history/
```

---

#### Move Data Files:

```bash
# Entity data
mv /t/website/data/entities-master.json /t/data/entities/entities-master.json
mv /t/website/data/entities.json /t/data/entities/entities.json

# Connection data
mv /t/website/data/connections.json /t/data/connections/connections.json
mv /t/website/data/hierarchy.json /t/data/connections/hierarchy.json

# FBI theme data
mv /t/website/data/fbi-personnel.json /t/data/entities/fbi-personnel.json
mv /t/website/data/fbi-theme-connections.json /t/data/connections/fbi-theme-connections.json

# Manifests (rename to be descriptive)
mv /t/website/data/manifest.json /t/data/website-manifest.json
```

---

#### Archive Old Backups:

```bash
# Move backup directories to /archive/
mv /t/briefs_backup_20251223_075731/ /t/archive/2025-12-23-briefs-backup/
mv /t/data_archive_20251223/ /t/archive/2025-12-23-data-archive/
mv /t/-md_backups/ /t/archive/legacy-markdown-backups/

# Delete .bak files (now versioned in git)
find /t/content/briefs/ -name "*.bak" -delete

# Consolidate website backups
mv /t/website/backups/ /t/archive/website-backups/
rm -rf /t/website/Backups/  # Remove duplicate case-variant directory
```

---

### Phase 4: Update References (Week 4)

**Goal:** Update all file references and symlinks

#### Update Python Script Imports:

```python
# Before:
from parse_brief import extract_entities

# After:
from src.extraction.parse_brief import extract_entities
```

**Tasks:**
1. Update all Python scripts with new import paths
2. Update requirements.txt location: `/t/src/requirements.txt`
3. Test all scripts to ensure they run

---

#### Update Documentation Links:

**Update all markdown files with new paths:**

```bash
# Example: Update links in docs/getting-started.md
# Before: [CLAUDE.md](CLAUDE.md)
# After: [Session Guide](reference/session-guide.md)

# Use sed or manual editing
find /t/docs/ -name "*.md" -exec sed -i 's|CLAUDE\.md|reference/session-guide.md|g' {} \;
find /t/docs/ -name "*.md" -exec sed -i 's|entities_index\.md|../data/entities/entities-index.md|g' {} \;
```

---

#### Create Symlinks for Website:

```bash
# Website needs to reference content and sources
cd /t/website/public/
ln -s ../../content/briefs ./briefs
ln -s ../../sources ./sources
ln -s ../../data ./data
```

**Verify symlinks work:**
```bash
ls -la /t/website/public/briefs/entity/
# Should show entity briefs from /t/content/briefs/entity/
```

---

#### Update Agent Configurations:

**Update agent YAML files with new paths:**

```yaml
# Before:
input_directory: /t/briefs/entity/

# After:
input_directory: /t/content/briefs/entity/
```

---

### Phase 5: Standardize Slugs (Week 5)

**Goal:** Ensure all entity slugs use consistent hyphenated format

#### Entity Slug Audit:

```bash
# Create mapping of old slugs to new slugs
# Example: alan_dershowitz → alan-dershowitz

cd /t/content/briefs/entity/

# Already renamed during move, but verify:
ls -1 *.md | grep "_"  # Should return nothing (no underscores)
```

#### Update Connection Brief Entity References:

**Connection briefs may reference old slugs in frontmatter/metadata:**

```bash
cd /t/content/briefs/connections/

# Search for underscore slugs in connection briefs
grep -r "alan_dershowitz" . | wc -l

# Replace with hyphenated versions
find . -name "*.md" -exec sed -i 's/alan_dershowitz/alan-dershowitz/g' {} \;
find . -name "*.md" -exec sed -i 's/jeffrey_epstein/jeffrey-epstein/g' {} \;
# ... repeat for all entities
```

#### Update JSON Data Files:

```bash
# Update entities-master.json with hyphenated slugs
cd /t/data/entities/

# Use Python script to update slugs in JSON
python3 << 'EOF'
import json

with open('entities-master.json', 'r') as f:
    data = json.load(f)

# Update slugs in data structure
# (Implementation depends on JSON structure)
# ... slug standardization logic ...

with open('entities-master.json', 'w') as f:
    json.dump(data, f, indent=2)
EOF
```

---

### Phase 6: Testing & Validation (Week 6)

**Goal:** Ensure all systems work after reorganization

#### Test Checklist:

**1. Python Scripts:**
```bash
cd /t/src/extraction/
python3 entity_discovery.py --test
python3 parse_brief.py --test

cd /t/src/generation/
python3 continuum_pipeline.py --dry-run
python3 generate_connection_briefs.py --test
```

**2. Website Build:**
```bash
cd /t/website/
./build.sh
# Verify /t/website/public/ populated correctly
ls -la public/briefs/entity/
```

**3. Agent Execution:**
```bash
# Test agent with new paths
cd /t/agents/tasks/
# Run test agent execution
```

**4. Documentation Links:**
```bash
# Verify all documentation links resolve
cd /t/docs/
grep -r "\[.*\](.*\.md)" . | while read line; do
  # Extract and test each link
  # (Manual verification recommended)
done
```

**5. Data Integrity:**
```bash
# Verify entity count unchanged
cat /t/data/entities/entities-master.json | jq '.people | length'
# Should match pre-migration count: 2,008

# Verify brief count
ls /t/content/briefs/entity/*.md | wc -l  # Should be 38
ls /t/content/briefs/connections/*.md | wc -l  # Should be 86
```

---

### Phase 7: Cleanup (Week 7)

**Goal:** Remove obsolete files and directories

#### Safe Deletion:

```bash
# Remove empty directories
find /t/ -type d -empty -delete

# Remove temp file
rm /t/NDH6SA~M

# Remove __pycache__ directories
find /t/ -type d -name "__pycache__" -exec rm -rf {} +

# Remove .pyc files
find /t/ -name "*.pyc" -delete

# Remove .tmp files
find /t/ -name ".tmp" -delete
```

#### Archive Old Structure:

```bash
# If any old directories remain, archive them
# Example: /t/database/paperless/ (empty)
rmdir /t/database/paperless/
rmdir /t/database/  # If now empty
```

---

### Phase 8: Documentation Update (Week 8)

**Goal:** Update all documentation to reflect new structure

#### Create New README.md:

```markdown
# The Continuum Report

> An independent intelligence analysis project mapping connections between power structures through primary source documentation.

## Quick Start

New to the project? Start here:
- [Getting Started Guide](docs/getting-started.md)
- [Session Workflow](docs/session-guide.md)
- [Project Architecture](docs/architecture.md)

## Documentation

All documentation is in [`/docs/`](docs/):
- **Reference:** Entity index, legal framework, citation guide
- **Guides:** Creating briefs, running extractions, deploying website
- **Standards:** Naming conventions, quality checklist

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| `/docs/` | Project documentation |
| `/src/` | Python automation scripts |
| `/data/` | Entity/connection data (source of truth) |
| `/sources/` | Primary source PDFs (33,745 documents) |
| `/content/` | Generated briefs and reports |
| `/website/` | Static website build |
| `/config/` | Configuration files |
| `/bin/` | Setup/deployment scripts |

See [docs/architecture.md](docs/architecture.md) for details.

## Contact

- **Website:** https://thecontinuumreport.com
- **Email:** contact@thecontinuumreport.com

---

*Another Node in the Decentralized Intelligence Agency*
```

#### Update Session Guide:

```markdown
# The Continuum Report — Session Guide

> For Claude agents: How to navigate this project effectively.

## Session Initialization

1. **Read this file first:** `/docs/session-guide.md`
2. **Check recent activity:** `/logs/session-log.md`
3. **Understand the architecture:** `/docs/architecture.md`

## Key Resources

| Resource | Location |
|----------|----------|
| Entity Index | `/data/entities/entities-index.md` |
| Entity Guide | `/docs/reference/entity-index-guide.md` |
| Legal Framework | `/docs/reference/legal-framework.md` |
| Quality Standards | `/config/quality-standards.md` |

## Common Tasks

### Research an Entity
1. Search entity index: `/data/entities/entities-index.md`
2. Read entity brief: `/content/briefs/entity/[slug].md`
3. Check connections: `/content/briefs/connections/[slug]_connections.md`

### Generate New Brief
1. Review template: `/config/templates/analytical-brief.md`
2. Follow standards: `/config/quality-standards.md`
3. Output to: `/content/briefs/entity/[slug].md`

### Run Extraction
1. Navigate to: `/src/extraction/`
2. Run script: `python3 entity_discovery.py`
3. Check output: `/agents/outputs/[agent-name]/`

[... continue with detailed task workflows ...]
```

---

### Rollback Plan

**If migration fails:**

1. **Git Reset:**
   ```bash
   cd /t/
   git reset --hard HEAD~1  # Return to pre-migration state
   ```

2. **Restore from Backup:**
   ```bash
   robocopy /mnt/backups/continuum/2025-12-24-pre-reorg/ /t/ /E /ZB /MT:8
   ```

3. **Document Issues:**
   - Log what failed in `/logs/migration-issues.md`
   - Identify root cause before retrying

---

## Maintenance Recommendations

### Daily Operations

**1. Session Logging:**
- Update `/logs/session-log.md` at end of each Claude session
- Include: date, task, files created/modified, agents spawned

**2. Brief Quality Review:**
- Before publishing to website, run quality checklist
- Verify all source links resolve
- Check for proper legal framework headers

**3. Backup Monitoring:**
- Ensure automated backups running to external storage
- Do NOT create .bak files manually (use git)

---

### Weekly Maintenance

**1. Dependency Updates:**
```bash
cd /t/src/
pip list --outdated
# Review and update requirements.txt
```

**2. Link Validation:**
```bash
# Check for broken citation links
cd /t/content/briefs/
grep -r "https://thecontinuumreport.com/sources/" . | \
  while read line; do
    # Extract URL and test (requires link checker tool)
  done
```

**3. Cache Cleanup:**
```bash
# Clear ephemeral cache
rm -rf /t/data/cache/*
rm -rf /t/tmp/*
```

**4. Archive Old Logs:**
```bash
# Move logs older than 90 days to archive
find /t/logs/ -name "*.log" -mtime +90 -exec mv {} /t/archive/logs/ \;
```

---

### Monthly Maintenance

**1. Entity Index Regeneration:**
```bash
cd /t/src/extraction/
python3 entity_discovery.py --full-reindex
# Updates /t/data/entities/entities-master.json
# Regenerates /t/data/entities/entities-index.md
```

**2. Slug Consistency Audit:**
```bash
# Check for underscore slugs (should find none)
find /t/content/briefs/ -name "*_*.md" | grep -v "_connections.md"

# If found, standardize to hyphens
```

**3. Configuration Backup:**
```bash
# Backup all config to external storage
tar -czf /mnt/backups/continuum/config-$(date +%Y%m%d).tar.gz /t/config/
```

**4. Archive Old Audits:**
```bash
# Move audits older than 6 months to archive
find /t/content/audits/ -type d -mtime +180 -exec mv {} /t/archive/audits/ \;
```

---

### Quarterly Maintenance

**1. Comprehensive Backup:**
```bash
# Full project backup (excluding sources, which are static)
robocopy /t/ /mnt/backups/continuum/quarterly-$(date +%Y%m%d)/ \
  /E /ZB /MT:8 /XD sources
```

**2. Dead Link Audit:**
- Review all briefs for broken PDF links
- Update links if documents moved
- Note any permanently unavailable sources

**3. Git Cleanup:**
```bash
# Remove old branches
git branch --merged | grep -v "\*" | xargs -n 1 git branch -d

# Garbage collection
git gc --aggressive
```

**4. Documentation Review:**
- Read through all `/docs/` files
- Update outdated information
- Add new guides as needed

---

### Annual Maintenance

**1. Full Entity Revalidation:**
- Re-extract entities from all sources
- Compare with current entity index
- Merge new discoveries

**2. Template Updates:**
- Review legal landscape for new case law
- Update templates if legal requirements changed
- Regenerate existing briefs if necessary

**3. Technology Stack Review:**
- Evaluate Python version
- Consider alternative LLM providers
- Assess website performance

**4. Archive Strategy:**
- Review archived materials
- Permanently delete obsolete archives (after 2+ years)
- Compress remaining archives

---

### Git Workflow

**Branching Strategy:**

```
main                     ← Production-ready content
├── develop              ← Active development
│   ├── feature/fbi-extraction
│   ├── feature/new-brief-template
│   └── bugfix/citation-links
└── archive/legacy       ← Historical snapshots
```

**Commit Standards:**

```bash
# Feature work
git checkout -b feature/entity-extraction-v2
# ... make changes ...
git add src/extraction/entity_discovery.py
git commit -m "feat(extraction): Add multi-document entity correlation

- Correlate entity mentions across documents
- Generate confidence scores for entity matches
- Export to entities-master.json

Closes #42"

# Bugfix
git checkout -b bugfix/broken-pdf-links
git commit -m "fix(briefs): Update PDF links for relocated sources

- Update 15 briefs with new source paths
- Verify all links resolve correctly

Fixes #38"

# Documentation
git commit -m "docs(guides): Add extraction pipeline guide"

# Merge to develop
git checkout develop
git merge feature/entity-extraction-v2
git branch -d feature/entity-extraction-v2

# Release to main
git checkout main
git merge develop
git tag -a v2.0.0 -m "Version 2.0: Reorganized project structure"
git push origin main --tags
```

**Commit Message Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:** feat, fix, docs, style, refactor, test, chore

---

### Quality Assurance Checklist

**Before Publishing a Brief:**

- [ ] **Legal Framework**
  - [ ] Opinion-protection header present
  - [ ] "Public Record" section contains only quotes + citations
  - [ ] "Editorial Analysis" uses opinion-signaling language
  - [ ] Alternative Interpretations section (5-7 minimum)
  - [ ] Right of Response invitation included

- [ ] **Citations**
  - [ ] Every quote has hyperlinked source
  - [ ] All PDF links resolve correctly
  - [ ] Source table at end of document
  - [ ] Page numbers provided for all quotes

- [ ] **Naming & Formatting**
  - [ ] Filename uses hyphenated slug
  - [ ] Entity name consistent across all briefs
  - [ ] Markdown formatting correct (headers, lists, blockquotes)
  - [ ] No trailing whitespace or formatting artifacts

- [ ] **Content Quality**
  - [ ] No rhetorical questions implying guilt
  - [ ] Exculpatory evidence included where applicable
  - [ ] Subject's legal status noted (charges vs convictions)
  - [ ] No use of "dossier" terminology
  - [ ] Neutral, analytical tone maintained

- [ ] **Technical**
  - [ ] File saved to correct directory (`/content/briefs/entity/` or `/content/briefs/connections/`)
  - [ ] Added to entities-master.json (if new entity)
  - [ ] Session log updated
  - [ ] Git commit created

---

### Automation Recommendations

**1. Pre-Commit Hooks:**

Create `/t/.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Pre-commit hook for The Continuum Report

echo "Running pre-commit checks..."

# Check for .bak files
if git diff --cached --name-only | grep -q '\.bak$'; then
  echo "ERROR: .bak files detected. Use git for versioning instead."
  exit 1
fi

# Check for exposed secrets
if git diff --cached | grep -q 'da99fe6aa0b8d021689126cf72b91986abbbd283'; then
  echo "ERROR: Old API token found in commit. Remove immediately."
  exit 1
fi

# Check for underscore slugs in entity briefs
if git diff --cached --name-only | grep 'content/briefs/entity/.*_.*\.md' | grep -v '_connections\.md'; then
  echo "WARNING: Entity brief with underscores detected. Use hyphens instead."
  echo "Example: alan-dershowitz.md (not alan_dershowitz.md)"
fi

# Validate JSON files
for file in $(git diff --cached --name-only | grep '\.json$'); do
  if ! python3 -m json.tool "$file" > /dev/null 2>&1; then
    echo "ERROR: Invalid JSON in $file"
    exit 1
  fi
done

echo "Pre-commit checks passed."
exit 0
```

Make executable:
```bash
chmod +x /t/.git/hooks/pre-commit
```

---

**2. Automated Link Checker:**

Create `/t/bin/check-links.sh`:

```bash
#!/bin/bash
# Check all PDF links in briefs

BRIEFS_DIR="/t/content/briefs"
SOURCES_DIR="/t/sources"
ERRORS=0

echo "Checking PDF links in briefs..."

# Extract all PDF links from markdown files
grep -roh 'https://thecontinuumreport.com/sources/[^)]*\.pdf' "$BRIEFS_DIR" | \
  sort -u | \
  while read url; do
    # Convert URL to local file path
    filepath=$(echo "$url" | sed 's|https://thecontinuumreport.com/sources/|'"$SOURCES_DIR"'/|')

    if [ ! -f "$filepath" ]; then
      echo "BROKEN: $url"
      ERRORS=$((ERRORS + 1))
    fi
  done

if [ $ERRORS -eq 0 ]; then
  echo "All links valid."
  exit 0
else
  echo "Found $ERRORS broken links."
  exit 1
fi
```

Run weekly:
```bash
chmod +x /t/bin/check-links.sh
./bin/check-links.sh
```

---

**3. Automated Backup Script:**

Create `/t/bin/backup-continuum.sh`:

```bash
#!/bin/bash
# Automated backup script

BACKUP_DIR="/mnt/backups/continuum"
DATE=$(date +%Y%m%d-%H%M%S)

# Daily backup (exclude sources, which are static)
echo "Creating daily backup..."
robocopy /t/ "$BACKUP_DIR/daily/$DATE/" \
  /E /ZB /MT:8 \
  /XD sources archive tmp \
  /LOG:"$BACKUP_DIR/logs/backup-$DATE.log"

# Rotate daily backups (keep last 7 days)
find "$BACKUP_DIR/daily/" -type d -mtime +7 -exec rm -rf {} +

# Weekly backup (Sundays)
if [ $(date +%u) -eq 7 ]; then
  echo "Creating weekly backup..."
  cp -r "$BACKUP_DIR/daily/$DATE/" "$BACKUP_DIR/weekly/$DATE/"

  # Rotate weekly backups (keep last 4 weeks)
  find "$BACKUP_DIR/weekly/" -type d -mtime +28 -exec rm -rf {} +
fi

echo "Backup complete: $BACKUP_DIR/daily/$DATE/"
```

Add to cron:
```bash
# Run daily at 2 AM
0 2 * * * /t/bin/backup-continuum.sh
```

---

**4. Entity Index Auto-Update:**

Create `/t/bin/update-entity-index.sh`:

```bash
#!/bin/bash
# Regenerate entity index from master JSON

cd /t/src/extraction/

echo "Regenerating entity index from entities-master.json..."

python3 << 'EOF'
import json
import os

# Load master JSON
with open('/t/data/entities/entities-master.json', 'r') as f:
    data = json.load(f)

# Generate markdown index
output = "# MASTER ENTITY INDEX\n\n"
output += "**Generated:** " + datetime.now().isoformat() + "\n\n"

# People section
output += "## People\n\n"
for person in sorted(data['people'].keys()):
    mentions = data['people'][person]['mentions']
    sources = len(data['people'][person]['sources'])
    output += f"**{person}** — {mentions} mentions across {sources} sources\n"
    # ... add sources list ...

# Organizations section
output += "\n## Organizations\n\n"
# ... similar processing ...

# Write output
with open('/t/data/entities/entities-index.md', 'w') as f:
    f.write(output)

print("Entity index regenerated.")
EOF

echo "Entity index updated: /t/data/entities/entities-index.md"
```

---

### Monitoring Recommendations

**1. Disk Space Monitoring:**

```bash
# Check if sources directory exceeds 100GB
du -sh /t/sources/ | awk '{if ($1 > "100G") print "WARNING: Sources directory exceeds 100GB"}'
```

**2. File Count Monitoring:**

```bash
# Alert if entity briefs count changes unexpectedly
CURRENT=$(ls /t/content/briefs/entity/*.md | wc -l)
EXPECTED=38

if [ $CURRENT -ne $EXPECTED ]; then
  echo "WARNING: Entity brief count changed ($CURRENT vs $EXPECTED)"
fi
```

**3. Session Log Monitoring:**

```bash
# Check if session log updated in last 7 days
LAST_UPDATED=$(stat -c %Y /t/logs/session-log.md)
NOW=$(date +%s)
DAYS=$((($NOW - $LAST_UPDATED) / 86400))

if [ $DAYS -gt 7 ]; then
  echo "WARNING: Session log not updated in $DAYS days"
fi
```

---

## Conclusion

### Summary of Recommendations

**Immediate Actions (This Week):**
1. Rotate exposed API token in CLAUDE.md
2. Create .env file for secrets management
3. Initialize git repository
4. Create external backup before reorganization
5. Delete 95 .bak files across briefs directories

**Short-Term Actions (Next Month):**
1. Implement proposed directory structure
2. Migrate files systematically (Phase 2-7 of migration plan)
3. Standardize all entity slugs to hyphenated format
4. Consolidate duplicate backup directories
5. Archive orphaned directories (briefs_backup_20251223_075731/, -md_backups/, etc.)

**Ongoing Practices:**
1. Use git for version control (no more .bak files)
2. Update session log after each Claude interaction
3. Follow naming convention standards for all new files
4. Run quality checklist before publishing briefs
5. Maintain clear separation of source vs generated content

---

### Benefits of Reorganization

**For Human Operators:**
- Faster navigation (clear directory purposes)
- Reduced confusion (single source of truth for data)
- Easier onboarding (comprehensive /docs/)
- Better collaboration (git workflow)
- Improved security (secrets in .env)

**For AI Agents:**
- Predictable file locations (standardized paths)
- Clear session initialization (docs/session-guide.md)
- Reliable entity lookup (data/entities/entities-index.md)
- Systematic task execution (organized /src/ scripts)
- Reduced hallucination (authoritative references)

**For Project Sustainability:**
- Scalable structure (supports growth to 10,000+ briefs)
- Maintainable codebase (organized scripts, clear dependencies)
- Professional presentation (suitable for collaboration/funding)
- Disaster recovery (systematic backups, git history)
- Legal defensibility (proper version tracking, audit trail)

---

### Next Steps

**Week 1:**
1. Review this analysis with WoodsBandit
2. Get approval for proposed structure
3. Schedule migration phases
4. Create pre-migration backup

**Week 2-8:**
1. Execute migration plan systematically
2. Test after each phase
3. Document any deviations from plan
4. Update session log with progress

**Week 9+:**
1. Begin using new structure for all work
2. Establish maintenance routines
3. Monitor for issues
4. Iterate on improvements

---

### Contact

**Questions about this analysis:**
- Document: `/t/FILE_ORGANIZATION_ANALYSIS.md`
- Created: 2025-12-24
- Analyst: Claude Sonnet 4.5 (Documentation Architect)
- Session: [Log session ID in /logs/session-log.md]

**For implementation support:**
- Spawn dedicated "File Organization Migration" agent
- Reference this document as specification
- Execute migration phases systematically

---

**END OF ANALYSIS**

*The Continuum Report — Another Node in the Decentralized Intelligence Agency*
