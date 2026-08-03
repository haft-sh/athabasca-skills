---
name: athabasca-prompt-packet-production
description: Build, revise, and dispatch project-attached AI-video prompt packets with explicit reference roles, dialogue timing, and reviewable generation groups.
version: 1.0.0
---

# Athabasca Prompt Packet Production

Use for production prompt HTML / Markdown packets that convert shot lists into reviewable, dispatch-ready AI-video groups.

## Core rules

- Treat project-attached media and their `publicUrl` values as canonical inputs; local files are staging only.
- Give every reference a single explicit role: identity/style authority, location/style authority, blocking-only, prop authority, or human-review candidate.
- If a reference is composition-approved but style-noncanonical, label it **blocking-only** in both the inventory and prompt. Do not let it silently override canonical character or location styling.
- Reset `@imageN` numbering per generation group and show the ordered asset mapping in each group.
- Publish a fresh immutable prompt-packet asset after material revisions so reviewers do not fight stale CDN/browser content.

## Dialogue timing and group design

1. Estimate whether dialogue fits the lane before dispatch. A natural, visible performance needs more time than text on the page suggests.
2. Keep compact visual coverage separate from long on-camera speech.
3. For a long speech, create:
   - a **visual master** for edit coverage;
   - semantic **dialogue carriers** with one speaker, one performance action, and a clean cut point each;
   - reaction / insert coverage where dialogue can continue off-screen in the final mix.
4. Do not turn a deliberately clipped test fragment into the final intended line.
5. When dialogue carriers overload a parent group, split them into an adjacent **helper group**. The helper must contain the actual expanded shots—not merely link to an appendix—and must declare its parent-group continuity handoff.
6. Preserve source/global shot IDs for reviewers, but use local sequential shot numbers in the copy-paste generation prompt.

## Reference hierarchy example

- Character sheet: face, costume, props, recurring identity.
- Location still: geography, palette, scale, lighting language.
- Blocking still: camera height, foreground/midground placement, scale relationship only.

When constraints conflict, identity/style and location/style authorities win over a blocking-only image.

## Continuity-critical character and prop coverage

For recurring characters, identity includes prop mechanics, screen direction, and camera state—not only face and costume.

1. **Attach real authorities.** Attach each visible character’s canonical sheet. For a continuation, attach an approved final/pre-cut frame from the exact preceding shot as the first-frame continuity authority; prose alone is insufficient.
2. **Keep authority roles separate.** The preceding frame controls entry composition, lighting, grade, camera axis, and immediate state. Canonical sheets control identity and prop design. Blocking-only images cannot override either.
3. **Publish a state table before dispatch** when props matter: per shot name shield arm/strap state, hand contact, sword hand or sheath side, entry/exit state, and permitted transition. Explicitly prohibit rim-gripping, arm-side switching, prop teleportation, and inferred off-screen stow.
   - Specify only visible, reference-supported contact states: for example, a hand visibly closed around a handle, or a shield visibly secured by arm straps. Do not invent unseen rear hardware, sheath mechanics, or blade poses merely to sound precise.
   - Never use `sheathed` as a standalone state. If no canonical sheath/scabbard is visible, choose a stable held state instead; otherwise models frequently render an unattached or floating prop.
   - Repeat a concise prop-state reminder in each shot where the prop is visible. Long global mechanical language does not replace visible shot-level contact direction.
4. **Lock spatial and camera continuity per shot.** State screen-left/right and facing direction for both characters. State locked camera or the exact permitted movement. If pullback is unwanted, prohibit zoom-out, dolly-back, crane-out, and reframing explicitly.
5. **Isolate mechanics into helpers.** A fall → recovery → prop-stow action should be a dedicated helper with explicit entry/exit states; split recovery and gear-stow into separate clips if both are important.
   - For a slapstick impact chain, describe the causal order as visible beats (charge → contact → deformation → rebound → airborne travel → landing) rather than generic “stumble” or “fall.” State what does *not* move, where the character travels, and how each prop stays attached.
   - For every hard cut inside a continuous action, begin the next shot with an explicit **start-frame handoff**: the exact preceding final pose, body orientation, face/costume condition, prop contacts, screen position, and allowed continuation. A new shot description without an incoming state invites visual resets.
   - If the action is non-injurious, say so explicitly and prohibit unwanted evidence of harm: black eye, bruising, cuts, blood, swelling, torn clothing, cracked shell, and helmet damage. “Safe” or “controlled” alone does not reliably prevent injury-like model inference.
   - Do not mistake a text handoff for a visual handoff. Even a detailed “retain exact continuity” instruction after a HARD CUT can reset pose, face, props, or geography. When a cut must preserve a high-risk physical state, dispatch the preceding action as its own clip, extract its verified final frame, and use that actual frame as `@image1` for the next clip.
   - Splitting is not a cure for bad action design. If a stunt requires several linked mechanics (for example elastic impact, launch, airborne rotation, bounce, slide, and recovery), first reduce it to one legible comic event or request purpose-built coverage. A chain that is mechanically over-specified often produces floaty, model-invented movement even with a real predecessor frame.
6. **Avoid ambiguous repeated dialogue.** If a line is echoed by a prop/creature/off-screen source, generate it as separate insert coverage or omit it from a character dialogue helper. Adjacent duplicate lines often collapse speaker attribution.

## Reference minimization and operator pacing

- Assign one authority per visual domain. Multiple environment frames with overlapping geography, palette, or layout are competing authorities—not harmless extra context.
- Keep only the strongest reference for a domain per group. Retain a second location image only when it has a distinct, shot-critical role that the primary authority cannot cover.
- Treat exploratory grids and emotion/look tests as weak identity sources, but retain one when it is the user-approved authority for a unique performance state, expression, or blocking beat. Do not remove that reference merely to reduce count; label its narrower role explicitly so it cannot compete with character identity.
- A collaborator’s explicit selection of a specific legacy or sequence-specific character asset overrides recency heuristics. Preserve that exact asset in the packet and dispatch stack, document its role as the sequence identity authority, and do not substitute a newer character sheet without explicit approval.
- Do not infer a provider reference-count cap from one generic upstream error. Confirm an actual documented limit or isolate the failing URL/role; a retry with the same approved stack and a fresh idempotency key may succeed.
- When a hero prop needs unusually strong fidelity, isolate its reveal into a short insert with the prop authority and one location/plinth context reference, rather than diluting it among broad sequence references.
- When an operator asks to open a packet, return its direct permanent link only. Do not add optional extraction, hashing, or process commentary.
- When an operator authorizes generation after packet review, dispatch the reviewed group directly; use validation proportionate to the paid action and do not block on optional parser mechanics.

## Pre-dispatch checklist

- Confirm all reference asset IDs resolve to green-approved assets unless intentionally marked as noncanonical blocking context.
- Confirm ordered reference URLs match prompt slots exactly.
- Confirm each group has a practical shot count and duration.
- Ensure no required long dialogue is compressed into an unrealistic visual beat.
- Use an idempotency key for each paid generation intent.
- For reference-heavy paid runs, verify the provider route forwards every intended reference image before dispatch.

## Packet QA

- Verify the published HTML contains every expected asset ID and has no obsolete reference IDs.
- **Reference-led visible text:** when an image reference is assigned as the authority for a calendar, sign, note, poster, jersey, or other readable detail, do not separately paraphrase or extend its wording in the prompt. Require the render to match the reference’s visible text, placement, scale, and line breaks; prohibit added filler copy, pseudo-text, glyph clusters, or unapproved labels. A visible-text defect in that authority image is a reference-quality issue to fix before using it downstream.
- **Direct packet requests:** when a collaborator asks to bring up or inspect a packet, provide its permanent link directly. Do not add extraction, hashing, or dispatch-process commentary unless they explicitly ask for validation or generation.
- **Single-shot repairs:** when only one shot needs correction from a multi-shot group, make a dedicated short shot/variation packet rather than rerunning unrelated coverage; express the corrected geography with concrete foreground/midground/background relationships.
- Search the public packet for forbidden / superseded terminology after user corrections.
- Open the public packet and verify the helper group is navigable and visually separate from its parent group.
- Record reference-role caveats in provenance and packet copy, not only in chat.
- A prompt packet must be a usable **HTML review surface**, not merely HTML containing text. Use the project's established dark card layout: hero/status, reference cards with thumbnails and explicit roles, director locks, a clearly separated copy-paste prompt block, and visible pre-dispatch QA gates.
- Resolve every ordered reference URL before paid dispatch. If an approved reference has a stale URL, repair the attachment/provenance mapping only; do not silently rewrite the approved source prompt.
- Extract the copy-paste block programmatically, normalize line endings only, and store source/submission hashes. Block paid dispatch if hashes differ.

## Controlled prompt-architecture comparisons

When comparing a general prompt-builder format against a continuity-first packet, publish two immutable, side-by-side prompt blocks. Keep story beats, reference order, duration, dialogue, and prop state constant; vary only the intended architecture (such as section vocabulary and camera-motion language). Generic authoring rules such as “motion from frame one” yield to explicit continuity requirements such as locked framing—record that override in the compared packet instead of silently blending variants.

Submit each variant with a distinct idempotency key and provenance hash. If a client call times out, query the idempotency record before retrying; never blindly resubmit a paid comparison variant.

## Related reference

See `references/dialogue-helper-groups.md` for a reusable long-dialogue split pattern.
