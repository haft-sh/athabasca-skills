# Repairing Broken Image Assets

## When to use

An image asset in Athabasca is broken when:
- The R2 object returns 404 at its `publicUrl`
- The asset has `sizeBytes: 0` or a mismatched `contentType` (e.g. `text/uri-list` for an image)
- The `storageKey` and `publicUrl` point to different R2 keys, and one or both are missing

## Why PATCH doesn't work

`PATCH /api/projects/:slug/media/:assetId` only updates metadata fields:
- ✅ `title`, `provenanceNote`, `metadataJson`, `ratingStars`, `colorTag`, `tags`, `sourceKind`
- ❌ `storageKey`, `publicUrl`, `contentType`, `sizeBytes`, `sha256`, `kind`, `originalFilename`

## Repair procedure

Use the `scripts/repair-broken-asset.ts` script from the athabasca repo root:

```bash
ASSET_ID=asset_xxx IMAGE_PATH=/path/to/replacement.png bun run scripts/repair-broken-asset.ts
```

The script:
1. Reads the replacement image and computes sha256 + size
2. Uploads to the asset's existing `storageKey` (overwrites in place)
3. Also uploads to the key extracted from `publicUrl` if different (both paths may serve the asset)
4. Updates DB fields via Drizzle (`contentType`, `sizeBytes`, `sha256`, `originalFilename`, `kind`)
5. Verifies the repaired asset

## Manual alternative (without script)

```typescript
import { uploadFileToR2 } from "@/server/storage/r2";
import { db } from "@/server/db/client";
import { mediaAssets } from "@/server/db/schema";
import { eq } from "drizzle-orm";

// Overwrite R2 at the existing key
await uploadFileToR2({ localPath: "/path/to/image.png", key: "existing/key.png", contentType: "image/png" });

// Update DB
await db.update(mediaAssets).set({
  contentType: "image/png", sizeBytes: 12345, sha256: "...", kind: "image"
}).where(eq(mediaAssets.id, "asset_xxx"));
```

## After repair

- Verify the `publicUrl` returns 200 with correct content-type
- Delete any duplicate assets created during attempted re-uploads
- The asset retains its original `id`, `attachments`, and `createdAt`
