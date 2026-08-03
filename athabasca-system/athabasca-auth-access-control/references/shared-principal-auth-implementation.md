# Shared-principal auth implementation notes

Captured from the session that implemented DB-backed shared principals, collaborator APIs, and atomic project creation.

## Implemented contracts

- `api_tokens.access_mode` is explicit: `membership`, `scoped`, or `global_owner`.
- Each API token has exactly one subject: either `user_id` or `principal_id`.
- Existing bearer token strings remain valid after migration because the rebuild preserves token IDs and token hashes.
- User tokens remain membership-backed unless scoped or global-owner semantics explicitly narrow/expand them.
- Principal tokens are principal-owned; they never borrow a backing user's memberships, operation modes, or provider grants.
- Principal project access is stored in `access_principal_project_grants`.
- Principal operation modes and provider capabilities are stored in principal-owned grant tables.
- Project creation is transaction-backed: project row, human owner membership, principal project grant when applicable, attribution fields, and audit event are created together.
- Collaborator endpoints enforce grant ceilings and last-human-owner protection.

## Legacy-token migration behavior

Do **not** tell operators to regenerate existing auth tokens by default.

The safe migration expectation is:

1. Rebuild/backfill token records while preserving existing token IDs and token hashes.
2. Infer access mode from existing state.
3. Preserve scope and operation-mode tables.
4. Existing bearer strings continue authenticating.

Compatibility caveat:

- Non-global scoped/membership tokens now depend on corresponding DB membership.
- If an old scoped token has scopes but the owning user lacks matching `project_memberships`, grant the missing membership to the same user rather than regenerating the token.

## Principal-created project request contract

When a shared-principal token creates a project, require an explicit mapped human owner:

- request header: `x-athabasca-telegram-owner-user-id`
- optional audit actor: `x-athabasca-telegram-initiator-user-id`

Do not silently use the speaker/initiator as owner when the Telegram owner cannot be mapped to an Athabasca user. Fail clearly and ask for the owner mapping to be fixed.

## Tests that should exist

At minimum, cover:

- existing invitation/session/token project access still works
- owner/admin collaborator listing and role changes
- admin cannot escalate another user above their own grant ceiling
- last human owner cannot be removed or demoted
- principal token sees only explicitly granted projects
- principal token receives its own operation/provider capabilities, not a human user's capabilities
- user-created projects immediately grant owner membership to the creator
- principal-created projects create both human owner membership and principal project grant
- existing zero-scope owner tokens still behave as global owner tokens

## Verification notes

Use focused contract tests first, then the full test suite. If repo-wide typecheck is polluted by unrelated untracked scripts, report that separately and verify source-owned paths with a filtered diagnostic run rather than hiding the unrelated failure.