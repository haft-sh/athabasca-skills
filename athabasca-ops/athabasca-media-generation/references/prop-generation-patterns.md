# Prop Generation Patterns

Learned from Character A project asset triage (2026-05-29). These patterns apply to any prop close-up shot that needs to match a canonical environment.

## Lighting: always match canonical environment

When regenerating a prop for a scene that already has a canonical environment shot:

1. Identify the canonical environment asset ID (e.g., `asset_mpqfuazjeb447e7u`)
2. Analyze its lighting: ambient vs directional, daytime vs nighttime, warm vs cool
3. Specify the lighting explicitly in the prompt — never let the model assume

**Default assumption pitfall**: Models default to dramatic spotlight or golden-hour lighting for prop shots. Always override with "even, soft ambient daytime natural light, no harsh directional shadows, no golden hour" unless the scene is specifically nighttime.

## Framing: close-up prop shots

For prop-only shots (bowl, cap, microwave, plates):
- "Close-up prop shot" in the prompt opening
- "The [prop] is the sole focus of the image, centered in frame"
- "Zoomed in tight on the [prop] — filling the frame"
- The environment surface (couch cushion, table, wall) should be visible beneath/behind the prop but NOT dominate the frame
- "No people visible" unless the shot requires a hand/face

## Reference-matching discipline

Always pass the canonical environment asset as `referenceAssetIds` so the model can match:
- Wall color and material (eggshell, wood paneling, marble)
- Surface texture (cream linen couch, wooden desk, tile)
- Light temperature and direction
- Overall room ambiance

Do NOT just describe "a living room" — specify "the cream linen sectional sofa shown in the reference image" to anchor the generation to the exact environment.

**Pitfall: model invents furniture not in the reference.** Even when you pass a canonical environment as a reference image, the model may generate a brand-new piece of furniture (e.g., a different couch, a different table) instead of placing the prop on the existing furniture visible in the reference. Workaround: be explicit — "sits directly on the cream linen cushion of the main sectional sofa shown in the reference image. Do NOT generate a new couch or table."

## Multi-reference prompting

When passing multiple `referenceAssetIds`, each serves a different purpose. State this in the prompt:
- One reference for the **subject** (e.g., character sheet for cap shape, face features)
- One reference for the **lighting/environment** (e.g., room shot for wall color, light direction)

Example: cap on hook used character sheet (`asset_mpqaokuaubvetraj`) for cap appearance + writing room (`asset_mpqgfarruuw3drs2`) for wall color and window light direction.

## Spatial relationship to other objects

When placing a prop relative to other objects in a room (e.g., "cap on a hook to the right of the swords"), describe the spatial relationship explicitly. The model cannot infer object placement from the reference image alone.

## Food/meal props: specify exact state

For food-related props (plates, bowls, sandwiches):
- "Barely-touched" means: nearly full portions with only one or two bites taken
- "Half-eaten" is ambiguous — models often render empty plates
- Be specific: "a whole sandwich with just a small bite missing" or "a full portion of pasta barely disturbed"
- The comedic intent matters: "meals accumulated over days of obsessive work" vs "someone just finished eating"

## Example: chip bowl v3 (approved)

```
provider: fal-ai
model: openai/gpt-image-2
referenceAssetIds: [canonical living room asset ID]
prompt: Close-up prop shot. A heavy stoneware ceramic bowl in earthy tones, filled with a moderate snack-sized portion of golden salted potato chips — not overflowing, casually arranged. The bowl sits directly on the cream linen cushion of the main sectional sofa shown in the reference image. Zoomed in tight on the bowl and chips — the bowl is the sole focus, filling the frame. The cream couch fabric is visible as the surface beneath. Lighting: even, soft ambient daytime natural light, no harsh directional shadows, no golden hour. Bright and diffused. Photorealistic, cinematic, ARRI Alexa quality. No people visible.
```

## Example: microwave Hot Pocket v2 (approved)

```
provider: fal-ai
model: openai/gpt-image-2
referenceAssetIds: [canonical kitchen asset ID]
prompt: Close-up prop shot of a Hot Pocket inside a microwave, visible through the microwave glass door. The Hot Pocket is golden-brown, slightly crispy, with a small amount of steam rising. The microwave is a modern built-in stainless steel appliance matching the luxurious mansion kitchen shown in the reference — the same high-end kitchen with marble countertops and dark wood cabinetry. Match the warm, even ambient daytime natural lighting from the reference kitchen — bright diffused daylight, no harsh shadows, no dramatic night lighting. The microwave should look like it belongs in this exact kitchen environment. Shot through the glass door at a slight angle. Photorealistic, cinematic, ARRI Alexa quality, anamorphic lens. No people visible.
```

## Example: fridge interior POV v2 (approved)

```
provider: fal-ai
model: openai/gpt-image-2
referenceAssetIds: [canonical kitchen asset ID]
prompt: Close-up POV shot from inside an open double-door stainless steel refrigerator, looking outward. The fridge has two wide doors that swing open, with organized shelves visible on both sides — bottles of craft beer, condiments, leftovers in glass containers, fresh produce. Through the open doors, bright natural daytime light floods in from a large kitchen window, illuminating the interior evenly. The kitchen behind is a luxurious mansion kitchen with marble countertops and dark wood cabinetry. The light is warm and diffused daytime sunlight — NOT nighttime, NOT cool blue fridge glow. The fridge interior feels like a well-stocked luxury appliance in broad daylight. Photorealistic, cinematic, ARRI Alexa quality, anamorphic lens. No people visible.
```

## Example: food plates v3 (approved)

```
provider: fal-ai
model: openai/gpt-image-2
referenceAssetIds: [canonical 2012 writing room asset ID]
prompt: Close-up prop shot. A small wooden side table in a spartan writing room, holding a stack of four white ceramic dinner plates. Each plate has a nearly full, barely-touched meal on it — only one or two bites taken from each. One plate has a whole sandwich with just a small bite missing. Another has a full portion of pasta barely disturbed. Another has a complete serving of rice and chicken with only a fork mark in it. The meals are cold, congealed, clearly abandoned hours ago. The gag is obsessive neglect — the writer was too absorbed to eat. Stray manuscript pages and loose papers scattered around the plates. No typewriter visible. The room has dark wood paneling, cramped space, warm overhead bulb light. Match the austere monk-like environment from the reference image. Photorealistic, cinematic, ARRI Alexa quality. No people visible.
```

## Example: cap on hook v3 (approved)

```
provider: fal-ai
model: openai/gpt-image-2
referenceAssetIds: [canonical 2026 writing room asset ID]
prompt: A brown fisherman cap hanging on a simple wall hook, placed to the right of crossed swords on the wall. The cap matches the character sheet reference — same shape, same fabric, same brim style, only slightly faded from age. The wall is eggshell-colored with classy moldings, matching the 2026 writing room shown in the reference image. The cap is lit by natural window light coming from the left side of the frame, creating soft shadows to the right. The lighting is warm, diffused daytime sunlight — not a spotlight, just natural ambient window illumination. The cap and swords are part of the room decor, not isolated props. Photorealistic, cinematic, ARRI Alexa quality. No people visible.
```

## Example: eye close-up (approved)

```
provider: fal-ai
model: openai/gpt-image-2
referenceAssetIds: [character sheet asset ID, canonical 2012 writing room asset ID]
prompt: Extreme close-up of intense human eyes, low angle looking slightly up. An older man with a heavy white beard, deep furrowed brow, bloodshot determined eyes with fiery intensity. He wears the brown fisherman cap from the character sheet — slightly faded, pulled low over his forehead. The lighting matches a spartan 2012 writing room: warm overhead bulb casting flat golden light, dark wood paneling in soft bokeh behind. Cinematic, ARRI Alexa quality, anamorphic lens flare. The eyes convey obsessive creative hunger — the warrior monk in combat mode. Tight framing on just the eyes and brow, from below.
```
