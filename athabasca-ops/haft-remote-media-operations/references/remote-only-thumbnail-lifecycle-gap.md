# Remote-only thumbnail lifecycle gap

## Symptom

A hosted Haft grid shows broken image tiles for remote-only artifacts. The installed `haft thumbnails audit --path . --repair` command may return zero eligible images and disabled queue state despite a populated artifact catalog.

## Why it happens

The legacy audit reads the file-backed `assets` table. Remote-only images can instead be catalog-only `artifacts` records with `storage_state=remote-only`, canonical `source_url`, source MIME, content hash, and source identity. If no file-backed asset row exists, the normal audit cannot enqueue it. A disabled publish target makes the normal queue unable to publish even if it could see the asset.

## Read-only preflight

1. Verify the exact deployed binary version, active systemd unit, service working directory, vault root, and FFmpeg availability.
2. Inspect the catalog schema/counts: active image artifacts in `artifacts`; `assets`, `asset_thumbnails`, `remote_counterparts`, and `auto_publish_jobs`; plus configured publish-target readiness.
3. Run `haft thumbnails audit --path . --vault <root> --json` as evidence, then compare its eligible count to catalog-only image count.
4. Do not treat a `0 eligible / disabled` response as successful repair evidence.

## Correct repair shape

Use a catalog-aware idempotent backfill: select active remote-only image artifacts; download originals only transiently with bounded size/timeouts; create 96px-max PNGs with FFmpeg; upload to R2/CDN using deterministic keys; verify every public URL and metadata; then persist thumbnail records against the source identity used by the browser grid. Take a catalog backup and validate one canary before deterministic batches.

## Acceptance criteria

- Expected image count = available + explicit failures/pending work.
- No original remote-only image bytes are written into the vault.
- Every available thumbnail URL returns a valid image.
- Browser grid projection resolves thumbnails against the corresponding artifacts.

## the project evidence pattern (2026-07-28)

the project ran Haft 0.1.50 with FFmpeg and a healthy public runtime. Its catalog contained hundreds of artifacts, while `assets`, `asset_thumbnails`, `remote_counterparts`, and auto-publish jobs were empty. The stock audit returned `eligible: 0` and `auto-publish.disabled`: a catalog-vs-file-backed lifecycle mismatch, not a decoder-installation problem.
