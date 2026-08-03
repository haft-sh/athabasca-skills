# Catalog and freshness cache verification

## Problem pattern

A provider/daemon can satisfy its own deadline while the product API fails its latency gate before provider execution. Common synchronous costs on large catalogs are rebuilding reader snapshots, semantic identity mappings, and deterministic freshness manifests.

## Safe cache contract

- Cache immutable snapshot-derived objects at their real lifecycle: process-scoped and keyed by vault root plus reader snapshot generation.
- Invalidate when the catalog generation changes.
- Continue to read/validate mutable freshness state on every request; do not cache away stale-index protection.
- A `WeakMap` keyed by a `ReaderDataStore` only helps when the exact store instance is retained. Treat route/plugin construction as potentially independent unless an integration test proves otherwise.

## Required proof

1. Unit test reuse across separately-created cache/route factories for the same vault.
2. Unit test invalidation after a catalog generation change.
3. Five warm, mapped semantic requests through the real Haft API, not only direct provider calls.
4. Confirm `effectiveMode=semantic`, `semantic.state=used`, mapped non-empty results, and product p95 within the release gate.
5. Add temporary bounded reader-performance diagnostics if the product path is still slow. Record snapshot build/open timing separately from provider timing, then remove diagnostic configuration.
6. On any failed activation canary, restore keyword-only configuration immediately and verify disabled truthful fallback before further profiling.
