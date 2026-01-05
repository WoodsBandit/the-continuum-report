# THE CONTINUUM REPORT — Unified Standards

**Created:** 2026-01-05
**Purpose:** Single source of truth for all project standards

---

## THE CORE PRINCIPLE

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│         CONNECTION BRIEFS ARE THE SOURCE OF TRUTH                       │
│                                                                         │
│         No connection exists without a corresponding brief.             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## CONNECTION MODEL (Binary)

A connection either **EXISTS** in a source document or it **DOESN'T**.

No subjective scoring. No "strength" levels. No "evidence levels."

### For Each Connection, Document:

| Field | Required | Description |
|-------|----------|-------------|
| **Quote** | ✅ | The exact text from the source showing the connection |
| **Source** | ✅ | Document ID + page number |
| **Link** | ✅ | Path to hosted PDF (e.g., `/sources/ecf-1328-44.pdf`) |
| **Summary** | ✅ | One-sentence description of what the connection is |

### Example:

```json
{
  "entity1": "jeffrey-epstein",
  "entity2": "ghislaine-maxwell",
  "quote": "Ghislaine was present when I first arrived",
  "source": "ECF 1328-44",
  "page": 89,
  "link": "/sources/giuffre-v-maxwell/ecf-1328-44.pdf",
  "summary": "Testimony describes Maxwell as present at Epstein properties"
}
```

---

## DATA FLOW

```
                    ┌───────────────────┐
                    │  SOURCE DOCUMENTS │
                    │  (Court filings,  │
                    │   depositions)    │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │  CONNECTION BRIEF │
                    │  (pairwise .md)   │
                    │                   │
                    │  Quote + Source + │
                    │  Summary          │
                    └─────────┬─────────┘
                              │
                              ▼ build_connections_from_briefs.py
                    ┌───────────────────┐
                    │  connections.json │
                    │  (DERIVED DATA)   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │  Website Display  │
                    │  (continuum.html) │
                    └───────────────────┘
```

**Key insight:** `connections.json` is DERIVED from briefs. The brief is the source of truth.

---

## WHAT WE DON'T DO

| ❌ Don't | ✅ Do Instead |
|----------|--------------|
| Assign "strength" scores (80, 60, etc.) | Document quote + source + summary |
| Use "evidence levels" (DOCUMENTED/ALLEGED/etc.) | Just show the quote and let it speak |
| Rate "confidence" (High/Medium/Low) | Cite the source - reader can evaluate |
| Infer connections without sources | Only document what's in the record |
| Create connections.json entries manually | Run `build_connections_from_briefs.py` |

---

## RELATIONSHIP TYPES (12)

These categorize the **nature** of a connection, not its "strength":

| Type | Definition |
|------|------------|
| professional | Business, employment, contractual relationship |
| social | Personal acquaintance, friendship |
| financial | Money transfers, accounts, investments |
| familial | Blood or marriage relation |
| institutional | Shared organizational affiliation |
| legal | Litigation, representation, testimony |
| alleged | Claimed in court docs but not proven |
| documented | Established by records |
| referenced | Mentioned together in documents |
| testimonial | Based on witness statements |
| transactional | Single or limited interaction |
| adversarial | Opposition, conflict, litigation |

---

## LEGAL FRAMEWORK

All analytical content follows *Milkovich v. Lorain Journal* opinion protections:

1. **Label as editorial commentary**
2. **Separate facts from interpretation**
3. **Use opinion-signaling language**
4. **Include 5-7 alternative interpretations**
5. **Invite subject responses**

---

## BRIEF APPROVAL SEPARATION

⚠️ **Creation of briefs should NEVER be approved in the same Claude session that made them.**

1. Session 1 creates brief → saves to `/pending/`
2. Session 2 reviews → approves → moves to production
3. No exceptions

---

## FILES UPDATED TO THIS STANDARD

| File | Location | Updated |
|------|----------|---------|
| entity-extractor.md | T:\agents\ | 2026-01-05 |
| overseer.md | T:\agents\ | 2026-01-05 |
| cross-reference-finder.md | T:\agents\ | 2026-01-05 |
| project-status-tracker.md | T:\agents\ | 2026-01-05 |
| CLAUDE_CODE_CONTINUUM_TASK.md | T:\config\ | 2026-01-05 |
| CLAUDE_PROJECT_KNOWLEDGE.md | T:\config\ | 2026-01-05 |

---

## IMPLEMENTATION

### Creating a New Connection

1. Find quote in source document
2. Create pairwise connection brief in `/briefs/connections/`
3. Run `python scripts/build_connections_from_briefs.py`
4. Verify connection appears on website

### Rebuilding All Connections

```bash
cd /continuum
python scripts/build_connections_from_briefs.py
```

This will:
- Parse all connection briefs
- Generate fresh `connections.json`
- Update `entities.json` with connection data

---

## SUMMARY

| Concept | Standard |
|---------|----------|
| Source of truth | Connection briefs (markdown) |
| Connection model | Binary - exists or doesn't |
| Required fields | Quote, Source, Page, Link, Summary |
| Strength scoring | **NONE** - the source speaks for itself |
| Evidence levels | **NONE** - just quote the source |
| Data generation | Briefs → `build_connections_from_briefs.py` → JSON |

---

*Another Node in the Decentralized Intelligence Agency*
