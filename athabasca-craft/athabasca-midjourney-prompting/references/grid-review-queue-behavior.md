# Midjourney grid review queue behavior

Use this when the user is reviewing a sequence of Midjourney 2×2 grids and selecting quadrants for true U-button upscales.

## Queue semantics

- Show one grid at a time as native Telegram media: `MEDIA:/tmp/...webp`.
- Stable quadrant mapping: `1=top-left`, `2=top-right`, `3=bottom-left`, `4=bottom-right`.
- The user may select multiple quadrants in one reply, e.g. `1,4` or `2,3,4`; upscale each selected quadrant in order.
- In this context, a bare `next` means **skip the currently displayed grid and advance**. Do not ask whether `next` means skip.
- After completing selected upscale(s), report the created asset IDs/URLs and immediately show the next grid in the same reply. Do not force the user to send a separate `next` after every upscale.
- If the user replies with a bare number after a long delay, recover the queue context from recent/session history before treating the number as ambiguous.

## Reporting shape

For each processed grid:

```text
Upscaled Round N #XX — Title:
- Q2 / top-right: `asset_...`
  https://...

Verified `200 image/png`.

Next grid X/Y — Title
Asset: `asset_...`

MEDIA:/tmp/grid.webp

Pick quad(s), or say next/skip:
`1=top-left`, `2=top-right`, `3=bottom-left`, `4=bottom-right`
```

Keep it compact; the image is the main payload.

## Persistence / verification

- Use the true Midjourney U-button upscale from stored `mjButtons`; do not crop grid quadrants.
- Persist each upscale through Athabasca project media with provenance linking source grid asset ID, selected quadrant, Discord message IDs, prompt index/title, and prompt set asset ID where available.
- Verify the returned Athabasca public URL with a HEAD/GET check before reporting success.

## Why this matters

the user corrected the workflow: he does not want to keep saying `next` after every upscale, and in a review queue `next` should be understood as skip. Encoding this keeps the review loop low-friction and prevents contextless-number confusion after delayed replies.
