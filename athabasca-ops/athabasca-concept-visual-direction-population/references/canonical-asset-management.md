# Canonical Asset Management Convention

Canonical-asset management for Athabasca visual development.

## Convention

**Color tags** = canonical status
- 🟢 **Green** = approved reference asset for the project
- 🟡 **Yellow** = superseded by a newer approved asset
- Other colors can be used for reject, experimental, or special review states

**Ratings** = visual quality
- 5 stars = high quality
- Ratings are independent of canonical status

**Tags** = descriptive metadata
- scene, location, mood, prop, era, technical details
- include role tags such as `canonical-location`, `canonical-character`, or `canonical-prop`
- keep tags descriptive rather than story-lore-heavy when possible

**Generated images only get canonical tags.** Moodboards, external photos, and imported reference images should not usually be marked green because they are working inputs, not locked production assets.

## API Endpoints

### Set `colorTag` and `ratingStars`
```bash
curl -sS -X PATCH "http://localhost:3000/api/projects/:slug/media/:assetId" \
  -H 'Content-Type: application/json' \
  --data-binary '{
    "colorTag": "green",
    "ratingStars": 5
  }'
```

**Important limitation:** this PATCH path supports `colorTag` and `ratingStars`, but not every other media field. Do not assume it is a full metadata editor.

### Set tags
```bash
curl -sS -X POST "http://localhost:3000/api/projects/:slug/media/:assetId/tags" \
  -H 'Content-Type: application/json' \
  --data-binary '{
    "set": ["location-name", "visual-keyword", "canonical-location"]
  }'
```

The tags endpoint requires one of `set`, `add`, or `remove`.

## Workflow

1. Generate or upload an asset
2. Review and compare variants
3. When the user approves one as canonical:
   - set `colorTag: "green"`
   - optionally set `ratingStars: 5`
   - add descriptive tags including canonical role tags
4. Reference canonical assets in future generations for continuity

### Superseding a canonical asset

When a newer iteration replaces a canonical asset:
1. Set the new asset to `colorTag: "green"`
2. Set the old asset to `colorTag: "yellow"`
3. If supported by the current workflow, record the supersession relationship in metadata

### Review-first discipline

When the user asks to review assets:
1. Review existing assets first
2. Do not generate new variants during the review queue unless asked
3. Skip already-locked green assets unless the user wants to revisit them
4. Skip external references during canonical review unless they are the actual decision object
5. Only generate after the review queue is complete and the next iteration target is clear

## Finding Canonical Assets

Query by colorTag:
```bash
curl -sS "http://localhost:3000/api/projects/:slug/media?colorTag=green"
```

Or filter by tags:
```bash
curl -sS "http://localhost:3000/api/projects/:slug/media?tags=canonical-location"
```

## Generic Example

A canonical environment asset should usually have:
- `colorTag: "green"`
- `ratingStars: 5`
- tags like `["era-label", "location-name", "canonical-location"]`

The exact project-specific tag vocabulary belongs in the project data, not in this reference file.