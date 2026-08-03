# Automation media-ingest empty-prefix scope bug

Use this reference when a live remote-only media canary against a managed Haft remote behaves like an auth problem but is actually a route-level scope mismatch.

## Pattern

Observed on the project after the delegated-grant route wiring and JWKS issues were already resolved:

1. `haft whoami --json` succeeds.
2. `haft remotes --json` shows the remote as available and `remote-target.ready`.
3. Central grant exchange for `operations: ["import"]` succeeds.
4. The exchanged grant decodes to a payload with:
   - `operations: ["import"]`
   - `routeFamilies: ["automation"]`
   - `capabilities: ["artifact.import", "automation.media.ingest"]`
   - `pathPrefixes: [""]`
5. `POST /api/automation/v1/media-ingest` with `destination.pathPrefix: "athabasca/<project-slug>"` fails with:
   - HTTP `403`
   - `automation.auth.scope-denied`
6. The same request with `destination.pathPrefix: ""` succeeds.

## Interpretation

This combination strongly suggests:
- grant exchange is working
- destination verifier/JWKS path is working
- remote-only media registration itself is working
- the remaining defect is route-specific scope handling for empty path prefixes

The likely code smell is a mismatch between:
- `automation-import` scope logic, which treats an empty allowed prefix as root-allowed
- `automation-media-ingest` scope logic, which may fail to treat `""` as allowing nested paths

## Live canary discipline

Run these in order:

### A. Intended-path canary
Use the real desired destination path first, for example `athabasca/<project-slug>`.

If it fails with `automation.auth.scope-denied`, do **not** immediately collapse the diagnosis into generic auth failure.

### B. Root-prefix fallback canary
Retry the same remote-only canary with:
- same remote
- same source URL
- same metadata
- new idempotency key
- `destination.pathPrefix: ""`

If that succeeds, classify the outcome precisely:
- remote-only ingest works live
- nested-path media-ingest scoping is still buggy

## What to verify on success

Do not stop at HTTP 200. Verify all of:

1. artifact row exists in the destination catalog
2. `storage_state = remote-only`
3. canonical `source_url` is preserved
4. metadata/provenance is preserved
5. no local file exists under likely vault asset paths
6. rerunning the same idempotency key returns `status: replayed`

## Suggested user-facing wording

Preferred wording:

> Remote-only ingest works live on the destination, but the intended nested media path is still blocked by a route-level scope bug. The fallback root-prefix canary proves registration, metadata preservation, and no-local-file behavior; it does not prove the intended `athabasca/<slug>` destination path is fixed.

Avoid saying:
- "auth is broken" when root-prefix fallback proves grant verification is fine
- "migration is complete" when the intended nested path still fails
- "JWKS issue" unless verifier diagnostics actually show JWKS/signature errors

## Follow-up code fix target

Patch `automation-media-ingest` scope handling to match `automation-import` semantics for empty allowed path prefixes, then rerun the original nested-path canary.
