# Seedance continuity and semantic prompt audit

## Pre-dispatch audit for continuing clips

1. Treat every named hard-cut/time segment as a potential fresh synthesis. Repeating “retain continuity” in the next segment is not a substitute for a real predecessor frame.
2. For high-energy transitions (impact, landing, prop transfer, size change), either generate one continuous beat or split at the transition and feed the accepted prior end frame to the next clip.
3. Before dispatch, scan literal nouns and verbs for accidental visual instructions:
   - `boot` / `shoe` / `sandal` can introduce footwear; use `bare turtle foot` and `visible toes` when needed.
   - `mouse-sized` / `Mouse the guardian` can produce a rodent; say “same turtle the guardian at ankle height; never a mouse, rodent, mammal, or new creature.”
   - `helmet` can invent a new costume item unless it is canonically anchored.
   - `open path`, `screen-right`, and `left-to-right` can turn a confrontation beat into a lateral escape walk. Define relation instead: “one small forward step reducing distance to the guardian’s fixed lower armored leg; no lateral travel, retreat, path-following, or pass-through.”
4. State exactly one scale change per clip. Anchor it to fixed environment rulers and require in-place reduction: no float, teleport, slide, sink, replacement, or new character.
5. Repeat critical identity, bare-foot, prop-side, light, geography, and no-injury locks in every separately generated continuation; text inheritance across clips is not conditioning.

## First-frame tradeoff

A predecessor frame is the strongest continuity authority but can impose unwanted initial pose/motion. If the user rejects the inherited opening movement, remove the predecessor image intentionally and retain only canonical character plus environment references. Explicitly state the continuity-vs-staging tradeoff in the packet/provenance.

## Review discipline

- Do not treat a generated continuation as canonical merely because it completed.
- If the wrong predecessor or a rejected predecessor was used, mark the output yellow and record the correct asset/frame before retrying.
- Attach selected predecessor frames as project media with source asset and timestamp in provenance, not only as a temporary local file.
