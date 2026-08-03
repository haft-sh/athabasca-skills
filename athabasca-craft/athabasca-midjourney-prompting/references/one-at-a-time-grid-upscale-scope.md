# One-at-a-time Midjourney grid review: scope of "all of these"

Session lesson from Jatayu visual-development review.

When the user is reviewing Midjourney grids one at a time and the assistant has just displayed a single 2x2 grid, pronouns like "these" usually refer to the currently displayed grid/quadrants — not every asset in the broader approved/favorites queue.

## Correct behavior

- Maintain explicit review state: current grid asset ID, queue position, prompt index/title, and any upscaled quadrants.
- After showing a grid, wait for the user's quadrant instruction.
- If the user says a number (`1`, `3`, `1 and 3`), upscale only those quadrants of the current grid.
- If the user says "upscale all of these" while a single grid is on screen, upscale all four quadrants of that current grid only.
- Do not batch-upscale every approved/favorite grid unless the user explicitly says something broad like "upscale all approved grids" or "batch all remaining grids." If the wording could change cost/scope materially, clarify before launching a broad batch.
- After finishing the current grid's upscales, advance only when the user says "next."

## Why this matters

A broad interpretation can accidentally submit many paid/slow Midjourney button interactions. The UI context is the last displayed grid, so scope pronouns to that visible grid unless the user explicitly broadens the scope.

## Recovery if over-broad batch starts

1. Kill the background process immediately.
2. Inspect logs to identify which upscales already completed.
3. Report exactly what was created.
4. Complete only the intended current-grid quadrant(s) if needed.
5. Resume the one-at-a-time queue.
