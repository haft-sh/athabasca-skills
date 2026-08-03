# Raw HTML canary, inert manifests, and managed-projection freshness

## Why this exists

A document migration can appear healthy when a Markdown mirror imports while the raw HTML path is still broken. A managed destination can likewise appear healthy immediately after enrollment while short-lived identity projections later disable imports or browser login. Validate the exact content path and the current authorization state.

## Canary sequence

1. Import one raw `.html` source into a disposable `*-html-sanity-check` path.
2. If it fails before a job is created, classify auth/trust separately from normalization.
3. If normalization fails, inspect active tags and attributes before falling back to Markdown.
4. Retest the same raw source after the importer fix.
5. Verify completed job, indexed artifact, normalized profile, visible title/content, and visual rendering.
6. Only then batch raw HTML. Chunk requests to the server contract limit (currently 25 files).

## Inert embedded JSON manifests

Athabasca living-doc HTML can contain:

```html
<script type="application/athabasca+json" data-ath-manifest="living-doc">
  {"schemaVersion":1,"artifactType":"prompt-preview"}
</script>
```

This is non-executable data. A safe Haft normalizer can accept scripts only when:

- `type` is exactly `application/json` or matches `application/*+json`
- there is no `src`
- there are no `on*` event attributes

The normalized reader artifact should omit the manifest JSON. Preserve the original raw HTML in the private source-snapshot lane. Continue rejecting executable/missing script types, remote scripts, event handlers, JavaScript URLs, forms, frames, objects, and embeds.

Regression coverage should include both a successful inert-manifest fixture and a rejected executable `<script>alert(1)</script>` fixture.

## Managed projection and JWKS freshness

Remote import and browser login can fail after enrollment even when discovery initially showed `ready`:

- `projection-expired` means the target must refresh and install a new signed projection before write grants are advertised.
- `auth.central-grant.bad-signature` after refresh often means the destination verifier still has an older public JWKS. Refresh/install projection and public JWKS as one operational unit, then restart the intended service if runtime verifier state changed.
- A completed enrollment journal may not be resumable for routine projection refresh. Do not hand-edit completed journals or fabricate claims. Use a supported refresh command when available; until then, treat destination-local refresh as a narrowly reviewed operational recovery and record the product gap.
- Short projection TTLs can expire during login or mid-migration. Refresh immediately before bounded work and verify the expiry is long enough for the operation. A manual refresh is not a durable repair.

## `claim revoked` may actually mean projection expired

Before starting recovery, transfer, or re-enrollment, inspect the full local claim shape and timestamps:

- top-level claim status and `revokedAt`
- server-claim status and `revokedAt`
- vault-claim status and `revokedAt`
- projection `syncedAt`, `expiresAt`, and version
- recent bounded auth audit codes

If all claim components are active and have no revocation timestamp, but `projection.expiresAt` is in the past, classify the incident as **projection expiry**, even if `/api/auth/status` or the browser says `auth.claim.revoked`. Do not transfer ownership or generate replacement claims for this state.

After recovery, verify both:

1. public auth status reports `state=claimed` and active claim status; and
2. the browser returns to the normal email-login form rather than the revoked-claim denial.

## Emergency refresh verification gates

When no supported refresh command exists and a reviewed destination-local recovery is authorized:

1. Use the destination's persisted instance-refresh credential without printing or transferring the raw handle.
2. Request a projection from the configured HQ origin with exact server claim ID, server fingerprint, vault claim ID, vault fingerprint, account ID, and team ID.
3. Fetch the **current HQ JWKS**. A stale destination copy can make a valid new projection appear to have a bad signature.
4. Verify the signed envelope before mutation:
   - expected profile, issuer, audience, key ID, and EdDSA algorithm
   - canonical payload SHA-256
   - Ed25519 signature against an active, currently valid JWKS key
   - exact binding equality for all requested IDs and fingerprints
   - expected vault access grant is present
   - `issuedAt <= now < expiresAt`
   - projection version does not go backwards
5. Back up the prior auth state with ownership and mode preserved.
6. Install through the product's projection installer when possible. If a narrowly reviewed recovery must update persisted state, replace it atomically, preserve unrelated users/memberships/sessions/audit data, and update only the verified projection-bound claim fields.
7. Verify status and the actual blocked route. Do not call public health alone proof of recovery.

If signature verification fails with a cached JWKS but succeeds with the current HQ JWKS, the durable issue is JWKS refresh coupling—not a reason to bypass signature checks.

## Durable product fix

A five-minute projection TTL without destination-side renewal creates a predictable login and migration outage. The correct product behavior is automatic refresh before expiry with bounded retries and fail-closed verification. A supported operator command such as `haft remote refresh <slug>` is useful as a recovery seam, but it should not be the normal availability mechanism. UI/status should distinguish `projection-expired` from true claim revocation.

## Batch verification

For each chunk, record completed state, imported count, skipped count, and batch ID. After all chunks, verify destination filesystem/index counts by extension and folder, plus one normalized HTML artifact. Do not infer full completion from CLI success on the first chunk.
