# Public semantic search rollout contract

Use this when turning an existing private QMD/Haft integration into a publicly usable search surface.

## Separate the layers

A healthy QMD CLI, bridge process, or `200` search response does not prove the product is doing semantic retrieval. Verify separately:

1. **Index freshness** — collection root and revision match the currently served Haft vault/catalog.
2. **Provider execution** — the private bridge actually returned semantic candidates before Haft mapped results.
3. **Identity mapping** — every accepted candidate maps to current Haft page/chunk identity; reject stale or ambiguous candidates.
4. **Public projection** — anonymous search is restricted server-side to public content; no private/unlisted rows, counts, snippets, facets, source paths, or ranking signals leak.
5. **Product UX** — labels are driven by effective execution, not only requested search mode.

## Truthful fallback contract

Keep the request mode and effective execution distinct. A recommended additive response shape is:

```ts
execution: {
  requestedMode: "keyword" | "semantic" | "hybrid";
  effectiveMode: "keyword" | "semantic" | "hybrid";
  degraded: boolean;
  semantic: {
    state: "not-requested" | "disabled" | "used" | "timeout" |
           "unavailable" | "overloaded" | "stale-index" | "mapping-empty";
    latencyMs?: number;
  };
}
```

Do not name a provider, endpoint, collection, raw error, raw path, or internal counter in public responses. A lexical fallback is acceptable for availability only if it is marked as degraded and reports `effectiveMode: "keyword"`.

## Provider containment

Do not solve latency solely by increasing Haft's HTTP timeout. Before raising caller timeout, the provider must own:

- a deadline no longer than the caller deadline;
- abort propagation;
- child process kill/reap on timeout or disconnect;
- bounded concurrency/queue with an explicit overloaded result;
- bounded stdout, stderr, request size, and candidate count;
- redacted logs (request ID, duration, counts, failure code; no raw query by default).

For QMD 2.5.3, verify CLI argument compatibility against the installed version; use `-n` for candidate limits where supported rather than assuming an older `--limit` flag.

## Delivery policy

Reusable source changes should be ordinary PRs to the shared default branch with provider execution disabled by default. First-host activation is deployment configuration from a reviewed pinned SHA, not a permanent environment source fork. Keep hybrid disabled until semantic mode is independently correct and measured; Haft should combine lexical and semantic candidates rather than delegating public hybrid semantics to a provider.
