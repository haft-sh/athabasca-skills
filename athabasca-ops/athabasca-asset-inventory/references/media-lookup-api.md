# Media Lookup API Reference

Verified endpoint for finding HTML documents attached to a project.

## Primary endpoint

```
GET /api/projects/{slug}/media
```

Query parameters (all optional):

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `phase` | string | — | Filter by phase tag, e.g. `storyboard` |
| `sortBy` | `createdAt` \| `ratingStars` | `createdAt` | |
| `sortOrder` | `asc` \| `desc` | `desc` | Newest first |
| `minRating` | integer | — | 0–5 filter |
| `maxRating` | integer | — | 0–5 filter |
| `colorTag` | string | — | `green`, `yellow`, `red`, `blue`, `purple` |

## Response envelope

```json
{ "ok": true, "assets": [...] }
```

Access `data.assets`, not `data` directly — the envelope is always wrapped.

## Asset fields for document discovery

| Field | Use |
|---|---|
| `contentType` | `"text/html"` for shot breakdowns |
| `title` | Full text title — filter with keyword matching |
| `publicUrl` | Direct download URL |
| `createdAt` | ISO timestamp — use as tie-break when multiple candidates match |
| `tags` | Phase/workflow tags applied to the asset (e.g. `"storyboard"`) |

## No title-filter endpoint exists

There is no `GET /api/projects/:slug/media?title=...`. Fetch all assets and filter client-side:

```bash
curl -s "http://localhost:3000/api/projects/{slug}/media?sortBy=createdAt&sortOrder=desc" \
  | jq '.assets[] | {title, contentType, publicUrl, createdAt}'
```

## Title keyword matching

For shot breakdowns, filter where `contentType === "text/html"` and `title` contains:

| User reference | Keywords |
|---|---|
| "canonical shot list" | `"shot"` + (`"breakdown"` \| `"list"` \| `"canonical"`) |
| "v2 script" | `"v2"` + (`"script"` \| `"shot"`) |
| "our shot breakdown" | `"shot"` + (`"breakdown"` \| `"list"`) |
| generic document | `"shot"` + `"breakdown"` |

Prefer the candidate with the most keyword matches; tie-break by `createdAt` desc.

## What is NOT in this table

- `media_assets` does NOT store per-shot rows. Individual shot fields (shot number, scene heading, description, sequence, character names) are not DB columns — they exist only in the content of user-supplied documents.
- There is no `/api/projects/{slug}/storyboard/shots` endpoint.
- There is no `/api/projects/{slug}/script` endpoint that returns structured shot data.
- Shot breakdowns are always user-supplied text parsed from an HTML document.
