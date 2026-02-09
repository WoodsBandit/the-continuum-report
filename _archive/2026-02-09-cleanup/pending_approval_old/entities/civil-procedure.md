---
title: "civil-procedure"
type: entity
generated: "2025-12-26T17:49:33.287141Z"
legal_review: "APPROVED"
review_date: "2025-12-26T17:49:33.287141Z"
reviewer: "legal-auditor-agent"
reason: "New entity discovered"
---

## Stage 3 Processing Result: BRIEF NOT GENERATED

**Entity:** civil-procedure  
**Decision:** SKIP - No brief warranted

### Determination Summary

| Check | Result |
|-------|--------|
| Entity exists in registry | ✓ Yes (16 mentions, 16 sources) |
| Entity in boilerplate filter | ✓ Yes - `exclude_exact` list |
| Filter classification | `legal_jargon` |
| Meaningful entity type | ✗ No - standard court terminology |
| Substantive connections | ✗ No - only co-occurs with other legal boilerplate |

### Reasoning

The entity "civil-procedure" refers to the **Federal Rules of Civil Procedure** - the body of rules governing civil litigation in U.S. federal courts. This term appears in court filings as standard procedural language (e.g., "pursuant to Federal Rule of Civil Procedure 26(b)").

**Why no brief:**
1. **Boilerplate exclusion**: Listed in `boilerplate_filter.json` under `exclude_exact` with reason `legal_jargon`
2. **Not a meaningful entity**: Not a person, organization, event, or substantive topic
3. **No intelligence value**: Standard legal terminology that provides no analytical insight
4. **Connection quality**: All 16 co-occurrences are with other legal boilerplate terms (case-no, electronic-filing, protective-order, etc.)

### Pipeline Log Entry

Entry written to `/continuum/logs/stage3_brief_generation.log`:
```
[2025-12-26T...] | SKIP | Entity 'civil-procedure' found in boilerplate_filter.exclude_exact list
[2025-12-26T...] | SKIP | Reason: legal_jargon - refers to 'Federal Rules of Civil Procedure' standard court terminology
[2025-12-26T...] | INFO | Brief generation SKIPPED - entity does not warrant analytical brief
```

### Recommendation

Consider removing "civil-procedure" from the `entity_registry.json` entirely, or maintaining a separate "excluded_entities" index to prevent future processing requests for known boilerplate terms.
