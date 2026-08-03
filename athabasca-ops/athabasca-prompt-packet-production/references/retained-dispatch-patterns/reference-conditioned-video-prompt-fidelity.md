---
name: reference-conditioned-video-prompt-fidelity
description: Dispatch reviewed reference-conditioned video prompt packets without prompt drift and with verified reference semantics.
version: 0.1.0
---

# Reference-Conditioned Video Prompt Fidelity

## Use when
Use for a reviewed multi-shot video packet that will be dispatched with ordered image references.

## Core rule
The reviewed group prompt is the source of truth. Extract its bounded group text and submit it verbatim. Do not summarize, rewrite, or collapse shot detail for API submission. Only apply explicit, approved minimal deltas.

## Dispatch procedure
1. Locate the reviewed packet and extract the group using stable start/end boundaries.
2. Verify every asset ID against its live title and public URL. Never infer a reference from a similarly named file or past use.
3. Produce a semantic map: one role per image—identity, expression, shared scale/blocking, environment, prop, or performance posture.
4. Verify the attached URL order exactly matches `@image1…@imageN` in the submitted prompt.
5. Preserve group text byte-for-byte apart from newline normalization and explicitly approved deltas.
6. Save the generation log, asset ID, and submitted reference order for review.

## Character-reference rules
- Full-body identity controls silhouette, proportions, costume, and gear.
- Expression sheets control face/visor/emote behavior only unless explicitly designated otherwise.
- A shared two-character frame is required when relative height, distance, or staging is critical; designate it as the scale/blocking authority.
- Describe correction deltas in concrete visible terms. Translate emotional intent into posture, prop placement, and spatial relationships.
- Use short exclusions only for observed drift (for example, no helmet horns, plume, crest, or feathers).

## Packet repair
When a render fails or drifts:
- Distinguish dispatch drift (wrong URL/order/text) from model drift (render ignores correctly mapped source).
- Confirm the failing provider received valid, fetchable URLs before attributing failure to prompt length or reference count.
- Keep the original packet text intact; append a clearly labeled minimal corrective delta rather than reconstructing the prompt.

## Verification checklist
- Correct reviewed group source?
- Exact uncompressed group text?
- Verified asset IDs and URLs?
- Reference order matches semantic declarations?
- Identity, expression, and shared-blocking roles are non-conflicting?
- Generation status and server-side log confirmed?
