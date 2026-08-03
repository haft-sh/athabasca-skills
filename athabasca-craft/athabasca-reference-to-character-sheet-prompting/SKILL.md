---
name: athabasca-reference-to-character-sheet-prompting
description: Derive high-fidelity white-background character-sheet prompts from user-supplied visual references when direct reference-conditioned image generation is unavailable or unreliable.
triggers:
  - User wants a character sheet based on attached images or project media
  - Need to preserve likeness/costume continuity without naming protected IP directly
  - Image generator only supports text prompts, or reference-image conditioning is not exposed through the current tool
---

# Reference-to-character-sheet prompting

Use this when the user wants a visual character sheet that matches supplied references as closely as possible, especially for Athabasca visual development, but the available image generation tool does **not** accept reference images directly.

## Core lesson
First determine whether the current image-generation path can accept reference images.

- If the tool supports image conditioning (for example Hermes `image_generate` with `reference_images` and GPT Image 2 / OpenAI Codex), use the actual reference image path or URL directly and state that it is reference-conditioned.
- If the generator cannot take image inputs, do **not** imply that it can. Instead:
  1. analyze the reference images with vision
  2. extract a concrete face/costume/pose brief
  3. turn that into a white-background character-sheet prompt
  4. say clearly that the result is text-guided, not true image-conditioned generation

This prevents a mismatch between the user's desired method ("use my reference images") and what the tool can actually do, while still taking advantage of true reference conditioning when it is available.

## When to use
- User says "make a character sheet" and means a real visual sheet, not a text spec
- User provides one or more stills and wants the result to match a specific character closely
- User wants continuity/fidelity poses on a white background
- Prompting around franchise/trademark sensitivity requires descriptive likeness cues rather than named IP

## Recommended provider for real-person character sheets

**Seedream 5.0 via Replicate** (`provider: "replicate"`, `model: "bytedance/seedream-5-lite"`) with `referenceAssetIds` is the best model for character sheets based on real people. It:
- Accepts reference images and preserves likeness
- Produces natural human proportions (unlike Gemini which produces toy/dwarf proportions)
- Is more permissive with real person content policy than GPT Image 2 (which blocks real people across ALL providers)
- Supports up to 14 reference images

**Fallback:** Seedream 4.5 Edit via fal.ai (`provider: "fal-ai"`, `model: "fal-ai/bytedance/seedream/v4.5/edit"`).

**Critical prompt pitfall:** Do NOT use the word "character" in prompts for realistic human images — it triggers action-figure/toy proportions in Seedream and most other models. Use "Film costume department reference sheet" or "Photographic reference sheet" instead.

## Required method

### 1) Gather the right reference signals
Use `vision_analyze` on the most useful reference images and ask for:
- facial structure
- hairline / hair length / texture
- beard and mustache shape
- eye color
- expression
- wardrobe details
- body language / pose / silhouette
- what must carry into a white-background character sheet

A good split is:
- one close portrait reference for face/hair/facial hair/costume detail
- one wider action reference for body language and silhouette

If the user names a quadrant from a generated 2x2 grid, first resolve the asset with `GET /api/media/:assetId`, download `asset.publicUrl`, crop the exact quadrant locally, and use that crop as the character reference. For Midjourney grids this is usually:
- top-left: `crop=iw/2:ih/2:0:0`
- top-right: `crop=iw/2:ih/2:iw/2:0`
- bottom-left: `crop=iw/2:ih/2:0:ih/2`
- bottom-right: `crop=iw/2:ih/2:iw/2:ih/2`

Example with ffmpeg:
```bash
ffmpeg -y -i grid.webp -vf 'crop=iw/2:ih/2:0:ih/2' /tmp/reference-bottom-left.png
```

If the user supplies an already-upscaled shot containing two people, crop tightly around the requested character before passing it as a reference image. This reduces identity contamination from the other actor and lets the prompt focus on the target character's face, hair, costume, and expression. Persist the crop as a durable reference asset when it will anchor future continuity work.

Then inspect the crop with vision before prompting, even when using it directly as a `reference_images` input.

### 2) Convert the references into renderable cues
Do not rely on abstract words like "continuity" or "same vibe". Convert the analysis into concrete prompt ingredients:
- exact facial-hair silhouette (for example: thick mustache with dense side-whiskers / mutton-chop beard, lighter center chin)
- eye color
- hairline recession / crop length
- costume layers and materials
- pose list for the sheet
- white seamless background
- no text / no labels / no UI / no environment

### 3) Use true character-sheet language
For users asking for a character sheet, say what that means visually:
- pure white seamless background
- studio-lit
- clean multi-pose lineup
- front, back, left profile, right profile, three-quarter left, three-quarter right
- optional commanding pose / victory pose / portrait crop
- same exact man in every panel
- strict face continuity and costume continuity

### 4) Include anti-drift constraints
Character-sheet prompts benefit from explicit continuity instructions:
- same exact face in every panel
- same exact body and costume in every panel
- no extra characters
- no props unless requested
- no environment storytelling
- no text, labels, watermark, UI, borders

### 4.5) Expression-sheet layout constraints
When the user wants a **friendly expression sheet** rather than a simple turnaround:
- explicitly ask for a **clean model-sheet grid/composite** with separated panels on a pure white background
- explicitly forbid **blurred overlays, fog, smoke, painterly wipes, merged panels, collage artifacts, or floating partial faces between panels**
- name the exact expressions you need (for example: neutral, excited, meditative calm, blink/wink, curious, reassuring) instead of relying on "different expressions"
- if eye readability matters, say so directly: for example, **"clear readable blue eyes"** rather than only "friendly" or "personal"
- prefer **character-reference assets only** as `referenceAssetIds` for identity work; avoid mixing in storyboard grids or scene stills unless the user specifically wants scene/composition carryover, because mixed reference classes can contaminate the sheet layout or expression clarity

### 5) Be honest about limitations after generation
If the user wanted true reference-conditioned output, say so plainly:
- the generator result is derived from prompt text extracted from the references
- it is not a direct image+text conditioning pass unless the current tool actually supports that

## Direct reference-conditioned generation recipe

When `image_generate` accepts `reference_images`, prefer this path for continuity work:

1. Resolve Athabasca asset IDs with `GET /api/media/:assetId`; use the returned `publicUrl` or a local downloaded/cropped file as the reference.
2. If the reference is a quadrant in a 2x2 grid, crop it exactly and persist the crop if it will become a durable comparison/reference artifact.
3. Run `vision_analyze` on the crop/reference to extract visible traits and catch ambiguity before generation.
4. Generate the sheet with `image_generate(reference_images=[...])`, while still writing concrete text cues for face, hair, wardrobe, pose list, and anti-drift constraints.
5. Vision-check the generated sheet for identity, wardrobe continuity, pose usefulness, and artifacts.
6. Persist both the generated sheet and any durable reference crop through `POST /api/projects/:slug/media` with provenance metadata: `sourceAssetId`, `sourceQuadrant` when applicable, `workflow`, `provider`, `model`, `prompt`, and intended use.
7. If the user later picks one sheet as final, mark that media asset as the final continuity anchor instead of only noting it in chat. Use `PATCH /api/projects/:slug/media/:assetId` to update `metadataJson` while preserving existing fields. Recommended keys: `characterName`, `characterRole`, `characterAnchorStatus: "final"`, `isFinalCharacterSheet: true`, `finalizedForContinuityPass: true`, `supersedesAlternateAssetIds`, and a short `decisionNote`.
8. Verify R2 availability with a HEAD request before reporting the asset as persisted.

See `references/grid-quadrant-character-sheet.md` for a compact worked pattern.
See `references/athabasca-character-anchor-selection.md` for marking a user-selected character sheet as the final continuity anchor in project media metadata.
See `references/athabasca-character-sheet-continuity.md` for the end-to-end Athabasca pattern: resolve asset, crop target character, generate a reference-conditioned character sheet, persist crop/sheet, verify R2, and mark final anchors.

## Prompt template

```text
Professional character sheet on a pure white seamless background, no text, no labels, no watermark, no UI, no props, no environment, no extra characters. The same exact man appears in every panel with strict face continuity and costume continuity.

[insert precise face brief from vision analysis]
[insert precise costume brief from vision analysis]

Show a clean multi-pose continuity sheet: full-body front view, full-body back view, left profile, right profile, three-quarter front left, three-quarter front right, relaxed neutral standing pose, commanding wide-legged captain stance, [optional action pose], half-body stern portrait, close facial portrait.

Bright neutral studio lighting suitable for a white-background model sheet, premium cinematic realism, highly detailed, sharp focus, designed as a continuity reference sheet.
```

## Negative prompt ideas
If the model supports negatives, use terms like:
- text, labels, captions, watermark, logo, UI
- extra characters
- inconsistent costume
- different haircut, different beard, different eye color
- busy background, ship deck background
- cartoon, anime, painterly
- cropped body, deformed hands
- asymmetrical identity drift

## Practical Athabasca notes
- If the user says "don’t populate the DB," keep the work conversation-only.
- If they later want the refs attached, use the Athabasca media API and preserve provenance notes.
- If the user wants a franchise-adjacent likeness without direct naming, avoid the IP name in the prompt and rely on descriptive visual cues.

## Pitfalls
- Do not claim the image generator used the reference images if it only accepted text.
- Do not answer with a text spec when the user explicitly asked you to generate an image.
- Do not overuse vague phrases like "Euron-like" without translating them into physical features.
- Do not forget that a character sheet normally means a white background with clean multi-angle presentation.
- **Always use Athabasca API** (`POST /api/projects/:slug/generate/image`) for generation — never curl provider endpoints directly. The Athabasca endpoint handles auth, R2 persistence, DB records, and provenance.
- **Use image-to-image when a reference photo exists** — pass it via `referenceAssetIds` with a SHORT prompt. Don't write verbose text descriptions of what the image already shows. The image does the heavy lifting; the text describes only the delta (poses, background, clothing changes).
- **GPT Image 2 blocks real person likeness** across all downstream providers (fal, replicate, byteplus, web UI). This is a platform-level content policy restriction. Route real-person character sheets to Seedream instead.

## What changed from experience
This skill exists because a user wanted a white-background captain character sheet based on attached project media and expected the image generator to use those references directly. The correct recovery path was to extract face/costume/pose cues from the references with vision and build a stricter character-sheet prompt, while explicitly stating the limitation that the current image generator call was text-guided rather than direct image-conditioned generation.
