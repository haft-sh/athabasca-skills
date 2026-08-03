# Midjourney timeout recovery through Athabasca

Use this note when an Athabasca project-scoped Midjourney image generation request appears to time out or return no asset, but there is reason to believe the Discord-side job completed.

## Signal pattern

Typical pattern:
- `POST /api/projects/:slug/generate/image` runs long or the client times out.
- No new project media record appears immediately.
- The Midjourney grid is visible in Discord, or a standalone Discord/BYOA probe can fetch the result.

Interpretation:
- generation may have succeeded upstream;
- the failure surface is often persistence, polling/matching, or client timeout rather than image creation.

Do **not** assume rerun-first.

## Recovery sequence

1. Confirm whether the grid exists upstream.
   - Check Discord channel history or run the validated standalone Midjourney script.
   - If a grid exists, switch mental model from "generation failed" to "recovery and persistence needed".

2. Download the returned grid immediately.
   - Prefer `curl -L` against the Discord attachment URL.
   - Rationale: Discord CDN URLs are ephemeral, and Python `urllib` may return `403` even when `curl` works.

3. Persist through Athabasca.
   - Upload the recovered file via `POST /api/projects/:slug/media`.
   - Include provenance-rich metadata, not just a title.

4. Preserve Midjourney provenance.
   Recommended metadata fields:
   - `artifactKind: midjourney_grid`
   - `workflow: ...` (describe the operator workflow, e.g. image-prompt experiment or direct-discord recovery)
   - `provider: midjourney`
   - `model: midjourney-v8.1`
   - `discordMessageId`
   - `discordChannelId`
   - `mjJobId`
   - `mjButtons` (`U1`-`U4`, `V1`-`V4`, `reroll`)
   - source/reference asset IDs used to build the prompt

5. Attach to the relevant shot when applicable.
   - If the request was shot-specific, finish the workflow with the shot media attachment endpoint.

## Why this matters

Without recovery persistence:
- the canonical artifact stays stranded on an ephemeral Discord URL;
- future upscales/variations become harder because the button metadata is not captured in Athabasca;
- the user sees a timeout even though useful output already exists.

## Operator heuristics

- Treat long-running Midjourney requests as ambiguous until Discord is checked.
- Separate three states clearly:
  1. upstream generation failed,
  2. upstream generation succeeded but Athabasca did not persist/return it,
  3. Athabasca persisted it but attachment/reporting failed.
- Use reruns only after checking whether the image already exists upstream.

## Session-backed evidence

In a Prenup shot-regeneration session (May 2026):
- project-scoped Midjourney generation attempts timed out;
- direct Discord/BYOA runs for shot 3 and shot 7 succeeded;
- Discord CDN downloads worked via `curl -L` after Python `urllib` hit `403`;
- recovered grids were uploaded through project media, annotated with `mjButtons`/job metadata, and attached to the correct shots.

That makes this a durable recovery pattern, not a one-off anecdote.
