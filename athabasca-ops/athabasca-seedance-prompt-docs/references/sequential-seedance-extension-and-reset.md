# Sequential Seedance extension and images-only reset

Use this when a prompt-preview scene is dispatched group by group and adjacent groups may be chained for continuity.

## Continuation path

1. Persist Group N and use its canonical Athabasca `publicUrl`.
2. Dispatch Group N+1 with the prompt document's canonical image references in the same `@imageN` order.
3. Add Group N as the sole video reference.
4. If requested, change only the first line to a continuation instruction such as: `I want you to extend video one and generate the following shots.`
5. Keep the rest of the approved group prompt unchanged unless the user provides corrections.
6. Use a distinct idempotency key for each group and reuse it for retries of that same generation intent.

## When extension over-conditions the next group

A prior clip can propagate or amplify errors. Symptoms include:

- duplicate protagonists
- duplicated or mirrored shelves/walls
- multiple copies of the destination character
- inherited facial blotches
- inherited wrong glow color or eye design

When the user rejects the extension for those reasons, reset deliberately:

1. Remove the video reference entirely. Do not extend the rejected clip again.
2. Keep the canonical image references and text prompt; for image-reference-capable Seedance this can still use `reference-to-video` mode with no `referenceVideoUrls`.
3. Replace stale character references with the exact asset IDs specified by the user.
4. Add count and geography constraints: exactly one protagonist, one destination character, one continuous shelf wall, and one clear route between them.
5. Explicitly prohibit the recurrent wrong features and state the desired treatment precisely, including source, color, and locality of any glow.
6. Record in provenance that this is an images-only reset rather than a continuation.

## Reference semantics

- A user-specified asset override supersedes the older card in the preview document.
- Keep `@imageN` order aligned with the request's image-reference array.
- For visor/display characters, distinguish flat graphic overlays from anatomical eyes in both positive and negative language.
- For room-crossing action, identify a single origin, a single destination, and a fixed spatial axis.

## Verification

- Verify the persisted Athabasca asset and project attachment.
- Probe duration, dimensions, and audio stream.
- Review representative frames for duplicates, room geography, identity, and effect color.
- If a requested micro-change might occur between sparse samples, inspect denser frames around that beat before declaring it absent.
