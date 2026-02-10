# TODO — Prioritized Task List

**Last Updated:** 2026-02-09

---

## NOW (After Restart)

| Priority | Task | Notes |
|----------|------|-------|
| 1 | Start Docker services | `docker-compose -f docker-compose.woodsden.yml up -d` |
| 2 | Test Paperless OCR | Upload test PDF to data/paperless/consume/ |
| 3 | Run Cloudflare tunnel setup | `powershell docker/setup-cloudflare-tunnel.ps1` |
| 4 | Verify website loads | http://localhost:8081 |

---

## NEXT (After Infrastructure)

| Priority | Task | Notes |
|----------|------|-------|
| 1 | Test BNIS pipeline | `python bnis/run_bnis.py --dry-run` |
| 2 | Test narrative generation | `python bnis/scripts/narrative_generator.py --dry-run` |
| 3 | Set up RSSHub locally | For Twitter monitoring (optional) |
| 4 | Git commit all changes | Push restructure to GitHub |

---

## CONTENT PRIORITIES

| Priority | Task | Source |
|----------|------|--------|
| 1 | Update Wexner brief with FBI co-conspirator designation | FBI Theme research |
| 2 | Connection Brief Overseer Phase 2 | 88 briefs remaining |
| 3 | DOJ 33k OCR processing | 33,564 files need OCR |
| 4 | Epstein Estate Nov 2025 release | ~150 files remaining |

---

## BLOCKED

| Task | Blocker | Resolution |
|------|---------|------------|
| Start Docker services | Docker restart needed | User action |
| OCR processing | Paperless not running | Start Docker first |

---

## COMPLETED (Recent)

| Date | Task |
|------|------|
| 2026-02-09 | Docker Desktop installed |
| 2026-02-09 | data/ directory structure created (local, in project folder) |
| 2026-02-09 | docker-compose.woodsden.yml created |
| 2026-02-09 | Archived pre-restructure state |
| 2026-02-09 | New session continuity system created |
| 2026-02-09 | Tower references purged from core files |
| 2026-02-09 | Network drive references purged from documentation |

---

## SOMEDAY (Backlog)

- Create user system for website login
- Remote access dashboard for pipeline status
- Cycle 2 document extraction
- CIA/Intelligence History theme (18/150+ docs)
- Maxwell Proffer manual download (21 files)
