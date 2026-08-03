---
name: athabasca-to-haft-migration
description: Migrate Athabasca project content into a Haft vault or remote Haft site while preserving remote-only media policies and generating import-safe document bundles.
version: 1.0.0
---

# Athabasca to Haft migration

Use this when moving a project's content from Athabasca into Haft, especially when the target wants **documents imported locally** but **images/videos left as remote-only references**.

## When to use

- A user wants to migrate an Athabasca project into a Haft vault or `*.haft.sh` site.
- The source of truth is Athabasca's live API, not just repo content.
- The destination has a mixed storage policy:
  - documents may exist locally and/or remotely
  - binary media should stay remote-only
- Haft docs are incomplete, so the workflow must be validated against the live codebase and importer behavior.

## Core rule

Do **not** force binary media through Haft's normal local-first import path when the user explicitly wants remote-only storage. Prefer first-class remote-only artifact registration when the live runtime supports it; otherwise stage a **manifest of remote references** and report the lane as incomplete.

## Recommended workflow

1. **Pull live Athabasca project data first**
   - Fetch project metadata.
   - Fetch project media inventory.
   - Fetch living-doc summaries and individual living-doc snapshots.
   - Treat live API responses as source of truth over stale local content.

2. **Separate content into two lanes**
   - **Document lane**: markdown, HTML, living docs, inventories, prompt previews, shot lists.
   - **Binary media lane**: images and videos.

3. **For the binary media lane, preserve remote-only semantics**
   - Record Athabasca asset ID, title, kind, category, SHA, content type, byte size, source timestamps, labels/ratings, storage key, and public URL.
   - Emit a machine-readable manifest (`json` and optionally `ndjson/csv`).
   - Probe the current Haft API/runtime for first-class remote-only registration; do not rely on an older migration note that says the feature is absent.
   - When supported, register each asset with `storage_state=remote-only`, canonical `source_url`, digest, stable source identity, and bounded provenance—without fetching or writing binary bytes.
   - When not supported, generate a human-readable index page that links to the remote URLs and report the media lane as staged rather than complete.
   - Do **not** download/import image or video bytes into Haft just to make the importer happy.
   - See `references/remote-only-media-registration.md` for the contract, metadata map, idempotency rules, and canary checklist.

4. **For the document lane, generate an import-safe bundle**
   - Download markdown sources as markdown.
   - Preserve raw HTML snapshots in the migration bundle.
   - Also generate **markdown mirror files** for HTML sources so Haft can import them even when raw HTML normalization rejects the source as unsafe.
   - Include provenance in each mirror document: source kind, source ID, source URL when available, and raw HTML bundle path.

5. **Choose a safe Haft target folder**
   - Avoid import target folders containing reserved/internal segments like `imports`, `manifest`, or `exports`.
   - Prefer ordinary content paths such as `athabasca/<slug>`.

6. **Dry-run locally before remote import**
   - Import the docs bundle into a scratch/local Haft vault first.
   - Verify imported file count and inspect a few generated documents.
   - Only after local verification should you attempt the authenticated remote import.

### Set duplicate semantics deliberately

- Haft import defaults to `--on-duplicate clone`. A repeated import creates collision suffixes such as `verse.md`, `verse-2.md`, and `verse-3.md`; these are import clones, **not** document revisions.
- For canonical, rerunnable source collections, use `--on-duplicate skip` so identical reruns cannot silently proliferate files. Use guarded overwrite only when an intentional source update has been reviewed.
- Before cleanup, inventory every canonical/suffixed set and compare content hashes. Retain exactly one canonical unsuffixed path only when the copies are byte-identical; a suffix copy with different content or provenance requires review rather than deletion.
- Do not report a cleanup as complete until the target is authorized, the post-mutation inventory is read back, and a before/after count is captured.
- For the full hash-manifest, service-stop, index-rebuild, and public-readback sequence, see `references/document-clone-deduplication.md`.

### Audit source-library completeness before calling a migration complete

When a source corpus includes ebooks, archives, or other compound source files, imported page count alone is weak evidence. Perform a read-only completeness audit before bulk repair:

1. Inventory the source files, exclude packaging artifacts, hash each source, and map each source to its intended destination collection. Identify duplicate source editions that intentionally map to one collection.
2. Compare source and destination at two levels: **structural coverage** (collection/chapter/section markers) and **content volume** (normalized word or character counts). Different import granularities are normal; a sharp volume deficit or a source table-of-contents with absent destination chapters is not.
3. Check the current deployed vault after clone cleanup. A path with few documents may be complete-but-flattened; inspect document word counts and headings before claiming content loss.
4. Repair only against a verified canonical source. Preserve the pre-repair folder or snapshot, stage the replacement, stop the index service, install/rebuild, restart, then verify local file counts plus the public reader manifest.
5. If the local source itself is incomplete or corrupt, do not silently substitute an external edition. Obtain explicit approval, pin the external source to an immutable revision, add a provenance document inside the destination collection, and report the edition distinction.
6. Publish an audit/addendum that distinguishes: source defects, extraction/segmentation defects, genuine omitted collections, repairs performed, and any source-policy decision.

See `references/corpus-completeness-audit.md` for the evidence model, repair boundaries, and a representative ebook-corpus case.

7. **Preflight the actual hosted destination before remote execution**
   - Resolve the intended custom hostname and identify its backing instance, service unit, and binary path.
   - Compare the hostname with every `apiOrigin` returned by `haft remotes --json`; a label such as `dev` is not proof that the remote is the intended custom-domain host.
   - Capture `haft version`, binary SHA-256, service start time, and local/public health.
   - Compare the deployed build with both the latest **published release** (`haft update --check --json`) and the current repository default branch; these can differ and must be reported separately.
   - Confirm the destination is centrally enrolled and its HQ server/vault claims correspond to its persisted local host identity before enabling delegated-grant verification.

8. **Remote execution once auth is available — canary first**
   - For a newly merged enrollment or automation feature, verify three independently deployed surfaces before dogfood: the operator CLI, Haft HQ, and the destination binary. A current local CLI alone does not make the protocol compatible end to end.
   - For every newly added managed automation endpoint, verify exact-route delegated-grant wiring—not just capability advertisement. The destination grant map must bind the endpoint's method/path to the intended operation, route family, and capability, and an integration test must call that exact route with an exchanged grant. Treat `auth.central-grant.route-unsupported` as a route-map failure before the handler, not as an import-payload failure.
   - Distinguish `origin/master`, the installed CLI, and the public release manifest. If the merged command is not yet in the published release, compile and install the current clean master build for operator testing, but do not use `haft update` if it would downgrade to an older published release.
   - Treat **local checkout freshness** and **installed CLI freshness** as separate checks. Pull the local Haft checkout first, preserving any uncommitted work safely, then update or rebuild the installed CLI and verify both identities explicitly.
   - Prefer the **CLI path first** for migration/auth work. Use browser navigation only when you specifically need browser-only evidence such as a rendered artifact check, a product-surface login verification, or UI-only settings. Do not substitute browser login for missing CLI remote capability without stating that the migration path is still CLI-blocked.
   - If the hosted destination is a **new instance** and `haft remotes --json` shows that the matching hostname advertises only `status` (for example `projection-expired` or `destination-verifier-not-ready`), classify the managed CLI path as blocked before retrying imports. In that state, a browser-authenticated import can be a fallback for the **document lane only**; it does not validate or complete the remote-only media lane.
   - Complete destination preparation and compatibility checks before requesting a short-lived OTP. Requesting OTP too early creates avoidable expiry and interruption; authentication should be the last just-in-time prerequisite before enrollment mutation.
   - For hosted browser OTP login, request the code only after the six-digit code-entry screen is visible and you are ready to submit immediately. If the page returns to the email form or you request another code, treat all earlier six-digit codes as invalidated by the new challenge and ask for the newest code only.

   - Transfer pairing invitations through a private, short-lived channel without printing their contents, preserve mode `0600`, and delete intermediary copies. When a stage proof is consumed, issue a fresh invitation and resume the same authoritative enrollment rather than creating parallel claims.
   - Stage `HAFT_CENTRAL_API_BASE_URL` and an absolute `HAFT_CENTRAL_JWKS_PATH` before pairing finalization. Enable `HAFT_CENTRAL_GRANTS_ENABLED=true` only after identity/JWKS installation, restart the exact destination service, and resume enrollment.
   - Verify the CLI identity and inspect configured central remotes before assuming the destination slug matches its public custom domain.
   - Match the canary to the behavior being validated. If the migration requires HTML fidelity or HTML normalization, import the **raw `.html` source** into a disposable path such as `athabasca/<slug>-html-sanity-check`. A Markdown mirror is a separate fallback lane and does not validate HTML.
   - Use `--wait` and structured output. Treat a successful local import as necessary but insufficient: verify the remote job, read the artifact back, and visually inspect rendering on the destination site before any batch import.
   - If the documents already migrated but the **assets lane is empty**, do not assume the remote-only media policy worked. Run a separate **single-asset media canary** against the actual asset path or registration flow before any bulk image/video attempt.
   - For a media canary, prefer one approved/green image, download and verify the source bytes first (content type, size, checksum if available), then test only that asset. A successful document import does not validate asset migration.
   - If both lanes matter, test them separately: (a) one normalized raw HTML artifact and (b) one import-safe Markdown mirror. Never describe Markdown success as HTML validation.
   - If the raw HTML canary fails, stop before batch upload. Fix the importer or obtain an explicit user decision to use Markdown mirrors; do not silently substitute mirrors.
   - Only after the raw HTML canary is readable and renderable should you import the complete document bundle.
   - Respect the remote automation contract’s batch limit. Current Haft automation imports accept at most 25 files per request; split larger folders into deterministic chunks and verify every batch count.
   - If a managed remote is `ready` and a one-file canary import succeeds, but `haft import <directory> --remote ... --recursive` fails with `automation.import.invalid-request`, do not reopen enrollment/auth debugging first. Treat that as a likely directory-payload/CLI-shape problem for the automation import contract and switch to **explicit file-list chunking** by subgroup and target folder. See `references/managed-remote-folder-import-chunking.md`.
   - Keep the remote-media manifest alongside the imported docs as the replayable batch source and audit artifact even when first-class remote-only registration is available.

## Pitfalls

### Raw HTML normalization must be tested as raw HTML

If Haft reports that uploaded HTML could not be normalized into a safe import artifact:

1. Stop the batch; confirm the failed request reached document normalization rather than auth or route gating.
2. Inspect the actual unsafe issue. Athabasca living documents may embed inert machine-readable manifests such as `<script type="application/athabasca+json">`; these are data, not executable JavaScript. A safe importer may allow `application/json` and `application/*+json` scripts only when they have no `src` or event-handler attributes, then omit the manifest payload from normalized reader content while retaining the original source snapshot.
3. Keep executable scripts, script `src`, event handlers, JavaScript URLs, forms, frames, and active embeds fail-closed.
4. Add a regression test using a representative inert-manifest fixture and retain a negative executable-script test.
5. Retest the same raw HTML remotely and visually inspect it. Only then authorize the HTML batch.
6. Keep Markdown mirrors available as an explicit fallback, but use them only after the user chooses that tradeoff. A mirror import is not an HTML fix and must not be reported as HTML validation.

### Haft import target-folder policy is stricter than it looks

Haft rejects target folders containing internal/generated scaffold names such as `imports`, `manifest`, and `exports`. If an import inexplicably skips every file, inspect the target folder policy before assuming the content is bad.

### Remote auth failures must be classified before debugging document normalization

A remote canary can fail before the importer sees the document. Keep these layers separate:

- `document_upload_invalid_html` or equivalent normalization errors are content/importer failures.
- `route.gate-denied` with a delegated-grant diagnostic such as `auth.central-grant.bad-signature`, `jwks-stale`, or `schema-invalid` is destination/HQ trust configuration; retrying different documents will not test HTML.
- Verify whether the mutation created a job or artifact. If authorization failed at the route gate, report that no remote artifact was created and stop before batch import.
- Do not treat a valid CLI identity, advertised capabilities, or HQ-projected readiness as proof that the destination can verify the exchanged target-bound grant. The canary import itself is the authorization proof.
- Prefer destination redeploy/trust-anchor reconciliation for signature diagnostics rather than repeated login/import attempts. Re-authenticate only after the verifier path is healthy or the session expires.

### Projection and JWKS freshness can regress after successful enrollment

Enrollment readiness is a point-in-time proof, not permanent write or browser-login readiness.

- Recheck `haft remotes --json` immediately before a canary or batch. If the target advertises only `status` with `projection-expired`, do not attempt upload.
- If browser login reports `auth.claim.revoked`, inspect the persisted claim components and projection expiry before initiating claim recovery or ownership transfer. Haft can fail closed on an **expired projection** while the top-level, server, and vault claims all remain active; some UI/status surfaces mislabel that condition as revocation.
- Refresh and install the signed projection **and** current public JWKS together. Refreshing only the projection can leave the verifier rejecting newly signed grants with `auth.central-grant.bad-signature`.
- A reviewed emergency refresh must verify the signed projection against the **fresh HQ JWKS**, exact server/vault/account/team fingerprints and IDs, expected access grant, freshness, and monotonic projection version before atomically replacing local auth state. Back up the prior mode-0600 state first; never copy unverified payload fields into it.
- Restart the exact destination service when verifier/JWKS runtime state changed, then verify the real login or import route—not only public health.
- Do not hand-edit completed enrollment journals to force refresh. Prefer a supported destination refresh command; if none exists, call out the product gap and keep any reviewed recovery narrowly scoped.
- Short projection TTLs can expire during login or multi-batch imports. A manual refresh is only temporary; refresh immediately before bounded work, verify expiry headroom, and treat automatic destination-side renewal as the durable product fix.

See `references/raw-html-canary-and-projection-freshness.md` for diagnosis, cryptographic verification gates, and recovery boundaries.

### `remote add` is not managed enrollment

Keep these paths distinct when preparing a hosted destination:

- `haft remote add <slug> --url <url> (--token-env ... | --token-stdin)` stores a **manual client-side remote record** and references caller-supplied bearer material. It assumes the destination and credential already exist.
- Managed enrollment is a distributed provisioning operation: create/recover HQ server and vault claims, persist authoritative local host identity, install current public JWKS, enable the verifier, create least-privilege access grants, and prove a target-bound grant exchange.
- A successful `remote add` must never be reported as central enrollment, and enrollment must not silently fall back to a manual bearer.
- For product design, keep the verbs distinct (`remote add` versus `remote enroll`) because enrollment has broader authority, resumability, rollback, and destination-side effects.

### Pre-Epic hosted destinations need managed enrollment, not just a new binary

An older destination can have a healthy local `auth-state.json` with `source=local-bootstrap` but no newer local-host-identity record. Updating the binary is necessary, but enabling central grants immediately can make startup fail closed with `No local host identity is stored for this vault`.

- Keep binary upgrade and central-grant enablement as separate reversible changes.
- Confirm the custom-domain host appears in HQ discovery with the correct `apiOrigin` before attempting a canary.
- Do not copy local-bootstrap claim IDs into central identity, invent IDs, or edit HQ tables to bypass enrollment.
- A proper enrollment flow must create/recover central claims, persist the returned central host identity locally, install current public JWKS, verify a target-bound grant exchange, and only then advertise verifier readiness.
- If central-grant startup fails, roll back the verifier configuration while retaining the upgraded binary if ordinary health checks pass.

### Safe binary upgrade details

- Distinguish the latest published release from the latest repository commit.
- Older binaries may predate `haft update`; bootstrap the first update from the release archive.
- Verify the archive SHA-256 and candidate build identity before replacement.
- Preserve a rollback binary and verify both local health and the public hostname after restart.
- Do not assume a raw executable URL listed in a manifest is available; verify it. The archive URL may be the actual published artifact.
- In SSM deployment scripts, avoid an `ERR` trap whose successful rollback allows execution to continue. Use `if ! deploy; then rollback; exit 1; fi` so failed deploys remain failed.

### HQ schema drift can masquerade as enrollment or discovery failure

A successful HQ deployment and healthy `/health` endpoint do not prove that production claim/discovery queries match the current schema.

- Preflight authenticated account status and remote-target discovery before issuing a one-time pairing invitation.
- When those routes return opaque HTTP 500 responses, compare live `PRAGMA table_info(...)` output with the current schema source, especially additive columns used by hosted claims, enrollment assertions, access grants, and verifier readiness.
- Do not trust `PRAGMA user_version` or migration-history rows alone when the database may be partially migrated; verify the actual table shape.
- If an emergency additive repair is required, apply only exact missing columns from the reviewed schema, verify each mutation, restart/recheck HQ, and follow with a code-level idempotent drift-repair fix. Never invent claim IDs or modify claim rows to bypass enrollment.
- Remote databases may briefly expose stale reads after additive DDL or new claims. Verify the exact route directly and use a bounded retry; preserve the same enrollment journal and authoritative IDs.

See `references/hq-schema-drift-during-enrollment.md` for the diagnostic and recovery sequence.

### Do not use a normal media import canary to validate remote-only asset migration

If the user wants images/videos to remain **remote-only**, a standard Haft CLI image/video import is the wrong test:

- it proves only that the destination can ingest caller-local bytes into the vault
- it does **not** prove that Haft can register or surface a remote-only asset without local storage
- describing that result as a remote-only migration success is misleading

When the docs lane has already imported but the assets lane is empty, classify the gap explicitly:

1. inspect the live runtime/API contract for a remote-only registration variant rather than assuming an older docs limitation still applies
2. if registration exists, map the manifest into bounded artifact-registry records and test one source URL without fetching bytes
3. if registration does not exist, say the media migration is still staged via manifest/index only
4. verify both the registry row and absence of a local asset file; then verify the user-facing asset discovery/preview surface
5. only run a binary-media CLI canary if the user explicitly accepts that it will violate strict remote-only semantics

Treat browser login as rendering/UI evidence, not as the default replacement for a requested CLI/API migration path. Diagnose the automation credential or managed-remote capability first and state clearly when the desired transport remains blocked.

### Empty central-grant path scope can mask a route-specific media-ingest bug

A successful managed remote with advertised `import` capability is still **not** proof that `POST /api/automation/v1/media-ingest` will accept a nested destination path.

Observed live failure mode:
- grant exchange succeeds
- remote readiness is `remote-target.ready`
- the exchanged central delegated grant carries `pathPrefixes: [""]`
- `destination.pathPrefix: "athabasca/<project-slug>"` fails with `automation.auth.scope-denied`
- retrying the same remote-only canary with `destination.pathPrefix: ""` succeeds, registers a `remote-only` artifact row, preserves `source_url`/metadata, and writes no local file

Working hypothesis to carry forward:
- `automation-media-ingest` scope enforcement may mishandle an **empty allowed path prefix** even though `automation-import` already treats empty prefix as root-allowed
- so the bug is route-level scope normalization, not grant exchange, JWKS, or media payload validity

Operational response:
1. keep the original nested-path canary because it tests the intended migration destination
2. if it fails with `automation.auth.scope-denied`, inspect the exchanged grant shape before blaming auth generally
3. run a **root-prefix fallback canary** (`destination.pathPrefix: ""`) to prove whether remote-only registration itself works end to end
4. verify all four things before reporting success: HTTP success, artifact row present, `storage_state=remote-only`, and no local file written
5. report the result precisely: "remote-only ingest works live, but nested-path media-ingest scope is still buggy"
6. patch the route to match the import route's empty-prefix semantics before claiming the intended `athabasca/<slug>` path is validated

See `references/automation-media-ingest-empty-prefix-scope-bug.md` for the live canary pattern and evidence shape.

### Do not overstate media migration completeness

If Haft lacks a first-class remote-only asset registration flow, say so directly. A docs import plus remote-media manifest is a **staged migration**, not a complete binary-media ingest.

## Verification checklist

- Project metadata export exists.
- Media inventory export exists.
- Living-doc detail export exists.
- Remote-media manifest exists and includes all images/videos.
- One representative remote-only asset is registered and read back with source URL, storage state, digest, and preserved metadata.
- The remote-only canary created no local binary file and is discoverable through the intended product surface.
- Idempotent replay succeeds; changed URL/digest/storage mode conflicts.
- Docs bundle imports successfully into a scratch Haft vault.
- Imported docs count matches bundle expectations.
- Next-step instructions for remote auth/import are written down.

## Deliverables

A good migration prep should leave behind:

- migration script in the Haft workspace
- export bundle directory
- docs import bundle
- remote-media manifest (`json` at minimum)
- human-readable remote media index page
- next-steps doc for the authenticated remote import

## References

- `references/the project-migration-example.md` — concrete example, commands, counts, and the HTML-mirror workaround from a real the project migration prep.
- `references/remote-canary-and-grant-triage.md` — canary-first remote validation, HTML-vs-auth failure classification, and delegated-grant troubleshooting.
- `references/hosted-destination-readiness.md` — custom-domain/remote identity checks, binary provenance and rollback-safe upgrades, pre-Epic enrollment gaps, and canary order.
- `references/post-merge-enrollment-dogfood.md` — compatibility matrix and just-in-time authentication sequence for exercising a newly merged enrollment implementation against a real hosted destination.
- `references/hq-schema-drift-during-enrollment.md` — actual-schema verification, additive repair boundaries, bounded retry, and enrollment recovery invariants when HQ health is green but claim/discovery routes fail.
- `references/raw-html-canary-and-projection-freshness.md` — raw-vs-mirror canary discipline, safe inert JSON manifests, projection/JWKS refresh coupling, batch limits, and destination verification.
- `references/remote-only-media-registration.md` — first-class remote-only registration contract, metadata mapping, no-fetch/no-local-byte safety rules, exact-route delegated-grant wiring, transport discipline, and post-merge canary verification.
- `references/standalone-haft-vault-enrollment-and-clone-audit.md` — public metadata audit versus managed mutation authority, host-side enrollment, secure pairing transfer, and hash-based clone-cleanup discipline.
