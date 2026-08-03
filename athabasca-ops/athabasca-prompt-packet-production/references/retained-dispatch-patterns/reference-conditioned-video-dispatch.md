---
name: reference-conditioned-video-dispatch
description: Prepare, dispatch, and review reference-conditioned video generations where continuity between generated groups and recurring-character identity must be preserved.
---

# Reference-Conditioned Video Dispatch

## Use when

Use for any image/reference-to-video dispatch involving a recurring character, a continuation from a prior generated clip, or a sequence composed from separately generated groups.

## Core rule

A prompt mention is not conditioning. Every visible recurring character needs its canonical identity sheet attached as an actual reference. A previous generated group needs an actual persisted handoff frame attached as the first-frame continuity reference.

## Pre-dispatch workflow

1. **Classify reference authority.** Record every attachment and its single primary authority: immediate continuity, character identity, location/geography, or blocking/style support.
2. **Create a handoff frame when continuing a prior group.** Extract the last visually usable frame before the intended cut; persist it as project media with timestamp, parent asset ID, frame hash, and an immutable public URL.
3. **Set reference priority.** Use attachment order:
   1. preceding-frame continuity;
   2. canonical identity sheets for every visibly recurring character;
   3. location/geography reference;
   4. blocking-only or other secondary style reference.
4. **Respect the provider cap deliberately.** If the cap cannot fit all references, remove the lowest-authority blocking/style reference first. Never silently omit the identity sheet for a visible character.
5. **Write an explicit continuity lock.** State first-frame match requirements: environment geometry, camera axis/height, light direction, exposure, shadow direction, color grade, dust/atmosphere, character pose, screen direction, and prop state. Ban a daylight reset, new environment, grade reset, or relight at the opening cut.
6. **Publish and approve a revised packet/kit.** Any changed reference role, attachment, or semantic prompt control requires a new reviewable packet before paid dispatch.
7. **Hash gate.** Extract the approved copy-paste text, normalize line endings, record source hash, submit that exact text, and persist source packet ID/URL, submitted-prompt hash, ordered references, provider/model, and settings.

## Post-generation QC

Review the first generated frame against the preceding handoff frame, then inspect each hard cut.

Check:
- opening-frame canyon/location geometry and camera-axis match;
- sun/key direction, exposure, contrast, shadows, atmosphere, and grade;
- visible characters match their canonical identity references;
- screen direction, eye lines, scale, prop arm/hand, and prop state;
- whether a character has drifted into an unintended expression or performance;
- actual delivered duration, dimensions, and audio stream.

If continuity or identity fails, mark the asset yellow/non-canonical. Preserve it as diagnostic evidence, but do not reuse it as the next continuity authority unless a specific usable frame is deliberately selected and documented.

## Pitfalls

- Do not write “use the prior frame/axis” without attaching the actual persisted frame.
- Do not rely on an environment, Guardian, or blocking reference to preserve Turbo (or another visible character). Attach that character’s canonical sheet.
- Do not allow a blocking-only reference to displace a continuity frame or character identity reference when attachment slots are limited.
- Do not silently rewrite an approved packet to repair reference omissions; publish a revision/continuation kit first.
