# TASK: Generate Sources Manifest JSON

Create a comprehensive JSON manifest of all source documents for the Sources page.

---

## OUTPUT FILE

Save to: `/continuum/website/data/sources-manifest.json`

---

## STEP 1: Scan the Sources Directory

Read the contents of `/continuum/sources/` and build a data structure.

```bash
find /continuum/sources -type f -name "*.pdf" | sort
```

---

## STEP 2: JSON Structure

Create this structure:

```json
{
  "generated": "ISO_TIMESTAMP",
  "totalDocuments": 0,
  "collections": [
    {
      "id": "executive-power",
      "title": "Executive Power Expansion",
      "description": "The documentary trail from Pollock to Loper Bright — tracing how executive authority expanded through emergency powers, judicial interpretation, and legislative delegation.",
      "icon": "scale",
      "dateRange": "1861-2024",
      "documentCount": 0,
      "categories": [
        {
          "id": "supreme-court",
          "name": "Supreme Court Opinions",
          "documents": []
        },
        {
          "id": "legislation",
          "name": "Legislative Acts",
          "documents": []
        },
        {
          "id": "executive-orders",
          "name": "Executive Orders",
          "documents": []
        },
        {
          "id": "congressional-investigations",
          "name": "Congressional Investigations",
          "documents": []
        }
      ]
    },
    {
      "id": "epstein-network",
      "title": "Epstein Network",
      "description": "Primary source documentation of the Epstein case — court filings, flight logs, and related litigation.",
      "icon": "network",
      "dateRange": "2006-2024",
      "documentCount": 0,
      "categories": [
        {
          "id": "court-filings",
          "name": "Court Filings",
          "documents": []
        },
        {
          "id": "personal-records",
          "name": "Personal Records",
          "documents": []
        },
        {
          "id": "related-litigation",
          "name": "Related Litigation",
          "documents": []
        }
      ]
    },
    {
      "id": "intelligence-operations",
      "title": "Intelligence Operations",
      "description": "Congressional investigations and reports on intelligence agency activities — Iran-Contra, BCCI, Church Committee, and INSLAW.",
      "icon": "eye",
      "dateRange": "1975-1992",
      "documentCount": 0,
      "categories": [
        {
          "id": "iran-contra",
          "name": "Iran-Contra",
          "documents": []
        },
        {
          "id": "bcci",
          "name": "BCCI",
          "documents": []
        },
        {
          "id": "church-committee",
          "name": "Church Committee",
          "documents": []
        },
        {
          "id": "inslaw-promis",
          "name": "INSLAW / PROMIS",
          "documents": []
        }
      ]
    },
    {
      "id": "parallel-cases",
      "title": "Parallel Cases",
      "description": "Related cases exhibiting similar patterns — trafficking, coercion, and elite protection.",
      "icon": "link",
      "dateRange": "2017-2024",
      "documentCount": 0,
      "categories": [
        {
          "id": "nxivm",
          "name": "NXIVM / Raniere",
          "documents": []
        }
      ]
    }
  ]
}
```

---

## STEP 3: Document Object Structure

For each PDF file, create a document object:

```json
{
  "id": "pollock-1895",
  "filename": "1895-POLLOCK-V-FARMERS-LOAN-TRUST-157-US-429.pdf",
  "title": "Pollock v. Farmers' Loan & Trust Co.",
  "citation": "157 U.S. 429 (1895)",
  "date": "1895-04-08",
  "year": 1895,
  "description": "Supreme Court ruled federal income tax unconstitutional as an unapportioned direct tax",
  "type": "court-opinion",
  "pages": null,
  "fileSize": "8.1 MB",
  "pdfPath": "/sources/executive-power/supreme-court/1895-POLLOCK-V-FARMERS-LOAN-TRUST-157-US-429.pdf",
  "textPath": "/sources/executive-power/supreme-court/1895-POLLOCK-V-FARMERS-LOAN-TRUST-157-US-429.txt",
  "hasText": true,
  "publicDomain": true,
  "tags": ["income-tax", "supreme-court", "constitutional", "direct-tax"]
}
```

---

## STEP 4: Document Metadata Extraction

For each document, extract/infer:

### From Filename:
- Year (first 4 digits)
- Document type (from path: supreme-court, legislation, etc.)

### Known Document Metadata:

**Supreme Court Cases:**
| Filename Pattern | Title | Citation | Description |
|-----------------|-------|----------|-------------|
| 1895-POLLOCK-V-FARMERS* | Pollock v. Farmers' Loan & Trust Co. | 157 U.S. 429 (1895) | Income tax ruled unconstitutional |
| 1895-POLLOCK-REHEARING* | Pollock v. Farmers' Loan (Rehearing) | 158 U.S. 601 (1895) | Rehearing reaffirmed unconstitutionality |
| 1916-BRUSHABER* | Brushaber v. Union Pacific Railroad | 240 U.S. 1 (1916) | 16th Amendment upheld income tax |
| 1952-YOUNGSTOWN* | Youngstown Sheet & Tube Co. v. Sawyer | 343 U.S. 579 (1952) | Steel Seizure Case - Jackson framework |
| 1861-EX-PARTE-MERRYMAN* | Ex parte Merryman | 17 F. Cas. 144 (1861) | Habeas corpus suspension challenged |
| 1866-EX-PARTE-MILLIGAN* | Ex parte Milligan | 71 U.S. 2 (1866) | Military tribunals unconstitutional |
| 1984-CHEVRON* | Chevron U.S.A. v. NRDC | 467 U.S. 837 (1984) | Agency deference doctrine |
| 2024-LOPER-BRIGHT* | Loper Bright v. Raimondo | 603 U.S. ___ (2024) | Overturned Chevron deference |

**Legislation:**
| Filename Pattern | Title | Citation | Description |
|-----------------|-------|----------|-------------|
| 1913-FEDERAL-RESERVE* | Federal Reserve Act | 38 Stat. 251 | Created Federal Reserve System |
| 1913-REVENUE-ACT* | Revenue Act of 1913 | 38 Stat. 114 | First income tax under 16th Amendment |
| 1917-TRADING-WITH-ENEMY* | Trading with the Enemy Act | 40 Stat. 411 | Wartime emergency powers |
| 1933-EMERGENCY-BANKING* | Emergency Banking Act | 48 Stat. 1 | Extended TWEA to peacetime |
| 1934-GOLD-RESERVE* | Gold Reserve Act | 48 Stat. 337 | Nationalized gold reserves |
| 1946-ADMINISTRATIVE-PROCEDURE* | Administrative Procedure Act | 60 Stat. 237 | Created regulatory framework |
| 1973-WAR-POWERS* | War Powers Resolution | 87 Stat. 555 | Limited presidential war powers |
| 1976-NATIONAL-EMERGENCIES* | National Emergencies Act | 90 Stat. 1255 | Codified emergency powers |
| 1977-IEEPA* | IEEPA | 91 Stat. 1626 | Economic emergency powers |
| 1978-FISA* | FISA | 92 Stat. 1783 | Secret surveillance courts |
| 2001-USA-PATRIOT* | USA PATRIOT Act | 115 Stat. 272 | Expanded surveillance powers |

**Executive Orders:**
| Filename Pattern | Title | Date | Description |
|-----------------|-------|------|-------------|
| 1933-EXECUTIVE-ORDER-6102* | Executive Order 6102 | April 5, 1933 | Required citizens to surrender gold |
| 1971-EXECUTIVE-ORDER-11615* | Executive Order 11615 | August 15, 1971 | Wage/price controls, closed gold window |

**Congressional Investigations:**
| Filename Pattern | Title | Description |
|-----------------|-------|-------------|
| *PUJO-COMMITTEE* | Pujo Committee Money Trust Investigation | Exposed concentrated banking power |

---

## STEP 5: Check for Text Versions

For each PDF, check if a .txt version exists in `/continuum/downloads/executive-power/extracted-text/`:

```bash
if [ -f "/continuum/downloads/executive-power/extracted-text/${basename%.pdf}.txt" ]; then
  hasText=true
fi
```

---

## STEP 6: Calculate File Sizes

Get file size for each document:

```bash
stat -c %s /continuum/sources/executive-power/supreme-court/FILE.pdf
```

Format as human-readable (e.g., "8.1 MB", "245 KB")

---

## STEP 7: Update Counts

After building the manifest:
1. Count documents in each category
2. Sum for each collection's documentCount
3. Sum all for totalDocuments
4. Update dateRange based on actual documents

---

## STEP 8: Write JSON File

Save to `/continuum/website/data/sources-manifest.json` with proper formatting (2-space indent).

---

## OUTPUT REPORT

```
MANIFEST GENERATED

Total Documents: X

Collections:
- Executive Power: X documents (Y categories)
- Epstein Network: X documents (Y categories)
- Intelligence Operations: X documents (Y categories)
- Parallel Cases: X documents (Y categories)

File saved: /continuum/website/data/sources-manifest.json
File size: X KB
```

---

## POST-TASK: PERMISSIONS (Run from root@Tower AFTER Claude Code completes)

```bash
chmod 666 /mnt/user/continuum/website/data/sources-manifest.json
chown nobody:users /mnt/user/continuum/website/data/sources-manifest.json
```

---

*The Continuum Report — Another Node in the Decentralized Intelligence Agency*
