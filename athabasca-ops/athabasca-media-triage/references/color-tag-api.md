# Color Tag API Reference

## Endpoint

```
PATCH /api/projects/:slug/media/:assetId
```

**Critical:** The path MUST include the project slug. `PATCH /api/media/:assetId` does NOT exist and returns `NOT_FOUND`.

## Body

```json
{
  "colorTag": "green",
  "ratingStars": 5
}
```

Valid `colorTag` values: `green`, `yellow`, `red`, `blue`, `purple`, `null` (clear tag)

## Response

Returns `{ ok: true, asset: { ... } }` with the updated asset object.

## Usage via curl (preferred)

```bash
curl -s -X PATCH http://<host>:3000/api/projects/<slug>/media/<assetId> \
  -H 'Content-Type: application/json' \
  -d '{"colorTag":"green"}'
```

This is the reliable path. `browser_console` fetch may fail if the browser is on `about:blank` or a different origin.

## Usage in browser_console (only when browser is on the project page)

```javascript
(async () => {
  const res = await fetch('http://<host>:3000/api/projects/<slug>/media/<assetId>', {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ colorTag: 'green' })
  });
  const data = await res.json();
  return JSON.stringify(data);
})()
```

## Tag management

```
POST /api/projects/:slug/media/:assetId/tags
```

Body (one of):
```json
{ "set": ["canonical-reference", "recurring", "hero-prop"] }
{ "add": ["new-tag"] }
{ "remove": ["old-tag"] }
```

Returns `{ ok: true, tags: [...] }`.

### "Approved and canonical" convention

When the user says "mark it approved and canonical" or similar, apply both:
1. `colorTag: "green"` via PATCH
2. Tags via POST tags endpoint: `{"set": ["canonical-reference", "recurring", "hero-prop"]}`

Adjust the tag set based on asset type:
- Reference images (locations, props): `canonical-reference`, `recurring`
- Hero props (typewriter, manuscript stack): add `hero-prop`
- Character sheets: `character-sheet`, `canonical-reference`
- Locations: `canonical-location`

## Batch tagging via curl

```bash
for id in asset_abc asset_def; do
  curl -s -X PATCH "http://<host>:3000/api/projects/<slug>/media/$id" \
    -H 'Content-Type: application/json' \
    -d '{"colorTag":"green"}'
done
```

## Verification

After tagging, confirm:

```bash
curl -s http://<host>:3000/api/projects/<slug>/media/<assetId> | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d['asset']['colorTag'], d['asset'].get('tags',[]))"
```
