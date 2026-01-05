# TASK: Executive Power Expansion Document Acquisition

## Mission
Download primary source documents tracing the expansion of executive power from the Tea Tax revolt to modern income tax withholding. These documents form Layer 6 of The Continuum Report.

---

## BACKUP & PERMISSIONS (REQUIRED)

After creating ANY file:
```bash
chmod 666 <filename>
chown nobody:users <filename>
```

At end of task:
```bash
find /continuum -type f -newer /continuum/progress_executive_power.json -exec chmod 666 {} \;
find /continuum -type d -exec chmod 777 {} \;
chown -R nobody:users /continuum/
```

---

## Infrastructure
- Download directory: /continuum/downloads/executive-power/
- Paperless-ngx: http://192.168.1.139:8040
- API Token: da99fe6aa0b8d021689126cf72b91986abbbd283
- Progress file: /continuum/progress_executive_power.json

---

## Create Directory Structure First
```bash
mkdir -p /continuum/downloads/executive-power/{tier1,tier2,tier3,tier4}
```

---

## TIER 1: CRITICAL PRIMARY SOURCES (Download First)

### 1.1 Federal Reserve Creation

**PUJO COMMITTEE HEARINGS (1912-1913) - "Money Trust Investigation"**
- Source: https://publicintelligence.net/pujo-committee-money-trust-wall-street-banking-cartel-investigation-1912-1913/
- Files: 29 parts + exhibits + final report
- Filename: 1912-1913-PUJO-COMMITTEE-MONEY-TRUST-PART-{XX}.pdf
- Tags: pujo-committee, federal-reserve, money-trust, 1912, congressional-hearing, tier1

**FEDERAL RESERVE ACT (1913)**
- Source: https://www.govinfo.gov/content/pkg/STATUTE-38/pdf/STATUTE-38-Pg251.pdf
- Alt: https://fraser.stlouisfed.org/title/federal-reserve-act-968
- Filename: 1913-FEDERAL-RESERVE-ACT-STATUTE-38.pdf
- Tags: federal-reserve-act, 1913, legislation, banking, tier1

### 1.2 Income Tax & 16th Amendment

**POLLOCK v. FARMERS' LOAN & TRUST CO. (1895)**
- Source: https://tile.loc.gov/storage-services/service/ll/usrep/usrep157/usrep157429/usrep157429.pdf
- Filename: 1895-POLLOCK-V-FARMERS-LOAN-TRUST-157-US-429.pdf
- Tags: pollock, income-tax, supreme-court, 1895, unconstitutional, tier1

**POLLOCK REHEARING (1895)**
- Source: https://tile.loc.gov/storage-services/service/ll/usrep/usrep158/usrep158601/usrep158601.pdf
- Filename: 1895-POLLOCK-REHEARING-158-US-601.pdf
- Tags: pollock, income-tax, supreme-court, 1895, tier1

**BRUSHABER v. UNION PACIFIC (1916)**
- Source: https://tile.loc.gov/storage-services/service/ll/usrep/usrep240/usrep240001/usrep240001.pdf
- Filename: 1916-BRUSHABER-V-UNION-PACIFIC-240-US-1.pdf
- Tags: brushaber, income-tax, supreme-court, 1916, 16th-amendment, tier1

**REVENUE ACT OF 1913 (Underwood-Simmons Tariff)**
- Source: https://www.govinfo.gov/ (search "38 Stat. 114")
- Filename: 1913-REVENUE-ACT-UNDERWOOD-SIMMONS.pdf
- Tags: revenue-act, 1913, income-tax, legislation, tier1

### 1.3 Emergency Powers - Gold Confiscation

**EXECUTIVE ORDER 6102 (April 5, 1933)**
- Source: https://www.presidency.ucsb.edu/documents/executive-order-6102-requiring-gold-coin-gold-bullion-and-gold-certificates-be-delivered
- Alt: Federal Register / National Archives
- Filename: 1933-EXECUTIVE-ORDER-6102-GOLD-CONFISCATION.pdf
- Tags: executive-order, gold-confiscation, 1933, fdr, emergency-powers, tier1

**EMERGENCY BANKING ACT (1933)**
- Source: https://www.govinfo.gov/ (search "48 Stat. 1")
- Filename: 1933-EMERGENCY-BANKING-ACT.pdf
- Tags: emergency-banking-act, 1933, fdr, bank-holiday, tier1

**TRADING WITH THE ENEMY ACT (1917)**
- Source: https://www.govinfo.gov/ (search "40 Stat. 411")
- Filename: 1917-TRADING-WITH-ENEMY-ACT.pdf
- Tags: twea, 1917, wwi, emergency-powers, wilson, tier1

**GOLD RESERVE ACT (1934)**
- Source: https://www.govinfo.gov/ (search "48 Stat. 337")
- Filename: 1934-GOLD-RESERVE-ACT.pdf
- Tags: gold-reserve-act, 1934, fdr, tier1

### 1.4 Steel Seizure & Executive Power Limits

**YOUNGSTOWN SHEET & TUBE v. SAWYER (1952)**
- Source: https://tile.loc.gov/storage-services/service/ll/usrep/usrep343/usrep343579/usrep343579.pdf
- Filename: 1952-YOUNGSTOWN-STEEL-SEIZURE-343-US-579.pdf
- Tags: youngstown, steel-seizure, supreme-court, 1952, jackson-framework, tier1

---

## TIER 2: SUPPORTING PRIMARY SOURCES

### 2.1 Nixon Shock & End of Gold Standard

**EXECUTIVE ORDER 11615 (August 15, 1971)**
- Source: https://www.presidency.ucsb.edu/documents/executive-order-11615-providing-for-stabilization-prices-rents-wages-and-salaries
- Filename: 1971-EXECUTIVE-ORDER-11615-NIXON-SHOCK.pdf
- Tags: executive-order, nixon-shock, 1971, gold-standard, tier2

**NIXON ADDRESS TO THE NATION (August 15, 1971)**
- Source: https://www.presidency.ucsb.edu/documents/address-the-nation-outlining-new-economic-policy-the-challenge-peace
- Filename: 1971-NIXON-ADDRESS-NEW-ECONOMIC-POLICY.pdf
- Tags: nixon, speech, 1971, gold-window, tier2

### 2.2 War Powers & National Emergencies

**WAR POWERS RESOLUTION (1973)**
- Source: https://www.govinfo.gov/ (search "87 Stat. 555")
- Filename: 1973-WAR-POWERS-RESOLUTION.pdf
- Tags: war-powers, 1973, nixon, congressional-oversight, tier2

**NATIONAL EMERGENCIES ACT (1976)**
- Source: https://www.govinfo.gov/ (search "90 Stat. 1255")
- Filename: 1976-NATIONAL-EMERGENCIES-ACT.pdf
- Tags: national-emergencies-act, 1976, tier2

**INTERNATIONAL EMERGENCY ECONOMIC POWERS ACT (1977)**
- Source: https://www.govinfo.gov/ (search "91 Stat. 1626")
- Filename: 1977-IEEPA.pdf
- Tags: ieepa, 1977, emergency-powers, sanctions, tier2

### 2.3 Civil War Era

**EX PARTE MERRYMAN (1861)**
- Source: https://tile.loc.gov/storage-services/service/ll/llst/llst017/llst017.pdf
- Filename: 1861-EX-PARTE-MERRYMAN-TANEY.pdf
- Tags: merryman, habeas-corpus, lincoln, taney, 1861, civil-war, tier2

**EX PARTE MILLIGAN (1866)**
- Source: https://tile.loc.gov/storage-services/service/ll/usrep/usrep71/usrep71002/usrep71002.pdf
- Filename: 1866-EX-PARTE-MILLIGAN-71-US-2.pdf
- Tags: milligan, military-tribunals, supreme-court, 1866, tier2

**HABEAS CORPUS SUSPENSION ACT (1863)**
- Source: https://www.govinfo.gov/ (search "12 Stat. 755")
- Filename: 1863-HABEAS-CORPUS-SUSPENSION-ACT.pdf
- Tags: habeas-corpus, 1863, lincoln, civil-war, tier2

---

## TIER 3: ADMINISTRATIVE STATE

**ADMINISTRATIVE PROCEDURE ACT (1946)**
- Source: https://www.govinfo.gov/ (search "60 Stat. 237")
- Filename: 1946-ADMINISTRATIVE-PROCEDURE-ACT.pdf
- Tags: apa, 1946, administrative-state, regulatory, tier3

**CHEVRON v. NRDC (1984)**
- Source: https://tile.loc.gov/storage-services/service/ll/usrep/usrep467/usrep467837/usrep467837.pdf
- Filename: 1984-CHEVRON-V-NRDC-467-US-837.pdf
- Tags: chevron-deference, supreme-court, 1984, regulatory, tier3

**LOPER BRIGHT v. RAIMONDO (2024)**
- Source: https://www.supremecourt.gov/opinions/23pdf/22-451_7m58.pdf
- Filename: 2024-LOPER-BRIGHT-CHEVRON-OVERTURNED.pdf
- Tags: loper-bright, chevron-overturned, supreme-court, 2024, tier3

---

## TIER 4: SURVEILLANCE STATE

**USA PATRIOT ACT (2001)**
- Source: https://www.govinfo.gov/content/pkg/PLAW-107publ56/pdf/PLAW-107publ56.pdf
- Filename: 2001-USA-PATRIOT-ACT.pdf
- Tags: patriot-act, 2001, surveillance, post-911, tier4

**FOREIGN INTELLIGENCE SURVEILLANCE ACT (1978)**
- Source: https://www.govinfo.gov/ (search "92 Stat. 1783")
- Filename: 1978-FISA-FOREIGN-INTELLIGENCE-SURVEILLANCE-ACT.pdf
- Tags: fisa, 1978, surveillance, intelligence, tier4

---

## EXECUTION INSTRUCTIONS

1. Create directory structure
2. Download each document using curl or wget
3. Verify PDF integrity (file size > 0, valid PDF header)
4. Log each download to /continuum/progress_executive_power.json
5. After all downloads complete, upload to Paperless-ngx using API
6. Apply tags as specified above
7. Add 2-second delay between downloads to avoid rate limiting

---

## PAPERLESS-NGX UPLOAD

For each document, first create any tags that don't exist:
```bash
curl -X POST "http://192.168.1.139:8040/api/tags/" \
  -H "Authorization: Token da99fe6aa0b8d021689126cf72b91986abbbd283" \
  -H "Content-Type: application/json" \
  -d '{"name": "TAG_NAME"}'
```

Then upload document:
```bash
curl -X POST "http://192.168.1.139:8040/api/documents/post_document/" \
  -H "Authorization: Token da99fe6aa0b8d021689126cf72b91986abbbd283" \
  -F "document=@/continuum/downloads/executive-power/tier1/FILENAME.pdf" \
  -F "title=DOCUMENT TITLE"
```

---

## PROGRESS TRACKING

Save progress after each successful download to /continuum/progress_executive_power.json:
```json
{
  "task": "Executive Power Document Acquisition",
  "started": "ISO_TIMESTAMP",
  "tier1_complete": false,
  "tier2_complete": false,
  "tier3_complete": false,
  "tier4_complete": false,
  "documents_downloaded": [],
  "documents_failed": [],
  "documents_ingested": []
}
```

---

## SUCCESS CRITERIA

- [ ] All Tier 1 documents (11 files) downloaded
- [ ] All Tier 2 documents (8 files) downloaded
- [ ] All Tier 3 documents (3 files) downloaded
- [ ] All Tier 4 documents (2 files) downloaded
- [ ] All documents uploaded to Paperless-ngx
- [ ] All documents tagged appropriately
- [ ] Progress file updated
- [ ] Permissions set for SMB access

---

## FILE PERMISSIONS (REQUIRED - RUN AT END)

```bash
find /continuum/downloads/executive-power -type f -exec chmod 666 {} \;
find /continuum/downloads/executive-power -type d -exec chmod 777 {} \;
chown -R nobody:users /continuum/downloads/executive-power/
chmod 666 /continuum/progress_executive_power.json
chown nobody:users /continuum/progress_executive_power.json
```

---

*This collection traces a question every American should be able to answer: How did a nation founded by men who revolted over a tea tax come to accept a government that takes their earnings before they ever see them? These primary sources document that journey — the executive orders, court decisions, and legislative maneuvers that transformed "limited government" from founding principle to historical footnote.*

*The Continuum Report — Another Node in the Decentralized Intelligence Agency*
