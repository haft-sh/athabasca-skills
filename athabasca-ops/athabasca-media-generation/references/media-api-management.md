# Athabasca Media API Management Patterns

Durable API knowledge for managing generated assets: tagging, rating, canonical marking, and superseding old versions.

## Canonical Asset Convention

the user established this convention (May 2026):

| Field | Purpose | Values |
|---|---|---|
| `colorTag` | Canonical status | `green` = official reference (locked for production use) |
| `ratingStars` | Visual quality | 1-5, independent of canonical status |
| `tags` | Descriptive metadata | Scene names, locations, props, era (`2012`, `2026`), `canonical-location`, `canonical-prop`, `canonical-reference`, `hero-prop`, `recurring` |

**Workflow after locking an asset:**
```bash
# 1. Mark as canonical
curl -sS -X PATCH "http://localhost:3000/api/projects/:slug/media/:assetId" \
  -H 'Content-Type: application/json' \
  --data-binary '{"colorTag": "green", "ratingStars": 5}'

# 2. Add descriptive tags
curl -sS -X POST "http://localhost:3000/api/projects/:slug/media/:assetId/tags" \
  -H 'Content-Type: application/json' \
  --data-binary '{"set": ["2012", "writing-room", "canonical-location", "wood-paneling"]}'

# 3. Mark superseded versions as yellow
curl -sS -X PATCH "http://localhost:3000/api/projects/:slug/media/:oldAssetId" \
  -H 'Content-Type: application/json' \
  --data-binary '{"colorTag": "yellow"}'
```

## API Limitations

### PATCH endpoint limitations

`PATCH /api/projects/:slug/media/:assetId` supports ONLY:
- `colorTag` (string: `green`, `yellow`, `red`, or `null`)
- `ratingStars` (integer: 0-5)

**Does NOT support:**
- `title` — title is set at upload time and cannot be changed via PATCH
- `tags` — tags are managed via the separate tags endpoint
- `provenanceNote` — set at upload time

### Tags endpoint

`POST /api/projects/:slug/media/:assetId/tags`

Supports three modes:
- `{"set": ["tag1", "tag2"]}` — replace all tags
- `{"add": ["tag3"]}` — append tags
- `{"remove": ["tag1"]}` — remove specific tags

### Media upload categories

`POST /api/projects/:slug/media` field `category` accepts:
- `research`
- `moodboard`
- `generated`
- `inbox`
- `misc`

Note: `document` is NOT a valid category. Use `misc` for markdown/HTML documents.

## Querying Assets

```bash
# List all assets (paginated)
curl -sS "http://localhost:3000/api/projects/:slug/media?limit=100"

# Filter by colorTag
curl -sS "http://localhost:3000/api/projects/:slug/media?limit=100" | \
  jq '[.assets[] | select(.colorTag == "green")]'

# Filter unreviewed
curl -sS "http://localhost:3000/api/projects/:slug/media?limit=100" | \
  jq '[.assets[] | select(.colorTag == null)]'

# Group by status
curl -sS "http://localhost:3000/api/projects/:slug/media?limit=100" | \
  jq '[.assets[]] | group_by(.colorTag) | map({tag: .[0].colorTag, count: length})'
```

## MJ Grid Delivery Pitfall

When showing MJ grid results to the user, **always download and deliver as native media** (`MEDIA:/local/path`), not just as a URL. MJ grids on R2 are WebP format despite `.jpg` extension — download with correct extension:

```bash
curl -sS -o /tmp/mj-grid.webp "https://media.example.com/<project-slug>/generated/..."
file /tmp/mj-grid.webp  # verify: RIFF (little-endian) data, Web/P image
```

Then deliver: `MEDIA:/tmp/mj-grid.webp`

the user corrected this (May 2026): "I don't see any MJ grid here, you didn't link me to the asset."

## Upscale Detection (mjButtons absent)

When Athabasca returns an MJ asset with empty `metadataJson.mjButtons`, the upscale button custom_ids were not captured. Recovery:

```python
# Fetch recent Discord messages
resp = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=10",
    headers={"Authorization": token})

# Find grid by prompt content substring
for m in resp.json():
    if "prompt keywords" in m.get("content", "").lower() and len(m.get("components", [])) > 0:
        for row in m["components"]:
            for btn in row.get("components", []):
                if "upsample::1" in btn.get("custom_id", ""):
                    u1_id = btn["custom_id"]
```

Then submit via `POST https://discord.com/api/v9/interactions` with `type: 3`.
