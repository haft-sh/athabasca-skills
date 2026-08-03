# Managed remote folder-import chunking after reenrollment

Use this note when a managed Haft remote has been repaired to `remote-target.ready`, a single-file canary succeeds, but the first full document import still fails.

## Observed live pattern on the project

After the new `<remote-host>` instance was fixed:

- `haft remotes --json` showed the target as `ready`
- allowed operations included `import`
- a single-file Markdown canary imported successfully with `haft import ./file.md --remote the project --target-folder ... --wait --json`
- but the bundle command

```bash
haft import /path/to/docs-dir --remote the project --target-folder athabasca/<project-slug> --recursive --wait --json
```

failed with:

```text
automation.import.invalid-request: Automation import request must match the v1 JSON contract.
```

## Practical interpretation

Do not treat that failure as proof that the remote or grant exchange is still broken.

If the one-file canary already succeeded, the managed remote path is alive. The problem is more likely the CLI's directory-to-remote request shape for this route, not enrollment or verifier readiness.

## Working recovery

1. Keep the successful one-file canary as the auth/readiness proof.
2. Stop retrying the same recursive directory import unchanged.
3. Enumerate the actual files under the docs bundle.
4. Import **explicit file lists** instead of the directory root.
5. Split the batch into deterministic chunks.
6. Keep target folders explicit per subgroup.

the project worked with this shape:

- top-level docs as a small explicit file list
- living docs as a small explicit file list
- media-document Markdown files split into two explicit chunks

## Why this matters

A remote import route can be healthy while one CLI payload shape is not. Avoid collapsing these into one diagnosis.

Say:
- managed remote is ready
- single-file remote import works
- recursive directory payload is rejected by the automation import contract
- explicit file-list chunking succeeds

Do **not** say:
- reenrollment failed
- grant exchange is broken
- the destination is not import-capable

when the canary already disproved those claims.

## Reuse rule

When a repaired managed remote accepts one-file imports but rejects a recursive folder import, switch immediately to explicit file-list chunking and continue the migration instead of reopening auth debugging.
