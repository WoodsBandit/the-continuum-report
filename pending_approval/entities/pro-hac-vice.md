---
title: "pro-hac-vice"
type: entity
generated: "2025-12-26T17:17:21.983303Z"
legal_review: "APPROVED"
review_date: "2025-12-26T17:17:21.983303Z"
reviewer: "legal-auditor-agent"
reason: "New entity discovered"
---

## Summary

**Entity "pro-hac-vice" has been REJECTED** as a boilerplate entity.

### Findings

| Property | Value |
|----------|-------|
| **Entity** | pro-hac-vice |
| **Status** | REJECTED |
| **Rejection Code** | `BOILERPLATE_ENTITY` |
| **Classification** | `legal_jargon` |
| **Mention Count** | 24 |
| **Source Count** | 4 |

### Explanation

"Pro hac vice" is a Latin legal term meaning "for this occasion only." It is a procedural designation used when an attorney is admitted to practice law in a court jurisdiction for a specific case. This term:

1. **Is explicitly listed** in `/continuum/indexes/boilerplate_filter.json` as `legal_jargon`
2. **Appears only in attorney admission notices** and signature blocks
3. **Has no substantive intelligence value** - it's purely procedural language
4. **Creates false co-occurrences** with actual entities (attorneys, parties) that are meaningless

### Actions Taken

1. **Rejection notice created**: `/continuum/briefs/entity/REJECTED_pro-hac-vice.md`
2. **REVIEW_LOG.md updated**: Added rejection entry to the Rejected (Boilerplate Entities) section
3. **Pipeline log updated**: `/continuum/logs/stage3_brief_generation.log`

### Pipeline Issue Identified

This entity should NOT have reached Stage 3 - it is explicitly in the `exclude_exact` list in `boilerplate_filter.json`. This indicates Stage 1 (Source Ingestion) may not be properly applying the boilerplate filter during entity registration.

**Recommended Action**: Remove "pro-hac-vice" from `entity_registry.json` and verify Stage 1 filter application is working correctly.
