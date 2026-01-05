# Data Consolidation Analysis

**Generated:** 2025-12-23
**Auditor:** Claude Code CC3

---

## Executive Summary

Two parallel data directories exist with **divergent content**. Neither is a subset of the other:
- **Development** (`/continuum/data/`) has RICHER schema (18 fields per entity) with ECF citations
- **Website** (`/continuum/website/data/`) has MORE entities (37 vs 15) with SIMPLER schema (8 fields)

**Recommendation:** Merge toward a UNIFIED schema that combines website's broader entity coverage with development's citation-rich format.

---

## Current State

| Location | entities.json | connections.json | Last Modified | File Size |
|----------|---------------|------------------|---------------|-----------|
| `/continuum/data/` | 15 entities | 95 connections | 2025-12-20 21:56 | 74 KB |
| `/continuum/website/data/` | 37 entities | 121 connections | 2025-12-19 19:48 | 16 KB |

---

## Schema Comparison

### entities.json

| Field | Development | Website | Notes |
|-------|-------------|---------|-------|
| id | ✅ | ✅ | Both |
| name | ✅ | ✅ | Both |
| type | ✅ | ✅ | Both |
| status | ✅ | ✅ | Both |
| summary | ✅ | ✅ | Both |
| brief_file | ✅ | ✅ | Both |
| mentions | ✅ | ✅ | Both |
| network | ❌ | ✅ | Website only |
| full_summary | ✅ | ❌ | Dev only - extended description |
| brief_url | ✅ | ❌ | Dev only - URL path |
| document_type | ✅ | ❌ | Dev only |
| primary_sources | ✅ | ❌ | Dev only - array of source docs |
| sources | ✅ | ❌ | Dev only |
| ecf_citations | ✅ | ❌ | Dev only - **CRITICAL for verification** |
| mention_details | ✅ | ❌ | Dev only |
| last_updated | ✅ | ❌ | Dev only |
| parsed_from | ✅ | ❌ | Dev only |
| connections | ✅ | ❌ | Dev only - embedded array |
| tags | ✅ | ❌ | Dev only |

**Development schema version:** Includes `schema_version` and `enriched: true` metadata

### connections.json

| Field | Development | Website | Notes |
|-------|-------------|---------|-------|
| source | ✅ | ✅ | Both |
| target | ✅ | ✅ | Both |
| strength | ✅ | ✅ | Both |
| type | ✅ | ✅ | Both |
| evidence | ✅ | ✅ | Both |
| bidirectional | ✅ | ❌ | Dev only |
| source_mentions_target | ✅ | ❌ | Dev only |
| target_mentions_source | ✅ | ❌ | Dev only |

---

## Unique Entities

### In Development Only
*(None - all 15 dev entities exist in website)*

### In Website Only (22 entities)
These represent historical/intelligence context entities:

**Intelligence/Government:**
- cia
- mossad
- william-casey
- oliver-north

**Financial:**
- bcci
- deutsche-bank
- meyer-lansky

**Historical Cases:**
- iran-contra-case
- promis-inslaw-case
- nxivm-case
- jpmorgan-epstein-case

**NXIVM-Related:**
- keith-raniere
- allison-mack
- clare-bronfman

**Epstein Network Extended:**
- robert-maxwell
- maxwell-family-network
- les-wexner
- jean-luc-brunel
- johanna-sjoberg
- juan-alessi
- roy-cohn
- intelligence-financial-nexus

---

## Analysis

### Why Development Files Are Larger Despite Fewer Entities

Development entities are **enriched** with:
1. **ECF Citations** - Direct court document references (critical for source verification)
2. **Embedded Connections** - Each entity contains its own connection array with sources
3. **Full Summaries** - Extended biographical/contextual information
4. **Source Tracking** - `parsed_from`, `last_updated`, `primary_sources`

This represents the **Citation Gap Audit** work - mapping entities to verifiable court documents.

### Why Website Has More Entities

Website includes **contextual entities** for the Zoom Framework visualization:
- Intelligence agencies (CIA, Mossad)
- Historical precedent cases (Iran-Contra, PROMIS)
- Extended network members not yet enriched

These provide navigation context but lack the citation depth of the core 15.

---

## Recommendation

**DO NOT simply replace one with the other.** Both contain unique value.

### Proposed Consolidation Approach

1. **Adopt Development Schema as Canonical**
   - 18-field schema provides verification capability
   - Add `network` field from website schema

2. **Merge Entity Sets**
   - Start with 37 website entities
   - Overlay the 15 enriched dev entities (they have same IDs)
   - Result: 37 entities, 15 with full enrichment, 22 with basic data

3. **Mark Enrichment Status**
   - Add `enriched: true/false` flag to each entity
   - 22 entities need enrichment work

4. **Merge Connection Sets**
   - Dev connections have bidirectionality data
   - Website has 26 additional connections (121 vs 95)
   - Merge keeping all unique connections

5. **Single Canonical Location**
   - Propose: `/continuum/data/` as canonical
   - Website reads from `/data/` via build/copy step
   - OR: symlink `/continuum/website/data/` → `/continuum/data/`

---

## Risk Assessment

| Action | Risk | Mitigation |
|--------|------|------------|
| Overwriting dev with website | LOSE all ECF citations, enrichment work | Don't do this |
| Overwriting website with dev | LOSE 22 entities, 26 connections | Don't do this |
| Merge without schema alignment | continuum.html may break | Test after merge |
| Symlink approach | Windows compatibility | Test on WoodsDen |
| Build/copy step | Data drift if forgotten | Automate deployment |

---

## Immediate Actions Required

1. **BACKUP BOTH** before any merge
2. **Schema decision** - Overseer to approve merged schema
3. **Enrichment priority** - Which of 22 new entities to enrich first?
4. **Deployment method** - Symlink vs build step?

---

*Analysis complete. Awaiting Overseer approval before any data modifications.*
