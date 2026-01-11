# Document Corpus — Complete Inventory

**The Continuum Report**
**Last Updated:** 2025-12-25

---

## Primary Document Collections

| Collection | Files | Size | Location | Status |
|------------|-------|------|----------|--------|
| **House Oversight DOJ 33k (Original)** | 33,564 PDFs | 13.8GB | `/continuum/downloads/house-oversight/extracted/epstein-pdf/` | ✅ Original archive (image-based, no OCR) |
| **House Oversight DOJ 2025 (Web)** | 33,572 PDFs | ~13.8GB | `/continuum/website/sources/house-oversight-2025/` | ✅ Processed for web hosting (DOJ-OGR-######## naming) |
| **Additional Website Sources** | 173 PDFs | Various | `/continuum/website/sources/[12 categories]/` | ✅ Organized by category |
| **TOTAL Website Sources** | **33,745 PDFs** | ~14GB+ | `/continuum/website/sources/` | ✅ Publicly accessible |
| **DOJ Combined DataSets 1-7** | 7 PDFs | ~3.2GB | `/continuum/downloads/doj-combined/` | ✅ Downloaded |
| **FBI Vault Epstein** | 8 parts | ~12MB | `/continuum/downloads/fbi-vault/` | ✅ Downloaded (also in website/sources) |
| **Giuffre v. Maxwell Unsealed** | 96 PDFs | Various | `/continuum/website/sources/giuffre-v-maxwell/` AND Paperless-ngx | ✅ Processed & hosted |

---

## Website-Hosted Source Documents

**Location:** `/continuum/website/sources/`
**Total PDFs:** 33,745 (as of 2025-12-24)

| Category | Files | Description |
|----------|-------|-------------|
| house-oversight-2025 | 33,572 | DOJ Congressional transparency release (renamed from original 33,564-file archive) |
| giuffre-v-maxwell | 96 | Unsealed 2024 court documents from civil case |
| cia-history | 18 | CIA historical documentation and analysis |
| financial-enablers | 15 | Deutsche Bank consent orders, JPMorgan litigation, Wexner documentation |
| fbi-history | 14 | FBI historical files |
| doj-transparency-2025 | 8 | Additional DOJ transparency releases |
| fbi-vault | 8 | FBI Vault Epstein investigation files (Parts 1-8) |
| florida-case | 6 | 2008 NPA, 2006 grand jury, 2020 OPR report, 2019 federal indictment |
| maxwell-criminal | 4 | Original/superseding indictments (sentencing memos verified June 2022) |
| regulatory-actions | 3 | FinCEN 311 (FBME), UK FCA Jes Staley notices |
| palm-beach-investigation | 1 | Palm Beach Police investigative records |
| epstein-sdny | 0 | Placeholder for SDNY case documents |
| epstein-estate | 0 | Placeholder for estate/probate documents |

---

## Source Documents by Category

### Florida Case
**Location:** `/continuum/website/sources/florida-case/`

- 2008 NPA (Non-Prosecution Agreement)
- 2006 Grand Jury Transcripts (176 pages)
- 2020 DOJ OPR Report (Acosta investigation)
- Palm Beach Police Records
- 2019 Federal Indictment (SDNY)

### Financial Enablers
**Location:** `/continuum/website/sources/financial-enablers/`

**Deutsche Bank:**
- NYSDFS consent orders ($150M Epstein, $425M mirror trades)
- FCA notices

**JPMorgan:**
- OCC consent orders
- Civil litigation documents
- Jes Staley FCA action (1,700+ emails)

**Wexner:**
- Foundation review documents
- Leaked emails (Dropsite News)
- Co-conspirator documentation

### Maxwell Criminal Case
**Location:** `/continuum/website/sources/maxwell-criminal/`

- Original indictment
- Superseding indictment
- June 2022 sentencing memos (verified)

### Regulatory Actions
**Location:** `/continuum/website/sources/regulatory-actions/`

- FinCEN 311 (FBME designation)
- UK FCA Jes Staley Final Notice
- UK FCA Jes Staley Decision Notice

---

## Document Acquisition Master List

**Location:** `/continuum/reports/MASTER_DOCUMENT_ACQUISITION_LIST.md`
**Total Identified:** 249 documents prioritized with URLs and costs

---

## Infrastructure Notes

### House Oversight Collection

- The house-oversight-2025 collection uses systematic naming: `DOJ-OGR-########.pdf`
- Original download (33,564 files) preserved in `/downloads/house-oversight/extracted/epstein-pdf/`
- Web version contains 8 additional files (33,572 total) — likely processing artifacts or supplemental documents
- **⚠️ All DOJ files are image-based scans requiring OCR for text search**

### Known Issues

| Issue | Impact | Fix |
|-------|--------|-----|
| DOJ 33k files not text-searchable | Can't grep for names | OCR processing needed (TOP PRIORITY) |
| Some external URLs not resolving | Can't download USVI docs | DNS issue in container |

---

*For CLAUDE.md summary, see: Section 3 (Document Corpus)*
