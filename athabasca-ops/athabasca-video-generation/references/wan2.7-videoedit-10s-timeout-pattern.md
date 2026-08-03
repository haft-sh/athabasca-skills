# Wan 2.7 video-edit 10s timeout pattern (session note)

## Context
Project: `scorpion-accuracy`
Flow: normalized `POST /api/projects/:slug/generate/video`
Model: `alibaba-cloud/wan2.7-videoedit`
Mode: `video-editing`
Settings repeatedly tested: `duration=10`, `resolution=720p`, `aspectRatio=landscape`, source video + reference face image.

## Observed behavior
- Client requests often timed out first (`ReadTimeout` at 300–360s), while server logs still showed `pending`.
- Polling by `idempotencyKey` showed eventual terminal `failed` with upstream error:
  - `Alibaba Cloud video generation timed out after 600s. Task ID: ...`
- This happened across multiple independent idempotency keys, indicating provider runtime limitation rather than local DB/schema issues.

## Practical handling
1. Always submit with `idempotencyKey`.
2. After client timeout, poll generation logs for terminal status before any resubmit.
3. If repeated 10s runs fail with the same 600s upstream timeout signature, classify as provider limitation for that request shape.
4. When user wants an immediate deliverable, run a shorter fallback (e.g., 5s) with a **new** explicit key and disclose fallback reason.

## Why it matters
This pattern prevents duplicate paid generations and gives a clean failure classification: upstream provider execution ceiling vs. local Athabasca routing/persistence bugs.
