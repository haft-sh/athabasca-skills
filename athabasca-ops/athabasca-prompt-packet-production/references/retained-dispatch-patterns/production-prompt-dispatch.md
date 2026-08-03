---
name: production-prompt-dispatch
description: Govern approved creative prompt packets, revision provenance, exact dispatch, and post-cut continuation repairs for Athabasca media generation.
version: 1.0.0
---

# Production Prompt Dispatch

Use this for any Athabasca still/video workflow where a human-approved prompt packet is the production source of truth, especially when paid dispatches, reference bindings, or continuity repairs are involved.

## Core rule: approved blocks are executable sources

A named, user-approved copy-paste block is immutable at dispatch.

- Extract and submit it verbatim after newline normalization.
- Record source asset/version, group, extraction method, normalized source hash, normalized submitted hash, reference order, settings, and idempotency key.
- Block a paid submission if source and submitted hashes differ.
- Do not summarize, reorder, omit, append, or "optimize" an approved prompt for a provider.

Provider heuristics (shorter takes, reference-count limits, quality suffixes) apply while **authoring a proposed revision**, never as invisible dispatch-time edits.

## Revision path

When user feedback, a new reference, a provider constraint, or a visual defect requires a prompt change:

1. Preserve the previous packet and generated output as provenance.
2. Create a new versioned packet with only the stated changes.
3. Attach the versioned packet to project media with a permanent URL and provenance linking source packet, affected output asset, feedback, and scope.
4. Show the revised copy-paste block for review when requested.
5. Dispatch only after approval, using the exact-block hash gate.

## Post-cut continuation repair

When early coverage works but continuity breaks at a known cut:

1. Keep the usable lead-in; do not rerun it by default.
2. Mark the flawed output yellow/non-canonical and document the failed timestamp.
3. Extract the last stable frame immediately before the cut and persist it as project media.
4. Create a continuation kit covering only downstream replacement shots.
5. Attach the extracted frame as `@image1`, with strict authority over environment geometry, light direction, exposure, contrast, grade, dust, shadows, and actor state.
6. Use only the minimum remaining identity/location references within model limits.
7. Include explicit no-reset controls: no new environment, daylight/sky reset, sun-angle change, relight, altered shadow direction, fresh grade, or dust-density change.
8. Keep lead-in and continuation separate until editorial review.

## Verification

Before reporting a generation complete:

- verify the persisted prompt equals the approved source;
- verify source/submission hashes match;
- verify public media URL and project attachment;
- inspect frames around any repaired cut for layout, key direction, color temperature, shadows, and exposure;
- distinguish provider output variance from a prompt/source mismatch.

See `references/post-cut-continuation-kit.md` for the reusable downstream-continuation procedure.
