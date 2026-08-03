# Athabasca character sheet continuity anchors

Use this pattern when the user asks for a character sheet from an existing Athabasca media asset and intends to compare/select continuity anchors for later storyboard regeneration.

## Reusable workflow

1. Resolve the source asset API-first:
   - `GET /api/media/:assetId`
   - Use `asset.publicUrl`, `title`, `phase`, `metadataJson`, and `attachments` as canonical context.
2. Download the image locally only as staging.
3. If the source is a 2x2 Midjourney grid, crop the requested quadrant exactly.
4. If the source is an already-upscaled two-person shot, crop tightly around the target character before generation. This reduces identity contamination from the other actor.
5. Inspect the crop with vision before generating:
   - face structure and expression
   - hair shape/color/styling
   - complexion/eyes/distinct marks
   - wardrobe materials and silhouette
   - pose/emotional cues that should carry into the sheet
6. Generate with reference-conditioned `image_generate` when available:
   - use `reference_images=[local_crop]`
   - still include concrete text cues extracted from vision
   - include anti-drift constraints: same exact person, no other characters, white seamless background, no text/labels/UI.
7. Vision-check the generated sheet for:
   - likeness fidelity
   - wardrobe continuity
   - useful multi-angle/full-body/portrait/action poses
   - face drift across panels
   - hand/anatomy or accidental text issues.
8. Persist both durable artifacts through `POST /api/projects/:slug/media`:
   - reference crop: `artifactKind=reference_crop`, source asset/quadrant/crop path metadata
   - character sheet: `artifactKind=character_sheet`, character name/version, provider/model, source asset/crop asset, intended use, prompt when practical.
9. Verify each R2 URL with `curl -I` and report concise asset IDs + URLs.
10. If the user selects one sheet as final, patch that existing media asset instead of re-uploading:
    - `PATCH /api/projects/:slug/media/:assetId`
    - merge existing `metadataJson`
    - add `characterAnchorStatus: "final"`, `isFinalCharacterSheet: true`, `finalizedForContinuityPass: true`, `characterRole`, `supersedesAlternateAssetIds`, and `decisionNote`.
    - verify with `GET /api/media/:assetId`.

## Prompt structure

For romcom photoreal character sheets, a good prompt shape is:

```text
Create a photorealistic high-budget Hollywood romantic-comedy character sheet for the [male/female] lead only, using the supplied image as the likeness and wardrobe reference. Pure white seamless studio background, no text, no labels, no watermark, no UI, no environment, no extra characters. The same exact person appears in every panel with strict face continuity, hair continuity, body continuity, and wardrobe continuity.

Character: [age range, regional/ethnic vibe if visible, complexion, build, presence]. Preserve the reference traits: [eyes, brows, face shape, nose, lips, cheekbones, marks, expression]. Hair: [color, highlights, length, texture, styling]. Wardrobe must match the reference: [fabric, color, silhouette, straps/collar, tailoring].

Show a clean multi-pose continuity sheet: full-body front view, full-body back view, left profile, right profile, three-quarter views, emotional/story action poses required by the sketch, half-body portrait, close facial portrait. Keep the character alone in every pose. Bright neutral studio lighting, premium cinematic realism, sharp focus, realistic anatomy and hands, detailed fabric texture, designed as a production continuity reference sheet.
```

## Reporting style

Keep the user-facing report short:
- source asset
- reference crop asset
- generated character sheet asset
- R2 verification status
- local `MEDIA:` preview
- 2-3 sentence evaluation comparing likeness/utility/issues.

Avoid narrating every command unless debugging is relevant.
