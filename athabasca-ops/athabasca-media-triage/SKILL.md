---
name: athabasca-media-triage
description: "Use when reviewing, approving, or rejecting generated assets for a project by iterating through them against a reference document."
version: 1.2.0
author: Hermes Agent (Athabasca)
metadata:
  hermes:
    tags: [athabasca, media, triage, review, approve, deny, color-tag]
    related_skills: [athabasca-media-attachment-finder, athabasca-media-generation, athabasca-media-upload]
---

# Athabasca Media Triage

## When to Use

- A user says "triage the assets", "review what we generated", or "approve or deny these"
- A user wants to iterate through project media and greenlight or reject items
- A user references a prompt list or shot breakdown and wants to match generated outputs against it

Do not use this for:
- Generating new media (use `athabasca-media-generation`)
- Discovering what media exists (use `athabasca-media-attachment-finder`)
- Uploading external media (use `athabasca-media-upload`)

## Workflow

### 1) Fetch the reference document

If the user provides a reference URL (typically on `media.wheretoaccess.com`), fetch it with `web_extract`. This document defines what was requested — use it to organize the triage by asset group or shot number.

### 2) Query all project media via API

```javascript
(async () => {
  const res = await fetch('/api/projects/:slug/media');
  const data = await res.json();
  const assets = data.assets; // NOT data directly — response is {ok, assets}
  // ...
})()
```

Run this in `browser_console` after navigating to the project media page.

### 3) Filter by colorTag

Assets carry a `colorTag` field (not `color`!):

| colorTag | Meaning | Action |
|---|---|---|
| `green` | Approved / greenlit | **Skip** — already approved |
| `yellow` | Older version / superseded | **Skip** unless the user asks to review |
| `null` | Unreviewed | **Triage these** |
| `red` | Rejected | Skip unless the user asks to re-review |

Focus on `kind === 'image'` (or whatever media type the user is reviewing) with `colorTag === null`.

### 4) Organize by reference groups

Match assets to the reference document's structure. Common groupings:
- **@image references** (MJ upscaled grids, e.g. `@image2: Spartan Writing Room`)
- **Seedream/GPT single-shot images** (generated individual stills)
- **Character sheets** (turnaround/reference sheets)
- **Location/environment plates**
- **GPT edits** (post-processed corrections)

Before triaging dependent shots, check whether the project already has the required canonical references for the thing under review:
- recurring characters / creatures → character sheet
- recurring hero props → canonical prop sheet/reference
- continuity-sensitive environment → canonical location reference

If the user's feedback is really about an upstream reference gap, pivot out of shot triage and resolve the prerequisite reference first. Do not keep asking for approve/deny calls on downstream shots that are guaranteed to be regenerated once the reference is fixed.

Present the groupings to the user so they can see coverage at a glance.

### 5) Set queue order, then present one asset at a time

Default queue behavior for the user:
- When the user says "newly generated assets," start with the unreviewed assets from the current generation batch, not the full historical media list.
- If the user asks for descending order / highest number to lowest, sort explicitly before presenting. Use the numeric suffix that defines the review sequence for that batch (shot number, variant number, or whichever visible numbering the assets are using), and walk from highest to lowest.
- If numbering is ambiguous, say what ordering key you are using before you start the queue.

For each asset needing review:

1. Show the title and its reference context (which @image or shot group it belongs to)
2. Embed the image inline using markdown: `![title](publicUrl)`
3. Note if a newer/approved version already exists (e.g. "v3 is already green, this is v2")
4. Ask: **Approve** ✅ or **Deny** ❌?

Wait for the user's decision before moving to the next asset.

### 6) Act on the decision

**Approve:** Set `colorTag` to `green`:
```bash
curl -s -X PATCH http://<host>:3000/api/projects/<slug>/media/<assetId> \
  -H 'Content-Type: application/json' \
  -d '{"colorTag":"green"}'
```

**Approve and canonical** (when the user says so): Apply green AND canonical tags:
```bash
# Step 1: green
curl -s -X PATCH http://<host>:3000/api/projects/<slug>/media/<assetId> \
  -H 'Content-Type: application/json' \
  -d '{"colorTag":"green"}'
# Step 2: tags
curl -s -X POST http://<host>:3000/api/projects/<slug>/media/<assetId>/tags \
  -H 'Content-Type: application/json' \
  -d '{"set":["canonical-reference","recurring","hero-prop"]}'
```

Adjust tag set by asset type: locations get `canonical-location`, props get `hero-prop`, character sheets get `character-sheet`.

**Deny:** Set `colorTag` to `red`:
```bash
curl -s -X PATCH http://<host>:3000/api/projects/<slug>/media/<assetId> \
  -H 'Content-Type: application/json' \
  -d '{"colorTag":"red"}'
```

**Critical:** The PATCH path is `/api/projects/:slug/media/:assetId` — NOT `/api/media/:assetId` (which returns `NOT_FOUND`).

Verify the change took effect by checking the response JSON.

See `references/color-tag-api.md` for full endpoint shapes, batch tagging, and verification.

### 7) Summarize when done

After all assets are triaged, report:
- Total reviewed
- Approved (green) count
- Denied (red) count
- Any skipped (already tagged)

## Regeneration Within Triage

When the user says "regenerate this" or gives specific corrections (wrong surface, wrong lighting, wrong quantity) instead of approve/deny:

1. **Identify the canonical environment asset** — the user will often name or reference it (e.g. "from our canonical kitchen: asset_..."). If not explicit, find the green-tagged environment asset that the prop/location should belong to.

2. **Analyze the canonical reference first** — Use `vision_analyze` on the environment asset to extract lighting characteristics, surface materials, and mood before writing the new prompt. Don't guess.

3. **Generate via `fal-ai` with `openai/gpt-image-2`** — This is the user's preferred provider for prop/environment regeneration during triage. Pass the canonical environment as `referenceAssetIds`.

4. **Match lighting explicitly in the prompt** — Don't just say "match the lighting." Describe: "even, soft ambient daytime natural light" vs "warm overhead bulb light." the user has corrected lighting drift multiple times.

5. **Control quantity for gag intent** — When a prop communicates a narrative idea (accumulation, neglect), specify exact quantity: "at most four plates" not "a tower of plates." the user corrected "overflowing" chip bowl and "too exaggerated" plate stacks.

6. **Present the new version and continue triage** — Show the regenerated asset, get approve/deny, then move to the next asset in the queue.

## Pitfalls

- **Field name is `colorTag`, not `color`.** The DB column and API field are both `colorTag`. Using `color` silently fails.
- **PATCH endpoint is `/api/projects/:slug/media/:assetId`.** NOT `/api/media/:assetId` — the bare path returns `NOT_FOUND`. Always include the project slug.
- **Verify assetId matches title before mutating.** Copy-paste errors between a data dump and the mutation call can green/red the wrong asset. Before each PATCH, confirm the `id` you're about to use corresponds to the correct `title`. One session accidentally greened `@image2` (Spartan Writing Room) instead of `@image4` (Manuscript Stack) by grabbing the wrong row from the asset list.
- **browser_console fetch may fail on about:blank.** If the browser tab is on `about:blank` or a cross-origin page, `fetch('/api/...')` throws a URL parse error. Fall back to `curl` via terminal — it's more reliable anyway.
- **Response wrapper is `{ok, assets}`, not a bare array.** `data.map(...)` will throw; use `data.assets.map(...)`.
- **Don't auto-approve or auto-deny.** Always wait for the user's explicit decision per asset.
- **Check for superseded versions.** If a newer version of the same asset is already green, mention it — the user may want to skip or deny the older one.
- **Telegram image delivery.** Inline markdown images (`![alt](url)`) render as native photos on Telegram. Use the `publicUrl` from the API, not a constructed path.
- **Don't invent new furniture/surfaces.** When the user says "place on the couch from the canonical living room," use that exact environment asset as reference — don't let the model generate a different couch. Pass the canonical environment asset via `referenceAssetIds`.
- **Lighting drift is the #1 correction.** Models default to dramatic directional lighting. Always specify ambient/even/diffused when the canonical environment has natural daytime light.
- **Character detail drift is the #2 correction.** Never describe glasses, hat, clothing, or other character features from memory or prior session text. Always re-read the canonical character sheet asset before generating any face/character shot. the user corrected: glasses were "light tan/brown thin frames" not "black horn-rimmed"; fisherman cap was "dark navy blue cotton" not "brown corduroy." Always pass the character sheet as a `referenceAssetIds` entry and explicitly say "matching the character sheet reference" in the prompt.
- **Use the edit engine for targeted corrections.** When the user says "just change the glasses" or "fix the hat color," use Seedream 5 Lite (`provider: replicate`, `model: bytedance/seedream-5-lite`) — it preserves everything except the target element. GPT Image 2 will content-policy-block face edits; Gemini will silently return no image.

## Presentation Style

- Number assets sequentially: "Asset 1 of ~50"
- Include the reference context: which @image, shot group, or prompt list entry it maps to
- Keep descriptions brief — the image speaks for itself
- Note continuity anchors from the reference doc when relevant (e.g. "this is the typewriter that must appear in both eras")
