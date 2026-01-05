# Claude Code Agents — Index

> Quick reference for Claude Code agent system and session context.

**Last Updated:** 2025-12-26

---

## Agent Definitions

| Agent | File | Purpose |
|-------|------|---------|
| brief-generator | `brief-generator.md` | Generate full analytical briefs |
| citation-mapper | `citation-mapper.md` | ECF → PDF source linking |
| connection-brief-generator | `connection-brief-generator.md` | Relationship documentation |
| document-acquisition | `document-acquisition.md` | Download source documents |
| entity-extractor | `entity-extractor.md` | Extract entities from documents |
| epstein-extractor | `epstein-extractor.md` | Parallel Epstein document extraction |
| financial-analyst | `financial-analyst.md` | Money flow analysis |
| legal-auditor | `legal-auditor.md` | First Amendment compliance |
| project-status | `project-status.md` | Status reports |
| qa-tester | `qa-tester.md` | Cross-browser, responsive testing |

---

## Project Rules

| Rule | File | Purpose |
|------|------|---------|
| Legal Framework | `../rules/legal-framework.md` | Milkovich opinion protection |
| Source Citation | `../rules/source-citation.md` | ECF citation standards |

---

## Session Logs

| Date | Session | Summary |
|------|---------|---------|
| 2025-12-26 | Remote Access Investigation | Searched for Tailscale project; documented .claude structure |

See: [log.md](log.md) for full session details.

---

## Context Storage

Claude Code per-project context location:

```
/continuum/.claude/
├── agents/           # This directory — agent definitions
│   ├── index.md      # This file
│   ├── log.md        # Session log
│   └── *.md          # Agent definitions
├── rules/            # Project rules (injected into context)
└── settings.json     # Permissions, env vars, model
```

**Note:** Claude Code does NOT persist conversation transcripts. Each session starts fresh, reading only:
- `CLAUDE.md` — Project instructions
- `.claude/settings.json` — Permissions
- `.claude/rules/*.md` — Rules
- `.claude/agents/*.md` — Agent definitions

To preserve session context, manually document in `log.md`.

---

## Quick Links

| Resource | Location |
|----------|----------|
| Main Project Context | `/continuum/CLAUDE.md` |
| Session Activity Log | `/continuum/log.md` |
| Agent Definitions (alt) | `/continuum/agents/` |
| Technical Infrastructure | `/continuum/config/technical_infrastructure.md` |

---

*Another Node in the Decentralized Intelligence Agency*
