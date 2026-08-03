# Seedance continuity-first policy

Use for sequential, reference-conditioned narrative video where character identity, props, screen direction, geography, or camera continuity matter.

## Winning operating policy

- Attach the immediate predecessor frame first. It is the authority for camera axis, lighting/grade, canyon/environment, scale, and the exact outgoing prop/posture state.
- Then attach canonical hero identity, canonical opposing-character identity, and geography reference—in that order.
- Prefer short timed hard-cut groups and locked framing. Do not add generic camera motion, creep-ins, lateral drift, or “cinematic movement” unless the shot needs it and it is explicitly approved.
- State props through visible contact only: e.g., “shield strapped to right forearm” and “left hand visibly grips sword handle.” Avoid invented unseen mechanics, undefined sheaths, or pose-specific blade directions.
- For transitions (fall, climb, stow, arm/hand changes, shrink stages), author a discrete helper clip or sequential group with one clear incoming and outgoing state. Do not leave a multi-action transition implicit inside a long multishot render.
- Reuse the selected usable outgoing frame—not automatically the literal final frame—as the next group’s first reference.

## QA / provenance

- New semantic prompt or reference changes require a new, reviewable packet and a source/submission hash check before dispatch.
- If a generation call times out, query generation logs/idempotency before resubmitting; server-side work may have completed.

## Failure diagnostics

- Floating prop: wording conflicts with the reference or has no visible attachment/contact relation.
- World/lighting reset: predecessor frame is underweighted or conflict-heavy additional refs compete with it.
- Axis drift: restate screen positions only at shots where both characters are visible and remove competing blocking references.
