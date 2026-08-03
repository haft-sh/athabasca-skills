/**
 * Repair a broken image asset by overwriting its R2 keys and updating DB fields.
 *
 * Use when an asset's R2 object is missing/corrupt (404, 0 bytes, wrong content-type)
 * and you have a replacement image file. The PATCH /api/media/:assetId endpoint does
 * NOT update storage-related fields, so direct R2 + Drizzle writes are required.
 *
 * Usage:
 *   ASSET_ID=asset_xxx IMAGE_PATH=/path/to/image.png bun run scripts/repair-broken-asset.ts
 */

import { uploadFileToR2 } from "@/server/storage/r2";
import { db } from "@/server/db/client";
import { mediaAssets } from "@/server/db/schema";
import { eq } from "drizzle-orm";
import crypto from "node:crypto";
import fs from "node:fs";

const assetId = process.env.ASSET_ID;
const imagePath = process.env.IMAGE_PATH;

if (!assetId || !imagePath) {
  console.error("Usage: ASSET_ID=asset_xxx IMAGE_PATH=/path/to/image.png bun run scripts/repair-broken-asset.ts");
  process.exit(1);
}

// Read file and compute sha256
const fileBytes = fs.readFileSync(imagePath);
const sha256 = crypto.createHash("sha256").update(fileBytes).digest("hex");
const sizeBytes = fileBytes.byteLength;

// Lookup asset
const asset = await db.query.mediaAssets.findFirst({
  where: eq(mediaAssets.id, assetId),
});

if (!asset) {
  console.error("Asset not found:", assetId);
  process.exit(1);
}

console.log("Repairing asset:", {
  id: asset.id,
  storageKey: asset.storageKey,
  publicUrl: asset.publicUrl,
  currentContentType: asset.contentType,
  currentSizeBytes: asset.sizeBytes,
});

// 1. Overwrite the storageKey in R2
const storageResult = await uploadFileToR2({
  localPath: imagePath,
  key: asset.storageKey!,
  contentType: "image/png", // adjust per file; could detect from extension
});
console.log("Uploaded to storageKey:", storageResult);

// 2. Also upload to the publicUrl key if different (both may serve the asset)
const publicUrlKey = asset.publicUrl!.replace(/^https:\/\/[^/]+\//, "");
if (publicUrlKey && publicUrlKey !== asset.storageKey) {
  const publicResult = await uploadFileToR2({
    localPath: imagePath,
    key: publicUrlKey,
    contentType: "image/png",
  });
  console.log("Uploaded to publicUrl key:", publicResult);
}

// 3. Update DB fields that PATCH endpoint won't touch
const originalFilename = imagePath.split("/").pop() ?? null;
await db
  .update(mediaAssets)
  .set({
    kind: "image",
    contentType: "image/png", // adjust per file
    sizeBytes,
    sha256,
    originalFilename,
    updatedAt: new Date().toISOString(),
  })
  .where(eq(mediaAssets.id, assetId));

console.log("DB updated successfully");

// 4. Verify
const updated = await db.query.mediaAssets.findFirst({
  where: eq(mediaAssets.id, assetId),
});
console.log("Repaired asset:", JSON.stringify(updated, null, 2));
