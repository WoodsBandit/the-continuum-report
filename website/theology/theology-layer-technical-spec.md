# Theology Layer — Technical Architecture Specification

**Date:** 2025-12-24
**Phase:** 2 — Technical Architecture
**Status:** Complete

---

## Executive Summary

This document defines the technical implementation strategy for the theology layer—translating the visual language (Phase 1.1), theological framework (Phase 1.2), and mood board (Phase 1.3) into a working web experience.

**Goal:** Create a cathedral-quality landing page with performance, accessibility, and artistic excellence.

---

## I. Page Structure Decision

### Options Considered

**Option A: New `index.html` — Theology layer becomes the true homepage**
- **Pros:** Forces every visitor through the theological lens, strongest positioning
- **Cons:** Requires restructuring existing site navigation

**Option B: `theology.html` — Separate page, linked from current index**
- **Pros:** Keeps existing structure, optional entry point
- **Cons:** Dilutes impact, can be skipped

**Option C: Overlay on existing page — First-time visitor experience**
- **Pros:** Progressive disclosure, respects return visitors
- **Cons:** Technical complexity, can feel like a popup (negative UX)

---

### RECOMMENDATION: Option A — New `index.html`

**Rationale:**
1. **Theological framework is foundational** — It should be the first thing visitors encounter
2. **Sets expectations** — Makes the Christian worldview explicit upfront
3. **Creates journey** — Clear progression: Theology → Macro → Events → Ground
4. **Memorable experience** — A threshold worth crossing
5. **Honest positioning** — No bait-and-switch; visitors know what they're entering

**Implementation:**
- Create new `index.html` as theology layer
- Existing zoom/macro content becomes `continuum.html` or `report.html`
- "Enter The Continuum" button links to main documentation
- Navigation includes "Return to Beginning" option from deeper pages

---

## II. File Structure

### Proposed Directory Layout

```
\\192.168.1.139\continuum\website\
│
├── index.html                    ← NEW: Theology layer (landing page)
├── continuum.html                ← RENAMED: Current zoom.html content
├── report.html                   ← ALTERNATIVE NAME for continuum.html
│
├── css/
│   ├── theology.css              ← NEW: Theology layer styles
│   ├── continuum.css             ← Existing styles (renamed if needed)
│   └── shared.css                ← Shared variables, fonts, utilities
│
├── js/
│   ├── theology.js               ← NEW: Theology layer interactions
│   └── continuum.js              ← Existing JS (if any)
│
├── assets/
│   ├── fonts/
│   │   └── Cinzel/               ← Already in use
│   │
│   ├── images/
│   │   └── theology/
│   │       ├── texture-overlay.png    ← Optional: Doré-style texture
│   │       └── sacred-geometry.svg    ← Optional: Geometric patterns
│   │
│   └── audio/                    ← Optional: Cathedral ambient sound
│       └── ambience.mp3
│
└── theology/                     ← Documentation folder (existing)
    ├── theology-layer-plan.md
    ├── theology-layer-mood-board.md
    ├── theology-layer-theological-framework.md
    └── theology-layer-technical-spec.md  ← This file
```

---

## III. HTML Structure

### Complete `index.html` Architecture

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="The Continuum Report — Documenting hidden corruption through a Christian worldview. Nothing hidden that will not be disclosed.">
    <meta name="keywords" content="investigative journalism, Christian worldview, spiritual warfare, documentation, truth">

    <title>The Continuum Report | Nothing Hidden Will Remain Hidden</title>

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap" rel="stylesheet">

    <!-- Styles -->
    <link rel="stylesheet" href="css/theology.css">

    <!-- Preload critical assets -->
    <link rel="preload" href="assets/images/theology/texture-overlay.png" as="image">
</head>

<body class="theology-layer">

    <!-- DARKNESS FOUNDATION -->
    <div class="darkness" aria-hidden="true"></div>

    <!-- LIGHT SOURCE ANIMATION -->
    <div class="light-source" aria-hidden="true">
        <div class="radial-glow"></div>
        <div class="light-rays"></div>
    </div>

    <!-- SACRED GEOMETRY BACKGROUND (OPTIONAL) -->
    <div class="sacred-geometry" aria-hidden="true">
        <svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
            <!-- Geometric patterns: circles, triangles, golden ratio spirals -->
            <!-- Rendered at 5-10% opacity -->
        </svg>
    </div>

    <!-- MAIN CONTENT CONTAINER -->
    <main class="revelation-container">

        <!-- PRIMARY SCRIPTURE -->
        <blockquote class="scripture-primary">
            <p class="verse-text">
                "For there is nothing hidden that will not be disclosed,
                and nothing concealed that will not be known or brought out into the open."
            </p>
            <cite class="verse-reference">— Luke 8:17</cite>
        </blockquote>

        <!-- DICHOTOMY STATEMENT -->
        <div class="dichotomy">
            <p class="dichotomy-line">Light and Darkness.</p>
            <p class="dichotomy-line">Truth and Deception.</p>
            <p class="dichotomy-line-emphasis">The ancient war continues.</p>
        </div>

        <!-- INVITATION -->
        <p class="invitation">The evidence is documented.</p>

        <!-- ENTRY BUTTON -->
        <a href="continuum.html" class="enter-button">
            <span class="button-text">Enter The Continuum</span>
            <span class="button-glow" aria-hidden="true"></span>
        </a>

        <!-- OPTIONAL: EXPANDABLE MANIFESTO -->
        <details class="manifesto-toggle">
            <summary class="manifesto-trigger">Why This Exists</summary>
            <div class="manifesto-content">
                <p>The Continuum Report documents hidden corruption, exposed conspiracies, and the mechanisms of deception operating in our world. We do this from an explicitly Christian worldview.</p>

                <p>We believe objective truth exists, rooted in Christ. Deception is not random but coordinated by spiritual forces opposed to truth. Our battle is not against people, but against the spiritual powers operating through them.</p>

                <blockquote class="scripture-secondary">
                    <p>"We do not wrestle against flesh and blood, but against the rulers, against the authorities, against the cosmic powers over this present darkness, against the spiritual forces of evil in the heavenly realms."</p>
                    <cite>— Ephesians 6:12</cite>
                </blockquote>

                <p>Everything here is sourced, archived, and verifiable.</p>
            </div>
        </details>

    </main>

    <!-- SKIP OPTION (for return visitors) -->
    <a href="continuum.html" class="skip-intro" data-skip="true">
        Skip Introduction →
    </a>

    <!-- OPTIONAL: AUDIO TOGGLE -->
    <button class="audio-toggle" aria-label="Toggle ambient sound">
        <svg class="audio-icon" viewBox="0 0 24 24"><!-- Speaker icon --></svg>
    </button>
    <audio id="ambience" loop>
        <source src="assets/audio/ambience.mp3" type="audio/mpeg">
    </audio>

    <!-- JavaScript -->
    <script src="js/theology.js" defer></script>

</body>
</html>
```

---

### Key Structural Decisions

**1. Semantic HTML**
- `<main>` for primary content
- `<blockquote>` for scripture (semantically correct)
- `<details>/<summary>` for expandable manifesto (native HTML, no JS required)
- Proper ARIA labels for decorative vs. functional elements

**2. Progressive Enhancement**
- Works without JavaScript (static, beautiful page)
- JavaScript adds animation and interactions
- CSS provides all visual styling
- No framework dependencies

**3. Accessibility**
- Screen readers skip decorative layers (`aria-hidden="true"`)
- Proper heading hierarchy
- Keyboard navigation for all interactive elements
- Skip link for return visitors
- Respects `prefers-reduced-motion`

---

## IV. CSS Architecture

### Design System Variables

```css
:root {
    /* === COLORS === */
    --color-void: #000000;              /* Pure black */
    --color-depth: #0a0a0a;             /* Near-black */
    --color-stone: #1a1612;             /* Warm black */

    --color-gold-divine: #d4af37;       /* Primary gold */
    --color-gold-soft: #f4e4c1;         /* Soft illumination */
    --color-gold-aged: #c9a961;         /* Aged gold */

    --color-white-pure: #ffffff;        /* Pure white */
    --color-white-parchment: #f5f5f0;   /* Off-white */

    --color-crimson-dark: #8b0000;      /* Accent: blood */
    --color-crimson-brown: #a52a2a;     /* Accent: burgundy */

    --color-blue-cathedral: #1a237e;    /* Optional: firmament */
    --color-blue-midnight: #0d1b2a;     /* Optional: depth */

    /* === TYPOGRAPHY === */
    --font-primary: 'Cinzel', serif;
    --font-fallback: Georgia, 'Times New Roman', serif;

    --text-scripture-size: clamp(2rem, 5vw, 4.5rem);
    --text-dichotomy-size: clamp(1.25rem, 3vw, 2rem);
    --text-invitation-size: clamp(1rem, 2vw, 1.5rem);
    --text-button-size: clamp(1.125rem, 2.5vw, 1.75rem);

    /* === SPACING (Golden Ratio) === */
    --space-xs: 0.618rem;    /* φ^-1 */
    --space-sm: 1rem;
    --space-md: 1.618rem;    /* φ */
    --space-lg: 2.618rem;    /* φ + 1 */
    --space-xl: 4.236rem;    /* φ^2 */
    --space-xxl: 6.854rem;   /* φ^3 */

    /* === ANIMATION === */
    --anim-duration-fast: 0.3s;
    --anim-duration-medium: 0.8s;
    --anim-duration-slow: 2s;
    --anim-duration-reveal: 5s;

    --anim-easing: cubic-bezier(0.4, 0.0, 0.2, 1);

    /* === Z-INDEX LAYERS === */
    --z-darkness: 1;
    --z-geometry: 2;
    --z-light: 3;
    --z-content: 10;
    --z-controls: 20;
}
```

---

### Core Stylesheet Structure

**`css/theology.css`**

```css
/* === RESET & BASE === */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body {
    height: 100%;
    overflow: hidden; /* Single-screen experience */
}

body {
    font-family: var(--font-primary), var(--font-fallback);
    background-color: var(--color-void);
    color: var(--color-white-parchment);
    line-height: 1.618; /* Golden ratio */
}

/* === DARKNESS LAYER === */
.darkness {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        135deg,
        var(--color-void) 0%,
        var(--color-depth) 50%,
        var(--color-stone) 100%
    );
    z-index: var(--z-darkness);
}

/* === LIGHT SOURCE === */
.light-source {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 100%;
    height: 100%;
    z-index: var(--z-light);
    pointer-events: none;
}

.radial-glow {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 150%;
    height: 150%;
    background: radial-gradient(
        circle at center,
        rgba(212, 175, 55, 0.3) 0%,      /* Gold center */
        rgba(244, 228, 193, 0.15) 20%,   /* Soft glow */
        rgba(201, 169, 97, 0.08) 40%,    /* Aged gold */
        transparent 70%
    );
    opacity: 0;
    animation: light-emerge var(--anim-duration-reveal) var(--anim-easing) forwards;
    animation-delay: 0.5s;
}

@keyframes light-emerge {
    0% { opacity: 0; transform: translate(-50%, -50%) scale(0.5); }
    100% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
}

.light-rays {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 200%;
    height: 200%;
    background:
        conic-gradient(
            from 0deg at 50% 50%,
            transparent 0deg,
            rgba(212, 175, 55, 0.1) 30deg,
            transparent 60deg,
            rgba(212, 175, 55, 0.1) 90deg,
            transparent 120deg,
            rgba(212, 175, 55, 0.1) 150deg,
            transparent 180deg,
            rgba(212, 175, 55, 0.1) 210deg,
            transparent 240deg,
            rgba(212, 175, 55, 0.1) 270deg,
            transparent 300deg,
            rgba(212, 175, 55, 0.1) 330deg,
            transparent 360deg
        );
    opacity: 0;
    animation: rays-extend 3s var(--anim-easing) forwards;
    animation-delay: 2s;
}

@keyframes rays-extend {
    0% { opacity: 0; transform: translate(-50%, -50%) rotate(0deg); }
    100% { opacity: 1; transform: translate(-50%, -50%) rotate(360deg); }
}

/* === SACRED GEOMETRY === */
.sacred-geometry {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 80vmin;
    height: 80vmin;
    opacity: 0.08;
    z-index: var(--z-geometry);
    pointer-events: none;
    animation: geometry-fade-in 2s ease-in forwards;
    animation-delay: 1.5s;
}

.sacred-geometry svg {
    width: 100%;
    height: 100%;
}

.sacred-geometry circle,
.sacred-geometry path {
    stroke: var(--color-gold-soft);
    stroke-width: 1;
    fill: none;
}

/* === MAIN CONTENT === */
.revelation-container {
    position: relative;
    z-index: var(--z-content);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: var(--space-lg);
    text-align: center;
}

/* === SCRIPTURE PRIMARY === */
.scripture-primary {
    max-width: 900px;
    margin-bottom: var(--space-xl);
    opacity: 0;
    animation: text-reveal 1.5s var(--anim-easing) forwards;
    animation-delay: 2.5s;
}

.verse-text {
    font-size: var(--text-scripture-size);
    font-weight: 400;
    line-height: 1.4;
    color: var(--color-gold-soft);
    text-shadow:
        0 0 20px rgba(212, 175, 55, 0.6),
        0 0 40px rgba(212, 175, 55, 0.3);
    margin-bottom: var(--space-md);
}

.verse-reference {
    display: block;
    font-size: var(--text-invitation-size);
    font-weight: 400;
    font-style: normal;
    color: var(--color-gold-aged);
    opacity: 0.8;
}

@keyframes text-reveal {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}

/* === DICHOTOMY === */
.dichotomy {
    margin-bottom: var(--space-lg);
    opacity: 0;
    animation: text-reveal 1.5s var(--anim-easing) forwards;
    animation-delay: 3.5s;
}

.dichotomy-line {
    font-size: var(--text-dichotomy-size);
    font-weight: 400;
    color: var(--color-gold-divine);
    margin-bottom: var(--space-xs);
    letter-spacing: 0.05em;
}

.dichotomy-line-emphasis {
    font-size: var(--text-dichotomy-size);
    font-weight: 700;
    color: var(--color-white-pure);
    margin-top: var(--space-sm);
    letter-spacing: 0.08em;
}

/* === INVITATION === */
.invitation {
    font-size: var(--text-invitation-size);
    font-weight: 400;
    color: var(--color-white-parchment);
    margin-bottom: var(--space-xl);
    opacity: 0;
    animation: text-reveal 1.5s var(--anim-easing) forwards;
    animation-delay: 4.5s;
}

/* === ENTER BUTTON === */
.enter-button {
    position: relative;
    display: inline-block;
    padding: var(--space-md) var(--space-xl);
    font-size: var(--text-button-size);
    font-weight: 700;
    font-family: var(--font-primary);
    color: var(--color-white-pure);
    text-decoration: none;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    border: 2px solid var(--color-gold-divine);
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(10px);
    cursor: pointer;
    overflow: hidden;
    transition: all var(--anim-duration-fast) var(--anim-easing);
    opacity: 0;
    animation: text-reveal 1.5s var(--anim-easing) forwards,
               button-pulse 2s ease-in-out infinite;
    animation-delay: 5.5s, 7s;
}

.enter-button:hover {
    border-color: var(--color-white-pure);
    box-shadow:
        0 0 30px rgba(212, 175, 55, 0.6),
        inset 0 0 20px rgba(212, 175, 55, 0.2);
    transform: scale(1.05);
}

.enter-button:active {
    transform: scale(0.98);
}

.button-glow {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 100%;
    height: 100%;
    background: radial-gradient(
        circle,
        rgba(212, 175, 55, 0.3) 0%,
        transparent 70%
    );
    opacity: 0;
    pointer-events: none;
    transition: opacity var(--anim-duration-fast);
}

.enter-button:hover .button-glow {
    opacity: 1;
}

@keyframes button-pulse {
    0%, 100% { box-shadow: 0 0 10px rgba(212, 175, 55, 0.3); }
    50% { box-shadow: 0 0 25px rgba(212, 175, 55, 0.6); }
}

/* === MANIFESTO (OPTIONAL) === */
.manifesto-toggle {
    position: absolute;
    bottom: var(--space-lg);
    left: 50%;
    transform: translateX(-50%);
    max-width: 600px;
    opacity: 0;
    animation: fade-in 1s ease-in forwards;
    animation-delay: 6s;
}

.manifesto-trigger {
    font-size: 0.875rem;
    color: var(--color-gold-aged);
    cursor: pointer;
    list-style: none;
    opacity: 0.7;
    transition: opacity var(--anim-duration-fast);
}

.manifesto-trigger:hover {
    opacity: 1;
}

.manifesto-content {
    margin-top: var(--space-md);
    padding: var(--space-md);
    font-size: 0.95rem;
    line-height: 1.8;
    color: var(--color-white-parchment);
    background: rgba(0, 0, 0, 0.7);
    border: 1px solid var(--color-gold-aged);
    border-radius: 4px;
    text-align: left;
}

.manifesto-content p {
    margin-bottom: var(--space-sm);
}

.scripture-secondary {
    margin: var(--space-md) 0;
    padding-left: var(--space-md);
    border-left: 3px solid var(--color-gold-aged);
    font-style: italic;
    opacity: 0.9;
}

/* === SKIP INTRO === */
.skip-intro {
    position: fixed;
    top: var(--space-sm);
    right: var(--space-sm);
    z-index: var(--z-controls);
    font-size: 0.875rem;
    color: var(--color-gold-aged);
    text-decoration: none;
    opacity: 0.5;
    transition: opacity var(--anim-duration-fast);
}

.skip-intro:hover {
    opacity: 1;
}

/* === AUDIO TOGGLE (OPTIONAL) === */
.audio-toggle {
    position: fixed;
    bottom: var(--space-sm);
    right: var(--space-sm);
    z-index: var(--z-controls);
    width: 40px;
    height: 40px;
    background: rgba(0, 0, 0, 0.5);
    border: 1px solid var(--color-gold-aged);
    border-radius: 50%;
    cursor: pointer;
    opacity: 0.6;
    transition: opacity var(--anim-duration-fast);
}

.audio-toggle:hover {
    opacity: 1;
}

.audio-icon {
    width: 24px;
    height: 24px;
    fill: var(--color-gold-divine);
}

/* === RESPONSIVE === */
@media (max-width: 768px) {
    .revelation-container {
        padding: var(--space-md);
    }

    .verse-text {
        font-size: clamp(1.5rem, 6vw, 2.5rem);
    }

    .enter-button {
        padding: var(--space-sm) var(--space-lg);
    }

    .manifesto-toggle {
        bottom: var(--space-md);
        max-width: 90%;
    }
}

/* === ACCESSIBILITY === */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

@media (prefers-contrast: high) {
    .verse-text {
        text-shadow: none;
    }

    .enter-button {
        border-width: 3px;
    }
}

/* === PRINT STYLES === */
@media print {
    .darkness,
    .light-source,
    .sacred-geometry,
    .skip-intro,
    .audio-toggle {
        display: none;
    }

    .revelation-container {
        color: #000;
        background: #fff;
    }
}
```

---

## V. JavaScript Architecture

### `js/theology.js`

```javascript
// ============================================
// THEOLOGY LAYER — INTERACTIVE BEHAVIORS
// ============================================

(function() {
    'use strict';

    // === CONFIG ===
    const CONFIG = {
        hasSeenIntro: 'continuumTheologyIntroSeen',
        audioEnabled: 'continuumAudioEnabled',
        animationDelay: 7000, // Total animation sequence length (ms)
    };

    // === DOM ELEMENTS ===
    const elements = {
        body: document.body,
        skipIntro: document.querySelector('.skip-intro'),
        audioToggle: document.querySelector('.audio-toggle'),
        audioElement: document.getElementById('ambience'),
        enterButton: document.querySelector('.enter-button'),
    };

    // === INITIALIZATION ===
    function init() {
        checkReturnVisitor();
        setupSkipIntro();
        setupAudioToggle();
        setupButtonTransition();
        setupParallax();
    }

    // === RETURN VISITOR HANDLING ===
    function checkReturnVisitor() {
        const hasSeenIntro = localStorage.getItem(CONFIG.hasSeenIntro);

        if (hasSeenIntro === 'true') {
            // Show skip intro link prominently
            if (elements.skipIntro) {
                elements.skipIntro.style.opacity = '1';
                elements.skipIntro.style.fontSize = '1rem';
            }
        }
    }

    function setupSkipIntro() {
        if (!elements.skipIntro) return;

        elements.skipIntro.addEventListener('click', function(e) {
            // Mark as seen when skipping
            localStorage.setItem(CONFIG.hasSeenIntro, 'true');
        });
    }

    // === AUDIO TOGGLE ===
    function setupAudioToggle() {
        if (!elements.audioToggle || !elements.audioElement) return;

        const audioEnabled = localStorage.getItem(CONFIG.audioEnabled);

        elements.audioToggle.addEventListener('click', function() {
            if (elements.audioElement.paused) {
                elements.audioElement.play();
                elements.audioToggle.classList.add('active');
                localStorage.setItem(CONFIG.audioEnabled, 'true');
            } else {
                elements.audioElement.pause();
                elements.audioToggle.classList.remove('active');
                localStorage.setItem(CONFIG.audioEnabled, 'false');
            }
        });

        // Auto-play if previously enabled (with user gesture required)
        if (audioEnabled === 'true') {
            // Note: Modern browsers require user interaction for autoplay
            // This will only work if user has interacted before
            elements.audioElement.play().catch(() => {
                // Silently fail if autoplay blocked
                console.log('Autoplay prevented by browser');
            });
        }
    }

    // === BUTTON TRANSITION ===
    function setupButtonTransition() {
        if (!elements.enterButton) return;

        elements.enterButton.addEventListener('click', function(e) {
            // Mark intro as seen
            localStorage.setItem(CONFIG.hasSeenIntro, 'true');

            // Optional: Add transition animation before navigation
            // Uncomment if you want light-expand effect
            /*
            e.preventDefault();
            elements.body.classList.add('transitioning');

            setTimeout(function() {
                window.location.href = elements.enterButton.href;
            }, 1000);
            */
        });
    }

    // === PARALLAX EFFECT (OPTIONAL) ===
    function setupParallax() {
        const lightSource = document.querySelector('.light-source');
        if (!lightSource) return;

        // Check if user prefers reduced motion
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (prefersReducedMotion) return;

        let mouseX = 0;
        let mouseY = 0;
        let currentX = 0;
        let currentY = 0;

        document.addEventListener('mousemove', function(e) {
            mouseX = (e.clientX / window.innerWidth - 0.5) * 30; // Max 15px shift
            mouseY = (e.clientY / window.innerHeight - 0.5) * 30;
        });

        // Smooth animation using requestAnimationFrame
        function animateParallax() {
            currentX += (mouseX - currentX) * 0.1; // Smooth easing
            currentY += (mouseY - currentY) * 0.1;

            lightSource.style.transform = `translate(calc(-50% + ${currentX}px), calc(-50% + ${currentY}px))`;

            requestAnimationFrame(animateParallax);
        }

        animateParallax();
    }

    // === RUN ON DOM READY ===
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
```

---

## VI. Animation Timeline

### Complete Sequence (7 seconds total)

```
0.0s — Page loads, pure black
0.5s — Darkness gradient subtle variation begins
0.5s — Light glow starts to emerge (radial gradient fades in)
1.5s — Sacred geometry fades in (subtle background)
2.0s — Light rays begin to extend (rotating conic gradient)
2.5s — Scripture text fades in with glow
3.5s — Dichotomy text appears
4.5s — Invitation text emerges
5.5s — Button materializes
7.0s — Button begins pulsing (idle state)
```

### Timing Philosophy

- **First 2 seconds:** Pure atmosphere. No text. Build anticipation.
- **2.5-5.5s:** Text reveals in hierarchy (scripture → dichotomy → invitation → button)
- **After 7s:** User is in control. Can enter or explore.

### Performance Considerations

- All animations use CSS (GPU-accelerated)
- JavaScript only for interactions, not animations
- `will-change` property for animated elements
- Respects `prefers-reduced-motion`
- Total animation sequence: < 8s (acceptable for landing page)

---

## VII. Performance Budget

### Target Metrics (Lighthouse)

- **Performance:** > 90
- **Accessibility:** 100
- **Best Practices:** > 95
- **SEO:** > 95

### File Size Budget

| Asset Type | Budget | Notes |
|------------|--------|-------|
| HTML | < 10 KB | Minimal markup |
| CSS | < 20 KB | Single file, minified |
| JavaScript | < 10 KB | Vanilla JS, no frameworks |
| Fonts (WOFF2) | < 50 KB | Cinzel only, subset if possible |
| Images (optional) | < 100 KB | Texture overlays, optimized |
| Audio (optional) | < 500 KB | Compressed MP3, lazy-loaded |
| **TOTAL** | **< 200 KB** | (excluding audio) |

### Loading Strategy

1. **Critical CSS:** Inline above-the-fold styles (< 14 KB)
2. **Font loading:** `font-display: swap` to prevent FOIT
3. **Image lazy-loading:** `loading="lazy"` attribute
4. **Audio:** Load only when user clicks toggle
5. **No external libraries:** Zero dependencies

---

## VIII. Responsive Design

### Breakpoints

```css
/* Mobile first approach */
--breakpoint-sm: 640px;   /* Landscape phones */
--breakpoint-md: 768px;   /* Tablets */
--breakpoint-lg: 1024px;  /* Laptops */
--breakpoint-xl: 1280px;  /* Desktops */
```

### Mobile Considerations

**Typography:**
- Use `clamp()` for fluid sizing
- Minimum 16px for body text (no zoom on iOS)
- Reduce letter-spacing on small screens

**Layout:**
- Stack vertically, center-aligned
- Reduce padding on sides (more content visible)
- Button remains prominent and tappable (min 44x44px)

**Animation:**
- Shorter durations on mobile (5s instead of 7s)
- Less parallax intensity
- Option to skip animations

**Performance:**
- No high-res textures on mobile
- Simplified gradients if needed
- Test on actual devices (not just DevTools)

---

## IX. Accessibility Checklist

### Keyboard Navigation
- [ ] All interactive elements reachable via Tab
- [ ] Skip intro link accessible without mouse
- [ ] Enter button activatable with Enter/Space
- [ ] Focus indicators visible (not removed)

### Screen Readers
- [ ] Decorative elements hidden (`aria-hidden="true"`)
- [ ] Scripture text properly structured (`<blockquote>`, `<cite>`)
- [ ] Button has descriptive text (not just icon)
- [ ] Page has proper `<title>` and meta description

### Visual Accessibility
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Text resizable to 200% without breaking layout
- [ ] No information conveyed by color alone
- [ ] Focus indicators have 3:1 contrast

### Motion & Animation
- [ ] Respects `prefers-reduced-motion`
- [ ] No flashing/strobing effects (seizure risk)
- [ ] Animations pauseable (audio toggle)
- [ ] Core content accessible without animations

### ARIA & Semantics
- [ ] Proper landmark roles (`<main>`, `<nav>`)
- [ ] Heading hierarchy logical (h1 → h2 → h3)
- [ ] Links descriptive (not "click here")
- [ ] Forms properly labeled (if any added later)

---

## X. Browser Support

### Target Browsers

| Browser | Version | Support Level |
|---------|---------|---------------|
| Chrome | Last 2 versions | Full |
| Firefox | Last 2 versions | Full |
| Safari | Last 2 versions | Full |
| Edge | Last 2 versions | Full |
| Mobile Safari | iOS 14+ | Full |
| Chrome Mobile | Last 2 versions | Full |
| IE 11 | N/A | Not supported |

### Progressive Enhancement

**Core Experience (works everywhere):**
- Static page with scripture and button
- Basic styling with system fonts
- Navigation functional

**Enhanced Experience (modern browsers):**
- CSS animations (radial gradients, keyframes)
- Custom fonts (Cinzel)
- Audio toggle
- Parallax effects

**Fallbacks:**
- `@supports` queries for modern CSS
- System font stack if Cinzel fails
- No JavaScript still navigable

---

## XI. Testing Strategy

### Pre-Launch Testing

**Manual Testing:**
- [ ] Test on real devices (iPhone, Android, tablet)
- [ ] Test with screen reader (NVDA, VoiceOver)
- [ ] Test keyboard-only navigation
- [ ] Test in private/incognito mode (localStorage)
- [ ] Test with slow network (3G throttling)

**Automated Testing:**
- [ ] Lighthouse audit (all categories)
- [ ] WAVE accessibility checker
- [ ] HTML validation (W3C)
- [ ] CSS validation
- [ ] Broken link checker

**Cross-Browser Testing:**
- [ ] Chrome (Windows, Mac, Android)
- [ ] Firefox (Windows, Mac)
- [ ] Safari (Mac, iOS)
- [ ] Edge (Windows)

**Performance Testing:**
- [ ] PageSpeed Insights
- [ ] WebPageTest.org
- [ ] GTmetrix
- [ ] First Contentful Paint < 1.5s
- [ ] Time to Interactive < 3.5s

---

## XII. Deployment Checklist

### Pre-Deployment

- [ ] Minify CSS and JavaScript
- [ ] Optimize images (WebP with fallbacks)
- [ ] Set proper cache headers
- [ ] Enable Gzip/Brotli compression
- [ ] Add security headers (CSP, X-Frame-Options)
- [ ] Test on staging environment

### DNS & Hosting

- [ ] SSL certificate active (HTTPS)
- [ ] CDN configured (if applicable)
- [ ] DNS propagation verified
- [ ] 301 redirects from old index (if applicable)

### Monitoring

- [ ] Analytics installed (privacy-respecting)
- [ ] Error tracking configured
- [ ] Uptime monitoring active
- [ ] Performance monitoring baseline

---

## XIII. Future Enhancements (Post-Launch)

### Phase 2 Additions (Optional)

1. **Interactive Light Source**
   - Mouse follows light (currently planned)
   - Click to create ripple effect
   - Touch gestures on mobile

2. **Extended Manifesto**
   - Full "About" page linked from manifesto
   - Theological resources section
   - FAQ on spiritual warfare interpretation

3. **Multi-Language Support**
   - Scripture in multiple languages
   - Toggle for translation
   - Proper i18n structure

4. **Dark Mode Toggle**
   - Ironic, but: "lighter" dark mode option
   - Accessibility for light-sensitive users
   - Preserves overall aesthetic

5. **Share Functionality**
   - Social meta tags (Open Graph, Twitter Cards)
   - Share quote image generator
   - Referral tracking

---

## XIV. Success Metrics

### Quantitative

- **Load Time:** < 2 seconds on 3G
- **Lighthouse Score:** > 90 average
- **Bounce Rate:** < 40% (visitors proceed to continuum)
- **Time on Page:** > 10 seconds (engage with content)
- **Error Rate:** < 1% (no JS errors)

### Qualitative

- **First Impression:** Visitors report "awe" or "gravitas"
- **Message Clarity:** Users understand Christian framework
- **Ease of Use:** No confusion about how to proceed
- **Artistic Merit:** Could be showcased as design excellence
- **Theological Accuracy:** No misrepresentation of scripture

---

## XV. Handoff to Phase 3

With technical architecture complete, Phase 3 will:

1. **Finalize Copy** — Exact wording for all text elements
2. **Art Direction** — Create/source sacred geometry SVG, texture overlays
3. **Audio Selection** — Source or create cathedral ambience
4. **Content Review** — Theological accuracy check, legal opinion compliance

---

## XVI. Conclusion

This technical specification provides:

- **Complete HTML structure** — Semantic, accessible, performant
- **Comprehensive CSS architecture** — Design system, animations, responsive
- **Minimal JavaScript** — Progressive enhancement, interactions only
- **Performance budget** — Fast loading, optimized assets
- **Accessibility compliance** — WCAG AA, keyboard navigation, screen readers
- **Browser support strategy** — Modern browsers, graceful degradation
- **Testing & deployment plan** — Quality assurance, launch readiness

**Ready for Phase 3:** Content development and asset creation.

---

*"For there is nothing hidden that will not be disclosed, and nothing concealed that will not be known or brought out into the open." — Luke 8:17*
