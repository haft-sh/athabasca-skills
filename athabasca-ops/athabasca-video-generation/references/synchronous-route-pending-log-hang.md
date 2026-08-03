# Synchronous video route pending-log hang

## Trigger

Use this note when `POST /api/projects/:slug/generate/video` appears to hang or the caller gets a generic HTTP client/transport error, but direct provider submission succeeds.

## Observed pattern

A normalized video generation request can create a generation log with `status: "pending"` and then never update it to `completed` or `failed`.

Typical log evidence:
- provider/model are resolved correctly
- `resolvedParamsJson` is populated
- `upstreamRequestJson` is `null`
- `upstreamResponseJson` is `null`
- `assetId` / `outputAssetId` is `null`
- `upstreamError` / `errorMessage` is `null`
- a direct provider request with the same payload succeeds

## Likely cause

The normalized route is doing a long synchronous provider job inside one HTTP request:

1. create pending generation log
2. submit/poll provider job
3. download provider output
4. upload/persist media
5. mark the generation log complete/failed

For long video generations, the client, proxy, tool wrapper, or undici transport can abort before the server reaches the completion/failure update. If the post-log provider call is not wrapped by a broad `try/catch`, the log remains a zombie `pending` row.

## Debug sequence

1. Query project generation logs before retrying. Do not submit a new paid generation with a new idempotency key until the existing key is classified.
2. If logs show pending rows with no upstream request/response/error, suspect route lifecycle/exception cleanup before suspecting the creative prompt.
3. Compare against a direct provider probe only if needed; if direct succeeds, ingest the output back into Athabasca with provenance rather than leaving it on provider storage.
4. Inspect service logs for route-level exceptions or aborted request symptoms, but absence of logs does not rule out the lifecycle bug.

## Fix direction

Short-term code fix:
- wrap the post-log provider/persistence block in `try/catch`
- on any thrown exception, call `failGenerationLog(log.id, { upstreamError, upstreamRequestJson, upstreamResponseJson, upstreamJobId, generationTimeMs })` when available
- return a structured failure instead of leaving `pending`

Better architecture:
- make `/generate/video` enqueue a generation job and return quickly with `logId`
- run provider polling/download/upload in a background worker
- expose status polling through generation logs

## Reporting to the user

Say clearly whether the evidence points to:
- prompt/provider rejection
- provider adapter bug
- HTTP lifecycle/client timeout
- missing failure cleanup after pending-log creation

Do not report a synchronous-route abort as a creative prompt failure when the same provider payload succeeds directly.