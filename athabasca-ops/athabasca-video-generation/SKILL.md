---
name: athabasca-video-generation
description: Generate Athabasca videos through the normalized project API, using live capabilities and code-backed provider constraints instead of ad hoc provider/model scripts.
version: 1.2.0
---

# Athabasca Video Generation

Use this when the user asks to generate, compare, or debug Athabasca video clips from shot prompts, source stills, or text/image-to-video requests.

This skill is intentionally provider-agnostic. Do **not** create or rely on separate skills for each provider/model permutation. Provider constraints and idiosyncrasies should be encoded in Athabasca code, validation, capability metadata, and tests wherever possible.

## Principle

Prefer the Athabasca abstraction over direct provider calls.

The normal path is:
1. query live video capabilities
2. select a supported provider/model from the returned capability list
3. submit generation through the normalized Athabasca API
4. let server-side adapters map normalized inputs to provider payloads
5. persist generated media and provenance through Athabasca
6. attach the resulting asset to the shot/project as appropriate
7. verify the public media URL and show the result inline

Direct provider calls are a temporary discovery/debug fallback only. If a provider/model becomes recurring, add or fix the Athabasca code path rather than codifying an agent-side script. If the normalized route is blocked but the user needs the approved clip now, a direct BytePlus Seedance fallback is acceptable only when the result is immediately downloaded, uploaded back into Athabasca as generated media, and verified; see `references/byteplus-direct-fallback-ingest.md`.

## Adding a new video generation provider

When the user asks to configure a new provider (e.g. Replicate), follow this exact file sequence:

1. **`/home/nrsimha/.config/athabasca/athabasca-dev.env`** — add the API key here (the systemd service's `EnvironmentFile`, NOT the checkout's `.env`)
2. **`src/shared/generation-config.ts`** — single file that defines:
   - `generationProviders[]` — add new provider string
   - `generationProviderLabels` — add label
   - `imageToVideoProviders[]` / `textToVideoProviders[]` — include new provider for relevant modes
   - `imageToVideoModelOptions["provider"]` / `textToVideoModelOptions["provider"]` — add model entries
3. **`src/server/workers/<provider>-video-worker.ts`** — new file implementing `generateProviderImageToVideo` and `generateProviderTextToVideo`. Pattern: `alibaba-video-worker.ts` for reference.
   - Replicate pattern: `POST /v1/predictions` → poll `GET /v1/predictions/:id` until `status: "succeeded"`. Same model ID for t2v and i2v; i2v adds `input.image` URL field.
4. **`src/server/workers/video-generation.ts`** — register adapter in `videoProviderAdapters` object:
   ```ts
   const videoProviderAdapters = {
     // ... existing ...
     "replicate": {
       imageToVideo: generateReplicateImageToVideo,
       textToVideo: generateReplicateTextToVideo,
     },
   };
   ```
5. Restart Athabasca service, verify via `GET /api/generation/video-capabilities`

Implementation plan reference: `docs/plans/replicate-provider-setup.md`

## Source of truth order

1. Schema, route validators, server-side provider adapters, and worker code
2. `GET /api/generation/video-capabilities`
3. OpenAPI docs: `GET /api/openapi/json`
4. API route definitions under `src/server/api/routes/`
5. Phase playbooks and docs
6. Skills and historical notes

If a skill or note conflicts with live capabilities or code, trust the code and update/delete the stale skill.

## Required workflow

### 0) Pre-generation prompt preview requests

When the user asks to “share the link with its prompt preview,” “review together before sending,” or otherwise wants prompts prepared before dispatching a paid video generation, do **not** submit `POST /generate/video` yet.

Instead:
1. Resolve the project/scene scope and search existing project media for matching prompt-preview artifacts before creating a duplicate.
2. If a matching preview already exists, share its Athabasca project/artifact link and title.
3. If no matching preview exists, build a durable Athabasca prompt-preview artifact with scope assumptions, proposed settings, clip-by-clip prompts, and review questions.
4. Explicitly state that nothing has been sent to the provider.
5. Only proceed to generation after the user approves or edits the preview.

Detailed pattern and a current report-backed implementation note are in `references/pre-generation-prompt-preview.md`.
Scene-specific artifact lookup for requests like “Act 2 Scene 2 prompt preview” is in `references/scene-prompt-preview-artifact-lookup.md`.

### 1) Health and capabilities

```bash
curl -sS http://localhost:3000/api/health
curl -sS http://localhost:3000/api/generation/video-capabilities
```

Use returned provider/model IDs, supported modes, durations, resolutions, aspect ratios, audio support, and exposed constraints.

Do not infer valid settings from memory when the capabilities API can answer it.

### 2) Use lowest-cost defaults unless the user asks otherwise

the user generally prefers lowest-res / cheapest practical video generations while iterating.

Default behavior:
- choose the lowest supported resolution for the selected model
- choose the shortest useful duration that satisfies the request
- enable audio only when requested or materially relevant
- preserve aspect ratio/framing intent from the shot or source still

If live capabilities expose defaults or allowed values, use those rather than hardcoded assumptions.

**Seedance 2.0 routing and defaults** (user preference, applies when using Seedance specifically):
- Provider routing is cost-sensitive: **prefer BytePlus first, Replicate second**.
- **Do not use fal.ai for Seedance 2.0 generations unless the user explicitly asks for fal.ai, or BytePlus/Replicate are verified unavailable/blocked and you disclose the fallback before or with the result.** fal.ai is the expensive fallback, not the default.
- If a project default still says `imageToVideoProvider: "fal-ai"` for Seedance, override it with BytePlus/Replicate unless the user explicitly requests project defaults.
- `resolution: "480p"` — most affordable, always default to this
- `generateAudio: true` — keep audio on by default for dialogue, foley, ambience, and sound effects
- Append `"No Music"` to the end of every Seedance prompt — music interferes with editing. This does **not** mean disabling audio; only set `generateAudio: false` when the user explicitly asks for silent/mute output.
- Append quality suffix before "No Music": `4K, Ultra HD, Rich details, Sharp clarity, Cinematic texture, Natural colors, Stable picture No Music`
- Use short granular takes (4–8s) instead of 15s multi-beat prompts — Seedance struggles with long prompts chaining multiple cuts
- When regenerating a still whose prior motion felt too slow or static, relax any low-frame-rate / strobing constraint instead of preserving it by habit. Replace vague motion language with an explicit beat-by-beat action sequence (for example: foreground subject pauses for a beat, then takes off and follows the background subject) so the model has choreography, not just mood.
- If the user asks for `3s` Seedance I2V, live providers may reject it despite capabilities. Replicate and BytePlus both rejected 3s on 2026-06-05; use the nearest valid `4s` setting, disclose the deviation, and patch/verify capabilities later rather than silently failing.
- Use "the man" / "the woman" instead of character names in Seedance prompts

See `references/seedance-fal-pitfalls.md` for the full async polling pattern, single-image constraint, and prompt strategy.

### 3) Persist source media before generation

If the first frame, reference image, or audio track is local, Telegram-cached, third-party ephemeral, or otherwise not canonical, upload it through Athabasca first and use the returned `asset.publicUrl` as generation input.

Preferred upload endpoint:

```text
POST /api/uploads
```

Use correct metadata such as `projectSlug`, `phase`, `category`, `sourceKind`, title, and provenance. Never use local cache paths as canonical generation inputs.

**Voice message audio trap**: when the user says "attached file" but sends a Telegram voice message, the audio is NOT a named file attachment. It lands in `~/.hermes/audio_cache/` as a hash-named `.mp3` or `.ogg` (e.g. `audio_d5aa648d44f9.mp3`). Check the most recent file in that directory before asking the user to re-send. The user's stated filename (e.g. "landed-the-shots.mp3") will not match anything on disk.

### 4) Submit through normalized API

Use:

```text
POST /api/projects/:slug/generate/video
```

**Hermes `athabasca_project_request` double-encoding pitfall**: when using the `json` parameter on `athabasca_project_request` (or `athabasca_request`), the body may be double-serialized into a JSON string, causing the server to reject with `422 "Invalid input: expected object, received string"`. If this happens, work around it by using `execute_code` with Python `urllib.request` and the `ATHABASCA_API_TOKEN` env var to send the POST directly. The same body that fails via the Hermes `json` param typically succeeds when sent as raw JSON bytes. Treat this as a Hermes transport/tooling issue, not a project-specific prompt issue.

Typical normalized request shape:

```json
{
  "mode": "image-to-video",
  "prompt": "...",
  "imageUrl": "https://...",
  "audioUrl": "https://...",
  "aspectRatio": "landscape",
  "duration": 4,
  "resolution": "720p",
  "provider": "...",
  "model": "...",
  "shotId": "shot_...",
  "title": "...",
  "provenanceNote": "..."
}
```

`audioUrl` is an optional field for audio-conditioned video generation. Upload audio through Athabasca first, just like images, and use the returned `asset.publicUrl`.

**Timeout**: video generation commonly exceeds 60s. Wan 2.7 runs observed around ~90–95s even for short clips. When curl-ing the generate endpoint directly, use `--max-time 180` (or higher) to avoid false timeout failures.

**Hermes tool-wrapper timeout pitfall**: even if curl uses `--max-time 180`, the Hermes terminal tool can still terminate at its own timeout unless you raise the tool-call timeout parameter. For long generation probes, set the terminal tool timeout to at least 240–300s so you can receive the API JSON success/error payload instead of exit 124.

**Idempotency key required for paid-generation safety**:
- Repeated submits/retries without idempotency can create duplicate paid upstream jobs.
- Always send `idempotencyKey` on `POST /api/projects/:slug/generate/video`.
- Use a stable key for the *single intended generation intent* (same key across retries of the same attempt; new key only when you intentionally want a fresh generation).
- Suggested key basis: project slug + mode + provider/model + prompt hash + source media IDs/URLs + shotId.
- If the API returns `409 generation_request_in_progress_for_idempotency_key`, do not resubmit with a new key; poll logs/wait and reuse the same key.
- If the API returns a completed replay for that key, treat it as success and reuse the returned existing asset.
- For long-running requests, always inspect `/api/projects/:slug/generation-logs` before retrying to classify `pending` vs terminal failure and avoid accidental overgeneration.
- **Retrieving assets when logs show `completed` but `outputAssetId` is null**: the generation completed upstream and persisted, but the log entry's `outputAssetId` may be stale or unpopulated. Find the asset by querying `/api/projects/:slug/media?kind=video&limit=50` and matching by `createdAt` timestamp (sort newest-first) or by title substring (e.g. `"HappyHorse r2v"`). Do not assume the log entry is the authoritative asset locator.
- If repeated 10s `wan2.7-videoedit` runs fail with upstream `timed out after 600s`, classify as provider runtime limitation and (when user wants an immediate deliverable) run a shorter fallback (e.g., 5s) with a new, explicit idempotency key and provenance note.

Provider-specific caution:
- For current Alibaba canonical video requests, do **not** send `generateAudio: false` as a harmless default. Omit the field entirely unless/until Athabasca changes the validator behavior.
- For BytePlus Seedance, upstream success payloads may return the final URL under `content.video_url` rather than top-level `video_url`, `output`, or `video.url`. If the normalized endpoint reports `BytePlus task succeeded without a video URL` while the error body contains `content.video_url`, download that URL, upload it through Athabasca as generated video, and patch the BytePlus response normalizer to read `data.content.video_url`.
- For `happyhorse-1.0-i2v`, omit `aspectRatio`; the model follows the first frame.
- Alibaba DashScope API uses `driving_audio` as the media type (not `audio`). If an adapter rejects with "Input should be 'first_frame', 'last_frame', 'driving_audio' or 'first_clip'", the audio type name is the culprit.
- Alibaba `wan2.7-r2v` should submit `input.media`, not `input.reference_urls`. For mixed image+reference-video requests, use typed media entries like `reference_image` and `reference_video`. If the upstream error says `Field required: input.media` or `Input should be 'reference_image', 'reference_video' or 'first_frame'`, the adapter payload shape is wrong, not the creative prompt.
- For `wan2.7-r2v`, do **not** rely on legacy `input.reference_urls`. The working payload uses `input.media` with `reference_image` and `reference_video` entries. See `references/wan-r2v-reference-inputs.md`.
- If you need audio/timing influence in `reference-to-video`, build and upload a black-screen 16:9 MP4 wrapper from the dialogue audio, then pass that uploaded asset in `referenceVideoUrls` rather than trying to feed raw audio directly into the r2v route.

Implementation note:
- If the user asks to "remember" a provider quirk at the code level, prefer a server-side validation + regression-test fix over relying on agent memory. In this repo, the right home is the normalized video validation/capability layer plus API-contract coverage for successful persistence/attachment.

### 5) Persist and attach through Athabasca

The generation endpoint should return an Athabasca asset. If a request path returns an upstream URL only, ingest it through Athabasca media APIs before reporting completion.

For shot-specific outputs, ensure the asset is attached to the relevant shot if the generation endpoint did not already attach it.

Current Athabasca expectation:
- if `shotId` is supplied to `POST /api/projects/:slug/generate/video`, the normalized path should auto-create a shot attachment
- generated video clips belong in the `clips` phase by default, not `shot_list`; `shot_list` precedes image/video generation
- Media phase/tag metadata may validly be absent; shot attachment and asset organization are separate concerns
- if an older asset predates the fix, it may still have `phase: null` or an incorrect phase and require manual attach/backfill only for the specific asset being discussed instead of claiming the fix was retroactive

Do not leave canonical artifacts only on upstream provider storage or `/tmp`.

### 6) Verify before reporting

Before final response:
- confirm response has `ok: true`
- verify returned `asset.publicUrl` returns HTTP 200
- verify attachment exists when shot attachment was requested/expected
- check whether the asset appears in `/api/projects/:slug/media` with `attachments: []`; if so, report success + attachment bug separately
- include the Athabasca public URL or inline video in the response, not just the upstream provider URL

## Multi-model comparison workflow

Use this when the user asks for the same still/prompt across multiple models.

**Known model tradeoffs (empirically confirmed on Prenup production)**:
- `happyhorse-1.0-r2v`: favored for emotional/face-readable romantic beats — closer two-shots, stronger character identity in motion. Supports full 15s.
- `wan2.7-r2v`: cleaner wide/scenic shots with better geography, but less emotionally immediate. Capped at 10s for `reference-to-video` — compress prompts proportionally rather than leaving surplus timestamps. Preferred for establishing and object-only coverage.

**Prompt compliance note for multi-beat lanes**: Models (both Happy Horse and Wan 2.7 r2v) tend to linger on the first-beat reference-image state (standing/hand-hold) before committing to later beats (knee drop). To improve action compliance:
- Front-load imperatives: "Within the first second, he clearly drops to one knee"
- Add explicit negative guidance: "Do not linger on a neutral standing pose"
- Make the progression obligatory, not optional

1. Upload the still once and reuse the Athabasca `asset.publicUrl`.
2. Query capabilities once.
3. Preserve the requested model list and any explicitly requested shot scope (for example, "first shot only"). Do not silently swap in nearby models.
4. Prefer Alibaba as the provider whenever the requested model is available there; only use FAL or OpenRouter for the models Alibaba does not cover or when the user explicitly asks otherwise.
5. Normalize settings per model from live capabilities.
6. Submit one `generate/video` request per model.
7. For every run, record requested settings, actual submitted settings, chosen provider, success/failure, provider error, and asset URL.
8. Disclose any fallback settings or provider substitutions in the final comparison.

Comparison modes:
- **Exact-match comparison:** if the user explicitly wants exact same settings, attempt them and report rejections. Do not silently normalize.
- **Best-effort comparison:** choose nearest valid per-model settings and disclose changes.
- **Apples-to-apples comparison:** choose the strongest common denominator across all requested models based on live capabilities.

If provider moderation/privacy rejects an input image, report that accurately. Do not mislabel it as a prompt-quality problem.

## Debugging workflow

Use this when a generation route fails or output indicates a provider capability mismatch.

1. Check Athabasca health and live capabilities.
2. Inspect generation logs:
   ```text
   GET /api/projects/:slug/generation-logs
   ```
3. Compare `requestJson`, `resolvedParamsJson`, `upstreamRequestJson`, `upstreamResponseJson`, and `upstreamError`.
   - If a video generation log is stuck as `pending` with `resolvedParamsJson` populated but `upstreamRequestJson`, `upstreamResponseJson`, `upstreamJobId`, `outputAssetId`, and `upstreamError` all null, suspect the normalized route created the pending log and then the long synchronous provider call aborted/threw before complete/fail cleanup ran.
   - Do not immediately blame the prompt or provider if the same provider payload works directly. Classify this as a route lifecycle/error-handling issue: the server should wrap post-log provider execution in `try/catch` and/or move long jobs to an async enqueue+poll model so client disconnects do not leave zombie `pending` rows.
4. Determine whether the issue is:
   - prompt/content problem
   - invalid normalized settings
   - missing server environment key
   - provider capability mismatch
   - adapter mapping bug
   - stale capability metadata
   - upstream provider limitation
   - provider account/billing lockout
5. If the issue should have been knowable before the provider call, treat it as an Athabasca validation/capability bug.
6. If the bug concerns generated clip visibility, distinguish phase misclassification from missing attachment. For shot-scoped video, the correct default home is the `clips` phase, while shot attachment remains orthogonal.
7. If an Alibaba `wan2.7-r2v` run fails with `Field required: input.media` or a type whitelist mentioning `reference_image` / `reference_video`, suspect the adapter payload shape first; do not misclassify it as a prompt failure.
8. For r2v audio-conditioned comparisons, be prepared to create an uploaded black-screen MP4 wrapper from the dialogue audio before retrying.
9. If generation logs show `status: "pending"` with resolved params but no upstream request/response/error, and the caller saw a generic transport/undici timeout/abort, suspect a synchronous long-running route lifecycle bug rather than the prompt. The route may have created the pending log, then lost/aborted the HTTP request before provider polling/download/upload completed or before failure cleanup ran. Before retrying with a new idempotency key, classify the pending row; if a direct provider fallback is used, ingest the result back into Athabasca. See `references/synchronous-route-pending-log-hang.md`.
10. If you patch validation/persistence code, restart the long-running Athabasca service before live re-tests; the current shell seeing new code is not enough.
11. Verify both code-level tests and live API behavior. In practice that means: targeted Bun tests first, then an actual `POST /api/projects/:slug/generate/video` re-run, then media/attachment verification.

Important environment diagnostic:
- route success depends on the long-running server/service environment, not the current shell environment. If a route reports a missing provider key, verify/restart the service environment rather than assuming the key is globally absent.
- if upstream returns a missing-key error for a server-side provider, check the service env specifically.
- if upstream returns account lock / exhausted balance, classify it as provider account state, not a prompt/settings failure.
- if a newly added provider appears in `video-capabilities` but the first real request still fails, separate **capability exposure** from **live generation success**. The correct first proof is a low-risk no-face/object-only probe; otherwise privacy moderation on face-bearing references can make a working integration look broken.

### Exact-match vs best-effort retries

When the user asks for multiple models with the same settings, preserve the comparison mode explicitly:

1. **Exact-match phase:** send the requested common settings unchanged.
2. If a model rejects them, report the rejection accurately.
3. Only do a **best-effort retry** if the user asked for it, or if you clearly disclose that you are switching modes to probe what would succeed.
4. In the final report, separate:
   - exact-match failures caused by unsupported settings
   - best-effort retries caused by provider-specific constraints
   - hard failures like missing API keys or exhausted billing

This prevents a provider capability mismatch from being misreported as 'the generation failed' in a single undifferentiated bucket.

### Persistence/attachment interpretation

If generation never reaches a successful asset persistence step, do **not** describe the result as a media-attachment bug.

Use this distinction:
- generation request failed before asset creation -> no media asset should exist in project media
- generation succeeded and returned an asset but media tab is empty -> investigate attachment/persistence with `athabasca-media-attachment-finder`
- generation succeeded and the asset exists in project media but `attachments: []` despite a submitted `shotId` -> classify as a likely attachment/persistence bug in Athabasca's normalized generation path, not a provider failure

Reference notes for recurring provider quirks and failure classification live in `references/provider-quirks.md`.
**Happy Horse 1.0 r2v vs Wan 2.7 r2v** empirical comparison findings from Prenup production runs: see `references/happyhorse-vs-wan-comparison.md`.
Wan 2.7 `input.media` + `reference_video` payload fix and black-screen audio-wrapper comparison pattern: `references/wan-r2v-reference-inputs.md`.
A reusable ffmpeg recipe for black-screen audio-to-video wrappers (i2v audio-driven input) is in `references/black-screen-audio-wrapper.md`.
The external video import workflow (bulk upload of provider-generated clips from Hermes cache) is in `references/external-video-import.md`.
A validated Wan 2.7 video-edit reference-image probe (including payload and timeout pitfalls) is documented in `references/wan2.7-videoedit-image-reference.md`.
Idempotency-key retry safety patterns (to prevent duplicate paid generations on timeout/retry) are in `references/idempotency-retry-guard.md`.
A concrete 10s `wan2.7-videoedit` timeout/fallback case study (client timeout vs server pending vs upstream 600s terminal failure) is in `references/wan2.7-videoedit-10s-timeout-pattern.md`.
Seedance 2.0 via fal.ai quirks (async subscribe vs run pitfall, defaults, `bun -e` gotcha, result shape) are in `references/seedance-fal-pitfalls.md`.
Dynamic first-frame Seedance regeneration pattern — source-still lookup, exact-first-frame prompting, provider routing, retry behavior, and terse report format — is in `references/dynamic-first-frame-seedance-regeneration.md`.
Replicate API shape, Seedance 2.0 specifics (same model ID for t2v/i2v, async poll pattern, `input.image` for i2v), and Replicate vs fal.ai decision guidance: `references/replicate-provider-notes.md`.
A proven Replicate validation pattern for distinguishing moderation-gated face shots from successful no-face insert probes, and for separating persistence success from attachment bugs, is in `references/replicate-seedance-validation-pattern.md`.
BytePlus Seedance 2.0 privacy-moderation behavior, missing-key-vs-upstream-rejection classification, and the recommended no-face/object-only wiring probe are in `references/byteplus-seedance-privacy-moderation.md`.
A BytePlus Seedance provider-wiring pattern — capabilities check, exact JSON review before dispatch, stale-service-env vs upstream-moderation classification, and no-face follow-up probe guidance — is in `references/byteplus-provider-validation-pattern.md`.
Direct BytePlus Seedance fallback + Athabasca ingest pattern for normalized-route blockers is in `references/byteplus-direct-fallback-ingest.md`.

## Panel Extraction from Storyboard Grids

For multi-model i2v comparisons using a storyboard grid as source image, extract the target panel with ffmpeg before uploading. See `references/ffmpeg-grid-panel-extract.md` for the full recipe including coordinate table, commands, and known constraints (e.g., `sourceKind` enum values, upload endpoint path, JSON body escaping).

## Model/provider constraints

The agent should not maintain a parallel encyclopedia of model quirks in skills.

Expected home for constraints:
- provider adapter code maps normalized request fields to upstream payload fields
- route validators reject impossible provider/model/settings combinations before provider calls
- capabilities endpoint advertises valid settings
- tests cover known idiosyncrasies and regression cases
- docs explain stable architecture-level behavior

When a user explicitly asks to encode a quirk in the codebase, the preferred change sequence is:
1. add/adjust validator logic in the normalized video path
2. add a focused unit/API regression test for the invalid combination
3. add an API-contract test for the expected successful persistence/attachment path when relevant
4. restart the live Athabasca service
5. re-run a real generation and verify media URLs plus shot attachment state

Examples of facts that belong in code/tests, not a model-specific skill:
- provider-specific request field names
- duration type/enum differences
- resolution limitations
- audio support flags
- first-frame/reference-image syntax normalization
- provider/model aliases
- invalid combinations that should fail fast
- whether a provider truly supports first-frame, last-frame, reference-image, or audio behavior for a specific model

If a generation fails due to a provider constraint that should have been knowable up front, propose or implement a code/API validation fix instead of creating a model-specific skill.

## Direct provider fallback policy

Only call a provider directly when all are true:
1. the user is explicitly experimenting or the model is not yet exposed in Athabasca
2. updating Athabasca first is not practical for the immediate task
3. the result will be immediately ingested into Athabasca with provenance
4. the discovery will be migrated into code/tests if it becomes recurring

When using a direct fallback, disclose it clearly and avoid creating a provider/model skill unless the user explicitly asks.

**Runtime pitfall**: use `bun -e '...'` for inline scripts, not `bun run -e` (which tries to resolve a script filename and fails). The `@fal-ai/client` package must be installed in the working directory — currently `/home/nrsimha/Sites/athabasca`.

## Final response style

Keep generation reports short:

```text
Generated via Athabasca: [provider/model]
Settings: [duration, resolution, audio, aspect]
Result: [Athabasca public URL or inline video]
Notes: [only important deviations/fallbacks]
```

If generation fails, report:
- provider/model
- normalized settings submitted
- concise error summary
- whether the fix belongs in prompt, settings, provider adapter, validation, or upstream provider behavior
