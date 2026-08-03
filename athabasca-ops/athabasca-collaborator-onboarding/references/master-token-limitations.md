# Master token limitations in current Athabasca auth

Use this note when the user asks for a super-admin bearer token that should automatically work across all current and future projects.

## Verified current constraints

Code-level constraints observed in the current implementation:

- `POST /api/auth/api-tokens` requires `projectScopes` with at least one entry.
- Token-auth project access is resolved from the token's explicit `tokenProjectRoles`.
- Token-auth project listing is resolved from the token's explicit project scope set.
- `expiresInDays` is nullable/optional, so a token can be non-expiring.

## Practical implication

The implementation supports:
- non-expiring tokens
- project-scoped tokens
- owner-owned or collaborator-owned tokens depending on `userId`

The implementation does **not** currently support:
- one master token that automatically reaches every current project
- one master token that automatically reaches future projects created later
- zero-scope token meaning "global owner access"

## Best-available workaround

If the user needs broad access today, the closest available option is:
1. list all current project slugs
2. create one non-expiring token scoped to all of them
3. accept that new projects created later will still require reissuing/replacing the token

## What would need to change

Any of these would unlock true master-token semantics:

- allow API tokens with zero `projectScopes` and treat certain owner-mode tokens as global
- add an explicit field such as `allProjects: true`
- add a token scope mode like `scopeMode: "global"`

Then update token access resolution so token auth can bypass explicit per-project scope enumeration when that global mode is present.
