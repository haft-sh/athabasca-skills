# Living Docs publish template preservation

Session-derived lesson: when publishing an edited Living Doc imported from an existing public HTML artifact, do not serialize from the manifest alone unless no usable source/template exists.

## Problem signal

A republished Prompt Preview contained only the changed/known manifest blocks and lost the original document shell:

- original CSS and layout
- header/title/provenance sections
- Prompt Preview visual template
- surrounding static explanatory content

This happened because save/publish regenerated HTML from the structured manifest using the minimal fallback serializer. The manifest is an editable projection, not the full artifact.

## Durable rule

For imported HTML-first artifacts, publishing should preserve as much of the original source file as possible:

1. Sanitize the base/source HTML.
2. Keep the original document shell: doctype, head, styles, body structure, header, static prose, and non-editable context.
3. Replace only recognized editable prompt-group sections or marked blocks.
4. Embed/update the public Living Docs manifest.
5. Use a minimal generated HTML serializer only as a last-resort fallback when no source/template HTML is available.

## Implementation pattern

Preferred base selection for publish/save:

1. Current draft `htmlSnapshot`, if it still contains the source/template shell.
2. Original imported source/public URL from manifest or metadata, fetched and sanitized, especially for older drafts that were already saved as minimal HTML.
3. Minimal serializer fallback only if neither base is available.

Serializer shape:

- `serializePromptPreviewHtml(manifest, { baseHtml })` should branch to a base-preserving serializer.
- The base-preserving serializer should strip unsafe scripts/event handlers/javascript URLs, remove stale `data-ath-*` decorations if needed, update `<title>`, replace the contiguous prompt-group section range, add Living Docs attributes to `<main>`, and append the public manifest script.
- Tests should assert both edit correctness and preservation markers such as original CSS class names, header text, and static sections.

## Regression test checklist

Add a focused fixture that includes:

- source-only header/static sections outside prompt groups
- distinctive CSS/template class names
- multiple prompt groups
- a patch changing one prompt or asset ref

Assert the serialized/published HTML:

- still contains source header/static content and style/template markers
- contains the updated prompt/asset ref
- embeds `type="application/athabasca+json" data-ath-manifest="living-doc"`
- does not contain unsafe scripts, event handlers, or `javascript:` URLs

## Product expectation

Published R2 assets are effectively immutable. If an already-published URL is wrong/minimal, fix the serializer path and republish the Living Doc to produce a new corrected asset URL rather than trying to mutate the old public file in place.
