---
name: athabasca-asset-batch-generation
description: Use when asked to batch generate all assets from a shot breakdown or asset inventory document — generates, critiques, and uploads production-quality stills for an entire film sequence or act.
version: 0.3.0
author: Hermes Agent (Athabasca)
---

# Athabasca Asset Batch Generation

Goal-directed iteration over every asset in a shot breakdown or asset inventory. For each item: read context, generate, critique, regenerate if needed, attach to project, and populate the inventory HTML.

## Trigger

User says (or means):
- "batch generate assets from the asset inventory"
- "generate all assets for [project/act]"
- "create all the stills for shot breakdown x"

## Pre-Flight

Before generating, read and internalize:

1. **Asset inventory HTML** — the canonical shot list (from project media or document cache)
2. **Shot breakdown markdown** — subject, action, composition, visual focus, emotion, continuity notes per shot
3. **Script** — full narrative context, character voices, key dialogue
4. **Project media library** — check for existing assets to avoid duplication

Build a **generation queue** from the inventory:
- Exclude: `PURE VOID / BLACK` shots (S001, S038 — sound only, no visual content)
- Number assets sequentially as `asset_001`, `asset_002`, etc. in shot order
- Track: generated image URL, canonical pick, regeneration count, notes

## Style Guidance

**Variant:** Default to the more ominous continuity track unless the user specifies otherwise. When a batch comes with a preferred grade/motif package, write those continuity anchors down before generating.

**Global continuity anchors:**
- note any indicator-light color shifts by shot range
- note any screen-state rules (for example, a device that must remain off)
- note any recurring screen direction / eyeline conventions
- note any POV camera constraints that should stay fixed across the batch

## Model Routing

| Shot type | Preferred model | Fallback |
|-----------|-----------------|----------|
| Cinematic establishing shots (exteriors, keynote stage, living room) | Midjourney v8.1 | GPT Images 2 |
| Character (human) | GPT Images 2 (openai-codex) | Midjourney |
| Character (realistic animal likeness) | Seedream 5.0 Lite (replicate) | GPT Images 2 |
| Props (collar, delivery box, collar bell, leash) | GPT Images 2 (openai-codex) | Midjourney |
| Environments with specific spatial layout needs | Midjourney v8.1 | GPT Images 2 |
| Screen/UI inserts (ChatGPT, DaVinci, Wikipedia panel) | GPT Images 2 (openai-codex) | GPT Images 2 (fal-ai) |
| Composites (background + foreground/UI element) | Midjourney base + GPT Images 2 edit pass ⚠️ paid fallback may be required | — |
| Title card | GPT Images 2 (openai-codex) | — |
| Montage/split-frame B-roll | Midjourney v8.1 | GPT Images 2 |

**Model routing priority:**
- **openai-codex** (GPT Image 2) is the primary for GPT Image 2 work — uses your OpenAI subscription, no extra fal.ai credit cost.
- **fal-ai** (GPT Image 2) is the fallback only when openai-codex quota is exhausted (5-hour or weekly limit).
- **Midjourney** is always available via BYOA Discord and is the default for cinematic work.
- **Seedream 5.0 Lite** via replicate is the best animal likeness model — use it for pivotal animal shots before falling back to Midjourney.

**Model-specific rules:**
- **Gemini/Nano Banana:** Avoid for character likeness work (poor fidelity for real animals/people). Use Seedream 5.0 Lite or GPT Images 2 instead.
- **GPT Images 2 via openai-codex:** Best for composites, UI mockups, character sheets, and editing existing images with specific changes. Primary route — use this before fal-ai.
- **GPT Images 2 via fal-ai:** ⚠️ **Paid fallback.** fal.ai credits cost money. Route here only after openai-codex exhaustion AND the user explicitly approves. Even when `referenceAssetIds` is the reason (fal-ai's `/edit` endpoint is currently the only Athena-capable path for referenced GPT Image 2), state the constraint and get permission before using it.
- **Midjourney v8.1:** Best for cinematic establishing shots, environments, mood pieces, and montage material.
- **Seedream 5.0 Lite:** Use when realistic animal likeness is the primary requirement.

> ⚠️ **Standing rule:** Never route GPT Image 2 through `fal-ai` by default. openai-codex is always the first choice. fal-ai is a paid fallback that requires explicit the user approval before use.

## Composite Pattern (Key Technique)

For shots that need both a background/environment AND a specific foreground element (screen, prop, character):

1. **Generate the background with Midjourney** — captures the cinematic environment, lighting, atmosphere
2. **Generate or extract the foreground element** — prop, screen mockup, collar close-up via GPT Images 2
3. **Edit via GPT Images 2** — use the Midjourney output as the input image and describe the changes you need (add the screen, add the collar, etc.)

This two-step pattern produces higher-quality results than asking a single model to do both simultaneously. See `references/composite-mj-base-gpt-edit.md` for API call shapes, prompt templates, and common pitfalls.

## Generation Workflow

### Per-shot loop

1. **Read the shot** — extract: ID, title, subject, action, composition, emotion, continuity notes from the shot breakdown
2. **Check for existing asset** — skip if already attached to this shot
3. **Choose model and approach** — route based on shot type
4. **Write prompt** — use the Midjourney or GPT Images 2 skill for prompt authoring
5. **Generate** — run the generation
6. **Critique** — use vision to evaluate: does it match the description? Does it serve the story purpose? Is the emotion right?
7. **Decide:** if poor, regenerate (up to 2 iterations before flagging for review)
8. **Upload** — attach to project with `POST /api/projects/:slug/media`
9. **Tag** — appropriate tags (see tagging convention below)
10. **Mark canonical** — if this iteration is the best so far and you have high confidence, mark `colorTag: "green"` (otherwise leave neutral for user review)
11. **Update inventory HTML** — swap the placeholder `<img>` src for the actual image URL
12. **Increment counter** — next asset

### When to flag for review instead of regenerating

- Shot involves a specific character or animal likeness that isn't matching after 2 regens
- Shot is narratively pivotal (the reflection shot S030, the clipping S017, the "dog?" Wikipedia shot S028)
- Style is inconsistent with adjacent shots after 2 regens
- You are genuinely unsure what the shot should look like

### When to skip regeneration and accept

- The shot is functionally correct (the right subject, the right emotion)
- Lighting/grade is close enough but not perfect
- You have high confidence in the asset and want to earn the canonical vote

## Tagging Convention

Apply **minimal, search-friendly tags**. Plain text search on titles is enabled — do not duplicate what titles already capture.

| Shot type | Tags |
|-----------|------|
| Establishing shot | `establishing-shot` |
| Character (human) | `character` |
| Character (animal) | `animal` |
| Environment / set | `environment` |
| Prop | `prop` |
| Screen/UI insert | `ui-element` |
| Cutaway / B-roll | `broll` |
| Composite | `composite` |
| Title card | `title-card` |

**Per-asset tags** (add to the above as appropriate):
- `variant-a` — applied to all assets for this batch (style variant)
- `asset-001` through `asset-035` — chronological order tag (enables ascending/descending review ordering)
- `canonical-candidate` — applied when you vote for this as the canonical version

**Provenance tag** always included: `act-i`, `seq-[N]`

## Upload Shape

```
POST /api/projects/:slug/media
phase=storyboard
category=generated
sourceKind=generated
title=[Shot ID] [Shot Title] — Asset [N]
provenanceNote=[brief description]
tags=[asset-001,character,seq-5,variant-a]
colorTag=green   # only if canonical candidate
file=@<local_file>
```

## Inventory HTML Update

After each asset is generated and uploaded, update the inventory HTML file:
1. Replace `<div class="placeholder-img">...</div>` in the matching row with `<img src="[publicUrl]">`
2. Add `canonical` class to the canonical candidate row
3. Save the updated HTML alongside the original with `_populated` suffix

## Pitfalls

- **Regeneration without direction:** If a shot is consistently failing, stop and flag for review rather than burning iterations. Art director judgment is the constraint.
- **Inconsistent grading:** Midjourney B-roll shots and GPT Images 2 character shots may not match in grade. For the inventory, accept the variation — color grading is a post-production decision, not a generation constraint.
- **Animal likeness:** Midjourney v8.1 produces serviceable but not always faithful animal likeness. For pivotal animal shots, try GPT Image 2 or Seedream 5.0 Lite as fallback. Do not spend more than 2 iterations before flagging for review.
- **Void shots:** Never attempt to generate pure void / black shots unless the user explicitly wants a visual plate. Sound-only beats often appear in visual inventories; verify the description before generating.
- **Reflection composites:** If a shot needs an off-screen reflection plus a precisely placed foreground subject, generate an environment-only base first, then add the foreground element with a targeted edit pass. If it still doesn't land, flag for review.
- **Inventory semantics:** Do not assume every row in a character section needs a visual. Some rows are placeholders for off-screen or sound-only beats; verify before generating.

## Skill Version History

- **v0.3.0** — Corrected GPT Image 2 provider routing: `openai-codex` is the primary (free via the user's OpenAI subscription), `fal-ai` is a paid fallback requiring explicit the user approval. Updated model-specific rules, standing rule callout, and all provider references throughout.
- **v0.2.0** — Updated pitfalls from an early production batch run. Added void-shot detection logic, reflection-composite technique, and model routing refinements (Midjourney via `/api/projects/:slug/generate/image`, GPT Image 2 via `fal-ai`).
- **v0.1.0** — initial version, generated from an early production batch run
