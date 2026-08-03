# Managed remote readiness vs browser fallback

Use this note during Athabasca -> Haft migrations when a hosted `*.haft.sh` destination has moved to a new instance and the operator wants a full re-import.

## Durable lesson

A destination can be visibly present in `haft remotes --json` and still be **not import-ready**.

Two concrete degraded states matter:

- `readiness.state = projection-expired`
- `readiness.state = destination-verifier-not-ready`

In either case, the remote may advertise only:

- `allowedOperations = ["status"]`

and **not** `import` or `automation.media.ingest`.

## What that means operationally

If `haft remotes --json` or `haft remote status <slug>` shows only status permission/readiness degradation, expect:

- `haft import --remote <slug> ...` to fail **before upload** with `cli-remote.operation-not-advertised`
- remote-only media registration to remain blocked even if the destination hostname is live
- further import retries to be wasted motion until projection / verifier / enrollment state is repaired

Do not misdiagnose this as a document-bundle problem.

## Important separation: access grants vs readiness

A fresh `haft remote edit-access grant ...` can succeed in HQ and still **not** make the destination import-ready.

Reason:
- the grant exists at the control-plane layer
- but the destination may still lack a fresh central projection or a ready delegated-grant verifier

So the right next step is **managed remote repair** (enrollment / projection / verifier), not repeated import attempts.

## Browser fallback discipline

If you initiate browser login on the hosted destination while the CLI path is degraded:

- describe it as a **browser/UI access path**, not as proof that the requested CLI migration path now works
- request the OTP only after the six-digit code-entry screen is visible and you are ready to enter it immediately
- if the page reloads back to the email form or you request another code, treat earlier six-digit codes as invalidated by the new challenge
- keep the migration status language precise: browser login can help continue a UI import/review path, and may be a docs-lane fallback, but it does not prove CLI/API import readiness or remote-only media readiness

## Recommended reporting language

Good:
- "The export bundle is ready, but the hosted the project destination is not currently grant-backed import-ready."
- "CLI import is blocked by projection/verifier readiness, not by the Athabasca export bundle."
- "Browser OTP login was started as a separate UI path, pending the code."

Bad:
- "Migration is complete" when only the export bundle exists
- "Grant created, so remote import should work now"
- "Browser login fixed the remote migration path"
