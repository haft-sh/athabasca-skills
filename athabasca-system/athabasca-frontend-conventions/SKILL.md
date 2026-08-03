---
name: athabasca-frontend-conventions
description: Frontend development conventions and patterns for Athabasca — CSS architecture, component design standards, API path conventions, and graceful-degradation requirements for the Athabasca React SPA.
version: 1.0.0
author: Hermes Agent (Athabasca)
metadata:
  hermes:
    tags: [athabasca, frontend, css, react, component-design, layout]
    related_skills: [athabasca-shot-list, athabasca-script-phase-source-supplied-intake]
---

# Athabasca Frontend Conventions

Frontend development standards for the Athabasca SPA (`src/`). Load this skill when working on UI components, CSS, layout, API integration, or anything touching the frontend layer.

## CSS Architecture

### Single file
All CSS lives in `src/index.css` (2,500+ lines). There is no CSS module system, no component-level CSS files, and no Tailwind. Everything is global class names and CSS custom properties.

### Design system tokens (defined in `:root`)
```css
:root {
  --bg: #131313;
  --surface-container-lowest: #0e0e0e;
  --surface-container-low: #1c1b1b;
  --surface-container-high: #2a2a2a;
  --surface-container-highest: #353534;
  --outline-variant: #5d3f40;
  --card-border: rgba(255, 255, 255, 0.08);
  --text: #e5e2e1;
  --text-variant: #e6bcbd;
  --muted: #ad8888;
  --primary: #ffb3b5;
  --primary-strong: #ff5167;
  --primary-soft: rgba(255, 179, 181, 0.12);
  --blocked: #ff9500;
  --blocked-soft: rgba(255, 149, 0, 0.1);
}
```

### Adding CSS rules
Append new sections above the `@media` block at the end. Always include:
- The full component class tree (parent + children)
- Placeholder variant for every visual slot that can be empty/null
- Responsive breakpoint if layout is viewport-sensitive

**Critical rule: never add a component class without also adding its placeholder variant.** The class tree must work with null/missing data, not just with fully-populated data.

## Component Design Standards

### Graceful degradation requirement
When optional data is absent, the layout must still render correctly with a styled placeholder. It must NOT break the grid, stack vertically in a broken way, or look like junk.

This applies to:
- Thumbnail grids with no image → styled placeholder with icon
- Text fields that are null → clamped ellipsis, not raw "null"
- Optional nested components → empty fallback, not error

### Responsive card rule for media + text layouts
If a card pairs a thumbnail/media column with descriptive text (for example the project info card above the Media route), do not keep a forced two-column layout on mobile. At small viewports (`max-width: 768px` is the current house breakpoint), switch the card to a single column so the thumbnail stacks above the text.

Implementation pattern:
- Desktop/tablet: `grid-template-columns: <fixed-media-width> 1fr`
- Mobile: `grid-template-columns: 1fr`
- If the media rail has a separating border, flip `border-right` to `border-bottom` in the stacked layout
- Stretch the thumbnail area to full width on mobile instead of centering a narrow column

This is a legibility rule, not a one-off fix. If the mobile view feels squeezed, stack first and only then consider typography or spacing tweaks.

### The ThumbnailImageById pattern
```tsx
// API path: GET /api/media/:assetId  (NOT /api/media-assets/:assetId)
// Response envelope: { ok: true, asset: { id, publicUrl, previewImageUrl } }

export function ThumbnailImageById({ assetId }: { assetId: string }) {
  const { data: asset } = useQuery({
    queryKey: ["asset", assetId],
    queryFn: () => fetchAssetById(assetId),
    staleTime: 5 * 60 * 1000,
  });

  const src = asset?.previewImageUrl ?? asset?.publicUrl ?? null;
  if (!src) {
    return <div className="project-card-thumbnail-placeholder">...</div>;
  }
  return <img src={src} alt="" className="project-card-thumbnail-img" />;
}
```

Key contract:
- Call `/api/media/{assetId}`, not `/api/media-assets/{assetId}`
- Access `data.asset` from the response envelope
- Always have a placeholder fallback for null/missing src

## Project Grid CSS (example of complete component class tree)

This was added as a reference implementation. When creating any new grid/card component, include the full class tree:

```css
.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}

.project-card {
  display: grid;
  grid-template-rows: auto 1fr;
  border-radius: 16px;
  border: 1px solid var(--card-border);
  background: var(--surface-container-low);
  overflow: hidden;
  text-align: left;
  cursor: pointer;
  transition: border-color 0.15s ease, background 0.15s ease;
  padding: 0;
}

.project-card-thumbnail {
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  border-bottom: 1px solid var(--card-border);
}

.project-card-thumbnail-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.project-card-thumbnail-placeholder {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  background:
    radial-gradient(circle at top, rgba(255, 179, 181, 0.1), transparent 40%),
    var(--surface-container-high);
}

.project-card-body {
  display: grid;
  gap: 8px;
  padding: 16px;
}
```

## Import patterns

React component imports live at the top of `App.tsx`. When adding a new component used in the routing tree, add the import alongside existing component imports:

```tsx
import { ThumbnailImageById } from "./components/ThumbnailImageById";
```

## API endpoint path conventions

- Project-scoped media: `/api/projects/:slug/media`
- System-wide media: `/api/media/:assetId`
- Project detail: `/api/projects/:slug`
- Shot detail: `/api/projects/:slug/shots`

Always verify the actual route path before wiring a fetch call. Check `src/server/api/routes/` for the canonical path definition.

### Modal overlay + grid pattern (project thumbnail picker reference)

```css
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: grid;
  place-items: center;
  z-index: 50;
}

.modal-panel {
  background: var(--surface-container-low);
  border: 1px solid var(--card-border);
  border-radius: 16px;
  display: grid;
  grid-template-rows: auto 1fr auto;
  max-width: 800px;
  width: 90%;
  max-height: 80vh;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--card-border);
}

.modal-body {
  overflow-y: auto;
  padding: 16px 20px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding: 12px 20px;
  border-top: 1px solid var(--card-border);
}

/* Selectable asset grid (thumbnail picker, media picker) */
.thumbnail-picker-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 10px;
}

.thumbnail-picker-item {
  aspect-ratio: 16 / 9;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid transparent;
  cursor: pointer;
  transition: border-color 0.15s;
}

.thumbnail-picker-item.selected {
  border-color: var(--primary-strong);
}

.thumbnail-picker-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
```

## Media grid card conventions

The project media grid (`src/components/project-media/ProjectMediaGrid.tsx`) uses a tile pattern where each card has:
- A preview area (thumbnail/video) with a clickable overlay
- A body section with title and muted metadata
- Small action buttons (info icon, copy ID) positioned absolutely in corners

### Hybrid approach: clean grid, inspector editing
**Do NOT put star ratings or color pickers on grid cards.** The grid is for scanning; the right-panel inspector is for adjusting. This matches the Lightroom CC pattern: thumbnails stay clean, metadata lives in the filter bar and inspector.

The only visual cue on cards is a **passive colored left border** (3px) when a color tag is set — read-only, no click handler.

### Color indicator pattern
- Thin colored **left border** (3px) on the tile when `asset.colorTag` is set
- Add the class dynamically: `${asset.colorTag ? ` color-${asset.colorTag}` : ""}`

```css
.project-media-tile.color-red    { border-left: 3px solid #ef4444; }
.project-media-tile.color-yellow { border-left: 3px solid #eab308; }
.project-media-tile.color-green  { border-left: 3px solid #22c55e; }
.project-media-tile.color-blue   { border-left: 3px solid #3b82f6; }
.project-media-tile.color-purple { border-left: 3px solid #a855f7; }
```

### Inspector: star rating + color + tags
All three are edited in `ProjectMediaInspector.tsx`:

**Star rating editor** — 5 star buttons (★), click star N to set rating to N; re-click the same star to clear (set to 0). PATCH `/api/projects/:slug/media/:assetId` with `{ ratingStars: N }`.

**Color label picker** — 5 colored square buttons (red/yellow/green/blue/purple) + a clear ✕ button. Click a color to set, click the same color again to remove. PATCH with `{ colorTag: "red" | null }`.

**Tags** — Three-part section in `ProjectMediaInspector.tsx`:
1. **Suggestions** (top): plain text labels with no border. Shows all tags used anywhere in the project *except* those already applied to the selected asset. Click to apply. Once applied, the tag disappears from suggestions and appears as a pill below.
2. **Applied tags** (middle): rounded pills (`border-radius: 12px`) with × button to remove. Each applied tag is removed from the suggestions list.
3. **Add new tag** (bottom): text input + Add button for tags not yet in the project. When added, they appear in suggestions for other assets.

### Inspector metadata grid layout
The metadata grid in `ProjectMediaInspector.tsx` uses a 2-column CSS grid with paired fields. Each `<div>` is a single grid cell; do NOT use `project-media-meta-grid-full` to span rows unless intentionally spanning both columns.

**Current pairing** (5 rows, 10 items):
| Column 1 | Column 2 |
|---|---|
| Phase | Created |
| Content type | Size |
| Filename | Media ID |

**Media ID row**: sits in the second column (right side), paired with Filename. Includes the ID text + inline copy-to-clipboard button (`<span class="material-symbols-outlined">content_copy</span>`) + status text. Do NOT span it full-width.

**Header section**: title display (with edit button), no "Project-wide asset" label, no "Open full asset" button. Keep it minimal — title + kind label in the card header.

### Filter bar conventions
The media filter bar (`ProjectMediaFilters.tsx`) has two rows:

**Row 1 (primary)**: Search input (placeholder: "Search ID, title, provenance, or prompt"), File Type dropdown, Sort control (Newest/Oldest/Highest rated/Lowest rated)

**Search haystack** (in `media-filtering.ts` → `filterProjectMediaAssets`): client-side text search matches against `asset.id`, `asset.title`, `asset.provenanceNote`, and `asset.generation?.prompt`. All lowercased. If a new field should be searchable, add it to the `haystacks` array there.

**Exact-match for asset IDs**: when the query looks like a full asset ID (`asset_` prefix + ≥12 chars), do an **exact match** against `asset.id` and skip the fuzzy substring search entirely. Without this, searching for `asset_mpqaokuaubvetraj` would also match any asset whose provenance note or prompt references that ID as a substring — returning false positives. Pattern:

```ts
if (searchNeedle.startsWith("asset_") && searchNeedle.length >= 12) {
  return asset.id.toLowerCase() === searchNeedle;
}
```

**Row 2 (advanced)**:
- **Star filter**: 5 individual star buttons. Clicking star N fills stars 1–N (yellow) and filters to ≥ N. Re-clicking the active star clears the filter (all gray). No "Any" button — all-gray is the reset state.
- **Color filter**: 5 colored swatch squares + "∅" to reset. Click to filter by that color.
- **Tag filter**: dropdown with all tags used in the project.

Filters pass through the API via query params (`minRating`, `maxRating`, `colorTag`, `tags`, `sortBy`, `sortOrder`). Client-side filtering for search text.

## Layout overflow rules

For long-text operational pages such as generation logs, treat horizontal scrolling as a bug unless it is confined inside an intentionally scrollable code block.

- Page wrappers should have an explicit width cap, e.g. `.page-shell { width: min(100%, 1280px); }`.
- Grid/flex containers that hold cards must include `min-width: 0`; otherwise long descendants can force the whole page wider than the viewport.
- Cards that contain generated prompts, URLs, JSON previews, or model payload snippets should use `min-width: 0`, `overflow: hidden`, and `overflow-wrap: anywhere` on text-bearing children.
- `<pre>` inside cards should use `max-width: 100%` and internal `overflow-x: auto`; do not let it expand the page.
- Log/history routes should paginate by default rather than rendering every entry; generation logs use 10 entries per page with Previous/Next controls.

## Design principles

1. **Layout must be complete with optional data absent.** Never say "works as designed" when a null field causes broken layout.
2. **CSS goes with the component.** If a component is added to App.tsx or any page, its CSS must be added to `index.css` at the same time.
3. **One placeholder variant per visual slot.** Every div that shows optional content needs a styled fallback.
4. **Use design tokens, not hardcoded values.** Reference `var(--name)` tokens for colors, spacing, and typography.
5. **Test with null/empty data.** Verify the UI renders gracefully when all optional fields are null.
6. **Paginate hostile large lists by default.** Logs and provider payload lists should default to small pages, include server-side pagination metadata, and not imply a total count unless one is actually returned. See `references/generation-log-list-pagination-overflow.md`.
7. **Prevent horizontal page overflow at the container level.** Long prompts, URLs, IDs, and JSON need `min-width: 0` on grid/flex ancestors plus wrapping rules on text children; fixing only the `<pre>` is not enough.

## Pitfalls

### New route renders the homepage — check stale dev service before rewriting router code
When a new Athabasca SPA route such as `/projects/:slug/living-docs` renders the project list/homepage, first check whether the running service is serving a stale frontend bundle. `readRoute()` falls back to `{ kind: "home" }` for unknown path shapes, so stale route code can look exactly like the homepage.

Fast check:
1. Inspect `src/App.tsx` and confirm `readRoute()` recognizes the path shape and the render tree has the matching `route.kind` branch.
2. If local code is correct, restart `athabasca-dev.service` or test on a separate `PORT` rather than continuing to patch router logic.
3. Ensure `src/index.ts` honors `PORT` before suggesting alternate-port dev servers.

See `references/living-docs-route-stale-dev-server.md` for the detailed debug pattern.

### Eden Treaty date coercion (silent runtime type mismatch)
Eden Treaty silently converts date-like string fields into JavaScript `Date` objects, even when the Zod schema declares `z.string()` and TypeScript says `string`. **Never use `String()` + `localeCompare()` or string comparison operators on `createdAt`/`updatedAt` fields** — `String(Date)` produces day-of-week-prefixed output that sorts incorrectly. Always convert to numeric timestamps via `.getTime()` with an `instanceof Date` guard. See `references/eden-treaty-date-coercion.md` for full diagnosis and fix pattern.

### Overview tab JSX structure — preserve parent wrappers
The project Overview tab (`App.tsx`, `route.kind === "project"`) uses nested Route-conditionals with structural `<div>` wrappers at each level. When removing child sections, **do not restructure the parent JSX** — remove only the child blocks. The outer `{route.kind === "project" ? (<>...` + closing `</> : null}` is the only wrapper at that level, but it is not safe to remove without checking what depends on its presence. A wrong edit can create a double-close or orphaned closing tag — the error only surfaces at runtime when the page breaks.

If editing the Overview section: read the full surrounding context (before + after the block you're removing) before patching. TypeScript typecheck via `bun run typecheck` should pass after every patch.

### Phase removal — `phase` field on media is a tag, not a scope
Athabasca is transitioning away from phases as a production gating mechanism. The `phase` field on media assets is **only a tag** — it has no effect on data visibility or workflow progression. When removing phase-related UI:
- Remove the phases strip section entirely
- Remove any section that displays phase context (workflow guidance, project context)
- Remove the metadata grid fields that reference phase (current phase, latest checkpoint)
- Remove generation settings UI (provider/model selects that were per-phase)
- Fix any confirmation dialogs that mention phases: `handleDeleteMediaAsset` should say "from this project?" not "from the ${phase} phase"
- Remove any `phaseMediaQuery` / `activePhaseMediaAssets` logic that scopes media by phase — use `projectMediaQuery` / `projectMediaAssets` instead (all project media, unfiltered)

### Overview tab reduction target
When the user asks to simplify the project Overview tab, the target shape is intentionally narrow:
- keep only the thumbnail, description/objective, a small set of basic metadata, and the danger zone
- remove the phases strip entirely
- remove generation provider/settings UI entirely
- remove workflow-guidance / project-context summary cards
- remove the duplicate media gallery from Overview; the Media route is the canonical place for browsing assets

### Aggressive legacy-phase removal
When the user explicitly says the old phase/storyboard/research/concept/approval UI is obsolete and safe to delete, treat it as an aggressive refactor request, not a request for a conservative deprecation pass.

Execution guidance:
- Preserve the core shell: Home, Project Overview, Project Media, and Project Logs unless the user says otherwise.
- Keep the Media tab working. the user considers it the main driver of the app.
- It is acceptable to remove obsolete phase routes, phase-specific views, old overview subsections, and their frontend fetches in the same pass.
- If those UI removals orphan backend endpoints that only served the removed UI, delete those endpoints in the same pass rather than leaving dead surface area behind.
- Expect API contract tests to fail after this kind of deletion until the obsolete test coverage is pruned or rewritten. Typecheck first, then report the concrete stale-test fallout instead of pretending the suite should still be green.

For "basic metadata", prefer the smallest durable set that still helps orient the project. Current target:
- runtime target
- aspect ratios

Do **not** keep audience or target-platform metadata in Overview. the user considers both extraneous to the current workflow.
Do **not** keep phase/progress/checkpoint/admin clutter just because the data exists.

### Project init minimalism
the user wants Project Init to stay as light as possible. When simplifying project-init UI or persistence:
- required: name/title and description (`shortDescription` in current API)
- optional: runtime target and aspect ratios
- do not require or prominently surface audience
- do not require or prominently surface target platforms
- if removing audience/target-platform fields from the DB/API, also remove them from Overview and create-project contracts in the same pass so the UI and persistence model stay aligned

### Media inspector: no phase metadata field
In the project media inspector, do not render a dedicated `Phase` metadata row. If the system still stores `asset.phase` during transition, treat it as backend baggage or an eventual tag source, not as a primary UI metadata field. The inspector should stay focused on title, preview, ratings/color/tags, creation info, content type, size, filename, and media ID.

## Related

- `athabasca-shot-prompt-authoring` — shot prompt authoring patterns
- `athabasca-video-generation` — video generation via project API
- `references/stale-cache-debugging.md` — diagnosing broken-page-after-clean-build as stale browser cache, not a new bug
- `references/generation-log-list-pagination-overflow.md` — generation-log pagination, list-payload truncation, and horizontal overflow fixes
- `references/living-docs-route-stale-dev-server.md` — diagnosing a new SPA route that renders the homepage because the running dev service is stale
- `references/sqlite-migration-pitfall.md` — why `db:push` can wipe data on SQLite and how to use `ALTER TABLE` in `client.ts` instead
- `references/eden-treaty-date-coercion.md` — Eden Treaty silently turns date strings into Date objects; how it breaks sorting and the fix
