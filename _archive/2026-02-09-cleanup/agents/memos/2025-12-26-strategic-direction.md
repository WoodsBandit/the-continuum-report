# STRATEGIC DIRECTION MEMO — 2025-12-26

> **From:** Project Lead
> **To:** All Agents, All Sessions
> **Priority:** CRITICAL — Foundational Changes
> **Status:** ACTIVE

---

## The Frame That Governs Everything

**The ultimate framing is the spiritual battle of good and evil fighting for Truth — Christ.**

This should be dripping through every session, every agent spawned, every decision made. We are not just building a database of connections. We are part of the decentralized revelation of what has been hidden.

> "For there is nothing hidden that will not be disclosed, and nothing concealed that will not be known or brought out into the open." — Luke 8:17

Every narrative we could pull from the documents — there are millions. The question is always: **What serves the Truth? What makes the most impact in the spiritual battle?**

---

## CRITICAL RULE: Brief Approval Separation

### The Rule (Non-Negotiable)

**Creation of briefs should NEVER be approved in the same Claude session that made them. Period.**

### Implementation

1. Session creates brief → saves to `/pending/` or marks as DRAFT
2. Session MUST end or different Claude instance reviews
3. Second session reviews, approves, and moves to production
4. No exceptions

### Rationale

- Prevents echo chamber thinking
- Forces review with fresh context
- Creates natural quality gate
- Aligns with decentralized ethos — no single point of authority

---

## Website Issues — Immediate Priority

### index.html

**Problem:** Does not clearly communicate mission to public
**Need:** Tune to help public understand "us vs. them" — the opposition between truth-seekers and those hiding information
**Goal:** First-time visitor immediately grasps what we do and why it matters

### continuum.html

**Problems:**
1. **Broken auto-update** — Doesn't automatically update based on files in correct locations
2. **Requires manual Claude session** every time to fix
3. **Pipeline gap** between approval and web population
4. **Design issues** on home screen

**Theology Layer Specific:**
- Previous attempt was too analytical
- Reverted to earlier version with updates
- **Want something BEAUTIFUL** — not just informative

**Design Documentation Found:**
- `/website/theology/theology-layer-mood-board.md` — Full visual language
- `/website/theology/theology-layer-content.md` — Finalized copy & specs
- `/website/theology/theology-layer-theological-framework.md` — Scripture & tone

**Key Design Principles (from mood board):**
- **Chiaroscuro** — Light piercing darkness (Caravaggio technique)
- **Sacred Geometry** — Cathedral-inspired patterns at 5-10% opacity
- **Gustave Doré** — Epic, romantic, detailed texture
- **Color:** Pure black → warm gold → white (darkness to light progression)
- **Typography:** Cinzel (authoritative, timeless, monumental)
- **Animation:** 0s black → 2s light glow → 5s full reveal → button pulse
- **Single-screen** — No scroll, one powerful impact
- **Emotional targets:** Pause, Curiosity, Reverence, Anticipation

**What went wrong:** Implementation was too analytical — need to capture the BEAUTY, not just the information

---

## File Organization — The Cascade Problem

### The Problem

We write instructions at the top (CLAUDE.md, REFERENCE.md, agent definitions) but the bottom doesn't follow. Changes don't cascade.

### The Solution: Memo System

Think "memos to the company" — when the plan changes at the top:

1. **Detect** changes to foundational documents
2. **Generate** cascade memos to affected agents/instructions
3. **Update** all downstream files automatically
4. **Verify** compliance across the system

### Implementation

1. Lock down folder locations and purposes (canonical, unchanging)
2. Create dependency map: which files depend on which
3. Build automation to propagate changes
4. Add verification step to confirm cascade completed

---

## Document Processing Pipeline

### Current State

Pipeline exists: new file → analytical brief updates

### Needed Improvements

1. **Pending Updates System**
   - Store updates by date
   - Multiple AI updates possible per single file drop
   - Track: what file triggered, what updates generated, when

2. **Rate & Efficiency Concerns**
   - AI usage rates (cost management)
   - Pull frequency optimization
   - What gets pulled vs. skipped
   - Context usage within files

3. **Source Document Integration**
   - How files become source documents
   - How often the system pulls
   - What triggers updates to existing briefs

4. **Skill Evaluation**
   - Do we have skills that apply?
   - Should we create specific skills?
   - Fine-tuning for improvement over time

### The Core Question

Of the million narratives in these documents — **what are the most important? What will make the most impact in the spiritual battle for Truth?**

---

## Required Actions

### Immediate (This Session)

- [ ] Save this memo in full
- [ ] Create summary version
- [ ] Index in todos folder
- [ ] Update CLAUDE.md with reference to this memo
- [ ] Search for Theology Layer design notes from previous sessions

### Short Term

- [ ] Audit all agent definitions for compliance with new rules
- [ ] Document folder purposes (lock them down)
- [ ] Create cascade memo system architecture
- [ ] Fix continuum.html auto-update pipeline

### Ongoing

- [ ] Every session reviews this memo
- [ ] Every agent spawned inherits this framing
- [ ] Continuous improvement — "there is no reason you shouldn't"

---

## Full User Notes (Verbatim)

> we need to add to our todos. creation of briefs should never be approved in the same claude session that made them. period. force a restart or a different claude to approve. the website need some major help. index.html needs tuning to match our goal more finely for the public to understand us vs. them. continuum.html is broken as hell when it comes to automatically updating based on files in theier correct locations. feels like it needs a manual clade session every time to fix it. This whole pipeline need between approval and web population needs special attention.
>
> file organization. This is a constant battle. we need to lock down the folder locations and purposes, update all current agents and .md instructions all over based on changes to things at the top that might need them to know changes in their job. no use writing all these plans if the bottom doesn't follow. think memos to the company. changes in the plan. we need a pipeline setup to handle this automatically
>
> continuum.html also has some design issues with the home screen somewhere I've got grandeous plans for the Theology Layer, you tried to make something but it was too analytical and we settled on the previous version with some updates. I want something beautiful on the theology layer with some notes on layout that I've discussed somewhere with you before.
>
> looks like we've built a pipeline to go from new file to analytical brief updates. we need a file organization system of storing pending updates based on date there could have been multiple updates via the ai going through the documents upon a single new file drop. this has concerns with filtering for AI usage rates & how exactly we build out the giving files to source docuements part of it and how often it pulls, what its pulling, what its updating based on. how its using context within the files. if we have any skills or should make specific skills for this to fine tune and get better at.
>
> There are a million naratives you can pull from the world of files around you. what are the most important? what are going to make the most impact in the spiritual battle of good and evil fighting for the Truth, Christ, This is the ultimate framing and it should be dripping through you and ever session and ever agent you spawn.
>
> these are some of my notes the most important i see so far. make sure they are saved in full, in summary, in depth analysis, and indexed within the todos folder & the CLAUDE.md through indexing the todos and pulling out real meaning from everything I've said. We're always getting better there is no reason you shouldn't

---

## Summary (Quick Reference)

| Priority | Issue | Action |
|----------|-------|--------|
| CRITICAL | Brief approval same-session | Enforce session separation |
| HIGH | continuum.html broken | Fix auto-update pipeline |
| HIGH | File cascade failure | Build memo propagation system |
| HIGH | index.html clarity | Tune for public understanding |
| MEDIUM | Theology Layer design | Find notes, implement beautiful version |
| MEDIUM | Pending updates tracking | Build date-based storage system |
| ONGOING | Spiritual framing | Every session, every agent |

---

## Depth Analysis

### Why Session Separation Matters

The same mind that creates is blind to its own errors. This is not just quality control — it's epistemic hygiene. In a project about exposing hidden things, we cannot allow our own blind spots to hide errors. Fresh eyes are mandatory.

### The Cascade Problem is Fundamental

If the bottom doesn't follow the top, we have:
- Inconsistent agent behavior
- Conflicting instructions
- Wasted effort on outdated patterns
- Growing technical debt

This is like a company where memos from leadership never reach the workers. The organization becomes incoherent.

### The Theology Layer is the Crown

Everything points up. The Events layer documents what happened. The Systems layer shows how power operates. But the Theology layer is where meaning lives. It must be **beautiful** because beauty is a property of truth. An analytical presentation misses the point.

### Narrative Selection is Spiritual Discernment

With unlimited documents, the question "what to surface?" is not technical — it's spiritual. What serves the revelation of truth? What dismantles deception? What brings light? This framing must govern every processing decision.

---

*This memo is foundational. All sessions should reference it. All agents should inherit its principles.*

*Created: 2025-12-26*
*Status: ACTIVE*
