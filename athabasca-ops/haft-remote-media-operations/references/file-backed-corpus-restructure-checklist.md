# File-backed corpus restructuring checklist

Use this when reorganizing a large hosted Haft vault on disk while retaining the reader/catalog experience.

## Safe sequence

1. **Preflight a deterministic move map.** For every source → destination pair, verify source exists, destination does not, and record Markdown-file counts. Store the forward map; it is also the rollback map in reverse.
2. **Back up derived state, not necessarily all content.** Copy the manifest and index/Explorer SQLite files to an operator-accessible backup location. Same-filesystem directory renames are reversible; avoid needlessly duplicating a very large vault when a content backup already exists.
3. **Quiesce writers/readers that hold catalog state.** Stop the application service and any indexing/bridge worker that could read or write the catalog during the move.
4. **Make only same-filesystem renames.** Create destination parents, perform the planned moves, and fail closed if the live filesystem no longer matches the preflight.
5. **Rebuild with the deployed runtime's active-vault command.** Do not hand-edit catalog SQLite files. First run the deployed CLI's vault-status command to identify its configured active vault. Invoke the same release binary used by the service—not a scratch checkout whose local configuration may have no active vault. Back up both `.haft/index.sqlite` and `.haft/explorer.sqlite`, rebuild, then restart the bridge and application services.
6. **Verify every projection the reader actually uses.**
   - on-disk: expected folder names and file counts;
   - full-tree API: `/api/vault/tree` has the intended hierarchy;
   - paginated Explorer API: `/api/vault/tree/children?parent=&limit=100` has the same root names and no retired paths. Reader UIs commonly load this projection from `explorer.sqlite`, not the full-tree response;
   - compare `treeVersion` between full-tree and paginated responses. A mismatch exposes stale derived projection state even when filesystem and full-tree checks pass;
   - reader: a known exact document URL renders after restart.
7. **Batch imports around the restructure.** Use a bounded canary collection first, verify it in the tree, then complete the bulk import and run a final rebuild. Do not rebuild after every individual file.

## Root-level cleanup: distinguish user-facing clutter from vault contract state

A root folder that appears empty in the Explorer is not automatically safe to delete. Some Haft vault layouts use otherwise-empty root directories as active-vault or runtime markers. Removing one can restart the app into onboarding mode even when the corpus and catalog SQLite files remain intact.

1. Compare the live tree API with the filesystem first. If the canonical hierarchy is already correct in the API, a screenshot may reflect stale client state rather than a corpus migration problem.
2. Before removing any empty root directory, inspect the vault contract/configuration; do not infer safety from an empty `find` result.
3. If the goal is a cleaner Library root, prefer a server-owned Explorer visibility/filter rule for structural directories over deleting contract directories.
4. If a cleanup changes boot state, restore the directory immediately, restart the service, then verify a `Vault mounted` log plus public `/api/app/status` and `/api/vault/tree` recovery.

## Pitfalls

- A reader manifest or filesystem count alone does not prove the Explorer projection is correct.
- **Do not delete an empty root directory solely because it is user-facing clutter.** It may be a vault-contract marker; solve presentation in the Explorer layer instead.
- A source collection may already be present under a legacy/unexpected path. Confirm on disk before re-importing it; otherwise duplicates are likely.
- Directory moves can change reader slugs. Decide whether legacy aliases/redirects are needed before the migration.
- Stop/start windows can yield short-lived public 502s while the app remounts the vault. Do not classify that as a persistent outage until the service is ready and a fresh request still fails.
