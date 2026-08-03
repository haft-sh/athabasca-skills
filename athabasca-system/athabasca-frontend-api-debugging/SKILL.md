---
name: athabasca-frontend-api-debugging
description: Debug frontend React components against Athabasca Elysia API routes — find the correct endpoint path, verify the response envelope, fix import mismatches, and confirm typecheck cleanliness. Use when writing or fixing a React component that calls an Athabasca API endpoint.
version: 1.0.0
author: Hermes Agent (Athabasca)
metadata:
  hermes:
    tags: [athabasca, frontend, react, api, debugging, typescript]
    related_skills: [athabasca-media-attachment-finder, athabasca-shot-list]
---

# Athabasca Frontend ↔ API Debugging

Use this skill when writing a new React component against an Athabasca API route, or when a frontend component is silently failing (wrong data, 404, or "Cannot find name X").

## Debugging Sequence

### Step 1 — Find the endpoint the component expects

Read the `fetch()` URL in the component:

```typescript
// Example: ThumbnailImageById.tsx
const response = await fetch(`/api/media-assets/${assetId}`);
```

Strip the path and search for it in routes:

```bash
grep -rn "media-assets" src/server/api/routes/
```

### Step 2 — Find the actual route in the Elysia route files

```bash
grep -rn "media/:assetId\|GET.*assetId" src/server/api/routes/
```

Common route files:
- `src/server/api/routes/system.ts` — `/api/media/:assetId` detail endpoint
- `src/server/api/routes/projects.ts` — all project-scoped routes

### Step 3 — Verify the response envelope

Elysia routes return `{ ok: true, asset }` or `{ ok: true, data }` — not a bare object.

```typescript
// CORRECT — unwrap the envelope
const data = await response.json();
return data.asset;

// WRONG — trying to use data directly
return response.json();
```

The `ThumbnailImageById` bug: component expected `data.asset` which is correct, but called the wrong URL path.

### Step 4 — Check if the component is imported in App.tsx

If TypeScript reports `Cannot find name 'XComponent'` but the component file exists:
1. Check the imports in `src/App.tsx` (line ~10-15 area)
2. Add the missing import alongside other component imports

```typescript
// Typical import block in App.tsx
import { ThumbnailImageById } from "./components/ThumbnailImageById"; // ← add here
```

Media-only refactor pitfall: do not resurrect deleted storyboard/shot components just because old docs or snippets mention them. If the schema has moved to media-only, stale imports for `StoryboardGrid`, `StoryboardVariationModal`, `StoryboardSlotCard`, or `storyboard-types` should be deleted with their routes/styles/tests, not fixed by re-adding the old subsystem.

### Step 5 — Typecheck

```bash
cd <athabasca-repository> && ~/.bun/bin/bunx tsc --noEmit
```

**bun not on PATH** — use the full path: `~/.bun/bin/bun` or `$HOME/.bun/bin/bun`.

## Known Route ↔ Component Path Mapping

| Component expects | Actual route |
|-------------------|-------------|
| `/api/media-assets/:id` | `/api/media/:id` (system.ts) |
| `/api/projects/:slug/media` | `/api/projects/:slug/media` (projects.ts) |

This mapping is incomplete — verify with grep before assuming. Route files change.

## Canonical vs legacy route cleanup

When you discover that a newer Athabasca endpoint fully supersedes an older one, do not stop at saying the legacy route is redundant. Verify the actual state and then clean it up end-to-end.

Recommended sequence:
1. confirm the canonical and legacy routes both dispatch to the same underlying service/helper
2. compare request/response schemas — if the canonical route is strictly richer, treat it as the source of truth
3. search runtime callers in `src/` and contract tests in `tests/` before removing the legacy route
4. remove the legacy route handlers and any now-unused schema/service imports
5. add contract tests asserting the removed routes now return `404`
6. prune stale docs/plans that still describe the legacy routes as active
7. run `bun run typecheck` and the relevant API contract tests

This came up with Athabasca video generation: `POST /api/projects/:slug/generate/video` superseded the old `/api/projects/:slug/video-generation/image-to-video` and `/api/projects/:slug/video-generation/text-to-video` routes. The correct cleanup was to delete the old handlers, add 404 coverage, and update the plan doc — not leave thin adapters around forever.

## Common Failure Modes

1. **URL path mismatch** — most common. Component was written with a guessed path that doesn't match the route definition.
2. **Missing import in App.tsx** — component exists and works standalone but isn't wired into the router.
3. **Response envelope confusion** — Elysia wraps everything in `{ ok: true, ... }`; direct destructuring fails.
4. **Large list payload masquerading as frontend loading bug** — if a list page shows `0 entries` plus a persistent loading state, do not assume React Query or routing is broken. First call the authenticated live endpoint and check response size/shape. Generation logs hit this when the list endpoint returned full stored JSON payloads, raw media byte maps, or provider base64 payloads; one page could exceed hundreds of MB, so the browser stayed stuck downloading/parsing. Fix list endpoints by returning summaries/previews, truncating heavyweight JSON fields for list views, and keeping full payloads only on per-record detail routes. See `references/generation-log-list-payload-bloat.md`.
5. **Missing pagination on potentially large list views** — for operational logs/history feeds, default to a small page size (10 for generation logs), support `limit` + `offset`, and fetch `limit + 1` server-side to compute `hasMore` without a count query. Return pagination metadata (`limit`, `offset`, `hasMore`, `nextOffset`, `previousOffset`) and reset the client offset when the project/route scope changes.
6. **bun not on PATH** — always use the full path: `~/.bun/bin/bun` in shell sessions.
6. **Phase is optional media-tag metadata** — `phase` on `/api/uploads` or `/api/projects/:slug/media` is not a media DB column or workflow gate. `"generated"` is a `category`, not a phase/tag. Prefer omitting `phase` unless the artifact has a useful organizational label; use `category=generated` for generated media.
7. **Legacy generation adapters still mounted** — when auditing or wiring video-generation calls, treat `POST /api/projects/:slug/generate/video` as canonical and treat `/api/projects/:slug/video-generation/image-to-video` plus `/api/projects/:slug/video-generation/text-to-video` as compatibility shims unless current callers prove otherwise. Verify all three things before deleting an older route: (a) both old and new paths call the same service helper, (b) tests and current callers use the canonical path, and (c) the canonical response/schema is at least as rich as the legacy one. Do not assume "older path still exists" means "older path is still needed."
8. **libsql wrapped errors hide the real column** — when `Failed query:` appears in a Turso/libsql error, always dig into `error.cause.cause.message` for the actual SQLite cause. The top-level message rarely names the offending column.
9. **Duplicate `storage_key` on retry after failed INSERT** — if an INSERT fails partway (e.g., FK error), R2 already has the file but the DB record rolled back. The next retry auto-generates the same `storage_key`, hitting the UNIQUE constraint. Always pass an explicit unique `storage_key` when retrying.
10. **Bun test module-singleton DB leakage** — if an API contract test passes alone but fails only when run after another test file, suspect cached module singletons (`src/server/db/client`, API app) before debugging the endpoint itself. Bun may keep imported modules alive across files in one test process, so changing `TURSO_DATABASE_URL` in a later `beforeAll` does not necessarily create a new DB client. Do not delete per-file SQLite test DBs in `afterAll` while a cached singleton may still point at them; keep temp DB cleanup at process exit or isolate module loading. Reproduce with both file orders, then fix the shared test harness rather than the endpoint symptom.

## Verification Checklist

- [ ] Component URL matches a real route in `src/server/api/routes/`
- [ ] Response unwrapping matches the envelope shape (`data.asset`, `data.assets`, etc.)
- [ ] Component is imported in `src/App.tsx` (if used there)
- [ ] `bunx tsc --noEmit` exits 0 with no errors
