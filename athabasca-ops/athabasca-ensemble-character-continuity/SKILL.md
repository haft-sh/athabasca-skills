---
name: athabasca-ensemble-character-continuity
description: Preserve exact hero identity and roster correctness in Athabasca multi-character still generations, especially radial huddles and other composition-locked ensemble shots.
version: 1.0.0
author: Hermes Agent (Athabasca)
metadata:
  hermes:
    tags: [athabasca, image-generation, ensemble, continuity, codex, reference-images]
    related_skills: [athabasca-media-generation, athabasca-reference-to-character-sheet-prompting]
---

# Athabasca Ensemble Character Continuity

Use this when generating a **multi-character still** where:
- one hero character must read exactly right
- the ensemble composition is already approved or tightly specified
- roster correctness matters (no duplicates, no missing teammate substitutions)
- radial / clock-face layouts make face orientation easy to get wrong

## Core rule

Do **not** weight every reference equally by default.

When one character matters most, too many equal references can cause:
- hero-face drift
- the hero borrowing features from the composition image instead of the approved sheet
- duplicate-hero substitutions in another roster slot
- correct placement but wrong radial face orientation

## Preferred reference hierarchy

For native Codex / GPT Image 2 ensemble stills, prefer:
1. **composition lock** — the latest approved ensemble frame or composition reference
2. **hero identity lock** — the single authoritative character sheet for the most important character
3. **surgical repair reference** — only add a third character sheet when repairing one specific wrong slot

Do not automatically attach the whole cast if the real task is "keep this composition but make Turbo exact."

## Prompting pattern

### 1) Name the visual priority explicitly

Say plainly that the hero is the visual priority.

Example shape:
- "Reference image 1 controls the composition."
- "Reference image 2 is the strict authoritative identity lock for Turbo."
- "Do not borrow Turbo's face from reference image 1."

### 2) List non-negotiable face cues

For the hero, spell out only the identity cues that must not drift:
- face shape
- nose / snout shape
- glasses / eye shape
- helmet fit
- core palette
- approved expression range

Do not rely on vague phrases like "same character" when the face is the real failure mode.

### 3) Anchor clock position when composition is radial

If the shot is a circle / huddle / overhead ring, name the hero's exact clock position.

Example:
- "Turbo is at 6 o'clock, directly opposite Gary."

### 4) State facial orientation explicitly for top/bottom positions

Clock position alone is not enough.

For radial faces, specify orientation like:
- "eyes nearest the inner sky opening, mouth/chin toward the outer rim"
- or the inverse when desired

Without this, models may keep placement but rotate the face 180 degrees.

## Single-error correction workflow

When an ensemble image is mostly correct, avoid a full reroll.

Use a **single-error correction prompt**:
- preserve the exact composition, camera, lighting, and all successful identities
- change only the bad slot or orientation
- explicitly say the good hero rendering must not change

This works well for:
- replacing a duplicate hero with the missing teammate
- fixing one upside-down / radially flipped face
- preserving a finally-correct hero while repairing another roster member

## Roster discipline

When the user names a fixed cast, restate the exact final roster in the prompt and forbid duplicates.

Useful language:
- "Exactly six distinct players once each"
- "No duplicate Turbo"
- "No extra turtle"
- "Bone belongs in the upper-left slot"

## Pitfalls

- Do not assume adding more references always improves identity.
- Do not let the composition reference become the accidental face reference for the hero.
- Do not reroll the whole ensemble after the hero is finally correct unless there is no narrower repair path.
- Do not use only clock position for radial shots; include eyes-inward / mouth-outward orientation when needed.
- Do not call a result final until you verify both hero fidelity and roster uniqueness.

## Verification checklist

- [ ] Hero uses the authoritative identity sheet, not just the composition frame
- [ ] Hero sits in the requested clock position
- [ ] Radial face orientation is correct for top/bottom placements
- [ ] Named roster appears exactly once per character
- [ ] No accidental duplicate hero substitutions
- [ ] Narrow repair prompt used when only one slot was wrong

## Relationship to other skills

- Use `athabasca-media-generation` for the full API-backed generation and persistence workflow.
- Use this skill for the **prompting and reference-weighting strategy** when a multi-character still keeps drifting on identity or roster correctness.
