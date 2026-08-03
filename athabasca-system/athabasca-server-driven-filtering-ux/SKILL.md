---
name: athabasca-server-driven-filtering-ux
description: Migrate Athabasca list/grid filtering from client-heavy behavior to server-driven queries without causing janky refetch UX or half-removed legacy contracts.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Athabasca Server-Driven Filtering UX

## When to use

Use this when changing an Athabasca page from loading a broad result set and filtering locally to pushing filters/sorts into API requests.

Typical triggers:
- project media/library pages feel slow because the client loads too much and filters in memory
- the API already supports partial filtering but the frontend is not sending query params
- a domain field is being removed or renamed during the same refactor, so filter plumbing and data-model cleanup must land together

## Goal

Move filtering/sorting responsibility to the server while keeping the review UI stable:
- no scroll jumps
- no grid collapse during refetch
- no twitchy refetch on every keystroke/toggle
- no stale legacy params lingering in routes, services, tests, scripts, or docs

## Recommended workflow

1. **Back up the DB first when the refactor removes or renames a first-class field.**
   - For Athabasca, run the DB backup/guard path before destructive cleanup.
   - If a legacy field already migrated into tags or another normalized store, remove the application-layer contract next instead of carrying compatibility forever.

2. **Clean server contracts before wiring the UI.**
   - Update request/query schemas.
   - Remove dead route plumbing.
   - Update service-layer request types.
   - Update persistence helpers and metadata writes.
   - Rewrite tests and utility scripts that still send the old field.

3. **Keep classification metadata optional unless the route truly requires it.**
   - Tags are organizational metadata, not a prerequisite for generation.
   - Generation endpoints should accept omitted tags and still succeed.
   - Normalize tags when provided; return `undefined`/empty when absent instead of inventing defaults just to satisfy typing.

4. **Split server-driven vs client-only filters explicitly.**
   - Push durable dataset-shaping controls to the API: kind/category/source/tags/rating/color/sort.
   - Keep cheap presentational search local if it only narrows the already fetched page and does not need backend indexing.
   - Do not leave the same filter implemented in both places unless the duplication is deliberate and documented.

5. **Debounce server-driven controls.**
   - Add a short debounce before refetching. In Athabasca, `120ms` was a good default for media filters.
   - Debounce the derived query state, not the raw controlled inputs.

6. **Preserve the previous dataset during refetch.**
   - With React Query, prefer `placeholderData: keepPreviousData` (or the current equivalent) on list/grid queries.
   - This prevents layout collapse and preserves scroll position while a filtered request is in flight.

7. **Do not unmount the grid on background refetch.**
   - The loading gate should be `isLoading && assets.length === 0` (or equivalent first-load logic), not a blanket `if (isLoading)` early return.
   - Once the page has data, keep the mounted list/grid and render a lighter updating state.

8. **Expose a separate refresh signal.**
   - Pass `isFetching`/debounce-settling state into the page and filter components.
   - Use a subtle updating indicator instead of a full-page loading replacement.

9. **Add a small visual refresh treatment.**
   - Apply a class like `.is-refreshing` to the layout during refetch/settling.
   - Prefer mild opacity/saturation transitions over spinners that replace the content.

10. **Sweep for legacy field residue outside `src/`.**
    - Check tests, one-off scripts, restore/import helpers, AGENTS/README text, and metadata payloads.
    - Historical import code may still need to *read* an old column from legacy sources, but it should write the modern shape on output.

## Pitfalls

### Pitfall: `isLoading` causes scroll reset

If the component returns a loading card whenever `isLoading` is true, React unmounts the existing grid, collapses DOM height, and the browser snaps scroll.

Fix:
- keep previous query data
- only show the full loading state on the first empty load
- use `isFetching` for background refresh UI

### Pitfall: removing a field from runtime code but not from scripts/tests

Typecheck often catches the remaining callers first. After removing a field like `phase`, search utility scripts and contract tests immediately.

### Pitfall: silently making tags required

When replacing a removed concept with tags, it is easy to accidentally turn `tags` into a required field in schemas or helper signatures. Do not do that unless the product requirement is explicit.

## Verification checklist

- [ ] DB backup/guard completed before destructive contract cleanup
- [ ] API schema/query params updated
- [ ] Route handlers no longer pass dead fields
- [ ] Service and worker request types updated
- [ ] Persistence helpers write the modern metadata shape
- [ ] React Query keeps previous data during refetch
- [ ] Background refetch does not unmount the grid
- [ ] Debounce applied to server-driven filters
- [ ] Updating state is visible but non-destructive
- [ ] Tests and scripts no longer send removed params
- [ ] Docs/agent guidance updated where they describe active runtime behavior

## Notes

This overlaps somewhat with `athabasca-frontend-conventions`: that skill should own broad React/UI conventions, while this skill owns the specific class of server-driven filtering migrations with refetch UX preservation and legacy-contract cleanup.
