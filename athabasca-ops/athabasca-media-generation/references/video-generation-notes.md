# Video generation notes absorbed from `athabasca-video-generation`

## Canonical route

`POST /api/projects/:slug/generate/video`

## Required preflight

- Check health endpoint
- Query `GET /api/generation/video-capabilities`
- Use live provider/model IDs and exposed constraints

## Default operating approach

- Prefer lowest-cost practical settings unless the user asks otherwise
- Upload source stills, audio, and reference media into Athabasca first
- Use normalized request fields and let server-side adapters map provider payloads
- Verify returned Athabasca asset/public URL and expected shot attachment

## Important video safeguards

### Idempotency

Always send an `idempotencyKey` for retriable paid generation requests. Reuse the same key for retries of the same intended generation; do not mint a new key unless you explicitly want a fresh paid run.

### Timeouts

Video requests can exceed a minute. Distinguish:
- client curl timeout
- Hermes terminal-tool timeout
- provider-side terminal failure after the request remained pending server-side

### Failure classification

Classify failures as:
- prompt/content issue
- invalid normalized settings
- service env / missing key issue
- capability metadata mismatch
- adapter mapping bug
- upstream provider limitation
- account/billing issue
- persistence/attachment bug after success

## Known recurring provider patterns captured from the absorbed skill

- Some Alibaba/Wan request shapes are sensitive to typed `input.media` entries rather than legacy fields
- For certain reference-to-video audio-conditioned flows, a black-screen MP4 wrapper can be a pragmatic canonical input
- If a route should have known an invalid combination up front, prefer fixing validation/capabilities/tests over growing the skill body with model-specific folklore

## Support references still worth consulting

- `references/provider-quirks.md`
- `references/black-screen-audio-wrapper.md`
- `references/idempotency-retry-guard.md`
- `references/wan-r2v-reference-inputs.md`
- `references/wan2.7-videoedit-image-reference.md`
- `references/wan2.7-videoedit-10s-timeout-pattern.md`
- `references/external-video-import.md`
- `references/seedance-2-fal-notes.md`
