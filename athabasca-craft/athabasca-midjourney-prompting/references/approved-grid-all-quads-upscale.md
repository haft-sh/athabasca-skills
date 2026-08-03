# Approved Midjourney grids → all-quads upscale workflow

Use this when the user reviews a batch of Midjourney 2×2 grids, marks several as approved/favorites, then says some form of **"upscale all of these"**.

## Interpretation

If the user says **"upscale all of these"** after approving multiple grids, treat it as:

- upscale **U1, U2, U3, and U4** for **each approved grid**;
- do **not** continue the one-at-a-time quadrant selection loop;
- do **not** ask for a quadrant unless he explicitly says he wants to choose one per grid.

This differs from the normal shortlist workflow where the user chooses one quadrant per grid.

## Required metadata

Each grid asset must have Midjourney metadata in `metadataJson`:

- `discordMessageId`
- `discordChannelId`
- `mjButtons.U1` through `mjButtons.U4`
- optionally `mjJobId`

The current Athabasca Midjourney generation path stores these automatically for new grids.

## Batch steps

For each approved grid asset, in stable review/order:

1. Read `metadataJson.mjButtons.U1`–`U4`.
2. Submit each button as a Discord component interaction (`type: 3`) against the grid message.
3. Poll the Midjourney channel for the resulting upscale message:
   - author is the Midjourney bot;
   - message ID is greater than the source grid message ID;
   - timestamp is after submit time minus small skew;
   - has exactly one image attachment;
   - is not another grid with U1–U4 buttons.
4. Download the Discord CDN image immediately.
5. Persist the upscale through Athabasca project media upload with:
   - `phase=visual_dev` or the active project phase tag;
   - `category=generated`;
   - `sourceKind=generated`;
   - project attachment role such as `visual_dev_midjourney_upscale`;
   - `metadataJson.artifactKind="midjourney_upscale"`;
   - `sourceGridAssetId`, `sourceGridDiscordMessageId`, `selectedQuadrant`, `quadrantMeaning`, `promptIndex`, and `promptTitle` when available.
6. Save a resumable local JSON log while running. If the batch is interrupted, skip already-successful `(gridAssetId, quadrant)` pairs and resume.

## Telegram review pitfall

When showing a grid for quadrant selection, always send the grid as native media (`MEDIA:/tmp/...`). If the user says **"show me the image"**, assume the prior media did not render or was missed; resend the same media plainly before asking again. Do not just repeat text around the asset ID.

## Practical notes

- Stagger Discord interactions by several seconds to avoid rate limiting.
- Use background execution with notify-on-complete for 10+ upscales; 28 upscales can take many minutes.
- Preserve the original grid asset. Upscales are new generated media assets linked back by metadata.
- Use the true Midjourney U-button path, not crops from the 2×2 grid, whenever `mjButtons` are available.
