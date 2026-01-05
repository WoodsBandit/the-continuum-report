# SESSION 7: Autonomous Pipeline Completion

**Created:** 2025-12-26
**Priority:** HIGH
**Estimated Phases:** 3 (parallel execution)

---

## Mission

Complete the autonomous document processing pipeline that triggers Claude when documents are uploaded to Paperless-ngx. The infrastructure is 90% built — this session finishes integration and runs first end-to-end test.

---

## Current State

### What's Done (Session 6)
- ✅ `invoke_claude.py` — Claude CLI wrapper via docker exec (FIXED: added missing `os` import)
- ✅ `webhook_listener.py` — Flask endpoint for Paperless triggers (port 5000)
- ✅ `run_stage1.py` — Entity extraction with Claude
- ✅ `run_stage2.py` — Context extraction, co-occurrence analysis
- ✅ `run_stage3.py` — Brief generation with legal compliance
- ✅ `run_stage4.py` — Publication to website
- ✅ `pipeline_watcher.py` — File system watchers
- ✅ `pipeline_daemon.py` — Master orchestrator
- ✅ All SOPs (SOP-000 through SOP-004, RUNBOOK)
- ✅ All index files exist in `/continuum/indexes/`
- ✅ `paperless_post_consume.sh` — Created but needs chmod +x

### What's Left
- [ ] Make post-consume script executable
- [ ] Configure Paperless container with PAPERLESS_POST_CONSUME_SCRIPT
- [ ] Verify webhook listener is running on Tower
- [ ] Verify Claude Code container is accessible
- [ ] Test end-to-end with document upload
- [ ] Update entities.json and connections.json from pipeline output
- [ ] Verify continuum.html updates automatically

### New Hardware
- **GTX 1060 6GB** installed in Tower
- Driver 580.82.09, CUDA 13.0 ready
- Available for GPU-accelerated OCR (future: DOJ 33k files)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  TOWER (192.168.1.139) - Unraid Server                      │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │  paperless-ngx  │───▶│ post_consume.sh │                │
│  │  (port 8040)    │    │ calls webhook   │                │
│  └─────────────────┘    └────────┬────────┘                │
│                                  │                          │
│                                  ▼                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  continuum-python container                          │   │
│  │  - webhook_listener.py (port 5000)                  │   │
│  │  - Writes to ingestion_queue.json                   │   │
│  │  - Docker socket access for Claude invocation       │   │
│  └──────────────────────────┬──────────────────────────┘   │
│                             │ docker exec                   │
│                             ▼                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  claude-code container                              │   │
│  │  - Claude Code CLI                                  │   │
│  │  - --dangerously-skip-permissions --print mode      │   │
│  │  - /continuum mounted                               │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Execution Plan

**Mode:** SEQUENTIAL — Complete each phase before starting next.
**Logging:** Update log.md after EVERY phase completion.

---

### PHASE 1: Infrastructure Verification

Run these checks in sequence:

**Agent 1: Container Health Check**
```
Check Docker containers on Tower:
1. Verify continuum-python is running with docker socket mounted
2. Verify claude-code container exists and is accessible
3. Verify paperless-ngx is running on port 8040
4. Test: docker exec claude-code claude --version
5. Report container status
```

**Agent 2: Webhook Endpoint Test**
```
Test the webhook infrastructure:
1. curl http://192.168.1.139:5000/health
2. curl http://192.168.1.139:5000/api/continuum/status
3. Send test payload to /api/continuum/ingest
4. Verify ingestion_queue.json is updated
5. Report endpoint status
```

**Agent 3: Paperless Configuration**
```
Configure Paperless post-consume:
1. chmod +x /continuum/scripts/paperless_post_consume.sh
2. Verify script syntax with bash -n
3. Document how to set PAPERLESS_POST_CONSUME_SCRIPT
4. Check if Paperless needs container restart
5. Report configuration steps
```

**After Phase 1:** Update `/continuum/log.md` with infrastructure status.

---

### PHASE 2: Integration Test (Sequential)

**Agent 4: End-to-End Test**
```
Run complete pipeline test:
1. Upload a test document to Paperless (or use existing doc)
2. Trigger: python run_stage1.py --document-id <ID> --dry-run
3. If dry-run succeeds, run without --dry-run
4. Monitor entity_registry.json for updates
5. Check Claude output for extracted entities
6. Report extraction results
```

**After Phase 2:** Update `/continuum/log.md` with test results.

---

### PHASE 3: Data Integration (Parallel)

Launch 2 agents simultaneously:

**Agent 5: Entity/Connection Sync**
```
Sync extracted data to website:
1. Read entity_registry.json
2. Compare with /website/data/entities.json
3. Merge new entities following schema
4. Update connection counts
5. Regenerate entities.json
```

**Agent 6: Brief Generator**
```
Generate briefs for new entities (if any):
1. Check which entities lack briefs
2. Use brief-generator agent pattern
3. Follow legal framework (Milkovich protections)
4. Include Alternative Interpretations section
5. Output to /briefs/entity/
```

**After Phase 3:** Update `/continuum/log.md` with final status.

---

## Key Files

| File | Purpose |
|------|---------|
| `/continuum/scripts/invoke_claude.py` | Claude CLI wrapper |
| `/continuum/scripts/webhook_listener.py` | Flask webhook endpoint |
| `/continuum/scripts/run_stage1.py` | Entity extraction |
| `/continuum/scripts/paperless_post_consume.sh` | Paperless trigger script |
| `/continuum/indexes/ingestion_queue.json` | Document queue |
| `/continuum/indexes/entity_registry.json` | Extracted entities |
| `/continuum/website/data/entities.json` | Website entity data |
| `/continuum/website/data/connections.json` | Website connection data |
| `/continuum/log.md` | Session activity log |

---

## Logging Requirements

**Update log.md after each phase with:**
```markdown
### 2025-12-26 — Session 7: Pipeline Completion

**Phase X Complete:** [timestamp]
**Status:** [SUCCESS/PARTIAL/FAILED]

#### Actions Taken
- [ ] Action 1
- [ ] Action 2

#### Results
- Key finding 1
- Key finding 2

#### Issues (if any)
- Issue description

#### Next Phase
- What's next
```

---

## Agent Definitions to Use

Reference these in `/continuum/agents/`:
- `entity-extractor.md` — Document analysis patterns
- `brief-generator.md` — Brief creation with legal compliance
- `paperless-integrator.md` — Paperless API patterns
- `legal-auditor.md` — Compliance verification

---

## Success Criteria

1. ✅ Webhook endpoint responds to health check
2. ✅ Post-consume script triggers on Paperless upload
3. ✅ Claude extracts entities from document
4. ✅ entity_registry.json updates with new entities
5. ✅ entities.json syncs to website data
6. ✅ continuum.html displays new entities (no code changes needed)

---

## Quick Start Command

```
Read this task file, then execute phases in order.
Use Task tool with subagent_type for parallel work.
Update /continuum/log.md after EVERY phase.
```

---

## Notes

- Paperless API token: Check `/continuum/scripts/.env`
- Tower SSH: `ssh root@192.168.1.139`
- Webhook URL: `http://192.168.1.139:5000/api/continuum/ingest`
- If containers aren't running, check Unraid Docker tab
