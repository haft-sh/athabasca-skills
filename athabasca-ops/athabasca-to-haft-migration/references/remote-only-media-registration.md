# Remote-only media registration pattern

Use this when a migration must make image/video assets first-class in Haft without copying binary bytes into the vault.

## Preferred contract

Extend or use the scoped automation media-ingest surface with two explicit asset variants:

- `local`: bounded bytes (`contentBase64`) plus MIME and digest; writes a vault file.
- `remote-only`: canonical HTTP(S) `sourceUrl`, MIME, byte size, digest, title, and bounded source metadata; writes only an artifact-registry record.

A remote-only registration should persist:

- `storage_state = remote-only`
- canonical `source_url`
- source MIME, content type, size, SHA-256
- artifact kind derived from MIME (`image`, `video`, `audio`, `pdf`, fallback `asset`)
- stable source identity, e.g. `<source-system>/<project>/media/<kind>/<source-asset-id>`
- project/source asset IDs and generation provenance
- useful source metadata such as category, original filename, source kind, storage key, color/rating labels, and source timestamps
- a logical destination path for organization, without claiming it is a local filesystem path

## Required safety properties

1. Do not fetch the remote URL during registration.
2. Accept only credential-free HTTP(S) URLs.
3. Do not create a fake vault file, fake local retrieval path, or placeholder bytes.
4. Keep provenance bounded and reject credential-like metadata.
5. Preserve idempotency. Replaying the same key, URL, digest, and storage mode returns the existing artifact; changed URL/digest/storage mode is a conflict.
6. Keep local-byte ingest backward compatible.
7. Verify the catalog row and absence of a local file, not only the HTTP response.

## Canary-first verification

For one representative image:

1. Register the remote-only record through the intended CLI/API auth path.
2. Verify the response reports `remote-only` and the canonical source URL.
3. Read back the artifact-registry row and verify metadata/provenance.
4. Confirm no binary appeared under the vault assets directory.
5. Confirm the product surface that users rely on can discover or preview the remote artifact. Registry success alone is insufficient if the UI still lists only filesystem-manifest assets.
6. Repeat the same request to prove idempotent replay.
7. Only then batch the manifest.

## Transport discipline

Keep product semantics and authentication transport separate:

- If the user asks for CLI/API migration, diagnose or repair that path first.
- Browser login may help inspect rendering, but should not silently replace an automation/CLI canary.
- If the current managed CLI auth cannot issue the required capability, use a scoped service credential or extend the managed remote contract; do not bypass the API with direct database edits.
- Treat an advertised capability as discovery evidence, not authorization proof. A managed target can advertise `automation.media.ingest` while its destination verifier still rejects the exact route.
- Verify the complete chain independently: current operator CLI → authenticated HQ session → remote discovery → grant exchange → destination route gate → route handler → catalog readback.
- Confirm the CLI exposes an actual command or transport for the operation. A current CLI build and capability advertisement do not imply that a user-facing remote-only media command exists.

## Exact-route grant wiring pitfall

Central delegated grants are commonly bound to an exact method/path contract, not merely a route family or capability string. When adding a new automation endpoint:

1. Add the route handler and request schema.
2. Add the exact route to the delegated-grant requirements map with the intended operation, route family, and capability.
3. Ensure HQ discovery advertises that same capability.
4. Ensure grant exchange can request the corresponding operation.
5. Add an integration test that exchanges a real delegated grant and calls the exact endpoint.

If the destination returns `route.gate-denied` with `auth.central-grant.route-unsupported`, the request did not reach the media handler. Do not debug payload validation or metadata mapping yet. Inspect the exact-route grant map first. After any rejected canary, verify that both the catalog row and expected local path are absent before retrying.

A useful post-merge canary sequence is:

1. Compare `origin/master`, installed CLI build identity, HQ build identity, and destination build identity.
2. Authenticate just in time and confirm remote discovery/readiness.
3. Exchange the operation grant without printing bearer material.
4. Call the exact remote-only endpoint with one stable idempotency key.
5. Read back the catalog row, prove no local bytes exist, and replay the same request.
6. Only then batch the media manifest.

If HQ admission control intermittently fails, diagnose it as a separate layer: verify that the central database is reachable and the rate-limit schema exists, then use a bounded service restart/retry only as recovery evidence. Do not mistake restored HQ access for proof that destination route authorization is correctly wired.

## Metadata mapping for Athabasca-style manifests

| Source field | Haft destination |
|---|---|
| asset ID | provenance source asset ID + stable source identity |
| project slug | provenance project scope |
| title | artifact title |
| kind/content type | artifact kind + source MIME/content type |
| public URL | `source_url` |
| SHA-256 | content/source hash |
| size bytes | bounded asset metadata |
| category/source kind | source metadata |
| original filename/storage key | source metadata |
| color tag/rating | source metadata |
| created/updated timestamps | source metadata; retain exact source values in provenance |

Do not store giant raw metadata JSON by default. Preserve the operationally meaningful allowlisted fields and add new bounded fields deliberately when a real migration requires them.
