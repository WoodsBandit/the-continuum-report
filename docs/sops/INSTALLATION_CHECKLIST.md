# SOP Suite Installation Checklist

**Version:** 1.0
**Date:** 2025-12-25

Use this checklist to verify the SOP suite is properly installed and the pipeline is ready for operation.

---

## 1. SOP Documents

Check that all SOP files exist and are readable:

- [ ] `SOP-000-master-pipeline.md` (21 KB)
- [ ] `SOP-001-source-ingestion.md` (23 KB)
- [ ] `SOP-002-context-extraction.md` (30 KB)
- [ ] `SOP-003-brief-generation.md` (44 KB)
- [ ] `SOP-004-publication.md` (35 KB)
- [ ] `RUNBOOK.md` (21 KB)
- [ ] `README.md` (overview)
- [ ] `INSTALLATION_CHECKLIST.md` (this file)

**Verify:**
```bash
ls -lh docs/sops/
```

---

## 2. Directory Structure

Check that all required directories exist:

### Workflow Directories
- [ ] `pending_approval/`
- [ ] `pending_approval/entities/`
- [ ] `pending_approval/connections/`
- [ ] `approved/`
- [ ] `approved/entities/`
- [ ] `approved/connections/`

### Archive Directories
- [ ] `archive/`
- [ ] `archive/published/`

---

## 3. Index Files

Check that index files exist with proper schemas:

- [ ] `indexes/processed_sources.json`
- [ ] `indexes/connection_contexts.json`
- [ ] `indexes/entity_registry.json` (pre-existing)
- [ ] `indexes/source_mentions.json` (pre-existing)
- [ ] `indexes/co_occurrence.json` (pre-existing)

**Verify:**
```bash
ls -lh indexes/
python -m json.tool indexes/processed_sources.json
```

---

## 4. Supporting Files

- [ ] `pending_approval/REVIEW_LOG.md` (template)
- [ ] `templates/entity-brief-template.md`
- [ ] `templates/connection-brief-template.md`

---

## 5. Permissions

Verify Claude Code has necessary permissions:

- [ ] Read/Write access to `indexes/`
- [ ] Read access to `sources/`
- [ ] Write access to `briefs/`
- [ ] Write access to `pending_approval/`
- [ ] Read access to `approved/`
- [ ] Write access to `website/`
- [ ] Write access to `archive/`

---

## 6. Installation Complete

When all checkboxes are marked, the SOP suite is ready for use.

**Next Steps:**
1. Read SOP-000 (Master Pipeline)
2. Review RUNBOOK.md for daily operations
3. Test approval workflow with sample document

---

**Installation Checklist Version:** 1.0
**Status:** Ready for Use
