# Executive Power Expansion Document Acquisition Task

## Mission
Systematically download, organize, and ingest primary source documents for The Continuum Report's executive power expansion layer into the Paperless-ngx document management system on the Unraid server "Tower."

## Infrastructure Context
- **Unraid Server**: "Tower" (Intel i7-10700K, 16GB RAM, 12TB free storage)
- **Paperless-ngx**: Running in Docker via Portainer-CE
- **Consume Directory**: `/mnt/user/appdata/paperless/consume/` (SMB accessible from Windows workstation)
- **API**: Token-based authentication configured
- **Network**: SMB sharing between server and Windows 11 workstation

## Document Acquisition Priority Tiers

### TIER 1: CRITICAL PRIMARY SOURCES (Download First)

#### 1.1 Federal Reserve Creation
```
PUJO COMMITTEE HEARINGS (1912-1913) - "Money Trust Investigation"
Source: https://publicintelligence.net/pujo-committee-money-trust-wall-street-banking-cartel-investigation-1912-1913/
Files: 29 parts + exhibits + final report
Format: PDF
Tags: pujo-committee, federal-reserve, money-trust, 1912, 1913, congressional-hearing
Correspondent: House Banking and Currency Committee
```

```
FEDERAL RESERVE ACT (1913)
Source: https://fraser.stlouisfed.org/ (search Federal Reserve Act)
Alt: https://www.govinfo.gov/content/pkg/STATUTE-38/pdf/STATUTE-38-Pg251.pdf
Format: PDF
Tags: federal-reserve-act, 1913, legislation, banking
```

```
NATIONAL MONETARY COMMISSION REPORTS
Source: https://fraser.stlouisfed.org/series/national-monetary-commission-publications-702
Format: PDF (multiple volumes)
Tags: national-monetary-commission, aldrich, 1910, 1911, banking-reform
```

#### 1.2 Income Tax & 16th Amendment
```
POLLOCK v. FARMERS' LOAN & TRUST CO. (1895)
Source: https://tile.loc.gov/storage-services/service/ll/usrep/usrep157/usrep157429/usrep157429.pdf
Alt: https://supreme.justia.com/cases/federal/us/157/429/
Format: PDF
Tags: pollock, income-tax, supreme-court, 1895, direct-tax, unconstitutional
```

```
POLLOCK REHEARING (1895)
Source: https://tile.loc.gov/storage-services/service/ll/usrep/usrep158/usrep158601/usrep158601.pdf
Format: PDF
Tags: pollock, income-tax, supreme-court, 1895, rehearing
```

```
BRUSHABER v. UNION PACIFIC (1916)
Source: LOC or Justia
Format: PDF
Tags: brushaber, income-tax, supreme-court, 1916, 16th-amendment
```

```
REVENUE ACT OF 1913
Source: https://www.govinfo.gov/
Format: PDF
Tags: revenue-act, 1913, income-tax, legislation, underwood-simmons
```

#### 1.3 Emergency Powers - Gold Confiscation
```
EXECUTIVE ORDER 6102 (April 5, 1933)
Source: https://www.presidency.ucsb.edu/documents/executive-order-6102-requiring-gold-coin-gold-bullion-and-gold-certificates-be-delivered
Alt: National Archives
Format: PDF
Tags: executive-order, eo-6102, gold-confiscation, 1933, fdr, emergency-powers
```

```
EMERGENCY BANKING ACT (1933)
Source: https://www.govinfo.gov/
Format: PDF
Tags: emergency-banking-act, 1933, twea-amendment, fdr, bank-holiday
```

```
GOLD RESERVE ACT (1934)
Source: https://www.govinfo.gov/
Format: PDF
Tags: gold-reserve-act, 1934, gold-revaluation, fdr
```

```
TRADING WITH THE ENEMY ACT (1917)
Source: https://www.govinfo.gov/
Format: PDF
Tags: twea, trading-with-enemy, 1917, wwi, emergency-powers, wilson
```

#### 1.4 Steel Seizure & Executive Power Limits
```
YOUNGSTOWN SHEET & TUBE v. SAWYER (1952)
Source: https://tile.loc.gov/storage-services/service/ll/usrep/usrep343/usrep343579/usrep343579.pdf
Format: PDF
Tags: youngstown, steel-seizure, supreme-court, 1952, truman, jackson-framework
```

```
EXECUTIVE ORDER 10340 (Steel Seizure)
Source: Federal Register / NARA
Format: PDF
Tags: executive-order, eo-10340, steel-seizure, 1952, truman
```

### TIER 2: SUPPORTING PRIMARY SOURCES

#### 2.1 Nixon Shock & End of Gold Standard
```
EXECUTIVE ORDER 11615 (August 15, 1971)
Source: https://www.presidency.ucsb.edu/ or Federal Register
Format: PDF
Tags: executive-order, eo-11615, nixon-shock, 1971, gold-standard, bretton-woods
```

```
NIXON ADDRESS TO THE NATION (August 15, 1971)
Source: https://www.presidency.ucsb.edu/documents/address-the-nation-outlining-new-economic-policy-the-challenge-peace
Format: PDF/transcript
Tags: nixon, speech, 1971, new-economic-policy, gold-window
```

```
SMITHSONIAN AGREEMENT (December 1971)
Source: IMF Archives / Treasury
Format: PDF
Tags: smithsonian-agreement, 1971, exchange-rates, bretton-woods
```

#### 2.2 Church Committee & Intelligence
```
CHURCH COMMITTEE FINAL REPORT (1976) - 6 Books
Source: https://www.intelligence.senate.gov/resources/intelligence-related-commissions
Alt: https://www.aarclibrary.org/publib/contents/church/contents_church_reports.htm
Format: PDF (multiple volumes)
Tags: church-committee, 1975, 1976, intelligence-abuses, fbi, cia, nsa, cointelpro
```

```
CHURCH COMMITTEE HEARINGS (7 volumes)
Source: Same as above
Format: PDF
Tags: church-committee, hearings, 1975, intelligence
```

```
COINTELPRO DOCUMENTS
Source: FBI Vault - https://vault.fbi.gov/cointel-pro
Format: PDF
Tags: cointelpro, fbi, domestic-surveillance, mlk, civil-rights
```

#### 2.3 Civil War Era
```
EX PARTE MERRYMAN (1861)
Source: https://tile.loc.gov/storage-services/service/ll/llst/llst017/llst017.pdf
Format: PDF
Tags: ex-parte-merryman, habeas-corpus, lincoln, taney, 1861, civil-war
```

```
LINCOLN MESSAGE TO CONGRESS (July 4, 1861)
Source: https://www.presidency.ucsb.edu/ or LOC
Format: PDF
Tags: lincoln, message-to-congress, 1861, habeas-corpus, civil-war
```

```
HABEAS CORPUS SUSPENSION ACT (1863)
Source: https://www.govinfo.gov/
Format: PDF
Tags: habeas-corpus, suspension-act, 1863, lincoln, civil-war
```

```
EX PARTE MILLIGAN (1866)
Source: LOC Supreme Court records
Format: PDF
Tags: ex-parte-milligan, supreme-court, 1866, military-tribunals, civil-war
```

#### 2.4 War Powers & National Emergencies
```
FIRST WAR POWERS ACT (1941)
Source: https://www.govinfo.gov/
Format: PDF
Tags: war-powers-act, 1941, wwii, fdr, executive-power
```

```
SECOND WAR POWERS ACT (1942)
Source: https://www.govinfo.gov/
Format: PDF
Tags: war-powers-act, 1942, wwii, fdr
```

```
WAR POWERS RESOLUTION (1973)
Source: https://www.govinfo.gov/
Format: PDF
Tags: war-powers-resolution, 1973, nixon, congressional-oversight
```

```
NATIONAL EMERGENCIES ACT (1976)
Source: https://www.govinfo.gov/
Format: PDF
Tags: national-emergencies-act, 1976, emergency-powers, congressional-oversight
```

```
IEEPA (1977)
Source: https://www.govinfo.gov/
Format: PDF
Tags: ieepa, 1977, emergency-economic-powers, sanctions
```

```
SENATE SPECIAL COMMITTEE ON NATIONAL EMERGENCIES REPORTS (1973-1974)
Source: Congressional archives
Format: PDF
Tags: church-mathias, national-emergencies, 1973, 1974, emergency-powers-inventory
```

### TIER 3: ADMINISTRATIVE STATE & MODERN ERA

#### 3.1 Administrative Procedure
```
ADMINISTRATIVE PROCEDURE ACT (1946)
Source: https://www.govinfo.gov/
Format: PDF
Tags: apa, administrative-procedure-act, 1946, fourth-branch, regulatory-state
```

```
ATTORNEY GENERAL'S MANUAL ON APA (1947)
Source: https://www.justice.gov/ or law school archives
Format: PDF
Tags: apa, attorney-general-manual, 1947, administrative-law
```

```
CHEVRON v. NRDC (1984)
Source: LOC / Justia
Format: PDF
Tags: chevron, supreme-court, 1984, deference, administrative-law
```

```
LOPER BRIGHT v. RAIMONDO (2024)
Source: https://www.supremecourt.gov/
Format: PDF
Tags: loper-bright, supreme-court, 2024, chevron-overruled, administrative-law
```

#### 3.2 USA PATRIOT Act
```
USA PATRIOT ACT (2001)
Source: https://www.congress.gov/107/plaws/publ56/PLAW-107publ56.pdf
Format: PDF
Tags: patriot-act, 2001, surveillance, fisa, terrorism, bush
```

```
FISA (1978)
Source: https://www.govinfo.gov/
Format: PDF
Tags: fisa, 1978, surveillance, intelligence, church-committee-reform
```

### TIER 4: SECONDARY SOURCES & BOOKS (Manual Acquisition)

These require purchase or library access:
- "The Creature from Jekyll Island" by G. Edward Griffin
- "A History of the Federal Reserve" Vols 1 & 2 by Allan Meltzer
- "The Unitary Executive" by Calabresi & Yoo
- "Other People's Money" by Louis Brandeis (1914) - may be public domain
- Carter Glass "An Adventure in Constructive Finance" (1927)
- Paul Warburg Federal Reserve history (1930)

## Acquisition Script Structure

For each document, the script should:

1. **Download** the PDF to a staging directory
2. **Rename** using convention: `YYYY-MM-DD_ShortTitle_Source.pdf`
3. **Generate metadata** file for Paperless-ngx tagging
4. **Move** to Paperless consume directory
5. **Log** acquisition status

### Suggested Directory Structure
```
/home/user/continuum-acquisition/
├── staging/           # Downloaded files before processing
├── processed/         # Successfully ingested files (backup)
├── failed/            # Failed downloads for retry
├── logs/              # Acquisition logs
└── scripts/           # Python/bash scripts
```

### Paperless-ngx Tagging Schema

**Document Types:**
- `legislation` - Acts, statutes, public laws
- `executive-order` - Presidential executive orders
- `supreme-court` - Court opinions
- `congressional-hearing` - Testimony, hearings
- `congressional-report` - Committee reports
- `presidential-document` - Messages, speeches, proclamations
- `regulatory` - Agency rules, regulations
- `historical-document` - Primary historical sources

**Topic Tags:**
- `federal-reserve`
- `income-tax`
- `emergency-powers`
- `gold-confiscation`
- `executive-power`
- `surveillance`
- `habeas-corpus`
- `administrative-state`
- `war-powers`

**Era Tags:**
- `progressive-era` (1900-1920)
- `new-deal` (1933-1939)
- `wwii` (1941-1945)
- `cold-war` (1947-1991)
- `post-911` (2001-present)

**Layer Tags (Continuum Report hierarchy):**
- `layer-executive-power` (this project)
- `layer-1-epstein` (existing)
- `layer-2-intelligence`
- `layer-3-financial`
- `layer-4-political`

## Execution Notes

1. **Rate Limiting**: Add delays between downloads (2-5 seconds) to avoid IP blocks
2. **User-Agent**: Use legitimate browser user-agent string
3. **Verification**: Check PDF integrity after download (file size, can open)
4. **Deduplication**: Check if document already exists before downloading
5. **Error Handling**: Log failures, continue with next document
6. **Progress Tracking**: Create manifest of acquired vs. pending documents

## Priority Order

Execute in this order:
1. Pujo Committee hearings (foundation for Federal Reserve narrative)
2. Pollock case + 16th Amendment materials
3. Executive Order 6102 + Emergency Banking Act
4. Youngstown case (executive power limits framework)
5. Church Committee reports (intelligence/surveillance)
6. Nixon Shock documents
7. War Powers / National Emergencies Act
8. APA / Chevron / administrative state
9. PATRIOT Act / FISA
10. Civil War era documents

## Success Criteria

- [ ] All Tier 1 documents acquired and ingested
- [ ] Tier 2 documents 80%+ acquired
- [ ] All documents properly tagged in Paperless-ngx
- [ ] Searchable by topic, era, document type
- [ ] Backup copies in processed directory
- [ ] Acquisition manifest complete with sources/dates

## Network Paths

- **SMB Share**: `\\Tower\paperless-consume\` or `/mnt/user/appdata/paperless/consume/`
- **Paperless Web UI**: Check Unraid Docker settings for port
- **API Endpoint**: `http://[tower-ip]:[port]/api/`

---

*This acquisition task supports The Continuum Report's mission to map power structures through rigorous analysis of primary source documents. All materials will be independently verifiable to support the decentralized intelligence network.*
