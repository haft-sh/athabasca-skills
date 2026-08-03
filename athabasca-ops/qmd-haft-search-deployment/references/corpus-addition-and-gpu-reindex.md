# Corpus additions with private GPU QMD reindexing

Use this when adding an approved, bounded set of new Markdown books/pages to a live Haft vault whose semantic provider uses a private persistent QMD daemon.

## Safety model

- Treat source staging, canonical-vault mutation, catalog/Explorer rebuild, GPU index update, and freshness reconciliation as separate gates.
- Keep public semantic routing truthfully degraded until the new catalog and QMD index are both certified. Do not clear an “updating” UI state manually.
- Never bulk-copy an upstream repo into the canonical vault. Copy only an allowlisted, preflighted directory set.

## Import procedure

1. Pin source repo commit, archive checksum, license, exact allowlisted book directories, and per-directory file counts.
2. Stage pages outside the live vault. Generate the metadata/navigation shape required by the target reader, including immutable provenance fields: repository, commit, upstream path, license, and source-content SHA-256.
3. Assert target directories are absent and existing canonical books are excluded. Verify page count and every staged Markdown page’s metadata before transfer.
4. Transfer the staged bundle with an archive checksum, then verify it again on the target before mutation.
5. Stop the public service only for the short copy/rebuild window. Run copy and `haft index rebuild` as the runtime service account, not root. Root-owned Explorer SQLite/WAL/SHM files make the UI report that the Explorer projection is unavailable.
6. Verify three layers after restart: filesystem counts, catalog page count, and public tree children/root endpoint.

## Persistent-daemon QMD pitfalls

- An interactive shell’s default QMD config/cache can be an empty smoke index even while the live daemon serves the full index.
- Identify the active index from the actual systemd daemon before issuing `qmd update` or embedding work: inspect its effective environment, service user, working directory, and open SQLite file descriptors under `/proc/<pid>/fd`.
- Invoke QMD with the daemon’s exact configuration and cache/index context. Do not initialize, remove, or update a collection through a default shell context just because it shares the same collection name.
- Before incremental embedding, stage the exact canonical added files onto the GPU collection root and compare exact case-sensitive relative paths. Preserve old index data and use a resumable, bounded embedding process.

## Certification after content additions

1. Generate the new semantic rebuild manifest.
2. Require exact identity/source/content comparison for old vs new corpus; additions must be the approved paths only, with no modified preexisting documents.
3. Require `eligible = indexed = mapped`, with `unmapped = pending = 0`.
4. Restart and warm the private QMD daemon/provider, then perform a BBT-originated provider canary.
5. Reconcile Haft freshness only with verified counts and current index revision. Finally verify a real public semantic request returns `effectiveMode: semantic`, `semantic.state: used`, and non-empty mapped results.

## Operator communication

For long catalog and GPU builds, report verified milestones: staged, copied, catalog/tree verified, GPU update started, embedding completed, semantic reconciliation completed. State plainly when semantic UI fallback is expected rather than implying automatic indexing.
