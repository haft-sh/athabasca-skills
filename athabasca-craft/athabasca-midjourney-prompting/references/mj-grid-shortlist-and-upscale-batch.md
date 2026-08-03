# Midjourney Grid Shortlisting and Batch Upscale Workflow

Use this when the user wants to review a sequence of Midjourney 2x2 grids, choose quadrants, and only then run all upscales in batch.

## User Interaction Pattern

1. Do **not** upscale immediately after the first choice.
2. Persist a simple selection state file while collecting answers, for example:
   ```json
   {
     "projectSlug": "project-slug",
     "mode": "collecting_quadrants_before_batch_upscale",
     "mapping": {"1":"top-left","2":"top-right","3":"bottom-left","4":"bottom-right"},
     "answers": {"1":2,"2":1}
   }
   ```
3. Show grids one at a time as native Telegram media.
4. Ask for exactly one answer per shot: `1, 2, 3, or 4`.
5. Record each answer, confirm concisely, then show the next grid.
6. After all choices are collected, summarize selections and start the batch upscale unless the user requested a review checkpoint.

## Quadrant Mapping

Midjourney grid convention:
- `1` = top-left = `U1`
- `2` = top-right = `U2`
- `3` = bottom-left = `U3`
- `4` = bottom-right = `U4`

Use the same numeric mapping in Telegram so answers stay fast.

## Batch Upscale Execution Pattern

For each selected shot:
1. Read persisted grid asset metadata from Athabasca. Prefer `metadataJson.mjButtons.U<n>` plus `discordMessageId` and `discordChannelId`.
2. If metadata is missing, recover from Discord message history.
3. Submit a Discord component interaction using the stored button metadata.
4. Poll the channel for the upscaled result.
5. Download immediately because Discord CDN URLs are ephemeral.
6. Persist through `POST /api/projects/:slug/media`.
7. Include metadata such as:
   - `artifactKind: "midjourney_upscale"`
   - `sourceGridAssetId`
   - `sourceGridDiscordMessageId`
   - `selectedQuadrant`
   - `upscaleButtonCustomId`
   - result `discordMessageId`
   - `provider: "midjourney"`, `model: "midjourney-v8.1"`
8. Attach the upscaled asset to the relevant shot if applicable.
9. Verify shot attachments after the batch.

## Recovery Workflow When Athabasca Times Out but Discord Succeeds

This is a success-recovery path, not a generation failure:
1. Fetch recent Discord channel messages using the configured token/channel.
2. Match by prompt snippet and submit-time gating.
3. Download the grid attachment immediately.
4. Extract `mjButtons`, `discordMessageId`, `discordChannelId`, and `mjJobId` from the message.
5. Upload through the Athabasca project media API with all button metadata stored in `metadataJson`.
6. Attach to the corresponding shot if needed.

Do not rerun blindly if the good grid already exists in Discord. Recover and persist it instead.

## Telegram Delivery Detail

When presenting grid choices, keep the loop fast:

```markdown
Recorded: **Shot 003 → quadrant 4 / bottom-right**.

## Shot 004 / 009 — Insert or Hero Shot

MEDIA:/tmp/project_mj_grids/shot_004_grid.webp

Which quadrant should I upscale for **Shot 004**? Reply with **1, 2, 3, or 4**.
```

## Anti-Bloat Rule

Keep the workflow here. Do not preserve one production's full shot inventory, temporary state file path, or named story beats in this reference file.