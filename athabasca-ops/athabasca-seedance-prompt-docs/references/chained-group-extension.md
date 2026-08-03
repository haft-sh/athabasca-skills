# Chained Seedance Group Extension

Use this when a later Seedance prompt group should continue the previously generated group rather than start independently.

## Normalized dispatch shape

- Persist the previous group first and use its Athabasca `asset.publicUrl`.
- Keep canonical image references in the prompt document's displayed order.
- Submit through `POST /api/projects/:slug/generate/video` with:
  - `mode: "reference-to-video"`
  - `referenceVideoUrls: [previousGroupPublicUrl]`
  - `referenceImageUrls: [ordered canonical image URLs]`
  - a new per-group `idempotencyKey`
- When the user requests only an opening-line change, replace exactly that line and preserve the rest of the published group prompt verbatim.
- Established continuation wording: `I want you to extend video one and generate the following shots.`
- If the continuation is otherwise identical, carry forward provider, model, duration, resolution, aspect ratio, and audio settings.

## BytePlus Seedance 2.0 proven lane

The live capability-backed combination that succeeded for a 15-second continuation was:

```json
{
  "provider": "byteplus",
  "model": "dreamina-seedance-2-0-260128",
  "mode": "reference-to-video",
  "duration": 15,
  "resolution": "480p",
  "aspectRatio": "landscape",
  "generateAudio": true,
  "referenceVideoUrls": ["<previous Athabasca video publicUrl>"],
  "referenceImageUrls": ["<@image1>", "<@image2>", "<@image3>", "<@image4>"]
}
```

Always re-query live capabilities before dispatch; model IDs and constraints are runtime truth.

## Verification

1. Confirm `ok: true` and capture the returned asset ID and Athabasca public URL.
2. Read back `GET /api/media/:assetId` and verify project attachment plus generation provenance.
3. Download the persisted public URL and run `ffprobe` to verify duration and audio stream.
4. Inspect representative frames/contact sheet for requested beat coverage and continuity.
5. Show the persisted clip inline and link the Athabasca URL.

Encoding note: a provider request labeled 480p may produce a stored stream with small padding beyond exactly 480 pixels high (observed 864×496 while normalized generation metadata reported 864×480). Treat it as the 480p delivery class, but quote `ffprobe` dimensions when exact encoded geometry matters.
