---
name: athabasca-schema-drift-repair
description: Safely reconcile Athabasca local DB schema drift before or during `bun run db:push`, especially when legacy bootstrap code or stale indexes keep resurrecting obsolete schema.
version: 1.0.0
author: Hermes Agent (Athabasca)
metadata:
  hermes:
    tags: [athabasca, schema, drizzle, sqlite, drift, migrations, db]
---

# Athabasca Schema Drift Repair

## Purpose

Use this skill when Athabasca's local SQLite DB has drifted from the current Drizzle schema and `bun run db:push` either:
- shows unexpected data-loss warnings for columns that should already be gone
- fails because old indexes or columns still exist locally
- keeps reintroducing legacy columns on app startup

This was validated against a real local drift case involving:
- stale `projects.workflow_mode`
- stale `media_assets_public_url_unique`
- bootstrap code in `src/server/db/client.ts` that re-added `workflow_mode`

## Core rule

Back up the DB before touching schema state.

Run first:
- `bun run db:backup`

Do not proceed until a backup path is returned successfully.

For destructive cleanup, do not trust project-detail JSON alone as proof that a relationship/table is dead. First inventory live references across:
- `src/server/db/schema.ts` relations and foreign keys
- backend bootstrap/service/worker code
- project routes and API schemas
- frontend components/types
- tests and fixtures
- the live DB row counts for candidate tables

If any candidate table is still used by active routes/workers/UI, pause and ask for a scope decision instead of deleting it under a broad "legacy" assumption.

## Typical symptoms

### Case A: `db:push` warns about deleting `workflow_mode`
This usually means one of two things:
1. the live DB still has legacy column `projects.workflow_mode`
2. `src/server/db/client.ts` still contains compatibility code that re-adds `workflow_mode` on startup

### Case B: report/image writes 500 on reused project-media URL
If `POST /api/projects/:slug/research-report` fails inserting into `media_assets` when reusing an existing project-media URL, check for stale unique index:
- `media_assets_public_url_unique`

Current intended behavior allows multiple `media_assets` rows to share the same `public_url` across different phase/report contexts.

## Investigation workflow

### 1. Back up
- `bun run db:backup`

### 2. Inspect live DB shape
Useful SQLite checks:
- `PRAGMA table_info(projects)`
- `PRAGMA index_list('media_assets')`
- candidate-table row counts before any `DROP TABLE`, e.g. `SELECT count(*) FROM shots;`

Look specifically for:
- `workflow_mode` in `projects`
- `media_assets_public_url_unique` in `media_assets`
- project columns that imply obsolete workflow state, generation defaults, or phase gating
- relationship tables that still contain real production data

### 3. Inspect schema/code mismatch
Check current source of truth:
- `src/server/db/schema.ts`
- `src/server/db/client.ts`
- `src/server/db/bootstrap.ts`
- `src/server/api/schemas.ts`
- `src/server/api/routes/projects.ts`
- `src/server/services/**` and `src/server/workers/**`
- `src/App.tsx` and `src/components/**`
- `tests/**`

Questions to answer:
- Does schema still define the column/index/table?
- Does bootstrap/client compatibility code still add or populate it at runtime?
- Are there routes, workers, services, UI views, or tests that actively read/write it?
- Is the desired product model truly media-only, or should active shot/storyboard tooling survive while only phase-gating tables are removed?

## Repair pattern

### Confirm product scope before destructive deletion
When the user requests a broad cleanup of project relationships, classify each candidate as one of:
- **obviously obsolete**: no active route/service/worker/UI/test references and no meaningful rows
- **API-shape debt**: still exposed in project detail but not otherwise useful; remove from schemas/responses before dropping tables
- **active subsystem**: currently used by workers/UI/routes, even if philosophically outdated

For active subsystems, ask a concrete scope question before deleting. Example: media-only cleanup may require removing `shots`, `storyboard_slots`, workers, job queues, UI components, and media attachment helpers, not just dropping joins. A narrower cleanup can preserve shot/storyboard tooling while removing phase status/default-provider fields and research/concept/approval joins.

### Fix legacy bootstrap first
If `client.ts` re-adds obsolete columns, remove that compatibility code before pushing.

Validated examples:
- remove `ensureWorkflowColumns()` logic that adds/updates `workflow_mode`
- when the product model is media-only, remove compatibility code that re-adds phase state/default generation columns instead of preserving it
- if media `phase` survives, treat it as tag migration input only: backfill `media_asset_tags`, then drop direct phase columns/foreign-key requirements

See `references/media-only-schema-cleanup.md` for the validated destructive-cleanup pattern.

### Clean up live DB drift
After backup and code fix, remove stale live artifacts.

Validated examples:
- drop stale unique index:
  - `DROP INDEX IF EXISTS media_assets_public_url_unique`
- drop stale legacy column when confirmed obsolete:
  - `ALTER TABLE projects DROP COLUMN workflow_mode`

Do not drop anything unless:
- backup already exists
- current schema no longer defines it
- you understand why it is obsolete

## Push workflow

Once code and live drift are aligned:
- `bunx drizzle-kit push --force`

Why `--force` was necessary in the validated case:
- Drizzle wanted to rebuild several SQLite tables after schema cleanup
- interactive confirmation is awkward in automation
- using `--force` is acceptable only after backup + review

## Verification checklist

Run all of these:
- `bun run db:guard`
- `bun test tests/api-contract.test.ts`
- `curl -sS http://localhost:3000/api/health`

Then re-check live DB shape if relevant:
- `PRAGMA table_info(projects)`
- `PRAGMA index_list('media_assets')`

Expected outcome for the validated case:
- `projects` no longer contains `workflow_mode`
- `media_assets` no longer contains `media_assets_public_url_unique`
- `db:push` no longer warns about deleting `workflow_mode`
- report-image URLs can reuse existing project-media URLs without 500s

## Practical notes

- On this repo, `bun run db:push` may surface broad SQLite table rebuild statements. Review them, but they can still be safe if they are rebuild-copy-rename operations and you already have a backup.
- `bun run db:guard` is the fastest sanity check that the local DB still exists, is non-empty, and has schema tables.
- If the app is already running, restart it after removing legacy bootstrap code so it stops reintroducing obsolete schema.
- **SQLite CHECK constraints on existing data**: Adding a CHECK constraint to a table that already has rows forces drizzle-kit to rebuild the entire table (DROP + CREATE + INSERT + RENAME). All FK-related tables get rebuilt too. The interactive "data-loss" warning is expected but **safe** when the new column has `default(N)` — existing rows get the default. Use `npx drizzle-kit push --force` because piping to the interactive prompt doesn't work reliably.
- **Zod `.default()` on query schemas makes Eden client types required**: If you add `.default("createdAt")` or `.default("desc")` to optional query params in a Zod schema, the Elysia Eden auto-generated client type marks those fields as required, breaking existing frontend calls. Use `.optional()` without `.default()` in the schema, and apply defaults in the route handler (`query.sortBy ?? "createdAt"`). This keeps the Eden client type optional while still providing server-side defaults.

## PITFALL: Adding NOT NULL columns to existing tables

When you add a `notNull().default(0)` column to a table that already has data via the Drizzle schema, `drizzle-kit push` generates a `DELETE FROM <table>` statement **without** a corresponding `INSERT INTO __new_table SELECT * FROM old_table`. This **will wipe your data**. SQLite's `ALTER TABLE ... ADD COLUMN` does not require a table rebuild, but drizzle-kit does not detect this.

**Safe pattern for adding columns to existing tables:**
1. Add the column definition to `src/server/db/schema.ts`
2. **Do NOT run `bun run db:push`** for this change
3. Add an `ALTER TABLE ... ADD COLUMN` migration in `src/server/db/client.ts` using the existing `ensureXxx()` pattern (check `PRAGMA table_info` to see if the column already exists before adding)
4. Add the `CREATE TABLE` and `CREATE INDEX` statements for new tables (these are safe since they are empty)
5. **Do NOT run `bun run db:push`** for this change. Even with `--force`, drizzle-kit generates `DELETE FROM <table>` without a corresponding `INSERT` back in. The data **will be lost**. The safe path is: ALTER TABLE at runtime + keep schema.ts in sync. Drizzle-kit's SQLite introspection always wants to rebuild tables it detects as "different," and it does not preserve data during that rebuild. Simply skip `db:push` for this change — as long as `schema.ts` matches the live DB shape (which it will, since ALTER TABLE added the same column definition), the app will work correctly.
6. If you must run `bun run db:push --force` for unrelated schema changes, it will attempt to rebuild the table you ALTERed. This is fine **only if** you have a backup and the new column has a default value (existing rows get the default, not deleted). But the cleanest approach is to avoid `db:push` for the ALTER COLUMN change entirely.
7. Verify data is intact: `SELECT count(*) FROM media_assets` (or whatever table you altered).

**Why this happens:** SQLite supports `ALTER TABLE ... ADD COLUMN` natively without rebuilding the table, but drizzle-kit's SQLite introspection always generates a full table rebuild plan. For existing tables with data, bypass drizzle-kit for the `ADD COLUMN` step.

## When to use this skill

Use it when:
- `db:push` behavior does not match your expectations from current schema.ts
- a supposedly fixed schema issue reappears after server restart
- local SQLite state is ahead/behind current code due to iterative refactors

Do not use it as a substitute for normal schema changes. For ordinary schema edits, follow the standard sequence:
1. edit `src/server/db/schema.ts`
2. `bun run db:push`
3. typecheck/tests
