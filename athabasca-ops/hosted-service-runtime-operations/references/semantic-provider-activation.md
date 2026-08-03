# Semantic-provider activation preflight

Use this for a deployed application that can route semantic retrieval to a private provider.

## Separate the states

Treat these as distinct, evidence-bearing states:

1. **Semantic-capable release**: route and adapter are deployed, but routing remains disabled.
2. **Provider-ready**: the actual provider contract is reachable on loopback/private networking, is pinned to the deployed revision, and targets the certified index.
3. **Activation-eligible**: relevance, latency, privacy, freshness, and rollback gates pass.
4. **Activated**: routing is enabled during an explicitly approved release window.

Never equate route existence, provider liveness, or a completed ticket with activation eligibility.

## Preflight sequence

1. Read live health and capture exact build commit **and** version.
2. If the version is wrong but the commit is correct, inspect the service environment for a stale embedded-version override. Back up the env file, change only the expected entry, restart, and verify both local and public health before proceeding.
3. Inspect the *effective* provider process configuration—not just an old bridge service name or static source file:
   - provider service active/enabled state;
   - loopback binding only;
   - provider build SHA;
   - QMD binary/runtime revision;
   - collection name and canonical vault root;
   - index document/vector cardinality and freshness.
4. Prove one private provider request returns contract-valid candidates. Record only aggregate status/counts; do not log raw queries, paths, excerpts, endpoints, or credentials.
5. Time a real cold/warm query under the production timeout. A provider that only succeeds after increasing the timeout is not ready for an activation gate. Do not raise timeouts before cancellation, child cleanup, queue bounds, and latency evidence exist.
6. Keep public semantic routing disabled until all gates pass. Verify a semantic request reports a truthful disabled/degraded keyword fallback while disabled.

## Accelerator reuse and access

When an existing accelerator is expected but not visible in the service's usual AWS region, search the account inventory by instance type and stable name across the stated historical region before proposing a replacement. A stopped GPU instance with its persisted volume is normally preferable to a new host.

1. Verify instance ID, region/AZ, stopped/running state, attached volume, and instance profile.
2. Start it only for an approved concrete workload. A first `InsufficientInstanceCapacity` response is not proof the instance is unrecoverable; re-read state and make one bounded retry before considering migration.
3. Prefer SSM when the instance profile reports online. It avoids opening public SSH and can verify GPU model, pinned runtime, index cardinality, and Tailscale status without exposing secrets.
4. Do not infer that a GPU makes the provider fast enough. Measure real QMD candidate requests against the same 2-second production deadline.

## Certified index and QMD runtime pitfalls

A QMD SQLite index can be correct while its collection configuration is missing or stale. Verify both layers:

- Query aggregate active document and vector cardinalities from the candidate index.
- Query the database's stored collection name; do not rename or mutate the derived index merely to improve a label.
- Reconstruct/configure the collection root from an indexed relative document path and prove it resolves to the intended canonical vault before using the provider.
- Keep the collection label and filesystem source root private; public evidence needs only cardinalities, pinned QMD revision, and bounded provider state.

QMD's package script may invoke `tsx`, which in turn uses the host's system Node. A native SQLite binding built for a different Node ABI can fail even though the pinned source and index are intact. Diagnose the ABI mismatch from a sanitized error, then use the pinned Bun runtime to execute the TypeScript CLI directly (`bun src/cli/qmd.ts …`) rather than invoking the package script. Reinstall/rebuild dependencies only as needed for the intended runtime; then re-run a direct candidate probe before restarting the provider.

## Legacy bridge pitfall

A pre-existing QMD bridge may be running yet still be unsuitable for the current server integration: it can point to a stale collection, old CLI/runtime, unfinished index, or an incompatible response shape. Do not enable a new semantic adapter against it merely because its process is healthy. Validate its response contract and index provenance first.

## Capacity escalation

If the certified CPU-backed index cannot meet the agreed semantic latency budget, stop the provider and preserve disabled routing. Restart an existing accelerator only with an approved concrete workload. Provisioning a *new* accelerator is a cost-bearing infrastructure change and needs explicit authorization even where activation is generally approved.

## Rollback invariant

Before public activation, prove that setting the semantic enable flag off and restarting restores keyword-only operation with truthful disabled status. Preserve the previous server artifact/configuration until this is demonstrated.
