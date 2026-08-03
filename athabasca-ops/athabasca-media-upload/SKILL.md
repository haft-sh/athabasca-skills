---
name: athabasca-media-upload
description: Persist Telegram/web/local media and generated text artifacts into Athabasca via media upload APIs, including Telegram-to-project attachment flows and research-report image replacement semantics. Never store local cache paths, tmp markdown paths, or ephemeral URLs as canonical artifacts.
version: 1.3.0
author: Hermes Agent (Athabasca)
metadata:
  hermes:
    tags: [athabasca, r2, cloudflare, media, storage, uploads]
---

# Athabasca Media Upload

## Core Rule

Every image, video, document, or generated text artifact stored in Athabasca must first be persisted through Athabasca's own upload API:
- `POST /api/uploads`
- `POST /api/projects/:slug/media` when the target project slug is known

Do not store:
- local cache paths
- Hermes tmp markdown paths
- Telegram CDN URLs
- data URIs

Only store the returned permanent `asset.publicUrl` from Athabasca.

## Trigger

Use this workflow when:
- the user sent an image in Telegram and wants it persisted into the production pipeline
- the user sent one or more Telegram images and wants them attached to a project artifact, gallery, or research report
- a local file path appears in the message context and the image should become a research image, moodboard item, or durable media artifact
- a web image should be archived into Athabasca-owned storage before being referenced downstream
- the user asks to attach markdown/text/model responses to a project phase, especially research
- Hermes produced local `.md` or `.txt` files that should become durable Athabasca artifacts

This umbrella now absorbs the narrower Telegram-project-image-attachment workflow. The critical replacement-rule for research galleries lives here: `POST /api/projects/:slug/research-report` replaces the report's image references rather than appending to them.

## Reusable Skill Boundary

Keep Athabasca-specific upload, persistence, provenance, and verification rules in this skill. Replace film-project-specific naming examples in the main body with generic placeholders, and move concrete production-specific examples into `references/` so the skill stays class-level instead of becoming a dump of project lore.

## API Contract

`POST /api/uploads` or `POST /api/projects/:slug/media` as `multipart/form-data` with:
- `file` (required)
- `projectSlug` (optional)
- `phase` (optional)
- `category` = `research|moodboard|generated|inbox|misc`
- `sourceKind` = `telegram_upload|web_import|generated|manual|api_upload`
- `title` (optional)
- `provenanceNote` (optional)
- `metadataJson` (optional JSON object string for artifact/workflow context)
- `generation` (optional JSON object string with `provider`, `model`, `prompt`, and optional `parametersJson`)

Response:
```json
{
  "ok": true,
  "asset": {
    "id": "asset_...",
    "projectId": "proj_...",
    "phase": "research",
    "category": "research",
    "sourceKind": "telegram_upload",
    "title": "ACK page 122",
    "originalFilename": "img_xxx.jpg",
    "contentType": "image/jpeg",
    "sizeBytes": 251861,
    "sha256": "...",
    "storageProvider": "r2",
    "storageKey": "bhima/research/img_xxx.jpg",
    "publicUrl": "https://media.wheretoaccess.com/bhima/research/img_xxx.jpg",
    "provenanceNote": "..."
  }
}
```

## Workflow

1. Use the local cached image path for `vision_analyze` if visual understanding is needed.
2. Before upload, confirm you are using the file attached in the current user message, not a stale path from a prior turn.
3. If the user only sends a naming correction like "this is X" without a fresh attachment, do **not** auto-reuse the previous image path for a new upload. Either:
   - treat it as a metadata/title correction for the already-uploaded asset when the referent is clear, or
   - ask for resend/clarification when it is unclear which image they mean.
4. Telegram image-set quirk: when the user refers to multiple attached images collectively but only one image is surfaced directly in the current message, check `~/.hermes/image_cache/` for the other recent image files before asking for clarification. In this environment, that cache often contains the full attached set.
5. If the image should persist in Athabasca state, call `POST /api/uploads` or `POST /api/projects/:slug/media`.
6. Take `asset.publicUrl` from the response.
7. Use that URL in downstream Athabasca APIs (`research-report`, moodboard items, etc.).
8. Optionally mention the created `asset.id` in provenance text for traceability.

## Derived Media From Existing Asset IDs

Use this when the user points at an existing Athabasca asset like `asset_...` and wants a transformed derivative, for example:
- extract audio from a video asset
- trim or normalize an attached audio file
- convert formats while preserving provenance

If the user explicitly asks to trim/edit an existing video and "write over" or "replace" the previous asset, preserve the same `asset.id`, `storageKey`, `publicUrl`, and attachments. Download, ffmpeg-trim, overwrite the same R2 object, update storage fields in the media row, merge trim provenance into `metadataJson`, then verify the remote URL's duration/hash. Full checklist: `references/video-trim-overwrite-existing-asset.md`.

For Telegram-origin clips that are not yet in Athabasca, first look for a local cached source file (in this environment often under `~/.hermes/cache/videos/` for videos), verify the candidate with `ffprobe`, then upload through the normal media API rather than treating the Telegram path as canonical state. When the user says "check your video cache" or otherwise implies the clip was just sent, sort cached videos by modified time, show/choose the newest candidate by default, and include duration + size from `ffprobe`; if multiple recent clips are plausible, ask for confirmation before editing/uploading unless the user says it should be the latest. For simple trim requests against a cached clip, use `ffmpeg` to produce a local derivative, verify the output duration with `ffprobe`, and deliver the local `MEDIA:` file immediately; only attach/upload to Athabasca when the user explicitly asks to attach it to the project or the broader workflow requires persistence.

When the user says to "check your video cache" for a trim/upload task, inspect recent files under `~/.hermes/cache/videos/`, sort by mtime, and run `ffprobe` on likely candidates. If multiple recent clips have the same duration, report the newest candidate and ask for confirmation before editing unless the user already made the target unambiguous. For a requested cut such as `0:00–00:14.038`, use `ffmpeg` to trim/re-encode and verify the output with `ffprobe`; at 24fps, a requested 14.038s cut may probe as about `14.041667s`, which is frame-accurate/effectively correct. If the user supplies the upstream manual-generation prompt after approving the local trim, upload the trimmed clip through `POST /api/projects/:slug/media` with `phase=clips`, store provider/model/prompt in `generation`, include trim/source-cache/duration metadata in `metadataJson`, and verify the remote URL with ranged GET plus remote `ffprobe`.

Default sequence:
1. Inspect the source asset via `GET /api/media/:assetId`.
2. Read the returned `publicUrl`, `phase`, `attachments`, and `generation` metadata.
3. Derive the target project slug from the asset response before upload:
   - prefer `JSON.parse(asset.metadataJson).projectSlug` when present
   - otherwise resolve from broader project context before uploading
4. Download from the returned `publicUrl` and create the derivative locally.
5. Re-upload the derivative through `POST /api/projects/:slug/media`.
6. Branch by source asset kind before deriving:
   - if `asset.kind === "video"`, do a normal audio extraction / transcode flow from the downloaded file
   - if `asset.kind === "audio"`, do **not** describe it as extraction-from-video; treat it as an audio export / re-encode / trim / normalize workflow instead
7. If the user asked to "attach" the derivative, preserve attachability intentionally:
   - inspect `asset.attachments` on the source asset first
   - if the source asset is attached to a shot (`targetType === "shot"`), prefer uploading the derivative and then attaching it to the same shot with `POST /api/projects/:slug/shots/:shotId/media`
   - if you only need project-level attachment and the source has a meaningful phase, pass `phase` on upload so the new asset gets a project attachment in that phase context
   - do **not** assume a successful upload implies an attachment exists; verify `attachments` on the returned / re-looked-up asset
   - important pitfall: a project media upload with no `phase` can persist the asset but still return an empty `attachments` array
8. Record provenance in `metadataJson`, including at minimum:
   - `derivedFromAssetId`
   - `derivedFromUrl`
   - `workflow`
   - `intendedUse`
9. Add a concise `provenanceNote` describing the transformation.
10. Verify the new uploaded asset via API before reporting success, including attachment presence when the user explicitly asked for an attached result.
11. Promotion rule: if this same asset-ID audio derivation flow is being repeated, stop treating it as one-off shell work and prefer a productized helper endpoint. The right Tier-3 shape is a dedicated API path that performs lookup, derivation, upload, optional shot reattachment, and verification in one call.

Important: do not start with ad hoc SQL when the user gives an asset ID. The asset-ID fast path is now the API route `GET /api/media/:assetId`.

## External clip attachment workflow

Use this when the user provides local/Telegram-cached video clips, existing video asset IDs, or a manually generated video URL that already exists outside Athabasca and wants them attached to a specific shot or project context. If the user provides the generation prompt alongside the video, store that prompt as generation/metadata on the media asset; do **not** treat the prompt as an instruction to rewrite a nearby HTML prompt-preview unless he explicitly asks for a doc edit.

If the user says he will provide the prompt in the next message, attach the video immediately as media with `metadataJson.promptStatus="pending-next-message"` and do not edit prompt-preview HTML, markdown, or other documents. Later, when the prompt arrives, update only the existing media asset's generation/metadata unless he explicitly asks for document changes — do not create a second asset or a separate prompt document. Set `metadataJson.promptStatus="provided-by-user"`, add lightweight prompt provenance (`promptSource`, `promptProvidedAt`, and optionally `promptText` when useful), update the generation prompt/parameters on the same asset, and verify with `GET /api/media/:assetId` that the prompt is visible in `asset.generation.prompt`. If there is no API route for editing generation metadata yet, use the smallest safe DB update to `media_generations` plus a media metadata update, then read back through the API before reporting success.

Important prompt-visibility rule:
- Athabasca media UI/search surfaces look at `asset.generation.prompt`, not just `metadataJson.prompt`.
- If a manual/generated video was uploaded before the prompt was available, do **not** consider the follow-up prompt saved until `GET /api/media/:assetId` returns a non-null `generation` object with the full prompt in `generation.prompt`.
- The public `PATCH /api/projects/:slug/media/:assetId` route is metadata-limited and will not create/update `media_generations`, title, or provenance. For follow-up manual-generation prompts, either use a productized API route if one exists, or a small repo-local Drizzle helper that upserts `media_generations` and updates `media_assets` title/provenance/metadata, then verify with `GET /api/media/:assetId`.
- Reusable helper: `scripts/upsert-manual-video-generation.ts` upserts `media_generations.prompt` and updates the media row from env vars plus a prompt file. Use it when a manually uploaded video later receives its provider/prompt and the UI must show the prompt.

Steps:
1. Resolve the project slug and target `shotId` first via `GET /api/projects/:slug/shot-list`.
2. Upload each clip through `POST /api/projects/:slug/media` with `phase=clips`, appropriate title/provenance, and generation metadata when the upstream model/provider is known.
3. Do **not** assume upload-time `metadataJson.shotId` or `shotNumber` will create the shot attachment for you.
4. Explicitly attach the uploaded asset IDs with `POST /api/projects/:slug/shots/:shotId/media`.
5. Verify both layers after attach:
   - asset exists at project level with `phase=clips`
   - shot has `mediaAttachments` containing the asset
   - public URL returns `200`/`206`

Current Athabasca quirk:
- a shot attachment created through `POST /api/projects/:slug/shots/:shotId/media` may come back with attachment `phase: shot_list` even when the asset itself correctly lives in `phase: clips`
- treat `asset.phase` as the canonical location of the clip and the shot attachment row as linkage metadata
- report this mismatch accurately instead of claiming the clip failed to attach

Static-review workflow note:
- for HTML/Markdown review docs used as lightweight project surfaces, a stable canonical URL can be more useful than proliferating timestamped assets
- if the user wants the document URL to stay fixed, prefer the productized helper route `POST /api/projects/:slug/media/:assetId/replace`
- that replace route is for **text/document artifacts only**: HTML, Markdown, JSON, SVG, XML, plain text; do not generalize it to image/video/audio replacement
- if the document is already a project media asset and the user wants the URL to stay fixed, prefer `POST /api/projects/:slug/media/:assetId/replace` rather than direct R2 writes; this preserves DB fields like `sha256`, `sizeBytes`, `contentType`, and `updatedAt` while keeping the same `asset.id`, `storageKey`, and `publicUrl`
- reserve new asset rows / new keys for checkpoints the user actually wants to preserve

Prompt-preview cleanup note:
- for HTML prompt-preview sheets, treat the visible reference/candidate cards and the copy-paste prompt block as one artifact; when adding/removing/renumbering `@imageN` cards, update the `<pre>` prompt text to match in the same pass
- for Seedance prompt previews, do **not** describe external project history or scene labels as context the model should understand (for example, do not say an image comes from another scene); Seedance is stateless and only receives the immediate prompt plus attached `@imageN` references
- phrase image anchors by their role in the current prompt, e.g. `@image2 = Anchor image — Shot 1`, `@image5 = Anchor image — Shot 5`, with no reliance on outside continuity labels
- after replacement, fetch the public URL and verify the target section specifically: expected asset IDs present/absent, reference numbering, candidate count, and prompt-block `@imageN` lines
- reserve new asset rows / new keys for checkpoints the user actually wants to preserve

Reference: `references/text-artifact-replace-route.md`

Reference: `references/derived-media-from-asset-id.md`
In-place trim/overwrite checklist for existing video assets: `references/video-trim-overwrite-existing-asset.md`
Conversation/research transcript artifact recipe: `references/conversation-record-markdown.md`
Design note for promoting repeated manual audio-derivation work into code: `references/asset-audio-helper-endpoint.md`
Text artifact replace-route guidance: `references/text-artifact-replace-route.md`
Storyboard continuity pass persistence checklist: `references/storyboard-continuity-pass-persistence.md`

## Generated storyboard/contact-sheet images from Hermes tools

When a Hermes image-generation tool returns a local image path for an Athabasca project deliverable, treat that path as staging only. Persist it through `POST /api/projects/:slug/media` before reporting it as attached.

If a user later selects one generated asset as the final character/reference anchor, update the existing asset instead of re-uploading it. Use `PATCH /api/projects/:slug/media/:assetId` with a merged `metadataJson` object so prior provenance fields are preserved. Useful keys include `characterAnchorStatus: "final"`, `isFinalCharacterSheet: true`, `finalizedForContinuityPass: true`, `supersedesAlternateAssetIds`, and `decisionNote`. Verify the patch with `GET /api/media/:assetId`.

For shot-specific generated grids or stills, do **not** rely on `metadataJson.shotId` alone. Upload the asset first, then explicitly attach the returned `asset.id` to the shot with `POST /api/projects/:slug/shots/:shotId/media`, and verify the shot's `mediaAttachments` in `GET /api/projects/:slug/shot-list`.

Recommended fields for storyboard grids/contact sheets:
- `phase=storyboard` (or omit `phase` entirely if no phase-scoped filtering is needed)
- `category=generated`
- `sourceKind=generated`
- project-level attachment role such as `storyboard_grid` or `contact_sheet`
- `metadataJson` with source markdown/report asset id, reference asset ids, provider/model, and prompt summary

Verification:
- inspect or vision-check the local image before upload when quality matters
- verify the uploaded asset with `GET /api/media/:assetId`
- confirm `attachments` includes the intended project or shot target
- optionally `curl -I` the returned public URL to confirm R2 availability

## Batch character/reference image uploads from Telegram

Use this when the user sends several Telegram images and asks to attach them as updated project references, especially character sheets or v2 reference images.

Important Telegram behavior for this user/setup:
- when the user refers to multiple attached images collectively but only one image appears inline in the current message, do not immediately ask for resend or clarification
- first inspect `/home/nrsimha/.hermes/image_cache/` for the other recent sibling `.jpg` files from the same send batch
- treat those cache files as staging inputs only, then upload the intended full set through Athabasca APIs

Steps:
1. Treat every Telegram/local image path as staging only; upload each file through `POST /api/projects/:slug/media`.
2. If the user expects identification from the image (for example, a named character or creature), inspect each image before titling. Use known project context when available, but label uncertain identifications conservatively rather than inventing exact names.
3. Put the version in the human-facing `title` when requested, e.g. `Character Reference v2`.
4. Recommended fields for project-level character references:
   - `phase=storyboard` when the reference supports shot/storyboard generation
   - `category=misc`
   - `sourceKind=telegram_upload`
   - `metadataJson.artifactKind="character_reference"`
   - `metadataJson.version="v2"` or the requested version
   - `metadataJson.characterName`, `visualDescription`, `workflow`, and `sourcePath`
   - project attachment `role` such as `character_reference_v2`, `character_reference_alt_v2`, etc.
5. Upload all images in one batch when the project and intent are clear. Do not ask for redundant confirmation just because there are multiple images.
6. Verify each returned `asset.publicUrl` with a HEAD request and report concise title → asset id / URL results.

Pitfall: if the user asks "what do you see?" while also saying the images should be attached, answer the visual identification briefly and still perform the requested attachment workflow unless they explicitly say conversation-only/no-write.

## Direct R2 overwrite path for global static assets

Use this when the artifact should live on R2 **without** creating or updating an Athabasca media DB record, for example:
- shared CSS used by many generated HTML docs
- global JS/helpers for static review pages
- stable-key HTML pages you want to overwrite in place during rapid iteration
- non-project-scoped planning/design markdown such as `docs/plans/...` that the user wants shared by URL only
- any non-project-scoped asset that would be noise in the Media UI

Preferred approach:
1. Use Athabasca's existing R2 helper directly from the repo: `src/server/storage/r2.ts`.
2. Upload to a **stable key** such as `shared/styles/athabasca-docs-v1.css`, `shared/plans/<filename>.md`, or another deliberate non-project path.
3. Re-upload to the same key when you want in-place overwrite behavior.
4. Link generated HTML/docs to that stable public URL.
5. For project docs already attached in Athabasca, if you want to keep the same asset URL, overwrite the existing R2 object at its current `storageKey` instead of creating a new media asset.

Example Bun snippet:
```ts
import { uploadFileToR2 } from "./src/server/storage/r2";

await uploadFileToR2({
  localPath: "/abs/path/to/athabasca-docs-v1.css",
  key: "shared/styles/athabasca-docs-v1.css",
  contentType: "text/css",
});
```

Important distinction:
- `POST /api/projects/:slug/media` => creates a **new DB asset row** and usually a **new timestamped storage key**.
- direct `uploadFileToR2()` / `uploadBytesToR2()` to the **same key** => overwrites the object in place with **no new DB asset**.

Use the direct path when the user explicitly wants stable URLs, in-place updates, or global non-project assets invisible to the Media UI.

Common non-project document pattern:
- for shareable planning/review markdown that should **not** be attached to any Athabasca project, upload directly to a stable key such as `shared/plans/<filename>.md`
- after upload, verify the **public URL body** with a real `GET` (or ranged `GET` plus targeted content check), not just local file existence
- when overwriting an existing key, confirm the remote body contains the newly-added sections/phrasing before reporting success
- this is the right path for docs that live in `docs/plans/` and are meant to be shared by URL without creating Media UI noise

For **project-attached text/document artifacts** that already exist as Athabasca media, prefer the dedicated replace route instead of raw R2 overwrite:

- globally shared review docs or notes that should have a permanent URL
- any text artifact the user explicitly says does **not** need project association

For these non-project text artifacts:
1. upload with `uploadFileToR2()` directly, not `POST /api/projects/:slug/media`
2. choose a deliberate stable key under a shared prefix such as `shared/plans/`
3. when the document is revised, re-upload to the **same key** so the link stays constant
Use the direct path when the user explicitly wants stable URLs, in-place updates, or global non-project assets invisible to the Media UI.

Non-project planning/docs rule:
- for markdown planning docs under repo paths like `docs/plans/...` that the user wants shareable but **not** associated with any Athabasca project, upload directly to a deliberate stable non-project key such as `shared/plans/<filename>.md`
- when revising the same document, overwrite the same key so the share link stays fixed
- after upload, verify by fetching the public URL and confirming expected content markers from the document body, not just the upload return payload

For **project-attached text/document artifacts** that already exist as Athabasca media, prefer the dedicated replace route instead of raw R2 overwrite:
- `POST /api/projects/:slug/media/:assetId/replace`
- accepts exactly one of `file` or `sourceUrl`
- preserves `asset.id`, attachments, `storageKey`, and `publicUrl`
- refreshes DB content fields such as `sha256`, `sizeBytes`, `contentType`, `originalFilename`, and `updatedAt`
- rejects non-document assets; use it for HTML, Markdown, JSON, SVG, XML, and plain text artifacts

Reference: `references/text-artifact-replace-route.md`
Reference: `references/non-project-markdown-r2-upload.md`

## Text Artifact Workflow

Use this for requests like:
- "attach the responses we received as markdown files to the research phase"
- "store these model comparison outputs with the project"
- "persist this Hermes-generated `.md` file as research context"
- "record our conversation to an Md file and store it in R2"
- "write these prompts as a `.md`, attach it, and share the link"

Steps:
1. Resolve the project slug.
2. Identify or create each local `.md` or `.txt` file to attach.
   - For conversation records, synthesize a concise research/development record rather than dumping irrelevant raw tool logs. Include project context, key Q&A, source-backed claims, caveats, and useful script decisions.
   - See `references/conversation-record-markdown.md` for the recommended shape and upload fields.
3. Upload each file with `POST /api/projects/:slug/media`.
   - In normal agent code, prefer the project media API/tool path.
   - If raw terminal HTTP calls to Athabasca are blocked or multipart tooling is unavailable, run a small Bun script that imports `createMediaAssetFromUpload` from `src/server/db/media`, constructs a `File` with an explicit UTF-8 content type, and passes `projectSlug`, optional `phase` tag, `category`, `sourceKind`, `title`, `provenanceNote`, `metadataJson`, and optional project attachment metadata. This preserves DB + R2 consistency without direct DB row edits.
4. For research support artifacts, set `phase=research`, `category=research`, and `sourceKind=generated` when model-created. For visual-development prompt packs or style boards, use `phase=visual_dev` plus a descriptive `metadataJson.artifactKind` such as `midjourney_prompt_set_markdown`.
5. Add a concise `title` and `provenanceNote`.
6. Put structured workflow context in `metadataJson`, not in `provenanceNote`.
7. Put model run details in `generation` when provider/model/prompt are known.
8. Verify with `GET /api/projects/:slug/media?phase=research` / `?phase=visual_dev` or `GET /api/media/:assetId`.
9. For public R2 URL verification of text artifacts, prefer a ranged `GET` that reads the first bytes. Do not treat a `HEAD` 403 as failure if `GET`/ranged `GET` returns the expected object; some public object configurations allow reads but reject HEAD.

Example:
```bash
curl -sS -X POST http://localhost:3000/api/projects/womb-rental/media \
  -F file=@/tmp/womb-rental-claude-response.md \
  -F phase=research \
  -F category=research \
  -F sourceKind=generated \
  -F 'title=Womb Rental research comparison - Claude response' \
  -F 'provenanceNote=Generated by Hermes during multi-model comparison and attached to the research phase.' \
  -F 'metadataJson={"workflow":"multi-model-text-comparison","artifactType":"model_response_markdown","contextLabel":"research comparison","sourcePath":"/tmp/womb-rental-claude-response.md"}' \
  -F 'generation={"provider":"openrouter","model":"anthropic/claude-sonnet-4","prompt":"<prompt here>","parametersJson":"{\"workflow\":\"multi-model-text-comparison\"}"}'
```

## Pitfalls

- **PATCH /api/projects/:slug/media/:assetId is metadata-limited.** The live PATCH route updates `metadataJson` only, unless `ratingStars` or `colorTag` is supplied, in which case it updates rating/color and returns early. It does **not** update `title`, `provenanceNote`, `sourceKind`, storage fields, tags, or `media_generations`. Set title/provenance/source/generation fields correctly at upload time when possible. To update tags, use the separate `POST /api/projects/:slug/media/:assetId/tags` endpoint with `{ "set": [...] }`, `{ "add": [...] }`, or `{ "remove": [...] }`. If the visible prompt is missing after a delayed manual-generation prompt update, check `generation.prompt` specifically; storing the text only in `metadataJson.prompt` is insufficient for UI visibility.
- Storage-related fields (`storageKey`, `publicUrl`, `contentType`, `sizeBytes`, `sha256`, `kind`, `originalFilename`, `storageProvider`) are immutable via the public PATCH route. To repair a broken image asset (e.g. 0-byte file, wrong content-type, 404'ing R2 object), use direct R2 overwrite + Drizzle DB update. See `scripts/repair-broken-asset.ts` for a reusable script that:
  1. Uploads the replacement image to both `storageKey` and the key extracted from `publicUrl`
  2. Updates DB fields (`contentType`, `sizeBytes`, `sha256`, `originalFilename`, `kind`) via Drizzle
  3. Verifies the repair
  Run: `ASSET_ID=asset_xxx IMAGE_PATH=/path/to/image.png bun run scripts/repair-broken-asset.ts` from the athabasca repo root.

- Text artifacts like `.md`, `.txt`, `.json`, `.xml`, `.svg`, and other UTF-8-readable payloads must be uploaded with a UTF-8 charset in the stored object content type. In Athabasca this now means the persisted object should carry a header like `text/markdown; charset=utf-8`, not bare `text/markdown`, otherwise some viewers will misdecode Unicode punctuation into mojibake such as `â€”`.
- `category=reference` is NOT a valid enum value. The valid options are: `research|moodboard|generated|inbox|misc`. Use `misc` for reference images that don't fit the other categories.
- The `phase` upload field is optional organizational metadata and should be treated as a media tag, not as a DB column or workflow gate. Omit it if unsure; use `category` for media type such as `generated`, `moodboard`, or `research`.
- Do not combine multiple model responses into one research report just to persist them. The research report is the synthesis; generated markdown/text files are supporting media artifacts.
- Current multipart quirk for `POST /api/projects/:slug/media`: `generation` is validated as an **object**, but nested fields like `parametersJson` must be **JSON strings** (not nested objects). If you get `expected string, received object` on `parametersJson`, stringify it: `"parametersJson":"{\"key\":\"value\"}"`. Alternatively, skip `generation` entirely and put provider/model/prompt provenance in `metadataJson`.
- For remote image attachment via `sourceUrl`, it is acceptable to attach the asset successfully with strong provenance in `metadataJson` even when the endpoint shape does not accept a multipart `generation` string field.
- **Midjourney grid assets need `mjButtons` stored at upload time.** When uploading a Midjourney grid, extract all button `custom_id` values from the grid message and store in `metadataJson.mjButtons` immediately. Without them, future upscale/variation actions require re-querying Discord — and the grid message may have aged out of the `?limit=25` window. Store `discordMessageId`, `discordChannelId`, and `mjJobId` alongside `mjButtons` for a complete self-contained action record. See `athabasca-midjourney-prompting` for extraction code and interaction format.

## Current Storage Configuration

Athabasca uses Cloudflare R2.
Configured env vars:
- `R2_ACCOUNT_ID`
- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`
- `R2_BUCKET_NAME`
- `R2_PUBLIC_URL`

Check status via:
- `GET /api/health` → `r2.configured`

## Image Generation Provider Reference

When generating images via `POST /api/projects/:slug/generate/image`, the valid provider/model combinations are:

| Provider Label | `provider` value | `model` value | Notes |
|---|---|---|---|
| Midjourney V8.1 | `midjourney` | `midjourney-v8.1` | Best for mood/atmosphere. Rate-limited by Discord. |
| Gemini (Nano Banana 2) | `google-gemini` | `gemini-3.1-flash-image-preview` | Best for complex spatial compositions. Reliable. |
| GPT Image 2 | `openai-codex` | `gpt-image-2` | Complex compositions. ~50% reliability (returns empty results). |

**Do NOT use** `provider: "openai"` or `model: "gpt-image-1"` — these are rejected by the API validation.

For provider routing guidance (which model for which shot type), see `athabasca-midjourney-prompting` skill.

## Discord Rate Limiting for Parallel MJ Generations

When firing multiple Midjourney generations in parallel (3+), Discord returns 429 errors on `/interactions`. Mitigation:

- Add `sleep 3-8` before each parallel curl call to stagger submissions
- The Athabasca MJ provider already handles single-call 429 retries, but parallel bursts exceed the per-second limit
- For batch visual dev (6+ prompts), prefer staggered sequential submission or mix providers (some MJ, some Gemini)

## Key Convention

Objects are stored inside the `athabasca` bucket under keys like:
- `bhima/research/...`
- `inbox/inbox/...`
- `womb-rental/research/...`

## Example Decision Rule

If the user says something like:
- "add this image to the research section"
- "persist this Telegram upload"
- "put this into the moodboard"

Then do:
1. upload through `/api/uploads`
2. use returned `publicUrl`
3. write/update the relevant Athabasca record

Never assume the local file path itself is durable.

## Related Skills

For generated or transformed audio workflows, especially speech-to-speech voice changing from an existing `asset_...`, use:
- `athabasca-audio-generation`

Relationship between the skills:
- `athabasca-media-upload` = persistence primitive plus Telegram attachment/report-update workflow, source-asset lookup, and derivation conventions
- `athabasca-audio-generation` = normalized generation workflow for provider-backed audio outputs that should end by persisting generated audio through the media primitives here
