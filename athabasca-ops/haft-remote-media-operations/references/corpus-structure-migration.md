# Hosted Corpus Structure Migration

Use this for a file-backed corpus whose Explorer tree, reader paths, catalog, and semantic index can diverge.

## Evidence layers

Keep these separate:

1. **Source inventory** — upstream commit, license/permission, folder/title manifest, and file hashes.
2. **Vault filesystem** — actual paths, document counts, parsed metadata, and hashes.
3. **Explorer projection** — direct-child tree rows and exact artifact routes.
4. **Retrieval index** — current collection/index build and semantic-search results.

An Explorer count may represent direct child nodes rather than total Markdown documents. A missing Explorer row does not prove that a collection is absent from disk.

## Safe migration pattern

1. Snapshot source and destination manifests before changing paths.
2. Normalize title/path matching (punctuation, diacritics, singular/plural, legacy naming) but retain original source IDs.
3. Classify each proposed move as **unique**, **byte-identical duplicate**, **near duplicate**, or **conflict**. Different filenames are not proof of uniqueness.
4. Build an explicit old-path → new-path map. Preserve reader aliases/redirects or record a deliberate compatibility break before moving public material.
5. Apply moves in a bounded batch with a rollback manifest. Do not run a full index rebuild after every small move.
6. Rebuild the Explorer/catalog projection and semantic index once after the approved batch.
7. Verify: on-host file count, Explorer direct-child structure, selected reader URLs, and search retrieval for both canonical and legacy terms.

## Ingesting a third-party corpus

Before bulk import, record the upstream URL, immutable commit SHA, license text/location, granted scope, import timestamp, and per-file source path/hash. For a large multi-year collection, import one bounded cohort first, validate browser/tree/index behavior, then import the remainder with the same manifest pipeline.

## GPU-worker boundary

GPU helps with semantic near-duplicate detection, embeddings, reranking, and metadata enrichment. It does not itself repair a hosted reader: an index built on a separate worker is useful only when the hosted application is deliberately wired to consume that worker's retrieval service or derived index.