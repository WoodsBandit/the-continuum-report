# Epstein Document Extraction — File Index

**Generated:** 2025-12-24
**Total Extracted Files:** 100 markdown reports

---

## Directory Structure

```
T:\agents\epstein-extraction\
│
├── extract_pdf.py                    # Single PDF extraction script
├── batch_process.py                  # Batch processing script
├── log.md                            # Activity log
├── index.md                          # Methodology documentation
├── PHASE_1_REPORT.md                 # This report
├── FILE_INDEX.md                     # This file
│
├── findings\
│   ├── court-filings\                # Giuffre v. Maxwell documents
│   │   ├── _summary.json             # Aggregate statistics
│   │   ├── ecf-1320-1.md             # Individual extractions (96 files)
│   │   ├── ecf-1320-2.md
│   │   ├── ... (94 more files)
│   │   └── ecf-1331-4.md
│   │
│   ├── criminal-case\                # Maxwell criminal case
│   │   ├── _summary.json             # Aggregate statistics
│   │   ├── ghislaine-maxwell-indictment-2020-07-02.md
│   │   ├── maxwell-superseding-indictment-2021-03-29.md
│   │   ├── maxwell-sentencing-memo-govt-2022-06.md
│   │   └── maxwell-sentencing-memo-defense-2022-06.md
│   │
│   └── depositions\                  # (Reserved for future use)
```

---

## Court Filings (96 files)

### ECF-1320 Series (40 files)
High-priority court filings from Giuffre v. Maxwell case.

**Documents:**
- ecf-1320-1.md through ecf-1320-40.md

**Highlights:**
- **ecf-1320-1.md** — Maxwell email regarding Clinton, Prince Andrew
- **ecf-1320-12.md** — Largest document (179 pages, 126 people, 181 dates)
- **ecf-1320-13.md** — Investigation details (45 pages, 215 people)
- **ecf-1320-38.md** — Virginia Giuffre deposition (89 pages, 747 quotes)

### ECF-1325 Series (3 files)
Additional court filings.

**Documents:**
- ecf-1325-1.md
- ecf-1325-3.md
- ecf-1325-4.md

### ECF-1327 Series (12 files)
Legal motions and exhibits.

**Documents:**
- ecf-1327-2.md
- ecf-1327-4.md
- ecf-1327-12.md through ecf-1327-14.md
- ecf-1327-19.md
- ecf-1327-21.md through ecf-1327-25.md
- ecf-1327-28.md

### ECF-1328 Series (19 files)
Extensive filing series with depositions and exhibits.

**Documents:**
- ecf-1328-4.md, ecf-1328-5.md, ecf-1328-7.md, ecf-1328-8.md
- ecf-1328-12.md, ecf-1328-14.md through ecf-1328-19.md
- ecf-1328-23.md through ecf-1328-25.md
- ecf-1328-31.md, ecf-1328-34.md, ecf-1328-37.md
- ecf-1328-42.md through ecf-1328-44.md

### ECF-1330 Series (9 files)
Legal arguments and witness materials.

**Documents:**
- ecf-1330-1.md through ecf-1330-5.md
- ecf-1330-9.md, ecf-1330-14.md
- ecf-1330-21.md, ecf-1330-22.md

### ECF-1331 Series (13 files)
Final series of court filings.

**Documents:**
- ecf-1331-4.md
- ecf-1331-11.md through ecf-1331-13.md
- ecf-1331-18.md, ecf-1331-19.md
- ecf-1331-30.md through ecf-1331-32.md
- ecf-1331-34.md through ecf-1331-36.md

---

## Criminal Case (4 files)

### Indictments

**ghislaine-maxwell-indictment-2020-07-02.md**
- Original federal indictment
- 18 pages
- Filed July 2, 2020

**maxwell-superseding-indictment-2021-03-29.md**
- Additional charges
- 2 pages
- Filed March 29, 2021

### Sentencing Memoranda

**maxwell-sentencing-memo-govt-2022-06.md**
- Government's sentencing recommendations
- 4 pages
- 17 people mentioned
- Filed June 2022

**maxwell-sentencing-memo-defense-2022-06.md**
- Defense sentencing arguments
- 3 pages
- 13 people mentioned
- Filed June 2022

---

## Summary Statistics Files

**Court Filings Summary:**
- File: `T:\agents\epstein-extraction\findings\court-filings\_summary.json`
- Format: JSON
- Contains: Aggregate statistics, file-by-file breakdown

**Criminal Case Summary:**
- File: `T:\agents\epstein-extraction\findings\criminal-case\_summary.json`
- Format: JSON
- Contains: Aggregate statistics, file-by-file breakdown

---

## Search & Navigation Tips

### Finding Specific Documents

**By Person:**
Use grep to search across all markdown files:
```bash
grep -r "Prince Andrew" T:/agents/epstein-extraction/findings/
grep -r "Virginia Giuffre" T:/agents/epstein-extraction/findings/
```

**By Location:**
```bash
grep -r "Little St. James" T:/agents/epstein-extraction/findings/
grep -r "Palm Beach" T:/agents/epstein-extraction/findings/
```

**By Date:**
```bash
grep -r "2015" T:/agents/epstein-extraction/findings/
grep -r "January" T:/agents/epstein-extraction/findings/
```

**High-Value Documents (Most Data):**
1. ecf-1320-38.md — 747 quotes (Giuffre deposition)
2. ecf-1320-13.md — 215 people (investigation)
3. ecf-1320-12.md — 179 pages (largest)
4. ecf-1320-18.md — 189 people
5. ecf-1328-18.md — 198 people

---

## File Naming Convention

**Court Filings:**
- Format: `ecf-[docket#]-[attachment#].md`
- Example: `ecf-1320-38.md` = Docket 1320, Attachment 38

**Criminal Case:**
- Format: `[description]-[date].md`
- Example: `maxwell-sentencing-memo-govt-2022-06.md`

---

## Next Steps

**For Deep Investigation:**
1. Review high-priority documents listed above
2. Search for specific entities of interest
3. Cross-reference timeline events across documents
4. Compare criminal case docs with civil case materials

**For Analysis:**
1. Load JSON summaries for statistical analysis
2. Create entity relationship graphs
3. Build comprehensive timeline from dated events
4. Aggregate quotes by topic/subject

---

**Last Updated:** 2025-12-24
**Maintainer:** Master Epstein Document Extraction Agent
