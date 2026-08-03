---
name: athabasca-seedance-prompt-docs
description: Create, iterate, and upload Seedance prompt HTML documents for Athabasca projects. Covers group-based video generation prompts with inline reference image cards, shot renumbering, and version management.
version: 1.0.0
author: Hermes Agent (Athabasca)
---

# Athabasca Seedance Prompt Documents

Use this skill when JP asks to create, update, or upload a Seedance prompt HTML document for an Athabasca project. These documents are the dispatch surface for Seedance 2.0 / Kling I2V image-to-video generation — they contain group-based shot breakdowns with inline reference images that Seedance uses as anchors.

## Document Structure

A Seedance prompt HTML document has this structure:

1. **Project header** — title, project name, workflow, style, model, total shot count
2. **Status banner** — colored indicator (red = draft, green = ready)
3. **Table of Contents** — links to each group and the reference manifest
4. **Director's Note + Technical Rules** — style guide and generation rules
5. **Per-group cards** — each group contains:
   - Group header with badges (era, shot count, duration, ref count)
   - Continuity note
   - **Reference Images section** — grid of cards with thumbnails, titles, descriptions, prompts, and asset IDs
   - **Seedance Prompt** — preamble with @imageN tags, then shot-by-shot breakdowns
6. **Reference Image Manifest** — canonical table with green-linked asset URLs
7. **Cross-Group Continuity Anchors** — match-cut reference table
8. **Footer** — generation provenance

## Reference Image Cards

Each group must have a **Reference Images section** with actual image cards — NOT just text labels like `@image1, @image2`. JP will reject a document that lists refs as bare text without thumbnails.

### Card format

Each reference image card includes:
- **Thumbnail** — `<img>` tag loading from the asset's `publicUrl`
- **@imageN tag** — the Seedance reference identifier (e.g., `@image1`)
- **Title** — human-readable name (e.g., "George 2012 — Character Sheet")
- **Description** — brief visual description (e.g., "Younger lean bearded fantasy novelist. Fisherman's cap.")
- **Generation prompt** — the original text-to-image prompt used to create it
- **Asset ID** — the Athabasca asset ID in monospace (e.g., `asset_mpq74mjl8bbeggmf`)

### CSS for ref cards

```css
.ref-cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }
.ref-card { background: #1e1b2e; border-radius: 8px; padding: 0.75rem; }
.ref-card img { width: 100%; aspect-ratio: 1; object-fit: cover; border-radius: 6px; margin-bottom: 0.5rem; }
.ref-card-tag { color: #a78bfa; font-weight: 700; font-size: 0.85rem; }
.ref-card-title { font-weight: 600; font-size: 0.9rem; margin: 0.25rem 0; }
.ref-card-desc { font-size: 0.8rem; color: #9ca3af; margin-bottom: 0.5rem; }
.ref-card-prompt { font-size: 0.75rem; color: #a78bfa; font-style: italic; background: #2d2640; padding: 0.4rem; border-radius: 4px; }
.ref-card-asset { font-size: 0.7rem; color: #6b7280; margin-top: 0.3rem; font-family: monospace; }
```

## Prompt Preamble

Inside each group's `seedance-prompt` div, the preamble must integrate `@imageN` tags as Seedance instructions — not as a bare list.

### Correct format

```html
<p class="preamble">I want you to generate the following scenes for our live-action cinematic satirical comedy film.

The setting is the spartan writing room in @image2. Character: @image1. Typewriter: @image3. Manuscript stack: @image4.
14 shots. Duration per shot: ~1.1s. Transition: hard cuts between all shots.</p>
```

### Incorrect format (JP will reject)

```html
<p>📎 Reference images for this group: @image1, @image2, @image3, @image4</p>
```

The preamble must tell Seedance HOW to use the reference images, not just list them.

## Group-to-Reference Mapping

Each group has a specific set of reference images. Build this mapping from the original reference manifest, then generate the reference card section per group:

| Group | Reference Images |
|-------|-----------------|
| A (2012 Machine) | @image1, @image2, @image3, @image4 |
| B (King at Rest + Eyes) | @image1, @image5, @image6, @image7, @image8 |
| C (Fridge Epiphany) | @image5, @image9, @image10, @image11 |
| D (Stack Grows) | @image1, @image2, @image3, @image12 |
| E (Microwave Ding) | @image5, @image9, @image13 |
| F (Publisher Call) | @image5, @image6, @image14 |
| G (War Room + Match) | @image1, @image2, @image3, @image15 |
| H (Play Fails) | @image5, @image6, @image7, @image14 |
| I (Writing Room Threshold) | @image5, @image16, @image17, @image19 |
| J (Writing Room Setup) | @image5, @image3, @image17, @image19 |
| K (Writing Room Typing) | @image5, @image3, @image17 |
| L (Writing Room Exit) | @image5, @image3, @image17, @image18, @image19 |
| M (Hunger + Sandwich) | @image1, @image5, @image6, @image7 |
| N (Final Tweet + drago) | @image5, @image6, @image17, @image18, @image19 |

## Shot Renumbering

**Seedance is stateless** — it sees only the current group's prompt. Shot numbers must reset for each group.

### Renumbering rules

1. Inside each copy-paste Seedance prompt, start at unpadded `Shot 1` and continue sequentially (`Shot 2`, `Shot 3`, etc.).
2. Keep original/global padded ranges such as `001–005` only in human-facing group headers, TOC labels, or metadata outside the prompt block.
3. Multi-shot ranges inside a prompt must be renumbered relative to that group.
4. Update shot IDs, shot headers, and ranges consistently; do not leak phrases such as `source Shot 013` into model-facing prompt copy.
5. Reset `@imageN` numbering per group as well, because each dispatch is independent.
6. Update group badges and TOC ranges to make both local dispatch numbering and source coverage unambiguous.

### Example

A group covering source shots `016–020` should display that global range in its header, while its prompt contains `Shot 1` through `Shot 5`.

## Style Language: Cinematic, Not Anime

Seedance generates live-action cinematic video. **All "anime" references must be replaced with cinematic/live-action language.**

### Common replacements

| Anime term | Cinematic replacement |
|-----------|----------------------|
| anime action close-up | cinematic action close-up |
| anime storyboard layout | cinematic storyboard layout |
| anime storyboard insert | cinematic storyboard insert |
| anime storyboard panel | cinematic storyboard panel |
| anime production sketch | production sketch |
| anime drama close-up | cinematic drama close-up |
| anime comedy framing | cinematic comedy framing |
| anime comedy layout | cinematic comedy composition |
| anime comedy close-up | cinematic comedy close-up |
| anime comedy insert | cinematic comedy insert |
| anime deadpan comedy | cinematic deadpan comedy |
| anime satire layout | cinematic satire composition |
| anime visual irony | cinematic visual irony |
| anime visual match cut comedy | cinematic visual match-cut comedy |
| anime close-up | cinematic close-up |
| anime insert | cinematic insert |
| anime layout | cinematic composition |
| anime lighting | cinematic lighting |
| anime detail shot | cinematic detail shot |

Catch any remaining standalone "anime" words with a final regex pass: `re.sub(r'\banime\b', 'cinematic', html, flags=re.IGNORECASE)`.

## Source-synthesis rule when JP provides both a shot list and a script

When JP supplies **both** a scene shot list and the broader script and asks for a prompt preview doc, do not treat them as redundant.

Use them in this precedence order:
1. **Shot list drives the beat decomposition** — which moments belong in Group A vs Group B, what the shot count should be, and which visual actions deserve their own prompt shots.
2. **Script supplies exact dialogue, props, and emotional wording** — pull spoken lines, object details, and behavioral nuance from the script when the shot list is more schematic.
3. **Canonical assets constrain identity and geography** — character-sheet refs preserve who the character is; environment refs preserve where the scene is.

Operationally:
- do not simply paraphrase the script scene top-to-bottom into a prompt block
- do not blindly mirror every shot-list shot one-for-one if the preview format wants grouped 15-second lanes
- compress the scene into dispatchable groups while preserving the shot list's emotional order and the script's exact visible beats
- if a line of dialogue is important to the beat, include the literal line in the prompt rather than summarizing it vaguely
- if the script and shot list differ in specificity, prefer the shot list for staging order and the script for exact on-screen content

This is especially important for intimate room-scale GLY scenes: the shot list usually contains the camera psychology and continuity logic, while the script carries the exact spoken beats and prop business that Seedance needs stated explicitly.

## Stateless prompt explicitness for Seedance

Seedance does **not** know the broader script, ritual, lore, or prior discussion unless you restate it in visible terms inside the prompt.

When a shot references something like:
- "the ritual"
- "the lesson"
- "the callback"
- "the words land"
- "he follows the instruction"

rewrite it into concrete on-screen information:
- the exact spoken phrase when important
- the exact hand placement / body action
- the exact prop appearance and visible text
- the exact light effect or motion cue
- the exact identity/appearance of the characters and setting elements that matter

Bad:
- `GLY instructing Turbo in the Just Walk Through Shield ritual.`
- `Turbo follows the first ritual instruction.`
- `The ritual language is introduced clearly and simply.`

Better:
- `GLY, a small calm glowing blue guide, tells Turbo: "This is the Just Walk Through Shield. One hand on your chest. One hand on your shell. Breathe in. Breathe out. Then just walk through."`
- `Turbo places one hand flat on the center of his chest while listening.`
- `Turbo's wooden shield fills the foreground with the painted word "Turbo" visible as a soft golden-green ripple crosses it.`

Rule of thumb: if the line would make sense only to a human who already read the script, it is too implicit for Seedance and must be expanded.

## Format-cloning workflow

When JP says a new prompt preview should be **"in this format"** and points at an existing published HTML prompt preview, do not invent a new wrapper.

Preferred workflow:
1. Fetch the referenced published HTML and treat it as the structural template.
2. Preserve the same CSS link, page rhythm, section ordering, reference-card treatment, and overall review-doc shape unless JP explicitly asks for a redesign.
3. Rewrite the scene-specific copy inside that wrapper: title, director note, group headers, reference cards, prompt preambles, and per-shot text.
4. If the user calls out a markup defect in the existing wrapper, fix that defect while preserving the wrapper shape. In particular, when JP says the text should wrap and the page needs a fixed-width container, add a bounded main wrapper (for example `max-width` + centered margin + padding) and explicitly set long prompt blocks / figcaptions to wrap (`white-space: pre-wrap`, `overflow-wrap: anywhere` or equivalent) so large pasted prompts and long asset URLs do not overflow.
5. If a normal full GET is blocked but a ranged GET works, use the ranged/body fetch path rather than concluding the document is unavailable.
6. Only after the wrapper is locally inspectable should you rewrite the new scene.

Required wrapper repair pass when the source doc has legibility issues:
- Add a fixed-width main content container (for example `max-width` + centered margin) so long prompt text does not stretch edge-to-edge.
- Add `white-space: pre-wrap`, `overflow-wrap: anywhere`, or equivalent wrapping protection on long prompt blocks and captions so text wraps instead of overflowing.
- Keep explicit `width` / `height` attributes plus `max-width:100%; height:auto; object-fit:contain;` on reference images so cards stay constrained.
- Make full-resolution review intentional: wrap each thumbnail in an anchor to the original `publicUrl` and add an obvious `Open full size` link below it. Constrained thumbnails are for scanning; the original asset is the review surface for detail.
- Put `min-width: 0; overflow: hidden; overflow-wrap: anywhere;` on cards/captions and `box-sizing: border-box` globally so long asset names and URLs cannot bleed past borders.
- Verify the published HTML actually contains the wrapper fix before reporting success.

This is especially important for GLY Seedance previews because JP is often approving a dispatch surface shape, not just the prompt text inside it.

9. Verify the uploaded HTML body contains the expected wrapper-fix markers (for example `max-width:` and `white-space:pre-wrap`) before reporting success.

This is especially important for GLY Seedance previews because JP is often approving a dispatch surface shape, not just the prompt text inside it.

## Character-reference interpretation rule

When the supplied reference asset is a **character sheet whose wardrobe does not match the target scene**, treat it as an **identity / silhouette / proportion reference**, not a literal costume instruction.

Operational rule:
- preserve head-to-body ratio, face shape, shell shape, limb scale, eye size, and overall childlike acting silhouette
- do **not** blindly carry over clothing, glasses, sports uniforms, or other scene-specific wardrobe from the sheet if the script beat clearly wants a different costume/state
- if needed, state this explicitly in the reference card description so the Seedance operator understands what the reference is controlling

## Two-group intimate-scene timing rule

When the scene is intimate, room-scale, and performance-driven rather than action-heavy, a good default for **two groups of 15 seconds each** is:
- **5 shots per group**
- **~3.0 seconds per shot**

This gives enough hold time for:
- breathing beats
- prop/business comedy timing
- small emotional transitions
- clear room geography

Use faster shot counts only if the scene genuinely wants montage energy.

## High-density sequence compression rule

When the source shot list is **long and editorially dense** (for example 25–35 shots for a dream, sports play, panic spiral, or action passage) but JP asks for a Seedance prompt preview doc, do **not** automatically mirror the source one-shot-for-one-shot into the preview.

Instead:
1. Identify the **emotional spine** of the sequence.
2. Build dispatchable groups around that spine, not around arbitrary shot-count chunks.
3. Preserve the beats that the scene actually lives or dies on:
   - setup pressure
   - commitment / handoff / instruction
   - brief success or possibility
   - reversal / freeze / failure
   - exit image
4. Pull in the script's **exact dialogue lines** when they are the hinge of the beat (for example: the trust line, the command, the joke button, the confession).
5. Keep each group to a small number of shots with clear cause/effect progression rather than trying to summarize every insert from the source markdown.

Example pattern for a pressure-dream sports scene:
- **Group A:** arena pressure → huddle compression → key instruction → trust lands on hero → ball/handoff becomes real
- **Group B:** launch/run → threat glance → open lane appears → freeze behavior triggers → impact / aftermath / black

### Full-shot preservation mode

If JP explicitly pushes back on over-compression, asks to **maintain all the original shots**, or frames the preview doc as a fuller scene-preservation pass rather than a quick-generation probe, switch modes.

In this mode:
- preserve the entire source shot-list order
- keep every original beat represented somewhere in the preview doc
- **retain every source control field in the model-facing shot copy:** Subject, Action, Dialogue / sound, Composition, Visual focus, Emotion, and Continuity note. Do not condense these into a one-sentence beat summary: framing, eye trace, performance, and cut logic are dispatch controls.
- redistribute the material into **dense multi-shot groups** rather than collapsing the whole scene into two broad lanes
- if JP specifies the group size (for example, **groups of 5 shots**), treat that as exact: a 30-shot list becomes six groups covering 001–005, 006–010, 011–015, 016–020, 021–025, and 026–030
- when no group size is specified, use the scene rhythm to choose it; for action/dream sequences, a strong default is **~6–7 shots per group at ~2 seconds each**, while intimate room-scale coverage often benefits from **5 shots at ~3 seconds each**
- preserve intentionally static transition shots such as full black or full white when the user asks for **all** source shots; do not silently drop them merely because static frames are normally inefficient for Seedance
- show the **original source-shot ranges** in the group headers so the grouping is traceable back to the markdown
- reset the copy-paste prompt numbering to local `Shot 1`–`Shot N` inside every group; keep global/source numbering outside the prompt block only
- be explicit in the director note about why this version exists (for example: preserving all 30 source shots instead of a 10-shot summary)
- verify coverage mechanically before upload: group count, source ranges, local shot resets, required reference IDs, absence of replaced reference IDs, fixed-width wrapper, and prompt text wrapping

Important distinction:
- **quick probe / first-pass generation doc** -> aggressive compression is acceptable
- **canonical prompt preview doc when the user cares about preserving storyboard grammar** -> over-compressing into two or three giant lanes is the wrong move

Rule of thumb: the preview doc is a **dispatch surface**, not an archival mirror of the full storyboard markdown — but when the user explicitly asks to preserve the original shot architecture, honor that and compress only as much as needed for generation, not more.

See `references/full-shot-five-shot-group-expansion.md` for a compact build-and-verification recipe.

For a full review/dispatch packet that preserves source coverage, dialogue placement, visual-element continuity, legible reference cards, and durable project handoff, use `references/prompt-packet-review-checklist.md`.

### Dialogue-duration expansion rule

Do not force a full spoken thought into a short visual shot merely because the source shot list assigned dialogue to that beat. A 2-second shot can normally support only a brief phrase with readable performance; long lines become rushed, ignored, or unusable for lip sync.

Use a hybrid dispatch plan:
- retain the source visual shots as the composition/editorial backbone;
- add **dialogue carriers** only where a visible speaker needs enough time to perform a complete thought;
- make each carrier one speaker, one performance action, one camera idea, and a stated duration (usually 2.5–4 seconds; 6–10 seconds only for a genuine uninterrupted monologue);
- split long speeches at semantic cut points, then use reaction, insert, shadow, or walking coverage while off-screen dialogue continues in the final edit;
- preserve deliberately interrupted phrases (for example, a threat cut off mid-command) only when the interruption is narratively motivated;
- plan the final dialogue/foley mix separately from visual generation. Do not truncate scripted dialogue merely to fit a test clip.

In packet metadata and headers, distinguish `visualShotCount`, `dialogueCarrierCount`, and `totalGenerationUnits` so reviewers understand that the added carriers supplement—not replace—the storyboard.

## Version Management

### Color tags

- **Red** (`colorTag: "red"`) — DRAFT, not final, needs review
- **Green** (`colorTag: "green"`) — approved, ready for Seedance dispatch
- **Yellow** (`colorTag: "yellow"`) — superseded by a newer version

### Upload workflow

1. Generate the HTML file locally (e.g., `/tmp/seedance-prompts-expanded-direct-v4.html`)
2. Upload via `POST /api/projects/:slug/media` with `phase=storyboard`, `category=misc`, `sourceKind=manual`
3. Color it with `PATCH /api/projects/:slug/media/:assetId` `{"colorTag":"red"}` (draft) or `{"colorTag":"green"}` (ready)
4. For in-place overwrites (updating an existing **document** version), use `POST /api/projects/:slug/media/:assetId/replace` — this preserves the asset ID, URL, and attachments while updating content.
5. When a reviewer has already encountered stale browser/CDN content, or when replacing an **image** reference, publish a new immutable media asset under a new key/URL instead of relying on an in-place object overwrite. Attach the new asset, green-tag it if approved, update every packet reference binding to the new asset ID/public URL, and yellow-tag the superseded reference only after the new packet is verified. Never claim an old stable URL now represents a changed image merely because an origin fetch with a cache-busting query saw it.

### Metadata

Include in `metadataJson`:
- `workflow: "seedance-storyboard"`
- `artifactType: "seedance_prompt_html"`
- `version: "v4-draft"` or `"v4-ready"`
- `status: "draft"` or `"ready"`
- `color: "red"` or `"green"`
- `changes: [...]` — list of modifications from previous version

## Provenance Links in Prompt Packets

When a prompt packet is derived from project documents, make that provenance legible in the published HTML—not merely in the media asset metadata.

1. Resolve the canonical `publicUrl` for each primary source, normally the script and shot list.
2. Add a visible `Source material:` line near the packet header using standard HTML anchors (`<a href="…" target="_blank" rel="noopener">…</a>`).
3. Keep reference-image provenance in the existing reference manifest; do not duplicate every image link in the source-material line.
4. Preserve the packet's stable URL by replacing the existing document asset in place through `POST /api/projects/:slug/media/:assetId/replace`.
5. If the replace route is driven by `sourceUrl`, stage the revised HTML at a temporary R2 URL, call the authenticated replace route, then verify the *canonical packet URL* contains both human-readable source labels and their expected hrefs.
6. Record the link addition in `metadataJson.changes` without dropping the source asset IDs already present in metadata.

This creates an audit trail a reviewer can follow from a dispatch surface back to its narrative and shot-architecture sources.

## Resolving Canonical Reference Images

When building the reference manifest, resolve the canonical (green-approved) version of each `@imageN` from Athabasca's media API:

```bash
# List all assets with @image in the title
curl -sS "http://localhost:3000/api/projects/george/media" | python3 -c "
import sys,json
data=json.load(sys.stdin)
for a in data.get('assets',[]):
    if '@image' in a.get('title','').lower():
        print(f'{a[\"id\"]} | {a[\"title\"][:60]} | {a.get(\"color\",\"none\")} | {a[\"publicUrl\"]}')
"
```

**CRITICAL: Always verify `colorTag: "green"`** before including a reference image. Do NOT select an asset based on title matching alone — JP has multiple versions of each reference (v1, v2, v3, U1, U2, etc.) and only the green-approved one is canonical. Query the individual asset if unsure:

```bash
curl -sS "http://localhost:3000/api/media/asset_XXXXX" | python3 -c "import sys,json; d=json.load(sys.stdin); a=d.get('asset',{}); print(f'color: {a.get(\"colorTag\")}, title: {a.get(\"title\")}')"
```

If no green version exists for a given `@imageN`, ask JP which one to use rather than guessing.

## Iterative Audit Workflow

When JP asks to review and fix a Seedance prompt document:

1. **Assume local-first unless explicitly told to persist.** If JP asks for rewritten prompts inline in chat or asks for a v2 preview file, do not upload or replace the Athabasca asset unless he explicitly asks for that step.
2. **Preserve the existing document structure.** For preview-doc revision work, keep the same overall HTML format, reference-card layout, headers, and group structure; update the shot-copy inside the prompt blocks rather than reinventing the wrapper.
3. **For shot-copy passes, make the prompts stateless and dispatchable.** Add explicit dialogue, exact body actions, exact prop behavior, and visible cause/effect beats. Do not leave screenplay shorthand like "the ritual", "he follows the instruction", or "the words land" unexplained.
4. **Don't upload after each fix.** Accumulate changes locally in the temp file.
5. **Make changes one at a time when JP is auditing.** JP may review fixes incrementally.
6. **Do a full upload only after JP approves the complete audit or explicitly asks for persistence.**
7. Use `POST /api/projects/:slug/media/:assetId/replace` for the final in-place overwrite when persistence is requested.

This avoids creating multiple intermediate assets, preserves the preview-doc shape JP already approved, and keeps manual Seedance dispatch workflows lightweight.

## Prompt handoff to live dispatch

When JP pastes a prompt and wants it used for generation:

1. Preserve the user-supplied prompt text as-is unless there is an **egregious** mistake.
2. Replace internal Athabasca asset IDs embedded inline (for example `asset_...`) with the corresponding canonical `publicUrl` values before dispatch.
3. Keep the original `@imageN` / `@videoN` labels in the prompt body; only swap the asset identifiers to URLs.
4. If you detect an internal contradiction in the mapping (for example `@image1` is defined as Turbo but a later shot says "Dozer, matching @image1 exactly"), call it out explicitly as a compliance risk.
5. Do not silently rewrite the creative text for small stylistic reasons. Only correct the contradiction automatically when the user explicitly allows prompt fixes or when the mistake would obviously break identity/continuity.
6. When the preview doc's displayed reference set is lighter than the actual dispatch needs, expand the live dispatch ref set with any already-attached environment / authority anchors the scene clearly depends on (for example a stadium establishing shot or coach character sheet) and disclose that you did so. The dispatch payload should optimize for model compliance, not blindly mirror an under-specified preview card list.
7. If JP provides an additional room or environment angle specifically as a spatial anchor (for example, "reverse angle" or "for 360 spatial coverage"), preserve that note in the prompt body and include the asset in the dispatched reference set even if the original preview doc only showed the main hero angle. This is especially useful for bedroom/interior scenes where Seedance needs help maintaining continuous geography across multiple shots.

### Chained group extension dispatch

When JP wants Group B (or any later group) to continue from the previously generated group for continuity:

1. Use the prior group’s **persisted Athabasca `publicUrl`** as the continuation video reference; never chain from a local cache or an upstream temporary URL.
2. Keep the later group’s displayed image references in their original order and attach them alongside the video reference.
3. Dispatch through the normalized API with `mode: "reference-to-video"`, `referenceVideoUrls: [previousGroupPublicUrl]`, and the group’s ordered `referenceImageUrls`.
4. Change only the opening line when JP asks for that exact delta. The approved wording is: `I want you to extend video one and generate the following shots.` Preserve every remaining character of the published group prompt unless JP requests further edits.
5. Carry forward the same provider, model, duration, resolution, aspect ratio, and audio settings when the user says the continuation is otherwise identical.
6. Use a new idempotency key for the new group, but keep it stable across retries of that same group.
7. Record the previous video asset/URL in provenance, then verify the new asset, public URL, audio stream, and project attachment before reporting success.

This turns independent preview groups into a continuity chain without sacrificing the canonical identity and geography images.

See `references/chained-group-extension.md` for the normalized payload, proven BytePlus settings, persistence rules, and verification checklist.

### Reset after a contaminated extension

Do not keep chaining a rejected continuation when the prior video causes duplicated characters, mirrored or repeated room geography, or inherited design errors.

1. Remove `referenceVideoUrls` entirely and rerun from the approved text plus canonical images.
2. Treat exact user-specified asset IDs as overrides of stale reference cards.
3. Add explicit count and geography constraints: exactly one protagonist, one destination character, one continuous shelf/wall, one route between them.
4. State recurrent visual prohibitions directly, then specify the desired treatment positively—for example, flat graphic visor overlays rather than anatomical eyes, or a localized cool-blue badge light rather than a warm full-body glow.
5. Record in provenance that the generation is an images-only reset, not an extension.
6. Review for duplication, fixed geography, character identity, and effect color before presenting the result.

See `references/sequential-seedance-extension-and-reset.md` for the full reset recipe and verification checklist.

For the combined accepted-clip continuation vs rejected-clip recovery decision tree—including carrying a successful image-reference set forward and separating light-source ownership—see `references/seedance-multigroup-continuation-and-recovery.md`.

## Prompt-preservation overlays for existing packets

When a user asks to make a hybrid from an existing Seedance packet, treat the existing packet as the **semantic source of truth**. Preserve every model-facing shot field and its order: subject, action, dialogue/sound, composition, visual focus, emotion, and continuity note. Add a narrowly scoped overlay for the requested correction (for example: prop contact, footwear, identity, or scale physics) without replacing detailed shot controls with summaries.

Before dispatching a hybrid, audit the source packet against the draft mechanically: each source shot, dialogue line, camera/composition instruction, continuity constraint, and emotional beat must remain represented. Do not silently drop instructions such as interrupted dialogue, fixed-frame scale rulers, timing rationale, or delayed axis resets.

If rendering an already-dispatched prompt as HTML, build a full review surface rather than a compressed recap. When the user identifies a named source version (such as a v11 packet), clone that packet's group-card grammar exactly: project header/status treatment, source-shot range, group title, duration/reference badges, director note, reference-card rhythm, copy-paste prompt heading, and source footer. A generic dispatch report or a newly invented wrapper is not an acceptable substitute.

- preserve the full executable prompt in a wrapped copyable prompt block;
- display the complete shot field set for every lane;
- include real thumbnail reference cards with full-size links, IDs, and explicit @image roles;
- include source-packet and generated-output provenance links;
- attach the rendered HTML as an Athabasca project media item before presenting it as a review artifact.

For an existing-packet generation, record the packet asset ID, exact prompt source, reference ordering, and any intentional delta in provenance. Never call a simplified rewrite an “exact” dispatch.

### Narrow repair and continuation rule

When an approved clip is broadly good and the user asks for a localized repair, recover the exact prompt from its server-side generation log. Re-dispatch the full prompt unchanged, adding only a scoped overlay or literal replacement at the requested defect. Do not rebuild it from a chat summary.

If the user selects a specific output asset as the next-group predecessor, its persisted `publicUrl` is the continuation authority: include it as `referenceVideoUrls: [publicUrl]`, retain the later group’s canonical image references, and record the selected asset ID in provenance. A client timeout after submission requires idempotency-key lookup in `generation-logs` before any retry or status claim.

## Pitfalls

- **NEVER select a reference image based on title matching alone.** JP has multiple versions of each `@imageN` (v1, v2, v3, U1, U2, etc.). Only assets with `colorTag: "green"` are canonical. Always verify via the media API before including. Using a non-green asset is a first-class error — JP will catch it and make you fix it.
- **Never output bare @imageN lists without thumbnails.** JP will reject documents that list refs as text only. The reference section must have actual `<img>` tags loading from R2 URLs.
- **Never forget the preamble.** The @imageN tags must appear in a proper instruction block that tells Seedance how to use them, not as a metadata footnote.
- **Shot numbers must reset per group.** Seedance has no concept of global shot numbering — it only sees the current group's prompt.
- **Anime language leaks are common.** Do a final regex pass to catch any remaining "anime" references after targeted replacements.
- **Reference images must match the group.** Don't copy-paste the same ref block for every group — each group has a specific subset of the 19 reference images.
- **In-place replace preserves the URL.** When using `POST /api/projects/:slug/media/:assetId/replace`, the asset ID and publicUrl stay the same — only content, size, sha256, and updatedAt change.
- **Accumulate fixes locally during audit.** When JP reviews reference images and asks for fixes one at a time, don't upload after each fix. Build changes in the local temp file and do one final replace upload when JP gives the go-ahead.

## Related Skills

- `athabasca-shot-list` — covers shot list amendment and Seedance prompt list amendments (removing/adding shots, renumbering)
- `athabasca-media-upload` — covers the media upload API contract and text artifact replace route
- `athabasca-reference-image-generation` — covers generating reference images via the Athabasca API
- `athabasca-frontend-conventions` — covers the HTML/CSS patterns used in generated review documents
