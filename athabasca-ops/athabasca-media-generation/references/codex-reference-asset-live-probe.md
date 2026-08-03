# Codex `referenceAssetIds` Live Probe Pattern

## Lesson

Do not treat an old warning or guardrail such as `Reference images are not supported for openai-codex generation in v1` as authoritative without checking the current live route. In a live session, the user explicitly challenged this assumption. A live `POST /api/projects/:slug/generate/image` with `provider: "openai-codex"`, `model: "gpt-image-2"`, and multiple `referenceAssetIds` succeeded with `201` and produced a persisted R2 PNG.

## What worked

Use the canonical project-scoped route and pass the intended provider/model explicitly:

```json
POST /api/projects/:slug/generate/image
{
  "provider": "openai-codex",
  "model": "gpt-image-2",
  "prompt": "...",
  "aspectRatio": "square",
  "referenceAssetIds": ["asset_...", "asset_..."],
  "title": "...",
  "provenanceNote": "..."
}
```

Expected success shape:
- HTTP `201`
- `asset` persisted under project media
- `generation.provider` = `openai-codex`
- `generation.model` = `gpt-image-2`
- `generation.parametersJson.referenceAssetIds` contains the input IDs
- R2 public URL verifies with `curl -L` as a valid PNG

## Operator rule

When a capability warning may be stale:
1. State that it is an unverified code/doc claim, not a fact.
2. Try the smallest safe live request through the normal Athabasca API.
3. If it succeeds, update the guardrail/skill/docs and proceed through the normal path.
4. If it fails, capture the exact HTTP status/body and only then call it unsupported.

## Implementation note

The native Codex path can support references by loading Athabasca media assets and passing them through the Responses request as `input_image` content parts alongside the prompt `input_text`. The important workflow lesson is not the exact patch from one commit, but that the normalized API should be live-probed before falling back to fal-ai or declaring a capability unsupported.

## Verification quirk

Python `urllib` may receive `403` from some R2 public media URLs while `curl -L` succeeds. For media verification, prefer `curl -L -s -o /tmp/file -w ...` and then inspect the PNG signature/byte size.
