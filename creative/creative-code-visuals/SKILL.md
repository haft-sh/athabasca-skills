---
name: creative-code-visuals
description: "Use when producing generated or animated visual media with code/tools: ASCII art/video, p5.js sketches, Manim animations, TouchDesigner MCP scenes, Pretext typography demos, and pixel-art images or animations."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [creative-coding, ascii, p5js, manim, touchdesigner, pretext, pixel-art, animation]
    related_skills: [creative-design-artifacts]
---

# Creative Code Visuals

## Overview

This umbrella covers visual outputs generated through code or interactive visual tooling: ASCII art/video, p5.js sketches, Manim animations, TouchDesigner scenes, Pretext typographic demos, and pixel-art stills/animations. The common requirement is to produce a runnable/rendered artifact and verify the result.

## When to Use

- Generate text banners, cowsay/boxes, image-to-ASCII, or colored ASCII video/GIFs.
- Build p5.js generative art, shaders, interactive sketches, or 3D browser visuals.
- Create Manim/3Blue1Brown-style educational animations.
- Control TouchDesigner via MCP to build real-time node networks and visuals.
- Build typography/text-layout demos with Pretext.
- Create pixel-art sprites, scenes, palettes, or pixel-art video.

## Router

| Need | Route |
| --- | --- |
| Terminal text art or image-to-ASCII | ASCII art |
| Video/audio converted into ASCII MP4/GIF | ASCII video |
| Browser generative art / interaction / shader | p5.js |
| Mathematical or explainer animation | Manim |
| Real-time visual node network | TouchDesigner MCP |
| Text-as-geometry / kinetic typography | Pretext |
| Retro sprite/scene/palette | Pixel art |

## Universal Production Loop

1. Select medium and output format: text, HTML, image, GIF, MP4, project file, or TouchDesigner network.
2. Check local prerequisites and install/use a project-local environment if needed.
3. Generate source files/scripts with clear parameters.
4. Render/export the artifact.
5. Verify the artifact exists and, when possible, inspect a screenshot/frame or run a smoke test.

## ASCII Art and Video

ASCII art is best for terminal banners, playful text, and image-to-text conversions. ASCII video is a full media pipeline: input extraction, frame conversion, color/effect handling, audio sync if needed, and MP4/GIF output. Keep legibility high; do not overfilter until the subject disappears.

## p5.js and Pretext

Use p5.js for canvas/WebGL, interaction, animation, and generative systems. Use Pretext when text measurement/layout itself is the creative material. For browser outputs, create a self-contained HTML artifact and verify it opens.

## Manim

Use Manim for math, algorithms, data, and paper explainers where camera motion, equations, and staged transformations matter. Render short scenes first before full-quality export.

## TouchDesigner MCP

Use TouchDesigner when the user has a running TouchDesigner instance and wants real-time visuals. Discover existing operators first, then create/wire nodes incrementally and verify network state through MCP responses/screenshots.

## Pixel Art

Use pixel-art workflows for era palettes (NES, Game Boy, PICO-8), sprites, tiles, low-resolution scenes, or animations. Keep resolution constraints explicit and preserve palette consistency.

## Common Pitfalls

1. **Stopping at source code.** Render/export and verify the visual artifact.
2. **Ignoring medium constraints.** Pixel art, ASCII, and diagrams need different density and contrast.
3. **Running long renders blind.** Use small previews/smoke renders first.
4. **Assuming TouchDesigner state.** Discover the live network before editing.
5. **Overloading one file.** Keep reusable scripts/templates in support files when projects grow.

## Verification Checklist

- [ ] Medium route selected from the table.
- [ ] Source files/scripts created in an appropriate workspace.
- [ ] Output artifact rendered/exported.
- [ ] Artifact existence and basic visual correctness verified.
- [ ] Final response includes path/URL and reproduction command if useful.
