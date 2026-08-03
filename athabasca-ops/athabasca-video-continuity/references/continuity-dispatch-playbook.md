---
name: athabasca-video-continuity-dispatch
description: Prepare, dispatch, and verify continuation or multi-group AI-video generations that must preserve prior-shot visual continuity and recurring-character identity.
---

# Video Continuity Dispatch

## Use when

Use for a downstream video group, partial rerun, post-cut continuation, or any render expected to join an existing generated clip without a visible reset.

## Core rule

A prose instruction to preserve continuity is insufficient. Attach the actual stable predecessor frame and the canonical identity reference for every visible recurring character.

## Workflow

1. **Identify the cut boundary.** Inspect the source clip around the intended handoff; choose a stable pre-cut or final frame, not a frame affected by the failure being repaired.
2. **Persist the frame.** Extract it, upload it as project media, and record source clip asset ID, timestamp, frame SHA-256, new frame asset ID, and immutable URL.
3. **Build the reference budget in order.**
   - first: predecessor frame — first-frame/camera/environment authority;
   - then: canonical sheets for every visible recurring character;
   - then: environment/geography reference.
   Drop abstract composition/blocking references before dropping any visible character identity sheet.
4. **Write an explicit continuation lock.** Require the opening frame to be the next instant after the predecessor frame. Lock camera axis, character positions, prop state, canyon/room layout, key direction, exposure, grade, atmosphere, and shadow direction. Explicitly forbid relight, daylight/sky reset, environment swap, grade reset, and axis flip.
5. **Preserve approved shot controls.** A changed duration, reference set, or continuation split requires a new versioned kit. Retain existing approved shot text verbatim except for reviewed, explicitly scoped revisions.
6. **Dispatch with provenance.** Store kit asset ID/URL, normalized prompt hash, submitted prompt hash, ordered references, provider/model/mode/settings, predecessor-frame facts, and acceptance criteria. Do not submit if source/submission hashes differ.
7. **Verify before acceptance.** Compare the generated first frame side-by-side with the predecessor frame, then inspect each hard cut for lighting/environment resets and character drift. Mark a failed candidate yellow; do not silently reuse it as an authority.

## Acceptance checklist

- First generated frame matches predecessor geometry, light direction, exposure, grade, atmosphere, and camera axis.
- No abrupt environment or lighting reset in the first second or across internal hard cuts.
- Every visible recurring character matches its canonical sheet, including face, proportions, wardrobe, props, and markings.
- Character performance obeys the reviewed shot control; no unrequested smile, heroic posture, or altered emotional beat.
- Delivered duration, dimensions, and audio are read from the actual file, not assumed from requested settings.

## Pitfalls

- **Text-only continuity:** “Continue from Group B” has no conditioning effect unless the actual reference frame is attached.
- **Missing character sheet:** A group featuring Turbo, Guardian, or another recurring character must include that character’s canonical identity sheet even if a prior clip or environment reference shows them.
- **Reference-budget inversion:** Blocking images are optional; immediate continuity and visible identity are not.
- **Prompt drift at dispatch:** Provider heuristics never authorize rewriting an approved packet. Publish and approve a revised kit first.
- **False completion:** A client timeout can coexist with a pending provider job. Query the generation log by idempotency key before retrying; do not create a duplicate paid job.
