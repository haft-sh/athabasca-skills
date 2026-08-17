# Living Docs Implementation Plan Review Checklist

Use this when reviewing or revising a Living Docs implementation plan before code work begins. These checks came from reviewing the initial `docs/plans/living-docs.md` MVP plan.

## Contracts that must be explicit

1. **Safe editor preview**
   - Imported/public HTML must not be rendered directly into the React app without containment.
   - Prefer a sandboxed iframe with scripts disabled, or a strict sanitizer plus CSS isolation.
   - Editor controls should live outside the imported document DOM.
   - Inline editing must target marked regions only; avoid unrestricted `contenteditable` across arbitrary HTML.

2. **Publish-manifest redaction**
   - Public HTML can embed an inert manifest, but it must be a public projection.
   - Strip private draft comments, unresolved review notes, internal actor IDs, token IDs, non-public provenance, and any editor-only state.
   - Keep private/full manifest snapshots in DB versions.

3. **Import guardrails**
   - Prefer import by existing Athabasca asset ID because project access can be checked.
   - If arbitrary URL import is allowed, require SSRF protections: allowlist or same-R2 constraint for v1, content-type and size limits, redirect limit, timeout, and no private-network fetches.

4. **Attribution/provenance**
   - Do not collapse actors into a single `createdByType: user|agent|system` plus `createdById` if the current auth model has users, access principals, and API tokens.
   - Prefer fields aligned with current audit semantics: `actorUserId`, `actorPrincipalId`, `actorTokenId`, plus a compact actor kind/display label when needed.
   - Reuse or extend `audit_events` for publish/import/patch actions instead of inventing a parallel audit trail unless there is a deliberate reason.

5. **SQLite/Drizzle migration path**
   - Spell out runtime migration/backfill steps for new Living Docs tables and indexes.
   - Back up before schema changes on a live/local DB.
   - New tables are usually safe; later additions of NOT NULL columns to existing tables need the repo’s safer `client.ts` migration pattern.
   - Verification should include `bun run db:guard`, focused API tests, typecheck, and at least one live route probe when the server is running.

6. **Version pointer lifecycle**
   - If `living_documents` stores `currentDraftVersionId` / `currentPublishedVersionId` while versions point back to the document, define nullable pointer lifecycle and transaction boundaries.
   - Insert the document first, insert version rows second, then update current pointers in the same transaction where possible.
   - Decide whether pointer FKs are enforced or intentionally soft references to avoid circular migration friction.

7. **Media enum / upload semantics**
   - Existing media enums may not have a first-class `living_doc` category/source kind.
   - Either deliberately use the current values (for example `category: generated`, `sourceKind: generated`) or include enum/schema/test work to add a clearer value.

8. **Media picker API scope**
   - Project-scoped recent/search can usually use existing project media routes.
   - Global fuzzy search, tag search, color/star filters, and recent global media likely need a new authorized route and explicit cross-project access semantics.
   - For MVP, consider exact asset ID paste as the only global insertion path unless the global route is in scope.

## Good review output shape

- Lead with whether the architecture is directionally sound.
- List high/medium findings with file/line references when reviewing a concrete plan.
- Convert vague TODOs into implementation contracts.
- Push back on security/auth/migration ambiguity before implementation starts.
