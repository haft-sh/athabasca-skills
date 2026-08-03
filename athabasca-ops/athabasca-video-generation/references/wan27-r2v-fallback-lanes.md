# Wan 2.7 r2v fallback lanes for Prenup-style multi-reference coverage

Use this pattern when a lane pack is authored for 15s coverage but Wan 2.7 reference-to-video is being used as a fallback pass and the practical target should stay to a single clip per lane.

## Durable lessons

- Prefer **one compressed fallback clip per lane** over splitting each 15s lane into multiple Wan clips when the goal is apples-to-apples comparison against another provider's lane batch.
- For Wan fallback passes, compress 15s choreography into **10s** and **front-load the key motion** so the model does not spend precious duration on neutral setup.
  - Example: make the knee drop happen in the first second.
  - Example: make the ring-box snap begin immediately rather than lingering on anticipation.
- Keep the lane structure, references, and emotional intent intact; shorten timing blocks rather than rewriting the whole shot language.
- Before submitting any multi-reference lane batch, **verify that every referenced media URL resolves publicly**. A single 404 reference can cause Alibaba/Wan r2v submission or data-inspection failure.
- If a newer preview page points to a broken reference URL but the intended shot exists in an earlier valid preview/package, **fall back to the known-good asset URL** and continue the batch. Capture that substitution in provenance notes.
- For retries, use a **new idempotency key** when the reference set or prompt compression changes.

## Failure modes seen

- Alibaba Cloud / Wan r2v may fail with data-inspection errors like:
  - `InvalidParameter.DataInspection`
  - `Failed to download <reference-url>`
- These errors can be caused by broken public media URLs even when the prompt and model parameters are otherwise valid.

## Good retry strategy

1. Keep successful lanes as-is.
2. Isolate only the failed or stuck lanes.
3. Replace broken reference URLs with a known-good public asset for the same intended shot.
4. Resubmit only those lanes with fresh idempotency keys.
5. Preserve the same lane titles so outputs remain easy to compare in the Media page.
