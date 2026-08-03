# Canonical prop/detail repair with GPT Image 2

Use this pattern when an otherwise-approved Athabasca still has one incorrect localized element and the user asks for a redo/fix using GPT Image 2.

The lesson is generic: make an atomic image change while preserving composition and continuity. Do not encode project-specific characters, props, or one-off art direction in this reference.

## Proven pattern

Submit a project-scoped image generation request through native Codex/GPT Image 2 when available:

- `provider`: `openai-codex`
- `model`: `gpt-image-2`
- `referenceAssetIds`: `[problem_asset_id, canonical_control_asset_id]`
- `aspectRatio`: match the original shot's normalized aspect class (`landscape`, `portrait`, or `square`)
- `phase`: optional media tag; preserve it only when useful for organization

Reference ordering:

1. The exact base shot to preserve composition.
2. The canonical prop, character, costume, or environment reference controlling the replacement detail.

## Prompt shape

Use a strict minimal-delta edit prompt:

```text
Use reference image 1 as the exact base shot: same camera, composition, pose, environment, lighting, character scale, expression, costume, render style, and framing.
This is a strict minimal-delta repair.
The only required change is [target detail]: replace any [wrong variants] with the canonical [description] shown in reference image 2.
The corrected [detail] must read clearly as [desired material/shape/color/function], not [forbidden interpretations].
Preserve everything else exactly: [identity/continuity details], body pose, background, mood, depth, and continuity.
No extra characters, no text, no watermark.
```

## Hard-negative pattern

When the model repeatedly misreads the target detail, name both the desired reading and forbidden readings:

```text
replace any [wrong object/material/color/shape] with the canonical [correct object/material/color/shape] shown in reference image 2. The corrected detail must read clearly as [safe/soft/simple/brand-appropriate reading], not [metal/sharp/sci-fi/realistic/incorrect-color/etc.].
```

Use project-neutral descriptors. The point is not the specific object; the point is constraining the model to change only one localized thing.

## Provenance

Make the provenance note explicit:

```text
GPT Image 2 minimal-delta edit of [problem_asset_id] using canonical [control type] reference [canonical_asset_id] to replace [incorrect detail] with [canonical detail] while preserving the shot.
```

## Verification

After generation:

1. Verify Athabasca persistence and the public URL.
2. Compare the target detail against the canonical reference.
3. Confirm the composition, identity, lighting, background, and pose did not drift.
4. If `HEAD` fails on the media host, verify with authenticated API readback or a short `GET` instead of treating the `HEAD` rejection as generation failure.
