---
name: athabasca-environment-layout-regeneration
description: Preserve an existing environment image's aesthetic while remapping architecture/layout to a second reference such as a floor plan, elevation sheet, or destination room.
version: 1.0.0
author: Hermes Agent (Athabasca)
metadata:
  hermes:
    tags: [athabasca, image-generation, environment-edit, floor-plan, layout, reference-images, replicate, seedream]
    related_skills: [athabasca-media-generation]
---

# Athabasca Environment Layout Regeneration

## When to use

Use this when the user wants to keep the **same room/environment identity and aesthetic** from one image, but change the spatial geography so it matches another reference.

Typical asks:
- regenerate image 1 with the same vibe, but make the room obey image 2's floor plan
- keep this hallway/living-room aesthetic, but have it open into the room shown in the second reference
- preserve the same materials/lighting/styling, but remap the architecture to the supplied elevations or plan

This is an **environment remap** skill, not a generic style-transfer skill and not a character-reference skill.

## Core rule

Split the task into two separable goals and state both explicitly in the prompt:
1. **aesthetic continuity** — preserve the original room's look, lighting, materials, lens feel, and decorative density
2. **spatial fidelity** — obey the second reference's wall relationships, openings, furniture placement, and circulation

If you do not explicitly weight both, the model usually over-preserves the vibe and under-obeys the layout.

## Workflow

### 1) Import both references into the target project first
For project-scoped image generation with `referenceAssetIds`, import both references into the target project:
- the original image whose aesthetic should be preserved
- the layout reference: floor plan, elevation sheet, or destination room

Do not rely on cross-project asset IDs or off-platform URLs when project-local references are easy to create.

### 2) Use a valid media category for imported references
When importing visual references through `POST /api/projects/:slug/media`, do **not** assume `category: "reference"` exists.

A durable safe default for source stills / plans / elevations is:
- `category: "moodboard"`

If you send an unsupported category, the route returns a validation error.

### 3) Verify the live provider/model surface before promising it
Do not claim a provider/model exists just because the vendor may offer it somewhere. Check the live Athabasca runtime / config first.

Example durable lesson:
- in the observed runtime, Replicate exposed `bytedance/seedream-5-lite`, not a non-lite Seedream 5 / 5 Pro path

So: **promise only what the live runtime exposes**.

### 4) Build the prompt in 3 blocks

#### A. Aesthetic-preservation block
Specify:
- lighting/time of day
- materials and palette
- lens/composition feel
- clutter density / dressing density
- emotional tone
- what must remain the same about the room's identity

#### B. Spatial-remap block
Specify:
- overall dimensions if known
- ceiling height if known
- wall assignments by cardinal direction or camera-relative position
- door/window placement
- which furniture belongs to which wall
- circulation / spacing constraints

#### C. Identity-preservation block
Explicitly say:
- same room, not a different room
- same design language
- same theme / memorabilia / room-function identity
- remapped architecture, not a brand-new set dressing concept

## Prompt pattern

```text
Recreate the first reference image with the exact same aesthetic and overall look and feel: [lighting, materials, palette, mood, rendering style].

Keep the same visual style, mood, materials, lighting quality, lens feel, and decorative density as the first image. Do not change the design language.

However, change the room layout so it conforms to the spatial geography of the second reference image, which is a [floor plan / elevation sheet / destination room]. The resulting room must read as a believable [dimensions] room with [ceiling height], and the architectural relationships must match the reference:

- [wall assignment 1]
- [wall assignment 2]
- [wall assignment 3]
- [wall assignment 4]
- [window / door placement]
- [circulation constraint]

Preserve the same room identity from the first image: [theme / objects / emotional continuity]. This should feel like the same room re-laid out to match the second reference, not a different room.

Prioritize spatial fidelity to the second reference while preserving the exact aesthetic language of the first image.
```

## When the first pass is too loose spatially
This is common. A strong first pass may preserve the vibe but only partially prove the requested geometry.

If the user cares more about architecture than atmosphere, rerun with stronger language such as:
- "architectural fidelity over composition"
- "spatial geography is non-negotiable"
- "do not invent a new layout"
- "the room must read as this exact floor plan, not a loose reinterpretation"
- "camera angle must clearly reveal the requested wall relationships"

## Review checklist after generation
Check whether the result:
- preserves the original room's lighting/material identity
- clearly shows the dominant wall/furniture relationship the user asked for
- actually places key objects on the requested walls
- reveals enough of the room to verify geography
- feels like the same environment rather than a merely similar one

If the image is aesthetically excellent but spatially ambiguous, do not overclaim success. Call it a partial hit and rerun with stricter camera/layout constraints.

## Pitfalls

- Using an unsupported media category like `reference` when importing source images
- Overstating model availability instead of checking what the live runtime exposes
- Letting the prompt bias too hard toward style, causing architecture drift
- Using a camera angle that hides the room relationships you need to verify
- Reporting a floor-plan match when the composition only implies, rather than proves, the requested geometry

## Relationship to other skills

This overlaps with `athabasca-media-generation`, but it is narrower in a useful class-level way: it governs **environment remaps driven by second-reference layout control**. Keep provider-specific and route-specific quirks here only when they materially affect this class of task.
