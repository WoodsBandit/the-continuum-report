# Claude Code Task: Citation Gap Audit

**From:** Infrastructure Lead (Claude Main)
**To:** Claude Code (Tower)
**Date:** 2025-12-22
**Priority:** HIGH — Blocks brief citation updates

---

## Objective

Identify gaps between ECF documents cited in analytical briefs and documents actually hosted at `/sources/giuffre-v-maxwell/`.

---

## Phase 1: Extract Citations from Briefs

### 1.1 List all briefs
```bash
ls -la /continuum/briefs/
```

### 1.2 Extract ECF patterns from all briefs

Search for ECF citation patterns in all markdown files:
```bash
grep -rohE 'ecf-[0-9]+-[0-9]+' /continuum/briefs/*.md | sort -u
grep -rohE 'ECF[- ][0-9]+-[0-9]+' /continuum/briefs/*.md | sort -u
grep -rohE '[0-9]{4}-[0-9]{1,3}' /continuum/briefs/*.md | sort -u
```

Also check for PACER-style references:
```bash
grep -rohE 'gov\.uscourts\.[a-z]+\.[0-9]+\.[0-9]+\.[0-9]+' /continuum/briefs/*.md | sort -u
```

### 1.3 Map citations to briefs

For each unique ECF citation found, identify which brief(s) contain it:
```bash
for ecf in $(grep -rohE 'ecf-[0-9]+-[0-9]+' /continuum/briefs/*.md | sort -u); do
  echo "=== $ecf ==="
  grep -l "$ecf" /continuum/briefs/*.md
done
```

---

## Phase 2: Inventory Hosted Files

### 2.1 List all hosted source files
```bash
ls -1 /continuum/website/sources/giuffre-v-maxwell/*.pdf | xargs -n1 basename | sort
```

### 2.2 Count
```bash
ls -1 /continuum/website/sources/giuffre-v-maxwell/*.pdf | wc -l
```

---

## Phase 3: Gap Analysis

### 3.1 Create comparison

Using the citations from Phase 1 and files from Phase 2, identify:

**Category A — MATCHED:** Citation exists AND file is hosted
**Category B — GAP:** Citation exists BUT file is NOT hosted
**Category C — ORPHAN:** File is hosted BUT not cited in any brief (informational only)

---

## Phase 4: Check Paperless for Gap Documents

For each gap identified in Category B, query Paperless:

```bash
# Example for ecf-1331-14
curl -s -H "Authorization: Token da99fe6aa0b8d021689126cf72b91986abbbd283" \
  "http://192.168.1.139:8040/api/documents/?query=1331-14" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'Results: {data.get(\"count\", 0)}')
for doc in data.get('results', []):
    print(f\"  ID: {doc['id']} | Title: {doc['title']} | File: {doc.get('original_file_name', 'N/A')}\")"
```

Categorize gaps as:
- **B1 — EXPORTABLE:** Gap document exists in Paperless, can be exported
- **B2 — MISSING:** Gap document not in Paperless, requires PACER acquisition

---

## Deliverable

Create `/continuum/reports/citation_gap_audit_2025-12-22.md` with:

```markdown
# Citation Gap Audit Report

**Generated:** 2025-12-22
**Briefs Scanned:** [COUNT]
**Unique Citations Found:** [COUNT]
**Hosted Files:** [COUNT]

---

## Summary

| Category | Count | Status |
|----------|-------|--------|
| A — Matched | X | ✅ Ready for linking |
| B1 — Exportable | X | ⚠️ In Paperless, needs export |
| B2 — Missing | X | ❌ Requires PACER acquisition |
| C — Orphan | X | ℹ️ Hosted but not cited |

---

## Category A: Matched (Citation + Hosted)

| ECF | Brief(s) | Public URL |
|-----|----------|------------|
| ecf-1328-44 | brief_name.md | /sources/giuffre-v-maxwell/ecf-1328-44.pdf |
| ... | ... | ... |

---

## Category B1: Exportable Gaps (In Paperless)

| ECF | Brief(s) | Paperless ID | Action |
|-----|----------|--------------|--------|
| ecf-XXXX-XX | brief_name.md | 123 | Export needed |
| ... | ... | ... | ... |

---

## Category B2: Missing (Not in Paperless)

| ECF | Brief(s) | Action |
|-----|----------|--------|
| ecf-XXXX-XX | brief_name.md | PACER acquisition required |
| ... | ... | ... |

---

## Category C: Orphan Files (Hosted but Not Cited)

| File | Notes |
|------|-------|
| ecf-XXXX-XX.pdf | Available for future use |
| ... | ... |

---

## Recommendations

[Summary of actions needed]
```

---

## Also Update Response File

Copy findings summary to `Citation_Gap_Audit_Response.md` in the Infrastructure Expert folder for Claude Main to review.

---

## Success Criteria

1. Every ECF citation in briefs is accounted for
2. Every hosted file is catalogued
3. Gaps are identified and categorized
4. Paperless has been checked for exportable documents
5. Clear action list for filling gaps

---

*Task issued by Infrastructure Lead — 2025-12-22*
