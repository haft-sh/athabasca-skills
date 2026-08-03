# Living Docs route shows Projects list — stale dev server check

## Symptom

A project route such as `/projects/:slug/living-docs` renders the same project-list UI as the homepage.

## Likely cause

If the local `readRoute()` implementation already recognizes the route and the render tree has a matching branch, the browser is probably hitting a stale running dev service or old frontend bundle, not missing route code.

Athabasca's SPA router intentionally falls back to `{ kind: "home" }` for unknown path shapes, so a stale server/bundle can make a new route look exactly like the homepage.

## Debug sequence

1. Inspect `src/App.tsx` route parsing first:
   - `readRoute()` should match the path shape before more general project routes.
   - The render tree should have a `route.kind` branch for the page.
2. If the code is present locally, do not keep editing route logic. Treat it as a runtime freshness problem.
3. Rebuild/typecheck after any small server/frontend patch:
   - `bun run build`
   - `bun run typecheck`
4. Restart the running Athabasca dev service so it picks up the current source/bundle:
   - `systemctl --user restart athabasca-dev.service`
5. If avoiding disruption to the live dev service, run an alternate instance on a different port, but only if `src/index.ts` honors `process.env.PORT` / `Bun.env.PORT`.

## Implementation note

For isolated test servers, the Bun entrypoint should bind from an environment override, e.g. defaulting to `3000` only when `PORT` is absent. Without this, `PORT=4173 bun run dev` may still try to occupy `3000` and falsely look like every alternate port is unavailable.

## Communication note

When the user reports that a new frontend route "looks identical to the homepage," lead with the practical diagnosis and the exact restart/test URL. Avoid a long explanation unless the restart fails or the code is actually missing.
