# Media-only schema cleanup pattern

Use when Athabasca is intentionally removing legacy phase-gated project relationships and keeping project content as media attachments plus tags.

## Safety sequence

1. Back up the live local DB first with `bun run db:backup`.
2. Count every destructive candidate table before dropping it, especially:
   - `phases`
   - `project_phase_plans`
   - `research_sources`, `research_insights`, `reference_items`
   - `concept_route_documents`, `visual_directions`
   - `shots`, `shot_jobs`, `storyboard_slots`, `storyboard_variations`
   - `approval_decisions`, `research_reports`, `source_excerpts`
3. Export those legacy tables to a JSON backup before dropping them. A dedicated migration script can write `data/backups/*-legacy-workflow-*.json`.
4. Preserve provenance instead of preserving joins:
   - non-project media attachment targets become project attachments with `legacyAttachmentTarget` stored in `metadata_json`
   - `media_generations.shot_id`, `scene_id`, and `shot_number` move into `parameters_json.legacyShotContext`
   - media `phase` values become rows in `media_asset_tags`
5. Rebuild `projects` without workflow/default-generation columns:
   - remove `current_phase`, `workflow_profile`, `phase_statuses`, `latest_approval_state`
   - remove text/image/video generation default provider/model columns
6. Rebuild `media_generations` without shot/scene columns.
7. Drop legacy workflow/content tables.
8. Run `PRAGMA foreign_key_check` before declaring success.
9. Run `bunx drizzle-kit push --force` only after the backup/export exists; expect SQLite copy/rename table rebuilds.
10. Verify:
   - `bun run db:guard`
   - `bun run typecheck`
   - `bun test tests`
   - a final SQLite check that no legacy candidate tables still exist and media/project counts are retained.

## Code cleanup checklist

Remove or adapt all references across:
- `src/server/db/schema.ts` relations and inferred types
- `src/server/db/bootstrap.ts` project-detail joins
- `src/server/db/client.ts` compatibility bootstraps that re-add deleted columns
- `src/server/api/routes/projects.ts` and `src/server/api/schemas.ts`
- generation/audio workers that still pass `shotId` into media generation records
- frontend components and CSS for shots/storyboard/clips phase views
- restore scripts, contract tests, and docs/skills that mention deleted routes or tables

## Expected product behavior after cleanup

- Project detail exposes core project fields plus media, not phase state, generation defaults, shots, storyboard slots, reports, excerpts, or approval joins.
- `/generation-settings` is not mounted.
- Phase-like strings are accepted only as media tags/filter inputs.
- Old relationship data is recoverable from backup/export but no longer part of runtime schema.