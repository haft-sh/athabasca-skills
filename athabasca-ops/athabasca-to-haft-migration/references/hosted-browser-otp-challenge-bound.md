# Hosted Haft OTP canary pitfall

For hosted `*.haft.sh` migration or visual-verification work that requires browser OTP login:

- Treat six-digit browser login codes as **challenge-bound**.
- If you request a second login email, assume the earlier code is no longer valid for the new challenge, even if it is still within the displayed expiry window.
- Therefore, request the OTP only when you are ready to enter it immediately.
- If a code entry leads to a blank page or React auth-screen crash after you have re-requested a code, suspect **challenge mismatch** before spending time on deeper app debugging.
- For canary-first migration flows, finish CLI prep, file prep, and target selection first; do the browser OTP step last.

This came up during GLY migration follow-up on `gly.haft.sh` while trying to visually verify a single-image canary after re-requesting login codes.