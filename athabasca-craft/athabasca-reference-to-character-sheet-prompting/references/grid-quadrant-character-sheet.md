# Grid quadrant → character sheet reference workflow

Use when the user points at a specific quadrant of a generated 2x2 grid and wants a character sheet for comparison or continuity.

## Steps

1. Resolve the source asset first:

```bash
curl -sS http://127.0.0.1:3000/api/media/asset_... > /tmp/source-asset.json
```

Read `asset.publicUrl`; do not guess the file location.

2. Download the grid:

```bash
curl -L -sS "$PUBLIC_URL" -o /tmp/source-grid.webp
```

3. Crop the requested quadrant. For a standard 2x2 grid:

```bash
# top-left
ffmpeg -y -i /tmp/source-grid.webp -vf 'crop=iw/2:ih/2:0:0' /tmp/ref-top-left.png

# top-right
ffmpeg -y -i /tmp/source-grid.webp -vf 'crop=iw/2:ih/2:iw/2:0' /tmp/ref-top-right.png

# bottom-left
ffmpeg -y -i /tmp/source-grid.webp -vf 'crop=iw/2:ih/2:0:ih/2' /tmp/ref-bottom-left.png

# bottom-right
ffmpeg -y -i /tmp/source-grid.webp -vf 'crop=iw/2:ih/2:iw/2:ih/2' /tmp/ref-bottom-right.png
```

4. Run vision on the crop before generation. Extract concrete traits: age, hair, face shape, complexion, facial hair, body type, wardrobe texture/color, expression, and pose.

5. Generate with true reference conditioning when available:

```python
image_generate(
  aspect_ratio="landscape",
  reference_images=["/tmp/ref-bottom-left.png"],
  prompt="Professional photorealistic character sheet... same exact character... white seamless background..."
)
```

6. Vision-check the output. Report whether it is useful as a continuity sheet and name issues concisely.

7. Persist artifacts through Athabasca:
- reference crop: `phase=visual_dev`, `category=misc`, `sourceKind=generated`, `artifactKind=reference_crop`
- character sheet: `phase=visual_dev`, `category=misc`, `sourceKind=generated`, `artifactKind=character_sheet`

Recommended metadata fields:
- `sourceAssetId`
- `sourceQuadrant`
- `workflow="grid-quadrant-crop-for-character-sheet"` for crop
- `workflow="gpt-image-2-reference-character-sheet"` for sheet
- `provider`, `model`, `prompt`, `characterName`, `version`, `intendedUse`

8. Verify public URLs with `curl -I` before final response.

## Reporting pattern

Keep the user-facing result concise:
- generated asset id + URL
- reference crop asset id + URL
- local media embed if useful (`MEDIA:/abs/path.png`)
- 2–4 sentence comparison/evaluation
