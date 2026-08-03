# Midjourney grid upscale and Athabasca import

Use this when a user wants a specific panel from an already-generated Midjourney grid to become a reusable upstream reference.

## Goal
Recover the real Midjourney upscale for a chosen quad (`U1`-`U4`) instead of faking it with a crop, then persist that upscale back into Athabasca with provenance.

## Durable pattern
1. Inspect the source media asset metadata / generation log for:
   - `mjButtons`
   - `discordMessageId`
   - `discordChannelId`
   - `mjJobId`
2. Use the stored button custom ID for the requested quad (for example `MJ::JOB::upsample::4::<job-id>`).
3. Trigger a Discord interaction against Midjourney using the lean message-component payload; avoid inventing extra guild fields if not needed.
4. Poll/fetch the channel until the returned upscale message appears and capture its attachment URL.
5. Download the returned image and re-upload it through Athabasca project media.
6. Store it as a reference asset when that is the real role, and preserve provenance in title/notes/metadata:
   - source asset ID
   - button used (`U1`-`U4`)
   - parent Discord message ID
   - returned Discord message ID

## Why this matters
- The true U-button upscale is a better upstream reference than a crop from the 4-up grid.
- It preserves Midjourney's detail recovery and gives later character-sheet / prop-sheet generations a cleaner anchor.
- Provenance makes future regeneration auditable.

## Prompting / review implication
If the user says "use quad 4" or otherwise points to a specific panel in a Midjourney grid, treat that as a request for the actual variant, not merely the approximate visual region.

## Review queue behavior
When running a human review queue over shortlisted/green Midjourney grids, do not make the user say "next" after every upscale. After completing the requested upscale(s), report the completed asset IDs/URLs and immediately show the next queued green grid for review in the same reply, unless the queue is exhausted or the user explicitly asks to stop. Preserve queue position from the approved/green shortlist order. In this review context, a bare "next" means skip the currently displayed grid and advance to the next grid without upscaling.

A bare number or comma-separated list after a displayed grid is an active-grid quadrant selection, not an ambiguous chat message: `1=top-left`, `2=top-right`, `3=bottom-left`, `4=bottom-right`. If the reply arrives hours later and the prompt context is not visible, recover the prior grid/queue state from session history or queue logs before asking the user to restate it.

## Do not store as durable rules
When running a green-flagged / shortlisted grid review queue, short replies are often stateful commands rather than standalone messages:

- A bare number `1`, `2`, `3`, or `4` after a quad prompt means trigger the corresponding true Midjourney U-button upscale for the most recently shown grid. Do not treat it as ambiguous just because many hours passed; first recover the prior prompt from conversation/session history or the known queue artifacts.
- `next` means show the next green-flagged/approved grid in the established shortlist order, not generate or upscale anything by itself.
## Prompting / review implication
If the user says "use quad 4" or otherwise points to a specific panel in a Midjourney grid, treat that as a request for the actual variant, not merely the approximate visual region.

## Review queue behavior
When running a human review queue over shortlisted/green Midjourney grids, do not make the user say "next" after every upscale. After completing the requested upscale(s), report the completed asset IDs/URLs and immediately show the next queued green grid for review in the same reply, unless the queue is exhausted or the user explicitly asks to stop. Preserve queue position from the approved/green shortlist order. In this review context, a bare "next" means skip the currently displayed grid and advance to the next grid without upscaling.

A bare number or comma-separated list after a displayed grid is an active-grid quadrant selection, not an ambiguous chat message: `1=top-left`, `2=top-right`, `3=bottom-left`, `4=bottom-right`. If the reply arrives hours later and the prompt context is not visible, recover the prior grid/queue state from session history or queue logs before asking the user to restate it.

## Do not store as durable rules
- Missing credentials or temporary auth failures are environment state, not skill truth.
- The lesson is the recovery/import workflow, not any one session's token or API error.
