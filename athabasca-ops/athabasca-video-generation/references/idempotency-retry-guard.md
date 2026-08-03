# Video generation idempotency retry guard (Athabasca)

## Why this exists
Video generations are paid and often take >60s. Client/tool timeouts can make completion ambiguous. Blind retries on a non-idempotent endpoint can create duplicate paid jobs and duplicate assets.

## Implemented behavior (server)
`POST /api/projects/:slug/generate/video` supports optional `idempotencyKey`.

- If a matching generation log for `(projectSlug, kind=video, idempotencyKey)` is `pending`:
  - API returns `409` with error `generation_request_in_progress_for_idempotency_key` (plus existing log id).
- If a matching log is `completed` with `assetId`:
  - API returns existing asset (`200`) and does not submit a new upstream generation.

Schema/storage additions:
- `generation_logs.idempotency_key` column
- index on `(project_slug, kind, idempotency_key)`

## Agent/operator usage
1. Generate and send a stable idempotency key for one intended generation attempt.
2. On transport timeout or uncertainty, retry with the SAME key.
3. Treat `409 in progress` as expected dedupe behavior (wait/poll), not as a reason to regenerate.
4. Use a NEW key only when intentionally requesting a new output.

### Polling discipline after client timeout (important)
For long generations, client timeouts can happen before the server reaches terminal state.

Recommended pattern:
1. Submit once with `idempotencyKey`.
2. If client times out (e.g., 300–360s), do **not** submit a new request immediately.
3. Poll `GET /api/projects/:slug/generation-logs` every 10–15s for that key until terminal state (`completed`/`failed`/`cancelled`).
4. Only when terminal `failed` should you decide whether to launch a fresh attempt with a new key.

This avoids duplicate paid jobs while a prior run is still executing upstream.

## Practical key recipe
Build key from deterministic request intent fields (then hash if needed):
- `projectSlug`
- `mode`
- `provider`, `model`
- normalized prompt string/hash
- source media IDs (video/image/audio/reference)
- `shotId` (if present)

Example logical form:
`video:<slug>:<mode>:<provider>:<model>:<promptHash>:<srcHash>:<shotId|none>`

## Test expectations
Add/maintain API tests for:
- duplicate key while first is pending -> `409`
- duplicate key after completion -> returns existing asset, no new upstream job
