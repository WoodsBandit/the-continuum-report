---
title: "case-no"
type: entity
generated: "2025-12-26T15:56:47.700191Z"
legal_review: "MANUAL_REVIEW"
review_date: "2025-12-26T15:56:47.700191Z"
reviewer: "legal-auditor-agent"
reason: "New entity discovered"
issues:
  - "Could not parse legal check output"
---

## Stage 3 Processing Result: SKIP

### Entity: `case-no`

**Decision:** NO BRIEF GENERATED

**Reason:** Entity is classified as boilerplate (`legal_jargon`) in `/continuum/indexes/boilerplate_filter.json`

### Analysis Summary

| Field | Value |
|-------|-------|
| Entity Name | Case No |
| Entity Type | unknown |
| Mention Count | 46 |
| Source Count | 46 (4 unique) |
| Boilerplate Status | **YES - EXCLUDED** |
| Exclusion Type | `legal_jargon` |
| Matched Filter | `exclude_exact` (line 25) + pattern `^case-` |

### Why This Entity Is Excluded

"Case No." is standard legal document header text that appears in virtually every court filing. Examples:
- "Case No. 18-cv-80590-KAM"
- "Case No. 9:08-cv-80736"

This is procedural boilerplate, not a substantive entity worthy of an analytical brief. The high mention count (46) simply reflects that every document references its case number.

### Log Entry
```
2025-12-26T15:55:48+00:00 | INFO | Stage 3 SKIP: Entity 'case-no' is classified as boilerplate (legal_jargon) in boilerplate_filter.json - no brief generated
```

### Recommendation

The entity `case-no` should be **removed from the entity registry** during the next Stage 1 or Stage 2 cleanup pass, as the boilerplate filter was added specifically to exclude such terms. Current index files still contain this entity due to being processed before the filter was in place.
