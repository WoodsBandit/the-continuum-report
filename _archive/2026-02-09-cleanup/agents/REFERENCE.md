# THE CONTINUUM REPORT — Custom Agent Reference

> **Location:** /continuum/agents/
> **Purpose:** Specialized AI agents for The Continuum Report project
> **Created:** 2025-12-24
> **Architecture:** Single Claude Code session spawns specialized Task agents

---

## Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MAIN SESSION (Overseer)                       │
│         Full project context, strategic coordination             │
│                                                                   │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │ Agent 1 │ │ Agent 2 │ │ Agent 3 │ │ Agent 4 │ │ Agent N │   │
│  │(parallel)│ │(parallel)│ │(parallel)│ │(parallel)│ │(parallel)│   │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘   │
│       │           │           │           │           │          │
│       └───────────┴───────────┴───────────┴───────────┘          │
│                           │                                       │
│                    Results flow back                              │
│                    to main session                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Agent Inventory

| # | Agent | File | Purpose | Status |
|---|-------|------|---------|--------|
| 1 | Legal Auditor | `legal-auditor.md` | First Amendment compliance, defamation protection | ✓ |
| 2 | Citation Mapper | `citation-mapper.md` | ECF → PDF linking, gap identification | ✓ |
| 3 | Connection Brief Generator | `connection-brief-generator.md` | Entity relationship documentation | ✓ |
| 4 | Visualization Expert | `visualization-expert.md` | continuum.html UI/UX | ✓ |
| 5 | Project Status Tracker | `project-status-tracker.md` | Status reports, gap analysis | ✓ |
| 6 | File Organizer | `file-organizer.md` | Canonical paths, deduplication | ✓ |
| 7 | Document Acquisition | `document-acquisition.md` | Download and organize sources | ✓ |
| 8 | Entity Extractor | `entity-extractor.md` | Extract entities from documents | ✓ |
| 9 | Paperless Integrator | `paperless-integrator.md` | Paperless-ngx API operations | ✓ |
| 10 | Financial Analyst | `financial-analyst.md` | Money flows, timelines | ✓ |
| 11 | Brief Generator | `brief-generator.md` | Full analytical briefs | ✓ |
| 12 | Cross-Reference Finder | `cross-reference-finder.md` | Connection discovery | ✓ |
| 13 | **Overseer** | `overseer.md` | **Meta-coordination, agent orchestration, synthesis** | ✓ Created 2025-12-24 |
| 14 | **QA Tester** | `qa-tester.md` | **Cross-browser, responsive, functional testing** | ✓ Created 2025-12-24 |

---

## How To Use Agents

### Spawning an Agent
```
Use Task tool with:
- subagent_type: "general-purpose"
- prompt: [Read agent file for full prompt]
- description: [Short task description]
```

### Parallel Execution
Multiple agents can be spawned simultaneously in a single message.
Results flow back to main session for synthesis.

### Agent Reports
All agents write reports to: `/continuum/reports/agent-outputs/`
Format: `{agent-name}_{task}_{date}.md`

---

## Project Context (All Agents Should Know)

### The Mission
The Continuum Report is an independent intelligence analysis project documenting
connections between power structures through primary source documents (court filings,
depositions, FOIA releases). Every claim must be independently verifiable.

**Tagline:** *Another Node in the Decentralized Intelligence Agency*

### Legal Framework
All content operates under First Amendment protections per *Milkovich v. Lorain Journal* (1990):
- Clearly labeled as editorial commentary
- Documented facts separated from interpretation
- Opinion-signaling language throughout
- Alternative interpretations provided
- Right of response invited

### Canonical Paths
| Resource | Path |
|----------|------|
| Entities | `/continuum/website/data/entities.json` |
| Connections | `/continuum/website/data/connections.json` |
| Entity Briefs | `/continuum/website/briefs/entity/` |
| Connection Briefs | `/continuum/website/briefs/connections/` |
| Source PDFs | `/continuum/website/sources/` |
| Reports | `/continuum/reports/` |
| Agent Outputs | `/continuum/reports/agent-outputs/` |
| Agent Definitions | `/continuum/agents/` |

### Current Asset Counts (as of 2025-12-24)
- 37 entities with analytical briefs
- 131 documented connections
- 85+ connection briefs
- 97+ source PDFs hosted
- 33,564 DOJ-OGR files (image-based, need OCR)

---

## Report Format Standard

All agents should output reports in this structure:

```markdown
# [AGENT NAME] Report — [Task Description]

**Agent:** [agent-name]
**Task:** [brief description]
**Date:** [YYYY-MM-DD HH:MM]
**Status:** [Complete/Partial/Blocked]

---

## Executive Summary
[2-3 sentences on what was accomplished]

## Findings
[Detailed results]

## Actions Taken
[What the agent did]

## Recommendations
[What should happen next]

## Blockers (if any)
[What prevented completion]

---
*Report generated by [agent-name] agent*
```

---

## Migration Notes

This agent system replaces the previous Expert Chat structure:
- Infrastructure Lead → citation-mapper + paperless-integrator
- Legal Framework → legal-auditor
- Connection Brief Methodology → connection-brief-generator
- Continuum Visualization → visualization-expert
- Comprehensive Project Status → project-status-tracker
- File Organization → file-organizer
- Landing Page → (handled by visualization-expert or main session)
- MISC → (handled by main session)
- CC1/CC2/CC3 Workers → (replaced by parallel agent spawning)

**Benefits:**
- Full context in single session
- True parallel execution
- No file-based communication overhead
- Results synthesized automatically

---

*Last Updated: 2025-12-24*
