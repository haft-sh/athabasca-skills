# Case-sensitive QMD provider identity

## Failure mode

A provider that retrieves existing documents with a case-insensitive path comparison can collapse distinct files on a case-sensitive filesystem (for example, `README.md` and `readme.md`). The resulting index may report a successful scan but contain fewer active document identities than the canonical catalog.

## Safe response

1. Stop active embedding work once identity coverage differs from the deterministic catalog manifest.
2. Keep semantic and hybrid routing disabled/fail-closed.
3. Preserve the provider database for evidence, but do not reuse it as certified state.
4. Fix the provider to use exact path identity (or use a catalog-owned opaque-key projection).
5. Build a new provider database from scratch and reconcile before embedding and after completion.

## Required evidence

- Canonical eligible documents, keyed by page ID + exact relative source path + source/content hash.
- Provider active-document count and exact identity set.
- Exact collision count and case-fold collision count.
- Final reconciliation: `eligible = indexed = mapped`; `pending = unmapped = ambiguous = 0`.
- Direct vector canaries only after reconciliation succeeds.

## Compatibility trade-off

An implicit case-only legacy migration cannot safely distinguish an old normalized record from a genuine sibling file that differs only by case. Make such migrations explicit and operator-reviewed; do not retain an automatic case-insensitive fallback in the normal update path.
