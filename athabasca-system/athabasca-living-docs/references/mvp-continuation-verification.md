# Living Docs MVP continuation verification

Use this when resuming an in-progress Living Docs implementation from `docs/plans/living-docs.md` / handoff notes.

## Resume sequence

1. Load `athabasca-living-docs` first; do not rely on filesystem guesses for skill paths.
2. Inspect `docs/plans/living-docs.md` and `docs/plans/living-docs-handoff.md` if present.
3. Check `git status --short` to understand existing uncommitted work before editing.
4. Run focused verification before assuming what remains:
   - `bun test src/server/living-docs/__tests__/parser.test.ts tests/living-docs-api.test.ts`
   - `bun run typecheck`
5. Compare the implemented surface to the MVP acceptance target, not just route/file existence.
6. If React/editor code changed, also run `bun run build` before calling the feature complete.

## Common MVP gap to check

A Living Docs editor that lets users manually type asset IDs is not the full media-picker expectation. V1 should keep exact asset-ID paste but also expose project-scoped recent/searchable media with useful filters where possible:

- fuzzy title/tag/provenance/prompt search
- kind filter
- star/rating filter
- color tag filter
- tag filter
- insert/add or replace modes for references and candidates

Global browsing is not required unless an authorized global route exists; exact global asset ID paste is enough for MVP.

## Completion standard

Only say the Living Docs MVP is complete after parser/API tests, typecheck, and frontend build pass against the current worktree. If a real R2 fixture cannot be fetched, say that explicitly and rely on reduced real-DOM fixtures plus focused tests rather than fabricating live verification.