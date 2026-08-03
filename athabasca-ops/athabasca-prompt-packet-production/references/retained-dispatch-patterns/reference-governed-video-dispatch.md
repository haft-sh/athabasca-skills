---
name: reference-governed-video-dispatch
description: Dispatch reviewed multi-shot AI-video prompt packets without prompt drift or reference-authority mistakes.
version: 0.1.0
---

# Reference-Governed Video Dispatch

Use when dispatching a reviewed prompt packet that has multiple image references, recurring characters, or paid video generations.

## Core rule

The approved packet prompt is the dispatch source of truth. Extract the requested group’s **complete prompt block verbatim** and send it unchanged except for line-ending normalization. Never summarize, paraphrase, collapse shot fields, or reconstruct a prompt from its outline.

For a corrective rerun, retain the full approved prompt and append only a bounded correction. State that all existing shot camera, composition, focus, blocking, and emotion remain unchanged unless the user explicitly changes them.

## Pre-dispatch reference audit

1. Resolve every asset ID to its public URL and visually verify the actual image, not merely its filename/title.
2. Write down one authority per reference: identity, expression, shared-scale/blocking, environment geography, prop, or emotional posture.
3. Preserve the user-approved order of distinct reference URLs. Do not silently swap variants or remove a reference.
4. Flag competing references that control the same environment, character, or prop. Ask or make the smallest supported consolidation.
5. For a recurring two-character scene, use:
   - character A identity authority;
   - character B identity/expression authority;
   - a verified shared two-shot reference when relative scale or blocking matters;
   - only the environment/prop/posture authorities genuinely needed.

## Prompt wording that protects identity and geography

- Describe a character’s visual identity separately from emitted light, emotional tone, or narrative function. Do not allow terms like `small glowing guide` to replace an approved character design.
- Translate continuity into renderable constraints: equal child-scale height, left/right placement, open-ground separation, plinth between subjects, forearm carrying a shield, exact helmet silhouette.
- Use precise negative exclusions only for observed drift: e.g. `smooth leather helmet, no horns, plume, crest, feathers, spikes, or ornament`.
- Do not call an output canonical until visual review confirms identity, scale, prop handling, and spatial geography.

## Verification

Before reporting completion:
- verify the provider accepted the request and record asset ID, log ID, public URL, and exact reference URL order;
- when a request times out client-side, query its idempotency record before retrying;
- distinguish wiring failure (wrong/missing URLs), packet drift (changed prompt), and model drift (correct dispatch, wrong render).

## Pitfalls

- A successful generation does not prove reference compliance.
- A similarly titled reference may be the wrong visual version; visually inspect it before dispatch.
- Treat a provider’s generic error as unclassified until retry/idempotency evidence isolates the cause; do not assert a reference-count limit without evidence.
