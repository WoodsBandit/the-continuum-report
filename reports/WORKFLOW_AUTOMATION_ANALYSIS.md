# Workflow Automation Analysis: The Continuum Report

**Date:** 2025-12-24
**Analyst:** Claude Opus 4.5 (Temporal Workflow Specialist)
**Scope:** Automated document processing and website publishing capabilities

---

## Executive Summary

The Continuum Report project has established foundational automation components but relies heavily on manual orchestration. The current system includes:

- **brief_watcher.py**: Polling-based daemon that triggers Claude Code for graph updates
- **continuum_pipeline.py**: Document-to-dossier generation via Ollama/Mistral
- **entity_discovery.py**: Batch entity extraction with checkpointing
- **parse_brief.py / build_graph.py**: Brief-to-JSON knowledge graph pipeline

**Key Finding:** The automation components exist in isolation without unified orchestration. Critical gaps include missing event-driven triggers, no CI/CD for website deployment, and manual steps between document ingestion and web publication.

---

## Table of Contents

1. [Current Automation Analysis](#1-current-automation-analysis)
2. [Document Processing Workflow](#2-document-processing-workflow)
3. [Website Publishing Workflow](#3-website-publishing-workflow)
4. [Workflow Gaps](#4-workflow-gaps)
5. [Recommendations](#5-recommendations)
6. [Implementation Roadmap](#6-implementation-roadmap)

---

## 1. Current Automation Analysis

### 1.1 brief_watcher.py

**Location:** `T:/scripts/brief_watcher.py`

**Purpose:** File system watcher that monitors `/mnt/user/continuum/briefs/` for new markdown files and triggers Claude Code to update the knowledge graph.

**Implementation Details:**
```
- Polling interval: 5 seconds
- Trigger mechanism: subprocess.run(["claude", "-p", prompt])
- Timeout: 600 seconds per invocation
- State management: In-memory set (SEEN_FILES)
- Logging: File-based to /mnt/user/continuum/logs/watcher.log
```

**Strengths:**
- Simple, no external dependencies
- Automatic trigger on new briefs
- Logging for audit trail

**Weaknesses:**
- **Polling-based** (5-second intervals) rather than event-driven
- **In-memory state** lost on restart (re-scans on boot)
- **Single-threaded** blocking execution
- **No retry logic** for failed Claude invocations
- **No health monitoring** or alerting
- **Hardcoded paths** (Linux-specific)

### 1.2 continuum_pipeline.py

**Location:** `T:/scripts/continuum_pipeline.py`

**Purpose:** Comprehensive document processing pipeline that:
1. Searches Paperless-ngx for documents matching a subject
2. Extracts entities using local Ollama/Mistral
3. Generates dossiers with source citations
4. Outputs formatted markdown reports

**Implementation Details:**
```
- Paperless URL: http://192.168.1.139:8040
- Ollama URL: http://192.168.1.139:11434
- Model: Mistral (1024 context window - memory optimized)
- Memory management: Forced GC, model unloading every 10 docs
- Delays: 10s between docs, 30s between batches of 5
- Checkpointing: JSON files in /mnt/user/continuum/checkpoints/
```

**Strengths:**
- **Checkpoint system** allows resume after interruption
- **Memory-safe design** with aggressive cleanup
- **Auto-tagging** of processed documents in Paperless
- **Source filtering** to exclude AI-generated dossiers

**Weaknesses:**
- **Memory constrained** (16GB RAM limit) requires aggressive pacing
- **Single-threaded** sequential processing
- **No distributed execution** capability
- **Local Ollama** inferior to Claude for analysis quality
- **No workflow orchestration** - runs as standalone script
- **No notification** on completion or failure

### 1.3 entity_discovery.py

**Location:** `T:/scripts/entity_discovery.py`

**Purpose:** Entity extraction pipeline designed for batch processing:
1. Fetches all documents from Paperless-ngx
2. Exports document batches for processing
3. Maintains entity database (JSON)
4. Generates dossier priority queue

**Implementation Details:**
```
- Entity database: /continuum/entity_data/entity_database.json
- Checkpoint: /continuum/entity_data/discovery_checkpoint.json
- Dossier queue: /continuum/entity_data/dossier_queue.json
- Batch size: 10 documents per batch file
- Pattern matching: Hardcoded key_people, key_orgs, key_locations lists
```

**Strengths:**
- **Primary source verification** built-in
- **Batch export** for offline processing
- **Priority queue** for dossier generation
- **Checkpoint/resume** capability

**Weaknesses:**
- **Hardcoded entity lists** - no dynamic discovery
- **Pattern matching only** - no AI-powered extraction
- **No integration** with Claude Code agent system
- **Manual command execution** required
- **Designed for Claude Desktop** integration

### 1.4 parse_brief.py / build_graph.py

**Location:** `T:/scripts/parse_brief.py`, `T:/scripts/build_graph.py`

**Purpose:** Parse analytical briefs and build knowledge graph JSON:

**parse_brief.py:**
- Extracts entity metadata from markdown structure
- Detects mentions of known entities
- Weights mentions by section (Public Record vs Editorial)
- Outputs structured JSON per entity

**build_graph.py:**
- Scans all briefs in briefs directory
- Calls parse_brief.py for each
- Calculates bidirectional connection strengths
- Generates entities.json, connections.json, manifest.json

**Implementation Details:**
```
- Known entities: 88 name variants mapping to 15 entity IDs
- Connection strength: 0-100 scale based on mutual mentions
- Section weighting: Public Record 3x, Editorial 2x, Other 1x
- Output: /continuum/data/*.json
```

**Strengths:**
- **Automatic connection detection** via cross-referencing
- **Evidence-based strength** calculation
- **Structured output** for D3.js visualization
- **Summary generation** for debugging

**Weaknesses:**
- **Static entity list** - new entities require code changes
- **No fuzzy matching** for name variations
- **Manual execution** required
- **No incremental updates** - full rebuild each time
- **No validation** of brief structure

---

## 2. Document Processing Workflow

### 2.1 Current Flow Diagram

```
                    DOCUMENT INGESTION
                          |
        +----------------+----------------+
        |                                 |
        v                                 v
   Paperless-ngx                    Direct PDF/MD
   (Auto-OCR/Index)                   Upload
        |                                 |
        +----------------+----------------+
                         |
                         v
                  Manual Selection
                  (Human Decision)
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
 entity_discovery   continuum_pipeline   Claude Agent
   (Batch Mode)      (Subject Mode)     (Interactive)
        |                |                |
        v                v                v
   Entity JSON       Dossier MD        Brief MD
        |                |                |
        +----------------+----------------+
                         |
                         v
                  Manual Integration
                  (Copy to briefs/)
                         |
                         v
                   parse_brief.py
                   build_graph.py
                         |
                         v
                  entities.json
                  connections.json
```

### 2.2 Paperless-ngx Ingestion

**Endpoint:** http://192.168.1.139:8040

**Capabilities:**
- Auto-OCR on ingestion
- Full-text search
- Tag-based organization
- REST API for queries

**Current Integration:**
- `continuum_pipeline.py` queries via API
- `entity_discovery.py` fetches full document list
- No webhook/notification for new documents

**Gap:** No event-driven trigger when new documents arrive in Paperless.

### 2.3 Entity Extraction

**Current Methods:**

1. **Pattern Matching** (entity_discovery.py):
   - Hardcoded list of ~27 key people
   - Hardcoded list of ~15 key organizations
   - Regex for case numbers
   - Fast but limited

2. **Ollama/Mistral** (continuum_pipeline.py):
   - JSON prompt for entity extraction
   - Truncates documents to 3000 chars
   - Memory-constrained operation
   - Moderate quality

3. **Claude Agent** (entity-extractor.md):
   - Spawned via Task tool
   - Full document analysis
   - High-quality extraction
   - Manual invocation only

**Gap:** No unified extraction pipeline combining all methods.

### 2.4 Brief Generation

**Current Flow:**
1. Human identifies subject for brief
2. Search documents in Paperless for subject
3. Extract relevant quotes and citations
4. Draft brief using templates from `/templates/`
5. Legal review for opinion-protection compliance
6. Save to `/briefs/entity/` or `/website/briefs/`

**Automation Level:** Low - primarily manual with Claude assistance

---

## 3. Website Publishing Workflow

### 3.1 Current Flow Diagram

```
                    CONTENT CREATION
                          |
        +----------------+----------------+
        |                                 |
        v                                 v
    Brief MD                        Source PDFs
    (Manual Write)                  (Manual Host)
        |                                 |
        v                                 v
  /briefs/entity/                   /website/sources/
  /briefs/connections/                    |
        |                                 |
        +----------------+----------------+
                         |
                         v
              Manual Script Execution
              (parse_brief, build_graph)
                         |
                         v
              /website/data/*.json
                         |
                         v
              Manual File Sync
              (rsync or copy)
                         |
                         v
              continuum-web Container
              (nginx on port 8081)
                         |
                         v
              Cloudflare Tunnel
                         |
                         v
              thecontinuumreport.com
```

### 3.2 Brief to Web Content

**Current Process:**
1. Write brief in markdown format
2. Copy to `/website/briefs/entity/` or `/website/briefs/connections/`
3. Briefs served as raw markdown (no HTML conversion)
4. `continuum.html` fetches briefs via JavaScript

**Gap:** No markdown-to-HTML conversion for standalone brief pages.

### 3.3 JSON Data Exports

**Generated Files:**
- `entities.json` - 37 entities with metadata
- `connections.json` - 131 relationships
- `manifest.json` - Processing metadata

**Generation Trigger:** Manual execution of `build_graph.py`

**Gap:** No automatic rebuild when briefs change.

### 3.4 D3.js Graph Updates

**Current Behavior:**
- `continuum.html` fetches JSON on page load
- D3.js force-directed graph renders entities
- Connections drawn based on `connections.json`

**Update Process:**
1. Modify brief markdown
2. Run `parse_brief.py` and `build_graph.py`
3. JSON files updated
4. Browser refresh shows new data

**Gap:** No cache invalidation, no WebSocket updates.

---

## 4. Workflow Gaps

### 4.1 Manual Steps That Should Be Automated

| Step | Current State | Automation Opportunity |
|------|---------------|----------------------|
| Document arrives in Paperless | No notification | Webhook trigger |
| Select documents for analysis | Human decision | Queue-based processing |
| Run entity extraction | Manual script | Event-driven pipeline |
| Write analytical brief | Manual + Claude | Templated generation |
| Legal compliance check | Manual audit | Automated validation |
| Copy brief to website | Manual file copy | Git-based deployment |
| Rebuild JSON graph | Manual script | File watcher trigger |
| Deploy to production | Container restart | CI/CD pipeline |
| Source link validation | Manual audit | Automated link checker |

### 4.2 Missing Triggers and Event Handling

**No Event Sources:**
- Paperless-ngx document ingestion
- Git commits to brief repository
- Scheduled processing tasks
- External webhook integrations

**No Event Consumers:**
- Entity extraction pipeline
- Brief generation workflow
- Graph rebuild process
- Website deployment

**No Event Infrastructure:**
- Message queue (Redis, RabbitMQ)
- Task scheduler (Celery, Temporal)
- Webhook receiver
- Event bus

### 4.3 Error Recovery Procedures

**Current State:**
- Checkpoint files for resume (continuum_pipeline, entity_discovery)
- No retry logic for API failures
- No dead letter queue for failed tasks
- No alerting on failures
- Manual intervention required

**Missing:**
- Automatic retry with exponential backoff
- Error classification (transient vs permanent)
- Compensation/rollback logic
- Health monitoring dashboard
- Failure notification system

### 4.4 Notification Systems

**Current:** None

**Needed:**
- New document alert
- Processing completion
- Error notifications
- Quality check failures
- Source link validation results

---

## 5. Recommendations

### 5.1 Event-Driven Architecture

**Recommended Stack:**
```
Paperless-ngx Webhook --> Redis Queue --> Celery Workers --> Outputs
                              |
                         Scheduler (cron)
                              |
                         Health Monitor
```

**Implementation:**

1. **Paperless Post-Consume Hook:**
   ```python
   # Configure in docker-compose.yml
   PAPERLESS_POST_CONSUME_SCRIPT=/usr/local/bin/notify_continuum.sh
   ```

2. **Redis Message Broker:**
   - Add Redis container to Unraid
   - Configure Celery to use Redis
   - Implement task queues

3. **Celery Task Definitions:**
   ```python
   @celery.task(bind=True, max_retries=3)
   def extract_entities(self, doc_id):
       # Fetch document from Paperless
       # Run entity extraction
       # Store results
       pass

   @celery.task
   def rebuild_graph():
       # Run build_graph.py
       # Invalidate caches
       pass
   ```

### 5.2 Queue-Based Processing with Celery

**Task Categories:**

1. **Entity Extraction Tasks:**
   - `extract_from_document(doc_id)`
   - `batch_extract(doc_ids[])`
   - `verify_entities(entity_ids[])`

2. **Brief Generation Tasks:**
   - `generate_brief(subject_name)`
   - `update_brief(brief_id)`
   - `validate_brief(brief_path)`

3. **Graph Update Tasks:**
   - `parse_single_brief(brief_path)`
   - `rebuild_full_graph()`
   - `update_connections(entity_id)`

4. **Deployment Tasks:**
   - `sync_website_files()`
   - `invalidate_cdn_cache()`
   - `validate_source_links()`

**Celery Configuration:**
```python
# celery_config.py
broker_url = 'redis://192.168.1.139:6379/0'
result_backend = 'redis://192.168.1.139:6379/0'

task_routes = {
    'extract_*': {'queue': 'extraction'},
    'generate_*': {'queue': 'generation'},
    'rebuild_*': {'queue': 'graph'},
    'deploy_*': {'queue': 'deployment'},
}

task_default_retry_delay = 60
task_max_retries = 3
```

### 5.3 CI/CD Pipeline for Website Deployment

**Recommended Flow:**
```
Brief Commit --> Git Hook --> Build --> Test --> Deploy
                    |
                    v
              - Parse briefs
              - Build JSON
              - Validate links
              - Run tests
                    |
                    v
              Deploy to Container
```

**GitHub Actions Workflow:**
```yaml
name: Deploy Continuum Website

on:
  push:
    paths:
      - 'briefs/**'
      - 'website/**'
  workflow_dispatch:

jobs:
  build:
    runs-on: self-hosted  # Unraid runner
    steps:
      - uses: actions/checkout@v4

      - name: Parse Briefs
        run: python scripts/build_graph.py --briefs-dir briefs --output-dir website/data

      - name: Validate Links
        run: python scripts/validate_links.py

      - name: Run Tests
        run: pytest tests/

      - name: Deploy
        run: |
          rsync -av website/ /mnt/user/continuum/website/
          docker restart continuum-web
```

### 5.4 Scheduled Automation

**Cron Jobs (systemd timers preferred):**

| Schedule | Task | Purpose |
|----------|------|---------|
| Every 5 min | brief_watcher health check | Ensure daemon running |
| Hourly | Source link validation | Detect broken links |
| Daily 2 AM | Full graph rebuild | Ensure consistency |
| Daily 3 AM | Paperless backup | Data protection |
| Weekly | Entity index update | Maintain master index |
| Weekly | Unused source cleanup | Storage management |

**Systemd Timer Example:**
```ini
# /etc/systemd/system/continuum-graph-rebuild.timer
[Unit]
Description=Rebuild Continuum Graph Daily

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

### 5.5 Webhook Integrations

**Paperless-ngx Post-Consume Webhook:**
```python
# /usr/local/bin/notify_continuum.py
import requests
import os

CELERY_WEBHOOK = "http://192.168.1.139:5000/tasks/document-ingested"

doc_id = os.environ.get('DOCUMENT_ID')
requests.post(CELERY_WEBHOOK, json={'document_id': doc_id})
```

**Webhook Receiver (Flask):**
```python
@app.route('/tasks/document-ingested', methods=['POST'])
def handle_document():
    doc_id = request.json['document_id']
    extract_entities.delay(doc_id)
    return jsonify({'status': 'queued'})
```

---

## 6. Implementation Roadmap

### Phase 1: Foundation (Week 1-2)

**Objective:** Establish event infrastructure

**Tasks:**
1. Deploy Redis container on Unraid
2. Set up Celery with Redis broker
3. Create Flask webhook receiver
4. Implement health monitoring

**Deliverables:**
- Redis running on port 6379
- Celery workers operational
- Webhook endpoint `/tasks/`
- Health check endpoint `/health`

### Phase 2: Document Pipeline (Week 3-4)

**Objective:** Automate document ingestion to extraction

**Tasks:**
1. Configure Paperless post-consume hook
2. Implement `extract_entities` Celery task
3. Add retry logic and error handling
4. Create extraction queue monitoring

**Deliverables:**
- Automatic entity extraction on new documents
- Processing status dashboard
- Error notification via Discord/email

### Phase 3: Brief Generation (Week 5-6)

**Objective:** Semi-automated brief generation

**Tasks:**
1. Implement brief template system
2. Create `generate_brief` Celery task
3. Add legal compliance validation
4. Build brief queue and approval workflow

**Deliverables:**
- Draft brief generation from entity data
- Compliance check automation
- Approval queue interface

### Phase 4: Website Deployment (Week 7-8)

**Objective:** CI/CD for website updates

**Tasks:**
1. Set up Git repository for briefs
2. Configure GitHub Actions runner on Unraid
3. Implement deployment pipeline
4. Add cache invalidation

**Deliverables:**
- Git-based brief management
- Automatic deployment on commit
- Link validation in pipeline

### Phase 5: Integration (Week 9-10)

**Objective:** End-to-end automation

**Tasks:**
1. Connect all pipeline stages
2. Implement notification system
3. Build monitoring dashboard
4. Document operations runbook

**Deliverables:**
- Full automation: Document --> Website
- Monitoring and alerting
- Operational documentation

---

## Appendix A: Technology Recommendations

### Recommended Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Message Broker | Redis | Task queue, caching |
| Task Queue | Celery | Distributed tasks |
| Webhook Receiver | Flask | HTTP endpoint |
| Scheduler | Celery Beat | Periodic tasks |
| CI/CD | GitHub Actions | Deployment |
| Monitoring | Prometheus + Grafana | Metrics |
| Alerting | Discord Webhooks | Notifications |
| Workflow Engine | Temporal (future) | Complex orchestration |

### Container Architecture

```
Unraid Stack:
├── paperless-ngx (8040)
├── redis (6379)
├── celery-worker (no port)
├── celery-beat (no port)
├── flask-webhooks (5000)
├── continuum-web (8081)
├── cloudflared-tunnel
└── monitoring (9090, 3000)
```

---

## Appendix B: Temporal Workflow Alternative

For complex, long-running workflows with saga patterns, consider **Temporal** as the orchestration engine:

**Advantages:**
- Durable workflow execution
- Automatic state persistence
- Built-in retry and timeout handling
- Time-travel debugging
- Activity separation for external calls

**Example Workflow:**
```python
@workflow.defn
class DocumentToWebsiteWorkflow:
    @workflow.run
    async def run(self, doc_id: str) -> str:
        # Activity 1: Extract from Paperless
        doc = await workflow.execute_activity(
            fetch_document,
            doc_id,
            start_to_close_timeout=timedelta(minutes=5)
        )

        # Activity 2: Entity extraction
        entities = await workflow.execute_activity(
            extract_entities,
            doc,
            start_to_close_timeout=timedelta(minutes=30)
        )

        # Activity 3: Brief generation
        brief = await workflow.execute_activity(
            generate_brief,
            entities,
            start_to_close_timeout=timedelta(hours=1)
        )

        # Activity 4: Legal validation
        validated = await workflow.execute_activity(
            validate_compliance,
            brief,
            start_to_close_timeout=timedelta(minutes=10)
        )

        # Activity 5: Deploy to website
        result = await workflow.execute_activity(
            deploy_brief,
            validated,
            start_to_close_timeout=timedelta(minutes=5)
        )

        return result
```

**Recommendation:** Start with Celery for simpler queue-based processing. Migrate to Temporal when workflow complexity increases (multi-step sagas, compensation, long-running processes).

---

## Appendix C: Quick Wins

Immediate improvements requiring minimal effort:

1. **Add systemd service for brief_watcher.py**
   - Ensures daemon survives reboots
   - Automatic restart on failure

2. **Add file watcher trigger for build_graph.py**
   - Modify brief_watcher.py to also trigger graph rebuild
   - Reduces manual steps

3. **Add Discord webhook for notifications**
   - Simple HTTP POST for alerts
   - Immediate visibility into processing

4. **Add cron job for source link validation**
   - Weekly scan for broken links
   - Email report of failures

5. **Convert markdown briefs to HTML**
   - Use pandoc for conversion
   - Enables standalone brief URLs

---

*Generated: 2025-12-24*
*The Continuum Report - Another Node in the Decentralized Intelligence Agency*
