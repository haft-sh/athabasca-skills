# Discord Interactions API — Validated Findings (May 2026)

Validated end-to-end on 2026-05-13 using `scripts/mj-sanity-check.ts` and `scripts/mj-upscale.ts`.

## Confirmed Working Flow

### 1. Fetch command metadata

Channel-level search returns empty for DM channels:
```
GET /api/v10/channels/{dm_channel_id}/application-commands/search?query=imagine&type=1
→ {"application_commands": []}
```

Application-level endpoint works:
```
GET /api/v10/applications/936929561302675456/commands
→ returns array including the imagine command
```

Confirmed values (as of May 2026):
- `command.id`: `938956540159881230`
- `command.version`: `1237876415471554623`
- `command.application_id`: `936929561302675456`

**Fetch dynamically every time** — don't hardcode these.

### 2. Submit /imagine interaction

```
POST /api/v10/interactions
Body:
{
  "type": 2,
  "application_id": "936929561302675456",
  "channel_id": "{channel_id}",
  "session_id": "{32-char hex}",
  "nonce": "{18-digit string}",
  "data": {
    "version": "{command.version}",
    "id": "{command.id}",
    "name": "imagine",
    "type": 1,
    "options": [{"type": 3, "name": "prompt", "value": "..."}],
    "application_command": { ... full command object ... },
    "attachments": []
  }
}
Response: 204 No Content
```

### 3. Poll for grid results

```
GET /api/v10/channels/{channel_id}/messages?limit=5
Poll every 5s, timeout after 3 minutes.
Filter: msg.author.id === "936929561302675456"
Match: content includes prompt text or "--" params
Extract: attachments[0].url
```

Result is a Discord CDN URL with expiring query params (`?ex=...&is=...&hm=...`). Download immediately and persist.

### 4. Image characteristics

- First test: 2912×1632 (16:9), 8.3MB PNG
- Second test: 2688×1792 (3:2), 8.5MB PNG
- Filename format: `{discord_username}_{truncated_prompt}_{uuid}.png`

## Upscale Interaction

After extracting the job ID from the grid message's buttons, submit an upscale:

```
POST /api/v10/interactions
{
  "type": 3,
  "application_id": "936929561302675456",
  "channel_id": "{channelId}",
  "message_id": "{gridMessageId}",
  "session_id": "{32-char hex}",
  "nonce": "{18-digit}",
  "data": {
    "component_type": 2,
    "custom_id": "MJ::JOB::upsample::2::{jobId}"
  }
}
→ 204 No Content
```

Poll with `GET /channels/{channelId}/messages?limit=5`. Upscaled messages have exactly 1 attachment (grid messages have multiple or an embed thumbnail).

## Extracting Button custom_ids from Grid Messages

Grid messages have `components` (array of action rows). Each button's `custom_id` encodes the action:

```
MJ::JOB::upsample::{N}::{jobId}         → U{N} upscale
MJ::JOB::variation::{N}::{jobId}         → V{N} variation
MJ::JOB::reroll::0::{jobId}::SOLO       → reroll
```

To extract all buttons at once (needed for storing in asset `metadataJson.mjButtons`):

```typescript
function extractButtonActions(msg: any): Record<string, string> {
  const buttons: Record<string, string> = {};
  for (const row of msg.components ?? []) {
    if (row.type !== 1) continue;
    for (const btn of row.components ?? []) {
      const id = btn.custom_id ?? "";
      if (id.startsWith("MJ::JOB::upsample::")) buttons[`U${id.split("::")[3]}`] = id;
      else if (id.startsWith("MJ::JOB::variation::")) buttons[`V${id.split("::")[3]}`] = id;
      else if (id.includes("reroll")) buttons["reroll"] = id;
    }
  }
  return buttons;
}
```

Store the resulting map in `metadataJson.mjButtons` on the asset — enables future U/V actions without re-querying Discord.

## Bot-Only Endpoint Workaround

`GET /channels/:id/messages/:msg_id` (single message fetch) → `20002 Only bots can use this endpoint`

Workaround: `GET /channels/:id/messages?limit=25` → find message by ID in the array. The message must still be within the limit window. Since Discord DM retention is short, storing button custom_ids at upload time is the durable solution.

## Authentication

- Header: `Authorization: {user_token}`
- Token format: base64-encoded (starts with user ID like `MjM4...`)
- Tokens expire periodically — 401 means re-extract from browser Dev Tools
- No Cloudflare challenges needed

## Known Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| 401 Unauthorized | `{"message": "401: Unauthorized", "code": 0}` | Re-extract token from browser |
| Channel search empty | `application_commands: []` for DM | Use `/applications/{app_id}/commands` |
| Deno APIs in Bun | `ReferenceError: Deno is not defined` | Use `process.env` and `process.exit` only |
| Expiring CDN URLs | Image inaccessible after hours/days | Download and store in R2 immediately |
| Single message GET 403 | `20002 Only bots can use this endpoint` | Use `?limit=25` and find by ID in list |

## Token Extraction

1. Open Discord in Chrome
2. Dev Tools → Network tab
3. Find `discord.com/api/v10/` request
4. Copy `Authorization` header value
5. Set as `MIDJOURNEY_DISCORD_TOKEN`

## Midjourney Web API (NOT for automation)

Confirmed working but NOT suitable for automation:
- `POST https://www.midjourney.com/api/submit-jobs`
- Payload: `{"t":"imagine","f":{"mode":"fast","private":false},"channelId":"singleplayer_{userId}","prompt":"...","metadata":{...}}`
- Requires `cf_clearance` cookie (expires 15-30 min, needs browser challenge)
- Requires Firebase JWT cookie (expires ~1 hour)
- Clean payload but Cloudflare blocks automated use