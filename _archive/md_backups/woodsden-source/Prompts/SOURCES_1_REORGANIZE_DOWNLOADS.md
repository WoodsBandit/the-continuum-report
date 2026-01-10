# TASK: Reorganize Source Documents into New Directory Structure

Reorganize the existing downloaded documents into a structured hierarchy for the public-facing Sources page.

---

## CURRENT STATE

Documents are scattered across:
- `/continuum/downloads/` (Epstein-related documents)
- `/continuum/downloads/executive-power/` (Executive power documents in tier1-4)

---

## TARGET STRUCTURE

Create this hierarchy under `/continuum/sources/`:

```
/continuum/sources/
├── executive-power/
│   ├── supreme-court/
│   ├── legislation/
│   ├── executive-orders/
│   └── congressional-investigations/
│       └── pujo-committee/
├── epstein-network/
│   ├── court-filings/
│   ├── personal-records/
│   └── related-litigation/
├── intelligence-operations/
│   ├── iran-contra/
│   ├── bcci/
│   ├── church-committee/
│   └── inslaw-promis/
└── parallel-cases/
    └── nxivm/
```

---

## STEP 1: Create Directory Structure

```bash
mkdir -p /continuum/sources/executive-power/{supreme-court,legislation,executive-orders,congressional-investigations/pujo-committee}
mkdir -p /continuum/sources/epstein-network/{court-filings,personal-records,related-litigation}
mkdir -p /continuum/sources/intelligence-operations/{iran-contra,bcci,church-committee,inslaw-promis}
mkdir -p /continuum/sources/parallel-cases/nxivm
```

---

## STEP 2: Copy Executive Power Documents

### Supreme Court Opinions → `/continuum/sources/executive-power/supreme-court/`
- 1895-POLLOCK-V-FARMERS-LOAN-TRUST-157-US-429.pdf
- 1895-POLLOCK-REHEARING-158-US-601.pdf
- 1916-BRUSHABER-V-UNION-PACIFIC-240-US-1.pdf
- 1952-YOUNGSTOWN-STEEL-SEIZURE-343-US-579.pdf
- 1861-EX-PARTE-MERRYMAN-*.pdf (both versions)
- 1866-EX-PARTE-MILLIGAN-71-US-2.pdf
- 1984-CHEVRON-V-NRDC-467-US-837.pdf
- 2024-LOPER-BRIGHT-CHEVRON-OVERTURNED.pdf

### Legislation → `/continuum/sources/executive-power/legislation/`
- 1913-FEDERAL-RESERVE-ACT-STATUTE-38.pdf
- 1913-REVENUE-ACT-UNDERWOOD-SIMMONS.pdf
- 1917-TRADING-WITH-ENEMY-ACT.pdf
- 1933-EMERGENCY-BANKING-ACT.pdf
- 1934-GOLD-RESERVE-ACT.pdf
- 1946-ADMINISTRATIVE-PROCEDURE-ACT.pdf
- 1973-WAR-POWERS-RESOLUTION.pdf
- 1976-NATIONAL-EMERGENCIES-ACT.pdf
- 1977-IEEPA.pdf
- 1978-FISA-FOREIGN-INTELLIGENCE-SURVEILLANCE-ACT.pdf
- 2001-USA-PATRIOT-ACT.pdf
- 1863-HABEAS-CORPUS-SUSPENSION-ACT.pdf

### Executive Orders → `/continuum/sources/executive-power/executive-orders/`
- 1933-EXECUTIVE-ORDER-6102-GOLD-CONFISCATION.pdf
- 1971-EXECUTIVE-ORDER-11615-NIXON-SHOCK.pdf
- 1971-NIXON-ADDRESS-*.pdf (supporting documents)

### Congressional Investigations → `/continuum/sources/executive-power/congressional-investigations/`
- 1912-1913-PUJO-COMMITTEE-FINAL-REPORT.pdf
- 1912-1913-PUJO-COMMITTEE-REPORT.pdf
- 1912-JP-MORGAN-PUJO-TESTIMONY.pdf

### Pujo Committee Parts → `/continuum/sources/executive-power/congressional-investigations/pujo-committee/`
- All files from `/continuum/downloads/executive-power/tier1/pujo-committee-parts/`

---

## STEP 3: Copy Epstein Network Documents

Look in `/continuum/downloads/` for these document types:

### Court Filings → `/continuum/sources/epstein-network/court-filings/`
- Any NPA (Non-Prosecution Agreement) documents
- Appeal documents
- Indictments
- Court orders

### Personal Records → `/continuum/sources/epstein-network/personal-records/`
- Flight logs
- Black Book
- Any personal documentation

### Related Litigation → `/continuum/sources/epstein-network/related-litigation/`
- JP Morgan lawsuit documents
- Any civil case documents

---

## STEP 4: Copy Intelligence Operations Documents

Look in `/continuum/downloads/` for:

### Iran-Contra → `/continuum/sources/intelligence-operations/iran-contra/`
- Iran-Contra reports

### BCCI → `/continuum/sources/intelligence-operations/bcci/`
- Kerry Report / BCCI documents

### Church Committee → `/continuum/sources/intelligence-operations/church-committee/`
- Church Committee documents

### INSLAW/PROMIS → `/continuum/sources/intelligence-operations/inslaw-promis/`
- INSLAW case documents
- PROMIS software documents

---

## STEP 5: Copy Parallel Cases Documents

### NXIVM → `/continuum/sources/parallel-cases/nxivm/`
- NXIVM indictments
- Keith Raniere documents

---

## EXECUTION INSTRUCTIONS

1. First, list all files in `/continuum/downloads/` to see what exists:
```bash
find /continuum/downloads -type f -name "*.pdf" | head -100
```

2. Create the directory structure (Step 1)

3. Copy files (NOT move - keep originals in downloads as working copies):
```bash
cp /continuum/downloads/executive-power/tier1/FILENAME.pdf /continuum/sources/executive-power/supreme-court/
```

4. For each file copied, verify it exists in the destination

5. Generate a report of what was copied where

---

## OUTPUT REPORT

Provide a summary:
```
REORGANIZATION COMPLETE

Executive Power:
- Supreme Court: X files
- Legislation: X files  
- Executive Orders: X files
- Congressional Investigations: X files
- Pujo Committee Parts: X files

Epstein Network:
- Court Filings: X files
- Personal Records: X files
- Related Litigation: X files

Intelligence Operations:
- Iran-Contra: X files
- BCCI: X files
- Church Committee: X files
- INSLAW/PROMIS: X files

Parallel Cases:
- NXIVM: X files

TOTAL: X files organized

Files not categorized (need manual review):
- [list any files that didn't fit categories]
```

---

## POST-TASK: PERMISSIONS (Run from root@Tower AFTER Claude Code completes)

```bash
chmod -R 777 /mnt/user/continuum/sources/
chown -R nobody:users /mnt/user/continuum/sources/
```

---

*The Continuum Report — Another Node in the Decentralized Intelligence Agency*
