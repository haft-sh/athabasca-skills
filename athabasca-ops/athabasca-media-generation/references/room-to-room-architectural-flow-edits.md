# Room-to-Room Architectural Flow Edits

## When to use

When the user asks to edit an existing room/hallway asset so that it opens into or connects with a **different room** shown in a second reference image. Both references are environments, not characters/props.

Examples:
- "Edit the hallway so it leads to the kitchen instead of the living room"
- "Make this doorway open into the study shown in asset_X"
- "Replace the couch at the end of the hall with the kitchen"

## Prompt pattern that works

```
Edit the first reference image only. Keep the exact same [composition anchors: camera angle, perspective, wall color, moldings, flooring, lighting]. Make one change: at the end of the hallway, instead of [what's currently there], the hallway now opens into the [room type] shown in the second reference image. The [room] should flow naturally from the hallway — same bright airy aesthetic, same warm natural lighting.

Critical spatial instruction: [camera-relative placement, e.g. "the fridge is on the LEFT side as seen from the hallway, not straight ahead"]. [What should be visible ahead and to the right/left].

The transition from [room A] to [room B] should feel architecturally natural — no door or wall dividing them. Keep everything else the same: [list non-negotiable details].
```

## Key elements

1. **Reference 1 = base room to edit** (the hallway/room whose composition stays)
2. **Reference 2 = destination room** (the kitchen/study/etc. that replaces what's at the end)
3. **Camera-relative spatial instructions** — "left side of the kitchen as seen from the hallway" not "left side of the image" (ambiguous). Be explicit about viewer orientation.
4. **Architectural flow language** — "opens into", "no door or wall dividing", "transition should feel natural". This prevents the model from inserting a doorframe or hard boundary.
5. **Preservation anchors** — list every detail that must not drift: crown molding, wainscoting, hardwood floor, recessed light, framed art, etc.

## API call shape

```bash
curl -sS --max-time 180 -X POST http://localhost:3000/api/projects/:slug/generate/image \
  -H 'Content-Type: application/json' \
  --data-binary '{
    "prompt": "...",
    "provider": "fal-ai",
    "model": "openai/gpt-image-2",
    "aspectRatio": "landscape",
    "phase": "visual_dev",
    "title": "...",
    "provenanceNote": "GPT Image 2 via fal.ai. Edit of [room A asset] — replaced [old destination] with [new room] ([room B asset]), [key spatial instruction].",
    "referenceAssetIds": ["asset_hallway_id", "asset_kitchen_id"]
  }'
```

## Pitfalls

- **"Left side" ambiguity**: Always specify "left side as seen from the hallway/camera/viewer". The model interprets "left" relative to the room's own orientation otherwise, which can flip the fridge to the wrong wall.
- **Over-specifying the destination room**: Don't describe the kitchen in detail — the second reference image carries that. Just name the key spatial constraint (fridge position, island location) and let the model read the rest from the reference.
- **Hard boundaries**: Without explicit "no door or wall" language, GPT Image 2 tends to insert a doorframe or arch at the transition point. Always say the spaces should flow without division.
- **Drift in the base room**: The model may subtly change wall color, molding style, or floor tone in the base room when it's trying to match the second reference. List preservation anchors explicitly.

## Successful example (Character A project, May 2026)

Edited `asset_mpqh99zkf3kasmh8` (hallway to living room) → `asset_mpqi2h13s3jy2dof` (hallway to kitchen, fridge on left).

- Reference 1: hallway with cream walls, classical moldings, hardwood floor, living room visible at end
- Reference 2: mansion kitchen with stainless steel fridge, marble island, white Shaker cabinetry
- Key instruction: "fridge is on the LEFT side of the kitchen as seen from the hallway (not straight ahead at the end of the corridor)"
- Result: hallway preserved exactly, fridge tucked into left-wall alcove, kitchen island visible ahead, natural architectural flow
