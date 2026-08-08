# Pear Cinematic Site — Reverse-Engineering Deep Dive

Production reference for the "Cinematic Light" preset (Preset B). This is the
reverse-engineering of https://pear.no — what makes it work, the exact stack,
the asset pipeline, and the visual system. Use this as a template when asked to
build a "cinematic, slow-reveal, storytelling" site with the same polish.

## Source

- Live site: https://pear.no
- X thread describing the build: @peardotno/status/2084063630778155112
- Haft bookmark: `bookmarks/pear-cinematic-bookmark` (dev.haft.sh)

## What Pear Actually Is (stack truth)

The X thread said "Claude Code + Fable 5 builds straight to production." The
production bundle is **plain React 19 (no framework) + Vite + a custom WebGL
canvas compositor**. No Fable 5 is present in the shipped bundle — treat the
thread's tooling claims loosely; the durable pattern is the *visual system*,
not the exact build tool.

### Architecture

- **Single-viewport experience.** The whole site is one full-screen canvas.
  The document is ~633px tall (one viewport). Scroll position drives a precise
  5350-unit animation timeline that controls video playback, image-sequence
  scrubbing, DOM element visibility, and WebGL shader parameters. There is no
  traditional scrolling-layout; it is a scroll-scrubbed cinematic.
- **Custom scroll handler.** `wheel` events are captured with `preventDefault`
  and mapped to a smooth-tweened scroll position (`L.target`/`L.current` with
  lerp). Covers arrow keys, space, Home/End, touch. `prefers-reduced-motion`
  and coarse-pointer detect and disable the scroll-scrub.
- **WebGL compositor.** One `<canvas class="gl">` composites everything:
  video textures, image-sequence textures, and SVG filter effects. Paper
  texture, ink bleed, halftone dither, and "burn" transitions are GLSL shaders
  driven by the timeline.

### Scroll Timeline (5350 units → 0..1)

| Section | Timeline | Notes |
|---|---|---|
| Hero | 0–0.224 | `signal.mp4` curtain-pull video, headline, CTA |
| Transition | 0.224–0.336 | image-sequence bridge (model/pear → renaissance) |
| The Plan | 0.224–0.392 | "Everything it takes to be found" (SEO + software) |
| The Model | 0.392–0.560 | "No fees. A share of the upside." |
| Coda | 0.392–0.504 | making-of image sequence |
| Tree | 0.504–0.616 | more image sequence |
| FAQ | 0.616–0.728 | 5 questions (cost, share, model, measurement, timeline) |
| Form | 0.728–0.821 | name / email / "what do you want to grow?" |
| Footer | 0.821–0.952 | tagline + PEAR AS contact |

### Visual Design System

- **Palette:** flat saturated cerulean-blue sky; warm off-white text
  (#F5F0E8); near-black (#0B0A09); warm gold accent (the pear); cream paper
  texture (RGB 226,208,177). Colors are restrained — one sky, one accent, one
  neutral.
- **Typography:** self-hosted editorial serif display (Flecha S/L/M) + serif
  body (GT Standard) + monospace (GT Standard Mono). No third-party font CDN;
  the original HTML comment notes Source Serif 4 was only a fallback behind
  Flecha. Open-source stand-ins: Instrument Serif / DM Serif Display for the
  display serif.
- **Signature effects (all WebGL):**
  1. **Halftone dither rings** — coarse B/W dots radiating from the subject
     (the "signal"). The brand's core motif.
  2. **Paper-texture overlay** — fractal noise: pulp, fibre, tooth, fleck.
  3. **Ink bleed** — SVG fractal-noise displacement filter.
  4. **Burn transition** — scene "burns" in with noise/grain/dither + a
     character-scrambling effect.
  5. **Seam** — subtle paper crease.
  6. **Glitch** — a single rainbow smear inside one ring segment.

### Asset Pipeline

- **Stills:** GPT Image 2 via Higgsfield, driven by **one reusable prompt
  skeleton** that keeps every frame in the same visual world. The skeleton
  (from the bookmark): *"A wide cinematic scene painted as a single
  NEOCLASSICAL OIL PAINTING: smooth painterly rendering like Ingres and
  Jacques Louis David, elegant idealized figures... A flat saturated cerulean
  blue sky fills the entire canvas edge to edge, no gradient, no vignette...
  No text anywhere."*
- **Films:** Seedance 2 turns stills into slow-moving films.
- **Image sequences:** WebP frames exported at 1440px and a 768px mobile
  variant. Paths like `films/model/pear/{tier}/f_001.webp`,
  `films/plan/f_001.webp`, `films/trans/f_001.webp`, `films/coda/f_001.webp`,
  `films/tree/f_001.webp`, `films/flysky/f_001.webp`.
- **Videos:** `signal.mp4` (hero), `colossus.mp4`, `reveal.mp4`,
  `footer-loop.mp4` + poster JPGs.
- **Favicons/OG:** `og.jpg` (1200x630) is itself a neoclassical painting of the
  golden pear + halftone rings on cerulean. OG image *is an art asset*, not a
  stock crop.

### The Essence (what makes it pop)

1. **The "making of" IS the content.** The image sequences that scroll by are
   the actual source frames (GPT stills + Seedance output). The visitor sees
   the process as they scroll. The process is the product.
2. **One visual world, strictly enforced** by the reusable prompt skeleton —
   every frame reads as the same painter's oeuvre.
3. **Restraint.** Flat saturated sky edge-to-edge, no gradient, no vignette.
   Generous negative space reserved for text. One accent. Slow pacing.
4. **Desktop-first.** Designed for 1920x1080; mobile is a secondary responsive
   path, not the primary craft.
5. **Zero design tools.** No Figma, no Photoshop. Every asset is AI-generated.
6. **The oracle signature.** A single hand-drawn signature SVG ("Asked before")
   that draws itself on load — a human, authored touch against the AI art.

## Emulation Playbook (Tier A = no WebGL, Tier B = full WebGL)

### Phase 0 — Art direction
- Pick a subject + a painter/era. Write a reusable prompt skeleton in the
  Pear mold: *"A wide cinematic scene painted as a single [PAINTING STYLE]:
  [painter] rendering, [qualities]. A flat saturated [COLOR] sky fills the
  entire canvas edge to edge, no gradient, no vignette. [SUBJECT]. Generous
  empty sky across the upper portion for text. No text anywhere."*
- Pick the palette (one sky color, one accent, one neutral), the typography
  (editorial serif display + serif text + mono), and the signature motif (the
  "signal" equivalent — could be light beams, halftone rings, ripples, etc.).

### Phase 1 — Assets
1. Generate hero + chapter stills via GPT Image (ChatGPT native image mode /
   `chatgpt-native-media` skill). Keep the skeleton; vary only subject/position.
2. Turn 1–2 stills into slow films via Seedance 2.5 (`seedance-2-5-prompting`
   skill) — pan/dolly/transform, 10–15s.
3. Export WebP sequences at 1440px + 768px. Export OG image as an art asset.

### Phase 2 — Build
- **Tier A (3 weeks):** React 19 + Vite + GSAP ScrollTrigger. Video
  backgrounds per section, scroll-reveal animations, CSS/SVG ink effects.
- **Tier B (5 weeks):** React 19 + custom WebGL canvas compositor, custom
  scroll timeline, full shader treatment (paper, ink, dither, burn).

### Phase 3 — Deploy
- Self-host fonts (no third-party font CDN). WebP sequences, responsive sizes,
  lazy loading. Cloudflare Pages/Vercel. OG meta tags with the art hero.

### Phase 4 — The "making of"
- Include original generated stills in the scroll timeline. Optionally show the
  prompt skeleton on screen. Make the process part of the narrative.

## Skills & Tools Used

`chatgpt-native-media` (stills), `seedance-2-5-prompting` (films),
`athabasca-premium-web-design` (rubric/animation patterns), `claude-design` /
`claude-code` (build), `cloudflare-domain-deploy` + `cloudflare-workers-deploy`
(deploy), `social-posting` (launch).