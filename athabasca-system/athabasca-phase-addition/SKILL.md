---
name: athabasca-phase-addition
description: Use when adding a new production phase to Athabasca or changing the phase lifecycle. Covers schema, API routes, frontend phase views, docs, tests, and future foreign-key wiring for phase-scoped artifacts.
---

# Athabasca Phase Addition

Use this skill when you are introducing a new phase to Athabasca, such as stills generation, video generation, shot list refinement, VFX review, or any other phase that becomes part of the project lifecycle.

## Canonical Order

Treat `src/server/db/schema.ts` as the source of truth. If a phase changes there, update the rest of the system to match.

## Workflow

1. Read `src/server/db/schema.ts` first.
2. Add or update the phase in the schema.
3. Avoid adding phase-scoped tables/enums/foreign keys unless the user explicitly asks to reintroduce phase-gated system behavior.
4. Update bootstrap/data-layer helpers in `src/server/db/bootstrap.ts` and any related DB modules.
5. Update API schemas in `src/server/api/schemas.ts`.
6. Add or update routes in `src/server/api/routes/`.
7. Update the read-only frontend in `src/App.tsx` and `src/index.css` if the new phase should be visible in the UI.
8. Add or update reusable workflow guidance as skills or concise docs, not `docs/phases/` playbooks.
9. Update current specs/docs that still exist and match the runtime contract.
10. Add contract tests in `tests/api-contract.test.ts`.
11. Run `bun run db:push`, `bun run typecheck`, and `bun test tests`.

## What Usually Changes

### Schema

- Add the new phase to `canonicalPhaseSeeds`.
- Add it to `defaultProjectPhaseStatuses`.
- Add it to `approvalTargets` if approvals apply to the phase.
- Add tables instead of storing phase payloads in blobs when the phase has structured data.
- Add foreign keys early if future media or generated artifacts will attach to phase items.

### API

- Add list/read endpoints for the phase.
- Add create/update endpoints only if the phase should be mutated through the API rather than chat-driven replacement.
- Keep route validators in sync with the data model.
- Return `400` for validation problems and `404` for missing project/phase resources.

### Frontend

- Add a phase entry in the project navigation/order if the phase should be visible.
- Keep the UI read-only unless there is a strong reason to add direct editing.
- Render structured data explicitly; do not flatten it into generic blobs.

### Docs

- Prefer a skill/reference doc for reusable workflow guidance; do not recreate obsolete phase playbooks by default.
- Keep the playbook aligned with the schema and routes.
- Update the phase index and workflow docs in the same change.

### Tests

- Cover the happy path.
- Cover at least one 404 case.
- Cover validation failures for malformed payloads.
- If the phase changes project progression, assert the new phase state explicitly.

## Design Rules

- Prefer explicit tables over polymorphic JSON blobs.
- Keep enums small and operationally meaningful.
- Add foreign keys aggressively.
- Do not hardcode phase assumptions in the frontend.
- Do not update docs without updating schema and routes first.

## Good Default Sequence

When adding a phase for a new artifact type, follow this order:

1. Define the phase and data model.
2. Add the API contract.
3. Wire persistence and relationships.
4. Expose the phase in the UI.
5. Document the workflow.
6. Lock it down with tests.

## Example Future Uses

This skill should be used for work such as:

- adding a stills generation phase
- adding a video generation phase
- adding a storyboards phase
- adding a review/approval phase with structured records
- adding any new phase that needs its own persistent rows and API surface
