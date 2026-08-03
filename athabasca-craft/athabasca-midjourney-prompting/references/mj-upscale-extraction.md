# MJ Upscale Extraction from Discord (When mjButtons Missing)

When `mjButtons` wasn't persisted at generation time, extract button custom_ids directly from Discord's message API.

## Steps

1. **Fetch recent channel messages:**
```bash
curl -s -H "Authorization: $MIDJOURNEY_DISCORD_TOKEN" \
  "https://discord.com/api/v9/channels/$MIDJOURNEY_CHANNEL_ID/messages?limit=15"
```

2. **Find the grid message by prompt text or timestamp.** Grid messages have `components` with buttons whose `custom_id` starts with `MJ::JOB::upsample::`.

3. **Extract button IDs:**
```python
for row in msg.get('components', []):
    if row.get('type') != 1: continue
    for btn in row.get('components', []):
        cid = btn.get('custom_id', '')
        if cid.startswith('MJ::JOB::upsample::'):
            n = cid.split('::')[3]
            print(f'U{n}: {cid}')
```

4. **Submit upscale interaction:**
```bash
curl -s -o /dev/null -w "%{http_code}" -X POST "https://discord.com/api/v10/interactions" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": 3,
    "application_id": "936929561302675456",
    "channel_id": "$CHANNEL_ID",
    "message_id": "$GRID_MSG_ID",
    "session_id": "<32-hex>",
    "nonce": "<18-digit>",
    "data": {
      "component_type": 2,
      "custom_id": "MJ::JOB::upsample::2::<jobId>"
    }
  }'
# Returns 204 on success
```

5. **Poll for upscaled result** (~15-20s). Upscaled messages have 1 attachment, grid messages have components with buttons.

6. **Download and persist immediately** — Discord CDN URLs are ephemeral.

## Note
Upscaled messages in Discord still have components (Vary buttons), so distinguish by checking: grid messages have 4 U buttons + 4 V buttons + reroll; upscale messages have Vary (Subtle/Strong) buttons only.
