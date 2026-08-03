# Wan 2.7 Video Edit + Reference Image (Athabasca normalized API)

## What was validated

Runtime validation succeeded using Athabasca normalized endpoint:

- Endpoint: `POST /api/projects/:slug/generate/video`
- Provider: `alibaba-cloud`
- Model: `wan2.7-videoedit`
- Mode: `video-editing`
- Inputs:
  - `videoUrl` (source video)
  - `referenceImageUrls` (character sheet still)

Observed success response included `ok: true`, generated `asset` row, and `generationInfo` with job metadata.

## Why this matters

Capabilities/schema can imply support, but this run confirms practical acceptance of `referenceImageUrls` for Wan 2.7 video-edit in Athabasca's live path.

## Minimal probe payload

```json
{
  "prompt": "Keep everything identical; test support for reference image in video edit.",
  "mode": "video-editing",
  "provider": "alibaba-cloud",
  "model": "wan2.7-videoedit",
  "videoUrl": "https://...source.mp4",
  "referenceImageUrls": ["https://...reference.jpg"],
  "duration": 2,
  "aspectRatio": "landscape",
  "resolution": "720p"
}
```

## Operational pitfalls

### 1) Client/tool timeout vs server outcome

If the request appears to "hang" or returns timeout 124, distinguish:

1. curl-level timeout (`--max-time` too low)
2. Hermes terminal tool timeout (tool call timeout too low)

Raise both for definitive runtime validation.

### 2) 10s Wan 2.7 video-edit can fail upstream at ~600s

In production-style face-replacement attempts, 10s runs repeatedly failed with upstream errors of the form:

`Alibaba Cloud video generation timed out after 600s. Task ID: ...`

This is distinct from client-side timeout. In these cases:

- generation log entries are created and move `pending -> failed`
- no output `assetId` is produced
- retrying with a fresh key may still fail the same way

### 3) Practical delivery fallback when user needs output now

If repeated 10s attempts fail due upstream 600s timeout:

- keep idempotency protection enabled
- switch to a shorter duration fallback (e.g., 5s) to produce a deliverable clip
- clearly report that 10s is blocked by provider timeout, not by Athabasca wiring
