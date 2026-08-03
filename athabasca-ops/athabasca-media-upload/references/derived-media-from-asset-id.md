# Derived Media From Existing Athabasca Asset IDs

Use when the user says something like:
- "extract the audio from `asset_...`"
- "trim this attached audio asset and reattach it"
- "convert this project media asset to WAV/MP3"

## Fast path

1. Look up the source asset:

```bash
curl -sS http://localhost:3000/api/media/asset_...
```

2. Read from the JSON:
- `asset.publicUrl`
- `asset.phase`
- `asset.attachments`
- `asset.generation`
- `JSON.parse(asset.metadataJson).projectSlug` when available

3. Derive the project slug before re-upload.
- Prefer `asset.metadataJson.projectSlug` when present.
- If it is missing, resolve the slug from broader project context before uploading.

4. Download the source file and produce the derivative.

Branch by source kind:

### A. Source asset is a video

Audio extraction example:

```bash
curl -L --fail --silent --show-error "$PUBLIC_URL" -o source.mp4
ffmpeg -y -i source.mp4 -vn -ac 1 -ar 24000 -c:a pcm_s16le extracted.wav
ffmpeg -y -i extracted.wav -codec:a libmp3lame -q:a 2 extracted.mp3
```

### B. Source asset is already audio

Do **not** describe this as extracting audio from video. Treat it as an audio export / re-encode / trim / normalize flow:

```bash
curl -L --fail --silent --show-error "$PUBLIC_URL" -o source.wav
ffmpeg -y -i source.wav -ac 1 -ar 24000 -c:a pcm_s16le exported.wav
ffmpeg -y -i exported.wav -codec:a libmp3lame -q:a 2 exported.mp3
```

5. Re-upload the derivative to the project media API:

```bash
curl -sS -X POST http://localhost:3000/api/projects/$PROJECT_SLUG/media \
  -F file=@extracted.wav \
  -F phase="$SOURCE_PHASE" \
  -F category=generated \
  -F sourceKind=generated \
  -F 'title=Extracted audio from asset_...' \
  -F 'provenanceNote=Audio track extracted by Hermes from source asset for external testing.' \
  -F 'metadataJson={"derivedFromAssetId":"asset_...","derivedFromUrl":"...","workflow":"audio-extraction","intendedUse":"hume-sts-test"}'
```

Only pass `phase` when you intentionally want the derivative attached/scoped to that phase context.

If the user explicitly asked to "attach it":
- inspect the source asset's `attachments` first
- if it is attached to a shot, upload the derivative and then attach the new asset to the same shot with:

```bash
curl -sS -X POST http://localhost:3000/api/projects/$PROJECT_SLUG/shots/$SHOT_ID/media \
  -H 'content-type: application/json' \
  -d '{"assetIds":["'$NEW_ASSET_ID'"]}'
```

- if you skip both `phase` and an explicit shot attach step, the upload may persist successfully but still have an empty `attachments` array
- always re-look-up the new asset and verify the requested attachment actually exists before reporting success

6. Verify by looking up the newly returned asset ID:

```bash
curl -sS http://localhost:3000/api/media/$NEW_ASSET_ID
```

## Provenance minimums

For derived uploads, keep these fields in `metadataJson` unless there is a strong reason not to:
- `derivedFromAssetId`
- `derivedFromUrl`
- `workflow`
- `intendedUse`

Useful extras when available:
- `sourceShotId`
- `sourceShotNumber`
- `sourcePhase`
- `transform` or `editWindow`

## Promotion rule

If a session involves repeated requests of the form "extract/derive audio from `asset_...` and attach it back," stop treating that as one-off shell glue. Promote it into a dedicated API helper, ideally:
- `POST /api/media/:assetId/derive-audio`

That helper should own:
- source asset lookup
- source-kind branching (`video` extraction vs `audio` export/edit)
- ffmpeg transform
- re-upload with provenance
- optional shot reattachment
- post-upload verification

See also: `references/asset-audio-helper-endpoint.md`

## Pitfalls

- Do not use ad hoc DB queries if `GET /api/media/:assetId` is available.
- Do not report success before the derivative has been re-looked-up by returned asset ID.
- Prefer WAV for downstream voice / STS testing unless the user specifically asks for MP3 only.
- Preserve project provenance even when the derivative is for external testing.