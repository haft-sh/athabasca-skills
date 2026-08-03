# Live remote-only media batch import notes

Use this reference when finishing an Athabasca → Haft media migration where documents already moved but images/videos need to be registered as first-class **remote-only** assets on a managed remote.

## Durable takeaways

### 1. Reconcile against live Athabasca media immediately before import
Do not trust an older saved `remote-media-manifest.json` as complete.

Practical rule:
- fetch live `GET /api/projects/:slug/media`
- filter to `kind in (image, video)`
- diff by Athabasca asset ID against the prior manifest
- append any newer assets before batching

Observed case:
- prior manifest: 275 assets
- live image/video inventory: 285 assets
- missing from old manifest: 10 newer images

So the right import source became a refreshed current manifest, not the original export artifact.

### 2. A direct media-ingest canary is valid when the product contract exists but CLI ergonomics lag
If the live Haft system supports remote-only media registration at `POST /api/automation/v1/media-ingest`, but the CLI still lacks a first-class user-facing subcommand for that exact operation, do not treat that as a blocker for migration validation.

Safe bridge pattern:
1. use the CLI/HQ identity already on disk
2. discover the managed remote target
3. exchange a central delegated grant for the target with `operations=["import"]`
4. call `POST /api/automation/v1/media-ingest` directly with one stable idempotency key
5. verify `status`, `storageState`, `sourceUrl`, and `indexed`
6. only then batch the full manifest

This keeps the test on the **real deployed product route** rather than inventing a side path.

### 3. Filename extension must match MIME for remote-only ingest
The destination filename is validated against MIME even for remote-only assets.

Observed failure class:
- Athabasca asset had `contentType=image/webp`
- original filename ended in `.jpg`
- Haft returned `automation.media.path-denied`
- error text: `MIME type image/webp does not match extension .jpg`

Operational fix:
- derive the destination filename extension from canonical MIME, not from the original filename alone
- preserve the descriptive stem when possible
- for duplicates, suffix with the Athabasca asset ID before the extension

Suggested mapping:
- `image/jpeg` → `.jpg`
- `image/png` → `.png`
- `image/webp` → `.webp`
- `image/gif` → `.gif`
- `video/mp4` → `.mp4`
- `video/webm` → `.webm`
- `video/quicktime` → `.mov`

### 4. Replay-safe reruns are expected
A partial batch may succeed for early items before a later asset fails. After fixing the payload shape, rerun the full batch with stable idempotency keys.

Expected result shape:
- previously successful items return `status: replayed`
- new/fixed items return `status: ingested`

That is a healthy recovery path, not evidence of duplication.

### 5. Browser/UI verification is separate from backend migration proof
A successful media-ingest response with `indexed: true` is strong backend evidence that the asset was registered, but it is not the same thing as authenticated browser verification of the assets lane.

Report these distinctly:
- backend migration proof: canary and batch responses, remote-only state, source URL preserved
- UI proof: authenticated browser session shows the asset in the intended product surface

Do not overclaim UI validation if the browser is still unauthenticated.

## Concrete live proof shape

A good canary response looked like:
- HTTP `200`
- `status: ingested`
- `asset.storageState: remote-only`
- `asset.sourceUrl: <Athabasca public URL>`
- `indexed: true`

A successful full import can legitimately end as a mix of:
- `ingested` for first-time items
- `replayed` for items already registered during an earlier partial run

## When to reuse this reference

Use this note when:
- the docs lane is already complete
- the remote target is managed through central delegated grants
- the missing work is the image/video lane
- live Athabasca assets may have changed since the last export
- you need to preserve strict remote-only semantics
