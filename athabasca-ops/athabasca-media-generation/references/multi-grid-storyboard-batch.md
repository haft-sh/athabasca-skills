# Multi-grid GPT Image storyboard batch from Athabasca references

Use when the user asks for an entire scene or long sequence as several 3x3 storyboard grids using GPT Image / Codex with project media references.

## Pattern

1. Load the source shot-list artifact.
   - If the user provides a media URL to markdown, fetch it directly and extract the shot sequence/continuity constraints.
   - If the user provides an `asset_...` id or earlier-scene shot-list id as context, do **not** assume it is the current scene's markdown. Check the asset title/metadata against the requested scene, and if they mismatch, search project media for the actual current-scene shot-list markdown before generating.
   - For long scenes, segment the beats by editorial sequence, not by arbitrary shot numbers.
   - Common pattern for a 20-shot scene: `001-009` as a 3x3 grid, `010-018` as a second 3x3 grid, and `019-020` as a separate two-panel final sheet rather than forcing a weak nine-panel third board.

2. Resolve current references from project media.
   - Prefer the **immediately previous-scene storyboard grid(s)** as the primary style/layout anchor when the task is a direct continuation. That adjacent board is usually the best source for numbering treatment, divider weight, color finish, and editorial rhythm.
   - Prefer latest/versioned assets by title/metadata, e.g. `Character Reference v2`, `Location Reference v2`.
   - When the user says "latest media attachments" or "the two latest attachments", search project media across **all phases/categories**, not only the target generation phase. Recent visual references may live in `concept` while the generated grids belong in `storyboard`.
   - Sort candidate image assets by `createdAt`/`updatedAt` and confirm titles match the user's description (for example, versioned room or character-board titles) before using their `publicUrl`s as `reference_images`.
   - Include all recurring characters plus the location reference when style/environment continuity matters.
   - Include opposing-team/action-specific references (e.g. a defender who appears only in the tackle grid) when they govern a key beat.
   - Check URLs before generation; a stale or truncated media URL can make Codex fail while downloading references.

3. Build one prompt per grid.
   - Ask for `one square 3x3 storyboard contact sheet` with `nine equal panels in reading order`.
   - Identify each reference by role: `primary character`, `secondary character`, `opposing character`, etc.
   - Put global style once near the top: e.g. `v2 Pixar-like children's TV style`, `high-saturation vibrant colors`, `expressive eyes with catchlights`, `comic readability`, `exaggerated physics`, `strong silhouettes`, `fast comedic pacing`, `cinematic framing`.
   - Then list each panel as a concrete shot with camera angle, staging, and action.
   - Keep no-text guardrails: `No captions, no speech bubbles, no watermarks, no panel numbers` unless labels are explicitly requested.

4. Preserve special editorial asks explicitly.
   - If the user expresses bias toward a shot grammar, such as a worm's-eye clock-formation huddle, include that as a named panel rather than hoping it emerges from generic huddle language.
   - For screen direction, repeat constraints in action panels: `the protagonist travels screen-right`, `the body still moves screen-right while the character looks back`.

5. Generate each grid separately.
   - Parallel calls are fine if prompts and reference URLs are independent.
   - If one grid fails due to a bad reference URL, fix only the bad URL and regenerate that grid; do not discard successful grids.

6. Verify visually before upload.
   - Check each grid has 9 panels.
   - Confirm the grid covers the intended beat range.
   - Check key requests landed (e.g. worm's-eye huddle, open gap, freeze, blind-side impact, blackout panel).
   - Note concise caveats; do not over-explain if the result is usable.

7. Persist each generated local PNG through `POST /api/projects/:slug/media`.
   - `phase=storyboard`
   - `category=generated`
   - `sourceKind=generated`
   - project attachment role such as `storyboard_grid_v2` or `storyboard_grid`
   - `sortOrder` matching grid order
   - metadata: `artifactKind=storyboard_grid`, `version`, `workflow=gpt-image-2-codex-storyboard-grid`, `sourceMarkdownUrl`, `referenceAssetIds`, `provider`, `model`, and a concise `promptSummary`.

8. Verify final R2 URLs with `HEAD` and report each image inline with title, asset id, and URL.

## Example four-grid segmentations

For a football dream sequence:
- Grid A: opening pressure and huddle, including a worm's-eye clock-formation huddle.
- Grid B: line of scrimmage, snap, Statue of Liberty fake, handoff, launch.
- Grid C: sprint, glance back, defense wall, open gap, feet lock/freeze start.
- Grid D: shell retreat, blind-side defender shadow/materialization, child-friendly impact, aftermath/reactions, blackout.

For a quiet bedroom-to-portal transition:
- Grid A: black from prior scene, desk wake-up, homework insert, bedroom pressure geography, post-its/calendar, shell retreat and recovery.
- Grid B: reflection/shame beat, pulsing shelf object, character notices/approaches, invitation beat, confession beat.
- Grid C: consent while anxious, meditation cushion relocation, breath ritual, room swirl, lotus portal begins, pillow starts floating.
- Grid D: final gag/transition beat; repeat or extend final transition beats if needed to fill nine panels.

When a scene has fewer than 36 natural beats, fill the last grid by splitting transition moments into visually distinct panels (wide, close-up, abstract bloom, full white) rather than inventing new story events.

## Pitfalls

- Do not pass asset IDs directly to `image_generate`; resolve to public URLs first.
- Do not reuse old/v1 references when the user asks for v2; search project media by title/metadata and prefer the latest versioned assets.
- Do not assume the newest useful references share the output phase. Reference assets may be in `concept`, `visual_dev`, or `misc` while the generated storyboard grids should still be uploaded as `phase=storyboard`.
- A single incorrect reference URL among many causes the whole Codex image call to fail with a download error. Fix the URL and retry that grid only.
- Generated grids are local staging files until uploaded through Athabasca media APIs.
