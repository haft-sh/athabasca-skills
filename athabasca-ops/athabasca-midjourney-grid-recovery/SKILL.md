---
name: athabasca-midjourney-grid-recovery
description: Recover true Midjourney grid variants and upscales from older Athabasca assets by tracing Discord provenance, then re-import with canonical Athabasca metadata.
version: 1.0.0
---

# Athabasca Midjourney Grid Recovery

Use this when a user wants a specific panel or upscale from an older Midjourney asset already stored in Athabasca, especially when the original asset no longer exposes `mjButtons`, `discordMessageId`, or a clean generation row.

## When to use

- User asks for `U1`/`U2`/`U3`/`U4` from an existing Midjourney 2x2 grid
- The asset is old and current Athabasca surfaces appear incomplete or stale
- The asset was previously recovered from Discord CDN rather than persisted through a clean Midjourney response path
- The goal is the **true Midjourney upscale**, not a crop from the 4-up grid

## Core rule

Do **not** crop the quadrant unless the user explicitly accepts a fake substitute.

If the user asks for a quadrant from a Midjourney grid, the default interpretation is: recover the real Midjourney variant/upscale if it is still available.

## API and provenance discipline

1. Prefer `athabasca_request` / `athabasca_project_request` over raw curl when the Athabasca plugin is available.
2. Read the global asset route first when project-scoped media lookup is awkward:
   - `GET /api/media/:assetId`
3. Treat `metadataJson`, `attachments`, `generation`, and provenance notes as the recovery surface.
4. After recovery, re-import the result immediately through Athabasca project media so the project regains a canonical asset with provenance.

## Recovery workflow

### 1) Inspect the source asset carefully

From the asset body, look for any of:
- `mjButtons`
- `discordMessageId`
- `discordChannelId`
- `mjJobId`
- `metadataJson.sourceDiscordUrl`
- `generation.parametersJson`
- titles / provenance notes that indicate Discord recovery or timeout recovery

Do not trust the title alone. The real image pixels and the Discord linkage are more authoritative than stale text metadata.

### 2) Verify the source image is really a 2x2 grid

Inspect the actual image bytes, not just the title/prompt.
Confirm:
- it is a 4-panel Midjourney grid
- the requested quadrant is visually identifiable
- quadrant numbering matches the user's intent (`U1` = top-left, `U2` = top-right, `U3` = bottom-left, `U4` = bottom-right)

### 3) Choose the best recovery path

#### Path A — direct stored button metadata exists
If the asset already exposes `mjButtons` plus `discordMessageId` / `discordChannelId`:
- use the stored `MJ::JOB::upsample::<n>::<job-id>` custom ID directly
- trigger the interaction against the original message

#### Path B — only Discord recovery metadata exists
If the asset lacks `mjButtons` but has `metadataJson.sourceDiscordUrl` and `metadataJson.discordChannelId`:
- parse the Discord CDN URL and recover the original **attachment ID**
- search the Discord channel history for the message carrying that attachment
- recover the original grid message from that match
- extract the `U1`–`U4` custom IDs from the recovered message components

This is the key durable technique for old Discord-recovered assets.

#### Path C — prompt-text search fallback
If attachment-ID recovery is unavailable, search Discord history by a distinctive prompt substring and locate the original grid message that still has `U1`–`U4` buttons.
Do **not** stop at later upscale messages that only expose `Upscale (Subtle)` / `Vary` / `Zoom` controls.

### 4) Trigger the true interaction

Use the lean Discord component interaction payload:
- `type: 3`
- `application_id: 936929561302675456`
- `channel_id`
- `message_id`
- `session_id`
- `nonce`
- `data.component_type: 2`
- `data.custom_id: MJ::JOB::upsample::<n>::<job-id>`

A `204` response only means the click was accepted. It is **not** proof that the upscale succeeded.

### 5) Poll for the returned result

Poll recent channel messages until the returned single-image upscale appears.
Capture:
- returned Discord message ID
- attachment URL
- timestamp
- any follow-up buttons

### 6) Visually verify the returned image

Compare the returned single-image result against the original grid.
Confirm it actually matches the requested quadrant.
Do not report success from Discord interaction acceptance alone.

### 7) Re-import into Athabasca immediately

Persist through:
- `POST /api/projects/:slug/media`

Recommended provenance fields:
- `title`
- `sourceKind: generated`
- `category: generated`
- `sourceUrl` = returned Discord/media URL
- `metadataJson` containing:
  - `workflow: midjourney-grid-upscale-recovery`
  - `derivedFromAssetId`
  - `midjourneyQuadrant`
  - `discordChannelId`
  - `sourceDiscordMessageId`
  - `returnedDiscordMessageId`
  - `mjJobId`
- `generation` containing:
  - `provider: midjourney`
  - `model: midjourney-v8.1`
  - `prompt: Recovered from original Midjourney grid via true U<n> button.`
  - `parametersJson` with button + message IDs

## Pitfalls

- Do not trust stale asset titles or prompts over the actual image.
- Do not confuse a later upscale message with the original grid message.
- Do not report success from the `204` interaction response; always wait for the returned image.
- Do not leave the result only on Discord CDN; import it back into Athabasca.
- Do not default to crops when a real Midjourney button path is still recoverable.

## Verification checklist

- [ ] Confirmed source asset is a 2x2 Midjourney grid
- [ ] Identified the requested quadrant visually
- [ ] Recovered original grid message or stored button metadata
- [ ] Triggered the true `U1`–`U4` Midjourney button
- [ ] Found the returned upscale message and attachment URL
- [ ] Visually confirmed the returned image matches the requested quadrant
- [ ] Re-imported into Athabasca with provenance
- [ ] Verified the Athabasca public URL returns HTTP 200
