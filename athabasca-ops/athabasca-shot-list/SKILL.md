---
name: athabasca-shot-list
description: Use when saving or updating Athabasca project shot lists from structured or markdown shot-list input, and when attaching generated media to specific shots.
version: 1.0.0
---

# Athabasca Shot List Persistence

Use this skill when the user gives a shot list and asks you to persist it in Athabasca, or when you need to attach generated media to a specific shot.

The canonical phase for this work is `shot_list`.

## Workflow

### Default persistence path

1. Read the current project state.
2. Parse each shot into:
   - `shotNumber`
   - `durationText`
   - `durationMinSeconds`
   - `durationMaxSeconds`
   - `frame`
   - `action`
   - `purpose`
   - `notes` when needed
3. Write the full list with `POST /api/projects/:slug/shot-list`.
4. Verify with `GET /api/projects/:slug/shot-list`.
5. When attaching existing media to a specific shot, first upload or create the asset, then attach it explicitly to the shot.

### Text-only / no-DB-write path

If the user explicitly says they do **not** want individual shot-list rows written to the DB, do **not** call `POST /api/projects/:slug/shot-list`.

When the user asks for an exploratory scene shot list, bias toward **over-generation rather than minimal coverage**. Give more editorial options than strictly necessary, then let later triage remove redundant shots. Do not prematurely compress the scene to a minimal set unless the user asks for a selects pass.

Instead:
1. Read the current project + script/report context so the source scene is identified precisely.
2. Draft the shot list as markdown text.
3. Include a short provenance block in the markdown with at least:
   - project slug/name
   - source script/report id and title when available
   - source scene/sequence heading
   - authoring model/provider
   - skill name + version used for the conversion
   - explicit note that this is exploratory text coverage and does not mutate structured shot rows
4. **Preferred path (report-based):** Write the shot list as a research report with phase `shot_list`:
   ```
   POST /api/projects/:slug/research-report
   {"phase":"shot_list","title":"...","summary":"...","contentMarkdown":"...","images":[]}
   ```
   This auto-advances `phaseStatuses.shot_list` to `drafted` and sets `currentPhase` to `shot_list`.
5. Upload the markdown as an R2 media artifact for durable file storage:
   ```
   POST /api/uploads  (multipart form)
   ```
6. Verify the report exists and phase status was updated:
   ```
   GET /api/projects/:slug
   ```

**Why report-based over media-based:** The report approach sets phaseStatus automatically and gives a reviewable artifact in the project's phase record. The media upload path (`POST /api/projects/:slug/media`) works but doesn't advance phase state.

Use this path for requests like:
- "text only"
- "don't update the DB"
- "just attach it as a .md file"
- "conversation/output only, no shot entries"

When the user wants coverage for a whole script or act but still wants it **divided into scenes**, prefer one markdown artifact per scene rather than one giant omnibus file. Keep each scene self-contained with its own dramatic objective, geography/axis strategy, shot list, and editing risks so later triage can happen scene-by-scene.

### Scene numbering convention for the user

When the user wants scene-based artifacts derived from a script, default to **resetting scene numbers at the start of each act** for the artifact title/body (for example, `Act 2 Scene 1`) even if the source script uses global numbering (for example, `Scene 3`). Preserve the source script numbering in the provenance block when relevant so the mapping stays explicit.

Use this especially for shot-list markdown, storyboard-grid titles, and provenance notes where global numbering would otherwise make the review surface harder to scan.

## Parsing Rules

- Preserve the user's wording for `frame`, `action`, and `purpose`.
- Keep `durationText` exactly as written when it is meaningful.
- Normalize simple ranges into numeric bounds.
- Do not invent missing shot content; leave the shot as provided and note any gaps in `notes`.
- Keep shot numbers unique and ordered.
- Prefer stable numbering over renumbering if the user is revising only one shot.

## API Notes

- Use `GET /api/projects/:slug/shot-list` to read the current list and resolve the target `shotId`.
- Use `POST /api/projects/:slug/shot-list` to replace or update the list.
- For shot-specific user-supplied media, prefer a single-step upload to `POST /api/projects/:slug/media` with multipart fields including `phase=shot_list` and an `attachment` JSON string like `{"targetType":"shot","targetId":"shot_...","role":"reference"}`. This creates the asset and links it to the shot in one request.
- This one-step `POST /api/projects/:slug/media` + `attachment` flow works for both images and videos and also puts the asset into the project's media library.
- If you already have an existing project asset id, or if you used `POST /api/uploads` instead, then attach it separately with `POST /api/projects/:slug/shots/:shotId/media` and `{ "assetIds": ["asset_..."] }`.
- Do not assume a project media upload attaches to the shot unless you explicitly pass the `attachment` payload or make the follow-up shot-attachment call.
- If the project does not yet have shots, create the shot list before linking media.

## Finding Existing Shot List Artifacts

Shot list markdown artifacts are stored as project media assets with `phase=shot_list` and `category=generated`. They are NOT accessible via a dedicated `/shot-list-artifacts` endpoint — they are mixed into the general media library.

**Discovery query:**
```bash
curl -sS "http://localhost:3000/api/projects/:slug/media?phase=shot_list"
```

From the response, extract entries where `phase === "shot_list"`. The `title` field contains the scene name (e.g., `"Act 2 Scene 2 Shot List v1"`).

**Constructing the R2 URL:**
The `storageKey` field in each asset gives the R2 key. Construct the public URL directly:
```
https://media.example.com/{storageKey}
```

Example:
- storageKey: `project-slug/generated/act-2-scene-2-shot-list-v1_1778681001581.md`
- public URL: `https://media.example.com/project-slug/generated/act-2-scene-2-shot-list-v1_1778681001581.md`

**JSON parsing note:** Responses from `/api/projects/:slug/media` with large asset lists may contain invalid control characters. Use `strict=False` in `json.loads()` or handle with regex extraction for reliability.

### Shot Breakdown + Seedance Prompt List Amendment

When the user asks to amend shots (remove, add, change) after the initial shot list is locked, there are typically **two documents** that must be updated in lockstep:

1. **Shot breakdown** (markdown) — per-shot framing, composition, lighting, prompt cores
2. **Seedance prompt list** (HTML) — group-based Seedance generation prompts with inline reference image cards and @imageN prompt preambles

If the change is not just editorial coverage but a **core premise / product-logic correction** (for example: the device is bidirectional, a UI mode changes meaning, a translated-speech pathway becomes explicit, or a hero prop's operational states are redefined), treat it as a **cross-phase continuity update**, not just a storyboard edit.

In that case, also update the script-phase artifact so the premise is canonical in prose before or alongside the storyboard amendment.

**Related skill:** `athabasca-seedance-prompt-docs` — covers the full Seedance prompt document structure, reference card format, prompt preamble format, shot renumbering per group, and style language rules (cinematic, not anime).

### Amendment workflow

When removing or adding shots:

1. **Identify affected sections in both documents.** Use `grep` or search for shot numbers, section headers, and reference image IDs.
2. **Remove/add shot entries** in the shot breakdown markdown.
3. **Renumber all subsequent shots** by the delta (e.g., removing 1 shot means all shots after it shift by -1).
4. **Update the Seedance prompt list:**
   - Remove/add the shot description in the group's Seedance prompt text
   - Update the group header badge (shot count)
   - Update the shot range (e.g., `Shots 099–110` → `Shots 099–109`)
   - Update the shot detail table rows
   - Renumber shot table rows for all subsequent groups
5. **Update reference image manifests** if a shot removal eliminates the only consumer of a reference image:
   - Remove the `@imageN` ref card from the group's reference grid
   - Remove the `@imageN` reference from the Seedance prompt text
   - Remove the `@imageN` row from the reference manifest table at the bottom of the HTML
6. **When the user clarifies product behavior or operational grammar**, propagate that logic through the storyboard artifact explicitly:
   - update the **global continuity anchors** section first
   - revise keynote / exposition shots that teach the audience how the device works
   - revise downstream shots whose motivation depends on that premise (e.g. why a character can understand TTS)
   - if the prop has distinct operational states, name them clearly and keep their visual grammar consistent (for example OFF / INPUT / OUTPUT / SYSTEM)
7. **Upload both amended documents** as new versions to Athabasca:
   - `phase=storyboard`, `category=misc`, `sourceKind=generated`
   - Include `metadataJson.supersedes` pointing to the old asset ID
   - Add provenance note describing the change
8. **Tag the new versions** with `v2`, `canonical-doc`, and change-specific tags (e.g., `phone-screen-amended`).
9. **Mark old versions** with `colorTag: "yellow"` (superseded).

### Asset Inventory HTML (from shot breakdown)

When the user asks for a visual asset inventory as an HTML table derived from a shot breakdown:

1. Parse the shot breakdown markdown — extract: ID, title, subject, action, sequence, category per shot
2. Classify shots into categories: CHARACTER, CHARACTER (DOG), ESTABLISHING SHOT, ENVIRONMENT/SET, PROPS, INSERT/UI ELEMENT, CUTAWAY/B-ROLL, PURE VOID/BLACK
3. Reuse the project's existing CSS (check for a shared stylesheet URL like `athabasca-seedance-prompts-v1.css` in the project media library) via `<link rel="stylesheet">` for visual consistency
4. Build an HTML table with columns: ID, Item, Description, Sequence, Image
5. Include a styled placeholder image cell in each row — use a `div` with dashed border and centered placeholder text, not a broken `<img>` tag
6. Upload as `POST /api/projects/:slug/media` with `phase=storyboard`, `category=generated`, `sourceKind=generated`, and `metadataJson` including act, type, version, shot_count

**Related skill:** `athabasca-anime-layout-master` covers the live-action session patterns (brand substitution, VO remix, document amendment) that often accompany shot breakdown work.

### Pitfalls

- **Always renumber after removal.** Shot numbers are used as cross-references between groups. Missing a renumber creates broken continuity anchors.
- **Check inline references.** Shot numbers appear in section headers, shot tables, continuity notes, and Seedance prompt text. Search broadly, not just in the affected section.
- **Reference images may have multiple consumers.** Before removing an `@imageN`, verify no other group or shot references it.
- **The Seedance prompt text and shot detail table must agree.** If you remove a shot from the prompt text but leave its row in the table, Seedance will generate the wrong number of clips.
