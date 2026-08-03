# BytePlus provider validation pattern

Use this when the user adds BytePlus as a new provider and wants to know whether it is truly wired up.

## Goal

Separate three different failure classes cleanly:
1. capability/config exposure
2. server runtime env loading
3. upstream BytePlus moderation/privacy rejection

## Recommended validation sequence

1. **Check live capabilities first**
   - `GET /api/generation/video-capabilities`
   - Confirm `provider: "byteplus"` exists and the expected model IDs are advertised.
   - For Seedance 2.0, confirm the intended mode (`image-to-video`, `text-to-video`, or `reference-to-video`) is listed.

2. **Show the exact request JSON before dispatch when the user is validating wiring**
   - If the user wants to double-check params, present the exact body that will be POSTed to `/api/projects/:slug/generate/video`.
   - Do not paraphrase or summarize the payload.
   - Include the actual `idempotencyKey` you plan to use.

3. **Submit once and classify the first failure carefully**
   - If the route returns a missing-key error such as `BYTEPLUS_ARK_API_KEY environment variable is not set`, this does **not** mean the config file is missing the key.
   - Verify whether the key exists in the service env file, then check the running service environment.
   - If the env file has the key but the long-running service does not, restart the Athabasca service and retry with a **new idempotency key**.

4. **Use the generation log to separate local/runtime errors from upstream errors**
   - Inspect `GET /api/projects/:slug/generation-logs/:logId`.
   - If `upstreamRequestJson` is null and the error is a missing env key, the request failed before reaching BytePlus.
   - If the log shows a BytePlus 400 with an upstream request id, the provider path is live and the failure is upstream moderation/validation, not wiring.

## Interpretation rules

### Case A — missing env key on first attempt

Typical pattern:
- env file contains `BYTEPLUS_ARK_API_KEY`
- route still says key is missing
- log status is `failed`
- `upstreamRequestJson` is null
- `upstreamError` says key missing

Interpretation:
- the running service has stale environment state
- restart the service before concluding BytePlus is broken

### Case B — upstream moderation/privacy rejection after restart

Typical BytePlus error:
- `InputImageSensitiveContentDetected.PrivacyInformation`
- message like `input image may contain real person`

Interpretation:
- BytePlus is wired correctly
- auth is loaded
- request reached the provider
- failure is provider-side moderation/privacy policy
- no asset should exist

Do **not** misreport this as an Athabasca routing failure.

## Reporting template

For a provider-wiring test, keep the conclusion explicit:

- `Capabilities:` provider/model visible or not
- `Runtime:` service env loaded or required restart
- `Provider reachability:` request reached BytePlus or failed locally
- `Outcome:` generated / moderated / validation failed
- `Asset:` public URL if present, otherwise state that no asset was created

## Seedance-specific note

For the user's default Seedance test posture:
- prefer `480p`
- set `generateAudio: true`
- when doing a real lane test, keep the canonical lane prompt unchanged unless the goal is a sanitized probe
- Runtime pitfall observed 2026-06-05: BytePlus Seedance 2.0 image-to-video rejected `duration: 3` with `the parameter duration specified in the request is not valid for model dreamina-seedance-2-0 in r2v`, despite Athabasca capabilities advertising 1–15. Treat Seedance i2v as minimum 4s unless the server capability adapter is updated and live-tested.

## When you need a clean end-to-end probe

If a face-heavy lane is rejected upstream, run a no-face/object-only BytePlus probe next. That validates:
- provider auth
- request submission
- polling
- asset persistence
- public URL verification

without confounding moderation on real-person imagery.
