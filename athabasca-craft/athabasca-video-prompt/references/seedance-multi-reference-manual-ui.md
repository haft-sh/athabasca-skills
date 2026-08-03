# Seedance multi-reference manual-UI workflow

Use this when generating in manual UIs such as Mitte.ai or Replicate where you can attach multiple images and reference them in the prompt as `@image1`, `@image2`, etc.

## Core lesson

Do **not** ask Seedance to perform a facial beat from a reference set that does not contain that face.

Bad pattern:
- hand-only or object-only reference image
- prompt says to push into her face / his reaction / tears / confusion arriving
- model must guess the face because the workflow is stateless
- result is often a wasted generation

This is especially easy to miss when a lane begins as an insert shot and later asks for a reaction close-up.

## Safe rule

If a lane contains any of these:
- face close-up
- reaction beat
- eyes shifting
- confusion arriving
- smile changing
- any emotional performance readable in the face

then the attached references must include:
1. the relevant character sheet or face anchor for that person
2. at least one scene still that already contains that person in the right wardrobe / lighting / environment

Prefer attaching both leads' character sheets when both appear in the lane.

## Recommended attachment pattern

For face-sensitive romance/comedy lanes:
- `@image1` — female lead character sheet
- `@image2` — male lead character sheet
- `@image3+` — scene stills for blocking / prop / wardrobe / lighting continuity

Character sheets preserve identity.
Scene stills preserve blocking, costume, environment, prop state, and emotional context.

## When to prefer multi-reference 15s lanes over granular single-image lanes

Prefer the multi-reference manual-UI workflow when:
- the UI supports up to several `reference_images`
- the lane needs both object inserts and face reactions
- the model should interpolate between several anchored beats
- single-image stateless prompting would force the model to invent faces or wardrobe continuity

This is often stronger than micro-lanes because you can keep:
- character identity
- prop continuity
- scenic continuity
- emotional progression

inside one 15-second coverage lane.

## Sequence design rule

Coverage matters more than chronology.

Write 15-second lanes around editorial jobs, not strict shot order. Good lane types:
- romance setup lane
- proposal + ring beauty lane
- reversal lane (reach → snap → confusion)
- prenup reveal lane
- reaction-processing lane
- final tableau lane
- insert / glue lane

## Prompt structure for manual multi-reference lanes

Use time blocks plus explicit cut cues:
- `[0–3s] Begin on @image3 ...`
- `[3–6s] Cut to @image4 ...`
- `[6–10s] Stay in the @image4 family but push closer ...`
- `[10–13s] Return to @image3 ...`

When asking for a closer facial beat, explicitly remind the model which character-sheet reference governs likeness.

Example pattern:
- `Use @image1 to preserve her likeness.`
- `Use @image2 to keep his face coherent in partial profile.`

## Specific pitfall to avoid

A lane like "hold on her suspended hand, then go into her confused face" is **unsafe** if the attached references only include:
- the hand/reach still
- the snap-shut insert

It becomes safe only when the lane also includes:
- her character sheet
- a reaction still containing her face

## Relationship to API workflows

This guidance is for manual multi-reference environments using `reference_images`.

It is different from the single-image API workflow using:
- `image`
- `last_frame_image`

Do not mix the assumptions. If the workflow is stateless single-image i2v, keep prompts short and do not ask for unsupported face inventions. If the workflow is manual multi-reference, exploit the larger reference set aggressively.