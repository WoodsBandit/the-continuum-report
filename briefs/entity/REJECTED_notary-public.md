---
entity_name: "notary-public"
entity_type: "BOILERPLATE"
brief_version: "N/A"
last_updated: "2025-12-26T16:45:00Z"
status: "REJECTED"
rejection_reason: "boilerplate_classification"
legal_review: "N/A"
---

# Brief Generation REJECTED: notary-public

## Rejection Summary

**Entity:** notary-public
**Status:** REJECTED - Not a valid entity for analytical brief generation
**Date:** 2025-12-26
**Rejection Code:** BOILERPLATE_ENTITY

---

## Rejection Details

### Classification Finding

The entity "notary-public" has been identified and classified in the pipeline's `boilerplate_filter.json` as:

- **Category:** `exclude_exact`
- **Reason:** `legal_jargon`

### Why This Is Not a Valid Entity

1. **Not a Person, Organization, or Place:** "Notary Public" is a professional legal designation, not a specific individual or entity.

2. **Boilerplate Legal Text:** This term appears in standardized certification blocks on:
   - Deposition transcripts
   - Sworn affidavits
   - Court filings requiring notarization
   - Legal declarations

3. **No Substantive Content:** The 27 source mentions represent notary stamps/certifications, not substantive information about a person or organization.

4. **False Co-Occurrence Inflation:** This entity appears to have connections with many people (Jeffrey Epstein, Ghislaine Maxwell, Alan Dershowitz, etc.) only because their depositions were notarized—not because any meaningful relationship exists.

### Evidence from Index Files

**Entity Registry Entry:**
```json
"notary-public": {
  "name": "Notary Public",
  "mention_count": 27,
  "source_count": 27,
  "sources": ["ecf-1320-12", "ecf-1320-26", "ecf-1320-29", "ecf-1320-30"]
}
```

**Boilerplate Filter Entry:**
```json
"exclude_exact": ["notary-public", ...],
"reason": {
  "notary-public": "legal_jargon"
}
```

---

## Pipeline Action

Per SOP-003 decision logic:

- **No brief generated:** Entity is classified as boilerplate
- **No legal review required:** Entity rejected before content generation
- **Recommendation:** Remove "notary-public" from entity_registry.json to prevent future false triggering

---

## Recommended Cleanup Actions

1. Remove "notary-public" from `entity_registry.json`
2. Remove "notary-public-in" from `entity_registry.json` (related variant)
3. Remove all co-occurrence pairs involving "notary-public" from `co_occurrence.json`
4. Update entity extraction rules to exclude notary certification blocks

---

*Stage 3 Brief Generation - Rejection Notice*
*The Continuum Report Intelligence Pipeline*
*Generated: 2025-12-26T16:45:00Z*
