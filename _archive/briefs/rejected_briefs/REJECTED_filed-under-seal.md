---
entity_name: "filed-under-seal"
entity_type: "BOILERPLATE"
brief_version: "N/A"
last_updated: "2025-12-26T18:35:00Z"
sources_count: 15
legal_review: "REJECTED"
rejection_code: "BOILERPLATE_ENTITY"
rejection_reason: "legal_jargon"
---

# ENTITY REJECTED: filed-under-seal

> **STATUS: REJECTED - NOT A VALID ENTITY**
>
> *The Continuum Report Intelligence Pipeline*
>
> This entity has been flagged for rejection based on automated boilerplate filtering.

---

## Rejection Summary

| | |
|---|---|
| **Entity** | filed-under-seal |
| **Status** | **REJECTED** |
| **Rejection Code** | `BOILERPLATE_ENTITY` |
| **Classification** | `legal_jargon` |
| **Filter Source** | `/continuum/indexes/boilerplate_filter.json` |

---

## Explanation

"Filed under seal" is a legal procedural notation indicating that a court document or exhibit has been submitted to the court confidentially and is not part of the public record. This notation appears on cover sheets, exhibit lists, and filing notices.

### Why This Is Not a Valid Entity

1. **Legal Procedural Term**: "Filed under seal" is a standard legal phrase appearing in court filing metadata, not a person, organization, location, or event.

2. **No Substantive Intelligence Value**: The term indicates document status (confidential vs. public), not the content of documents. It provides no information about the substance of cases or relationships between parties.

3. **Explicit Boilerplate Classification**: This term is explicitly listed in `boilerplate_filter.json`:
   ```json
   {
     "exclude_exact": ["filed-under-seal", ...],
     "reason": {
       "filed-under-seal": "legal_jargon"
     }
   }
   ```

4. **False Co-occurrence Inflation**: The term's appearance on exhibit cover sheets and filing notices creates spurious connections with actual entities (witnesses, parties, attorneys) that have no substantive meaning. Documents being "filed under seal" does not establish a relationship between the entities mentioned in those documents.

---

## Source Analysis

| Metric | Value |
|--------|-------|
| Total Mentions | 15 |
| Source Documents | 4 |
| Source IDs | ecf-1320-26, ecf-1325-4, ecf-1327-21, ecf-1327-22 |

### Context of Mentions

The 15 mentions across 4 documents represent:
- Cover sheet notations indicating sealed filing status
- Exhibit list annotations marking sealed exhibits
- Filing notices indicating confidential submission
- Protective order compliance statements

**No substantive content was identified.**

### Co-occurring Entities in These Sources

The sources containing "filed-under-seal" also contain the following entities, which may have substantive value:
- **ecf-1320-26**: Prince Andrew, Kelli Ann Willis
- **ecf-1325-4**: Detective Joe, Jared Weisfeld, Jeff Pagliuca, Luc Brunel, Lynn Miller, Maria Alessi, Michael Austrich, Sigrid McCawley
- **ecf-1327-21**: Dear Ghislaine, Eva Dubin, Glenn Dubin, Leslie Fagin
- **ecf-1327-22**: Kelli Ann Willis

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
2025-12-26T18:35:00Z | REJECT | Entity "filed-under-seal" rejected as BOILERPLATE
2025-12-26T18:35:00Z | INFO   | Classification: legal_jargon
2025-12-26T18:35:00Z | INFO   | Filter source: boilerplate_filter.json (line 6)
2025-12-26T18:35:00Z | WARN   | Entity should not have been registered - review Stage 1 filter
```

---

*Generated: 2025-12-26*

*The Continuum Report Intelligence Pipeline - Stage 3: Brief Generation*
