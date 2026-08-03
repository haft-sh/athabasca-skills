# Midjourney direct upscale from stored buttons

Use this when the user asks to upscale a quadrant from an already-stored Midjourney grid asset and the asset metadata contains `mjButtons`, `discordMessageId`, `discordChannelId`, and `mjJobId`.

## Key lesson

Do not depend on re-fetching the old Discord message from the channel history when the grid may no longer be in the last N messages. If Athabasca already stored the exact button custom ID, trigger the interaction directly from metadata.

## Workflow

1. Fetch the grid asset through `GET /api/media/:assetId`.
2. Read:
   - `metadataJson.mjButtons.U1` / `U2` / `U3` / `U4`
   - `metadataJson.discordMessageId`
   - `metadataJson.discordChannelId`
   - `metadataJson.mjJobId`
3. Submit the Discord interaction using the stored custom ID:
   - `type: 3`
   - `application_id: 936929561302675456`
   - `channel_id`: stored channel ID
   - `message_id`: stored Discord message ID
   - `data.component_type: 2`
   - `data.custom_id`: stored `MJ::JOB::upsample::<quad>::<jobId>`
4. Poll recent channel messages for the Midjourney bot (`936929561302675456`) after the submit time.
5. Match on one attachment and, when possible, a prompt-content snippet from the original generation prompt.
6. Import the returned Discord CDN URL into Athabasca with `POST /api/projects/:slug/media` using:
   - `sourceUrl`: returned Discord CDN attachment URL
   - `category: generated`
   - `sourceKind: generated`
   - `phase: visual_dev` when relevant
   - a project attachment role such as `visual_dev_midjourney_upscale`
   - metadata linking source grid asset ID, selected quadrant, original Discord message ID, returned Discord message ID, MJ job ID, and button custom ID
7. Verify the imported Athabasca public URL returns HTTP 200.

## Pitfall

`scripts/mj-upscale.ts` fetches recent messages and can fail with `Message ... not found in last 25 messages` for older grids. That is not a blocker if the button custom IDs were already persisted on the Athabasca asset. Use the stored custom ID directly.

## Import provenance fields to preserve

- `artifactKind: midjourney_upscale`
- `sourceGridAssetId`
- `sourceGridDiscordMessageId`
- `sourceGridDiscordChannelId`
- `sourceGridMjJobId`
- `upscaleDiscordMessageId`
- `selectedQuadrant`
- `quadrantMeaning`
- `promptIndex`
- `promptTitle`
- `upscaleButton`
- `sourceDiscordCdnUrl`
