# Generation log list payload bloat

## Symptom

A project route such as `/projects/:slug/logs` shows `0 entries` while also showing a persistent loading state. The backend has generation log rows, but the frontend never appears to finish loading.

## Root cause pattern

List endpoints can accidentally return full diagnostic JSON blobs. In Athabasca generation logs, `generationInfoJson` may contain raw media byte maps or other huge upstream payloads. A single row can reach tens of MB; a `limit=50` list response can become hundreds of MB. React Query still reports no data while the browser is stuck downloading, parsing, or rendering the response.

## Debugging recipe

1. Check the component fetch path and response envelope first, as usual.
2. Call the authenticated API endpoint directly with a small limit, then a normal limit.
3. Measure response size and inspect string lengths for heavyweight fields.
4. Do not rely on the UI's `0 entries` label during loading; it may simply be rendering `query.data ?? []` before the query resolves.

## Fix pattern

For list endpoints, return compact previews for heavyweight JSON fields and keep full-fidelity data on the individual detail endpoint.

Example fields to truncate for generation log lists:

- `requestJson`
- `resolvedParamsJson`
- `generationInfoJson`
- `upstreamRequestJson`
- `upstreamResponseJson`

Use a visible marker such as:

```text
… truncated for list view; open the individual generation log for the full payload (N chars total).
```

## Verification

- Typecheck passes: `~/.bun/bin/bunx tsc --noEmit`
- Authenticated `GET /api/projects/:slug/generation-logs?limit=50` returns quickly.
- Response size is in KB/low MB, not hundreds of MB.
- Returned logs count matches expected rows.
- A deliberately large JSON field contains the truncation marker in the list response.
