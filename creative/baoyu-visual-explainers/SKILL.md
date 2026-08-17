---
name: baoyu-visual-explainers
description: "Use when creating Baoyu-style visual explainers: article illustrations, knowledge comics, and infographics. Selects the right format, style/palette system, prompt construction route, and output structure for educational or explanatory visuals."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [baoyu, illustration, comics, infographics, visual-explainers]
    related_skills: [claude-design, popular-web-designs]
---

# Baoyu Visual Explainers

## Overview

This umbrella covers the Baoyu family of explanatory visual content: single article illustrations, multi-panel knowledge comics, and structured infographics. Use it to choose the right artifact class, then apply the relevant composition, style, palette, and prompt-construction rules.

The key maintainer rule is format-first selection. Do not create separate one-off skills for each visual artifact type; keep format-specific details as subsections or support files under this umbrella.

## When to Use

- The user asks for an article illustration, hero image, or conceptual editorial visual.
- The user asks for an educational/knowledge comic, biography comic, tutorial comic, or storyboarded explanation.
- The user asks for an infographic, visual summary, comparison chart, process diagram, or data-light explainer.
- The request is in Chinese/English mixed context and benefits from Baoyu-style prompt catalogues, style presets, palettes, and layout recipes.

Do **not** use this for general web UI mockups (`claude-design`, `sketch`, `popular-web-designs`) or technical architecture diagrams (`architecture-diagram`, `excalidraw`).

## Format Router

| User need | Choose | Core output |
| --- | --- | --- |
| One idea, article, essay, newsletter, or abstract concept | Article illustration | One strong image prompt with type × style × palette consistency |
| A concept needs sequential explanation, character continuity, or comic panels | Knowledge comic | Storyboard, panel beats, character sheet, art/tone preset |
| A concept needs structured comparison, hierarchy, timeline, framework, or process | Infographic | Structured content template, layout choice, style choice, labels |

## Article Illustration Pattern

Use article illustrations for single-image editorial visuals. First identify the illustration type (conceptual metaphor, scene, object study, UI-ish card, symbolic collage, etc.), then pick a coherent style and palette. Keep the prompt compact but explicit about subject, composition, mood, palette, and avoidances. Consistency matters more than piling on style words.

## Knowledge Comic Pattern

Use comics when information must unfold over time. Start with the teaching objective, then draft panel beats before visual details. Decide whether the comic needs recurring characters, a narrator, diagrams inside panels, or a pure visual metaphor. Preserve character continuity through a mini character template and keep each panel's text short.

## Infographic Pattern

Use infographics when the structure is the main value. Convert the source material into a small schema: title, sections, key facts, relationships, and emphasis. Then choose the layout (matrix, timeline, ladder, radial map, process flow, comparison cards, etc.) and style (technical schematic, retro grid, hand-drawn education, origami, bold graphic, chalkboard, aged academia). Labels should be readable and hierarchy should be obvious.

## Prompt Construction Workflow

1. Extract the explanatory goal and intended audience.
2. Select format: illustration, comic, or infographic.
3. Choose style and palette as a pair; do not mix unrelated aesthetics casually.
4. Draft the artifact-specific structure:
   - illustration: subject + metaphor + composition + palette
   - comic: panels + beats + recurring visual elements
   - infographic: data/schema + layout + label hierarchy
5. Add constraints: white/transparent background if needed, aspect ratio, language of labels, text density, and avoidances.
6. Return paste-ready prompts plus a short rationale when helpful.

## Common Pitfalls

1. **Choosing an infographic for a metaphor.** If there is no structured content, use article illustration instead.
2. **Choosing a comic for a static framework.** If sequence is not meaningful, an infographic is clearer.
3. **Style soup.** Pick one style family and one palette system; conflicting descriptors degrade generation.
4. **Too much text in images.** Keep labels short; move explanations outside the prompt when possible.
5. **Skipping the format router.** The old separate skills had overlapping triggers; route by artifact class, not by skill name.

## Verification Checklist

- [ ] Artifact class selected explicitly.
- [ ] Style and palette are coherent.
- [ ] Structure matches the artifact: scene, panels, or layout.
- [ ] Prompt is paste-ready and includes text-language/aspect/background constraints if needed.
