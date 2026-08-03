# Midjourney Direct Discord Recovery + Athabasca Persistence

Use this when Athabasca's `/api/projects/:slug/generate/image` call times out or fails to return an asset, but the Midjourney grid is visible in Discord.

## Durable lesson

A timeout from the Athabasca generation endpoint is not proof that Midjourney failed. If Discord completed the grid, recover the grid from Discord, download it immediately, persist it to R2 through Athabasca media APIs, and attach it to the intended shot/project record. Preserve `mjButtons` metadata so later upscale/variation actions remain deterministic.

## Recovery flow

1. Fetch recent Discord channel messages using the configured `MIDJOURNEY_DISCORD_TOKEN` and `MIDJOURNEY_CHANNEL_ID`.
2. Match on the descriptive prompt body, not on volatile URL text. Use submit-time gating where possible.
3. For the matching Midjourney bot message:
   - read `message.id`
   - read attachment URL from `message.attachments[0].url`
   - extract button `custom_id`s from `message.components`
   - derive `mjJobId` from the button IDs when present
4. Download the Discord attachment immediately to `/tmp` or another staging path. Discord CDN URLs expire.
5. Upload through `POST /api/projects/:slug/media`:
   - `phase=storyboard` for storyboard grids
   - `category=generated`
   - `sourceKind=generated`
   - `metadataJson` should include:
     - `artifactKind: "midjourney_grid"`
     - `workflow: "direct-discord-recovery"` or `"direct-discord-generation"`
     - `projectSlug`
     - `shotId` and `shotNumber` when applicable
     - `prompt`
     - `provider: "midjourney"`
     - `model: "midjourney-v8.1"`
     - `discordMessageId`
     - `discordChannelId`
     - `mjJobId`
     - `mjButtons`
6. If the grid belongs to a shot, explicitly attach the returned asset with `POST /api/projects/:slug/shots/:shotId/media` and verify `GET /api/projects/:slug/shot-list` shows the asset under `mediaAttachments`.

## Practical matching notes

- Discord/Midjourney can rewrite leading prompt URLs to `s.mj.run`, so do not require exact full-prompt string equality.
- Unicode dashes and whitespace can be normalized away before matching.
- If multiple recent matches exist, prefer the newest message after the submission timestamp; if recovering a known already-visible grid, use the newest prompt match and record the source as `direct-discord-recovery`.

## Verification

- `GET /api/projects/:slug/media?phase=storyboard` includes the asset.
- `GET /api/projects/:slug/shot-list` shows one or more `mediaAttachments` for the target shot.
- The persisted `asset.publicUrl` is an R2 URL, not a Discord CDN URL.
- `metadataJson.mjButtons` includes U/V/reroll custom IDs.
