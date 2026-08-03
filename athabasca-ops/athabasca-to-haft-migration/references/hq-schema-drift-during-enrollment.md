# HQ schema drift during managed enrollment

Use this when a current CLI/HQ/destination build is deployed but authenticated discovery or pairing returns opaque `central-api.http-500` / `pairing.central-unavailable` failures.

## Diagnostic sequence

1. Confirm build identity independently on operator CLI, HQ, and destination.
2. Verify HQ `/health`, then separately exercise authenticated account-status and remote-target discovery. Health alone is insufficient.
3. Classify the failed enrollment stage:
   - preflight: account/session/team query
   - claim: challenge, server claim, or vault claim
   - finalize: projection refresh or JWKS installation
   - activation: destination route gate/verifier state
4. Inspect the current schema source for additive migrations used by that stage.
5. Query live `PRAGMA table_info(...)` for the involved tables. Compare actual columns, not just migration history or `PRAGMA user_version`.
6. If the schema is partial, add only exact missing columns from reviewed source. Verify every statement and re-run the affected authenticated route.
7. Expect bounded remote-replica lag after DDL or claim creation. Confirm the exact route directly, then retry the same journal after a short delay.

## Managed-enrollment columns worth checking

Check current source rather than treating this list as timeless. The enrollment rollout that motivated this procedure depended on additive fields such as:

- server claim label and enrollment assertion reference
- vault slug, remote slug, API origin, verifier state, and enrollment assertion reference
- claim-challenge enrollment binding
- enrollment assertion-use/replay tables

## Recovery invariants

- Preserve the existing enrollment journal and authoritative claim IDs.
- A consumed pairing stage requires a fresh invitation, not parallel claims.
- Do not hand-edit claim rows, fabricate IDs, or fall back to a manual bearer.
- Stage central API/JWKS configuration before pairing finalization.
- Enable delegated grants only after local identity and JWKS installation; restart the exact service, then resume.
- Treat direct production DDL as an emergency repair requiring a follow-up idempotent migration/drift-reconciliation code fix.

## Verification

Enrollment is not complete until all are true:

- central target discovery reports the intended custom origin
- local identity and public JWKS are installed
- destination verifier is enabled after restart
- a fresh target-bound no-content readiness grant is accepted
- a one-document remote import completes and the artifact can be read/rendered
