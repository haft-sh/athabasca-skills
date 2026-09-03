# Composite Reference Asset Workflow

## When to use

When you need a new canonical character reference that combines elements from multiple existing assets (e.g., a character in a specific outfit with specific footwear), and the resulting composite should be used as a Seedance/image-to-video reference.

## Workflow

### 1. Generate composite image locally

Use `image_generate` with:
- `image_url` = primary identity reference (controls face, proportions, pose)
- `reference_image_urls` = additional references (controls footwear, props, costume details)
- Prompt describing the exact composite desired

Save result to local cache.

### 2. Upload to R2

Use the upload script from the main Athabasca repo:

```bash
cd /home/nrsimha/Sites/athabasca
bun run scripts/upload-to-r2.ts /path/to/local/image.png --key "gly/generated/descriptive-name.png"
```

Returns a permanent `publicUrl` on `media.wheretoaccess.com`.

### 3. Register as Athabasca media asset

```text
POST /api/projects/:slug/media
```

```json
{
  "kind": "image",
  "category": "generated",
  "sourceKind": "generated",
  "sourceUrl": "https://media.wheretoaccess.com/gly/generated/descriptive-name.png",
  "storageKey": "gly/generated/descriptive-name.png",
  "storageProvider": "r2",
  "title": "Descriptive Title — Canonical Reference",
  "originalFilename": "descriptive-name.png",
  "sizeBytes": 1234567
}
```

**Important**: use `sourceUrl`, not `publicUrl` in the request body. The API requires exactly one of `file` or `sourceUrl`.

### 4. Use in video generation

Use the returned `asset.publicUrl` as a `referenceImageUrls` entry:

```json
{
  "referenceImageUrls": [
    "https://media.wheretoaccess.com/gly/generated/descriptive-name.png",
    "...other references..."
  ]
}
```

## Pitfalls

- The `POST /api/media` route returns 404. Use `POST /api/projects/:slug/media` instead.
- The `category` field accepts: `research`, `moodboard`, `generated`, `inbox`, `misc`. Use `generated` for AI-created reference images.
- The `sha256` field is optional and can be `"none"` if you don't have the hash handy.
- The upload script (`bun run scripts/upload-to-r2.ts`) runs from the main Athabasca repo directory, not the cliphouse worktree.
