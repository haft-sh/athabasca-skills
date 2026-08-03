# Midjourney review queue continuation

Use this for one-at-a-time Midjourney grid review queues where the user is choosing quadrant upscales from generated 2x2 grids.

## Lessons from Jatayu style review

- A bare number or comma-separated list after a grid is displayed is a quadrant selection for the active grid, even if the previous assistant turn was many hours earlier.
- If context may have rolled off or time has passed, recover the queue state from session history / queue logs before asking the user what the number means.
- `1=top-left`, `2=top-right`, `3=bottom-left`, `4=bottom-right`; `1,2,3` means upscale all three selected quadrants.
- After completing requested upscales, do not stop with only the completed assets. In the same reply, show the next grid in the queue as native media and ask for the next quadrant selection.
- Only stop auto-advancing when the queue is exhausted, the user explicitly stops, or the next step is genuinely ambiguous.

## Reporting shape

1. Briefly list completed upscales with asset IDs and verified URLs.
2. Immediately show the next grid with `MEDIA:/tmp/...`.
3. Include the quadrant mapping and allow `skip`.

This reduces review friction and avoids making the user repeatedly say `next`.