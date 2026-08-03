---
name: athabasca-replicate-image-model-wiring
description: Verify, add, and operationalize Replicate still-image models in Athabasca without exposing fake or unverified model slugs.
triggers:
  - User asks to add a new Replicate still-image model to Athabasca
  - A Replicate model slug is uncertain and must be verified before wiring
  - A newly added Replicate image model works in docs but fails in Athabasca runtime
version: 1.0.0
---

# Athabasca Replicate image model wiring

Use this when the task is to expose a new **Replicate still-image model** through Athabasca's normalized image-generation API.

## Core rule

Do **not** monkey-patch guessed slugs into the runtime and leave them there.

A model is only real once you have verified all three:
1. the Replicate model page exists
2. the Replicate model API resolves successfully
3. a real Athabasca project-scoped generation probe succeeds

## Workflow

1. **Verify the exact model slug**
   - Check `replicate.com/<owner>/<model>/api`
   - Query Replicate's model API for the same slug
   - Do not trust hearsay or obvious-looking guessed names

2. **Inspect the upstream schema**
   - Capture real input fields from Replicate's model metadata
   - Confirm reference-image limits, size options, aspect-ratio options, and output format fields
   - Do not assume a new model shares the exact request shape of an older sibling

3. **Patch Athabasca in the minimum necessary places**
   - Add the model to `src/shared/generation-config.ts`
   - Extend the Replicate worker's supported-model map
   - Add model-specific request-shape logic when schema differs
   - Update reference-image allowlists in normalized generation routing if needed

4. **Typecheck and restart the live runtime**
   - Run the project's typecheck
   - Restart the actual Athabasca dev service
   - Do not claim support from a code diff alone

5. **Run a cheap probe first**
   - Use a trivial image prompt through `POST /api/projects/:slug/generate/image`
   - Verify the generation persists as Athabasca media
   - Only then run the user's expensive or reference-heavy job

6. **Watch for false timeout failures**
   - If the model is slow, inspect the worker poll timeout before declaring the provider broken
   - A longer-running model may need a larger polling window even when the upstream generation succeeds

## Proven durable lessons

### Guessed slugs are a trap
A guessed model id such as `bytedance/seedream-5` can pass local validation changes but still fail upstream with `422 Invalid version or not permitted`.

Operational rule: if the model page or model API does not validate the exact slug, do not add it.

### Seedream-family request shapes can differ
Do not assume every Seedream variant uses the same limits or payload knobs.

Validate per-model fields such as:
- `image_input` reference count
- `size`
- `output_format`
- `aspect_ratio`
- any sequential/multi-image generation controls

### Timeouts can be local, not upstream
A real model can succeed upstream while Athabasca times out locally because the polling window is too short.

When the first large real generation fails with timeout after a cheap probe succeeded, check worker poll duration before classifying the model as unsupported.

## Support files

- `references/replicate-seedream-5-pro.md` — verified notes for wiring Replicate Seedream 5 Pro into Athabasca, including schema and timeout lessons.

## Pitfalls

- Do not expose guessed model slugs in UI/API options.
- Do not copy the request body from a sibling model without checking actual Replicate schema.
- Do not report success after patching config only; verify via a real project-scoped generation.
- Do not treat the first timeout as proof of incompatibility when the worker poll window may be too short.
