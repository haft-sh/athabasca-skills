# Text-only project brief persistence fallback

Use this reference when a new Athabasca project starts from a chat brief with no uploaded media, and the brief itself should be durable project state.

## Pattern observed

1. Create the project through `POST /api/projects` as usual.
2. Preserve the full user brief as a phase report, usually `phase: "init"`, rather than only relying on top-level `shortDescription`/`objective` fields.
3. Record the supplied source URL (for example, a YouTube track) as a research source, but do it idempotently: check existing project sources first or dedupe immediately after verification.
4. Verify with `GET /api/projects/:slug` that:
   - the project exists;
   - the `researchReports` array contains the init report;
   - the `researchSources` array contains one canonical source record, not duplicates.

## Fallback when the report POST route is not exposed

Some local Athabasca builds may not expose a `POST /api/projects/:slug/research-report` route in OpenAPI even though the repo still has the DB bootstrap helper used by seed/bootstrap paths.

If the live API route is absent, and you are operating inside the Athabasca repo, a narrowly scoped Bun script can call the existing helper rather than hand-editing DB rows:

```ts
import { createResearchSourceForProjectSlug, upsertResearchReportForProjectSlug } from "./src/server/db/bootstrap";

await upsertResearchReportForProjectSlug("<slug>", {
  phase: "init",
  title: "Initial Project Brief",
  summary: "User-supplied initial brief.",
  contentMarkdown: "# ...full preserved brief...",
  images: [],
});

await createResearchSourceForProjectSlug("<slug>", {
  sourceType: "video",
  title: "...",
  url: "https://...",
  publisher: "...",
  summary: "...",
  notes: "User supplied in initial brief.",
});
```

Run it from the repo root with `bun script.ts`, then verify through the API. Treat this as a fallback for local repo ops, not as the preferred production API path.

## Pitfall: duplicate sources

`upsertResearchReportForProjectSlug` is idempotent per project+phase, but `createResearchSourceForProjectSlug` creates a new row each time. If you rerun the script after adding a note, you can duplicate the same source URL. Avoid by checking existing sources first, or clean duplicates before reporting success.
