---
name: athabasca-asset-inventory
description: Generate a Lightroom Classic-inspired HTML asset inventory from a shot breakdown. Outputs a sortable table organized by asset category with shot IDs, descriptions, sequence tags, and thumbnail placeholders. Saved locally and attached to the Athabasca project.
category: athabasca-ops
trigger: "create asset inventory based on shot breakdown"
version: 1.0.0
---

# Asset Inventory — Athabasca

Generate a visual HTML asset inventory from any shot breakdown (storyboard, script, or user-supplied text).

## Trigger

> "create an asset inventory based on shot breakdown [project-slug]"
> "generate asset inventory for [project-slug]"

Also use this umbrella for lightweight visual contact sheets / style boards from existing Athabasca media filters, such as "all generated images rated 2★+ with no color tags." For that variant, use `references/rated-media-style-board.md` rather than the shot-breakdown table workflow.

## Inputs

- **Project slug** (required): e.g. `good-boy`
- **Shot breakdown text** (required): raw text, markdown, or file path provided by the user

## Output

- HTML file saved to `~/.hermes/document_cache/<project>_asset_inventory.html`
- Media attached to Athabasca project via `POST /api/projects/:slug/media` (category: `generated`, tagged `storyboard`)

---

## Steps

### 0. Check reference prerequisites first

Before building the visual inventory, inspect the project's media for reference prerequisites that downstream generation will depend on.

At minimum, check for:
- canonical character sheets for recurring main characters / creatures
- canonical prop references for recurring hero props
- canonical location references for continuity-critical environments

If a likely main recurring character or creature has no character sheet, record that explicitly in the inventory output as a **missing prerequisite** rather than silently assuming the sheet exists.

### 1. Find the shot breakdown document

There are three valid input modes:

**A. Inline text**
If the user provides the shot breakdown text directly in the prompt → use it as-is.

**B. File attachment / local path**
If the user references a local file path or provides an attachment, read it.

**C. Existing Athabasca media asset**
If the user gives a specific Athabasca media asset ID such as `asset_...`, use the Athabasca media API to fetch that exact document first, then read its `publicUrl` or local cached source.

For ID-driven lookup, prefer:
- `GET /api/media/:assetId`

If the user also names a project slug, verify the returned `projectId` / project context matches that project before building the inventory.

Only do broader project-media discovery when the user has **not** supplied the exact asset ID.

**Do NOT invent fallback chains**. Use the actual media lookup route or the user-supplied file/text.

```bash
curl -s "http://localhost:3000/api/projects/{slug}/media?sortBy=createdAt&sortOrder=desc" | jq '.assets[] | {title, contentType, publicUrl, createdAt}'
```

Filter client-side for `contentType === "text/html"` and `title` containing relevant keywords:
- "shot" + "breakdown" / "list" / "canonical" → most recent matching asset
- "v2 script" → title with "v2" and ("script" or "shot")
- "our shot list" → title with "shot" and ("list" or "breakdown")

If multiple candidates, prefer the one with the most keywords matched; tie-break by `createdAt` desc.

Download the selected HTML:
```bash
curl -s "<publicUrl>" -o /tmp/shot_breakdown.html
```

**Do NOT invent fallback chains** like `Tries /api/projects/{slug}/storyboard/shots → falls back to /shot-list`. Only use API routes the user has explicitly asked you to hit.

### 2. Parse shots from the document

Support both of the shot-breakdown shapes that currently appear in Athabasca:

- flat markdown shot lists with headers like `## Shot 001 — White Light Resolves into the Hollow`
- sequence-grouped markdown with `## SEQ <name>` blocks and shot headers like `### Shot 001—Title`

Extract shot records from the text/HTML:
- **Shot ID**: numeric IDs like `001`, `002`, etc., or prefixed IDs like `S001` when present
- **Title**: the text after the shot header dash / em dash
- **Subject**: text under `Subject:` or `**Subject:**` (may wrap)
- **Action**: text under `Action:` or `**Action:**` (may wrap)
- **Description**: when the document is prose-style rather than fielded, use the paragraphs below the heading
- **Sequence / scene**: nearest `SEQ` group when present; otherwise use the scene label if the document is a flat scene shot list

Normalization rules:
- Treat `Shot 001`, `S001`, and `001` as the same logical shot only if the source document clearly uses them interchangeably.
- Preserve the original displayed shot ID in the final HTML.
- Keep accumulating wrapped `Subject` / `Action` text until the next labeled field or the next shot header.
- Plain-label scene shot lists (`Subject:` / `Action:` without markdown bolding) are first-class inputs, not edge cases.
- If there is no `SEQ` grouping, do not invent one from thin air; use a simple scene label (for example `Act 2 Scene 2`) or leave sequence blank.
- If an R2-backed document `publicUrl` is readable with `curl -L` but Python `urllib` returns `403`, fetch it with `curl -L` into `~/.hermes/document_cache/` and continue. Treat this as a retrieval quirk, not as a missing asset.

- Support both plain labels (`Subject:`) and bold markdown labels (`**Subject:**`).
- Keep accumulating wrapped `Subject` / `Action` text until the next labeled field or the next shot header.
- If an R2-backed document `publicUrl` is readable with `curl -L` but Python `urllib` returns `403`, fetch it with `curl -L` into `~/.hermes/document_cache/` and continue. Treat this as a retrieval quirk, not as a missing asset.

### 3. Categorize each shot

Classify by `shotType` or by keyword analysis of description:

| Category | CSS class | Badge color | Indicators |
|---|---|---|---|
| CHARACTER | `cat-character` | green | human names, dialogue, reaction |
| CHARACTER (DOG) | `cat-char_dog` | amber | dog name, "wheaten", "terrier", "tail" |
| ENVIRONMENT / SET | `cat-env` | purple | "INT.", "EXT.", location, set description |
| PROP | `cat-prop` | orange | object name, "collar", "box", "bell" |
| INSERT / UI | `cat-insert` | yellow | close-up, UI, screen, text |
| B-ROLL / CUTAWAY | `cat-broll` | red | cutaway, cut to, B-roll, stock-feel |
| VOID / BLACK | `cat-void` | gray | "black", "pure dark", "nothing" |

Use *token-aware* matching for UI / insert indicators. Do **not** classify `INSERT / UI` via naive substring checks like `"UI" in text`, because that produces false positives on ordinary words. Match whole words or explicit interface terms instead (for example with word-boundary regexes such as `\bUI\b`, `\bSCREEN\b`, `\bINTERFACE\b`).

Ground-level feet inserts, shield/sword emphasis, and other tactile body-mechanics close-ups should usually classify as `PROP` / `PROPS`, not `INSERT / UI`, unless an actual screen/interface is present.

When a shot is really a character performance beat that merely mentions props (for example a character holding a prop while thinking / walking), keep it under CHARACTER unless the shot is clearly an insert or prop-isolated composition.

### 4. Count per category

Build summary row:
```html
<span><strong>N</strong> character shots</span>
<span><strong>N</strong> establishing / env shots</span>
<span><strong>N</strong> environments / sets</span>
<span><strong>N</strong> props</span>
<span><strong>N</strong> inserts / UI elements</span>
<span><strong>N</strong> cutaways / B-roll</span>
<span><strong>N</strong> pure void / black</span>
```

### 5. Generate HTML

Use this exact CSS — it's the Athabasca media UI standard:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{PROJECT} — Asset Inventory</title>
<link rel="stylesheet" href="https://media.example.com/shared/styles/athabasca-seedance-prompts-v1.css">
<style>
  body { padding: 1.5rem 2rem 4rem; }
  .inv-header { margin-bottom: 0.25rem; }
  .inv-meta { color: var(--text-dim); font-size: 0.85rem; margin-bottom: 1.5rem; display: flex; flex-wrap: wrap; gap: 0.5rem 1.5rem; }
  .inv-meta span { display: inline-block; }
  .inv-summary { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1rem 1.25rem; margin-bottom: 2rem; display: flex; flex-wrap: wrap; gap: 0.5rem 1.5rem; }
  .inv-summary span { font-size: 0.85rem; color: var(--text-dim); }
  .inv-summary strong { color: var(--text); }
  .cat-section { margin-bottom: 2.5rem; }
  .cat-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }
  .cat-label { color: var(--accent2); font-size: 0.9rem; font-weight: bold; letter-spacing: 0.05em; text-transform: uppercase; }
  .cat-count { font-size: 0.75rem; color: var(--text-dim); background: var(--surface2); padding: 2px 8px; border-radius: 4px; }
  table.inv-table { width: 100%; border-collapse: collapse; margin-bottom: 0.5rem; font-size: 0.8rem; }
  thead tr { background: var(--surface2); }
  th { color: var(--accent); text-align: left; padding: 8px 12px; border-bottom: 2px solid var(--border); font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; }
  td { padding: 10px 12px; border-bottom: 1px solid var(--border); vertical-align: top; }
  tr:hover td { background: #1c212830; }
  td.id { color: var(--accent); font-weight: bold; white-space: nowrap; width: 40px; }
  td.item { font-weight: 600; color: var(--text); max-width: 260px; }
  td.desc { color: var(--text-dim); font-size: 0.78rem; line-height: 1.5; }
  td.seq { color: var(--text-dim); font-size: 0.75rem; white-space: nowrap; }
  td img { width: 80px; height: 60px; object-fit: cover; border-radius: 4px; display: block; }
  td.imgcell { width: 96px; }
  .placeholder-img { width: 80px; height: 60px; background: var(--surface2); border: 1px dashed var(--border); border-radius: 4px; display: flex; align-items: center; justify-content: center; color: var(--text-dim); font-size: 0.65rem; text-align: center; line-height: 1.3; }
  .badge { display: inline-block; padding: 1px 6px; border-radius: 3px; font-size: 0.7rem; margin-right: 4px; }
  .badge-seq { background: #58a6ff20; color: var(--accent); border: 1px solid var(--accent); }
  .badge-character { background: #3fb95020; color: var(--green); border: 1px solid var(--green); }
  .badge-dog { background: #f7816620; color: var(--accent2); border: 1px solid var(--accent2); }
  .badge-env { background: #bc8cff20; color: var(--purple); border: 1px solid var(--purple); }
  .badge-insert { background: #d2992220; color: var(--yellow); border: 1px solid var(--yellow); }
  .badge-void { background: #8b949e20; color: var(--text-dim); border: 1px solid var(--text-dim); }
  .badge-broll { background: #f8514920; color: var(--red); border: 1px solid var(--red); }
  .cat-character .cat-label { color: var(--green); }
  .cat-char_dog .cat-label { color: var(--accent2); }
  .cat-insert .cat-label { color: var(--yellow); }
  .cat-void .cat-label { color: var(--text-dim); }
  .cat-broll .cat-label { color: var(--red); }
  .cat-env .cat-label { color: var(--purple); }
  .cat-prop .cat-label { color: var(--orange); }
</style>
</head>
<body>
```

### 6. Build per-category table rows

Each `<tr>`:
```html
<tr>
  <td class="id">S003</td>
  <td class="item">SARAH CONNOR (V.O.) / REACTION FRAME</td>
  <td class="desc">Description text here...</td>
  <td class="seq"><span class="badge badge-seq">SEQ 1 — THE WARNING</span></td>
  <td class="imgcell"><div class="placeholder-img">placeholder<br>— TBD —</div></td>
</tr>
```

- **Item name**: scene heading in uppercase, or a short label derived from description
- **Description**: strip markdown, preserve line breaks as `<br>`, truncate at 300 chars
- **Sequence badge**: extract from description or heading; format `SEQ N — NAME`
- **Image cell**: placeholder div (images added later as media attachments)

### 7. Save and attach

```bash
# Save locally
SAVE_PATH=~/.hermes/document_cache/<project>_asset_inventory.html
# Save the HTML to that path

# Attach to Athabasca via Bun upload:
cd <athabasca-repository>
bun -e "
const fd = new FormData();
fd.append('phase', 'storyboard');
fd.append('category', 'generated');
fd.append('sourceKind', 'generated');
fd.append('title', '<Project> Asset Inventory');
fd.append('provenanceNote', 'Generated from shot breakdown. Athabasca asset inventory skill.');
fd.append('metadataJson', JSON.stringify({source: 'shot-breakdown', shotCount: N}));
fd.append('file', new Blob([require('fs').readFileSync('<SAVE_PATH>')], {type: 'text/html'}), 'asset_inventory.html');
const r = await fetch('http://localhost:3000/api/projects/<slug>/media', {method: 'POST', body: fd});
const j = await r.json();
console.log(j.ok ? 'Attached: ' + j.asset.publicUrl : 'Error: ' + JSON.stringify(j));
"
```

---

## Columns

| Column | Content |
|---|---|
| **ID** | Shot number (S001, S002…) |
| **Item** | Scene heading / short label, uppercase |
| **Description** | Stripped markdown, max 300 chars |
| **Sequence** | `SEQ N — NAME` badge |
| **Image** | Placeholder `— TBD —` (filled in when media is attached) |

## Pitfalls

- **UI classifier false positives:** Do **not** classify `INSERT / UI ELEMENT` with naive substring checks like `"UI" in desc` — that will misfire on ordinary words such as `guidance`, `build`, or other text fragments. Use whole-word / token matching (regex word boundaries) for `UI`, `screen`, `interface`, `monitor`, etc. This misfire showed up in a live production inventory, where several normal character/prop shots were mis-bucketed until the classifier was tightened.

- **No shots found**: tell the user clearly that no shot data was found and ask them to provide the breakdown text.
- **Missing sequence tags**: look for `INT.`/`EXT.` location headers or infer from scene grouping.
- **Long descriptions**: truncate at 300 chars with `…`, preserve complete text in `title` attribute for hover.
- **Category with 0 shots**: skip the section entirely (don't show empty tables).
- **Discord CDN downloads fail with 403**: Midjourney images use public CDN but Discord webhook attachments require Bun runtime — use `bun -e "..."` for downloads, not Python urllib.

## Verification

1. Open the saved HTML — verify all categories present with correct counts
2. Verify the summary row totals match sum of category counts
3. Confirm `POST /api/projects/:slug/media` returns `{ok: true, asset: {id, publicUrl}}`
