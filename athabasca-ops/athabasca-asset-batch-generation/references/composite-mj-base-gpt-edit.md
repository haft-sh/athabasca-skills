# Composite Pattern: Midjourney Base + GPT Image 2 Edit Pass

**When to use:** shots requiring both a cinematic environment and a specific foreground element that neither model can reliably produce in a single pass.

**Generic example:**
- Step 1 (MJ): environment-only plate with the screen/device/background state locked correctly
- Step 2 (GPT Image 2): edit the MJ output to add the foreground subject, prop glow, UI insert, or other precise element

> ⚠️ **Provider note for Step 2:** `openai-codex` does not currently support `referenceAssetIds` for edit passes, so the routed path requires `fal-ai`. Before using `fal-ai` for this composite step, state the constraint and get the user's explicit approval.

## Why the composite approach works

- **Midjourney** excels at environments, mood, lighting, texture, and spatial depth.
- **GPT Image 2** excels at precise spatial edits and adding specific elements.
- **Combining them:** MJ provides cinematic quality, GPT Image 2 provides precise compositing.

## API call shapes

### Step 1: Midjourney base
```text
POST /api/projects/:slug/generate/image
provider: midjourney
model: midjourney-v8.1
prompt: <environment-only prompt>
aspectRatio: landscape
```

### Step 2: GPT Image 2 edit via fal-ai
```text
POST /api/projects/:slug/generate/image
provider: fal-ai
model: openai/gpt-image-2
prompt: <add the foreground element while preserving the existing background>
referenceAssetIds: [<mj_base_asset_id>]
aspectRatio: landscape
```

## When NOT to composite
- character portrait with no environment need
- environment-only plate
- simple single-element prop close-up
- shots where a direct model route already satisfies both environment and subject

## Common pitfalls
1. edit pass adds elements to the wrong area — be explicit about placement.
2. MJ base already contains an unwanted subject — ask for an empty environment.
3. paid fallback approval skipped — do not use `fal-ai` without approval.
4. edit pass flattens the lighting — keep the background-preservation language tight.
