---
name: prompt-packet-revision-control
description: Revise approved Athabasca HTML prompt packets without semantic or structural drift.
version: 1.0.0
---

# Prompt Packet Revision Control

Use for any request to alter an existing approved or dispatchable HTML prompt packet while preserving its full source content.

## Principle

A packet revision is a controlled transformation, not a rewrite. Preserve every shot, line of dialogue, action, composition, focus, emotion, duration, and packet section unless the user explicitly authorizes that exact change.

## Procedure

1. Retrieve the canonical source packet and save an immutable local source copy.
2. Identify the precise approved edit. For reference deprecation, state the removed asset/reference role and any necessary `@imageN` renumbering.
3. Clone the complete HTML packet. Do not recreate it from a browser snapshot, summary, or hand-authored abbreviated layout.
4. Apply only mechanical edits: remove the specified reference card/attachment and update role labels and `@imageN` tokens consistently.
5. For minified HTML, edit complete bounded reference-card elements. Never use a broad regex that can span unrelated markup. Assert expected removal count, remaining deprecated-reference count of zero, expected reference-card count, and a plausible output-size ratio.
6. Extract every copy-paste prompt block from source and revision. Normalize line endings only, then produce a source-vs-revision diff. It must contain only the approved reference-role removal/renumbering. Block publication if broader prompt or structural drift appears.
7. Calculate and record source and revision SHA-256 hashes. Render the revised HTML and visually confirm the packet wrapper, cards, groups, and prompt blocks remain intact.
8. Validate dispatch inputs independently of prompt text: every `@imageN` role must resolve to the corresponding intended asset URL, and distinct visual roles must not accidentally reuse a duplicated URL. Treat duplicated/misordered reference URLs as a dispatch-blocking error.
9. Upload and attach the revised packet through Athabasca only after verification. Dispatch only the exact extracted revised copy-paste prompt, retaining the audit record.

## Never

- Summarize or reauthor shot prose while making a reference-only revision.
- Treat a selected continuity frame as merely a character identity image when the user specifies it as the first-frame authority.
- Report a packet as published, valid, or dispatched if size/card-count/diff verification failed.
