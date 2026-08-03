---
name: athabasca-video-generation-guardrails
description: Preflight guardrails for Athabasca video generations where provider capabilities, reference-image handling, and canonical media URLs materially affect whether a paid run is usable.
version: 1.0.0
---

# Athabasca Video Generation Guardrails

Use this alongside broader video-generation workflows when the task involves paid generations, multiple character references, or provider switching.

This skill exists because a provider can appear healthy and still be the wrong route for the creative intent if its normalized path does not actually forward the reference stack the prompt assumes.

## When to use

- the user asks to run a paid Athabasca video generation
- the prompt names multiple `@imageN` references
- character-sheet fidelity matters
- you are switching providers to overcome a limitation
- a provider was recently re-enabled and needs a real wiring check

## Core rule

Do not treat prompt text like transport reality.

If the prompt says `@image2`, `@image3`, etc., that does **not** mean the provider received those images. Verify the actual route semantics before dispatching.

## Required preflight

1. Check live capabilities.
2. Check whether the chosen provider/model/mode truly supports the needed reference strategy.
3. Inspect the normalized Athabasca path or known skill/docs for whether those references are actually forwarded upstream.
4. If the route only supports a single first-frame image but the prompt depends on multiple character-sheet references, stop and tell the user before dispatching.
5. Treat that mismatch as a material blocker, not a minor caveat.

## the user-specific operating rule

If a provider limitation is likely to make the output unusable — especially missing multi-reference character conditioning — disclose it **before** spending the run.

## BytePlus reference-image hygiene

For BytePlus multi-reference runs:

- use canonical Athabasca `asset.publicUrl` values from live media records
- do not guess `generated_*.png` URLs from filenames, titles, or memory
- if BytePlus returns a `content[n].image_url` resource-not-found error, re-resolve every reference from the asset record and retry with a new idempotency key

## Reference-borne text and panel-marker hygiene

Storyboard references can contaminate generated video with panel digits, shot labels, corner numbers, or reinterpreted text on helmets and scoreboards. For paid reference-to-video runs:

1. Inspect reference pixels for editorial marks before dispatch.
2. Prefer a clean canonical derivative when available; removing contaminated pixels is more reliable than prompt suppression.
3. If no clean derivative exists, say `No text on screen`, identify the exact artifact and reference slot to ignore, and repeat the constraint in the affected shot plus the closing prompt block.
4. Preserve only text explicitly requested by the user, such as natural jersey numbers.
5. After completion, inspect sampled frames across the clip—not only the generated preview image. Check corners, helmets, scoreboards, signage, captions, watermarks, and UI-like marks.
6. Do not equate `the corner 6 is gone` with `the clip has no unwanted text`. Report each remaining glyph and its location honestly.
7. If contamination persists, recommend a clean-reference derivative or post-production cleanup instead of repeatedly paying to regenerate from the same marked source.

## Dispatch checklist

- provider/model visible in live capabilities
- mode supports the intended reference strategy
- every user-supplied `asset_...` ID has been resolved through `GET /api/media/:assetId`
- preview exposes the ordered mapping `@imageN` → asset ID → canonical `publicUrl`; do not call ID-supplied media “attached images”
- every reference URL is a canonical Athabasca public URL and transport order exactly matches the prompt’s `@imageN` order
- actual reference pixels have been checked for material facts such as daylight/night, palette, wardrobe, and geography; do not carry contradictory prose forward from an older shot list
- if there is no source video, remove `@video1`, extension/continuation language, and video-reference inputs rather than sending conceptual placeholders
- idempotency key prepared
- if dialogue attribution matters, make speaker ownership explicit in the prompt and split long dialogue across shots when requested
- if the run is a probe rather than a likely deliverable, label it as such in provenance

## Verification after completion

- inspect the **individual** generation log, not only a truncated generation-log list response
- confirm `upstreamRequestJson` contains the complete ordered reference-image stack
- for BytePlus image-only `reference-to-video` runs, confirm every intended image appears as a `reference_image` entry and that no `reference_video` was sent; a prior video is not required merely because the normalized mode is named `reference-to-video`
- confirm requested duration, resolution, aspect ratio, and audio setting reached the provider
- for strict delivery settings, download and `ffprobe` the canonical persisted MP4; provider status and generation metadata alone are insufficient. Verify delivered runtime, video raster/display geometry, and presence of an audio stream when audio was requested. Treat a requested `16:9` ratio as unverified unless the delivered geometry is actually 16:9. If it differs, report a provider-output discrepancy and do not silently crop or overwrite the canonical asset.
- **Observed BytePlus Seedance 2.0 case:** runs accepted `ratio: "16:9"` and reported `864 × 480` in normalized metadata, but the persisted H.264 MP4 probed as `864 × 496`. Use the delivered ffprobe geometry as the source of truth and explicitly disclose this mismatch; offer a derivative crop/reframe only when the user asks for one.
- confirm zero video references were forwarded when none were intended
- distinguish “provider was reachable” from “provider honored the creative constraint”
- verify the resulting Athabasca asset, project attachment, R2-backed public URL, and a real HTTP 200 response
- if the result is non-canonical because the route still drifted, mark it accordingly

### Client-timeout recovery

A client/tool timeout does not establish that a paid BytePlus run failed. With the original idempotency key intact, query the existing generation log by its ID (or locate it by idempotency key) before considering any retry. If it reaches `completed`, use the persisted Athabasca asset and do not submit a fresh request.

## Relationship to other skills

This overlaps with broader Athabasca video-generation guidance. Prefer the main workflow skill for end-to-end generation steps, and use this guardrail skill for the preflight decision about whether a given provider/mode is honest-to-goodness capable of the run the user is asking for.
