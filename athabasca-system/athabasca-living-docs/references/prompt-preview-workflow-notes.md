# Living Docs Session Notes — Prompt Preview Workflow

Source conversation: JP discussed replacing rigid DB-backed prompt-preview/shot-breakdown/asset-inventory workflows with HTML-first artifacts, then identified the editing costs of opaque static HTML.

## Problem statement

HTML-first prompt previews are faster and more flexible than the old formal DB-backed schema because JP can describe the needed document shape and the agent can generate the exact artifact without schema migrations, joins, relationships, or foreign-key friction.

The cost is that static HTML artifacts become opaque blobs after publishing:

- edits require chat-only instructions one at a time
- user manually looks up media IDs and pastes them into chat
- agent downloads/reuploads HTML and keeps a local copy synced
- no good version history
- changes do not feel inline
- asset insertion lacks fuzzy DB-backed search/typeahead

## Desired product shape

Feature name: **Living Docs**.

Broader workspace/caption: **Athabasca Workbench**.

Living Docs should feel like a lightweight, Athabasca-native production document editor: Notion-like block editing where useful, but not Notion and not a generic CMS.

Core requirements:

- static/shareable HTML output
- inline editing for marked prompt/text fields
- DB-backed media search/typeahead for assets
- insert/delete/reorder reference images and candidates
- custom fields/blocks for prompt-preview workflows
- version history/rollback/provenance
- inline AI/agent edits via structured patch operations
- no third-party Notion dependency
- no return to rigid fully normalized DB schema for every creative field

## Agreed early decisions

- v1 scope: **Prompt Preview only**.
- architecture: **Hybrid** — HTML artifact + embedded manifest + DB versions.
- UI home: **Both** — Media remains artifact registry; Living Docs is focused editing workspace.

## Recommended implementation principles

- HTML is the artifact; blocks are the interface.
- Keep DB use small and appropriate: identity, versions, latest pointer, patch ops, provenance, asset refs/search indexes.
- Avoid unrestricted `contenteditable` over arbitrary HTML; only marked fields/blocks should be editable.
- Prefer structured agent operations (`replaceAssetRef`, `setText`, `insertBlock`, `removeBlock`) over brittle full-document rewrites.
- Use an existing GLY A2S2 prompt preview as the first fixture/migration candidate.

## Candidate block vocabulary for prompt previews

- `living-doc`
- `section`
- `prompt-group`
- `prompt-field`
- `settings-block`
- `reference-gallery`
- `reference-image`
- `candidate-gallery`
- `candidate-image`
- `generation-result`
- `notes`
- `comment`

## Useful asset roles

Controlled role plus freeform label is preferable to unstructured labels only.

Candidate roles:

- `canonical-character`
- `anchor-frame`
- `continuity-reference`
- `style-reference`
- `candidate`
- `selected-candidate`
- `rejected-candidate`
- `generation-result`
- `source-still`
- `first-frame`
- `last-frame`

## Interview flow

When planning Living Docs with JP, use the ask-user-question workflow and ask one decision at a time. If JP says to keep going, queue the next question immediately after each answer instead of stopping with only a summary.