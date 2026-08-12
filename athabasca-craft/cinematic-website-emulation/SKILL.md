---
name: cinematic-website-emulation
description: Use for Pear-style scroll-scrubbed cinematic sites.
version: 1.1.0
triggers:
  - User wants to build a Pear-style cinematic landing page
  - User wants a scroll-driven storytelling site with AI-generated art
  - User wants to recreate the pear.no visual experience
metadata:
  hermes:
    tags: [cinematic, website, scrollytelling, pear, canvas, webgl, image-sequence, continuity]
    related_skills: [athabasca-premium-web-design, reference-led-video-prompting, athabasca-video-continuity]
---

# Cinematic Website Emulation

Build Pear-style single-viewport scrollytelling as one authored visual journey. Art direction, source-film generation, frame handoffs, scroll architecture, and QA are one system.

## What Pear Actually Does

Verified against the live `pear.no` experience and its loaded media on 2026-08-12:

- The primary story is rendered into fixed canvas/WebGL layers.
- Scroll directly scrubs large WebP frame sequences; it does not merely trigger independently looping background videos.
- Dedicated transition canvases and shader/compositing controls add texture, masking, and displacement, but the compositor is not what creates narrative continuity.
- Continuity is authored into the source motion. A gilded pear is pushed toward camera, keeps its stem and screen position, changes material into scarred wood, and resolves into a living grafted branch. Other sequences keep following the same column/branch/fruit geometry while the camera moves through classical tableaux, grafting, an orchard, and a handoff.
- The viewer sees movement and transformation *inside one spatially coherent shot*. There is no moment where an unrelated landscape becomes visible because its opacity increased.

This distinction is mandatory:

> A matched horizon plus an opacity fade is still a cross-dissolve. Pear-style continuity is an authored camera move or in-frame transformation that is scroll-scrubbed frame by frame.

Smoothing may be applied to scroll velocity or frame selection. It must not be used to disguise independent media with opacity.

## Immediate Rejection Criteria

Reject the implementation before visual polish if any of these are true:

- each chapter owns an unrelated looping video;
- chapter progression is implemented by cross-fading background opacity;
- “match cut” means only similar sky colors or horizon heights;
- transition direction is described in text but no exact endpoint images are supplied to generation;
- clip B is generated from a recreation of clip A's last frame instead of the exact same file;
- forward scroll plays a video but reverse scroll cannot return deterministically to prior frames;
- HTTP 200 is the only production verification.

Text, navigation, and editorial overlays may fade. The underlying visual world must remain spatially continuous.

## Phase 0: Reference Teardown

Before creating assets:

1. Open the reference site and inspect it visually at multiple scroll positions.
2. Inspect its live media/canvas architecture and network-loaded assets.
3. Capture a chronological contact sheet of source films or frame sequences where accessible.
4. Name the recurring anchor in every transition: silhouette, stem, horizon, light source, contour, camera axis, or motion vector.
5. Separate observed fact from inference. Do not infer Pear's mechanism from screenshots alone when the live site is accessible.

Record the teardown in a continuity map before prompting a model.

## Phase 1: Art Direction and Continuity Bible

### Choose one visual world

Select a painterly or cinematic language with stable:

- palette and grade;
- lens/camera height;
- light direction;
- texture and grain;
- atmospheric depth;
- subject scale conventions;
- editorial negative space.

Good starting points include Romanticism, Baroque, Golden Age illustration, Ukiyo-e, Art Nouveau, and controlled surrealism. Do not imitate a living artist by name.

### Define one journey, not a gallery

Write a single sentence that can be filmed as a continuous journey. Example:

> A witness follows one beam of dawn across the ocean; the beam becomes a harbor beacon, the beacon becomes an idea bulb, and its filament becomes the illuminated roads of a shared future.

Every chapter must be a waypoint in that sentence.

### Build the continuity map

For every segment, specify:

| Field | Required decision |
|---|---|
| Start authority | Exact image file and its role |
| End authority | Exact image file and its role |
| Persistent anchor | Object/line/light that survives the whole segment |
| Camera trajectory | Pan, truck, orbit, push, pull, tilt, or crane |
| Screen direction | Fixed left/right/up/down vector |
| Material transformation | What changes and what cannot change |
| Light lock | Source position, angle, intensity, and color |
| Environment lock | Horizon, landmarks, topology, weather, and grade |
| Prohibitions | Cuts, fades, teleports, relighting, extra subjects, text |

A transition without a visible persistent anchor is not approved.

## Phase 2: Generate Canonical Keyframes

### Endpoint authority rule

Generate continuity pairs, not isolated chapter art:

1. Create the opening hero.
2. Generate the first destination as a continuation of that exact hero.
3. Reuse that exact destination file as both segment A's end authority and segment B's start authority.
4. Repeat for the complete journey.

Never regenerate “the same” seam frame. Reuse the same bytes.

### Keyframe acceptance

For each pair, verify visually:

- same aspect ratio and safe crop;
- compatible camera axis and focal length;
- anchor occupies a plausible continuous trajectory;
- horizon and major geometry do not jump;
- light source does not switch sides;
- grade, texture, and atmospheric density remain one world;
- no invented text, labels, logos, or accidental subjects.

Build one labeled contact sheet and review it before paid video generation.

## Phase 3: Author the Motion

### Preferred architecture: one source film

The best result is one continuous source film covering the complete journey. It can hold on chapter compositions for editorial copy, but it does not reset the world between chapters.

### Segmented fallback

If provider duration limits require several clips:

- use first-frame + last-frame generation when supported;
- attach the exact preceding endpoint and exact next endpoint in the generation payload;
- state the authority of each reference explicitly;
- use 4–8 second single-motion segments rather than multi-beat prompts;
- keep the camera moving in one named direction;
- prohibit cuts, dissolves, black frames, speed ramps, teleports, and exposure resets;
- generate silent footage unless audio is part of the product;
- concatenate only after seam QA.

Text-only continuity is not conditioning. “Continue smoothly” without attached endpoint authorities is insufficient.

### Motion prompt scaffold

```text
START AUTHORITY: @image1 controls the exact first frame, camera axis,
geometry, palette, lighting, atmosphere, and object state.
END AUTHORITY: @image2 controls the exact final composition and anchor.

One continuous shot. The camera [single trajectory]. The [persistent anchor]
stays on [screen path] while [one material/spatial transformation]. Preserve
[light lock] and [environment lock]. Arrive naturally at @image2 and hold.

No cut, cross-dissolve, fade, teleport, relight, environment swap, extra
subject, text, logo, border, collage, jitter, or camera-axis reversal.
```

### Seam QA

For every clip boundary:

1. Extract clip A's last stable frame and clip B's first stable frame.
2. Compare them side by side with the canonical seam authority.
3. Reject identity, geometry, light, horizon, or grade jumps.
4. Inspect the full clip at normal speed and while frame-stepping.
5. Verify reverse traversal remains coherent.

A short overlap may be trimmed to the best common frame. Do not hide a bad seam with a dissolve.

## Phase 4: Export a Scroll-Scrubbable Sequence

Prefer deterministic image sequences for a Pear-level result.

Example extraction:

```bash
ffmpeg -i journey-master.mp4 \
  -vf "fps=12,scale=1440:-2:flags=lanczos" \
  public/films/journey/1440/f_%04d.webp

ffmpeg -i journey-master.mp4 \
  -vf "fps=12,scale=768:-2:flags=lanczos" \
  public/films/journey/768/f_%04d.webp
```

Also keep:

- one poster/first frame;
- a reduced-motion representative frame;
- a contact sheet;
- source prompt and endpoint provenance;
- the source MP4 for re-encoding.

Choose frame rate by motion complexity and payload budget. Twelve fps is a useful starting point; test lower/higher rates visually.

## Phase 5: Build the Site

### Required media architecture

- native vertical document scroll;
- one fixed full-viewport canvas or media compositor;
- a large semantic scroll spacer;
- scroll progress mapped deterministically to frame index;
- neighboring-frame preloading and bounded cache behavior;
- chapter copy mapped to frame ranges, not separate background assets;
- `requestAnimationFrame` drawing outside React render state;
- responsive object-cover/source crops;
- reduced-motion fallback and keyboard/touch support.

Do not set `body { overflow: hidden }` when the controller depends on native `scrollY`.

### Minimal frame mapping

```ts
const maxScroll = document.documentElement.scrollHeight - innerHeight;
const progress = maxScroll > 0 ? scrollY / maxScroll : 0;
const target = Math.round(progress * (frameCount - 1));
requestAnimationFrame(() => drawFrame(target));
```

Lerp the numeric scroll/frame target if desired. Do not lerp opacity between unrelated chapter worlds.

### Canvas compositor

A Tier A build may use a 2D canvas with preloaded WebP frames. A Tier B build may add WebGL for:

- paper/grain treatment;
- dither or halftone motifs;
- light bloom;
- local displacement around a transformation;
- masked editorial reveals.

Shaders enrich authored continuity; they do not substitute for it.

### Loading

- show a real progress signal based on loaded critical frames;
- preload the first playable window before revealing the stage;
- continue loading ahead and behind the current frame;
- avoid downloading every high-resolution frame before first paint;
- provide an image/poster fallback if canvas or decoding fails.

## Phase 6: Production Verification

Validate interactively and visually:

- mouse wheel and touchpad advance the journey;
- touch and keyboard navigation work;
- reversing scroll reverses the visual motion deterministically;
- no chapter seam exposes a dissolve or unrelated layer;
- text remains readable without covering the persistent anchor;
- mobile crops preserve the anchor and subject;
- reduced motion is usable;
- frame payload, decoding, and memory are acceptable;
- deployed production is inspected at beginning, every seam, and end;
- browser console has no failed media requests or runtime errors.

HTTP 200, build success, and lint success are necessary but not visual acceptance.

## Quality Rubric

| Dimension | Weight | Acceptance |
|---|---:|---|
| Authored continuity | 25 | One continuous journey; no opacity-disguised clip swaps |
| Seam fidelity | 15 | Exact endpoint reuse and no geometry/light jump |
| Scroll determinism | 15 | Frame-accurate forward and reverse control |
| Visual authority | 10 | Coherent palette, lens, texture, and scale |
| Narrative transformation | 10 | Every morph advances the central idea |
| Typography and layout | 10 | Editorial authority without obscuring anchors |
| Loading/performance | 10 | Progressive, responsive, bounded |
| Accessibility | 5 | Keyboard, touch, fallback, reduced motion |

A result scoring below full marks on authored continuity is not “Pear-style,” regardless of polish elsewhere.
