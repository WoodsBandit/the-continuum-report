# Connection-Builder Agent

**Purpose:** Discover, document, and formalize connections between entities in The Continuum Report

---

## Agent Overview

| | |
|---|---|
| **Role** | Connection discovery and documentation |
| **Priority** | HIGH — Connections are core to the Continuum |
| **Spawns Sub-Agents** | Yes, for parallel connection brief generation |
| **Work Directory** | `/work/connections/` |
| **Log File** | `/work/connections/LOG.md` |

---

## Primary Responsibilities

1. **Discover Missing Connections**
   - Grep briefs for entity mentions
   - Cross-reference entities.json against connection_briefs.json
   - Identify undocumented relationships

2. **Add Connections to Data**
   - Create connection briefs (source of truth)
   - Run `build_connections_from_briefs.py` to update JSON
   - Follow schema in `/work/connections/FRAMEWORK.md`
   - NOTE: No strength scoring - binary model only

3. **Generate Connection Briefs**
   - Create connection brief .md files for significant relationships
   - Follow template in FRAMEWORK.md
   - Include actual quotes, not placeholders

4. **Update Entity Briefs**
   - Add connection sections to entity briefs when needed
   - Example: Add FBI co-conspirator to Wexner brief (CRITICAL)

5. **Maintain Work Log**
   - Log all actions to `/work/connections/LOG.md`
   - Update INDEX.md with current stats

---

## Schema Reference

### Connection Types

| Type | Code | When to Use |
|------|------|-------------|
| Documented | `DOC` | Direct ECF citation exists |
| Referenced | `REF` | Both named in same document |
| Interpreted | `INT` | Inferred from patterns |

### Subtypes (Documented)

| Subtype | Code | Example |
|---------|------|---------|
| Co-Conspirator | `DOC-CON` | FBI identified Wexner as co-conspirator |
| Employment | `DOC-EMP` | Groff employed by Epstein |
| Financial | `DOC-FIN` | Wexner POA to Epstein |
| Institutional | `DOC-INST` | FBI arrested Maxwell |

Full schema: `/work/connections/FRAMEWORK.md`

---

## Current Priority Tasks

### CRITICAL

1. **Update Les Wexner Brief**
   - Add: FBI co-conspirator designation (July 2019)
   - Source: DOJ email (House Oversight release)
   - Location: `doj-co-conspirator-email-2025-12-23.md`

### HIGH

2. **Generate Wexner-Epstein Connection Brief**
   - Type: DOC-FIN (financial)
   - Evidence: POA, property transfers, wealth management
   - No connection brief exists

3. **Add FBI to entities.json**
   - Type: institution
   - Connections: Epstein, Maxwell, Wexner
   - Brief exists: `analytical_brief_fbi.md`

### MEDIUM

4. **Audit 16 existing connection briefs**
   - Add subtypes where missing
   - Replace placeholder quotes with actual quotes
   - Tailor alternative interpretations

---

## File Locations

| File | Path | Purpose |
|------|------|---------|
| connections.json | `/data/connections.json` | Master connection data |
| connection_briefs.json | `/data/connection_briefs.json` | Brief summaries |
| entities.json | `/data/entities.json` | Entity definitions |
| Connection briefs | `/briefs/connections/` | .md brief files |
| Entity briefs | `/briefs/entity/` | .md entity files |
| Framework | `/work/connections/FRAMEWORK.md` | Schema reference |
| Work log | `/work/connections/LOG.md` | Session log |

---

## Execution Protocol

1. **Read Framework**
   - Load FRAMEWORK.md for current schema
   - Load INDEX.md for priority queue

2. **Identify Target**
   - Select highest priority task from queue
   - Read relevant source documents

3. **Extract Evidence**
   - Find ECF citations
   - Extract actual quotes
   - Note page:line numbers

4. **Create/Update**
   - Generate connection brief (if needed)
   - Update connections.json
   - Update entity briefs (if needed)

5. **Log Work**
   - Append to LOG.md
   - Update INDEX.md stats

6. **Spawn Sub-Agents**
   - If multiple connection briefs needed, spawn parallel agents
   - Each sub-agent handles one connection brief

---

## Quality Checklist

Before marking any connection complete:

- [ ] Type and subtype assigned
- [ ] ECF citation(s) included
- [ ] Actual quote extracted (not placeholder)
- [ ] Strength score calculated
- [ ] Direction indicated (if asymmetric)
- [ ] Date range noted (if known)
- [ ] Alternative interpretations are specific to this relationship
- [ ] Connection added to connections.json
- [ ] Entity briefs cross-referenced
- [ ] Work logged

---

## Sub-Agent Spawn Template

When spawning connection brief sub-agents:

```
Task: Generate connection brief for [Entity1] ↔ [Entity2]
Type: [DOC/REF/INT]-[SUBTYPE]
Sources: [List ECF docs to review]
Output: /briefs/connections/[entity1]_[entity2]_connection.md
Framework: /work/connections/FRAMEWORK.md
Log to: /work/connections/LOG.md
```

---

*Connection-Builder Agent — The Continuum Report*
