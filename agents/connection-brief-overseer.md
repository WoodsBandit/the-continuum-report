# Connection Brief Overseer Agent

**Purpose:** Manage comprehensive review and enhancement of all connection briefs
**Work Directory:** `/agents/overseer/connection-brief-audit/`
**Log File:** `/agents/overseer/connection-brief-audit/LOG.md`
**Index:** `/agents/overseer/connection-brief-audit/INDEX.md`

---

## Agent Overview

| | |
|---|---|
| **Role** | Project management and quality assurance for connection briefs |
| **Scope** | 89 connection briefs, 38 entity briefs |
| **Spawns Sub-Agents** | Yes — for parallel brief processing |
| **Legal Compliance** | Required — Milkovich framework |

---

## Project Objectives

1. **Review all 89 connection briefs** for accuracy and completeness
2. **Cross-reference with entity briefs** to find additional source documentation
3. **Enhance each brief** with comprehensive entity-to-entity connections
4. **Add clickable source links** using PDF viewer format
5. **Run legal audit** on all updated briefs
6. **Integrate with continuum.html** and sources page

---

## Execution Protocol

### Phase 1: Index and Inventory

1. Verify CONNECTION_BRIEF_INDEX.md is complete
2. Map all entity relationships
3. Identify source documents for each connection
4. Log progress to LOG.md

### Phase 2: Source Cross-Reference

For each connection brief:
1. Read the brief
2. Identify ECF citations
3. Cross-reference with entity briefs for additional sources
4. Document all source locations

### Phase 3: Brief Enhancement

For each connection brief:
1. Add "All Entity Connections" section listing every related entity
2. Add clickable PDF viewer links: `[ECF Doc. XXXX](https://thecontinuumreport.com/sources/collection/filename.pdf)`
3. Ensure Alternative Interpretations section exists and is specific
4. Add cross-references to related briefs

### Phase 4: Legal Audit

Use legal-auditor agent or apply manually:
1. Verify Milkovich header present
2. Check "The Public Record" vs "Editorial Analysis" separation
3. Ensure Alternative Interpretations section exists
4. Verify Fifth Amendment context where applicable
5. Check all opinion language is properly qualified

### Phase 5: Website Integration

1. Update continuum.html data source with connection data
2. Add connection briefs to sources page
3. Verify PDF viewer links work
4. Test navigation between briefs

---

## Sub-Agent Spawn Protocol

When spawning sub-agents for parallel processing:

**Brief Review Sub-Agent:**
```
Task: Review and enhance connection brief [filename]
1. Read brief at /briefs/connections/[filename]
2. Read related entity briefs
3. Add "All Entity Connections" section
4. Add clickable source links (PDF viewer format)
5. Ensure legal compliance
6. Log completion to /agents/overseer/connection-brief-audit/LOG.md
```

**Batch Assignment:**
- Spawn 5-10 sub-agents in parallel
- Each handles 5-10 briefs
- All log to central LOG.md

---

## Quality Standards

### Required Sections in Each Connection Brief

1. **Header** — Milkovich editorial commentary notice
2. **Document Classification** — Subjects, type, sources
3. **The Public Record** — Factual content with ECF citations
4. **All Entity Connections** — Matrix of connections to other entities
5. **Editorial Analysis** — Clearly labeled opinion
6. **Alternative Interpretations** — 3+ interpretations specific to connection
7. **Source Documents** — Table with clickable PDF links
8. **Cross-References** — Links to related briefs

### Link Format Requirements

**PDF Viewer Links:**
```markdown
[ECF Doc. 1320-38](https://thecontinuumreport.com/sources/giuffre-v-maxwell/ecf-1320-38.pdf)
```

**Brief Cross-References:**
```markdown
See [Entity Brief](../entity/analytical_brief_name.md)
See [Connection Brief](related_connection.md)
```

---

## File Locations

| Resource | Path |
|----------|------|
| Work directory | `/agents/overseer/connection-brief-audit/` |
| Index | `/agents/overseer/connection-brief-audit/INDEX.md` |
| Log | `/agents/overseer/connection-brief-audit/LOG.md` |
| Master brief index | `/briefs/connections/CONNECTION_BRIEF_INDEX.md` |
| Connection briefs | `/briefs/connections/` |
| Entity briefs | `/briefs/entity/` |
| Legal auditor | `/agents/legal-auditor.md` |
| PDF sources | `/website/sources/` |

---

## Progress Tracking

Update LOG.md after each action:
- Brief reviewed
- Brief enhanced
- Legal audit passed
- Website integration complete

Update INDEX.md with:
- Phase progress percentages
- Completed brief counts
- Issue flags

---

*Connection Brief Overseer Agent — The Continuum Report*
