---
title: "federal-rules"
type: entity
generated: "2025-12-26T18:03:14.091550Z"
legal_review: "APPROVED"
review_date: "2025-12-26T18:03:14.091550Z"
reviewer: "legal-auditor-agent"
reason: "New entity discovered"
---

## Stage 3 Brief Generation Complete

**Entity:** `federal-rules`
**Status:** **REJECTED** - Boilerplate classification
**Rejection Code:** `BOILERPLATE_ENTITY`

### Summary

The entity "federal-rules" was rejected for analytical brief generation because:

1. **Not a substantive entity:** "Federal Rules" refers to the Federal Rules of Civil Procedure (FRCP), a standard body of procedural rules in federal litigation
2. **Already in boilerplate filter:** Entity is listed in `/continuum/indexes/boilerplate_filter.json` under `exclude_exact` with reason `legal_jargon`
3. **No public interest value:** Procedural rules are neutral legal framework elements with no investigative significance
4. **False NER extraction:** The 16 mentions across 4 sources are standard legal citations, not substantive content

### Pipeline Actions Completed

| Action | Status | Output |
|--------|--------|--------|
| Entity assessment | ✅ Complete | Identified as boilerplate |
| Rejection notice | ✅ Written | `/continuum/briefs/entity/REJECTED_federal-rules.md` |
| Pipeline log | ✅ Updated | `/continuum/logs/stage3_brief_generation.log` |
| Boilerplate filter | ✅ Verified | Already present in filter |

### Recommended Cleanup

- Remove `federal-rules` from `/continuum/indexes/entity_registry.json`
- Remove co-occurrence pairs involving `federal-rules` from `co_occurrence.json`
- Update Stage 1 extraction to apply boilerplate filter earlier in pipeline
