---
name: athabasca-asset-review-operations
description: Set up and run Athabasca asset review queues, preserve user-specified traversal order, and classify outputs as canonical, exploratory, or not-yet-final.
version: 1.0.0
---

# Athabasca Asset Review Operations

Use this when reviewing batches of generated assets for an Athabasca project, especially when the user wants a queue, a ranking pass, or approval decisions on newly generated media.

## What this skill is for

This skill governs the operational side of review:
- turning a batch of generated assets into a review queue
- preserving the user's requested inspection order
- separating queue setup from shipping/approval
- reporting clearly on which assets are canonical versus exploratory
- keeping downstream review anchored to the strongest approved reference

It is not specific to one project. Apply it to any Athabasca media-review session involving multiple candidate assets.

## Trigger conditions

Use this skill when the user says things like:
- "start a review queue"
- "go through the newly generated assets"
- "review these in descending order"
- "pick the strongest one"
- "ship this one, then review the rest"
- "which of these is ready to lock?"

## Core workflow

1. **Identify the candidate set**
   - Confirm the relevant project and asset family.
   - Gather the newly generated assets that belong in the same comparison set.
   - Do not mix unrelated asset families in one queue unless the user explicitly wants that.

2. **Preserve the user's traversal order**
   - If the user specifies an order like "descending order, from highest number to lowest," use that exact order.
   - Do not silently substitute API return order, upload time order, or your own preferred ranking heuristic.
   - In user-facing reporting, state the review order explicitly when it matters.

3. **Anchor review to approved canon**
   - If one asset is already approved or shipped, use it as the reference anchor for adjacent review.
   - Review supporting artifacts relative to the approved canonical item rather than in isolation.
   - If reference stability is weak, pivot upstream instead of pretending downstream shots are reviewable.

4. **Separate queue setup from shipping**
   - Queue setup means: identify the ordered list and the first item to inspect.
   - Shipping means: explicitly promote/tag the chosen asset only after inspection.
   - Do not treat inclusion in a queue as implicit approval.

5. **Classify each reviewed asset cleanly**
   Use one of these buckets in the report:
   - **Canonical / ship-ready**: strong enough to lock and reuse downstream
   - **Good exploration**: useful directionally, but not the final reference
   - **Useful but not final**: structurally helpful, but still has text/detail drift or production-safety issues
   - **Needs redo**: misses the canon, introduces drift, or fails the task

6. **Report with operational clarity**
   For each asset, include:
   - asset ID
   - title
   - one-line verdict
   - the most important strengths
   - the main blocking issue, if any
   - recommended next action

## Review heuristics

### When reviewing product/brand/reference boards
- Distinguish between a board that is good for **direction** and one that is safe as a **final production reference**.
- If text is garbled, logos are unstable, or labels are model-noisy, call it a continuity/layout board rather than final packaging or final brand art.
- If a board contains several directions, identify the strongest direction and say whether it should be locked or refined.

### When reviewing character or prop sheets
- Check identity continuity first.
- Then check whether the approved prop or costume canon actually propagated into the refreshed sheet.
- Note residual multi-view drift briefly, but do not over-penalize normal generation variance when the sheet is otherwise production-usable.

## Pitfalls

- **Do not lose the requested ordering.** If the user asks for descending review, do not default to chronological or arbitrary order.
- **Do not confuse exploratory boards with shippable references.** A good board may still be unsuitable for final print, logo lock, or downstream production reuse.
- **Do not continue downstream cinematic review when upstream reference canon is still unstable.** Fix the reference layer first.
- **Do not bury the recommendation.** After reviewing a queue, say plainly what should be shipped, what should be refined, and what should be ignored.

## User-facing output pattern

A strong review response usually has:
1. a short queue/ordering statement
2. one subsection per asset
3. a blunt verdict for each asset
4. a final recommendation for the next move

## References

- `references/review-ordering-and-staging.md` — concise notes on queue ordering, staging, and reporting distinctions learned from a Good Boy asset-review pass.
