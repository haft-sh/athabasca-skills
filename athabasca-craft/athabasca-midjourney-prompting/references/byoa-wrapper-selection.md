# Midjourney BYOA — Approach Comparison & Confirmed Payloads

## Two Viable Approaches (May 2026)

### A) Midjourney Web API (confirmed working, NOT recommended for automation)

**Endpoint:** `POST https://www.midjourney.com/api/submit-jobs`

**Auth requires:**
- `__Host-Midjourney.AuthUserTokenV3_i` — Firebase JWT (expires ~1 hour)
- `cf_clearance` — Cloudflare anti-bot challenge (expires 15–30 min)
- `__cf_bm` — Cloudflare bot management
- Multiple session cookies (AMP, GAESA, etc.)

**Payload (confirmed working from captured curl, May 2026):**
```json
{
  "f": {"mode": "fast", "private": false},
  "channelId": "singleplayer_2f65afa4-c01d-4866-934d-ee2638c304f1",
  "metadata": {
    "isMobile": null,
    "imagePrompts": 1,
    "imageReferences": 2,
    "characterReferences": 0,
    "depthReferences": 0
  },
  "t": "imagine",
  "prompt": "..."
}
```

**Why NOT to use for automation:**
- `cf_clearance` expires in 15–30 minutes
- Requires real browser challenge solve to refresh
- Cloudflare bot management will flag/block automated use
- Token rotation is impractical for server-side integration

### B) Discord Interactions API (recommended for automation)

**Endpoint:** `POST https://discord.com/api/v10/interactions`

**Auth requires:**
- Discord user token (Authorization header) — lasts weeks

**Key constants (fetch dynamically, may change):**
- Midjourney Bot application ID: `936929561302675456`
- `/imagine` command ID: fetched at runtime via:
  `GET /api/v10/channels/{channel_id}/application-commands/search?query=imagine&type=1`
- Command version: fetched at runtime
- Channel ID: per-user configuration

**Result polling:**
```
GET /api/v10/channels/{channel_id}/messages?limit=5
```
Poll every 5s for up to 3 minutes. Match Midjourney bot messages (author.id = 936929561302675456) with attachments.

**Upscale button interaction:**
```json
POST /api/v10/interactions
{
  "type": 3,
  "application_id": "936929561302675456",
  "channel_id": "{channel_id}",
  "message_id": "{message_id}",
  "data": {
    "component_type": 2,
    "custom_id": "MJ::JOB::upsample::{1|2|3|4}::{message_id}"
  },
  "nonce": "<18-digit integer>"
}
```

Variation custom_id format: `MJ::JOB::variation::{1|2|3|4}::{message_id}`

## Standalone Validation Script

Location: `scripts/mj-sanity-check.ts`

Flow: env validation → fetch command metadata → submit /imagine → poll → extract image URL → verify accessible.

## Credentials Setup

Required env vars:
```
MIDJOURNEY_DISCORD_TOKEN=
MIDJOURNEY_CHANNEL_ID=
MIDJOURNEY_SERVER_ID= (optional)
```

See `../../../scripts/GETTING_DISCORD_TOKEN.md` for extraction instructions.