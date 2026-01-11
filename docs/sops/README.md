# The Continuum Report - SOP Suite Documentation

**Complete Standard Operating Procedure Suite for Autonomous Pipeline**
**Version:** 1.0
**Created:** 2025-12-25
**Status:** Production Ready

---

## Overview

This SOP suite provides comprehensive operational documentation for The Continuum Report's autonomous intelligence pipeline. The pipeline processes source documents through four automated stages with only two human touchpoints.

## Design Philosophy

**Autonomous Operation:** 95% of the pipeline runs without human intervention
**Human Touchpoints:** Only 2 points require human decision-making
**Legal Compliance:** Automated legal review with human oversight
**Quality Control:** Multiple validation gates at each stage
**Transparency:** Complete audit trail from source to publication

---

## SOP Documents

### Core Pipeline SOPs

1. **[SOP-000-master-pipeline.md](SOP-000-master-pipeline.md)**
   - **Purpose:** Complete pipeline overview and architecture
   - **Audience:** All operators, new team members
   - **Contains:**
     - Stage dependencies and data flow
     - Human touchpoint details
     - Critical decision logic
     - Quality control gates
     - Error handling strategy
   - **Read this first** to understand the complete system

2. **[SOP-001-source-ingestion.md](SOP-001-source-ingestion.md)**
   - **Purpose:** Process new documents and extract entities
   - **Trigger:** Paperless webhook on document upload
   - **Key Functions:**
     - Entity extraction (new + known)
     - Entity registry updates
     - Source tracking
     - Duplicate detection
   - **Outputs:** Updated entity_registry.json, source_mentions.json

3. **[SOP-002-context-extraction.md](SOP-002-context-extraction.md)**
   - **Purpose:** Extract relationship contexts and co-occurrences
   - **Trigger:** Change to entity_registry.json
   - **Key Functions:**
     - Context window extraction (±500 chars)
     - Co-occurrence detection
     - Relationship signal analysis
     - Relevance scoring
   - **Outputs:** Updated co_occurrence.json, connection_contexts.json

4. **[SOP-003-brief-generation.md](SOP-003-brief-generation.md)**
   - **Purpose:** Generate/update analytical briefs
   - **Trigger:** Change to connection_contexts.json
   - **Key Functions:**
     - CREATE vs UPDATE decision logic
     - Brief generation using templates
     - Legal compliance review (18-point checklist)
     - Auto-approval processing
   - **Outputs:** Briefs in pending_approval/ directory

5. **[SOP-004-publication.md](SOP-004-publication.md)**
   - **Purpose:** Publish approved briefs to website
   - **Trigger:** Files in approved/ directory
   - **Key Functions:**
     - Website data updates (entities.json, connections.json)
     - Brief publication
     - Source PDF publishing
     - Archival with timestamps
   - **Outputs:** Live website content, archived briefs

### Operational Documents

6. **[RUNBOOK.md](RUNBOOK.md)**
   - **Purpose:** Quick reference for daily operations
   - **Audience:** Pipeline operators
   - **Contains:**
     - Quick start guide
     - Common operations
     - Troubleshooting procedures
     - Emergency procedures
     - Maintenance tasks
   - **Use this** for day-to-day operations

---

## Pipeline Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│  HUMAN TOUCHPOINT #1: Upload Document to Paperless              │
└────────────┬─────────────────────────────────────────────────────┘
             │
             ▼
    ┌─────────────────┐
    │   STAGE 1       │  Webhook Trigger
    │   Ingestion     │  Extract entities (new + known)
    │   SOP-001       │  Update entity_registry.json
    └────────┬────────┘
             │ entity_registry.json modified
             ▼
    ┌─────────────────┐
    │   STAGE 2       │  File Watch Trigger
    │   Context       │  Extract context windows
    │   SOP-002       │  Identify co-occurrences
    └────────┬────────┘
             │ connection_contexts.json modified
             ▼
    ┌─────────────────┐
    │   STAGE 3       │  File Watch Trigger
    │   Briefs        │  CREATE or UPDATE briefs
    │   SOP-003       │  Legal compliance review
    └────────┬────────┘  Output to pending_approval/
             │
             ▼
┌──────────────────────────────────────────────────────────────────┐
│  HUMAN TOUCHPOINT #2: Review pending_approval/ and Approve      │
└────────────┬─────────────────────────────────────────────────────┘
             │
             ▼
    ┌─────────────────┐
    │   STAGE 4       │  Directory Watch Trigger
    │   Publication   │  Update website data
    │   SOP-004       │  Publish briefs and sources
    └────────┬────────┘  Archive published content
             │
             ▼
    ┌─────────────────┐
    │  LIVE WEBSITE   │
    │  continuum.html │
    └─────────────────┘
```

---

## Directory Structure

```
\\192.168.1.139\continuum\
├── pending_approval/          # Stage 3 output - awaiting human review
│   ├── entities/             # New/updated entity briefs
│   ├── connections/          # New/updated connection briefs
│   └── REVIEW_LOG.md         # Auto-generated review summary
│
├── approved/                  # Human-approved briefs ready for publication
│   ├── entities/
│   └── connections/
│
├── archive/
│   └── published/            # Published briefs with timestamps
│       ├── entities/
│       └── connections/
│
├── sops/                      # THIS DIRECTORY - Standard Operating Procedures
│   ├── SOP-000-master-pipeline.md      (21 KB)
│   ├── SOP-001-source-ingestion.md     (23 KB)
│   ├── SOP-002-context-extraction.md   (30 KB)
│   ├── SOP-003-brief-generation.md     (44 KB)
│   ├── SOP-004-publication.md          (35 KB)
│   ├── RUNBOOK.md                      (21 KB)
│   └── README.md                       (this file)
│
├── indexes/                   # JSON indexes tracking pipeline state
│   ├── entity_registry.json
│   ├── source_mentions.json
│   ├── co_occurrence.json
│   ├── processed_sources.json
│   └── connection_contexts.json
│
├── briefs/                    # Current analytical products
│   ├── entity/
│   └── connections/
│
├── templates/                 # Brief generation templates
│   ├── entity-brief-template.md
│   └── connection-brief-template.md
│
├── website/                   # Publication destination
│   ├── data/
│   │   ├── entities.json
│   │   └── connections.json
│   ├── briefs/
│   │   ├── entity/
│   │   └── connections/
│   ├── sources/
│   └── continuum.html
│
└── sources/                   # Original source documents
    └── paperless_mirror/
```

---

## Quick Start Guide

### For New Operators

1. **Read SOP-000** (Master Pipeline) - Understand the complete system
2. **Bookmark RUNBOOK.md** - Your daily reference guide
3. **Practice approval workflow:**
   ```bash
   cd \\192.168.1.139\continuum\pending_approval
   cat REVIEW_LOG.md
   # Review briefs in entities/ and connections/
   # Move approved items to ../approved/
   ```

### For Daily Operations

**Morning Routine:**
```bash
# Check pending approvals
ls \\192.168.1.139\continuum\pending_approval\entities\
ls \\192.168.1.139\continuum\pending_approval\connections\

# Read review log
cat \\192.168.1.139\continuum\pending_approval\REVIEW_LOG.md

# Check for errors
tail -50 \\192.168.1.139\continuum\logs\pipeline_errors.log
```

**Review and Approve:**
```bash
# Review each brief in pending_approval/
# Move approved briefs to approved/ directory
# Stage 4 auto-publishes within 60 seconds
```

---

## Key Decision Points

### Entity Brief: CREATE vs UPDATE

**The pipeline automatically decides:**

- **CREATE** new brief IF:
  - Entity has no existing brief in `briefs/entity/`
  - First time entity discovered

- **UPDATE** existing brief IF:
  - Brief exists AND new sources contain significant information
  - "Significant" = new quotes, connections, timeline events, status changes

- **SKIP** update IF:
  - New sources contain redundant information
  - No material changes to entity's profile

**Reference:** SOP-003 Section 2 for complete logic

### Connection Brief: CREATE vs UPDATE

**The pipeline automatically decides:**

- **CREATE** new brief IF:
  - Co-mention count ≥ 2
  - At least one high-relevance context (score ≥ 0.7)
  - No existing brief in `briefs/connections/`

- **UPDATE** existing brief IF:
  - New context snippets with relevance ≥ 0.5
  - New sources document the relationship

- **SKIP** IF:
  - Co-mentions < 2 (insufficient evidence)
  - Only low-relevance contexts (coincidental mentions)

**Reference:** SOP-003 Section 4 for complete logic

### Legal Auto-Approval

**18-Point Compliance Checklist:**

All briefs automatically reviewed against:
1. Source attribution
2. No speculation
3. No defamation
4. Neutral tone
5. No private facts
6. No intrusion
7. Context provided
8. No misrepresentation
9. Public interest
10. No financial harm
11. Verifiable claims
12. No emotional distress
13. Proper disclaimers
14. No criminal allegations
15. Privacy balance
16. No confidential info
17. Fair representation
18. Corrections noted

**Auto-approved IF:** All 18 points pass
**Flagged IF:** Any point fails (human review required)

**Reference:** SOP-003 Section 6.3 for detailed checklist

---

## Human Responsibilities

### You MUST Do:

1. **Upload Source Documents** to Paperless-ngx
   - Pipeline handles all subsequent processing

2. **Review Briefs** in `pending_approval/`
   - Read `REVIEW_LOG.md` first
   - Check accuracy and quality
   - Verify legal compliance
   - Move approved items to `approved/`

### You DO NOT Need To:

- Extract entities manually (Stage 1 automated)
- Find connections manually (Stage 2 automated)
- Write briefs manually (Stage 3 automated)
- Update website manually (Stage 4 automated)
- Track sources manually (all indexed)
- Run legal checks manually (automated with human oversight)

---

## Common Scenarios

### Scenario 1: New Document Uploaded

**What Happens:**
1. You upload PDF to Paperless → Webhook fires → Stage 1 runs
2. Entities extracted → entity_registry.json updated → Stage 2 runs
3. Contexts extracted → connection_contexts.json updated → Stage 3 runs
4. Briefs generated → Moved to pending_approval/ → You review
5. You approve → Move to approved/ → Stage 4 runs
6. Website updated automatically

**Your Action:** Review and approve briefs (Step 4)

### Scenario 2: Brief Has Legal Issues

**What Happens:**
1. Legal-auditor finds issues (e.g., missing source attribution)
2. Brief metadata shows `legal_review: "ISSUES FOUND"`
3. Specific issues listed in metadata
4. Brief still sent to pending_approval/ for human decision

**Your Action:**
- Read listed issues in brief metadata
- Fix the problems (edit brief)
- Update metadata to `legal_review: "MANUAL_APPROVAL"`
- Document your approval decision
- Move to approved/

**Reference:** RUNBOOK.md "Handling Briefs with Legal Issues"

### Scenario 3: Duplicate Entity Detected

**What Happens:**
1. "John Doe" and "J. Doe" extracted as separate entities
2. Pipeline may flag as potential duplicate in logs

**Your Action:**
- Review both entity briefs
- Determine if they are the same person
- If same: Use merge script to consolidate
  ```bash
  python scripts/merge_entities.py --primary "John Doe" --aliases "J. Doe"
  ```
- Pipeline will rebuild affected briefs

**Reference:** RUNBOOK.md "Duplicate Entities"

---

## Error Handling Philosophy

**Graceful Degradation:**
- Stages continue even if individual items fail
- Errors logged but don't halt pipeline
- Failed items can be retried

**Recovery Over Prevention:**
- Extensive backup systems
- All data recoverable
- Manual override available for all automated decisions

**Human Final Authority:**
- Automated decisions can be overridden
- Legal auto-approval can be manually reviewed
- Pipeline suggestions can be rejected

---

## Performance Expectations

### Processing Times (Target SLAs)

- **Stage 1:** < 2 minutes per document
- **Stage 2:** < 5 minutes per 10 entities
- **Stage 3:** < 10 minutes per brief
- **Stage 4:** < 1 minute per brief

**Total Pipeline:** Document upload → Published brief in < 30 minutes (automatic stages only)

### Quality Metrics

- **Entity Extraction Confidence:** > 0.8 average
- **Legal Auto-Approval Rate:** > 80% of briefs
- **Source Coverage:** > 95% of sources successfully processed
- **Brief Update Relevance:** > 75% of updates contain significant new information

---

## Troubleshooting Quick Reference

| Symptom | Likely Cause | Quick Fix | SOP Reference |
|---------|--------------|-----------|---------------|
| No briefs in pending_approval/ | Stage 3 errors | Check logs, re-run Stage 3 | RUNBOOK "Briefs Not Appearing" |
| All briefs fail legal review | Checklist too strict | Review criteria, manual approve | SOP-003 Section 6.3 |
| Duplicate entities | Name variations | Merge entities script | RUNBOOK "Duplicate Entities" |
| Pipeline not processing | Halt signal exists | Remove PIPELINE_HALTED file | RUNBOOK "Pipeline Status Check" |
| Publication failing | Permission errors | Check website/ permissions | SOP-004 Section 9 |
| Missing sources | Mirror incomplete | Re-mirror from Paperless | RUNBOOK "Missing Source Files" |

**Full troubleshooting:** See RUNBOOK.md Section "Troubleshooting"

---

## Maintenance Schedule

### Daily
- Check pending_approval/ for briefs
- Review error logs
- Approve briefs

### Weekly
- Archive old logs
- Validate data integrity
- Check for duplicates
- Review legal compliance patterns

### Monthly
- Full system backup
- Performance metrics analysis
- Content quality audit
- Clean old archives

**Full schedule:** See RUNBOOK.md Section "Maintenance Tasks"

---

## Emergency Procedures

### Emergency Shutdown
```bash
touch \\192.168.1.139\continuum\PIPELINE_HALTED
pkill -f run_stage
```

### Emergency Backup
```bash
python scripts/full_backup.py
```

### Emergency Content Removal
```bash
python scripts/emergency_remove.py --entity "entity_id" --reason "Legal takedown"
```

**Full procedures:** See RUNBOOK.md Section "Emergency Procedures"

---

## Document Versioning

### SOP Version History

**Version 1.0 (2025-12-25):**
- Initial production release
- Complete 4-stage pipeline documentation
- Legal compliance integration
- CREATE/UPDATE decision logic
- Comprehensive error handling

### Planned Updates

- **v1.1:** Additional entity types (FINANCIAL_INSTRUMENT, REGULATION)
- **v1.2:** Enhanced relationship classification
- **v1.3:** Performance optimization guidelines

---

## Support & Contact

### Resources

1. **This SOP Suite** - Complete operational documentation
2. **RUNBOOK.md** - Daily operations quick reference
3. **Error Logs** - `\\192.168.1.139\continuum\logs\`
4. **Backup Systems** - `\\192.168.1.139\continuum\backups\`

### Getting Help

1. **Check RUNBOOK.md first** - Most common issues covered
2. **Review relevant SOP** - Detailed procedures for each stage
3. **Check error logs** - Specific error details and context
4. **Create incident report** - For critical issues

### Feedback

Help improve these SOPs:
- Report unclear procedures
- Suggest additional scenarios
- Document edge cases
- Share best practices

**Submit to:** Pipeline Administrator

---

## License & Ownership

**Owner:** The Continuum Report
**Classification:** Internal Operations
**Distribution:** Operational team, authorized agents
**Confidentiality:** Internal use only

---

## Appendix: File Sizes & Statistics

### SOP Documents

| Document | Size | Lines | Content Type |
|----------|------|-------|--------------|
| SOP-000-master-pipeline.md | 21 KB | 650+ | Architecture overview |
| SOP-001-source-ingestion.md | 23 KB | 700+ | Entity extraction |
| SOP-002-context-extraction.md | 30 KB | 950+ | Context analysis |
| SOP-003-brief-generation.md | 44 KB | 1400+ | Brief creation |
| SOP-004-publication.md | 35 KB | 1100+ | Website publishing |
| RUNBOOK.md | 21 KB | 700+ | Operations reference |
| **Total** | **174 KB** | **5500+** | **Complete suite** |

### Coverage

- **Pipeline Stages:** 4 fully documented
- **Decision Points:** 12+ with complete logic
- **Error Scenarios:** 20+ with resolution procedures
- **Code Examples:** 100+ bash/python snippets
- **Schemas:** 8 JSON schemas defined
- **Quick References:** 15+ tables and diagrams

---

**Document Control**
- **Version:** 1.0
- **Created:** 2025-12-25
- **Last Updated:** 2025-12-25
- **Next Review:** 2026-01-25
- **Change Authority:** Pipeline Administrator
- **Status:** Production Ready

---

*End of SOP Suite Documentation*
