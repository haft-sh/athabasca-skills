# Corpus completeness audit for compound source libraries

Use this reference when a hosted Haft vault was assembled from ebooks, archives, OCR output, or another source where a single input can expand into many pages.

## Evidence hierarchy

1. **Source inventory:** enumerate meaningful source files, exclude packaging artifacts, record size + SHA-256, and map each to one intended collection.
2. **Structural check:** extract or inspect a table of contents, chapter/section markers, and destination tree. A destination with a few pages can be valid only if its content/structure supports that conclusion.
3. **Content-volume check:** compare normalized word counts (or character counts) from source and deployed collection. This tolerates different page granularity while exposing large omissions.
4. **Public readback:** after rebuild, read the hosted reader manifest and count collection-specific pages; service-active alone is insufficient.

## Safe repair pattern

- Do the audit first; do not assume clone cleanup caused a missing-looking collection.
- Preserve/move the old collection outside the active vault before a structural replacement.
- Stage generated files outside the vault, stop the index service, copy in the new collection, rebuild, restart, and verify local + public counts.
- Keep manifests, source hashes, and conversion scripts as reproducible audit artifacts.

## External source boundary

If an original local ebook advertises more chapters than it can actually yield, classify it as a source defect. Do not blend in a different edition by default. With explicit user approval, an external replacement must be pinned to a commit/release and accompanied by a collection-local provenance page declaring source, revision, license/source declaration, and edition difference.

## Representative result shape

A useful completion note lists: source-file count, unique target collections, verified-present collections, repaired segmentation defects, repaired omissions, externally sourced replacements, active page/chunk totals, and public health/reader-manifest evidence.
