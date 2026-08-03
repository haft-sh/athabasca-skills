---
name: athabasca-media-attachment-finder
description: Find all media attachments associated with an Athabasca project by checking the schema first, then using the project media API and the related reference tables.
version: 1.3.0
author: Hermes Agent (Athabasca)
metadata:
  hermes:
    tags: [athabasca, media, attachments, db, api, research, moodboard]
---

# Athabasca Media Attachment Finder

## Purpose

Use this skill when you need to answer a question like:
- "What media assets are associated with this project?"
- "Find all attachments for this project"
- "Show me the project's images, references, and uploaded media"
- "Does this generated image have a stored prompt?"
- "Why does the UI show the image card but not the generation prompt?"

This skill is for discovery only. It does not upload or mutate project state.

## Source of Truth Order

Follow the Athabasca precedence rules:
1. `src/server/db/schema.ts`
2. Route handlers in `src/server/api/routes/`
3. API responses from the running app
4. Direct DB inspection as a fallback for verification

Do not guess the data model. Read `src/server/db/schema.ts` first.

## What Counts As "Associated Media"

For an Athabasca project, media can show up in more than one place:
- `media_assets`: durable uploaded assets linked by `project_id` and optionally a `phase`
- `media_attachments`: phase and target linkage for generic assets
- `media_generations`: generation metadata for created assets
- `research_reports`: report metadata; report-linked media is attached through `media_attachments`
- `visual_directions`: direction records that can own attached media assets
- **reference prerequisites**: canonical character sheets, canonical prop sheets, and recurring location references that downstream generations depend on

If the user asks for "media assets" specifically, start with `GET /api/projects/:slug/media` and optionally filter by `phase`.
If the user asks for "all attachments" or "all associated media", include `media_assets` first, then inspect `attachments` and `generation` on the API response.

### Reference-asset rule (mandatory)

If the user asks for a list of **reference assets**, **canonical references**, or assets needed before generation/review, do **not** just dump whatever media exists.

You must explicitly check for:
1. character sheets for each recurring main character / creature
2. canonical hero props that recur across shots
3. canonical locations/environments used as reference anchors

For character sheets, look for titles/tags like `character sheet`, `character reference`, `turnaround`, `canonical-reference`, `character-sheet`, or equivalent role metadata. If none exists for a recurring character, say so clearly and treat it as a **missing prerequisite**, not as an optional nice-to-have.

If the user gives a specific media asset ID like `asset_...`, do **not** start with ad hoc SQL. First call:
- `GET /api/media/:assetId`

That route is the default lookup primitive for ID-driven media requests. It returns the full enriched media asset payload, including:
- top-level asset fields (`id`, `projectId`, `phase`, `kind`, `category`, `title`, `originalFilename`, `contentType`, `publicUrl`, etc.)
- `attachments`
- `generation`

Only fall back to schema inspection or direct DB access if:
- the route is missing or failing
- you need fields not returned by the route
- you need broader project context beyond the single asset

## Procedure

### Fast path: user supplies a project name/title

If the user names a project in natural language (for example “Fallback Model”) instead of giving a slug, do not guess. Call `GET /api/projects` first, find the closest project by `name` or `slug`, and use the returned canonical `slug` for all project-scoped requests.

### Fast path: user asks for an existing project document / HTML artifact

If the user asks for a shot breakdown, Seedance prompt preview, asset inventory, research/report markdown, or any existing project document, start with:

1. `GET /api/projects` if the slug is unknown.
2. `GET /api/projects/:slug/media` once the slug is known.
3. Filter media by title, tags, content type, `kind`, `phase`, `category`, `sourceKind`, `createdAt`, and metadata.
4. For uploaded HTML/markdown/document assets, use the asset’s `publicUrl` as the document location.
5. Only inspect source code/routes or direct DB state if the media API cannot answer the lookup or appears broken.

Athabasca often stores working film materials as public ad-hoc HTML files uploaded to R2 and attached as project media. The React app is a review surface; it does not expose dedicated phase routes for every shot breakdown, prompt preview, or asset inventory.

### Fast path: user supplies `asset_...`

1. Call `GET /api/media/:assetId` first.
2. Use that response as the canonical lookup result.
3. Read `asset.projectId`, `asset.phase`, `asset.attachments`, and `asset.generation` from the API response.
4. Only if the user then asks for related project-wide context, follow up with `GET /api/projects/:slug/media` or DB-backed inspection.
5. If the user asks to derive/export audio from the asset and reattach it to the same project, prefer:
   - `POST /api/media/:assetId/derive-audio`
   - Optional body fields: `intendedUse`, `title`, `provenanceNote`, `metadataJson`
   - This normalizes the derived output to mono 24kHz PCM WAV, creates a local MP3 convenience derivative during processing, and reattaches the WAV to the same project while preserving attachment context when possible.

### General project discovery path

1. Identify the project.
   - Resolve the project slug and confirm the project exists.
   - If needed, query `projects` by slug or name.

2. Read the schema first.
   - Open `src/server/db/schema.ts`.
   - Confirm which tables exist and which columns identify the project.
   - Pay special attention to:
     - `media_assets.projectId`
     - `media_attachments.assetId`
     - `media_generations.assetId`
     - `research_reports.projectId`
     - `visual_directions.projectId`

3. Prefer the API for direct media assets.
   - Use `GET /api/projects/:slug/media`.
   - Add `?phase=<phaseKey>` when the user wants a specific phase, such as `visual_dev`.
   - This returns the canonical `media_assets` rows for the project.
   - Each row also includes `attachments` and `generation` for relationship and generation metadata.
   - Important: for generated assets, `generation.prompt` is returned by the API and can be used to answer prompt-recovery questions.
   - If the project does not exist, the route returns `404`.

4. If you need report context, inspect the research report and its attached media.
   - Query `research_reports` for the same `project_id`.
   - Then query `media_attachments` where `target_type = 'research_report'` and `target_id = report_id`.

5. If you need direction context, inspect `visual_directions` and any attached media.
   - Query `visual_directions` for the same `project_id`.
   - Then query `media_attachments` where `target_type = 'visual_direction'`.

6. If you need a direct DB fallback, use the local DB.
   - Default local database: `data/athabasca.db`
   - Query `projects` first to get the project id.
   - Then query the related tables by `project_id`.

7. Present the result grouped by table.
   - `media_assets`
   - `media_attachments`
   - `media_generations`
   - `research_reports`
   - `visual_directions`
   - Mention when a group is empty.

## API Response Shape (important)

`GET /api/projects/:slug/media` returns `{ ok: true, assets: [...] }` — **not** a bare array. Always access `data.assets`, not `data` directly.

Key fields on each asset object:

| Field | Notes |
|---|---|
| `id` | `asset_...` prefix |
| `title` | Human-readable name |
| `kind` | `image`, `video`, `audio`, `document`, `other` |
| `category` | `generated`, `moodboard`, etc. |
| `sourceKind` | `generated`, `web_import`, `upload` |
| `colorTag` | **Not `color`!** Values: `green` (approved), `yellow` (older/superseded), `red`, `blue`, `purple`, `null` (unreviewed) |
| `ratingStars` | 0–5 integer |
| `tags` | Array of tag objects with `.name` |
| `publicUrl` | R2-backed canonical URL |

When querying via `browser_console`, wrap in an async IIFE: `(async () => { ... })()`.

## Practical Query Pattern

Use this order when inspecting a project named `project-slug`:

1. Find the project row:
   - `select id, slug, name from projects where lower(slug) = 'project-slug' or lower(name) = 'Project Name'`

2. Fetch direct assets:
   - `select * from media_assets where project_id = ? order by created_at desc`

3. Fetch attachments for those assets:
   - `select * from media_attachments where asset_id in (...) order by created_at desc`

4. Fetch generation metadata for those assets:
   - `select * from media_generations where asset_id in (...)`

5. Fetch research reports:
   - `select * from research_reports where project_id = ? order by created_at desc`

6. Fetch visual directions:
   - `select * from visual_directions where project_id = ? order by created_at desc`

## Verification

When you finish, confirm:
- for ID-based lookups, the exact `assetId` you used and whether `GET /api/media/:assetId` succeeded
- for project-wide lookups, the project slug or id you used
- the number of rows found in each table
- the final URLs or identifiers for each attachment
- for generated assets, whether `generation.prompt` exists and whether the UI currently renders it
- for reference-asset requests, which required character sheets / prop references / location references already exist, and which are missing prerequisites

## Operational Preference

For this user and codebase, ID-driven media inspection should be **API-first, not DB-first**.

If the user says something like:
- `extract the audio from asset_...`
- `attach asset_... to the project`
- `what is asset_...`

Then the default sequence is:
1. `GET /api/media/:assetId`
2. inspect returned `projectId`, `phase`, `publicUrl`, `attachments`, `generation`
3. if the requested action is audio derivation/export, call `POST /api/media/:assetId/derive-audio`
4. otherwise perform the requested follow-on action
5. only touch the DB directly if the API response is insufficient or broken

If the user asked for a concise answer, return only the grouped list and counts.

## UI Prompt Visibility Check

If the question is specifically about a missing prompt in the UI, use this sequence:
1. Confirm the backend path returns rich media entries:
   - `GET /api/projects/:slug/media[?phase=...]`
2. Find the target asset by `publicUrl`, `storageKey`, or title.
3. Check whether the asset has a `generation` object and whether `generation.prompt` is populated.
4. If the prompt exists in the API response, inspect the frontend card component and the fetch typing.
5. Distinguish clearly between:
   - data missing from storage
   - data present in API but omitted in rendering

In the current Athabasca implementation, project media responses include `generation.prompt`, and the common failure mode is UI omission rather than missing stored data.

## Pitfalls

- **Never invent API routes.** Before writing an endpoint into a skill — whether it is a lookup path, a mutation, or a parameter — verify it against `src/server/api/routes/` and `src/server/db/schema.ts`. Hypothesizing a route from table names and then hardcoding it in a skill is a reproducible error pattern; it survives across sessions and propagates to every future agent that reads the skill. If a route is not in the route handler file, it does not exist.
- Do not use ad hoc shell glue (`curl` + `ffmpeg`, `/tmp` staging) for audio extraction or media transformation when a Tier-3 Athabasca API endpoint exists. `POST /api/media/:assetId/derive-audio` is the canonical path for audio extraction: it normalizes to mono 24kHz WAV, creates an MP3 convenience copy, persists to R2, and attaches the result to the project with provenance. Shell-the project bypasses all of that.
- Do not assume a project has media just because it has a research report.
- Do not claim a table supports a field unless `schema.ts` shows it.
- Do not conclude the prompt is missing just because the card UI omits it; verify the API payload and `generation` row first.

## Related Skills
Related skills:
- `athabasca-media-upload`
