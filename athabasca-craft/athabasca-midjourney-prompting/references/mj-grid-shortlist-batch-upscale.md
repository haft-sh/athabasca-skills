# Midjourney Grid Shortlist → Batch Upscale Workflow

Use this when the user wants to review a set of Midjourney 2x2 grids, choose one quadrant per shot, and only then run upscales in a batch.

## UX pattern

1. Show grids one at a time in shot order as native Telegram media (`MEDIA:/tmp/...`).
2. State the quadrant mapping every time or at least before the loop:
   - `1 = top-left`
   - `2 = top-right`
   - `3 = bottom-left`
   - `4 = bottom-right`
3. Ask for exactly one digit: `1`, `2`, `3`, or `4`.
4. Record the answer durably in a small local state JSON while collecting, e.g. `/tmp/<project>_upscale_selection_state.json`.
5. Do **not** start upscaling until all answers are collected.
6. After the final answer, summarize the choices and then start the batch upscale job.

This avoids interleaving user review with slow provider work and makes the user's selection pass feel fast.

## Data needed for deterministic batch upscale

Each persisted grid asset should have `metadataJson` containing:

```json
{
  "artifactKind": "midjourney_grid",
  "projectSlug": "prenup",
  "shotNumber": 1,
  "shotId": "shot_...",
  "discordMessageId": "150...",
  "discordChannelId": "102...",
  "mjJobId": "uuid",
  "mjButtons": {
    "U1": "MJ::JOB::upsample::1::{jobId}",
    "U2": "MJ::JOB::upsample::2::{jobId}",
    "U3": "MJ::JOB::upsample::3::{jobId}",
    "U4": "MJ::JOB::upsample::4::{jobId}",
    "V1": "MJ::JOB::variation::1::{jobId}",
    "V2": "MJ::JOB::variation::2::{jobId}",
    "V3": "MJ::JOB::variation::3::{jobId}",
    "V4": "MJ::JOB::variation::4::{jobId}",
    "reroll": "MJ::JOB::reroll::0::{jobId}::SOLO"
  }
}
```

If `mjButtons` are missing, recover them from Discord before upscaling; see `references/mj-upscale-extraction.md`.

## Batch upscale steps

For each selected shot:

1. Resolve the grid asset from Athabasca:
   - Prefer `GET /api/projects/:slug/media?phase=storyboard` and match `metadataJson.artifactKind === "midjourney_grid"` plus `shotNumber`.
   - Fallback to matching the human title only if metadata is missing.
2. Read `metadataJson.discordMessageId` and `metadataJson.mjButtons["U<n>"]`.
3. Submit Discord component interaction:

```json
{
  "type": 3,
  "application_id": "936929561302675456",
  "channel_id": "{channelId}",
  "message_id": "{gridMessageId}",
  "session_id": "{32-char hex}",
  "nonce": "{18-19 digit nonce}",
  "data": {
    "component_type": 2,
    "custom_id": "MJ::JOB::upsample::<n>::{jobId}"
  }
}
```

4. Poll channel messages for the new upscale result.
   - Ignore the original grid message.
   - Ignore messages older than submit time minus a small skew margin.
   - Distinguish upscales from grids: grid messages have four U buttons plus four V buttons; upscale messages have a single attachment and vary/zoom/pan-style buttons, not U1-U4.
5. Download the upscale immediately; Discord CDN links are ephemeral.
6. Persist through `POST /api/projects/:slug/media` with:
   - `phase=storyboard`
   - `category=generated`
   - `sourceKind=generated`
   - `title=<Project> Shot NNN Upscale Q<n>`
   - `metadataJson.artifactKind="midjourney_upscale"`
   - `metadataJson.selectedQuadrant=<n>` and `quadrantMeaning`
   - `metadataJson.sourceGridAssetId`, `sourceGridDiscordMessageId`, `upscaleDiscordMessageId`
   - any new upscale buttons from the upscale message
7. Explicitly attach the uploaded upscale asset to the shot with `POST /api/projects/:slug/shots/:shotId/media`.
8. Verify each shot has the expected new media attachment and the returned public URL is durable.

## Pitfalls

- Do not launch upscales one-by-one while still collecting the user's choices unless he explicitly asks for that. First collect all answers, then batch.
- If the Athabasca generation endpoint times out but the grid appears in Discord, treat it as a polling/persistence failure, not a generation failure. Recover the Discord message, persist it to R2, and store `mjButtons` before proceeding.
- Do not rely on Discord CDN URLs in reports or project state. Download and re-upload to R2 immediately.
- Do not assume upload-time metadata attaches an asset to a shot. Upload the asset, then explicitly call the shot media attach endpoint and verify.
- Preserve the grid asset and the upscale asset separately. The grid remains useful for rerolls/variations and audit trail.
