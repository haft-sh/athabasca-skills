# Full-shot expansion into fixed five-shot Seedance groups

Use this recipe when a user rejects a compressed prompt preview and explicitly requests every source shot in groups of five.

## Build recipe

1. Fetch the published HTML named as the template and the complete shot-list source.
2. Preserve the template's shared CSS, bounded main wrapper, group-card rhythm, reference cards, and copy-paste prompt treatment.
3. Parse the source shot list in order. Preserve each shot's title, subject/action, composition, focus, emotion, dialogue, and continuity intent.
4. Split sequentially into exact five-shot groups. For 30 source shots, use six ranges: `001–005`, `006–010`, `011–015`, `016–020`, `021–025`, `026–030`.
5. Display each global/source range in human-facing group metadata. Inside each Seedance prompt, reset numbering to unpadded `Shot 1` through `Shot 5`.
6. Give each group a declarative preamble assigning every `@imageN` to a role. Reset `@imageN` locally per group.
7. When a main room angle and reverse angle are supplied, treat them jointly as 360-degree geography anchors. Explicitly name the axis and stable objects they control.
8. Treat character sheets as identity/proportion references when their wardrobe or pose differs from the target scene.
9. If the user supplies exact asset IDs, use those IDs as deliberate overrides after resolving and visually checking each asset. Record replaced IDs and verify they are absent from the final HTML.
10. Preserve static black/white transition shots if “all shots” was explicit, even though such frames are normally inefficient generation material.
11. Upload as a new project document version unless the user explicitly requests in-place replacement. Mark unapproved previews red/draft and tag them by scene, Seedance, prompt-preview, and version.

## Mechanical verification before reporting success

Check the published R2 body, not only the local file:

- expected group-card count
- exact source ranges with no gaps or overlaps
- one local `Shot 1` reset per group
- five local shot headers per group
- required reference IDs present
- replaced reference IDs absent
- fixed-width wrapper present
- `white-space: pre-wrap` and overflow wrapping present
- image cards have explicit dimensions and constrained sizing
- Athabasca readback shows project attachment, phase, metadata, tags, and draft color

## Prompt-density rule

Five shots over 15 seconds implies approximately three seconds per shot. This is appropriate for intimate, performance-led room scenes because it leaves time for breathing, object business, small emotional changes, and spatial readability. Do not force faster montage timing merely because the source list is long.