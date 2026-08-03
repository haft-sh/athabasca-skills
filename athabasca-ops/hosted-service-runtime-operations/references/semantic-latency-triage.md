# Semantic latency triage notes

Use after a private semantic path is functionally correct but an end-to-end benchmark is slow.

## Proven investigation order

1. Benchmark real application requests serially (at least five) with the exact requested mode, limit, and authorization context. Record `effectiveMode`, semantic state, result count, and wall time.
2. Separate warmed QMD/provider timing from BBT/application timing. A warm provider can be fast while the caller still blocks synchronously before or after `fetch`.
3. Inspect whether semantic mode eagerly computes lexical/FTS results before semantic success is known. Semantic-only routes should defer lexical collection until semantic fallback is required; hybrid still needs both lanes.
4. Measure reader-store construction, semantic identity mapping, freshness preparation, provider fetch, candidate resolution, and response projection independently. Do not keep adding caches without stage evidence.
5. If the first post-restart request is slower than warm requests, prewarm only immutable, generation-bound caller-side structures during server startup. Do not call a paid/private provider just to warm unless explicitly authorized.
6. Keep exact case-sensitive identity matching, freshness validation, bounded provider requests, and truthful keyword fallback intact.

## Deployment measurement discipline

- Build the exact merged commit and record the compiled artifact SHA-256.
- Verify the remote installed checksum and embedded health commit after swapping the immutable release symlink.
- A user may authorize live validation with semantic enabled even if a former strict p95 activation threshold is missed. Report that decision as a policy change, not as a benchmark pass.
- Keep hybrid disabled unless explicitly authorized.

## Findings from the BBT case

Deferring lexical fallback reduced semantic e2e latency from roughly 9–12 seconds to mostly 1.3–2.2 seconds. This validates eager lexical/FTS work as a major semantic-route overhead, but first-request and warm-tail costs still require stage-level tracing.
