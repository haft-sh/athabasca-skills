# Athabasca media generation operational pitfalls

Load this reference only when a generation, persistence, attachment, provider-routing, or review-loop edge case appears.

## Timeout does not prove failure

- GPT Image 2, Seedream, Midjourney, and video providers can finish after the HTTP caller times out.
- Before retrying a paid generation, check newest project media and provider-side evidence if available.
- If an upstream artifact exists but Athabasca did not persist it, treat the issue as correlation/persistence recovery, not generation failure.

## Midjourney recovery

- Discord success beats an Athabasca timeout.
- If a Discord CDN attachment exists, import it via `POST /api/projects/:slug/media` instead of rerunning.
- Preserve provenance: source Discord URL/message/channel, MJ job/button metadata when available, source reference assets, and original generation log ID if known.
- If the route rejects `referenceAssetIds` for Midjourney, place public reference URLs at the front of the MJ prompt and retry only when appropriate.

## Reference and edit support can drift

- Treat old capability warnings as hypotheses.
- For safe/cheap checks, live-probe the canonical project route with explicit `provider`, `model`, and contested fields before declaring unsupported.
- Record exact HTTP status/body when a route fails.

## Minimal-delta image repairs

- Use the latest approved/problem image as the first reference when preserving composition matters.
- Add canonical prop/character/environment references as secondary references.
- Phrase prompts as strict deltas: what changes, what must not change, and hard negatives for common wrong readings.
- See `canonical-prop-repair-with-gpt-image-2.md` for the generic atomic-edit prompt shape.

## Character and prop continuity

- Verify character details from canonical assets before generating; do not rely on memory or prior chat descriptions.
- For costume transfer: identity sheet first, donor costume/prop image second; state which reference controls which attributes.
- For morphology/costume rerolls, use two-reference conditioning when available: latest successful variant + canonical identity reference.

## Attachment vs generation failure

Classify failures separately:

- provider rejected prompt/settings
- normalized route validation failed
- adapter mapping bug
- provider account/billing issue
- generation succeeded but persistence failed
- asset persisted but shot/project attachment failed

Do not report provider failure when the asset exists in project media but shot attachment is missing.

## Media triage edge cases

- Color tag and semantic tags use separate endpoints.
- Approvals typically require both `colorTag: "green"` and canonical tags.
- Skip green/yellow finalized assets during review unless the user asks to revisit.
- A bare number after a displayed MJ grid is usually a quadrant selection; recover queue context before asking what it means.
- Deliver MJ grids as native media when the user needs to pick quadrants.

## Video-specific pitfalls

- Always use `idempotencyKey` for retriable paid video jobs.
- Use lowest-cost practical settings while iterating unless the user asks otherwise.
- Direct provider calls are fallback/debug paths only; successful direct outputs must be downloaded, uploaded back to Athabasca, and verified.
- For direct fal.ai Seedance fallback, prefer queue submit + polling over long `subscribe()` calls.
