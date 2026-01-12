# Session 7 Starter Prompt

**Copy and paste this to start the next Claude Code session:**

---

## PROMPT

```
Complete the autonomous pipeline per /continuum/agents/tasks/SESSION7_PIPELINE_COMPLETION.md

EXECUTION MODE: Sequential phases. Complete each phase fully before moving to next.

PHASE 1: Infrastructure Verification
1. Check containers: continuum-python, claude-code, paperless-ngx
2. Test webhook: curl http://192.168.1.139:5000/health
3. Make executable: chmod +x /continuum/scripts/paperless_post_consume.sh
4. Document Paperless config steps needed
→ UPDATE /continuum/log.md with Phase 1 results

PHASE 2: Integration Test
1. Get a document ID from Paperless
2. Run: python /continuum/scripts/run_stage1.py --document-id <ID> --dry-run
3. If success, run without --dry-run
4. Check /continuum/indexes/entity_registry.json for updates
→ UPDATE /continuum/log.md with Phase 2 results

PHASE 3: Data Sync
1. Sync entity_registry.json → /continuum/website/data/entities.json
2. Update connection counts
3. Generate briefs for any new entities (if applicable)
→ UPDATE /continuum/log.md with Phase 3 results + final session summary

Use the Task tool to spawn agents for each step. Reference agent definitions in /continuum/agents/ for patterns.

SUCCESS = Document upload to Paperless triggers Claude extraction and updates website data.
```

---

## Quick Context

- **Project:** The Continuum Report — open source intelligence analysis
- **Goal:** Autonomous doc → entity extraction → brief generation → website update
- **GPU:** GTX 1060 6GB installed (CUDA ready, for future OCR)
- **Key files:** See SESSION7_PIPELINE_COMPLETION.md for full list
- **Paperless:** http://192.168.1.139:8040
- **Webhook:** http://192.168.1.139:5000

---

## What's Already Built

| Component | Status |
|-----------|--------|
| invoke_claude.py | ✅ Ready (fixed missing import) |
| webhook_listener.py | ✅ Ready |
| run_stage1-4.py | ✅ Ready |
| SOPs 000-004 | ✅ Ready |
| post_consume.sh | ✅ Created (needs chmod) |
| Paperless config | ❌ Needs PAPERLESS_POST_CONSUME_SCRIPT |

---

## Log Update Template

After each phase, append to /continuum/log.md:

```markdown
### 2025-12-26 — Session 7: Pipeline Completion (continued)

#### Phase X: [Name]
**Completed:** [timestamp]
**Status:** SUCCESS | PARTIAL | BLOCKED

**Actions:**
- Action taken 1
- Action taken 2

**Results:**
- Finding 1
- Finding 2

**Issues:** (if any)
- Issue description

---
```
