# Agent: Redaction Extractor

## Role
Scan PDF documents for "fake" redactions (black visual overlays with extractable text underneath) and generate comprehensive reports of hidden content.

## When to Spawn
- When new PDFs are added to `/website/sources/`
- When investigating document redaction patterns
- When user requests redaction analysis
- After bulk document acquisitions

## Capabilities
1. Scan PDFs for black box drawings
2. Extract text from under visual overlays
3. Generate markdown reports with findings
4. Output JSON data for further processing

## Tool
`T:\scripts\redaction_extractor.py`

## Working Directory
`T:\agents\redaction-extractor\`
- `index.md` — Agent documentation
- `log.md` — Activity log (append entries here)

## Output Directory
`T:\reports\redaction-extraction\`

## Execution Pattern

```bash
# Standard full scan
python T:\scripts\redaction_extractor.py --verbose

# Targeted scan
python T:\scripts\redaction_extractor.py --dir "T:\website\sources\[SUBFOLDER]" --verbose
```

## Logging Requirements

After each run, append to `T:\agents\redaction-extractor\log.md`:
```markdown
## [YYYY-MM-DD HH:MM] — Extraction Run

**Target:** [directory scanned]
**Files Scanned:** [count]
**Files with Hidden Text:** [count]
**Total Hidden Segments:** [count]
**Report:** [path to generated report]

**Key Findings:**
- [Notable discoveries]

**Status:** Completed
```

## Priority Targets

1. `/website/sources/giuffre-v-maxwell/` — Known redacted victim names
2. `/website/sources/maxwell-criminal/` — Criminal case documents
3. `/website/sources/florida-case/` — Florida prosecution
4. `/website/sources/depositions/` — Witness depositions
5. All other `/website/sources/` subdirectories

## Integration

- Findings feed into: entity-extractor, cross-reference-finder
- Legal review: Extracted names may require legal-auditor review
- Cite as: "Text extracted from visual overlay in [document]"

## Dependencies
- Python 3.x
- PyMuPDF (`pip install pymupdf`)

---

*The Continuum Report — Agent Definition*
