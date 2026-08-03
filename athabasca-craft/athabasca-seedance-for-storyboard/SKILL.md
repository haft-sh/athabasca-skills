---
name: athabasca-seedance-for-storyboard
description: Use Seedance (image-to-video) as the creative engine for storyboard sequences. Instead of generating static 3x3 storyboard grids via text-to-image, group shots into ~10-shot blocks and generate 15s video clips with hard cuts. Seedance handles scene geography, continuity, and creative interpolation from minimal reference images.
version: 1.0.0
author: Hermes Agent (Athabasca)
metadata:
  hermes:
    tags: [athabasca, seedance, storyboard, video-generation, i2v, workflow]
---

# Seedance for Storyboard

## When to Use

Use this workflow when:

- The project has a detailed shot breakdown (shot list or shot breakdown doc)
- You want Seedance (or similar I2V model) to be the **creative engine** rather than a frame-by-frame executor
- The sequence benefits from temporal continuity — match cuts, recurring locations, character movement
- You want to preview all prompts before dispatching to generation

**Do NOT use this when:**

- The project needs a static 3x3 storyboard grid (use text-to-image storyboard grid workflow instead)
- Shots require pixel-perfect adherence to reference stills (Seedance is creative, not obedient)
- The sequence is mostly dialogue-heavy with minimal visual action

## Core Philosophy

Seedance possesses strong creativity and awareness of scene geography and continuity. Rather than handholding it with detailed storyboard stills, we give it **minimal reference inspiration** and tell it to imagine and generate the scene by itself. Reference images are **anchors**, not **constraints**.

## Fast Path for Existing Prompt Previews / Shot Docs

When the user asks for a link to an existing or recently staged prompt preview, shot breakdown, asset inventory, or Seedance HTML document, **do not start by spelunking source files or route definitions**.

Default lookup order:
1. `GET /api/projects` if the user gave a project name/title instead of a slug; resolve the canonical slug from the returned project list.
2. `GET /api/projects/:slug/media` — filter project media for HTML/markdown/document assets by title, tags, `phase`, `category`, `sourceKind`, `createdAt`, and `metadataJson`.
3. Prefer the newest matching asset whose title/tags include scene identifiers such as `A2S2`, `Act 2 Scene 2`, `Seedance`, `prompt-preview`, `shot breakdown`, or `asset inventory`.
4. Return the asset’s direct `publicUrl` to the HTML/R2 file, not just the project UI URL.
5. Only query project detail after media lookup if you need script context, phase state, or no matching media asset exists.
6. Only inspect repo code/routes when debugging a broken API path or implementing a development change.

For Seedance work, generated HTML files are often the project source-of-truth for shot breakdowns, asset inventories, and prompt previews. They live as uploaded Athabasca media attached to the project, not necessarily as database `shots` records or API route-specific resources.

## Workflow Steps

### 1. Group Shots into Timing Lanes

- Divide the shot breakdown into logical groups by narrative beat, location, era, or requested rhythm
- Default heuristic: approximately 10 shots per 15-second Seedance generation (~1.5s per shot)
- If the user says the cadence is too quick or asks for more readable shots, prefer smaller lanes such as **7 shots × 2 seconds** (about 14s) and create as many lanes as needed rather than forcing exactly two generations
- Each group becomes one Seedance generation with hard cuts
- Title cards, text overlays, and static frames are NOT Seedance — note them as exclusions

### 2. Identify Reference Images Per Group

For each group, determine the minimum set of reference images needed:

- **Character identity anchors** — one per distinct character appearance (e.g., protagonist at two different ages or timelines)
- **Location/setting backgrounds** — one per distinct room or exterior
- **Key props** — only for props that carry narrative weight (signature machine, hat, manuscript stack)
- **Match-cut anchors** — shots that must visually rhyme across groups need shared reference framing

Typical reference count: 3–5 per group. Reuse across groups where possible (e.g., same character anchor).

### 3. Write Seedance Prompts

Each group prompt follows this structure:

```
I want you to generate the following scenes for our [style] film.

The setting is @imageN [location description].
The character is @imageN [character description].
[Additional reference image assignments]

N shots. Duration per shot: 1.5s. Transition: hard cuts between all shots.

Shot 1 — [Title]
[Description with framing, action, emotion, continuity notes]

Shot 2 — [Title]
[...]
```

Key principles:

- Describe action and emotion, not pixel-perfect framing
- Flag match-cut anchors explicitly ("this motion must match Shot X")
- Include camera guidance (angle, movement) but let Seedance interpret
- Use the shot breakdown's "Prompt core" as the seed, then expand with narrative context

### 4. Generate HTML Preview Document

Create an HTML document (dark theme, monospace font) that includes:

- **Director's Note** — sequence overview and creative intent
- **Technical Rules** — workflow constraints (15s per group, hard cuts, reference rules)
- **Per-group cards** containing:
  - Group title, shot range, shot count, duration, reference count badges
  - Reference image grid with IDs (@imageN), titles, descriptions, and T2I prompts
  - Full Seedance prompt text (copy-paste ready, @imageN references highlighted)
  - Shot detail table (#, shot name, type, key action, continuity notes)
- **Reference Image Manifest** — optional master table of all @imageN across all groups; omit it when the prompt preview already shows per-group reference cards and the user wants a lean copy/review document. Do not include a manifest by default for short two-lane Seedance previews unless it adds information not already visible in the group cards.
- **Cross-Group Continuity Table** — match cuts, audio mirrors, prop continuity
- **Remaining Groups table** — what's not in this preview

Upload the HTML to R2 via `POST /api/projects/:slug/media` and attach to the project.

### 5. Preview, Approve, Iterate

- Share the HTML preview link with the user
- User reviews format, grouping, and reference image list
- Adjust grouping or reference strategy based on feedback
- Once approved, convert remaining shot groups using the same format

### 6. Generate Reference Images

Before dispatching to Seedance:

- Generate all reference images via text-to-image (Midjourney for characters/mood, Gemini for backgrounds/complex compositions)
- Upload each to Athabasca via `POST /api/projects/:slug/media`
- Record the asset IDs and public URLs for the Seedance dispatch

### 7. Dispatch to Seedance

- Use the Athabasca video generation API or direct Seedance API calls
- Attach reference images in the order specified (@image1, @image2, etc.)
- One dispatch per group
- Review output, extend individual shots if needed

## Prompt Format Reference

The Seedance prompt format uses `@imageN` notation for reference image slots:

```
The setting is the @image1 grass field beyond the edge of town.
10 shots. Duration per shot: 1.5s. Transition: hard cuts between all shots.

Shot 1 — The Excitement Spreads Through the Crowd
Medium-wide asymmetrical crowd shot from child height, referenced in @image2.
In the left foreground, a small hand grips a parent's dusty sleeve...
```

## Recommended Provider Routing for Reference Images

| Reference Type              | Recommended Provider                   | Why                                                                                                                            |
| --------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Character turnaround sheets | **Gemini** (concise prompts <50 words) | Clean white backgrounds, consistent multi-view. GPT Image 2 also works but rate-limited on Plus. MJ fails (messy backgrounds). |
| Eyes ECU / macro detail     | **Gemini**                             | Follows spatial instructions (cap brim shadow, iris detail)                                                                    |
| Phone UI / text-in-image    | **Gemini**                             | Crisp text rendering, realistic UI mockups                                                                                     |
| Room/location backgrounds   | MJ V8.1                                | Best mood, atmosphere, perspective                                                                                             |
| Props (simple)              | MJ V8.1                                | Clean silhouette, dramatic mood lighting                                                                                       |
| Props (complex/spatial)     | Gemini                                 | Multi-object compositions                                                                                                      |
| Match-cut anchors           | Same provider for both sides           | Consistency across the cut                                                                                                     |

**Observed pattern in a large production run (20 refs):** most environments/props came from MJ, while character sheets and UI-style references came from Gemini. GPT Image 2 was rate-limited and skipped entirely.

## Style Direction

Use the project’s actual visual style, not a generic Athabasca default.

For live-action projects, language like ARRI Alexa, anamorphic lenses, naturalistic lighting, shallow depth, handheld, etc. may be appropriate. For animated projects, do **not** use live-action / ARRI / hyper-realistic language unless the user explicitly asks for that treatment.

**Do NOT use "anime-style" language** in Seedance prompts or reference image prompts unless the project style explicitly calls for anime. The "Anime Layout Master" skill is a general composition/framing skill — its principles apply across media, but the output language should match the project’s actual style.

## Shared CSS

All Seedance prompt list HTML documents link to a shared CSS file hosted on R2:

```
https://media.wheretoaccess.com/shared/styles/athabasca-seedance-prompts-v1.css
```

Use `<link rel="stylesheet" href="...">` in the HTML `<head>`. Do NOT inline CSS.

## Local Staging for Edit Efficiency

Athabasca-generated HTML documents are stored on R2 and served at `media.wheretoaccess.com`. The API returns a `publicUrl` — but this is the served URL, not a file you can re-download for editing. To avoid regenerating entire HTML documents for small edits, maintain local staging copies:

**Staging directory:** `~/.hermes/staging/<project-slug>/`

```
~/.hermes/staging/project-slug/
├── seedance-prompt-list.html    ← local copy for patching
├── manifest.json                ← tracks asset ID, URL, replace route, last sync
└── mj-results/                  ← per-generation result JSONs
```

**manifest.json structure:**

```json
{
  "files": {
    "seedance-prompt-list.html": {
      "athabascaAssetId": "asset_xxxx",
      "athabascaAssetUrl": "https://media.wheretoaccess.com/...",
      "athabascaReplaceRoute": "POST /api/projects/:slug/media/:assetId/replace",
      "phase": "storyboard",
      "lastSynced": "2026-05-29T00:12:58Z",
      "sizeBytes": 79167,
      "description": "..."
    }
  },
  "project": "project-slug",
  "projectSlug": "project-slug",
  "cssUrl": "https://media.wheretoaccess.com/shared/styles/athabasca-seedance-prompts-v1.css"
}
```

**Edit workflow:**

1. Read `manifest.json` → find local file path
2. Patch the local HTML file with targeted edits
3. Re-upload via `POST /api/projects/:slug/media/:assetId/replace` with `file=@local-path`
4. Update `lastSynced` in `manifest.json`
5. Athabasca will persist the file to R2 and return a NEW `publicUrl` with a new timestamp in the key

**Important:** The `publicUrl` after a replace will differ from the old one (R2 key gets a new timestamp). Update `athabascaAssetUrl` in `manifest.json` with the new URL returned by the API.

**CSS shared across projects:** When creating a new project's prompt list HTML, extract reusable CSS to `shared/styles/athabasca-seedance-prompts-v1.css` on R2. Link to it rather than inlining. When updating the shared CSS, edit the single R2 file — all projects using it get the update automatically.

## Prompt Document Conventions

### Per-group shot and reference renumbering (stateless Seedance)

Each group/lane in the prompt document must **start at Shot 1** and renumber sequentially within the group. Use unpadded local numbering (`Shot 1`, `Shot 2`, `Shot 3`), not global/source numbering and not padded `Shot 001` style inside the copy-paste Seedance prompt. Seedance is stateless and only sees the current group's prompt — it has no awareness of global shot numbering.

Do **not** include phrases like `source Shot 013` inside the Seedance prompt text. Original/global numbering may appear only in human-facing group metadata outside the copy-paste prompt if useful for review.

`@imageN` references are also **relative to the group/lane**. Reset reference numbering for each group, so Group B starts again at `@image1`, `@image2`, etc. Do not use a single absolute @image sequence across the whole HTML document.

### Verbose/direct shot format

For generation-ready prompt documents, use the **expanded verbose format** per shot, but avoid redundant fields. Each shot should fold the generation guidance into structured fields such as:

```
Shot 3 — Title
Subject / Action: what fills the frame and what changes during the shot.
Camera: angle, position, perspective, movement.
Composition: subject placement, foreground/midground/background layers, continuity and editability guidance.
Lighting: quality, direction, color — optional per shot only when that shot needs specific lighting instructions. If a lighting note applies to every shot, move it to the global group preamble instead of repeating it per shot.
Focus: what is sharpest / eye trace.
Emotion: the dramatic read.

If a shot has a shortlisted anchor image, include `Anchor image: @imageN`. If it does not, omit the Anchor image line entirely; do not add explanatory fallback text about using candidate/context images.

Global prompt guidance should be direct instructions to Seedance only. Do not include agent-facing meta-instructions such as "do not repeat generic composition language" or explanations of how the prompt document was edited; silently apply those constraints while authoring the copy-paste prompt.
```

Do **not** add a separate `Prompt core` field when it merely duplicates the structured fields above. Merge any useful prompt-core language into Subject / Action, Camera, Composition, Lighting, Focus, or Emotion.

Do **not** append a separate `Shot Details` section after the prompt. If an action, continuity note, or editorial instruction matters, integrate it into the relevant shot prompt itself so the copy-paste block is self-contained and non-redundant.

Seedance prompts must be self-contained. Do **not** mention background process/history such as `v1 blocking problem`, `matching the script`, `source shot`, `previous grid`, `mandatory reference coverage`, or other context Seedance cannot know. Convert those notes into direct visual instructions (for example: `the character remains upright at the location edge, planted on their feet` instead of explaining what an earlier version got wrong).

Alternate angles/treatments must be first-class shots, not parenthetical permission language. Do **not** write `let Seedance find a low/wide angle` or similar. If alternate coverage is wanted, add a new numbered shot with the same fields as the others and describe the frame, camera, composition, lighting, focus, and emotion explicitly.

### Avoid redundant per-shot boilerplate

Do not repeat generic composition, lighting, or cinematic-quality rules in every individual shot. If guidance applies across the whole Seedance clip — for example `preserve foreground/midground/background separation`, `strong silhouette`, `clear eye trace`, global lighting mood, or premium animated-feature style — move it into the group preamble once. Individual `Composition:` lines should remain only when they add shot-specific staging: subject placement, screen direction, blocking, foreground/midground/background use for that beat, emotional emphasis, or continuity into/out of adjacent shots.

### Reference image text accuracy

Reference image descriptions are model-facing instructions, not labels for humans only. Do not embellish or infer prop colors/materials from memory. Match the actual canonical asset and user corrections exactly. When uncertain, inspect the asset or use neutral wording rather than a specific false visual attribute.

### Reference manifest with canonical asset links

When the reference image manifest is included in a prompt document:

- Reference IDs (e.g. `@image1`) should be styled in **green** to signal approved/canonical status.
- Each ID should **link directly** to the asset's `publicUrl` in Athabasca media (not a placeholder).
- The manifest table should include: ID, title (linked), used-in groups, provider, and notes.

This prevents the disconnect where @imageN references are opaque and agents must separately resolve them from the media API.

### Draft/review status tagging

Non-final prompt documents uploaded to Athabasca should be marked through media metadata, not inline warning boxes. Use `PATCH /api/projects/:slug/media/:assetId` with fields such as `colorTag`, `ratingStars`, and `tags` (for example `A2S1`, `seedance`, `prompt-preview`, `v2`). Do **not** include a visible `DRAFT` warning banner in the HTML body unless the user explicitly asks for inline status text.

## Pitfalls

- **CRITICAL: Always resolve @imageN to green-tagged (approved) assets.** When the reference image manifest lists `@imageN`, resolve it to the asset with `colorTag: "green"` in the Athabasca media section. Using non-green assets (yellow, red, or uncolored) is a common error — the user will catch it and ask you to swap. Query `GET /api/projects/:slug/media` and filter for `colorTag: "green"` assets matching the reference concept. If multiple green assets exist, pick the latest by `createdAt` or the one with the highest version in the title.
- **HTML group card div nesting bug.** When inserting reference image cards into group cards, the insertion point is **after** the note's closing `</div>` and **before** the `<h4>Seedance Prompt` heading. The regex pattern to match is `r'(</div>)\s*(<h4>Seedance Prompt — Expanded</h4>)'` — insert the reference section between capture group 1 and capture group 2. Do NOT consume the `</div>` in the replacement string; that leaves the note div unclosed and causes cumulative nesting (each group card gets narrower down the page).
- **Staging directory, not /tmp.** When building/editing Seedance prompt HTML documents locally before upload, use the project staging directory (`~/.hermes/staging/<project-slug>/`) as defined in the "Local Staging for Edit Efficiency" section. Do not use `/tmp` — it gets cleaned and you lose iteration history. Write to `~/.hermes/staging/project-slug/seedance-prompt-list.html` (or similar) and track it in `manifest.json`.
- Do not overload reference images. 3–5 per group is usually sufficient. 9 is the maximum. More refs = more identity drift risk.
- Do not expect Seedance to perfectly replicate reference stills. It interpolates and imagines. That's the point.
- Title cards and text overlays should be added in post, not generated by Seedance.
- Match-cut shots need extra attention: generate the reference for BOTH sides of the cut from the same seed/prompt structure.
- If a group has more than ~12 shots, consider splitting it. 15s is the practical maximum for coherent single-generation output.
- Static frames (black screen, title text) waste Seedance capacity — exclude them from groups.
- **Never use "anime" in prompts.** The style is live-action cinematic. The Anime Layout Master skill provides composition principles, not visual style.
- **AspectRatio enum:** Athabasca's image generation API validates `aspectRatio` against `landscape | square | portrait`. Passing `"16:9"`, `"1:1"`, or `"9:16"` returns a validation error. Always use the enum values.
- **Batch scripts belong in the project repo `scripts/` directory, not `/tmp`.** `/tmp` gets cleaned periodically and scripts are lost. Generation scripts are project-specific reference material — future iterations or similar projects benefit from having them on disk.
- **No Music means no musical bed, not no audio.** For Seedance dispatches, keep `generateAudio: true` when dialogue/foley/ambience/SFX are useful, and put `No Music` in the prompt to discourage generated score. Only disable audio when the user explicitly asks for silent visuals.
- **For same-prompt first-frame style tests, preserve the source still.** When the user asks to animate several shortlisted stills "for comparison" with the same prompt, use one shared prompt that emphasizes locked composition, preserving shapes/palette/handmade style, low-frame-rate stop-motion motion, tiny paper jitter, simple layer parallax, and restrained puppet-like motion. Avoid prompt-specific narrative beats that would make clips incomparable.
- **Seedance 3s I2V may be invalid upstream.** Replicate and BytePlus rejected 3s Seedance I2V on 2026-06-05 even though capabilities advertised it. If the user requests 3s, try the normal path safely; if upstream rejects duration, use 4s as nearest valid fallback and disclose clearly.
- **Reference Images vs Candidate Images:** In prompt-preview HTML, separate the slim Seedance attachment shortlist from human-editor context images. `Reference Images` are the only images assigned `@imageN` and referenced in the prompt. `Candidate Images` contain generated stills for context/inspiration only, do not need `@imageN` captions, and should not be attached to Seedance unless promoted.
- **Remaining-scene continuation fallback:** When continuing scene-by-scene through a film and a populated asset inventory is missing for the next scene, do not stall if the shot list and adequate canonical/reference assets exist. Build the preview from the shot list plus existing project media, prior I2V/prompt-preview context, and relevant canonical references; state the missing inventory clearly in the manifest and final report. Keep the same per-lane preview format and verification expectations so the user can keep momentum.
- **No redundant image-card captions:** If an image card title link already names the shot clearly, do not add a second line that repeats the same shot title in prose. Keep the linked title, usage/asset id, and any genuinely non-redundant metadata only.
- **Canonical green references:** If a user identifies a green canonical replacement asset, swap it into every affected group’s Reference Images and remove red/deletion-bound predecessors from the Reference shortlist. Candidate Images may still show historical/generated stills if useful for human context, but not as `@imageN` references.
- **Prompt preamble format:** Each group's Seedance prompt should begin with a declarative preamble that assigns reference images to roles before listing shots:

```
I want you to generate the following scenes for our [style] film.

The setting is @imageN [location description].
Character: @imageN [character description].
Typewriter: @imageN. Stack: @imageN.
N shots. Duration per shot: ~1.5s. Transition: hard cuts between all shots.
```

This tells Seedance how each reference maps to the scene, rather than just listing IDs.

## Example Output

See: a project prompt-list asset such as `project-slug-seedance-groups-abc` — a complete long-form prompt list split into multiple groups, using live-action cinematic style, shared CSS, and local staging.

## Related Reference Files

- `references/mj-batch-generation-via-api.md` — bash pattern for batch-submitting MJ reference image generations through the Athabasca API with 429-rate-limit protection
- `references/seedance-html-generator-pattern.md` — Python HTML generator pattern, live-action style language, no-anime rule
- `references/canonical-ref-image-resolution.md` — green asset resolution pattern, inline reference card HTML, and a verified asset-table pattern from a completed production run
- `references/canonical-ref-image-resolution.md` — color tag conventions, green asset resolution pattern, inline reference card HTML
- `references/asset-inventory-to-seedance-preview.md` — build a prompt-preview HTML from a shot-list markdown plus asset-inventory HTML, including anchor images, reuse-map supporting assets, `@imageN` role declarations, upload/tag/verification expectations
