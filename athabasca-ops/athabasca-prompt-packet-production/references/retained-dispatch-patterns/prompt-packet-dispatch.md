---
name: prompt-packet-dispatch
description: Create, revise, preview, and dispatch packet-governed Athabasca video prompts without text or reference drift.
version: 1.0.0
---

# Packet-Governed Prompt Dispatch

Use when a user asks to build, revise, inspect, or generate from an Athabasca HTML prompt packet.

## Core rule

A published packet is the dispatch authority. For a requested generation, submit its designated copy-paste prompt without summarizing, rewriting, adding continuity prose, or otherwise changing it.

## Revision workflow

1. Start from the last published HTML packet, not a reconstructed prompt.
2. Apply only the explicitly approved edits. For reference changes, update cards, attachment order, `@imageN` role text, and every matching prompt reference consistently.
3. Preserve all unedited shot text, timing, action, dialogue, and staging.
4. Publish a new packet version; do not silently overwrite the prior version.
5. Before dispatch, make an explicit reference manifest:
   `@imageN → asset ID → resolved public URL → intended role`.
6. Confirm reference URLs are not accidentally duplicated when the packet specifies different source assets.
7. Extract the exact bounded group prompt from the published packet (for example, Group B through immediately before Group C). Never submit an instruction such as “use/preserve the approved full prompt” in place of the actual packet text: the provider cannot retrieve packet content by reference.
8. Compare the extracted prompt to the outbound prompt byte-for-byte after line-ending normalization, and compare the ordered URL manifest before dispatch. Do not claim prompt fidelity without this check.
9. If a newly generated still, corrected reference, or first-frame authority materially changes a group’s reference stack, publish a packet revision first. Update its reference cards, ordered manifest, `@imageN` role text, and affected prompt copy together. Never label an abbreviated corrective rerun as an exact packet dispatch.
10. Dispatch the exact group prompt with that ordered URL manifest and a deterministic idempotency key.
11. When a user gives a predecessor/last frame, classify it explicitly before revising the packet: **continuity authority** preserves layout/state across the group; **mandatory first-frame authority** requires frame 0 to match it exactly. For mandatory first frames, state that requirement before all other prompt content and repeat it in Shot 1. Add the image to the revised ordered manifest and publish before dispatch.

## User-facing behavior

- If the user says “bring up” or “show” a packet, reply with the direct packet link only unless they request analysis.
- Generation reports should be brief: result link, asset ID, log ID, and material deviations only.
- Do not replace a requested action with process explanation. Perform checks silently when possible; only surface a blocker that prevents a correct dispatch.

## Pitfalls

- Never use broad HTML regex replacement without limiting it to the individual reference-card element being changed.
- Do not claim a packet is ready or that prompt equality was verified unless the exact text/reference manifest was checked.
- A model rendering the wrong subject or state is model-compliance drift; it is distinct from packet-to-dispatch text/reference drift. Diagnose and repair the right layer.
