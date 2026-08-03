# Dynamic first-frame Seedance regeneration

Use this when the user wants to animate an existing still with a more dynamic image-to-video prompt, especially when the still should be preserved as the exact opening frame.

## What belongs here

This reference is for operational guidance only:
- how to resolve the source still
- how to structure a reusable dynamic-motion prompt
- which Seedance provider to prefer
- what runtime pitfalls to watch for
- how to report the result tersely

Do **not** hardcode film-specific subjects, named characters, or one project's visual language into the reusable pattern.

## Provider routing

For Seedance 2.0, follow the cost-sensitive routing from the main skill:
1. BytePlus first
2. Replicate second
3. fal.ai only if the user explicitly asks or BytePlus/Replicate are verified blocked or unavailable

Do not follow project defaults blindly if they point Seedance to fal.ai.

## Source lookup

1. If the user gives an explicit `asset_...` ID, call `GET /api/media/:assetId` first.
2. Use that asset's `publicUrl` as the canonical `imageUrl`.
3. If the user refers to board numbers, shortlist numbers, or grid quadrants, resolve those through the relevant uploaded board artifact or source-grid metadata before generating.
4. If the user specifically wants the true Midjourney upscale rather than a crop, recover the real `U1`-`U4` result first and then animate that returned asset.

## Prompt pattern

When the user wants the still preserved as the opening image, start with:

> Use the supplied image as the exact first frame.

Then adapt the rest of the prompt to the source still while keeping the structure generic:
- preserve the source image's handmade/material/render style
- avoid slow or static animation
- establish a clear motion contrast between foreground and background action
- include a short pause or anticipation beat before the main subject launches or commits to motion
- ask for layered depth cues such as parallax, drifting atmosphere, camera push, or responsive shadows
- explicitly reject choppy / low-frame-rate motion when smooth motion is desired
- append the standard Seedance quality suffix when appropriate: `4K, Ultra HD, Rich details, Sharp clarity, Cinematic texture, Natural colors, Stable picture No Music`

The exact subject, environment, and action should be rewritten for the current project rather than copied from an earlier film.

## Default settings used successfully

- `mode: image-to-video`
- `provider: byteplus`
- `model: dreamina-seedance-2-0-260128`
- `resolution: 480p`
- `aspectRatio: landscape`
- `duration: 5` or `6` depending on the request
- `generateAudio: true`
- include an idempotency key naming project + provider + source asset + duration + version

## Reporting

Keep final reports terse:
- provider/model
- settings
- first-frame asset ID
- public URL
- verification status (`200 video/mp4`)

## Pitfalls

- If the user says "Seedance 2.0," choose the provider explicitly from current routing/capabilities; do not rely on deprecated project-level default provider fields.
- If a generation times out, inspect generation logs before retrying; retry with a new idempotency key only when the previous log is terminal failed.
- Preserve prompt/generation provenance so future media review can reconstruct the source still and action prompt.
- Hermes `athabasca_project_request` may double-serialize the `json` body, causing `422 "expected object, received string"`. Work around it with `execute_code` + Python `urllib.request` using `ATHABASCA_API_TOKEN` to POST raw JSON bytes directly.
- Video generation can exceed the tool's default timeout. Use a generous timeout and, if needed, verify completion by checking recent project media or generation logs.
