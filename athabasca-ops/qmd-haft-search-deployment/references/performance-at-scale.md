# Haft Performance at Scale — BBT Vault (13,383 pages)

Measured 2026-07-24 on bbt.haft.sh (t3.large, 2 vCPU / 8GB).

## Payload sizes (single request, no compression)

| Endpoint | Size | Contents |
|----------|------|----------|
| `/api/reader/navigation` | 11.1 MB | All 13,383 pages with slugs, prev/next, chunkIds |
| `/api/vault/tree` | 9.6 MB | Full recursive tree with metadata per node |
| `/api/vault/files` | ~2-4 MB (est.) | All content + asset files |

Total initial load: ~23 MB JSON before any user interaction.

## Frontend architecture (apps/web/src/app-shell/)

- `data-loading.ts` (line 433-436): fetches `/api/vault/files` and `/api/vault/tree` in parallel on mount
- `VaultBrowserTree.tsx`: renders tree rows as real DOM nodes, no virtualization
  - `collectVisibleTreeRows()` flattens expanded subtrees into a flat array
  - Only expanded folders contribute rows (default: all collapsed = ~20 top-level)
  - BUT: expanding a large book (e.g. SB Canto 10, 1000+ verses) creates all DOM nodes at once
- `vault-browser-tree.ts`: `buildLibraryTree()` maps VaultTreeResponse → LibraryTreeNode[] recursively
- No lazy loading, no depth limiting, no pagination on tree or navigation

## What's safe today

- Tree is collapsed by default → initial DOM is just ~20 folder rows
- Search is already paginated (cursor-based, max 50/page)
- `collectVisibleTreeRows` only processes expanded subtrees

## What breaks at scale

1. **Initial load time**: 23 MB download + parse + React state hydration = 2-4s on 100Mbps, 10-30s on mobile
2. **Large folder expansion**: Expanding SB Canto 10 (1000+ files) creates 1000+ DOM nodes in one render pass → visible jank
3. **Memory**: ~30 MB JS heap for tree data alone, plus React reconciliation overhead
4. **Cmd+A (select all)**: `collectAllTreeRows(tree)` flattens ALL 13K nodes regardless of expansion state

## Proposed fixes (priority order)

### 1. API depth-limiting + lazy expansion (server + client)
- `GET /api/vault/tree?depth=1` → top-level only (~5 KB)
- `GET /api/vault/tree/children?path=<folder>&depth=1` → on-demand
- Frontend fetches children on expand, caches in Map<string, LibraryTreeNode[]>
- Eliminates 9.6 MB initial download

### 2. Navigation split (server)
- Remove bulk `/api/reader/navigation` from initial load
- Use `/api/reader/pages/by-slug?slug=...` for single-page lookup (already exists)
- Add `/api/reader/navigation/adjacent?pageId=...` for prev/next only
- Eliminates 11 MB initial download

### 3. Virtualization (client)
- `@tanstack/react-virtual` on the flat `visibleTreeRows` array
- Fixed row height (~30px) makes this trivial
- Only ~50 DOM nodes in viewport regardless of expansion
- Fixes jank on large folder expansion and Cmd+A

### 4. Files pagination (server, low priority)
- `GET /api/vault/files?cursor=...&limit=100&folder=<path>`
- Grid view already shows one folder at a time, so less urgent
