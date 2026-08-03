# DB-backed RBAC/shared-principal plan review checklist

Use this when reviewing or revising plans that change project RBAC, token project creation, collaboration, or shared Telegram/Hermes principals.

## Required contracts

1. **Token access mode**
   - Add or require an explicit token access mode when zero-scope tokens need more than one meaning.
   - Recommended values: `membership`, `scoped`, `global_owner`.
   - Backfill existing tokens deterministically: zero scopes + owner mode => `global_owner`; non-empty scopes => `scoped`; otherwise => `membership`.
   - Runtime should check `access_mode`, not re-infer global access from empty scopes.

2. **Discriminated auth subject**
   - Shared principal support requires `AuthContext` to distinguish human users from non-human/access-principal subjects.
   - A token should have exactly one subject: `subjectType=user` with `userId`, or `subjectType=access_principal` with `principalId`.
   - Keep human membership lookup and principal grant lookup separate to avoid personal-project leakage.

3. **Principal capability model**
   - Do not leave provider capability checks user-only if principal-authenticated generation is in scope.
   - Preferred v1: access principals have their own operation modes and provider grants.
   - Safer than inheriting a backing user, because inheritance leaks personal provider privileges and creates attribution confusion.

4. **Transactional project creation**
   - Creation must be one DB transaction covering the project row, human owner membership, shared-principal project grant when applicable, `createdViaPrincipalId`, and audit event.
   - Avoid route-level sequencing like `createProject()` then `grantProjectMembership()` for RBAC-sensitive creation.
   - Add a failure-injection or equivalent regression test proving partial creation cannot leave an inaccessible project.

5. **Collaborator invariants**
   - Owner may grant/change/remove any role except violating last-human-owner invariant.
   - Admin may grant/change/remove only roles below admin; cannot grant owner/admin, modify owners/admins, remove last owner, or self-promote/self-demote unless explicitly allowed.
   - Last human owner cannot be removed or demoted, even if shared principals exist.

6. **Audit reuse**
   - Prefer extending existing `audit_events` with `actor_principal_id` and metadata fields over adding a parallel project-specific audit table.
   - Use metadata for transport-specific facts such as Telegram chat id, Telegram sender id, current group owner id, and failure reason.

7. **Migration detail**
   - Plans should mention both `src/server/db/schema.ts` and the repository runtime migration path in `src/server/db/client.ts`.
   - Include uniqueness constraints such as `(kind, telegramChatId)` and `(principalId, projectId)` where applicable.
   - Specify indexes and FK delete behavior.

## Minimum regression tests

- zero-scope creator token can be minted and is membership-backed, not global
- global owner token still sees all projects
- token scopes intersect with DB membership and lower effective role
- creator token can create a project and immediately access it
- unrelated project access remains denied
- shared principal granted one project cannot see unrelated personal projects
- principal provider grant is required for generation
- project creation transaction rolls back all auth records on failure
- owner/admin collaborator ceilings and last-owner invariants are enforced
