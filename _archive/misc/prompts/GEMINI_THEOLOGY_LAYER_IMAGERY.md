# Gemini Prompts — Theology Layer Imagery

**Project:** The Continuum Report
**Purpose:** Generate imagery for Theology Layer (Level 0) in continuum.html
**Date:** 2025-12-24

---

## Design Direction

- **Style:** Chiaroscuro (Caravaggio, Rembrandt)
- **Palette:** Deep black (#0a0a0b), warm gold (#c9a227), pure white, crimson accents
- **Mood:** Reverent, weighty, cathedral gravitas
- **Avoid:** Cheesy religious imagery, obvious symbols, conspiracy aesthetics

---

## Prompt 1: Main Background — Light Emerging from Darkness

```
Generate an image of: A dramatic chiaroscuro scene where golden light
emerges from pure darkness. The light source is a radial glow at
center, Caravaggio-style tenebrism technique. Color palette is deep
black (#0a0a0b) transitioning to warm gold (#c9a227) at the center.
No figures, abstract and atmospheric. Cathedral-like reverence.
16:9 aspect ratio, dark moody, cinematic lighting.
```

**Use for:** `.theology-light-source` background

---

## Prompt 2: Sacred Geometry Element

```
Generate an image of: Minimal sacred geometry pattern - a subtle
golden Vesica Piscis or seed of life symbol emerging from darkness.
Thin elegant gold lines on pure black background. Mathematical
precision, cathedral rose window inspiration. No text, abstract,
suitable as subtle background overlay. Square aspect ratio.
```

**Use for:** Overlay element or decorative accent

---

## Prompt 3: Light Rays / Divine Light

```
Generate an image of: Volumetric light rays piercing through darkness,
inspired by Gustave Doré biblical illustrations. Golden crepuscular
rays descending from above into void. High contrast, dramatic
chiaroscuro. No figures or religious symbols, pure abstract light
phenomenon. Vertical composition, cinematic quality.
```

**Use for:** Hero image or animated reveal element

---

## Prompt 4: Abstract Truth vs Deception

```
Generate an image of: Abstract duality concept - one half pure radiant
gold light, other half deep shadow, meeting at a sharp vertical divide.
Represents light versus darkness, truth versus deception. Painterly
texture, Renaissance oil painting quality. No figures, symbolic and
atmospheric. Wide cinematic aspect ratio.
```

**Use for:** Thematic imagery supporting "Light and Darkness. Truth and Deception."

---

## Prompt 5: Cathedral Atmosphere

```
Generate an image of: Abstract impression of cathedral interior at
night, only visible through golden candlelight glow. Hints of gothic
arches dissolving into darkness. Rembrandt lighting technique, warm
gold against cool black. Atmospheric, reverent mood. No religious
iconography, pure architectural abstraction.
```

**Use for:** Background texture or atmospheric layer

---

## Prompt 6: Unveiled Eye / Revelation

```
Generate an image of: A single human eye emerging from shadow,
illuminated by warm golden light from one side. Extreme close-up,
photorealistic. The eye reflects light, suggesting revelation and
seeing truth. Caravaggio lighting, dramatic chiaroscuro. Dark
background fading to black. No other facial features visible.
Cinematic, contemplative mood.
```

**Use for:** Optional hero element representing "nothing hidden shall not be disclosed"

---

## Prompt 7: Ancient Manuscript / Documentary Weight

```
Generate an image of: Aged parchment or vellum partially illuminated
by candlelight, emerging from darkness. Subtle gold leaf accents
catching the light. No readable text, abstract impression of ancient
documents. Renaissance still-life quality, Rembrandt lighting.
Represents documented evidence, archival gravitas. Horizontal
composition.
```

**Use for:** Visual reference to documentary/evidence nature of the project

---

## Iteration Prompts

Use these follow-up prompts to refine generated images:

```
Make the darkness deeper and the gold more saturated
```

```
Increase the contrast between light and shadow
```

```
Make it more abstract, less literal
```

```
Add subtle texture like aged canvas or stone
```

```
Shift the gold tone warmer, more amber
```

```
Remove any elements that look cheesy or cliché
```

---

## Technical Specifications

| Spec | Value |
|------|-------|
| **Primary format** | PNG (transparency) or WebP |
| **Resolution** | 1920x1080 minimum for backgrounds |
| **File size target** | < 500KB per image (optimize) |
| **Color profile** | sRGB |
| **Save location** | `\\192.168.1.139\continuum\website\assets\images\theology\` |

---

## Recommended Naming Convention

```
theology-bg-main.webp          # Main background
theology-geometry-overlay.png   # Sacred geometry (with transparency)
theology-light-rays.webp        # Light rays element
theology-duality.webp           # Truth vs deception
theology-cathedral.webp         # Cathedral atmosphere
theology-eye.webp               # Unveiled eye (if used)
theology-manuscript.webp        # Document imagery (if used)
```

---

## CSS Integration Reference

Once images are generated, integrate with:

```css
.theology-darkness {
    background: url('../assets/images/theology/theology-bg-main.webp') center/cover;
}

.theology-light-source::before {
    content: '';
    background: url('../assets/images/theology/theology-geometry-overlay.png') center/contain no-repeat;
    mix-blend-mode: screen;
    opacity: 0.3;
}
```

---

## Quality Checklist

Before finalizing imagery:

- [ ] No cheesy or cliché religious imagery
- [ ] Color palette matches brand (#0a0a0b, #c9a227)
- [ ] Sufficient contrast for text overlay
- [ ] Works on both desktop and mobile
- [ ] File sizes optimized for web
- [ ] Consistent style across all images

---

*Prompts optimized for Gemini 2.5 Flash / Nano Banana Pro*
