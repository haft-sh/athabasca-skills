---
name: athabasca-auth-access-control
description: Use when changing, debugging, or verifying Athabasca authentication, API tokens, invitations, project memberships, operation modes, or access-control behavior. Covers owner/global token semantics, project role lookup, accessible-project listing, route validation, and contract tests.
---

# Athabasca Auth & Access Control

Use this skill when the task touches Athabasca auth, especially:

- `/api/auth/*` routes
- invitations or invite acceptance
- login/session behavior
- API token creation or validation
- project membership roles
- operation modes such as `owner`, `creator`, or `system_operator`
- `getProjectRole(...)`, `listAccessibleProjectIds(...)`, or route guards
- questions like “who can access what?” or “make this token/user global”

## Source-of-truth order

1. Runtime code and schemas:
   - `src/server/api/routes/auth.ts`
   - `src/server/auth/index.ts`
   - `src/server/api/schemas.ts`
   - `src/server/db/schema.ts`
2. OpenAPI docs if the server is live:
   - `http://localhost:3000/api/openapi/json`
3. Contract tests:
   - `tests/api-contract.test.ts`
4. UI/docs are downstream of API behavior.

## Working sequence

1. Inspect the relevant auth route and helper before editing.
2. Identify whether the request is about:
   - browser session auth
   - API token auth
   - invitation flow
   - project membership
   - operation-mode authorization
3. Make the smallest schema/validator/helper change that preserves existing scoped-token behavior.
4. Add or update API contract tests that cover:
   - happy path
   - rejection/guardrail path
   - at least one cross-project or 404/access-denied case when project scope is involved
5. Run focused tests first, then broad verification:
   - `bun test tests/api-contract.test.ts -t "<focused test name>"`
   - `bun run typecheck`
   - `bun test tests`
6. If changing live auth behavior, verify the server health and, when practical, probe the live endpoint with curl.

## Hermes-profile invitation semantics

When checking whether an Athabasca invite is enough to "wire up Hermes", verify the actual runtime behavior rather than assuming the invite also creates a usable bearer-token bridge.

Current behavior to remember:
- `inviteCreateBodySchema` accepts optional `hermesProfileName`
- invite acceptance creates/updates the Athabasca user, project membership, and operation modes
- if `hermesProfileName` was present, acceptance also inserts a row in `hermes_profiles` with `providerOwnership: "user_managed"`
- invite acceptance sets the browser session cookie (`athabasca_session`)
- invite acceptance does **not** itself mint an Athabasca API token for Hermes/Telegram use

Operational consequence:
- adding a Telegram user to a Hermes profile allowlist and/or setting `hermesProfileName` on the Athabasca invite is still **not** the same thing as issuing a usable `ATHABASCA_API_TOKEN`
- if the bridge needs bearer auth, create that token explicitly via `POST /api/auth/api-tokens`


Athabasca supports a deliberately special owner/superadmin API token pattern:

- `projectScopes: []`
- `operationModes` includes `"owner"`
- token is created by an authenticated owner for their own user

Semantics:

- zero project scopes on an owner-mode token means global owner access, not “no access”
- `getProjectRole(...)` should treat this token as `owner` for every project
- `listAccessibleProjectIds(...)` should return `null` to mean “all projects” for this token shape
- project listing routes should interpret `null` from `listAccessibleProjectIds(...)` as unrestricted project visibility
- future projects should be included automatically because no project IDs/slugs are baked into the token

Guardrails:

- do not allow non-owner users to create zero-scope global tokens
- do not allow owners to create zero-scope global tokens for another user unless the user explicitly requests that broader delegation model
- require the requested token operation modes to include `owner`
- preserve normal scoped-token behavior for all non-empty `projectScopes`

See `references/global-owner-api-token.md` for implementation details captured from the session that introduced this pattern.

## Collaborator project-creation token semantics

When the product requirement is "a collaborator or Hermes profile can create new projects and then immediately own/read/mutate them," do **not** keep `api_token_project_scopes` as the sole source of project authority.

Why:
- project creation already writes a `project_memberships` owner row for the creator
- a token minted before the new project exists cannot enumerate that future project in `projectScopes`
- treating token scopes as the primary authority forces either token mutation after every create or an overly broad global owner token

Preferred authz model:
- DB membership (`project_memberships`) is the source of truth for normal project access
- token operation modes answer whether the caller may perform creator/system actions
- token project scopes are an **optional narrowing layer**, not the primary access list
- the special zero-scope + owner-mode token remains the only true global-access token shape

When creation is initiated from a shared Telegram/group principal, prefer this ownership model:
- the **current Telegram group owner** (`creator` in Telegram admin semantics) becomes the new project's default `owner`
- the shared principal also receives an explicit project grant at creation time so the group can keep operating on the project
- the human actor who sent the command is stored separately as the initiating actor for auditability
- do **not** auto-add every current raw chat member as a human collaborator just because they are present in the group
- if you later want bulk collaborator propagation, derive it from explicit designated membership such as `access_principal_members`, not live Telegram membership

Before implementing shared principals, settle the subject model explicitly:
- whether API tokens can be principal-owned instead of user-owned
- whether `AuthContext` becomes a discriminated human/principal subject
- how operation modes and provider grants are computed for principals
- whether principal grants are independent or intersected with a backing human/user token

Do not start schema/routes for shared principals while those contracts are vague; otherwise the implementation will either leak a backing user's personal access or block legitimate generation because capabilities remain user-only.

Current implemented subject model:
- `api_tokens.access_mode` is explicit: `membership`, `scoped`, or `global_owner`
- an API token has exactly one subject: `user_id` or `principal_id`
- shared-principal tokens are principal-owned and never use a backing user
- principal project access comes from `access_principal_project_grants`
- principal operation modes and provider capabilities come from principal-owned grant tables
- the auth migration preserves existing token IDs and hashes; existing bearer secrets do not need regeneration
- if an old non-global token loses access after migration, first check for missing `project_memberships` for the token's owning user and add the membership; do not rotate the bearer secret just to repair membership state

See `references/shared-principal-auth-implementation.md` for the implemented contracts, token-regeneration answer, request headers for principal-created projects, and regression-test matrix.

Important precision:
- implement **current owner at creation time**, not a supposed permanently durable "original founder" concept
- the practical Telegram-side lookup is the current owner/`creator` from admin metadata
- if that Telegram owner cannot be mapped to an Athabasca user, fail clearly; do **not** silently fall back to making the speaker the owner

Why this default is safer:
- preserves a durable ownership anchor for long-lived shared groups
- keeps shared-group workflow intact without granting broad personal access
- preserves accountability by separating owner from initiating actor
- avoids unstable auth semantics when chat membership changes
- avoids passive or loosely related group members silently receiving project access

Recommended semantics for non-global-owner tokens:
- empty `projectScopes` means **no additional restriction**; use DB memberships for project listing and access
- non-empty `projectScopes` means intersect token scopes with DB memberships
- when both DB membership and token scope provide roles, use the narrower effective role

Token-minting precision:
- do not let `projectScopes.length === 0` alone mean “requesting a global owner token”
- a zero-scope creator/non-owner token is a valid membership-backed collaborator token, not global access
- global-owner intent must be identified by owner mode plus the existing owner/self guardrails, or preferably by an explicit token access-mode field if the API is being redesigned
- update `/api/auth/api-tokens` tests alongside `getProjectRole(...)` / `listAccessibleProjectIds(...)`; otherwise the desired zero-scope creator token cannot be minted even if runtime access lookup is fixed

Policy implication:
- if collaborators should be able to create projects, `POST /api/projects` should usually allow `creator` mode rather than requiring only `owner` or `system_operator`

Verification expectations for this class of change:
- a creator-mode collaborator token can create a project and immediately access it
- the same token is still denied on unrelated projects without membership
- explicit token scopes still narrow multi-project memberships
- zero-scope owner tokens still behave as global owner tokens

See `references/collaborator-project-creation-rbac.md` for the session-specific migration guidance and test matrix, including the token-minting guardrail and shared-principal auth/capability open questions.

## Reviewing or revising RBAC implementation plans

When asked to review or improve an Athabasca auth/access-control plan, turn findings into concrete implementation contracts rather than leaving vague TODOs such as “possibly modify auth” or “decide during implementation.” A good revised plan should explicitly define:

- token semantics: prefer an explicit token `accessMode` such as `membership`, `scoped`, or `global_owner`; do not infer global-owner intent from `projectScopes.length === 0` alone
- auth subject model: make `AuthContext` a discriminated union when shared/non-human principals exist, with exactly one subject per token (`user` or `accessPrincipal`)
- capability model: shared principals need their own operation modes and provider grants, or a deliberately specified intersection model; never let them accidentally inherit a backing user's personal grants
- atomicity: project creation plus owner membership, principal grant, attribution fields, and audit event must happen in one transaction
- collaborator invariants: define grant ceilings, self-change rules, and last-human-owner protection before coding endpoints
- audit strategy: extend/reuse `audit_events` where possible instead of introducing a parallel audit table
- migration details: include runtime `client.ts` migration/backfill steps, unique constraints, indexes, foreign-key delete behavior, and regression tests

See `references/db-backed-rbac-plan-review.md` for a compact checklist distilled from the DB-backed RBAC/shared-principal plan review.

## Fast 401 diagnosis for agents

In Athabasca, `GET /api/health` only proves liveness. It does not prove that the caller is authenticated.

When an agent sees `401` on routes like:
- `GET /api/projects`
- `GET /api/auth/me`
- project read/write endpoints

assume **missing auth first**, not a broken route.

Preferred Hermes-side bearer path:
- repo-local Hermes plugin: `.hermes/plugins/athabasca-api`
- first-class Hermes plugin tools: `athabasca_request` and `athabasca_project_request`
- env contract remains `ATHABASCA_BASE_URL`, `ATHABASCA_API_TOKEN`, optional `ATHABASCA_PROJECT_SLUG`
- keep `~/.hermes/scripts/athabasca_client.py` only as a temporary compatibility/recovery fallback during migration

Recommended sequence before touching server code:
1. verify the env vars exist in the active Hermes profile
2. retry the failing request through the Hermes Athabasca plugin tool; if the plugin is unavailable during migration, use `athabasca_client.py` as a fallback
3. only debug route implementation after bearer-auth success has been ruled out

## Hermes plugin bearer-auth pattern

When moving Athabasca agent auth out of prompts/scripts, use code-based persistent auth instead of relying on AGENTS.md instructions:

- implement a custom Hermes plugin that registers explicit Athabasca API tools such as `athabasca_request` and `athabasca_project_request`
- use `requires_env` for `ATHABASCA_BASE_URL` and `ATHABASCA_API_TOKEN`; treat `ATHABASCA_PROJECT_SLUG` as optional convenience
- have the tool inject `Authorization: Bearer <token>` internally and return structured `{ status, payload }`-style results without printing secrets
- add a `pre_tool_call` hook only as a guardrail/audit layer: block raw terminal `curl`, `wget`, HTTPie, or `xh` calls to the configured Athabasca host and tell the agent to use the plugin tool
- do **not** depend on a hook mutating arbitrary terminal/curl arguments to add auth; use the hook to block or warn, not as the primary injection mechanism
- keep AGENTS.md limited to routing guidance and operational context, not token mechanics or secret-bearing command recipes

See `references/hermes-plugin-bearer-auth.md` for the migration shape and guardrail rationale.

## Better Auth / docs-audit note

When asked whether Athabasca is following Elysia Better Auth guidance, verify the implementation shape before discussing best practices.

Fast sequence:
1. Check whether the app actually uses Better Auth at all (`package.json`, imports, `betterAuth(...)`, `auth.handler`, `auth.api.getSession(...)`, Better Auth OpenAPI plugin wiring).
2. If those are absent, say the app is using a custom auth layer rather than Better Auth — do not frame it as a partial Better Auth integration.
3. Then evaluate route protection quality separately: route-group guards, session cookie flags, bearer token support, role/mode/capability checks, and auth contract tests.
4. If the user wants docs updated, add a short README note that the current system is custom auth/authz, not Better Auth, and mention the likely migration rationale only as future-looking context.

This avoids a common review mistake: scoring the app poorly against Better Auth docs without first stating the more important fact that Better Auth is not actually in use.

## Pitfalls

- Do not interpret all zero-scope tokens as global. The global behavior is only for owner-mode superadmin tokens.
- Do not represent “all projects” by materializing every current project scope into the token; that fails for future projects.
- In runtime DDL/backfill auth migrations (`src/server/db/client.ts`), order matters: create the auth tables and indexes first, then run legacy backfills that read/write related scope or mode tables. A backfill that references token-scope or operation-mode tables before they exist can fail on fresh test databases even if it works on an already-migrated local DB.
- Do not add server-side fallback generators or unrelated behavior while touching auth routes; keep auth changes narrow and contract-tested.
- Avoid trusting stale docs or UI assumptions. Probe the live endpoint or read the actual handler.
- When comparing auth behavior against framework/library docs, first verify whether that library is actually integrated; absence of Better Auth should be stated explicitly, not buried in the conclusion.
- Response envelopes should stay `{ ok: true, ... }` / `{ ok: false, error: "..." }`.

## Verification checklist

Before finishing an auth/access-control task, report real outputs for:

- focused contract test
- `bun run typecheck`
- full `bun test tests` when the change is not purely docs-only
- any live curl probe if the task was about live behavior
