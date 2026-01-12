---
entity_name: "pro-hac-vice"
entity_type: "BOILERPLATE"
brief_version: "N/A"
last_updated: "2025-12-26T17:15:00Z"
sources_count: 24
legal_review: "REJECTED"
rejection_code: "BOILERPLATE_ENTITY"
rejection_reason: "legal_jargon"
---

# ENTITY REJECTED: pro-hac-vice

> **STATUS: REJECTED - NOT A VALID ENTITY**
>
> *The Continuum Report Intelligence Pipeline*
>
> This entity has been flagged for rejection based on automated boilerplate filtering.

---

## Rejection Summary

| | |
|---|---|
| **Entity** | pro-hac-vice |
| **Status** | **REJECTED** |
| **Rejection Code** | `BOILERPLATE_ENTITY` |
| **Classification** | `legal_jargon` |
| **Filter Source** | `/continuum/indexes/boilerplate_filter.json` |

---

## Explanation

"Pro hac vice" is a Latin legal term meaning "for this occasion only." It is a procedural designation used when an attorney is admitted to practice in a court for a specific case, despite not being a member of that jurisdiction's bar.

### Why This Is Not a Valid Entity

1. **Legal Procedural Term**: "Pro hac vice" is a standard legal phrase appearing in court filings, not a person, organization, location, or event.

2. **No Substantive Intelligence Value**: The term appears in attorney admission notices, signature blocks, and procedural filings. It provides no information about the substance of cases.

3. **Explicit Boilerplate Classification**: This term is explicitly listed in `boilerplate_filter.json`:
   ```json
   {
     "exclude_exact": ["pro-hac-vice", ...],
     "reason": {
       "pro-hac-vice": "legal_jargon"
     }
   }
   ```

4. **False Co-occurrence Inflation**: The term's appearance in attorney blocks creates spurious connections with actual entities (witnesses, parties, attorneys) that have no substantive meaning.

---

## Source Analysis

| Metric | Value |
|--------|-------|
| Total Mentions | 24 |
| Source Documents | 4 |
| Source IDs | ecf-1320-11, ecf-1320-18, ecf-1320-21, ecf-1320-25 |

### Context of Mentions

The 24 mentions across 4 documents represent:
- Attorney admission certificates
- Signature blocks indicating "pro hac vice" status
- Procedural notices of appearance

**No substantive content was identified.**

---

## Recommended Actions

1. **Do Not Generate Brief**: No analytical brief should be created for this term.

2. **Verify Filter Application**: This entity should have been filtered during Stage 1 ingestion. Review why it was added to the entity registry despite being in the exclusion list.

3. **Remove from Entity Registry**: Consider removing this entry from `entity_registry.json` to prevent future false processing triggers.

4. **Pipeline Review**: Ensure Stage 1 applies `boilerplate_filter.json` before entity registration.

---

## Pipeline Processing Note

This rejection notice was generated during Stage 3 (Brief Generation) when the entity was queued for brief creation. The entity should not have reached this stage, indicating a potential issue in Stage 1 filtering.

**Processing Log Entry:**
```
2025-12-26T17:15:00Z | REJECT | Entity "pro-hac-vice" rejected as BOILERPLATE
2025-12-26T17:15:00Z | INFO   | Classification: legal_jargon
2025-12-26T17:15:00Z | INFO   | Filter source: boilerplate_filter.json (line 4)
2025-12-26T17:15:00Z | WARN   | Entity should not have been registered - review Stage 1 filter
```

---

*Generated: 2025-12-26*

*The Continuum Report Intelligence Pipeline - Stage 3: Brief Generation*
