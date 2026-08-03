# Collaborator Project Creation RBAC

Session-specific guidance captured from the JT / Cliphouse collaboration rollout.

## Problem shape

Current Athabasca behavior already grants DB ownership on project creation, but normal token auth historically resolved project access only from `api_token_project_scopes`.

That breaks the use case:
1. collaborator token creates a new project
2. server writes `project_memberships` owner row
3. token still cannot access the new project because its scope list was frozen at mint time

## Recommended model

Use DB-backed membership as the primary project authority for normal users and Hermes-profile tokens.

### Keep unchanged
- zero `projectScopes` + `owner` mode token = global owner access
- only explicit owner flows may mint that shape

### Change for normal tokens
- empty `projectScopes` on a non-owner token = no additional restriction; use DB membership
- non-empty `projectScopes` = intersect with DB membership
- effective role = narrower of DB membership role and token-scoped role

### Token creation guardrail to check

Do not only update runtime access lookup. Also review `/api/auth/api-tokens`.

A common blocker is treating `projectScopes.length === 0` as “requesting global owner token.” That makes the target creator-token shape impossible to mint even if `getProjectRole(...)` and `listAccessibleProjectIds(...)` are fixed.

Safer rule:
- zero scopes + owner mode + owner/self guardrails = global owner token
- zero scopes + non-owner/creator mode = membership-backed token with no extra project restriction
- if redesigning the API, prefer an explicit access-mode field over inferring global intent from an empty array

## Route-policy implication

If collaborator-operated Hermes profiles should create projects, `POST /api/projects` should allow `creator` mode instead of only `owner` / `system_operator`.

## Shared-principal design questions to resolve before coding

When extending this model to Telegram groups/channels, decide the auth subject and capability model before adding tables/routes.

Required decisions:
- Does `api_tokens` support principal-owned tokens, or are shared-principal tokens still backed by a human `userId`?
- Does `AuthContext` become a discriminated union such as human user vs shared principal?
- Are operation modes stored directly for principals, inherited from a backing user, or intersected between both?
- Are provider grants stored for principals, inherited from a backing user, or intersected with backing-user grants?
- How is project creation made atomic: project row, owner membership, shared-principal grant, `createdViaPrincipalId`, and audit event should be one transaction.

Security pitfall:
- If shared-principal tokens are simply user-backed without an explicit intersection, a Telegram group can accidentally inherit a human collaborator's personal projects or provider capabilities.
- If capabilities remain user-only with no principal rule, the group may pass project RBAC but fail generation/capability checks unexpectedly.

## Test matrix

Add contract coverage for:
- creator-mode collaborator token can `POST /api/projects`
- creator-mode token can immediately `GET /api/projects/:slug` for the newly created project
- creator-mode token sees the new project in `GET /api/projects`
- same token still gets `403` for unrelated projects
- explicit token scope narrows multi-project membership
- explicit token role can lower effective access (e.g. DB owner + token viewer => denied on write route)
- zero-scope owner token still lists and reads every project

## Anti-patterns

Do not:
- auto-mutate token scopes after project creation
- reinterpret all zero-scope tokens as global
- solve collaborator creation by handing out global owner tokens
- leave token scope behavior undocumented; the empty-scope distinction must be explicit in code comments and tests
