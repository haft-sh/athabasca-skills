# User-specified canonical reference override rule

Use this when building or revising Athabasca Seedance prompt previews or dispatch prompts.

## Rule

If JP explicitly supplies the reference asset IDs for a preview doc or generation lane, treat those assets as the canonical set for that task.

Do **not**:
- substitute nearby older refs
- substitute greener stand-ins
- substitute semantically similar assets discovered through browsing the media library
- silently keep earlier draft refs after JP replaces them

## Operational pattern

1. Rebuild the reference-card section around the exact supplied assets.
2. Renumber `@imageN` tags around the user-specified set rather than around whatever was previously in the doc.
3. Carry those exact assets through to live dispatch by resolving each asset ID to its `publicUrl` and replacing the inline asset IDs with those URLs verbatim.
4. If JP gives a composition image for a specific shot (for example a worm's-eye huddle image), treat it as an explicit shot-composition anchor, not general inspiration.
5. If JP names the roster for a team/crowd beat, state the roster explicitly in the prompt text so Seedance does not collapse the group into generic players.

## Example from GLY A1S1

JP overrode discovered refs with a specific set:
- stadium establishing shot
- Turbo / Dozer / Racy / Bone / Gary for the opening huddle
- Smoky / Marvin for opposing-team continuity
- a separate worm's-eye huddle image as the explicit opening composition anchor

The correct update path was:
- replace the old preview doc in place
- rewrite the opening shot order to start on the worm's-eye composition shot
- map every supplied asset ID to its exact `publicUrl` during generation dispatch

## Why this matters

For JP, a named asset list is not advisory. It is a continuity lock.
