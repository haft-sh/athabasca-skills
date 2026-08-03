---
name: athabasca-media-manifest-and-downloader
description: Export newline-delimited Athabasca media URLs for external downloaders or editing machines, validate extensionless video URLs, and provide a downloader/handoff contract without sharing R2 credentials.
version: 1.1.0
author: Hermes Agent
metadata:
  hermes:
    tags: [athabasca, media, manifest, urls, downloader, editing, r2, gist]
---

# Athabasca Media Manifest and Downloader

## Purpose

Use this when a user wants to move generated Athabasca clips or other project media to another machine without copying Cloudflare R2 credentials.

Typical use cases:
- export project clip URLs for DaVinci Resolve or other NLE ingest
- feed a newline-delimited manifest into a Bun, Python, or shell downloader
- transfer the manifest file directly or host it at a plain-text URL such as a gist

## Why this path is preferred

A public media URL like:
- `https://media.wheretoaccess.com/<project-slug>/`

is usually not enough to enumerate objects. The Athabasca media API is the canonical source for project media URLs.

Benefits:
- no R2 credentials need to move between machines
- uses Athabasca's asset registry instead of bucket guessing
- works even when public bucket listing is unavailable
- gives a deterministic manifest for downstream ingest workflows

## Core procedure

1. Verify Athabasca is running.
   - `GET /api/health`
   - example: `curl -sS http://localhost:3000/api/health`

2. Fetch project media.
   - `GET /api/projects/:slug/media`
   - example: `curl -sS http://localhost:3000/api/projects/<slug>/media`

3. Filter the assets.
   - usually `kind == "video"`
   - require non-empty `publicUrl`
   - if the user wants all media, widen the filter intentionally rather than by accident

4. Sort deterministically.
   - usually `createdAt` ascending for timeline-friendly ingest order
   - state the sort order explicitly if it matters to the user

5. Validate edge cases.
   - if a selected `publicUrl` path has no file extension, send a `HEAD` request
   - keep it if the response is `200` and `content-type` is `video/*`

6. Write the manifest.
   - plain text only
   - one URL per line
   - no bullets or commentary in the file
   - usually save as `.txt`

## jq extraction pattern

```bash
curl -sS http://localhost:3000/api/projects/<slug>/media \
  | jq -r '.assets
    | map(select(.kind == "video" and .publicUrl != null and .publicUrl != ""))
    | sort_by(.createdAt)
    | .[]
    | .publicUrl'
```

## Validation pattern for extensionless URLs

```bash
curl -I -sS "<publicUrl>"
```

Keep the URL if the response is `200` and `content-type` is `video/mp4` or another `video/*` type.

## Manifest output contract

The exported manifest should be:
- plain text
- newline-delimited
- one URL per line
- safe to transfer directly to another machine
- free of markdown bullets or explanatory text

## Persisting the manifest back into Athabasca

If the user wants the manifest itself uploaded and attached to the project, persist it as a text/document artifact through Athabasca rather than handing around only a local tmp path.

Recommended upload shape:
- `POST /api/projects/:slug/media`
- multipart `file=@<manifest>.txt`
- `phase=clips` when the manifest is for editing/download of generated clips
- `category=generated`
- `sourceKind=generated`
- concise `title`, for example `Prenup generated video URL manifest`
- `provenanceNote` explaining that it is a newline-delimited public-URL manifest for external download/editing
- `metadataJson` including at least:
  - `workflow=athabasca-media-manifest-and-downloader`
  - `artifactKind=video_url_manifest`
  - `projectSlug`
  - `lineCount`
  - `sortOrder`
  - `sourcePath`

Verification after upload:
1. inspect the returned `asset.id`, `publicUrl`, and `attachments`
2. confirm the asset is attached at project level, usually `targetType=project`
3. verify the uploaded text is readable from the returned public URL with a small ranged `GET`
4. if needed, re-read via `GET /api/media/:assetId` as the canonical confirmation

The downstream consumer should accept all of these input forms:
- local file path
- `file://` URL
- absolute `http://` or `https://` URL pointing to a plain-text manifest

## Downloader contract

If you also write the downloader, make it support:
- local manifest paths
- `file://...` manifest URLs
- `http://...` or `https://...` manifest URLs
- ignoring blank lines and comment lines beginning with `#`
- skipping files that already exist and are non-empty
- preserving ordering with zero-padded numeric prefixes
- deriving a filename from the source URL path
- inferring an extension such as `.mp4` when the URL path has no extension but `HEAD` reports `video/mp4`

## Suggested downloader behavior

- read the manifest from local disk or fetch it remotely
- split on newlines and ignore blank/comment lines
- `HEAD` media URLs when extension inference is needed
- save files with deterministic numeric prefixes so import order remains stable
- default `video/mp4` to `.mp4` when the URL lacks an extension
- skip any destination file whose size is already greater than zero

## Optional gist sharing

If the user wants the manifest uploaded as a GitHub gist:

```bash
gh gist create <manifest-file> --desc "<description>"
```

Important caveat:
- `gh gist create` requires a token with the `gist` scope
- GitHub may return `HTTP 404` for `https://api.github.com/gists` when the token lacks `gist`; treat that as an auth/scope problem, not a missing endpoint

Useful checks/fix:

```bash
gh auth status
gh auth refresh -h github.com -s gist
```

This flow may require interactive browser/device auth on the machine where `gh` is running.

## Pitfalls

- Do not assume a bare public media domain can list bucket contents.
- Do not drop valid video assets just because the URL path lacks `.mp4`.
- Prefer Athabasca API results over guessing from bucket prefixes.
- Do not hand the editing machine R2 credentials unless the user explicitly wants that.
- State the chosen sort order explicitly if the user cares about timeline ingest order.
- Treat gist `404` responses cautiously; they may indicate missing token scope rather than a broken API.

## Verification

Before finishing, confirm:
- project slug used
- total assets returned by the API
- number of exported URLs
- whether any kept URLs were extensionless and how they were validated
- chosen sort order
- manifest output path
- if applicable, where the downloader script was written
- if applicable, hosted manifest URL
