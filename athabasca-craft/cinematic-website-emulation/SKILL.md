---
name: cinematic-website-emulation
description: Use to build Pear-style cinematic scrollytelling sites.
version: 1.0.0
triggers:
  - User wants to build a Pear-style cinematic landing page
  - User wants a scroll-driven storytelling site with AI-generated art
  - User wants to recreate the pear.no visual experience
metadata:
  hermes:
    tags: [cinematic, website, scrollytelling, pear, gsap, scrolltrigger, webgl, cinematic-light]
    related_skills: [athabasca-premium-web-design, chatgpt-native-media, seedance-2-5-prompting, claude-design, cloudflare-workers-deploy]
---

# Cinematic Website Emulation

## Overview

Execute a Pear-style cinematic single-viewport scrollytelling website from
scratch. The workflow is: art direction → GPT Image stills → Seedance films →
React 19 + GSAP build → Cloudflare deploy.

## Phase 0: Art Direction

### Choose a painter/era
Pick a fine-art style that has:
- A strong, recognizable visual language
- Flat, saturated, edge-to-edge sky (for text placement)
- Dramatic scale or sublime mood
- Iconic composition (figure, landscape, or object)

Good choices: Romanticism (Friedrich, Turner), Ukiyo-e (Hokusai, Hiroshige),
Baroque (Caravaggio, Rembrandt), Art Nouveau (Mucha), Golden Age Illustration
(Wyeth), Surrealism (Magritte, Dali).

### Define the prompt skeleton
```
A wide cinematic scene painted as a single [STYLE]: [PAINTER] rendering,
[QUALITIES]. A flat saturated [COLOR] sky fills the entire canvas edge to
edge, no gradient, no vignette. [SUBJECT]. Generous empty sky across the
upper portion for text. No text anywhere.
```

### Pick the palette
- One sky color (flat, saturated)
- One accent color
- One neutral (background/text)
- One paper texture color

### Define the signature motif
The Pear site uses halftone dither rings. What's your equivalent? Crepuscular
rays, wave ripples, particle swarms, geometric expansion, ink splatter?

### Choose the typography
- Editorial serif display (self-hosted, no CDN)
- Clean serif body
- Technical monospace

## Phase 1: Generate Assets

### Step 1: Hero + chapter stills
Use ChatGPT's native image mode with the prompt skeleton. Generate:
1. Hero image (the "OG" — the iconic frame)
2. 3–5 chapter images (each section gets its own painting)
3. 1–2 transition images

### Step 2: Films from stills
Use Seedance 2.5 (Dreamina) to turn 1–2 stills into slow films (10–15s).
- Seedance 2.5 does image-to-video with reference conditioning
- Export as MP4 and/or WebP image sequences
- Generate at 1440px + 768px

### Step 3: OG image
Create a 1200×630 OG image that is itself an art asset in the same style.

## Phase 2: Build the Site

### Tier A (recommended start — 2–3 weeks)
- React 19 + Vite + TypeScript
- GSAP ScrollTrigger for scroll-driven animations
- Video backgrounds per chapter section
- CSS/SVG ink effects (no WebGL shaders)
- Desktop-first, responsive breakpoints
- Single-viewport canvas with scroll scrubbing

### Tier B (Pear-level — 4–6 weeks)
- React 19 + custom WebGL canvas compositor
- Custom scroll timeline (5350-unit model)
- Full shader treatment: paper texture, ink bleed, dithering, burn
- Image sequence scrubbing
- SVG filter compositing (fractal noise displacement)

### Key components to build
1. **Scroll controller** — intercept wheel/touch, map to 0–1 timeline, lerp
2. **Section manager** — each section gets a timeline range, renders when active
3. **Video controller** — load video, scrub to frame based on scroll position
4. **Image sequence preloader** — progressive WebP loading with warm-up
5. **Overlay** — navigation, headline, CTA, chapter rail, tagline
6. **Footer** — brand mark, tagline, contact
7. **Menu** — full-screen overlay with chapter links

## Phase 3: Deploy

1. Self-host fonts (no third-party CDN)
2. Optimize assets (WebP sequences, responsive, lazy)
3. Cloudflare Pages or Vercel
4. Custom domain + OG meta tags
5. Verify: mobile, reduced-motion, loading states

## Phase 4: The Making Of

The Pear differentiator is that the scroll shows the source art. Include:
- Original generated stills in the scroll timeline
- Optionally display the prompt skeleton on screen
- Make the process visible — the "how" is the story

## Scoring Rubric (100 points)

| Dimension | Target | Notes |
|-----------|--------|-------|
| Typography Authority | 9/10 | Editorial serif + body serif + mono, self-hosted |
| Color Restraint | 9/10 | One sky, one accent, one neutral — no waste |
| Spatial Confidence | 9/10 | Generous sky reserved for text, asymmetrical layouts |
| Animation Weight | 8/10 | GSAP custom easing, scroll-choreographed reveals |
| Micro-Interaction Detail | 8/10 | Magnetic buttons, stateful hover, scroll progress |
| Scroll Experience | 9/10 | Scrub-driven, not block-based; reward the scroll |
| 3D/Technical Visuals | 7/10 | Signature motif (waves/rays/ripples) plus canvas effects |
| CTA Clarity | 8/10 | Commanding presence, inevitable placement |
| Responsive Craft | 7/10 | Desktop-first, functional mobile |
| Brand Coherence | 10/10 | Every frame reads as the same painter's oeuvre |

## Related Skills

`athabasca-premium-web-design` (rubric, animation patterns, Preset B),
`chatgpt-native-media` (still generation), `seedance-2-5-prompting` (films),
`claude-design` / `claude-code` (build), `cloudflare-domain-deploy` (domain),
`cloudflare-workers-deploy` (static deploy), `social-posting` (launch).