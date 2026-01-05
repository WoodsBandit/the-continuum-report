# Next Steps Checklist - Pipeline Optimization Follow-Up

**Date:** 2025-12-25
**Pipeline Status:** ✓ COMPLETE - All 7 phases executed successfully

---

## Immediate Actions (Priority: HIGH)

### [ ] 1. Review Priority Connections Queue
**File:** `\\192.168.1.139\continuum\work\priority_connections_queue.md`
**Action:** Manual review of top 20 priority pairs
**Focus:** Attorney-client and witness relationships
**Decision:** Which pairs warrant connection documentation?

**Top 10 for Review:**
- [ ] meredith-schultz ↔ virginia-giuffre (attorney-client, 3 co-mentions)
- [ ] brad-edwards ↔ virginia-giuffre (attorney-client, 3 co-mentions)
- [ ] paul-cassell ↔ virginia-giuffre (attorney-client, 3 co-mentions)
- [ ] ghislaine-maxwell ↔ laura-menninger (defendant-attorney, 3 co-mentions)
- [ ] david-boies ↔ meredith-schultz (co-counsel, 3 co-mentions)
- [ ] juan-alessi ↔ sarah-kellen (witness-defendant, 3 co-mentions)
- [ ] johanna-sjoberg ↔ sarah-kellen (witness-defendant, 3 co-mentions)
- [ ] paul-cassell ↔ sarah-kellen (attorney-witness, 3 co-mentions)
- [ ] brad-edwards ↔ meredith-schultz (co-counsel, 3 co-mentions)
- [ ] jane-doe ↔ paul-cassell (client-attorney, 3 co-mentions)

---

### [ ] 2. Create Analytical Briefs for High-Priority Entities
**File:** `\\192.168.1.139\continuum\reports\entity_curation_gaps.md`
**Total:** 23 entities identified

**Phase 1 - Attorneys (Create First):**
- [ ] David Boies (31 mentions, 4 sources) - Lead attorney for Giuffre
- [ ] Meredith Schultz (38 mentions, 8 sources) - Associate attorney for Giuffre
- [ ] Brad Edwards (27 mentions, 6 sources) - Victims' attorney
- [ ] Paul Cassell (14 mentions, 4 sources) - Victims' rights attorney
- [ ] Jeffrey Pagliuca (20 mentions, 4 sources) - Attorney (needs research)

**Phase 2 - Witnesses (Create Second):**
- [ ] Juan Alessi (16 mentions, 4 sources) - Epstein's house manager
- [ ] Rinaldo Rizzo (13 mentions, 4 sources) - Witness (needs research)
- [ ] Alfredo Rodriguez (12 mentions, 4 sources) - Epstein's employee

**Phase 3 - Locations (Create Third):**
- [ ] Mar-a-Lago (11 mentions, 4 sources) - Trump's resort
- [ ] Virgin Islands (14 mentions, 4 sources) - Epstein's island location
- [ ] London (19 mentions, 4 sources) - Key location in allegations

**Phase 4 - Organizations (Create Fourth):**
- [ ] Palm Beach Police (11 mentions, 4 sources) - Investigating agency
- [ ] Daily Mail (11 mentions, 4 sources) - Media outlet (Sharon Churcher)

**Note:** Jane Doe entities (37 mentions) need careful analysis - may refer to multiple victims

---

### [ ] 3. Switch to Clean Indexes
**Action:** Update all analysis scripts and agents to use clean indexes

**Files to Use:**
- ✓ `\\192.168.1.139\continuum\indexes\entity_registry_clean.json` (1,861 entities)
- ✓ `\\192.168.1.139\continuum\indexes\co_occurrence_clean.json` (95,500 pairs)

**Files to Reference:**
- ✓ `\\192.168.1.139\continuum\indexes\entity_normalization.json` (variant mappings)
- ✓ `\\192.168.1.139\continuum\indexes\boilerplate_filter.json` (exclusion rules)

**Deprecate (Keep for Reference Only):**
- ⚠ `\\192.168.1.139\continuum\indexes\entity_registry.json` (2,015 entities - has boilerplate)
- ⚠ `\\192.168.1.139\continuum\indexes\co_occurrence.json` (117,954 pairs - has noise)

---

## Medium-Priority Actions

### [ ] 4. Build Connection Documentation Agent
**Input:** Priority connections queue
**Output:** Draft connections for `connections.json`
**Approach:**
1. Read shared source documents for each priority pair
2. Extract relationship context (attorney-client, witness-defendant, etc.)
3. Draft connection entry with evidence citations
4. Human review and approval

**Target:** Document top 20 priority pairs

---

### [ ] 5. Refine Boilerplate Filter
**File:** `\\192.168.1.139\continuum\indexes\boilerplate_filter.json`
**Action:** Add additional exclusions discovered in clean data

**Candidates for Addition:**
- [ ] "documents-you" (5 co-mentions with interrogatory terms)
- [ ] "income-you" (5 co-mentions with interrogatory terms)
- [ ] "your-attorneys" (5 co-mentions with interrogatory terms)
- [ ] "your-complaint" (5 co-mentions with interrogatory terms)

**Before Adding:** Verify these are truly non-substantive across all sources

---

### [ ] 6. Expand Entity Normalization Map
**File:** `\\192.168.1.139\continuum\indexes\entity_normalization.json`
**Current:** 11 canonical entities, 10 variants
**Action:** Identify additional variants during manual review

**Watch For:**
- Name variations (e.g., "J. Epstein", "J. E. Epstein")
- Title variations (e.g., "Dr. Smith", "Doctor Smith")
- Organization variations (e.g., "JPMorgan Chase", "JP Morgan")

**Approach:** Conservative - only merge obvious variants

---

## Long-Term Actions

### [ ] 7. Expand Source Corpus
**Issue:** Max co-mention count is only 6 (low overlap in current corpus)
**Target:** Increase co-mention counts to 10+ for key relationships
**Action:** Process additional court documents

**Focus Areas:**
- Documents mentioning low-coverage curated entities
- Depositions (high entity density)
- Trial transcripts
- Discovery responses

---

### [ ] 8. Integrate Filters into Extraction Pipeline
**Current:** Boilerplate filtering happens post-extraction
**Better:** Apply filters during initial extraction
**Benefit:** Reduces processing time and file sizes

**Implementation:**
1. Load boilerplate filter at extraction start
2. Check each entity against filter before adding to registry
3. Apply normalization during extraction (not post-processing)

---

### [ ] 9. Build Automated Connection Suggestions
**Objective:** AI-assisted connection documentation
**Approach:**
1. Agent reads priority pair and shared sources
2. Agent drafts connection with evidence
3. Human reviews and approves
4. Commit to `connections.json`

**Benefits:**
- Faster documentation of 412 priority pairs
- Consistent format and citation style
- Human oversight ensures accuracy

---

## Quality Assurance

### [ ] 10. Validate Clean Indexes
**Action:** Spot-check clean indexes for data integrity

**Tests:**
- [ ] Verify variant merging (check ghislaine-maxwell has 94 mentions)
- [ ] Verify boilerplate exclusion (check "case-no" not in clean registry)
- [ ] Verify co-occurrence normalization (check merged pairs have combined counts)
- [ ] Check for false positives (entities that shouldn't have been excluded)
- [ ] Check for false negatives (boilerplate that slipped through)

---

### [ ] 11. Cross-Reference Curated Connections
**File:** `\\192.168.1.139\continuum\website\data\connections.json` (131 connections)
**Action:** Verify existing connections appear in clean co-occurrence index

**Test:**
- [ ] Load connections.json
- [ ] For each connection, check if pair exists in clean co-occurrence
- [ ] Identify connections with 0 co-mentions in clean data
- [ ] Investigate why (external sources? different entity IDs?)

---

### [ ] 12. Monitor Data Quality Metrics
**Establish Baselines:**
- Entity count: 1,861 (from 2,015)
- Co-occurrence pairs: 95,500 (from 117,954)
- Documented connections: 131
- Curated entities: 37
- Priority undocumented pairs: 412

**Track Over Time:**
- [ ] Entity growth rate
- [ ] Connection documentation rate
- [ ] Brief creation rate
- [ ] Co-occurrence density (avg co-mentions per pair)

---

## Documentation Updates

### [ ] 13. Update README/Documentation
**Action:** Document the new clean indexes and how to use them

**Sections to Add:**
- Clean vs. Original Indexes: When to use which
- Entity Normalization: How variants are mapped
- Boilerplate Filtering: What's excluded and why
- Priority Queue: How scoring works

---

### [ ] 14. Create Entity Extraction Guidelines
**Purpose:** Prevent variant proliferation in future extractions
**Content:**
- Use canonical entity IDs from normalization map
- Check against boilerplate filter before adding
- Standard naming conventions (e.g., "firstname-lastname")
- When to create new entity vs. merge with existing

---

## Files Reference

### Work Files
- `priority_connections_queue.md` - Top 50 undocumented pairs
- `pipeline_optimization_log.md` - Execution log
- `PIPELINE_EXECUTION_SUMMARY.md` - Comprehensive results
- `NEXT_STEPS_CHECKLIST.md` - This file

### Index Files (Production)
- `entity_registry_clean.json` - 1,861 clean entities
- `co_occurrence_clean.json` - 95,500 clean pairs
- `entity_normalization.json` - Variant mappings
- `boilerplate_filter.json` - Exclusion rules

### Reports
- `entity_curation_gaps.md` - 23 entities needing briefs
- `pipeline_optimization_report.md` - Full analysis

### Deprecated (Reference Only)
- `entity_registry.json` - Original (has boilerplate)
- `co_occurrence.json` - Original (has noise)
- `index_pipeline_report.md` - Original gap analysis

---

## Success Criteria

### Phase 1 Complete When:
- [x] All 7 pipeline phases executed
- [x] Clean indexes generated
- [x] Priority queue created
- [x] Curation gaps identified
- [x] Reports generated

### Phase 2 Complete When:
- [ ] Top 20 priority pairs documented in connections.json
- [ ] Top 5 attorney briefs created
- [ ] Top 3 witness briefs created
- [ ] All agents switched to clean indexes
- [ ] Boilerplate filter refined

### Phase 3 Complete When:
- [ ] 412 priority pairs reviewed (documented or rejected)
- [ ] 23 high-priority entities have briefs
- [ ] Source corpus expanded (co-mention counts ≥10)
- [ ] Extraction pipeline uses filters
- [ ] Automated connection suggestions working

---

## Contact/Escalation

**Questions:**
- Check `PIPELINE_EXECUTION_SUMMARY.md` for detailed results
- Check `pipeline_optimization_report.md` for recommendations
- Check execution logs for debugging

**Issues:**
- False positives in boilerplate filter → Manual override in exclusion list
- Missing variants in normalization map → Add to canonical entity
- Data quality concerns → Re-run relevant pipeline phases

---

**Status:** Ready for Phase 2 - Connection Documentation & Brief Creation
**Next Review Date:** After top 20 priority pairs are processed
