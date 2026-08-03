# Seedance Multi-Group Continuation and Recovery Pattern

Use this when dispatching consecutive Seedance groups from a prompt-preview document.

## Accepted-clip continuation

When the previous group is approved and should control continuity:

1. Submit the next group in reference-to-video mode.
2. Pass the previous accepted Athabasca clip as the sole video reference (`video one`).
3. Reuse the exact successful image-reference set and ordering from the accepted group unless the user explicitly replaces an anchor.
4. Replace the prompt's opening line with the requested continuation instruction, for example: `I want you to extend video one and generate the following shots.`
5. Keep the remaining group prompt intact except for continuity corrections already approved in prior iterations.
6. Use a fresh idempotency key for each intentional group generation; retries of the same attempt reuse that key.
7. Verify the persisted asset, audio stream, duration, public URL, and representative frames.

## Failed-clip recovery

Do not extend a clip the user rejected. A video reference can propagate or amplify its mistakes.

1. Remove the video reference entirely.
2. Regenerate from the group's text plus canonical image references only.
3. Replace outdated identity anchors with the exact asset IDs selected by the user.
4. Convert failures into explicit, countable constraints: exactly one of each character, one shelf/location/destination, no mirrored room, and one clear path through the set.
5. Make identity/display rules concrete. Distinguish graphic visor overlays from anatomical eyes. For localized light, state exact source, color, and forbidden alternatives.
6. When the retry succeeds, use that accepted retry as the new continuation anchor for the next group and preserve its successful image-reference set.

## Continuity authority

- Video reference: immediate motion, staging, scale, and treatment continuity.
- Image references: character identity and environment geography authority.
- If the video conflicts with canonical images, remove the video rather than stacking more references onto the bad state.
- Separate competing light sources explicitly by ownership and color.
- Carry successful live-dispatch corrections forward even when the original preview document still contains older reference descriptions.

## Verification

- Correct accepted clip supplied as video one
- Same successful image assets and order reused
- Rejected clips excluded
- Exactly-one constraints checked in representative frames
- Identity-specific eye/display/light rules checked
- Duration, resolution class, and audio verified
- Result persisted to the project
