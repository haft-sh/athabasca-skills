# In-place video trim / overwrite for an existing media asset

Use when the user asks to remove a beat from an already-attached Athabasca video and explicitly wants to write over the previous video instead of creating a new asset.

## Pattern

1. Resolve the asset with `GET /api/media/:assetId` and capture:
   - `publicUrl`
   - `storageKey`
   - `projectId` / project slug context
   - existing `metadataJson`, `generation`, attachments, title, and provenance
2. Download the current `publicUrl` locally.
3. Trim locally with ffmpeg to the requested end timestamp. For frame-boundary-safe cuts, expect the verified duration to land on the nearest encoded frame boundary rather than exactly matching the decimal timestamp.
4. Verify the local result before upload:
   - `ffprobe` duration and size
   - `sha256sum`
   - optionally inspect/play the tail if the editorial change matters
5. Overwrite the existing R2 object at the same `storageKey`; do **not** create a new media row when the user says to write over the previous video.
6. Update the existing DB media row storage fields with the new file facts:
   - `sizeBytes`
   - `sha256`
   - `originalFilename`
   - `contentType`
   - `updatedAt`
   - preserve `asset.id`, `storageKey`, `publicUrl`, attachments, title, and generation record
7. Merge a concise `metadataJson.trim` object rather than replacing the whole metadata object. Include:
   - requested trim end timestamp
   - removed beat / editorial reason
   - workflow label such as `ffmpeg-trim-overwrite`
   - source asset id
8. Update `provenanceNote` with one sentence describing the in-place trim.
9. Verify remotely before reporting:
   - fetch `GET /api/media/:assetId` and confirm new size/hash/original filename/provenance
   - download or ranged-fetch the public URL and confirm `ffprobe` duration + `sha256sum` match the local output
10. If the user says the overwritten video still appears untrimmed/old-length, check stale CDN/client playback before assuming the wrong asset was uploaded:
   - re-download the exact `publicUrl` with a cache-busting query string such as `?v=verify-<timestamp>`
   - compare `ffprobe` duration, size, and `sha256sum` against the local trimmed file and DB fields
   - inspect response headers for cache hints like `cache-control: max-age=...`
   - give the user a cache-busted URL to test; only create a new media/key if fresh cache-busted playback still shows the old file

## Reporting style

Keep the confirmation terse:

- asset id
- unchanged public URL
- requested trim target
- verified remote duration, size, and sha256
- note that metadata/provenance were updated

## Pitfalls

- `PATCH /api/projects/:slug/media/:assetId` cannot update storage fields; use the repo's R2 helper plus a Drizzle media-row update or a dedicated replace endpoint if one exists for binary media in the future.
- Do not create a new asset when the user explicitly asks to overwrite the previous one.
- Do not claim the exact requested timestamp if ffmpeg lands on the nearest encoded frame boundary; report the verified duration.