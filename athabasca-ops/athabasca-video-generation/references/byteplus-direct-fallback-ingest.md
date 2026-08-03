# BytePlus Seedance direct fallback + Athabasca ingest

Use this only as a temporary escape hatch when the normalized Athabasca video route hangs or fails after you have already resolved a valid BytePlus Seedance request and a user needs the clip now. The durable fix remains the server-side adapter/normalizer.

## When this applies

- the user has approved a paid Seedance generation.
- Live capability/settings have been checked or are already known from the approved prompt preview.
- The normalized `POST /api/projects/:slug/generate/video` path is blocked by a runtime/tooling hang or a response-normalization bug.
- You can submit exactly the same intended generation to BytePlus, then ingest the returned MP4 into Athabasca immediately.

## Safety rules

- Use a stable idempotency key for the intended generation. Do not create a new paid upstream job just because a client call timed out.
- Preserve the user-requested settings in the provider payload: provider/model, duration, audio flag, aspect ratio, resolution, prompt, and reference assets.
- Keep source references as canonical Athabasca `asset.publicUrl` values, not local cache paths.
- After direct provider success, never report the upstream URL as the deliverable. Download the MP4, upload it as Athabasca generated media, and report the Athabasca/R2 URL.
- Include provenance noting that this was a direct BytePlus fallback for a normalized-route issue.

## Verification checklist

1. Provider task reaches terminal success.
2. Downloaded MP4 is non-empty and inspectable.
3. `ffprobe` or equivalent confirms expected duration, video dimensions, and audio stream when audio was requested.
4. Athabasca upload returns `201`/`ok: true` and a generated video asset.
5. The returned `asset.publicUrl` answers with a video content type (a `206` response to a range request is fine for MP4).
6. Verify attachment/project-media visibility when shot/project attachment was expected.

## Reporting

Keep the user-facing report terse:

- generated via BytePlus / Seedance 2.0
- settings actually used
- Athabasca asset ID
- Athabasca public URL or inline video
- one short note that the normalized route was bypassed and the result was persisted back into Athabasca

Do not turn the transient route/tool failure into a durable negative claim that the normalized API is broken; classify it as a current blocker and pursue a code fix if it recurs.