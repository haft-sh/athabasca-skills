# Prompt Packet Review Checklist

Use when turning a script-derived shot list into a human review / dispatch surface.

## Packet contents

- State the source script and source shot-list artifact IDs/URLs.
- Show source-shot ranges in each group; reset model-facing numbering to local `Shot 1…N` per group.
- Include every required beat when operating in full-shot preservation mode; mechanically confirm the group totals equal the source-shot total.
- Put exact dialogue only on the shots where it is performed or heard; retain non-dialogue foley/atmosphere instructions separately.
- Include a per-group continuity lock covering axis, screen direction, prop state, scale state, lighting, and any delayed tonal shift.
- Include real reference-image cards with thumbnail, asset ID, short control purpose, and an `Open full size` link.

## Review surface

- Treat thumbnails as scanning aids, not the detail-review surface.
- Use a bounded main container; all cards, captions, tables, and prompt blocks must have `min-width:0`, safe wrapping, and no horizontal bleed.
- Use `white-space: pre-wrap` and `overflow-wrap: anywhere` for copy-paste prompt blocks.
- Label the packet `DRAFT` until the user has reviewed creative and reference choices; draft assets should use the red color tag.

## Persistence and proof

- Project-attached HTML must be uploaded through `POST /api/projects/:slug/media` with storyboard phase metadata.
- Verify the returned asset attachment, permanent public URL, and remote HTML body markers (bounded layout, wrapping, full-size links, group coverage) before sharing.
- Do not final-handoff a local HTML or Markdown path as the collaboration surface; local files are staging only.
