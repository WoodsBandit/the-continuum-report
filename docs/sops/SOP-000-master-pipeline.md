# SOP-000: Master Pipeline Overview

**Document Version:** 1.0
**Last Updated:** 2025-12-25
**Owner:** The Continuum Report
**Classification:** Internal Operations

---

## Purpose

This document provides a comprehensive overview of The Continuum Report's autonomous intelligence pipeline, detailing how the four operational stages connect, where human intervention occurs, and how data flows through the system.

## Pipeline Philosophy

The Continuum Report operates on a **minimal human intervention** model. The pipeline is designed to:
- Autonomously extract, analyze, and synthesize intelligence
- Maintain comprehensive entity tracking across ALL sources
- Create and UPDATE analytical products based on new information
- Self-regulate through automated legal compliance checks
- Only require human oversight at two critical control points

## Human Touchpoints (ONLY 2)

### Touchpoint 1: Source Document Upload
**Location:** Paperless-ngx document management system
**Action:** User uploads source PDF/document to Paperless
**Frequency:** As needed (ad-hoc)
**Result:** Webhook triggers pipeline execution

### Touchpoint 2: Analytical Product Approval
**Location:** `\\192.168.1.139\continuum\pending_approval\`
**Action:** User reviews briefs and moves approved items to `\\192.168.1.139\continuum\approved\`
**Frequency:** Periodic review sessions
**Result:** Publication process triggered

**NO OTHER HUMAN INTERVENTION IS REQUIRED OR EXPECTED**

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    HUMAN TOUCHPOINT #1                          │
│              Upload Document to Paperless-ngx                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 1: SOURCE INGESTION (SOP-001)                            │
│  Trigger: Paperless webhook                                     │
│  Actions:                                                        │
│    - Extract ALL entities (new + known)                         │
│    - Update entity_registry.json                                │
│    - Update source_mentions.json                                │
│    - Update processed_sources.json                              │
│  Output: Updated entity indexes                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 2: CONTEXT EXTRACTION (SOP-002)                          │
│  Trigger: Change to entity_registry.json                        │
│  Actions:                                                        │
│    - Read context windows around entity mentions                │
│    - Identify co-occurring entities                             │
│    - Extract relationship signals                               │
│    - Update connection_contexts.json                            │
│    - Update co_occurrence.json                                  │
│  Output: Updated connection indexes                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 3: BRIEF GENERATION (SOP-003)                            │
│  Trigger: Change to connection_contexts.json                    │
│  Actions:                                                        │
│    - Check for existing entity briefs (UPDATE vs CREATE)        │
│    - Check for existing connection briefs (UPDATE vs CREATE)    │
│    - Run legal-auditor agent (auto-compliance check)            │
│    - Generate/update analytical products                        │
│    - Place output in pending_approval/                          │
│  Output: New/updated briefs awaiting approval                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    HUMAN TOUCHPOINT #2                          │
│           Review pending_approval/ and Move to approved/        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 4: PUBLICATION (SOP-004)                                 │
│  Trigger: Files detected in approved/                           │
│  Actions:                                                        │
│    - Parse metadata from approved briefs                        │
│    - Update website/data/entities.json                          │
│    - Update website/data/connections.json                       │
│    - Copy briefs to website/briefs/                             │
│    - Copy source PDFs to website/sources/                       │
│    - Update continuum.html data references                      │
│    - Archive published briefs                                   │
│  Output: Published website, archived records                    │
└─────────────────────────────────────────────────────────────────┘
```

## Stage Dependencies

### Sequential Execution
Stages MUST execute in order:
1. **Stage 1 → Stage 2:** Entity registry changes trigger context extraction
2. **Stage 2 → Stage 3:** Context updates trigger brief generation
3. **Stage 3 → Human Review:** Briefs require approval before publication
4. **Human Approval → Stage 4:** Approved items trigger publication

### Trigger Mechanisms

| Stage | Trigger Type | Detection Method |
|-------|-------------|------------------|
| Stage 1 | Webhook | Paperless POST to endpoint |
| Stage 2 | File Change | Monitor `entity_registry.json` modification timestamp |
| Stage 3 | File Change | Monitor `connection_contexts.json` modification timestamp |
| Stage 4 | Directory Watch | Detect files in `approved/` directories |

## Data Flow

### Entity Tracking
```
Source Document → entity_registry.json → analytical_brief_{entity}.md
                ↓
           source_mentions.json
```

### Connection Discovery
```
Source Document → co_occurrence.json → connection_contexts.json → {entity1}_{entity2}.md
```

### Publication Pipeline
```
pending_approval/ → [Human Review] → approved/ → website/ → archive/published/
```

## Directory Structure

```
\\192.168.1.139\continuum\
├── pending_approval/           # Stage 3 output - awaiting human review
│   ├── entities/              # New/updated entity briefs
│   ├── connections/           # New/updated connection briefs
│   └── REVIEW_LOG.md          # What changed and why (auto-generated)
│
├── approved/                   # Human-approved briefs ready for publication
│   ├── entities/
│   └── connections/
│
├── archive/
│   └── published/             # Published briefs with timestamps
│       ├── entities/
│       └── connections/
│
├── sops/                       # Standard Operating Procedures
│   ├── SOP-000-master-pipeline.md    (this document)
│   ├── SOP-001-source-ingestion.md
│   ├── SOP-002-context-extraction.md
│   ├── SOP-003-brief-generation.md
│   ├── SOP-004-publication.md
│   └── RUNBOOK.md             # Quick reference for operators
│
├── indexes/                    # JSON indexes tracking pipeline state
│   ├── entity_registry.json
│   ├── source_mentions.json
│   ├── co_occurrence.json
│   ├── processed_sources.json
│   └── connection_contexts.json
│
├── briefs/                     # Current analytical products
│   ├── entity/
│   └── connections/
│
├── templates/                  # Brief generation templates
│   ├── entity-brief-template.md
│   └── connection-brief-template.md
│
├── website/                    # Publication destination
│   ├── data/
│   │   ├── entities.json
│   │   └── connections.json
│   ├── briefs/
│   └── sources/
│
└── sources/                    # Original source documents
    └── paperless_mirror/
```

## Critical Decision Logic

### Entity Brief: CREATE vs UPDATE

```
DECISION POINT: When entity appears in new source

READ: \\192.168.1.139\continuum\briefs\entity\analytical_brief_{entity}.md

IF file does NOT exist:
    → CREATE new brief using entity-brief-template.md
    → Analyze ALL sources mentioning entity
    → Output to pending_approval/entities/
    → REASON: "New entity discovered"

ELSE IF file exists:
    READ existing brief
    COMPARE: Sources in brief vs sources in source_mentions.json

    IF new sources exist:
        ASSESS new information:
        - New quotes/statements
        - New connections/associations
        - New timeline events
        - Changed status/role
        - Contradictory information

        IF significant new information found:
            → UPDATE existing brief
            → Integrate new sources
            → Preserve existing analysis
            → Output to pending_approval/entities/
            → REASON: "New source material: [source_id]"

        ELSE:
            → LOG: "Entity {entity} mentioned in {source_id}, no significant new info"
            → NO brief generation

    ELSE:
        → LOG: "Entity {entity} already fully covered by existing brief"
        → NO action needed
```

### Connection Brief: CREATE vs UPDATE

```
DECISION POINT: When entity pair co-occurs

READ: \\192.168.1.139\continuum\indexes\co_occurrence.json
GET: co_mention_count for entity_pair

IF co_mention_count < 2:
    → LOG: "Insufficient co-mentions for connection brief"
    → NO brief generation

ELSE:
    READ: \\192.168.1.139\continuum\briefs\connections\{entity1}_{entity2}.md

    IF file does NOT exist:
        CHECK: connection_contexts.json for context snippets

        IF context_snippets exist AND are substantive:
            → CREATE new connection brief
            → Output to pending_approval/connections/
            → REASON: "New connection discovered: {count} co-mentions"

        ELSE:
            → LOG: "Co-mentions exist but lack substantive context"
            → NO brief generation

    ELSE IF file exists:
        READ existing brief
        COMPARE: Context snippets in brief vs connection_contexts.json

        IF new context snippets exist:
            ASSESS new information:
            - New interaction evidence
            - Timeline updates
            - Relationship changes
            - Transaction details

            IF significant new context:
                → UPDATE existing brief
                → Add new evidence
                → Output to pending_approval/connections/
                → REASON: "New context from source: [source_id]"

            ELSE:
                → LOG: "New context for {entity1}-{entity2} is redundant"
                → NO brief generation
```

### Legal Auto-Approval

```
FOR EACH generated/updated brief:

RUN: legal-auditor agent with compliance checklist

EVALUATE 18-point checklist:
[See SOP-003 for full checklist]

IF all points PASS:
    ADD to brief frontmatter:
    ---
    legal_review: "AUTO-APPROVED"
    review_date: "{timestamp}"
    reviewer: "legal-auditor-agent"
    ---

    PROCEED to pending_approval/
    NOTE: Human review still required for editorial approval

ELSE IF any point FAILS:
    ADD to brief frontmatter:
    ---
    legal_review: "ISSUES FOUND"
    review_date: "{timestamp}"
    reviewer: "legal-auditor-agent"
    issues:
      - "{specific issue 1}"
      - "{specific issue 2}"
    ---

    PROCEED to pending_approval/
    NOTE: Human MUST address legal issues before approving
```

## Quality Control Gates

### Gate 1: Entity Extraction Validation (Stage 1)
- Minimum entity confidence threshold: 0.7
- Require explicit mention in source text (no inference)
- Validate entity type classification
- Cross-reference against existing entity_registry

### Gate 2: Context Relevance (Stage 2)
- Context window must contain both entities
- Context must indicate interaction/relationship
- Filter out coincidental co-mentions (e.g., both in author list)

### Gate 3: Legal Compliance (Stage 3)
- All 18 legal checklist points must pass for auto-approval
- Flagged issues require human review
- No publication without legal clearance

### Gate 4: Publication Integrity (Stage 4)
- Verify metadata completeness
- Validate JSON schema compliance
- Ensure source PDF availability
- Confirm no data corruption

## Error Handling Strategy

### Recoverable Errors
- **Missing source file:** Log warning, skip processing, continue
- **Malformed JSON:** Restore from backup, retry operation
- **Webhook timeout:** Queue for retry (max 3 attempts)
- **Legal check failure:** Flag for human review, continue pipeline

### Critical Errors (Pipeline Halt)
- **Index corruption:** Restore from backup, manual verification required
- **Permission denied:** Alert operator, halt affected stage
- **Disk full:** Alert operator, halt all stages
- **Database unavailable:** Queue operations, retry until restored

### Error Logging
All errors logged to: `\\192.168.1.139\continuum\logs\pipeline_errors.log`

Format:
```
{timestamp} | {stage} | {severity} | {error_type} | {details} | {action_taken}
```

## Performance Metrics

### Target SLAs
- **Stage 1 (Ingestion):** < 2 minutes per document
- **Stage 2 (Context Extraction):** < 5 minutes per 10 entities
- **Stage 3 (Brief Generation):** < 10 minutes per brief
- **Stage 4 (Publication):** < 1 minute per brief

### Monitoring Points
- Queue depth at each stage
- Processing time per document
- Error rate by stage
- Brief approval rate
- Time from ingestion to publication

## Operational Procedures

### Daily Operations
1. Monitor `pending_approval/` for briefs requiring review
2. Review `REVIEW_LOG.md` for change summaries
3. Approve or reject briefs (move to `approved/` or back to `briefs/` with notes)
4. Check error logs for any pipeline issues

### Weekly Maintenance
1. Review entity_registry for duplicate/conflicting entries
2. Audit connection briefs for quality
3. Validate source file integrity
4. Archive old logs

### Monthly Review
1. Analyze pipeline performance metrics
2. Review legal compliance patterns
3. Update templates based on feedback
4. Optimize index structures if needed

## Integration Points

### Paperless-ngx Webhook Configuration
**Endpoint:** `http://{server}/api/continuum/ingest`
**Trigger:** Document consumed event
**Payload:**
```json
{
  "document_id": 12345,
  "title": "Document Title",
  "created": "2025-12-25T10:00:00Z",
  "file_path": "/path/to/document.pdf",
  "tags": ["intelligence", "source"]
}
```

### Legal-Auditor Agent Integration
**Invocation:** Claude Code tool call within Stage 3
**Input:** Brief markdown content
**Output:** Compliance assessment with pass/fail per checklist item

### Website Update Integration
**Mechanism:** Direct file system operations in Stage 4
**Target:** `\\192.168.1.139\continuum\website\`
**Validation:** JSON schema validation before writing

## Backup and Recovery

### Automated Backups
**Frequency:** Every 6 hours
**Scope:**
- All JSON indexes
- All briefs (entity + connection)
- Configuration files

**Location:** `\\192.168.1.139\continuum\backups\{timestamp}\`

### Recovery Procedures
**Index Corruption:**
1. Stop all pipeline stages
2. Restore latest valid backup from `backups/`
3. Verify integrity with validation script
4. Resume pipeline operations

**Brief Conflicts:**
1. Compare versions in `pending_approval/` vs `briefs/`
2. Identify conflicting changes
3. Manual merge if necessary
4. Document resolution in REVIEW_LOG.md

## Version Control

All SOP documents versioned and tracked:
- **Major version change:** Fundamental process redesign
- **Minor version change:** New steps or decision logic
- **Patch version change:** Clarifications or corrections

Current SOP versions:
- SOP-000: v1.0
- SOP-001: v1.0
- SOP-002: v1.0
- SOP-003: v1.0
- SOP-004: v1.0

## Appendices

### Appendix A: File Path Reference
All absolute paths use network share: `\\192.168.1.139\continuum\`

### Appendix B: JSON Schema References
See individual index files for embedded `_schema_version` fields

### Appendix C: Template Locations
- Entity brief template: `\\192.168.1.139\continuum\templates\entity-brief-template.md`
- Connection brief template: `\\192.168.1.139\continuum\templates\connection-brief-template.md`

### Appendix D: Related Documentation
- Legal compliance checklist: See SOP-003 Section 6.3
- Webhook configuration guide: See Paperless-ngx admin docs
- Agent invocation patterns: See RUNBOOK.md

---

**Document Control**
- **Next Review Date:** 2026-03-25
- **Change Authority:** Pipeline Administrator
- **Distribution:** Operational team, Claude Code agents
