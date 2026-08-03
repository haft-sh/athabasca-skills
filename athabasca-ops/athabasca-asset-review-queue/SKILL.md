---
name: athabasca-asset-review-queue
description: Run an asset review queue — present generated stills one at a time for human approval, update canonical status, and track regeneration flags.
version: 0.1.0
author: Hermes Agent (Athabasca)
---

# Athabasca Asset Review Queue

Present generated assets for human review. Accept approval/rejection/flag. Maintain canonical status per shot slot. Track regeneration needs.

## Trigger

User says:
- "start review queue"
- "review the assets"
- "go through the asset list"
- Any request to inspect, approve, or reject individual generated assets

## Pre-Flight

1. Identify the project slug (e.g. `good-boy`)
2. Load the asset inventory HTML from R2 or document cache
3. Query the project media via `GET /api/projects/:slug/media` to get all generated assets with their IDs, URLs, and color tags
4. **Before starting dependent shot review, check reference prerequisites**:
   - canonical character sheets for recurring main characters / creatures
   - canonical prop references for hero props that drive continuity
   - canonical location/environment references when the user's feedback concerns continuity-sensitive sets
5. If a user wants to critique or edit a shot but the relevant upstream reference is missing or unstable, **pivot the queue** to those references first instead of continuing to review dependent shots.
6. Build a review queue sorted ascending by asset number (or shot number if 1:1), unless the user explicitly requests a different order.
7. Exclude VOID shots (S001, S038) — they are sound-only

7. Exclude VOID shots (S001, S038) — they are sound-only

## Display Format (Telegram)

Every asset is presented with:
- **Asset #** | **Shot ID** | **Slot name** | **Brief description**
- Inline image via `![shot-id](url)` (renders as native photo in Telegram)
- Clickable URL beneath: `[URL](url)`
- Any relevant notes (e.g. "also mapped to S003 — description says VOID")

Example:
```
asset-001 / S002 — MONTAGE / SARAH CONNOR V.O.
Fast-cut cold montage: server farm, drone swarms, cyborg face, mushroom cloud reflection
```
![S002](https://media.wheretoaccess.com/good-boy/generated/generated_xxx.jpg)
[URL](https://media.wheretoaccess.com/good-boy/generated/generated_xxx.jpg)

## User Response Handling

### Approve → Make Canonical

If user says **"approve"**, **"yes"**, **"canonical"**, **"use it"**, or similar:
1. `PATCH /api/projects/:slug/media/:assetId` — set `colorTag: "green"` and `ratingStars: 5`
2. Find any other assets mapped to the **same shot slot** that already have `colorTag: "green"` → `PATCH` them to remove green (set to `null`)
3. Log the approval in notes

### Reject → Flag for Regeneration

If user says **"no"**, **"reject"**, **"regenerate"**, **"redo"**, or requests changes:
1. `PATCH /api/projects/:slug/media/:assetId` — set `colorTag: "red"` (flags for future deletion)
2. Log the regeneration request with the user's feedback
3. Add to regeneration queue

### Skip

If user says **"skip"** or **"next"**: advance without any DB change.

### General Note

If user gives feedback without a clear approve/reject: log as a note and continue. Do not change canonical status.

## Canonical Rules

- **One canonical (green) asset per shot slot.** Approving a new asset auto-degreens any previous canonical for that slot.
- **Red = flag for deletion.** Do not auto-delete — preserve the red asset so the user can review the flagged set later.
- **Green without de-greening another asset is a silent error.** Always check for competing greens before applying.

## Upstream Dependency Pivot

If the user says a shot cannot be reviewed meaningfully until its upstream references are locked (for example: *"we need the canonical prop reference and the canonical character sheet first"*), **stop reviewing dependent shots immediately** and pivot the queue upstream.

### What counts as an upstream dependency
- canonical character sheet / turnaround
- canonical prop reference
- canonical environment / location plate
- any reference image the user says downstream edits must match

### Required pivot sequence
1. **Pause the current shot queue without mutating the current shot asset.** Do not approve/reject the dependent shot yet.
2. **Check whether the canonical reference already exists in the live project media.** Look for existing green assets, canonical-style tags, or obvious dedicated reference assets.
3. **If no canonical reference exists, identify the best current source candidates** from project media and present those for review first.
4. **If the existing candidates are not clean enough to serve as canonical references, say so directly.** Recommend generating a dedicated reference asset rather than canonizing a compromised story frame.
5. **Only return to the dependent shot queue after the upstream reference decision is resolved.**

### Practical guidance
- For a **character sheet**, prefer frames that define stable anatomy and identity: overall body proportions, coat color/texture, ear shape, muzzle shape, and neutral pose. A cinematic close-up may be emotionally strong but still be a poor sheet source.
- For a **prop reference**, prefer clean isolated visibility of the product design. If the image drifts on color, materials, indicator lights, or accessories, do **not** bless it as canonical just because it is the closest existing shot.
- When comparing candidates, distinguish between **"best current source image"** and **"already-good canonical reference"**. Those are not the same thing.

### Pitfall
Do **not** keep marching through the descending asset queue when the user has reframed the task around upstream references. That produces critique on shots that are expected to change and wastes review cycles.

## Regeneration Queue

Track regeneration items separately. After the review pass, present the regeneration queue:
- Shot ID + slot name
- User's requested change
- Current asset ID (red-flagged)
- Generation context (prompt, model, provenance)

## Skill Version History

- **v0.1.0** — initial version, created from a live Athabasca review queue session
