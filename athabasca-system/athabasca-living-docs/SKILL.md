---
name: athabasca-living-docs
description: Design, plan, implement, or operate Athabasca Living Docs — editable HTML-first production artifacts with embedded manifests, DB-backed versions, media-aware editing, and structured agent patching.
version: 0.1.0
---

# Athabasca Living Docs

Use this skill when JP asks to ideate, plan, implement, debug, or operate **Living Docs**: Athabasca's hybrid workflow for prompt previews and other production documents that should remain portable static HTML while gaining inline editing, media search, versioning, and agent-assisted patching.

## Product definition

**Living Docs** are portable HTML production artifacts with an editable block interface.

Working tagline:

> Portable HTML production artifacts with inline editing, media intelligence, version history, and agent-assisted patching.

Keep **Athabasca Workbench** as a broader caption/name for the editing workspace, but the feature name is **Living Docs**.

## Core architecture

Default to the agreed hybrid model:

1. **HTML remains the shareable artifact** — the page should be viewable from R2/public media like existing prompt-preview HTML.
2. **HTML contains stable block metadata** — generated documents should include `data-ath-*` attributes such as `data-ath-block`, `data-block-id`, `data-ath-field`, and `data-ath-asset-id`.
3. **HTML embeds a manifest** — include a safe inert JSON manifest describing document type, version, blocks, editable fields, and asset refs.
4. **DB stores identity/versioning, not every creative field** — use DB for document records, version chain, current asset pointer, patch ops, provenance, and search/indexing. Do not recreate the old rigid DB-backed prompt-preview schema.
5. **Agent edits should be structured operations** — prefer block/DOM patch ops over full-document rewrites; keep full HTML rewrite as fallback only.
6. **Publish preserves the source template** — when a Living Doc was imported from existing public HTML, save/publish should update recognized editable blocks inside the original sanitized HTML shell instead of regenerating a minimal page from the manifest. The manifest is an editable projection, not the whole artifact.

Mantra: **HTML is the artifact; blocks are the interface.**

## V1 scope

For v1, scope Living Docs to **Prompt Preview docs only**. Use existing GLY-style Seedance prompt previews as the reference shape. Do not broaden immediately to shot breakdowns, asset inventories, or arbitrary HTML unless JP explicitly expands scope.

## UI home

Use both surfaces:

- **Media** remains the artifact/asset registry and source of truth for uploaded HTML/media assets.
- **Living Docs** is the focused project editing workspace for supported artifacts.

Likely route shape:

```text
/projects/:slug/living-docs
/projects/:slug/living-docs/:docId
/projects/:slug/living-docs/:docId/edit
```

## Editing model

Prefer hybrid editing:

- Inline editing for marked prompt/text fields.
- Right-side inspector for references, settings, metadata, roles, and save/version actions.
- Only marked regions are editable. Avoid unrestricted `contenteditable` over arbitrary HTML.

### Prompt-preview editor layout lessons

When the main wide-column edit surface owns title/prompt editing, do **not** duplicate title/prompt controls in the right sidebar. The sidebar should act as navigation/inspector/action context, not a second competing edit surface.

For dirty/save state, group status with the controls it affects: place labels such as `Unsaved changes` / `Draft current` next to the save/publish buttons instead of floating under the page title.

For scanability in the two-column editor, label both structural levels:

- top of the right column: a clear heading such as `Groups`
- top of the wide column: a clear heading such as `Prompt Groups`
- before each wide-column group/section: a visible section label before the editable block/card

## Media-aware editing

The highest-value v1 feature is a DB-backed media picker/typeahead:

- exact asset ID paste
- fuzzy title/tag search
- project-local recent assets
- filters for kind, color tag, rating/stars, category/sourceKind
- insert as reference, candidate, or generation result

When rendering Living Doc asset thumbnails, preserve the visual language from the Media tab: if a referenced media asset has a `colorTag`, render that assigned color as the thumbnail border in both inline reference/candidate rows and replacement/add-asset picker results. Do not treat color only as a filter control; it is review state and should remain visible on thumbnails.

Living Doc reference/candidate thumbnails should also mirror Media-tab interaction: clicking the thumbnail/image card opens the underlying media URL in a new browser tab/window for full inspection. Nested controls such as remove (`x`) and edit/replace buttons must stop propagation so they keep their own behavior and do not also open the asset.

For imported HTML/source artifacts, expose basic provenance in the inspector/right column when fields are available: original `createdAt`, `updatedAt`/modified time, and the public/source R2 link from asset metadata or `publicUrl`. Keep this as metadata/context, not competing editable controls.

Asset refs should carry semantics, not just images. Prefer controlled core role + freeform label, for example:

```json
{
  "role": "anchor-frame",
  "label": "Shot 5 voice-from-nowhere beat"
}
```

Useful core roles include: `canonical-character`, `anchor-frame`, `continuity-reference`, `style-reference`, `candidate`, `selected-candidate`, `rejected-candidate`, `generation-result`, `source-still`, `first-frame`, `last-frame`.

## Versioning model

Store small Living Docs records rather than modeling every doc field. Typical tables/records:

- `living_documents`: project, title, artifact type, current version/asset, status, metadata.
- `living_document_versions`: document, version number, HTML media asset, parent version, actor/provenance fields, change summary, manifest, patch JSON.
- optional `living_document_patches`: if patch history needs querying separate from versions.

Every save should preserve rollback/provenance. Draft-vs-publish is a product decision; if unclear, start with a simple version chain and current pointer.

If documents store `currentDraftVersionId` / `currentPublishedVersionId` while versions also point back to the document, make the pointer lifecycle explicit: insert document first, insert version rows second, then update current pointers in a transaction where possible. Decide whether those pointer columns are nullable FKs or soft references to avoid circular migration friction.

For attribution, align with Athabasca's current auth/audit model instead of collapsing everything into `createdByType: user|agent|system`. Prefer fields or audit events that preserve `actorUserId`, `actorPrincipalId`, and `actorTokenId`; Hermes/shared-principal edits should remain distinguishable from human browser edits.

## Agent patch operations

When an agent edits a Living Doc, prefer safe structured operations such as:

```json
[
  {
    "op": "replaceAssetRef",
    "blockId": "group-a",
    "oldAssetId": "asset_old",
    "newAssetId": "asset_new"
  },
  {
    "op": "setText",
    "blockId": "group-a",
    "field": "prompt",
    "value": "..."
  }
]
```

Server-side validation should ensure selectors/ops only touch editable regions, referenced assets belong to the project or allowed scope, and serialized HTML is sanitized before upload.

## Safety and implementation contracts

When reviewing or writing a Living Docs plan, make these contracts explicit before implementation:

- **Editor rendering:** imported/public HTML should be rendered in a sandboxed iframe or through strict sanitization/isolation. Do not drop arbitrary imported HTML into the React app DOM and then add inline editing on top.
- **Public manifest projection:** the manifest embedded in public R2 HTML must be a redacted public projection. Private draft comments, unresolved review notes, internal actor IDs, token IDs, and editor-only state stay in DB snapshots.
- **Import guardrails:** prefer import by existing Athabasca asset ID. If arbitrary URL import is supported, add SSRF protections, content-type/size limits, redirect limits, timeout, and an allowlist/same-R2 rule for v1 unless broader import is intentional.
- **Media picker scope:** project media search can use existing project media routes. Global fuzzy search/color-star/tag filtering likely requires a new authorized API route; otherwise limit MVP global insertion to exact asset ID paste.
- **Media upload semantics:** current media enums may not include a dedicated Living Docs category/source kind. Either deliberately use existing values such as `generated`/`generated`, or include enum/schema/test work to add a clearer value.
- **SQLite migration:** for schema work, follow Athabasca's SQLite/Drizzle safety posture: backup first, prefer safe runtime migration patterns for existing tables, and verify with `db:guard`, focused API tests, and typecheck.

See `references/implementation-plan-review-checklist.md` for the full plan-review checklist.

## Planning workflow

When requirements are not locked, use `ask-user-question` and interview JP one decision at a time. If JP asks to keep going, immediately queue the next `clarify` question after each answer instead of stopping at a summary.

Key decision order:

1. v1 document scope
2. canonical architecture
3. UI home
4. editing model
5. versioning semantics
6. media picker scope
7. asset reference roles
8. agent approval/autopatch policy
9. migration of existing prompt previews
10. DB schema vs media metadata footprint
11. spike-first vs production MVP

## Implementation posture

Prefer a spike before a full build if editor mechanics are uncertain:

1. Use an existing prompt-preview HTML artifact as fixture.
2. Parse block annotations/manifest.
3. Edit one prompt field.
4. Replace one reference image by asset ID.
5. Serialize safe HTML.
6. Upload as a new Athabasca media asset/version.
7. Use findings to write the production implementation plan.

When implementation starts from a plan, begin with the smallest reusable server-side core before DB/UI/API integration:

- isolated manifest/parser/serializer module under the server code
- focused tests for prompt groups, settings, references/candidates, text patching, asset replacement, public-manifest serialization, and script/event-handler stripping
- typecheck after the focused tests, because `noUncheckedIndexedAccess` will catch regex-capture assumptions early
- if the real R2/public fixture cannot be fetched in the current environment, use a representative local fixture for the parser tests and keep real fixture verification as an explicit follow-up, not as a fabricated pass
- when local generated prompt-preview HTML already exists under `artifacts/` or another work area, use it for a sanity parse, then add a reduced real-DOM regression fixture so tests do not depend on untracked files
- for publish/save serialization, preserve the imported source/template HTML whenever possible; replace only recognized editable sections/blocks and embed the public manifest. Do not let manifest-only serialization drop header/style/static context. See `references/publish-template-preservation.md`.
- do not add a new HTML parser dependency by reflex; first check package conventions. For controlled Athabasca prompt-preview HTML, a narrow deterministic parser can be acceptable for the spike if isolated and covered by tests.

See `references/parser-spike-notes.md` for the parser-spike pattern, including the production-style Prompt Preview DOM (`section.group-card`, `article.ref-card`, `code asset_...`, and `Seedance Prompt` `<pre>` extraction).

For Phase 0 completion, go beyond parser unit tests: run a real-artifact round trip with structured patching, public serialization, embedded-manifest extraction, re-parse, and security marker checks. See `references/round-trip-proof-pattern.md` for the reusable proof-script/test pattern.

When resuming an in-progress Living Docs build from a standing goal, verify before editing: read the plan/handoff, inspect the worktree, run focused parser/API tests and typecheck, then close the smallest remaining MVP gap. A manual asset-ID editor is not enough for the media-picker requirement; keep exact ID paste but add project-scoped searchable/filterable media insertion where possible. See `references/mvp-continuation-verification.md` for the continuation checklist and completion standard.

Do not implement a generic Notion clone. Build the narrow production-artifact editor Athabasca needs.