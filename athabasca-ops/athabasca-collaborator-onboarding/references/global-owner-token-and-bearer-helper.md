# Global owner token + bearer helper

Use this when Hermes or another server-side agent needs stable non-browser access to Athabasca.

## Current durable pattern

For operator-grade bearer access:

- create an API token with `projectScopes: []`
- include `"owner"` in `operationModes`
- allow it to be non-expiring when appropriate (`expiresInDays: null`)

This zero-scope owner token is intentionally treated as global access across current and future projects.

## Hermes-side env contract

Store these in the active Hermes profile env:

- `ATHABASCA_BASE_URL`
- `ATHABASCA_API_TOKEN`
- optional `ATHABASCA_PROJECT_SLUG`

## Canonical Hermes plugin path

Use the repo-local Hermes plugin for durable agent access:

- `.hermes/plugins/athabasca-api`
- tool: `athabasca_request`
- tool: `athabasca_project_request`

The plugin reads the same env vars, attaches `Authorization: Bearer <token>` internally, and blocks raw terminal HTTP calls to the configured Athabasca host through a `pre_tool_call` hook.

## Compatibility helper path

Legacy live helper:

- `~/.hermes/scripts/athabasca_client.py`

Repo-tracked recovery/reference copy:

- `docs/reference/agent-tools/athabasca_client.py`

The repo copy is a duplicate for migration/recovery. The plugin is the preferred runtime location.

## Why this matters

A common failure mode is treating `401` as an API bug when the real problem is that the agent is calling Athabasca anonymously.

Before debugging routes, verify:

1. `ATHABASCA_BASE_URL` is set
2. `ATHABASCA_API_TOKEN` is set
3. the same call works through `athabasca_request` or `athabasca_project_request`
4. if the plugin is unavailable, the same call works through `~/.hermes/scripts/athabasca_client.py`

Only after bearer auth is ruled out should you treat the endpoint as a likely implementation issue.

## Convenience commands

Preferred plugin calls are made by the agent through `athabasca_request` / `athabasca_project_request`.

Compatibility CLI:

```bash
set -a && source ~/.hermes/.env && set +a
python3 ~/.hermes/scripts/athabasca_client.py list-projects
python3 ~/.hermes/scripts/athabasca_client.py get-project good-boy
python3 ~/.hermes/scripts/athabasca_client.py project-get good-boy research-report
```
