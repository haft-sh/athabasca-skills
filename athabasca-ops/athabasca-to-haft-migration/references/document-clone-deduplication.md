# Safe document-clone deduplication

Use this when an imported document vault contains collision-created filenames such as `chapter-1.md`, `chapter-1-2.md`, and `chapter-1-3.md`.

## Why it happens

Haft import defaults to `--on-duplicate clone`. Re-running an import therefore preserves an existing document and adds an incremented sibling. These are import collisions, not version history.

## Safe cleanup contract

1. **Inventory from the active served vault**, not a staging/source folder.
2. Treat a candidate as a clone only when:
   - its basename ends in `-N` for `N >= 2` before the extension;
   - the corresponding unsuffixed canonical sibling exists; and
   - SHA-256 of both file bytes is identical.
3. Write a durable JSON/NDJSON audit manifest *before* deletion, listing canonical path, clone path, and both hashes.
4. Block deletion if any candidate differs by hash or if the live count differs from the reviewed count.
5. Stop the index-writing/server service before mutation when its catalog uses SQLite or may hold write locks.
6. Delete only audit-approved clone paths. Do not overwrite canonical files.
7. Rebuild the index, restart the exact service, and run a second zero-clone hash audit.
8. Verify local health, public hostname health, ready/indexed state, and the expected page-count delta.

## Expected accounting

If every clone is a one-for-one duplicate:

```text
post-cleanup pages = pre-cleanup pages - deleted identical clones
```

Require this equation to reconcile alongside an operational public readback.

## Prevention

For repeat imports where existing canonical content should win, use:

```bash
haft import <source> --on-duplicate skip
```

Use `overwrite` only for an explicit update operation with a reviewed source and the CLI's overwrite guard. Do not leave a recurring canonical ingestion on the default `clone` policy.
