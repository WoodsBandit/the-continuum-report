# Continuum.html Implementation Prompts
## The Continuum Report - Visualization System Overhaul

---

## Overview

This folder contains 5 phased prompts for Claude Code to implement the comprehensive update to `continuum.html`. Each phase builds upon the previous and includes:

- **Phase detection** - Automatically checks if the phase is already complete
- **Prerequisite verification** - Ensures previous phases are done
- **Backup protocol** - Creates versioned backups before changes
- **Detailed implementation** - Specific code and instructions
- **Verification checklist** - Items to confirm completion
- **Completion report** - Standard output format with next steps

---

## Phase Summary

| Phase | Name | Purpose |
|-------|------|---------|
| **1** | Macro Tab Update | Change box labels, add gold lines, remove Sources layer |
| **2** | Entities Layer | Build zoomable card grid, filter search bar |
| **3** | Web Layer | Entity colors, gradients, top-down gravity, focal emphasis |
| **4** | Connections Panel | Dropdown expansion, summaries, source links |
| **5** | Connection Briefs | Generate brief documents with legal protections |

---

## How to Use

### Running a Phase

1. Copy the entire content of the phase prompt file
2. Paste into Claude Code as the task
3. Let CC execute - it will:
   - Check if phase is already complete
   - Verify prerequisites
   - Create backup
   - Implement changes
   - Report completion status

### If You Accidentally Run a Phase Twice

Each prompt includes detection logic. If CC detects the phase is already complete, it will output:

```
═══════════════════════════════════════════════════════════════
PHASE [X] ALREADY COMPLETE
═══════════════════════════════════════════════════════════════
This phase has already been implemented. No changes made.

READY FOR: Phase [X+1] - [Name]
NEXT PROMPT: /continuum/prompts/PHASE[X+1]_[NAME].md
═══════════════════════════════════════════════════════════════
```

### Completion Reports

After each successful phase, CC will output:

```
═══════════════════════════════════════════════════════════════
✓ PHASE [X] COMPLETE: [Name]
═══════════════════════════════════════════════════════════════

CHANGES MADE:
  • [List of changes]

BACKUP CREATED:
  /continuum/website/backups/continuum_v[X]_[timestamp]_pre-phase[X].html

═══════════════════════════════════════════════════════════════
READY FOR: Phase [X+1] - [Name]
NEXT PROMPT: /continuum/prompts/PHASE[X+1]_[NAME].md
═══════════════════════════════════════════════════════════════
```

---

## File Locations

**Prompts (this folder):**
```
The Continuum Report/prompts/
├── README.md (this file)
├── PHASE1_MACRO_UPDATE.md
├── PHASE2_ENTITIES_LAYER.md
├── PHASE3_WEB_LAYER.md
├── PHASE4_CONNECTIONS_PANEL.md
└── PHASE5_CONNECTION_BRIEFS.md
```

**After moving to Tower:**
```
/continuum/prompts/
├── README.md
├── PHASE1_MACRO_UPDATE.md
├── PHASE2_ENTITIES_LAYER.md
├── PHASE3_WEB_LAYER.md
├── PHASE4_CONNECTIONS_PANEL.md
└── PHASE5_CONNECTION_BRIEFS.md
```

**Backups created during implementation:**
```
/continuum/website/backups/
├── continuum_v1_[timestamp]_pre-phase1.html
├── continuum_v2_[timestamp]_pre-phase2.html
├── continuum_v3_[timestamp]_pre-phase3.html
├── continuum_v4_[timestamp]_pre-phase4.html
└── continuum_v5_[timestamp]_pre-phase5.html
```

---

## Architecture After All Phases

### Layer Structure

```
┌───────────────────────────────────────────────────────────┐
│  LAYER 1: MACRO                                           │
│                                                           │
│              [PEOPLE]                                     │
│                  │                                        │
│     [GOV]───[THE CONTINUUM]───[FINANCIAL]                │
│                  │                                        │
│              [MEDIA]                                      │
│                                                           │
│  • Gold connecting lines                                  │
│  • No color legend                                        │
│  • Click box → Layer 2                                    │
└───────────────────────────────────────────────────────────┘
                           ↓
┌───────────────────────────────────────────────────────────┐
│  LAYER 2: ENTITIES                                        │
│                                                           │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │ Entity  │  │ Entity  │  │ Entity  │  │ Entity  │     │
│  │ Card    │  │ Card    │  │ Card    │  │ Card    │     │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘     │
│                                                           │
│  • Zoomable/pannable grid                                 │
│  • Filter search bar                                      │
│  • Click card → Layer 3                                   │
└───────────────────────────────────────────────────────────┘
                           ↓
┌───────────────────────────────────────────────────────────┐
│  LAYER 3: WEB                                             │
│                                                           │
│              [FOCAL NODE]  ← Top, larger, gold glow       │
│                   │                                       │
│         ┌─────────┼─────────┐                            │
│         ↓         ↓         ↓                            │
│      [Node]    [Node]    [Node]  ← Color by type         │
│         ↓         ↓                                       │
│      [Node]    [Node]        ← Gradient if multi-tag     │
│                                                           │
│  Side Panel:                                              │
│  ┌─────────────────────────┐                             │
│  │ Brief: [View Full Brief]│                             │
│  │ Connections (N):        │                             │
│  │  ▶ Entity A             │                             │
│  │  ▼ Entity B             │ ← Click to expand           │
│  │    └─ Summary text      │                             │
│  │       Sources: • • •    │                             │
│  │  ▶ Entity C             │                             │
│  │ [View Connections Brief]│                             │
│  └─────────────────────────┘                             │
└───────────────────────────────────────────────────────────┘
```

### Entity Color Schema

| Type | Color | Hex |
|------|-------|-----|
| Person: Gov Employee | Reddish | #E57373 |
| Person: CEO/Board | Tealish | #4DD0E1 |
| Person: Other | Yellow | #FFD54F |
| Org: Banking | Green | #81C784 |
| Org: Media | Pink | #F48FB1 |
| Org: Government | Dark Blue | #5C6BC0 |
| Org: Other | Purple | #9575CD |
| Case | Orange | #FFB74D |

Multi-tag entities display gradient between applicable colors.

---

## Troubleshooting

### Phase Detection Not Working

If CC doesn't detect a completed phase:
- Check that the specific indicators mentioned in the prompt exist
- Some indicators may have different class names - adjust selectors
- Run the phase anyway - it includes checks to prevent duplicate work

### Backups Not Being Created

```bash
# Manually create backup directory
mkdir -p /continuum/website/backups
chmod 755 /continuum/website/backups
chown nobody:users /continuum/website/backups
```

### Reverting a Phase

```bash
# Find the backup
ls -la /continuum/website/backups/

# Restore specific version
cp /continuum/website/backups/continuum_v[X]_[timestamp].html /continuum/website/continuum.html
```

---

## Created

**Date:** December 2024  
**Context:** Comprehensive Continuum.html visualization overhaul  
**Source Chat:** Claude.ai project conversation

---

## Next Steps After All Phases Complete

1. **Test Navigation Flow:** Macro → Entities → Web
2. **Verify Entity Colors:** Check multi-tag gradient display
3. **Test Connection Dropdowns:** Expand and check summary/sources
4. **Load Connection Briefs:** Click "View Connections Brief" button
5. **Mobile Testing:** Verify touch interactions work
6. **Performance Check:** Large entity counts should remain smooth
