# MJ Upscale Recovery — Session Findings (June 2026)

## Finding 1: `message_id` Digit-Swap Transcription Errors

When recovering an upscale from stored `metadataJson.discordMessageId`, the interaction may return **204 Accepted** but the upscaled image never appears in polling. Root cause: the stored message ID was mistranscribed at generation time.

**Symptom:**
- `POST /api/v9/interactions` → 204
- Upscaled image never found in polling window
- Grid message present in Discord when manually checked

**Diagnosis:** Compare stored `message_id` against the actual ID in Discord (via `GET /channels/:id/messages?limit=25` + inspect recent MJ messages). A digit-swap error will show as two IDs that are nearly identical but differ by one digit position.

**Example from June 2026:**
- Stored: `1510802176765957954` (wrong — digit 6 vs 5 at position 14)
- Correct: `1510802176765857954` (from browser Dev Tools network capture)

**Prevention:** When manually extracting `discordMessageId` from Discord Dev Tools, double-check the last 4 digits against the Discord UI URL or message timestamp to confirm you're capturing the right message. Discord embeds message IDs in the Dev Tools payload — verify it matches what you expect.

**Recovery when this happens:**
1. Fetch recent channel messages with `GET /channels/:id/messages?limit=25`
2. Filter for `author.id === "936929561302675456"` and `attachments.length === 1`
3. Find the grid message whose timestamp is closest to the generation time
4. Extract its `id` field — this is the correct `message_id`
5. Re-submit the upscale interaction with the correct ID
6. If the grid has aged out of the 25-message window, paginate with `?limit=50&before=<oldest_seen_id>` or `?limit=100&before=<oldest_seen_id>`

## Finding 2: Python urllib vs Bun — Discord CDN Webhook Attachment Downloads

Midjourney grid images come from two CDN sources:
1. **Midjourney's own CDN** (`s.mj.run`, `cdn.mj.run`) — public, accessible via any client, `Content-Type: image/png/webp`
2. **Discord's attachment CDN** (`cdn.discordapp.com/attachments/...`) — images posted by the Midjourney Bot webhook in the channel

Python's `urllib.request.urlopen()` gets **HTTP 403 Forbidden** when downloading Discord attachment CDN URLs, even with a valid bot token. This is NOT a token problem — the same URL downloads correctly via Bun.

**Affected code (fails):**
```python
req = urllib.request.Request(discord_cdn_url)
with urllib.request.urlopen(req) as r:
    data = r.read()  # HTTP 403 Forbidden
```

**Working code (Bun):**
```bash
bun -e "
const resp = await fetch('https://cdn.discordapp.com/attachments/...', {
  headers: { 'Authorization': token }
});
const buf = await resp.arrayBuffer();
require('fs').writeFileSync('/tmp/img.png', Buffer.from(buf));
"
```

**Why it happens:** Discord CDN checks for certain browser-like request characteristics. Python's urllib identifies as `python-urllib/x.x` by default and is rejected. Bun's fetch identifies as a browser-like client and is accepted.

**Rule:** For any download from `cdn.discordapp.com` (Discord webhook attachments), use Bun runtime via `terminal` + `bun -e "..."` — never Python urllib. Midjourney's own CDN URLs work fine with Python.

## Finding 3: Manual Payload Capture for Reverse Engineering

When the automated path fails and you're unsure of the correct API shape, ask the user to capture the request payload from browser Dev Tools. This is the most reliable way to get the exact:
- Endpoint URL
- Request headers (especially `authorization`, `content-type`, `x-super-properties`)
- Request body JSON structure
- Session ID format

From a single captured curl command (June 2026):
```
POST https://discord.com/api/v9/interactions
{
  "type": 3,
  "nonce": "1510861931349540864",
  "channel_id": "1028928040996196422",
  "message_id": "1510802176765857954",
  "application_id": "936929561302675456",
  "session_id": "ad0ba466c28ccbbbfd74c668c97bfd48",
  "data": {
    "component_type": 2,
    "custom_id": "MJ::JOB::upsample::1::1e9e4930-a644-4a4b-b1f8-5864392c64a0"
  }
}
```

Key observations:
- `session_id` is a 32-char hex string from the browser's localStorage (`localeStorage.midjourneyData.sessionId` or similar)
- `nonce` is an 18-19 digit timestamp-based string
- `message_id` must match the exact grid message in Discord — mismatches return 204 but do nothing

**Token refresh via `.env`:** If the stored token may be stale, re-read it from `~/.hermes/hermes-agent/.env` (Athabasca project dir) with:
```bash
grep MIDJOURNEY_DISCORD_TOKEN ~/.hermes/hermes-agent/.env
```
The token format is `MjM4...` (user account tokens, not bot tokens).
