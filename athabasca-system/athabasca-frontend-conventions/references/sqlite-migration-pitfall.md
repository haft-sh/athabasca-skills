# SQLite Migration Pitfall: `db:push` Can Wipe Data

**Date:** 2026-05-29
**Context:** Media ratings/color-tags schema migration on Athabasca

## The Problem

Adding a `CHECK` constraint to an existing SQLite table via `bun run db:push` triggers Drizzle-kit to perform a **full table rebuild** (DROP + CREATE + INSERT). SQLite does not support `ALTER TABLE ADD CONSTRAINT`, so drizzle-kit generates:

```sql
DELETE FROM media_assets;           -- ← DATA LOST HERE
CREATE TABLE __new_media_assets (...);
DROP TABLE media_assets;
ALTER TABLE __new_media_assets RENAME TO media_assets;
```

There is **no `INSERT INTO __new SELECT * FROM media_assets`** between the DELETE and the rebuild. The data is gone.

## The Fix

For new columns that can be nullable or have a default, use **`ALTER TABLE` at runtime** instead of `db:push`. Add the migration functions to `src/server/db/client.ts` following the existing pattern (`ensureWorkflowColumns`, `ensureShotPromptColumns`, etc.):

```typescript
async function ensureRatingAndColorColumns() {
  if (!(await tableExists("media_assets"))) return;

  const result = await client.execute("PRAGMA table_info(media_assets)");
  const columnNames = new Set(result.rows.map(r => String((r as Record<string, unknown>).name)));

  if (!columnNames.has("rating_stars")) {
    await client.execute("ALTER TABLE media_assets ADD COLUMN rating_stars INTEGER NOT NULL DEFAULT 0");
  }
  if (!columnNames.has("color_tag")) {
    await client.execute("ALTER TABLE media_assets ADD COLUMN color_tag TEXT");
  }
  await client.execute("UPDATE media_assets SET rating_stars = COALESCE(rating_stars, 0)");
}

async function ensureMediaAssetTagsTable() {
  await client.execute(`CREATE TABLE IF NOT EXISTS media_asset_tags (...);`);
  await client.execute("CREATE INDEX IF NOT EXISTS media_asset_tags_asset_idx ON media_asset_tags (asset_id)");
}

// Call at the bottom of client.ts:
await ensureRatingAndColorColumns();
await ensureMediaAssetTagsTable();
```

## When `db:push` IS Safe

- New tables (no existing data to preserve)
- Adding indexes (pure metadata, no table rebuild)
- Column additions where the schema change does NOT include constraints that SQLite can't ALTER

## When `db:push` Is DANGEROUS

- Adding `CHECK` constraints to existing tables
- Changing column types (triggers rebuild)
- Adding `NOT NULL` without a default to tables with existing rows

## Recovery

Always keep a backup before pushing:
```bash
bun run db:backup    # writes data/backups/athabasca-<timestamp>.db
```

To restore:
```bash
cp data/backups/athabasca-<latest>.db data/athabasca.db
```
