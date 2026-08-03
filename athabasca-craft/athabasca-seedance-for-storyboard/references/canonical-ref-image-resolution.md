# Canonical Reference Image Resolution Pattern

When building Seedance prompt documents, each `@imageN` tag should resolve to a **green-tagged** (`colorTag: "green"`) asset in Athabasca media. Non-green assets are drafts, superseded variants, or unapproved experiments.

## Resolution Steps

1. Query project media: `GET /api/projects/:slug/media`
2. Filter for `colorTag === "green"`
3. Narrow candidates by title keywords, tags, and intended role
4. If multiple green assets match, prefer:
   - highest explicit version number in the title
   - latest `createdAt`
   - the asset whose `provenanceNote` best matches the current prompt intent

## Resolution Rules by Reference Role

Use different matching language depending on what the reference controls:

- **Character anchor**: character sheet, turnaround, identity lock, wardrobe lock
- **Environment anchor**: room, location, set, exterior, lighting baseline
- **Prop anchor**: hero prop, insert prop, costume detail, graphic surface
- **Composition anchor**: storyboard panel, framing, staging, blocking

This keeps `@imageN` references semantically distinct instead of treating every image as a generic inspiration board.

## Inline Reference Card HTML

Each group's reference section should include thumbnail cards so the user can visually audit references before dispatch:

```html
<h4 class="ref-section-header">Reference Images</h4>
<div class="ref-cards-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:1rem;margin-bottom:1.5rem;">
  <div class="ref-card">
    <img src="{publicUrl}" alt="@imageN" style="width:100%;aspect-ratio:1;object-fit:cover;border-radius:6px;margin-bottom:0.5rem;">
    <div class="ref-card-tag">@imageN</div>
    <div class="ref-card-title">{title}</div>
    <div class="ref-card-desc">{brief description}</div>
    <div class="ref-card-prompt">{generation prompt}</div>
    <div class="ref-card-asset">{asset_id}</div>
  </div>
  <!-- repeat for each ref in group -->
</div>
```

## Generic Reference Manifest Template

Keep the manifest concise and role-driven:

| Tag | Asset ID | Title | Role | Why it was chosen |
|-----|----------|-------|------|-------------------|
| `@image1` | `asset_...` | Character Sheet v3 | character anchor | latest approved identity lock |
| `@image2` | `asset_...` | Writing Room v2 | environment anchor | current approved room look |
| `@image3` | `asset_...` | Typewriter Insert | prop anchor | hero prop detail |

Do not preserve giant per-project asset ledgers in this reference file. If a production needs a full manifest, store that in project docs or generate it at runtime.

## Practical Checks

Before finalizing a prompt doc:

1. Every `@imageN` resolves to an existing media asset
2. Every resolved asset is green-tagged unless the user explicitly wants a draft
3. The same concept is not assigned two conflicting approved anchors
4. The HTML cards and the text manifest point at the same asset IDs
5. The chosen anchors reflect the current canonical state, not an older session's assumptions

## Pitfall

The common failure is mixing reusable selection rules with a one-project asset spreadsheet. Keep the *rules* here. Keep large project manifests elsewhere.