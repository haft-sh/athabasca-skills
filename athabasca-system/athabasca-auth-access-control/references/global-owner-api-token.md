# Global owner API token pattern

Session learning: the user wanted a “god token” / superadmin token for Athabasca that grants complete access to every current and future project without project-by-project scopes.

## Chosen representation

Use an owner-mode API token with an empty project scope list:

```json
{
  "projectScopes": [],
  "operationModes": ["owner", "system_operator", "creator"]
}
```

The key is that empty scopes are only global for the superadmin owner-token shape. Empty scopes must not become global for ordinary creator/viewer/collaborator tokens.

## Implementation points

Files that carried the change:

- `src/server/api/routes/auth.ts`
  - allow `projectScopes: []` in token creation validation
  - add guardrails for the zero-scope global-token case
- `src/server/auth/index.ts`
  - `getProjectRole(...)`: owner-mode zero-scope token returns `owner` for any project
  - `listAccessibleProjectIds(...)`: owner-mode zero-scope token returns `null` to mean unrestricted/all projects
- `tests/api-contract.test.ts`
  - add a contract test proving global owner token access across multiple projects

## Guardrails to preserve

Zero-scope global token creation should be allowed only when:

1. requester has owner operation mode
2. target user is the requester themself
3. requested token operation modes include `owner`

This keeps the feature as owner-only superadmin access unless a future user explicitly asks to broaden delegation.

## Route semantics

When a helper returns accessible project IDs:

- array of IDs/slugs = restricted scope
- empty array = no accessible projects
- `null` = unrestricted/all projects

Do not collapse `null` and `[]`; they mean opposite things.

## Test shape

Useful focused test name from the original implementation:

```bash
bun test tests/api-contract.test.ts -t "allows owner-mode API tokens with zero project scopes"
```

The test should prove the token can see/access more than one project and that the behavior comes from the global owner token, not pre-materialized per-project scopes.

## Example token creation payload

```bash
curl -sS -b /tmp/athabasca-cookies.txt \
  -X POST http://100.84.189.23:3000/api/auth/api-tokens \
  -H 'content-type: application/json' \
  -d '{
    "name": "jp-superadmin-hermes",
    "kind": "hermes_profile",
    "projectScopes": [],
    "operationModes": ["owner", "system_operator", "creator"],
    "expiresInDays": null
  }'
```

Adjust host/cookie path for the current environment.
