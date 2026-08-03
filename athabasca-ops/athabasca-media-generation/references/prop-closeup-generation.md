# Prop Close-Up Generation Patterns

## When to Use

When generating standalone prop images (food, objects, tools) that need to visually belong to an already-established canonical environment (living room, kitchen, writing room, etc.).

## Core Principles

1. **Always use the canonical environment asset as reference** — pass the green-tagged environment asset via `referenceAssetIds`. Never let the model invent new furniture or surfaces.

2. **Analyze reference lighting first** — Before writing the prompt, use `vision_analyze` on the canonical environment asset to extract:
   - Light type (ambient/even vs directional/harsh shadows)
   - Color temperature (warm golden vs cool blue)
   - Time of day (daytime vs nighttime)
   - Key surfaces and materials (couch fabric type, countertop material)

3. **Frame the prop as sole focus** — Prop shots should be tight close-ups with the prop filling the frame. Specify:
   - "Close-up prop shot"
   - "zoomed in tight on [the prop] — the [prop] is the sole focus, filling the frame"
   - "No people visible" (unless hands/fingers are part of the gag)

4. **Place on the correct surface** — If the prop sits on something (couch cushion, side table, countertop), name the specific surface from the canonical reference. E.g. "resting on the cream linen cushion of the main sectional sofa" — not "on a couch" which lets the model invent a different one.

5. **Match lighting explicitly** — Don't just say "match the lighting." Describe the lighting characteristics:
   - "even, soft ambient daytime natural light from large windows"
   - "no harsh directional shadows, no golden hour"
   - "bright but diffused"
   - OR "warm overhead bulb light, sparse and monk-like" for austere rooms

6. **Control quantity for gag intent** — When a prop communicates a narrative idea (accumulation, neglect, obsession), specify the exact quantity and state:
   - "at most four plates" (not "a tower of plates")
   - "barely-touched, nearly-full meals — only one or two bites taken" (not "half-eaten")
   - The gag intent matters more than visual drama

## Provider Selection for Props

- **`fal-ai` with `openai/gpt-image-2`** — best for clean single prop stills with reference anchoring. the user's preferred path for prop generation.
- **`google-gemini` with `gemini-3-pro-image-preview`** — good fallback when fal times out or for complex compositional requirements.

## Prompt Template

```
Close-up prop shot. [Prop description with exact state/quantity]. 
[Placement: "resting on/sitting on [specific surface from canonical reference]"]. 
[Room context: brief description matching canonical reference]. 
[Lighting: explicit description matching reference lighting characteristics]. 
Photorealistic, cinematic, ARRI Alexa quality. No people visible.
```

## Common Pitfalls

- **Inventing new furniture** — the model will generate a generic couch/table instead of matching the canonical environment. Always pass the environment as reference.
- **Wrong lighting** — default cinematic lighting tends toward dramatic/directional. Explicitly specify "even ambient" or "bright diffused" when the canonical room has natural daytime light.
- **Wrong surface** — "on a couch" generates a random couch. "on the cream linen cushion of the main sectional sofa shown in the reference" anchors it.
- **Exaggerated quantity** — "tower of plates" generates 15+ plates when the gag only needs 4. Specify the maximum.
- **Wrong food state** — "half-eaten" means consumed; "barely-touched" means mostly full with one bite. The comedy depends on this distinction.
