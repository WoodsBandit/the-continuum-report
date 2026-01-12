# THE CONTINUUM REPORT - Project Briefing

> "For there is nothing hidden that will not be disclosed, and nothing concealed that will not be known or brought out into the open." — Luke 8:17

## What This Is

The Continuum Report is an independent intelligence analysis project focused on mapping connections between power structures, documented events, and the people involved. We are building a comprehensive, well-sourced repository of dossiers and reports based on primary source documents - court filings, depositions, FOIA releases, flight logs, financial records, and investigative books.

**Tagline:** *Another Node in the Decentralized Intelligence Agency*

---

## LEGAL FRAMEWORK (Critical)

This project operates under First Amendment protections. All content must comply with these standards:

### The Three Categories

Every statement in a dossier must be clearly one of:

1. **DOCUMENTED FACT** - Directly from source document, cited
   - "Flight logs show [Person] traveled on [Date]."
   - "Court filing 15-cv-7433 states..."

2. **ALLEGATION** - Claim made in a source, reported AS an allegation
   - "The plaintiff alleged in court filings that..."
   - "According to [Witness]'s deposition testimony..."

3. **ANALYSIS** - Editorial interpretation, clearly labeled
   - "The documented pattern suggests..."
   - "This raises questions about..."

### Required Attribution

NEVER state a fact without attribution:
- ❌ "Bill Clinton visited the island 26 times."
- ✅ "According to flight logs obtained in case 15-cv-7433, Bill Clinton..."

### Dossier Header

Every dossier MUST include this header:

```markdown
> **OPEN SOURCE INTELLIGENCE DOSSIER**
>
> *Classification: OSINT — Public Sources Only*
>
> This dossier synthesizes information from publicly available source documents.
> Allegations from legal filings are reported as allegations, not established facts.
> Analysis represents editorial commentary. Inclusion does not imply wrongdoing.
>
> [Editorial Standards](/legal.html)
```

### What We Don't Do

- Make accusations of criminal conduct
- State allegations as facts
- Speculate beyond what documents show
- Include private individuals not in public records
- Publish without source attribution

### Fair Report Privilege

We can report what's IN court documents even if the allegations are unproven. But we must:
- Accurately quote/represent the document
- Attribute to the document
- Present as allegation, not fact

### Florida Anti-SLAPP

Florida Statute § 768.295 protects against frivolous defamation suits related to free speech on public issues. This is our jurisdiction.

---

## Quality Standards for Dossiers

### Every Dossier Must Have:

1. **Header** with legal disclaimer
2. **Executive summary** (who/what is this about)
3. **Source list** - every document used, with Paperless IDs
4. **Methodology note** - "AI-assisted synthesis, human reviewed"
5. **Gaps section** - what we DON'T know
6. **No speculation** beyond documented connections

### Citation Format:

```
According to [Document Title] (Paperless ID: XX), [factual claim].
```

Or for court filings:

```
In [Case Name], Case No. [Number], [party] alleged that [allegation].
```

### Quality Checklist Before Publishing:

- [ ] Every factual claim has a source citation
- [ ] Allegations are clearly labeled as allegations  
- [ ] Analysis is framed as analysis ("suggests", "raises questions")
- [ ] Header disclaimer is present
- [ ] Source documents are listed with IDs
- [ ] No unsourced accusations
- [ ] Gaps/limitations acknowledged

The vision is rigorous, evidence-based investigation that connects dots across time and institutions. No speculation. Every claim sourced. The kind of work intelligence agencies do, but open source and decentralized.

## The Operator

WoodsBandit is the sole operator. Christian worldview informs the mission but the work itself is forensic - we document what the evidence shows, not what we want it to show. The goal is truth, rigorously sourced.

## Technical Infrastructure

### Server: Tower (Unraid)
- **Hardware:** Intel i7-10700K, 16GB RAM (memory constrained)
- **IP:** 192.168.1.139
- **OS:** Unraid

### Key Containers
| Container | Port | Purpose |
|-----------|------|---------|
| paperless-ngx | 8040 | Document management, OCR, search |
| ollama-cpu | 11434 | Local LLM (Mistral 7B) - backup option |
| continuum-python | - | Python runtime for scripts |
| continuum-web | 8081 | Nginx serving the website |
| cloudflared-tunnel | - | Secure tunnel to Cloudflare |
| claude-code | - | Claude Code CLI (THIS INSTANCE) |
| Redis | 6379 | Cache for Paperless |

### Paperless-ngx
- **API Token:** da99fe6aa0b8d021689126cf72b91986abbbd283
- **Documents:** ~200+ processed (Epstein case files, Whitney Webb books, court filings)
- **Tags:** CASE:*, PERSON:*, document types for categorization
- **Document Types:** AI Dossier, Book, Court Filing, Deposition, Exhibit, Flight Log, FOIA Release, etc.

### Website
- **Domain:** thecontinuumreport.com
- **Hosted via:** Cloudflare tunnel → continuum-web container
- **Email:** contact@thecontinuumreport.com (Cloudflare Email Routing)

## The Zoom Framework

Three-level hierarchical view for understanding events:

1. **Power Structures** (top level) - Systems, institutions, networks of control
2. **Specific Cases** (middle) - Documented events, legal cases, investigations  
3. **Breaking News** (ground level) - Current developments, new revelations

The website has an interactive zoom.html page implementing this with entity connections, document links, and navigation.

## The AI Pipeline

Located at: `/continuum/scripts/continuum_pipeline.py`

### What It Does
1. Searches Paperless for documents matching a subject
2. **Filters out previously generated dossiers** (critical - prevents circular sourcing)
3. Extracts structured entities (people, orgs, dates, locations, claims) from ALL matching docs
4. Auto-tags documents in Paperless based on detected entities
5. Generates a comprehensive dossier with citations to source documents
6. Saves markdown output to `/continuum/reports/`

### Key Design Principles
- **EXHAUSTIVE** - Process ALL matching documents, not arbitrary limits
- **NO SHORTCUTS** - Entity extraction is the whole point. Never skip it.
- **CHECKPOINTING** - Saves progress after each doc so crashes don't lose work
- **SOURCE INTEGRITY** - Never use previously generated dossiers as sources for new ones

### Current Version: 3.1 (Memory Safe)
Due to Tower's 16GB RAM limit, the pipeline has aggressive memory management:
- 10s delay between documents
- 30s pause every 5 docs
- Model unload every 10 docs
- Small context window and chunks

**This is why Claude Code is now the preferred approach** - processing happens on Anthropic's infrastructure, no local memory constraints.

## What's Been Built

### Website (thecontinuumreport.com)
- Landing page with project mission
- About page
- Interactive zoom.html with 3-level navigation
- Purple/black/gold theme with Cinzel, Cormorant Garamond, Source Sans typography
- Full mobile responsive

### Pipeline
- Working dossier generation
- Entity extraction and auto-tagging
- Checkpoint/resume capability
- Dossier filtering to prevent circular sourcing

### Sample Dossiers Generated
- Bill Clinton (test runs)

## Current Priorities

1. **Generate exhaustive dossiers** on all people, organizations, and events found in the source documents
2. **Overnight batch processing** - scan all docs for entities, generate dossiers for each, checkpoint progress
3. **Quality** - every dossier should cite multiple sources, note evidence strength, identify gaps

## TODO List (Pinned)
- Fix Claude's write access to `\\192.168.1.139\continuum\` share (currently read-only via SMB)
- Create user system for The Continuum Report (website login, pipeline users, or source attribution - TBD)
- Remote access for pipeline (Cloudflare SSH tunnel or web status dashboard at thecontinuumreport.com/status)

## File Locations

```
/continuum/
├── scripts/           # Python pipeline scripts
├── reports/           # Generated dossiers (markdown)
├── documents/         # Document storage
│   └── inbox/         # Paperless consumption folder
├── checkpoints/       # Pipeline progress checkpoints
├── website/           # HTML/CSS for thecontinuumreport.com
├── config/            # Configuration files
└── CLAUDE.md          # This file
```

## Working With Paperless API

```python
PAPERLESS_URL = "http://192.168.1.139:8040"
headers = {"Authorization": "Token da99fe6aa0b8d021689126cf72b91986abbbd283"}

# Search documents
GET /api/documents/?query=Bill+Clinton

# Get document content
GET /api/documents/{id}/

# Update tags
PATCH /api/documents/{id}/ with {"tags": [1, 2, 3]}

# Create tag
POST /api/tags/ with {"name": "PERSON: John Doe"}
```

## Guiding Principles

1. **Primary Sources First** - Court documents, depositions, official records over news articles or commentary
2. **Cite Everything** - "According to [Document Title]..." for every factual claim
3. **Note Evidence Quality** - Distinguish testimony, documents, circumstantial evidence
4. **Identify Gaps** - What don't we know? What's missing?
5. **No Speculation** - Report what the documents show, not theories
6. **Connections Matter** - The value is in mapping relationships across documents

## Commands for This Claude Instance

You have access to:
- `/continuum/` filesystem
- Ability to run Python scripts
- Ability to create/edit files
- Bash access in the container

Common tasks:
- `cd /continuum && ls` - see project structure
- `cat /continuum/scripts/continuum_pipeline.py` - read the pipeline
- Run Python directly or modify scripts as needed

## The Mission

Build the most comprehensive, well-sourced, publicly accessible intelligence repository on documented power networks. Every dossier should be something a journalist, researcher, or citizen could cite with confidence. 

We're not making accusations - we're organizing and presenting what's already in the public record, with rigorous citation back to primary sources.

*Another Node in the Decentralized Intelligence Agency*
