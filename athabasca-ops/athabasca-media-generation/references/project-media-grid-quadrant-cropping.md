# Project-media grid quadrant cropping for GPT Image 2 reference edits

Use this when the user names a **specific quadrant** of an Athabasca-persisted storyboard grid asset and wants GPT Image 2 to use that quadrant as the composition/image-prompt anchor.

## Rule

Do **not** pass the full 2x2 Midjourney grid when the user asked for a quadrant like `top left`.
Do **not** silently substitute a previously upscaled quadrant unless the user asked for that upscale.

Instead:
1. Resolve the named `asset_...` grid to its canonical `publicUrl`.
2. Crop the requested quadrant locally.
3. Persist that crop back into Athabasca as a new media asset with provenance pointing to the source grid asset.
4. Use the persisted crop's `publicUrl` as **reference 1** in Hermes `image_generate`.
5. Use the final character sheets as later references (`reference 2`, `reference 3`, etc.).
6. Persist the generated result back into Athabasca and attach it to the shot.

## Recommended provenance for the crop asset

- `phase=storyboard`
- `category=misc`
- `sourceKind=generated`
- Title like: `Prenup Shot 003 grid top-left quadrant crop`
- Provenance note like: `Derived by Hermes from asset_<gridId> by cropping the top-left quadrant for GPT Image 2 continuity regeneration.`

## Recommended prompt role ordering

- `reference 1` = quadrant crop = composition / pose / location anchor
- `reference 2` = final male character sheet = identity anchor
- `reference 3` = final female character sheet = identity anchor

Say this explicitly in the prompt so GPT Image 2 does not treat all references as equally interchangeable.

## Example crop command

```bash
ffmpeg -y \
  -i 'https://media.wheretoaccess.com/.../shot_003_grid.webp' \
  -vf 'crop=iw/2:ih/2:0:0' \
  /tmp/shot_003_grid_top_left.png
```

Quadrant offsets for a 2x2 grid:
- top-left: `crop=iw/2:ih/2:0:0`
- top-right: `crop=iw/2:ih/2:iw/2:0`
- bottom-left: `crop=iw/2:ih/2:0:ih/2`
- bottom-right: `crop=iw/2:ih/2:iw/2:ih/2`

## Verification checklist

Before reporting success, confirm:
- the requested quadrant was cropped, not the full grid
- the crop was persisted as a new Athabasca asset with source-grid provenance
- the generated still preserves the quadrant composition rather than drifting to a different panel feel
- the result was attached to the intended shot

## Common pitfall

If the user says `use the top left quadrant of this grid as image prompt`, that means the **grid panel itself** is the visual anchor. Do not reinterpret the request as `find an existing upscale from this shot` unless the user explicitly asks for the upscale instead.