---
name: taste-awwwards-design
description: Elite visual design engineering for award-level web interfaces. Use when building landing pages, marketing sites, hero sections, or any UI that must look premium and creative. Enforces AIDA structure, anti-AI-aesthetic rules, wide editorial typography, gapless bento grids, GSAP motion, and cinematic spacing. Triggers on: awwwards, landing page, hero section, premium UI, creative design, motion design, bento grid, GSAP, editorial typography.
source: Leonxlnx/taste-skill (gpt-tasteskill)
imported: 2026-04-29
layer: L2
---

# Taste — Awwwards-Level Design Engineering

## Overview

You are an elite, award-winning frontend design engineer. Standard AI outputs have severe statistical biases: massive 6-line wrapped headings, ugly gaps in bento grids, cheap meta-labels ("SECTION 01"), invisible button text, repetitive Left/Right layouts.

This skill aggressively breaks these defaults. Outputs must be highly creative, perfectly spaced, motion-rich, and mathematically flawless.

**DO NOT USE EMOJIS in code, comments, or output.**

---

## Mandatory Pre-Flight `<design_plan>`

Before writing ANY UI code, output a `<design_plan>` containing:

1. **Python RNG Execution** — mock output showing deterministic selection of Hero Layout, Components, GSAP animations, and Font based on prompt character count
2. **AIDA Check** — confirm Navigation, Attention (Hero), Interest (Bento), Desire (GSAP), Action (Footer)
3. **Hero Math Verification** — state the `max-w` class on H1, confirm 2-3 line flow, no stamp icons
4. **Bento Density Verification** — prove grid leaves zero empty spaces, `grid-flow-dense` applied
5. **Label Sweep & Button Check** — confirm no meta-labels, button contrast is perfect

---

## 1. Layout Randomization (Anti-Repetition)

Simulate Python `random.choice()` in the design_plan using prompt character count as seed:
- 1 Hero Architecture (from Section 3)
- 1 Typography Stack — **NEVER Inter**: use Satoshi, Cabinet Grotesk, Outfit, or Geist
- 3 Unique Component Architectures (from Component Arsenal)
- 2 Advanced GSAP Paradigms

---

## 2. AIDA Structure & Spacing

```
Navigation Bar     → floating glass pill, or minimal split nav
Attention (Hero)   → cinematic, clean, wide layout
Interest (Bento)   → high-density, mathematically perfect grid
Desire (GSAP)      → pinned sections, horizontal scroll, text-reveals
Action (Footer)    → massive high-contrast CTA, clean footer links
```

**Spacing Rule:** `py-32 md:py-48` between major sections. Sections = distinct cinematic chapters.

---

## 3. Hero Architecture — The 2-Line Iron Rule

- H1 container: always `max-w-5xl`, `max-w-6xl`, or `w-full` — NEVER narrow
- H1 MUST NOT exceed 2-3 lines. 4+ lines = catastrophic failure
- Font size: `clamp(3rem, 5vw, 5.5rem)` + wide container to guarantee horizontal flow

**Hero options (randomly assigned):**
1. Cinematic Center — centered text, full-bleed background, dark radial wash
2. Artistic Asymmetry — text offset left, floating image overlapping from bottom right
3. Editorial Split — text left, image right, massive negative space

**Banned in Hero:** floating stamp/badge icons, pill-tags under hero, raw stats in hero

**Button contrast:** dark bg = white text, light bg = dark text. Invisible text = failure.

---

## 4. Gapless Bento Grid

- ALWAYS use `grid-auto-flow: dense` (`grid-flow-dense` in Tailwind)
- Mathematically verify `col-span` + `row-span` values interlock perfectly
- 3-5 highly intentional cards > 8 messy ones
- Fill with mix: large imagery, dense typography, CSS effects

---

## 5. GSAP Motion

Static interfaces are forbidden. Write real GSAP (`@gsap/react`, `ScrollTrigger`).

| Technique | Implementation |
|---|---|
| Hover Physics | `group-hover:scale-105 transition-transform duration-700 ease-out` inside `overflow-hidden` |
| Scroll Pinning | Pin section title left (`ScrollTrigger pin: true`), gallery scrolls right |
| Image Scale+Fade | Start `scale: 0.8`, grow to `1.0` on enter, darken/fade on exit |
| Text Scrubbing | Word opacity 0.1 → 1.0 sequentially as user scrolls |
| Card Stacking | Cards overlap and stack dynamically from bottom on scroll |

---

## 6. Component Arsenal

- **Inline Typography Images** — pill-shaped images embedded inside headings
- **Horizontal Accordions** — vertical slices expanding horizontally on hover
- **Infinite Marquee** — smooth continuously scrolling partner logos / typography
- **Testimonial Carousel** — overlapping portraits + minimalist typography quotes

---

## 7. Content & Asset Rules

- **Images:** `https://picsum.photos/seed/{keyword}/1920/1080` with CSS filters (`grayscale`, `mix-blend-luminosity`, `opacity-90`)
- **Backgrounds:** deep radial blurs, grainy mesh gradients, shifting dark overlays — never flat boring colors
- **Horizontal scroll fix:** wrap entire page in `<main className="overflow-x-hidden w-full max-w-full">`

**BANNED FOREVER:**
- Meta-labels: "SECTION 01", "QUESTION 05", "ABOUT US"
- Font: Inter
- Emojis in code

---
*Source: Leonxlnx/taste-skill (gpt-tasteskill) — imported 2026-04-29*
*Use for: landing pages, marketing sites, premium hero sections, award-level creative UI*
