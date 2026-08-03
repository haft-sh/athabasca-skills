---
name: athabasca-runtime-auth-wiring
description: Diagnose and align Athabasca long-running service credentials with the intended Hermes profile, especially for native OpenAI Codex/GPT Image generation.
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [athabasca, runtime, systemd, authentication, openai-codex, profiles]
---

# Athabasca runtime authentication wiring

## When to use

Use this when a project-scoped Athabasca generation route reports missing, expired, or unexpected credentials while the initiating Hermes chat/session appears authenticated — especially for native OpenAI Codex / GPT Image requests.

## Core model

A Hermes chat/profile and the long-running Athabasca service are separate processes. A valid OAuth credential in the chat does not automatically make it available to Athabasca.

For Codex auth, Athabasca resolves its store from:

```text
$HERMES_HOME/auth.json
# otherwise
$HOME/.hermes/auth.json
```

The active systemd service environment determines which path it reads.

## Workflow

1. **Keep the canonical request path.**
   For project stills, use `POST /api/projects/:slug/generate/image`. A credential failure is not a reason to switch to a deprecated top-level endpoint or silently swap providers.

2. **Confirm the failure class.**
   Distinguish missing/expired credential errors from prompt, provider-content-policy, model, persistence, or attachment failures.

3. **Inspect the actual service, not the operator shell.**
   ```bash
   systemctl --user status athabasca-dev.service --no-pager -l
   systemctl --user cat athabasca-dev.service
   tr '\0' '\n' </proc/<main-pid>/environ | grep -E '^(HOME|HERMES_HOME)='
   ```

4. **Compare candidate auth stores without printing secrets.**
   Inspect only whether the provider's `access_token` and `refresh_token` fields are present in the global and intended profile `auth.json` files. Never emit token values to logs, chat, or generated artifacts.

5. **Point the service to the intended profile deliberately.**
   If the desired Codex credential belongs to profile `<profile>`, use a user-systemd drop-in:
   ```ini
   # systemctl --user edit athabasca-dev.service
   [Service]
   Environment=HERMES_HOME=/home/<linux-user>/.hermes/profiles/<profile>
   ```

6. **Reload, restart, and verify.**
   ```bash
   systemctl --user daemon-reload
   systemctl --user restart athabasca-dev.service
   systemctl --user status athabasca-dev.service --no-pager -l
   ```
   Then retry the same project-scoped generation request. On success, verify the returned Athabasca asset, its R2 `publicUrl`, and requested attachment state before reporting completion.

## Decision rules

| Observation | Correct response |
|---|---|
| Chat profile token exists; service-selected store lacks it | Wire the service's `HERMES_HOME` to the intended profile. |
| Both stores lack a valid token | Re-authenticate the selected owner profile; do not invent a credential. |
| Token is valid but generation fails upstream | Treat as a provider/API failure and report the precise error. |
| Image succeeds but no project asset/attachment appears | Treat as a persistence/attachment failure, not an auth failure. |

## Pitfalls

- Do not assume the current chat's OAuth state is inherited by systemd services.
- Do not copy raw token values into an environment file or shell history.
- Do not create a second global credential merely because the service is reading the wrong auth store; that muddles billing/account provenance.
- Do not change provider to a fallback merely to work around a profile-wiring error when the user explicitly requested native GPT Image.
- A service restart is an infrastructure change: verify the unit is active and the endpoint works after restart.
