# Generation log list UI: pagination and overflow

Use this when a project generation-log page is slow, appears stuck loading, shows too many entries, or causes horizontal page scrolling.

## List API contract

- Default list size should be small: 10 entries is the house default for generation logs.
- Prefer server-side pagination with `limit` + `offset` and return pagination metadata:
  - `limit`
  - `offset`
  - `hasMore`
  - `nextOffset`
  - `previousOffset`
- Fetch `limit + 1` internally to compute `hasMore`, then return only `limit` rows.
- The frontend query key must include the offset so React Query caches pages independently.
- Reset offset to 0 when the project changes.

## Payload safety

Generation logs can contain huge provider payloads. List endpoints must return previews, not full raw JSON, for fields like:

- `requestJson`
- `resolvedParamsJson`
- `generationInfoJson`
- `upstreamRequestJson`
- `upstreamResponseJson`

Keep the individual detail endpoint available for full inspection if needed.

## Layout safety

Generation logs are hostile content for CSS: long prompts, URLs, IDs, JSON, and base64-like strings. Add all of these together:

```css
.page-shell { width: min(100%, 1280px); }
.detail-column, .card, .generation-log-list, .generation-log-card { min-width: 0; }
.generation-log-card { overflow: hidden; }
.generation-log-meta p,
.generation-log-card > p { overflow-wrap: anywhere; }
.generation-log-details pre {
  max-width: 100%;
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-word;
}
```

Do not rely on `pre-wrap` alone. In grid/flex layouts, missing `min-width: 0` on an ancestor can still force the whole page wider than the viewport.

## UX pattern

Header should show the visible range, not imply a total count unless the API returns one:

- `Showing 1-10`
- `Showing 11-20`
- `0 entries`

Pagination controls: `Previous / Page N / Next`. Disable previous when `previousOffset == null`; disable next when `hasMore` is false.