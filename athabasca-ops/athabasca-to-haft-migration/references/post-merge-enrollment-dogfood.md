# Post-merge managed-enrollment dogfood sequence

Use this when a new `haft remote enroll` implementation has just merged and a real hosted destination must be enrolled before a migration canary.

## Compatibility matrix

Record these independently:

| Surface | Required evidence |
|---|---|
| Repository | `origin/master` contains the merged enrollment PR. |
| Operator CLI | `haft version --json` identifies a build containing the command. |
| Haft HQ | production health/build identity corresponds to a deployment containing the enrollment APIs. |
| Destination | its binary exposes enrollment pairing/readiness routes and uses the compatible grant contract. |
| Published release | `haft update --check --json` may legitimately lag repository master; report that rather than conflating the two. |

A clean locally compiled CLI may be used to test current master before the release manifest advances. Install it through the repository's supported local-install script and verify the installed path. Do not run `haft update` when its advertised release is older than the required merged feature.

## Order of operations

1. Sync a clean default branch and inspect the merged PR and security-sensitive files.
2. Compile and install the operator CLI; verify `remote enroll` and `remote pairing issue` help.
3. Verify HQ deployment contains the required endpoints.
4. Upgrade the destination binary while preserving a rollback binary; keep verifier activation separate.
5. On the destination, issue the short-lived mode-0600 pairing invitation bound to the exact account, team, origin, remote slug, and vault.
6. Transfer the invitation through the approved secure channel.
7. **Only now** request/verify the operator OTP. Short-lived authentication should be just-in-time after slow deployment and pairing work is complete.
8. Run workstation enrollment with the pairing file.
9. If activation is required, configure central grants/JWKS for the exact service, restart it, and resume enrollment.
10. Require central discovery plus the no-content target-bound readiness proof.
11. Import one reviewed Markdown-mirror canary into a disposable path, then read and visually inspect it.
12. Batch-import documents only after the canary passes. Remote-only media remains a manifest lane until first-class registration exists.

## Authentication pitfall

An expired central session and expired refresh credential require a fresh OTP login. OTP challenges are short-lived. Do not request one before destination deployment/pairing preparation, and do not present an expired challenge as an active blocker; request a new challenge when the user is present.

## Completion language

Keep outcomes separate:

- CLI installed
- HQ compatible
- destination compatible
- destination enrolled
- delegated readiness proven
- canary imported
- canary read/render verified
- document batch imported
- remote-only media registered or still staged

Never collapse these into “migration complete.”
