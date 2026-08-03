# Hosted corpus repair and browser verification

## Problem shape

A filesystem/import operation may make a collection present in the Markdown tree and reader catalog while the browser sidebar remains stale. Do not equate an index-rebuild success message with user-visible completion.

## Verification ladder

1. **Source:** count expected Markdown files on the host; inspect a representative source file.
2. **Catalog:** verify the reader manifest/path count after rebuild.
3. **Explorer:** query the bounded Explorer children endpoint for the collection and check the direct-child count and filenames.
4. **Browser:** open the exact artifact URL the user supplied and inspect rendered prose and heading structure.

If the Explorer still lists missing or obsolete records, preserve a backup of the catalog/projection files, rebuild the catalog and Explorer projection cleanly, restart the service, and repeat all four checks.

## HTML/MOBI conversion quality gate

- Convert visual block containers (`div`, `p`) into Markdown paragraphs.
- Convert intentional `<br>` lineation into Markdown hard breaks only for verse.
- Merge inline tags (`em`, `i`, `strong`) into their surrounding sentence; do not emit a paragraph per text node.
- Normalize a chapter title once. Avoid the visually noisy `Chapter N`, `N`, `Title` triple heading.
- Before publishing, inspect a long chapter that contains prose, Sanskrit verse, citations, and inline italic terms.

## Safe repair posture

Back up the existing collection before replacement. If a rebuilt catalog produces obsolete artifact rows, preserve the pre-clean catalog/projection files in an audit directory before regenerating them. Report browser verification only after the exact linked page reads smoothly.
