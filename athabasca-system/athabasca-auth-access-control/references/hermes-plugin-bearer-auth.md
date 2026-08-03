# Hermes plugin bearer auth for Athabasca

Use this reference when converting Athabasca API access from prompt-guided bearer-token scripts into a persistent Hermes plugin.

## Decision

Prefer a first-class Hermes plugin tool over AGENTS.md instructions or ad-hoc curl snippets.

Recommended shape:

- plugin reads `ATHABASCA_BASE_URL` and `ATHABASCA_API_TOKEN` from the active Hermes profile environment
- plugin lives at `.hermes/plugins/athabasca-api`
- plugin registers `athabasca_request(method, path, query?, json?, timeout?)`
- plugin registers `athabasca_project_request(method, project_slug?, suffix?, query?, json?, timeout?)`
- tool normalizes relative paths against `ATHABASCA_BASE_URL`
- tool attaches `Authorization: Bearer <token>` internally
- tool returns structured status/payload data and never logs the token
- optional helper behavior can resolve project-relative paths using `ATHABASCA_PROJECT_SLUG`

## Hook usage

Use `pre_tool_call` as a guardrail, not as the primary auth injector.

Good hook behavior:

- inspect terminal calls for raw `curl`, `wget`, HTTPie, or `xh` requests to the configured Athabasca host
- block those calls with a message telling the agent to use the Athabasca plugin tool
- optionally allow explicitly safe unauthenticated endpoints such as `/api/health`

Avoid:

- mutating arbitrary shell command strings to splice in bearer headers
- relying on undocumented in-place tool-call argument rewriting
- parsing every possible curl form as a security boundary

The hook is policy/audit. The plugin tool is the deterministic auth path.

## Migration sequence

1. Keep `~/.hermes/scripts/athabasca_client.py` temporarily for compatibility.
2. Add the repo-local Hermes plugin at `.hermes/plugins/athabasca-api` with `plugin.yaml`, package files, schemas, and tests where practical.
3. Register the explicit `athabasca_request` and `athabasca_project_request` tools and verify `GET /api/projects` with the active profile env.
4. Add the `pre_tool_call` block for raw curl calls to the Athabasca host.
5. Update skills/docs to prefer the plugin and demote the script to fallback/recovery.
6. Install or expose the plugin to the active Hermes runtime profile, then enable it with the normal Hermes plugin enable flow. Repo-local plugin files alone are not enough for a running gateway/profile unless that profile is configured to discover them.
7. Restart the Hermes gateway/profile so plugin/env changes are loaded.
8. Remove the old helper only after CLI, Telegram, and gateway paths all work through the plugin.

## Implementation checklist

- Keep the plugin dependency-light; stdlib HTTP is sufficient for simple JSON API calls and avoids profile install friction.
- Split responsibilities cleanly: schemas/metadata in `plugin.yaml`, tool registration in plugin code, and `pre_tool_call` hooks as enforcement guardrails.
- Normalize and validate outbound targets: accept relative API paths, resolve them against `ATHABASCA_BASE_URL`, and refuse absolute URLs whose host does not match the configured Athabasca base host.
- Return JSON-like envelopes such as `{ status, payload, text }` / `{ ok: false, error }`; never stream raw command output containing headers or secrets.
- Preserve project helper convenience without hiding scope: `athabasca_project_request` should make `/api/projects/:slug/...` easy while still allowing the caller to pass an explicit slug.

## Verification checklist

Before calling the migration done, capture real output for:

- `python3 -m py_compile` over the plugin package files
- a guard smoke test showing raw Athabasca `curl`/HTTPie-style terminal calls are blocked
- a non-Athabasca terminal call or URL shape that remains allowed, to prove the hook is not globally blocking network tools
- if the active runtime profile was updated, a live plugin-tool request such as `GET /api/projects`

## Security notes

- AGENTS.md is guidance, not enforcement; keep secrets and auth mechanics in code/env.
- Do not print token values during tests; only report whether env vars are present.
- If there are multiple Hermes profiles/collaborators, each profile should have its own env/token scope and load the same plugin code.
