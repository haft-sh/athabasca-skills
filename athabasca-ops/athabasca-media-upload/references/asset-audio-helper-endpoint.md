# Asset Audio Helper Endpoint

Use this reference when the same workflow keeps recurring:
- user provides `asset_...`
- Hermes must derive audio from the asset
- Hermes must upload the result back into Athabasca with provenance
- Hermes may need to preserve shot attachment context

## Why this should be code, not repeated shell work

Manual repetition in session showed a stable pattern:
1. `GET /api/media/:assetId`
2. inspect `kind`, `publicUrl`, `phase`, `attachments`, `metadataJson`
3. branch:
   - `video` -> extract audio
   - `audio` -> export / re-encode / trim / normalize
4. upload derivative through project media API
5. if source was shot-attached, explicitly attach derivative to the same shot
6. re-lookup returned asset ID and verify attachment presence before reporting success

That is a strong signal for Tier-3 promotion into a dedicated API capability.

## Recommended endpoint shape

Preferred:
- `POST /api/media/:assetId/derive-audio`

Possible request body:
```json
{
  "mode": "extract|export|normalize|trim",
  "attach": true,
  "target": "match-source",
  "intendedUse": "hume-sts-test",
  "title": "optional explicit title",
  "provenanceNote": "optional explicit note",
  "transform": {
    "startSeconds": 0,
    "endSeconds": 12.5,
    "sampleRate": 24000,
    "channels": 1,
    "format": "wav"
  }
}
```

Minimum response shape:
```json
{
  "ok": true,
  "sourceAsset": { "id": "asset_src..." },
  "asset": { "id": "asset_new...", "publicUrl": "...", "attachments": [] }
}
```

## Behavioral rules

### 1. Source lookup
- Always start from `GET /api/media/:assetId` semantics internally.
- No ad hoc DB lookup in the agent path if the API helper exists.

### 2. Branch by source kind
- If `source.kind === "video"`: extract audio.
- If `source.kind === "audio"`: treat as audio export / re-encode / edit, not video extraction.

### 3. Preserve provenance
Persist at least:
- `derivedFromAssetId`
- `derivedFromUrl`
- `workflow` = `audio-extraction` or `audio-export`
- `intendedUse`

Include when available:
- `sourceShotId`
- `sourceShotNumber`
- `sourcePhase`
- transform/edit metadata

### 4. Preserve attachment context intentionally
- If source has a shot attachment and caller requested `attach: true`, attach derivative to the same shot.
- If source only has project/phase context, carry phase intentionally on upload.
- Do not confuse persistence with attachment.

### 5. Verification is mandatory
Before reporting success, re-lookup the created asset and verify:
- returned asset exists
- `publicUrl` exists
- requested attachment exists when `attach: true`

## Key pitfall to encode in code
A successful upload can still yield an asset with empty `attachments`, especially when no `phase` is passed and no explicit shot-attach step occurs. The helper should prevent false-success reporting here.

## Suggested implementation note
This helper belongs near existing media routes/services, and should reuse the same ffmpeg/temp-dir pattern as other server-side media derivations rather than relying on ad hoc terminal usage.
