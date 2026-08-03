# Premium HQ media derivatives — remote-only design notes

## Trigger

Use when a hosted Haft destination has remote-only catalog images and needs thumbnails or compressed preview renditions without making each instance own codecs, R2 credentials, and a media worker.

## Observed gap

The legacy thumbnail audit can only scan file-backed `assets`. A remote-only catalog may instead hold images in `artifacts` with `storage_state=remote-only`, leaving `assets`, `asset_thumbnails`, and `auto_publish_jobs` empty. In that state, `haft thumbnails audit --repair` is a valid no-op and must not be reported as a repair.

## Recommended product boundary

Put premium derivative execution at Haft HQ:

- destination owns artifact catalog facts and browser projection;
- HQ verifies target-bound authorization and a `media-derivatives` entitlement;
- HQ owns durable jobs, transient source fetch, codec isolation, Cloudflare R2/CDN publication, verification, quota, retries, and audit;
- destination persists only fresh verified rendition facts keyed by browser `source_identity` and source hash;
- original bytes remain canonical and remote-only.

Use two distinct renditions:

1. **Thumbnail:** tiny bounded grid/list image.
2. **Optimized preview:** compressed useful-detail rendition (not a thumbnail), preferred for normal preview while preserving an explicit original URL/action.

## Security invariants

- Do not turn this into arbitrary URL import or a server-side fetch proxy.
- Bind artifact, source identity/hash, vault claim, target, and requested profile before a worker fetches.
- Allowlist source origins; revalidate bounded redirects and reject loopback, link-local, RFC1918, metadata, embedded credentials, and non-HTTPS URLs.
- Enforce MIME, source-byte, decoded-pixel, wall-time, temp-storage, and output limits.
- Strip nonessential metadata; keep source bodies transient; never expose credentials, signed URLs, raw object keys, codec stderr, or source bodies in browser/API diagnostics.

## Rollout discipline

1. Ship entitlement + contract first, then durable job model, then destination projection.
2. Prove one remote-only image canary end to end: CDN object verification, catalog record, grid thumbnail, optimized preview, explicit original, and no local original write.
3. Perform a dry-run-first, confirmed, chunked backfill with reconciled requested/succeeded/failed/stale counts.
4. On source-hash change, mark old renditions stale and non-selectable; do not silently reuse them.

## Related canonical spec

Haft PR #1358 (`docs/2026-07-28-premium-media-derivatives-hq-spec.md`) defined the initial proposed contract. Treat current source and live runtime as authoritative if it later drifts.
