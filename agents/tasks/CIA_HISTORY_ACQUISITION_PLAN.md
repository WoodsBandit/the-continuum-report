# CIA HISTORY DOCUMENT ACQUISITION PLAN

**Theme:** Intelligence History - CIA & OSS Era Documentation
**Created:** 2025-12-25
**Status:** IN PROGRESS - Phase 1 Partially Complete
**Priority:** HIGH
**Estimated Scope:** 150-200+ documents across 5 eras

---

## CRITICAL OPERATIONAL NOTES

### This is a LARGE MULTI-SESSION TASK

**DO NOT attempt to complete in one session.** This acquisition spans 5 historical eras and 150+ documents. Work is designed to be:

1. **Broken into discrete phases** - Complete one phase per session
2. **Frequently checkpointed** - Update this document after EACH document or batch
3. **Resumable** - Any session can pick up exactly where the last left off
4. **Parallelizable** - Multiple agents can work different eras simultaneously

### Progress Saving Protocol

After EVERY acquisition batch (5-10 documents):
1. Update the `## Progress Tracker` section below with completed items
2. Update `## Session Log` with timestamp and actions
3. If interrupted, document exactly where you stopped
4. Create `DOWNLOAD_SUMMARY.txt` in each era folder

### Agent Spawning for Parallel Work

The Overseer can spawn multiple Document Acquisition agents simultaneously:
- **Agent 1:** OSS Era documents
- **Agent 2:** Early CIA documents
- **Agent 3:** Cold War Peak documents
- **Agent 4:** Late Cold War documents
- **Agent 5:** Modern Era documents

Each agent works its assigned era, updates its section of this document, and reports completion.

---

## COMPREHENSIVE PROGRESS ANALYSIS

### Current State (as of 2025-12-25)

#### COMPLETED ACQUISITIONS

| Era | Folder | Documents | Size | Status |
|-----|--------|-----------|------|--------|
| **Foundational** | `/cia-history/foundational/` | 7 | ~200MB | COMPLETE |
| **Cold War Peak** | `/cia-history/cold-war-peak/` | 1 | ~25MB | PARTIAL |
| **Late Cold War** | `/cia-history/late-cold-war/` | 6 | ~940MB | COMPLETE |
| **Modern Era** | `/cia-history/modern-era/` | 4 | ~50MB | PARTIAL |
| **OSS Era** | `/cia-history/oss-era/` | 0 | 0 | NOT STARTED |
| **Early CIA** | `/cia-history/early-cia/` | 0 | 0 | NOT STARTED |

**Total Acquired:** 18 PDFs (~1.2GB)
**Total Remaining:** ~130-180 documents (estimated)

#### Detailed Inventory of Completed Documents

**Foundational (Church Committee) - COMPLETE:**
```
church_committee_assassination_plots.pdf
church_committee_vol1_foreign_military_intel.pdf
church_committee_vol2_rights_of_americans.pdf
church_committee_vol3_supplementary_staff_reports.pdf
church_committee_vol4_supplementary_staff_reports.pdf
church_committee_vol5_jfk_assassination.pdf
church_committee_vol6_supplementary_reports.pdf
```

**Cold War Peak - PARTIAL:**
```
cia_family_jewels_1973.pdf
```
*Remaining: MKUltra documents, Operation CHAOS, Phoenix Program*

**Late Cold War (Iran-Contra) - COMPLETE:**
```
tower_commission_report_1987.pdf (57MB)
iran_contra_congressional_report_1987.pdf (55MB)
iran_contra_walsh_report_1993_complete.pdf (413MB)
iran_contra_walsh_report_1993_vol1.pdf (124MB)
iran_contra_walsh_report_1993_vol2.pdf (101MB)
iran_contra_walsh_report_1993_vol3.pdf (188MB)
```

**Modern Era - PARTIAL:**
```
9-11_commission_report_2004.pdf
9-11_commission_executive_summary.pdf
senate_torture_report_executive_summary_2014.pdf
senate_torture_report_findings_2014.pdf
```
*Remaining: Torture memos, Snowden documents, Drone memos, Haspel cables*

---

## ACQUISITION PHASES

### PHASE 1: FOUNDATIONAL & LEGISLATIVE (COMPLETE)
**Status:** DONE
- [x] Church Committee volumes 1-6
- [x] Church Committee Assassination Report
- [x] Iran-Contra reports (Tower, Congressional, Walsh)

### PHASE 2: EARLY CIA ERA (1947-1960) - NOT STARTED
**Priority:** HIGH - Foundation for understanding all later operations
**Estimated Documents:** 25-35
**Research File:** `/continuum/research/cia-history/02_early_cia_1947-1960.md`

#### Phase 2A: Founding Documents
| Document | Source | URL Pattern | Status |
|----------|--------|-------------|--------|
| National Security Act of 1947 | GPO/NARA | govinfo.gov | PENDING |
| Executive Order 9621 (OSS Dissolution) | Federal Register | archives.gov | PENDING |
| CIA Cold War Records: Truman Era | CIA History | cia.gov/readingroom | PENDING |
| CIG Establishment Documents | NARA | archives.gov | PENDING |

#### Phase 2B: Operation TPAJAX (Iran 1953)
| Document | Source | URL Pattern | Status |
|----------|--------|-------------|--------|
| "ZENDEBAD, SHAH!" Internal History (2017) | CIA FOIA | cia.gov/readingroom | PENDING |
| TPAJAX Planning Documents | State Dept FRUS | history.state.gov | PENDING |
| CIA Confirmation Documents (2013) | NSA/CIA FOIA | nsarchive.gwu.edu | PENDING |
| Eisenhower Authorization Records | Eisenhower Library | eisenhowerlibrary.gov | PENDING |

#### Phase 2C: Operation PBSUCCESS (Guatemala 1954)
| Document | Source | URL Pattern | Status |
|----------|--------|-------------|--------|
| Cullather "Operation PBSUCCESS" CIA History | CIA CSI | cia.gov | PENDING |
| Assassination Planning Documents (DOC_0000135796) | CIA FOIA | cia.gov/readingroom | PENDING |
| PBSUCCESS Core Documents (DOC_0000134974) | CIA FOIA | cia.gov/readingroom | PENDING |
| FRUS Guatemala 1952-54 Volume | State Dept | history.state.gov | PENDING |
| NSA Guatemala Assassination Documents | NSA | nsarchive.gwu.edu | PENDING |

#### Phase 2D: Operation Paperclip
| Document | Source | URL Pattern | Status |
|----------|--------|-------------|--------|
| CIA Paperclip Documents (267 pages) | CIA FOIA/Black Vault | theblackvault.com | PENDING |
| FBI Paperclip Files (32 pages) | FBI/Black Vault | theblackvault.com | PENDING |
| Truman Library Paperclip Materials | Truman Library | trumanlibrary.gov | PENDING |

#### Phase 2E: MKULTRA & Mind Control
| Document | Source | URL Pattern | Status |
|----------|--------|-------------|--------|
| MKULTRA Documents (CIA-06760269) | CIA FOIA | cia.gov/readingroom | PENDING |
| NSA Behavioral Sciences Collection (1,200+ docs) | NSA | nsarchive.gwu.edu | PENDING |
| Project BLUEBIRD Materials | NSA | nsarchive.gwu.edu | PENDING |
| Project ARTICHOKE Records | NSA | nsarchive.gwu.edu | PENDING |
| John Marks FOIA Collection | NSA | nsarchive.gwu.edu | PENDING |

### PHASE 3: OSS ERA (1942-1945) - NOT STARTED
**Priority:** MEDIUM - Historical foundation
**Estimated Documents:** 20-30
**Research File:** `/continuum/research/cia-history/01_oss_era_1942-1945.md`

| Document Category | Source | Status |
|-------------------|--------|--------|
| OSS Founding Executive Orders | NARA/Federal Register | PENDING |
| Executive Order 9621 (Dissolution) | Federal Register | PENDING |
| Fritz Kolbe/George Wood Collection (sample) | NARA RG 226 | PENDING |
| Operation Sunrise Records | NARA | PENDING |
| OSS Personnel Files (Dulles, Helms, Wisner) | NARA | PENDING |
| OSS Field Manual No. 2 (Sabotage) | Internet Archive | PENDING |
| R&A Branch Reports (samples) | CIA FOIA | PENDING |
| SSU Transition Documents | NARA RG 226 | PENDING |

### PHASE 4: COLD WAR PEAK (1960-1975) - PARTIAL
**Priority:** HIGH - Key scandal documentation
**Estimated Documents:** 30-40
**Research File:** `/continuum/research/cia-history/03_cold_war_peak_1960-1975.md`

| Document Category | Source | Status |
|-------------------|--------|--------|
| CIA Family Jewels (702 pages) | CIA FOIA | COMPLETE |
| Rockefeller Commission Report | NARA | PENDING |
| Pike Committee Materials | NARA | PENDING |
| Operation CHAOS Documents | CIA FOIA | PENDING |
| Phoenix Program Records | CIA FOIA/NSA | PENDING |
| Bay of Pigs After-Action | CIA FOIA | PENDING |
| COINTELPRO Documents (FBI) | FBI Vault | PENDING |
| Watergate CIA Involvement | NARA | PENDING |
| KUBARK Manual (1963) | NSA | PENDING |
| Human Resource Exploitation Manual | NSA | PENDING |

### PHASE 5: LATE COLD WAR (1975-1991) - COMPLETE
**Status:** DONE
- [x] Tower Commission Report
- [x] Iran-Contra Congressional Report
- [x] Walsh Report (complete + volumes)

*Optional additions:*
- [ ] BCCI Investigation Records
- [ ] October Surprise Documents
- [ ] Reagan NSC Records

### PHASE 6: MODERN ERA (1991-PRESENT) - PARTIAL
**Priority:** HIGH - Recent accountability documents
**Estimated Documents:** 40-50
**Research File:** `/continuum/research/cia-history/05_modern_era_1991-present.md`

#### Completed:
- [x] 9/11 Commission Report
- [x] 9/11 Commission Executive Summary
- [x] Senate Torture Report Executive Summary
- [x] Senate Torture Report Findings

#### Remaining:

| Document | Source | Status |
|----------|--------|--------|
| **Torture Memos** |
| Bybee Memo #1 (Standards of Conduct) | DOJ OLC | PENDING |
| Bybee Memo #2 (Interrogation of al-Qaeda) | DOJ OLC | PENDING |
| Yoo Military Interrogation Memo | ACLU | PENDING |
| Levin Replacement Memo | DOJ OLC | PENDING |
| **Rendition & Black Sites** |
| Gina Haspel Torture Cables (12) | NSA | PENDING |
| European Parliament Report (2007) | EU Parliament | PENDING |
| ECHR Rulings (Abu Zubaydah, Al Nashiri) | ECHR | PENDING |
| **Surveillance** |
| Snowden SIDtoday Files | The Intercept | PENDING |
| OLC Stellar Wind Memo | DOJ OLC | PENDING |
| **Targeted Killing** |
| OLC Awlaki Memo (David Barron) | DOJ OLC/ACLU | PENDING |
| **Pre-9/11** |
| Phoenix Memo | FBI/DOJ IG | PENDING |
| CIA IG Report on 9/11 | CIA FOIA | PENDING |

---

## PROGRESS TRACKER

### Session Checkpoints

Use this section to track progress within and across sessions:

```
[SESSION DATE] [PHASE] [ACTION] [DOCUMENTS] [STATUS]
```

**Example entries:**
```
2025-12-25 PHASE-2A Downloaded National Security Act COMPLETE
2025-12-25 PHASE-2B Downloaded ZENDEBAD SHAH (3 parts) COMPLETE
2025-12-25 PHASE-2C Started Cullather download IN PROGRESS - 50%
```

### Active Checkpoint Log:

```
2025-12-25 ASSESSMENT Comprehensive analysis complete DONE
2025-12-25 PHASE-1 All foundational documents verified COMPLETE
```

---

## SESSION LOG

### 2025-12-25 00:10 - Initial Assessment Session

**Operator:** WoodsBandit
**Actions:**
- Analyzed all 5 research files in `/research/cia-history/`
- Inventoried existing downloads in `/website/sources/cia-history/`
- Confirmed 18 PDFs (~1.2GB) already acquired
- Identified ~130-180 remaining documents
- Created this comprehensive work plan

**Findings:**
- Late Cold War (Iran-Contra) is COMPLETE
- Foundational (Church Committee) is COMPLETE
- OSS Era and Early CIA are NOT STARTED
- Cold War Peak and Modern Era are PARTIAL

**Next Session Priority:**
1. Begin Phase 2A (Early CIA Founding Documents)
2. Download National Security Act of 1947
3. Download "ZENDEBAD, SHAH!" Iran coup history
4. Download Cullather Guatemala report

---

## SOURCE URLS REFERENCE

### CIA FOIA Reading Room
```
Base: https://www.cia.gov/readingroom/
Search: https://www.cia.gov/readingroom/search/site/
Collections: https://www.cia.gov/readingroom/collection/
```

### National Security Archive (GWU)
```
Base: https://nsarchive.gwu.edu/
Torture Archive: https://nsarchive.gwu.edu/project/torture-archive
Iran 1953: https://nsarchive.gwu.edu/briefing-book/iran/
Guatemala 1954: https://nsarchive.gwu.edu/briefing-book/guatemala/
MKULTRA: https://nsarchive.gwu.edu/briefing-book/intelligence/
```

### State Department FRUS
```
Base: https://history.state.gov/historicaldocuments
Iran 1951-54: https://history.state.gov/historicaldocuments/frus1951-54Iran
Guatemala: https://history.state.gov/historicaldocuments/frus1952-54Guat
```

### DOJ Office of Legal Counsel
```
Memos: https://www.justice.gov/olc/opinions
Torture: https://www.justice.gov/olc/opinions?keys=interrogation
```

### The Intercept (Snowden)
```
Snowden Archive: https://theintercept.com/snowden-sidtoday/
Document Search: https://theintercept.com/document/
```

### Internet Archive
```
OSS Manuals: https://archive.org/search.php?query=OSS+field+manual
Historical Reports: https://archive.org/details/texts
```

### The Black Vault
```
CIA: https://www.theblackvault.com/documentarchive/cia/
Paperclip: https://www.theblackvault.com/documentarchive/operation-paperclip/
MKULTRA: https://www.theblackvault.com/documentarchive/cia-mkultra-collection/
```

---

## AGENT COORDINATION PROTOCOL

### For Parallel Execution

When spawning multiple agents:

1. **Assign each agent ONE phase** from the list above
2. **Each agent updates ONLY its phase section** in Progress Tracker
3. **Agents do NOT overlap** - each era is owned by one agent
4. **Upon completion**, agent writes summary to Session Log
5. **Overseer consolidates** results after all agents complete

### Agent Task Template

When spawning a document acquisition agent, use this prompt structure:

```
You are the Document Acquisition Agent for The Continuum Report.

TASK: Complete Phase [X] of the CIA History Acquisition Plan

WORK PLAN LOCATION: \\192.168.1.139\continuum\agents\tasks\CIA_HISTORY_ACQUISITION_PLAN.md

SCOPE: [List specific documents for this phase]

INSTRUCTIONS:
1. Read the full work plan first
2. Navigate to your assigned phase
3. Download documents one at a time
4. Verify each download (file type, size, content)
5. Move to /continuum/website/sources/cia-history/[era]/
6. Copy to /continuum/documents/inbox/ for Paperless
7. Update Progress Tracker after EACH document
8. Create DOWNLOAD_SUMMARY.txt in the era folder
9. Update Session Log when complete

CHECKPOINTING: After every 5 documents, update the work plan file.

OUTPUT LOCATION: /continuum/website/sources/cia-history/[era]/

REPORT BACK: Summary of documents acquired, any failures, next steps
```

---

## QUALITY CHECKLIST

Before marking any phase COMPLETE:

- [ ] All PDFs verified as valid (file command)
- [ ] All PDFs have content (pdftotext extraction works)
- [ ] Naming convention followed
- [ ] Files in correct /sources/cia-history/[era]/ folder
- [ ] Copies sent to Paperless inbox
- [ ] DOWNLOAD_SUMMARY.txt created in folder
- [ ] Progress Tracker updated
- [ ] Session Log entry added
- [ ] No duplicate files

---

## ESTIMATED TIMELINE

| Phase | Documents | Sessions | Priority |
|-------|-----------|----------|----------|
| Phase 2 (Early CIA) | 25-35 | 2-3 | HIGH |
| Phase 3 (OSS Era) | 20-30 | 1-2 | MEDIUM |
| Phase 4 (Cold War Peak) | 30-40 | 2-3 | HIGH |
| Phase 6 (Modern Era) | 40-50 | 3-4 | HIGH |
| **TOTAL** | **115-155** | **8-12 sessions** | |

*Note: Sessions can run in parallel. With 3 parallel agents, work could complete in 3-4 sessions.*

---

## RESUMPTION INSTRUCTIONS

**For any future session picking up this task:**

1. Read this entire document first
2. Check the `Progress Tracker` section for last checkpoint
3. Check the `Session Log` for context on last session
4. Identify which phase is IN PROGRESS or next PENDING
5. Continue from exactly where the last session stopped
6. Update Progress Tracker frequently as you work
7. Add your own Session Log entry when done

---

**Document Version:** 1.0
**Last Updated:** 2025-12-25 00:30
**Maintainer:** The Continuum Report - Document Acquisition Team
