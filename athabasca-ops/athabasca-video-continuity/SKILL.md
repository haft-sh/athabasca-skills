---
name: athabasca-video-continuity
description: Prepare, dispatch, and QA Athabasca video continuations with strict frame handoff, recurring-character identity, and dialogue-speaker controls.
version: 1.0.0
---

# Athabasca Video Continuity

Use for a continuation, a follow-on group, or any recurring-character video clip whose quality depends on matching an earlier clip.

## Core rule

Text-only continuity is not continuity conditioning. Attach the relevant stable previous frame and the canonical identity sheets in the actual generation payload.

## Pre-dispatch checklist

1. Select a stable frame immediately before the discontinuity/cut from the prior approved or diagnostically useful clip.
2. Persist that frame through Athabasca as project media. Record source asset, timestamp, source-frame SHA-256, and permanent asset URL.
3. Attach references in this priority order when the provider supports four images:
   1. preceding-frame continuity authority;
   2. featured character canonical identity sheet;
   3. other recurring character canonical identity sheet;
   4. environment/geography authority.
4. Drop a generic composition/blocking reference if it would displace any of the first three. Do not claim a reference exists unless it is in the submitted reference array.
5. State which aspects each reference controls. The previous frame controls the handoff; identity sheets control character design; environment reference controls topology/axis.
6. Lock first-frame continuity explicitly: camera axis, rock/layout landmarks, exposure, light direction, shadow direction, grade, atmosphere/dust, scale, and current prop/character state. Prohibit daylight resets, relighting, environment swaps, and grade changes.
7. Extract the exact approved copy-paste prompt and compare normalized source/submission SHA-256 values before paid dispatch. Record asset IDs and order in provenance.

## Dialogue-helper discipline

- Audit all dialogue in chronological order before dispatch, including O.S., prop, off-camera, and echo lines.
- Do not duplicate a final line across two speakers unless the intended editorial effect is explicit and has been approved.
- Exclude incidental comedy, prop echoes, and extra button beats from a serious performance helper unless the user asks for them.
- If a prop/non-human voice is needed, make it a separate ground-level insert: primary character off-camera, mouth closed, and silent.
- Preserve a dialogue carrier's one-action-per-beat scope; do not overload it with unrelated cutaways.

## QA and recovery

1. Compare last usable source frame and generated first frame side-by-side before assessing the full clip.
2. Check character identity against canonical sheets, not merely a generic species/wardrobe resemblance.
3. Verify lighting/environment continuity at every hard-cut boundary.
4. Do not infer dialogue correctness from stills; play the audio.
5. Mark outputs yellow/non-canonical when identity, continuity, or speaker attribution fails.
6. Publish a revised review packet before re-dispatching. Never silently repair approved prompt text at dispatch.

### Action continuity and blocking pitfalls

- A hard-cut prompt cannot make the model literally inherit its prior synthesized pose just by saying “retain exact continuity.” For impacts, landings, costume state, prop orientation, or facial condition, extract and attach the actual predecessor frame to the follow-on generation.
- Do not compensate for unreliable stunt physics by making a long, dense continuous-action prompt. Simplify to one readable comic failure per clip before adding more temporal control.
- Screen direction is not relational blocking. “Move screen-right” can become a generic exit. When a character must approach an obstacle, lock the obstacle’s fixed position, require decreasing physical distance, and prohibit retreat, sidestepping, passing, and path-following.
- Audit literal nouns in **both action and audio** text. “Boot” can introduce footwear even when intended only as a footstep. For a barefoot character, use “bare [species] foot/toes contacting stone” and remove competing footwear nouns throughout the prompt.
- Do not use an animal noun as a scale shorthand for a recurring character (for example, “mouse guardian”). State both identity and scale: “the same turtle guardian at ankle height, not a mouse, rodent, mammal, or replacement character.”
- For a scale transformation, use one measurable change per clip. Keep the character planted at the same landmark, specify its unambiguous end height relative to the protagonist, and prohibit replacement, teleporting, sliding, sinking, and floating. Repeat the full identity/prop/environment lock in every successor clip; textual inheritance is not conditioning.

## Packet architecture and minimal-change revisions

- When combining a cinematic prompt-builder with an established production packet, preserve the packet’s useful operational spine: explicit reference roles, self-contained copy-paste blocks, numbered coverage, and a stated dispatch gate. Add cinematic sections only where they materially clarify the shot.
- Do not inherit generic style rules that conflict with continuity needs (for example, compulsory camera motion or an unnecessary edit list). For continuity action, prefer a one-take block or named cuts only when each cut has a real frame handoff.
- For a user-requested one-word rerun, perform a literal diff audit before dispatch: the requested token is the only prompt delta; preserve reference order, provider/model, duration, resolution, audio setting, and all other text byte-for-byte. Check adjacent lines, including audio, for competing nouns that could reintroduce the defect.

## Provenance minimum

Record source packet/kit asset, source and submitted prompt hashes, original clip/frame asset and timestamp, ordered references, provider/model/settings, output asset/log IDs, QA finding, and supersession status.

See `references/continuity-identity-failure-pattern.md` for a compact failure-to-revision pattern.
