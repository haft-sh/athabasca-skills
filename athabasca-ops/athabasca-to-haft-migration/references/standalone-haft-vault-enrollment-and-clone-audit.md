# Standalone Haft vault enrollment and duplicate-clone audit

## Situation class

A publicly reachable Haft host may be healthy and expose `/api/vault/tree`, while remaining absent from `haft remotes --json` for an authenticated Haft HQ account. Treat these as separate facts:

- **Public catalog/read surface** can support inventory and hash-only audits.
- **Managed mutation authority** requires central target discovery plus a valid scoped grant, or a separately authorized host-side enrollment process.
- Do not call `haft remote add` a grant: it only registers a caller-supplied static bearer record.

## Safe public preflight

1. Probe `https://<host>/health` to capture hosted build identity.
2. Fetch `/api/vault/tree` only when the endpoint is publicly intended to expose catalog metadata.
3. Flatten document entries and compare paths matching `name-2.md`, `name-3.md`, etc. against the unsuffixed sibling.
4. Use the tree-provided `contentHash` to classify clone candidates:
   - identical hash → deletion candidate after managed authorization
   - different hash → retain and flag for human review
5. Report exact counts, but do not attempt delete/move merely because tree metadata advertises those capabilities.

## Enrollment path when HQ discovery lacks the host

Enrollment must execute on the host that owns the vault root. A public hostname alone is insufficient because the flow writes/verifies host identity and verifier configuration.

1. Establish an authorized host-access route (prefer Tailscale/SSM; SSH only via a narrow temporary rule and approved key path).
2. From an authorized Haft HQ workstation, issue a short-lived pairing invitation bound to the intended slug, public URL, team, and account. Keep the file mode `0600`; transfer it privately, never via chat.
3. On the host, run managed enrollment with the real vault root, pairing file, public URL, team, and `--wait`.
4. Delete the pairing file after completion.
5. Re-run `haft remotes --json` from the operator environment. Only after it returns a centrally discovered, ready target should cleanup use scoped remote operations.
6. Verify the public hostname and a managed read/mutation canary before batch cleanup.

## Recurrence prevention

Haft import defaults to `--on-duplicate clone`; repeated imports create numeric filename suffixes. For canonical source libraries, use `--on-duplicate skip` for idempotent reruns. Use guarded `overwrite` only when an intentional source revision is authoritative.
