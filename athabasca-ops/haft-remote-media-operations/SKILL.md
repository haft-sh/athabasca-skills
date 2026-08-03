---
name: haft-remote-media-operations
description: Operate Haft remote-only media registration against hosted targets, with real CLI/version verification, canary discipline, and UI-vs-catalog validation.
version: 1.0.0
---

# Haft remote media operations

Use this when registering or debugging **remote-only media** on a hosted Haft target such as `*.haft.sh`.

## When to use

- The user asks to upload/register an image or video to a hosted Haft vault without writing local bytes.
- You need to validate `POST /api/automation/v1/media-ingest` end to end.
- You need to explain why a supposedly successful remote-only upload is not visible in the current UI.
- You need to separate CLI drift, runtime drift, route-scope bugs, and product-surface browse gaps.
- The user asks to persist a Markdown plan, report, or other local text artifact into a configured remote Haft vault.

## Persisting a text document to a remote vault

Use the normal remote import path for a file-backed Markdown artifact; do **not** register it as remote-only media.

1. Write the document locally with an explicit title, intended vault path, and provenance.
2. Run `haft update --check --json`; when an update is available, update and verify `haft version --json` before a live remote import.
3. Verify `haft whoami --json` and `haft remotes --json`; confirm the remote advertises `import` readiness.
4. Import with a deliberate folder and duplicate policy:
   ```bash
   haft import /absolute/path/report.md --remote dev --target-folder plans/topic --on-duplicate clone --wait --json
   ```
5. Capture the returned batch/job ID, vault path, page handle, source hash, and indexed status.
6. Query the remote by title/path, then read it back through `haft get --handle ... --remote <slug> --json`. A local import success is not enough.

Use `clone` when preserving prior reports matters. Use overwrite only with explicit user instruction and the CLI's force guard.

## Core rules

1. **Use the authenticated Haft CLI for private Haft documents before trying the browser.** A public `dev.haft.sh` reader URL may show a secure-login page even when the configured `dev` remote has delegated agent-read access. Retrieve the indexed document through the configured remote instead:
   ```bash
   haft get 'https://dev.haft.sh/#/haft/plans/topic/document?view=rendered' --remote dev --json
   ```
   `haft get` accepts exactly one target (a reader URL, slug, or handle) plus `--remote`; do not pass the URL path and remote slug as separate positional arguments. Treat the indexed projection as the operational source for plans; use a browser only when visual/rendered fidelity itself matters.
2. **Update the installed Haft CLI first** when the task is a live CLI-backed canary or upload.
2. Treat **repo freshness**, **installed CLI freshness**, and **remote runtime freshness** as separate facts.
3. A successful remote-only upload is not proven until you verify:
   - HTTP success
   - artifact row exists in the destination catalog
   - `storage_state=remote-only`
   - canonical `source_url` is preserved
   - no local file was written
4. Do **not** assume the current Haft vault browser will surface a successful remote-only artifact. The browse shell is file-tree-oriented and may omit catalog-only remote-only artifacts from both **Library** and **Recently Imported**.

## Preferred workflow

1. **Verify and update the installed CLI**
   - Run `haft update --check --json`.
   - If a newer public release exists, update the installed CLI before the live upload.
   - Confirm the installed binary with `haft version --json`.
   - **CDN fallback:** `haft update` may 404 if the release CDN has moved (as of 2026-07-23, releases live at `releases.haft.sh`, not `media.haft.sh`). If `haft update` fails:
     1. `curl -s https://releases.haft.sh/releases/latest.json` → get version + sha256 for your target
     2. `curl -sL -o /tmp/haft-<ver> "https://releases.haft.sh/releases/v<ver>/haft-v<ver>-bun-linux-x64"`
     3. Verify sha256 matches the manifest
     4. `chmod +x /tmp/haft-<ver> && cp /tmp/haft-<ver> "$(which haft)"`
   - Alternatively, build from source: `cd <destination-repository> && git pull && bun run build && bun link` (note: `bun link` may not replace the embedded binary in PATH — verify with `haft version --json` after).

2. **Verify auth and remote readiness**
   - Run `haft whoami --json`.
   - Run `haft remotes --json`.
   - Confirm the intended remote advertises `import` / `automation.media.ingest` readiness before attempting upload.

3. **Choose the correct canary shape**
   - If the intended nested destination path is known-good, test it directly.
   - If nested-path scope is suspected broken, a root-prefix fallback (`destination.pathPrefix: ""`) is a valid way to prove that remote-only registration itself works.
   - Report the distinction precisely: transport works vs intended destination path still broken.

4. **Execute the remote-only upload**
   - Use a unique idempotency key.
   - Include canonical remote URL, MIME, size, digest, title, and bounded provenance.
   - Prefer one representative approved asset first.

5. **Verify destination state after upload**
   - Read back the catalog row on the destination.
   - Verify `storage_state=remote-only` and `source_url`.
   - Check likely filesystem paths and confirm no local file exists.

6. **If the user expects to see it in the UI, validate the product surface explicitly**
   - The current vault browser may only reflect `vaultFiles` / file-tree data.
   - A catalog-only remote-only artifact may not appear in **Recently Imported** or the **Library** tree even when the upload succeeded.
   - Explain whether the absence is a failed upload or a browse-surface gap.

## Interpreting outcomes

### Success shape
- API returns `200` with `status: ingested` or `status: replayed`
- destination catalog row exists
- `storage_state=remote-only`
- `source_url` preserved
- no local file written

### Common mismatch: success in catalog, missing in UI
If the upload succeeded but the user cannot find it in the vault browser:
- check whether the artifact is catalog-only and remote-only
- check whether there is any local file path at all
- explain that the current browser is file-tree-based, not a full artifact-catalog surface
- do not tell the user to keep drilling into folders if the item has no file-backed node to show

### Common mismatch: nested path fails, root path works
If `destination.pathPrefix: "athabasca/<project-slug>"` fails but `destination.pathPrefix: ""` works:
- classify this as a **route/path-scope bug**, not a generic upload failure
- preserve the evidence that remote-only ingest works while the intended path semantics do not

## Pitfalls

- **Do not rely on checkout freshness alone.** A fresh repo does not prove the installed `haft` binary is current.
- **Do not rely on CLI freshness alone.** Also verify the remote target runtime/build when possible.
- **Do not treat browser absence as upload failure** without verifying the destination catalog and filesystem.
- **Do not overstate path validation.** A root-prefix success does not validate the intended nested destination path.
- **Do not assume “Recently Imported” includes remote-only catalog artifacts.** In the current product shape, it may only reflect file-backed `vaultFiles`.

## Remote-only thumbnail repair: catalog truth is not enough

Hosted remote-only media may be stored in the `artifacts` catalog rather than the file-backed `assets` table. Before invoking `haft thumbnails audit --repair`, run the audit without repair and verify:

1. active remote-only image artifacts exist in `artifacts`;
2. the audit's `eligible` count is comparable to that image count;
3. the thumbnail publish target is configured and reports `ready`, not `disabled`;
4. thumbnail rows and queued jobs use the same source identity as the browser grid.

If remote-only images exist but the audit returns `eligible: 0`, **do not report an FFmpeg/CDN repair as complete or run bulk `--repair` as if it will work**. This is a catalog-only thumbnail lifecycle gap. Use a catalog-aware, idempotent backfill: transiently download originals, generate bounded derivatives, store them on the configured CDN target, persist verified thumbnail records keyed to the browser source identity, and validate every public URL. Never write remote-only original bytes into the vault merely to satisfy a legacy thumbnail worker.

Before mutation, verify the exact active service name and vault root—deployment defaults may be stale—then back up the catalog and prove one bounded canary before batches.

See `references/remote-only-thumbnail-lifecycle-gap.md`. For the premium HQ-managed thumbnail plus optimized-preview architecture, authorization boundary, and canary/backfill discipline, see `references/premium-hq-media-derivatives.md`.

## File-backed corpus repairs: browser truth, not catalog truth

For a hosted vault whose contents are repaired directly on disk or by an index/import workflow, do **not** call a collection live merely because Markdown files, the reader manifest, or the SQLite catalog contain it. The Explorer sidebar can retain a separate stale projection.

1. Verify the target files and their rendered Markdown locally/on-host.
2. Run the current runtime's index rebuild, then verify the bounded Explorer tree endpoint for the collection and expected direct-child count.
3. Open the exact artifact URL in a browser and inspect the rendered content, not only the navigation row.
4. If the catalog and Explorer disagree, rebuild the Explorer/catalog projection cleanly with a backup of the prior catalog artifacts; then recheck both the sidebar and exact document URL.
5. **Probe the same tree route that the UI uses.** A whole-tree route (for example `/api/vault/tree`) can be regenerated from current filesystem/catalog state while the paginated sidebar route (`/api/vault/tree/children?parent=&limit=…`) still reads stale `explorer.sqlite` rows. Compare their root entries and `treeVersion`; do not dismiss a fresh-user screenshot as browser cache until the bounded route agrees.
6. **Rebuild with the deployed runtime CLI and its active-vault configuration**, not an arbitrary source checkout. First run the deployed binary's `vault status --json` to learn its config path and active root, back up `.haft/index.sqlite` and `.haft/explorer.sqlite`, quiesce app/bridge services, run that binary's `index rebuild --vault <active-root>`, restart, and verify health plus the bounded sidebar endpoint. A source checkout may lack the configured active vault and silently fail or rebuild the wrong state.
7. For HTML/MOBI conversion, preserve visual block containers as prose paragraphs and reserve intentional line breaks for verse. Never flatten all HTML text nodes with `stripped_strings` and join them with blank lines: that splits inline italics and citations into unreadable fragments.

See `references/hosted-corpus-repair-and-browser-verification.md` for a concise reproduction and recovery checklist. For deterministic same-filesystem hierarchy moves, service quiescing, index rebuilds, and three-layer verification, see `references/file-backed-corpus-restructure-checklist.md`. For safe tree restructuring, source-corpus provenance, collision classification, and GPU-worker boundaries, see `references/corpus-structure-migration.md`.

## What to report back

When done, give the user:
- installed CLI version/commit used
- remote target identity/readiness used
- exact upload result
- artifact ID
- whether it is remote-only in the catalog
- whether any local file was written
- whether the current UI is expected to show it or not
- for file-backed corpus repairs: on-host file count, Explorer count, and exact browser-rendered artifact verification

## References

Add task-specific transcripts, product gaps, and canary evidence under `references/` when a session uncovers a reusable failure mode or UI mismatch.
