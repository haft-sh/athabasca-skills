# External Video Import Pattern

When the user generates clips outside Athabasca (e.g., direct Kling 3.0, Runway, or provider UIs) and asks to "attach" them to a project, they typically land in the Hermes video cache.

## Where to find externally generated clips

```
~/.hermes/cache/videos/video_*.mp4
```

These are hash-named MP4 files dropped there by the Telegram/media handling pipeline. They are NOT named attachments.

## Import workflow

For each file, upload via `POST /api/uploads`:

```bash
curl -sS -X POST "http://localhost:3000/api/uploads" \
  -F "file=@~/.hermes/cache/videos/video_HASH.mp4" \
  -F "projectSlug=<slug>" \
  -F "phase=clips" \
  -F "category=generated" \
  -F "sourceKind=generated" \
  -F "title=<descriptive title>" \
  -F "provenanceNote=Generated externally using <provider>, imported into Athabasca"
```

For bulk imports, loop over the newest files:

```bash
find ~/.hermes/cache/videos/ -name "*.mp4" -newer ~/.hermes/audio_cache/audio_HASH.mp3 -type f
```

Use the newest audio cache file as a temporal anchor to avoid re-uploading clips from previous sessions.

## Verification

After upload:
1. Confirm `ok: true` and note the returned `asset.id`
2. Verify `asset.publicUrl` returns HTTP 200
3. Confirm the asset appears in `GET /api/projects/:slug/media`
