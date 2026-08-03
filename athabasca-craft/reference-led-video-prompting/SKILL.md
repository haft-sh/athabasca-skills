---
name: reference-led-video-prompting
description: Build and dispatch reference-conditioned video prompts with explicit authority, spatial geometry, visible-text controls, and compact variation packets.
version: 0.1.0
---

# Reference-Led Video Prompting

Use when a generation must preserve specific characters, set geography, props, visible text, or staging from supplied images.

## Core rule: reference authority is literal

When the user names an image asset as the authority, use that exact asset. Do not substitute a derivative, a repair, or a visually similar frame unless explicitly authorized.

Assign every reference a single role in the dispatch preamble:
- character identity
- room/environment geography
- prop or text authority
- secondary character identity

Do not let two references compete for the same role without flagging the conflict.

## Visible text

When a designated reference controls visible text, use this language in the prompt:

> Match @imageN’s visible text, placement, scale, and line breaks. Do not add, replace, extend, or invent text, glyphs, labels, marks, or filler text beyond @imageN.

Do not separately restate strings unless they exactly match the reference. Reference conditioning improves fidelity but does not guarantee it; inspect render output before promotion.

## Spatial logic

Translate room or prop continuity into concrete, visible relationships. Never rely on generic placement language.

Bad: `The globe is on a shelf.`

Good: `The globe rests on the existing side/rear wall shelf, a separate plane several feet from the desk. It is never on the desk or directly in front of the seated subject. The subject is visible only as a small curved reflection in the globe.`

## Single-shot variation packets

For a difficult shot, make a compact packet of three genuinely different staging/camera solutions before spending on broad sequence reruns:

1. distinguish variants by camera and spatial grammar, not adjective changes;
2. keep the same approved reference stack unless testing references is the point;
3. include one canonical prompt authored with the project shot-prompt scaffold;
4. label the canonical variant clearly;
5. if asked only to bring up the packet, return the direct link only.

## Dispatch checklist

Before a paid run, verify:
- prompt text is from the reviewed packet;
- the supplied reference URLs map to the intended @image roles in order;
- no competing prompt instruction contradicts a reference-led text or geography authority;
- title and idempotency key identify the specific variation/rerun;
- render is reviewed before calling it canonical.
