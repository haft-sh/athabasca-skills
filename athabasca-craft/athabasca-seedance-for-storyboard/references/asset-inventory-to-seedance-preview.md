# Asset Inventory → Seedance Prompt Preview

Use this when a Seedance prompt preview is built from an already-generated shot list plus an HTML asset inventory.

## Durable workflow pattern

1. Fetch the shot list markdown and parse each `## Shot NNN — Title` block into the verbose fields:
   - `Subject`
   - `Action`
   - `Composition`
   - `Visual focus`
   - `Emotion`
   - `Continuity note`
2. Fetch the asset inventory HTML and parse each shot row for:
   - shot number
   - anchor still image URL and asset id from the `Image` column
   - `Reuse map:` support asset ids from the item column
   - if the inventory HTML row markup has drifted or omits easy asset IDs, fall back to the project media API/list and resolve anchors by title/public URL patterns such as `A2S3 Shot 020 — ...`; do not block on a brittle table-row regex when the same anchor assets are already present in project media.
3. Group the shots into the requested Seedance generations. Default to the user's requested rhythm over a fixed shot count. If the user says the 15-shot / 1s cadence is too quick, use smaller lanes such as 7 shots × 2s (about 14s) and create as many lanes as needed. For two 15-second prompts on an 18-shot scene, a clean split is often 9 + 9 unless the dramatic beat suggests otherwise. When the user asks to process many scenes, still produce and verify prompt previews one scene at a time so source-selection, references, and format lessons do not drift across a large batch.
4. For each group, assign `@imageN` references in this order:
   - shared/supporting reuse-map assets first (characters, location, props)
   - then per-shot anchor stills
   This keeps identity/setting anchors visible before shot-specific compositions.
5. In the prompt text, explicitly declare every reference role before the shot list:
   - `@image1 = Hollow valley reference...`
   - `@image2 = character costume / wardrobe sheet...`
   - `@image7 = Anchor image — Shot 004...`
6. For each shot, preserve the source shot-list wording as much as possible, but wrap it in Seedance-friendly verbose fields and remove any non-visual project-history explanations:
   - `Anchor image: @imageN` only when the shot has a shortlisted reference; omit this line entirely for shots without a direct anchor
   - `Subject / Action:` source `Subject + Action`
   - `Camera:` source `Composition`
   - `Composition:` eye-trace, layer guidance, continuity/editability guidance, rewritten as direct visual instructions
   - `Lighting:` only when shot-specific; move scene-wide lighting/look/style into the group preamble
   - `Focus:` source `Visual focus`
   - `Emotion:` source `Emotion`
7. Do not use a separate `Prompt core` field when it duplicates the structured fields.
8. Do not append a separate `Shot Details` section after the copy-paste prompt. Integrate useful action/continuity guidance into the shot prompt itself.
9. Alternate angles/treatments must be inserted as new numbered shots with full fields. Do not write parenthetical language like `let Seedance find...`. For emotional-action scenes, deliberately add edit-friendly filler as first-class shots when it improves the lane rhythm: reaction close-ups, hand/prop inserts, atmospheric b-roll, scale cutaways, comic deflation beats, and light/shadow transition shots. These should preserve the sequence axis and eye trace while giving editors extra material to prune later.
10. Split image grids into:
   - `Reference Images`: the slim, actual Seedance attachment shortlist with `@imageN` labels that reset per group/lane.
   - `Candidate Images`: all generated stills for human editorial context/inspiration only, no `@imageN` captions.

## Missing inventory fallback

For film-wide continuation passes, the user usually values momentum over waiting for a perfect populated inventory. If the next scene has a shot list but no populated asset inventory in project media:

1. Search project media for the scene tag, prior I2V/prompt-preview HTML, Garden/Hollow/location plates, character references, hero prop references, and any scene-specific stills.
2. Use the shot list as the source of truth for numbered beats, then build 7-shot / 2s lanes as usual.
3. Promote existing canonical/reference assets into each lane's `Reference Images` shortlist (`@image1` etc.). If no per-shot anchor still exists, omit `Anchor image:` lines rather than inventing them.
4. Add first-class emotional cutaways/inserts/b-roll to fill the rhythm and improve editability, guided by layout/coverage principles.
5. Record the missing inventory explicitly in the local manifest and final report, including which substitute sources were used.
6. Keep verification identical to inventory-backed previews: prompt count, 7 shots per prompt, local `@imageN` refs, scene tag, `No Music`, 2s duration, and absence of known-bad strings.

## Athabasca API resolution note

When Athabasca auth is active, local API calls for media details require `Authorization: Bearer $ATHABASCA_API_TOKEN`. Use the API to resolve supporting reuse-map asset ids to their canonical `publicUrl`, `title`, and color tag. The anchor still URL is usually already present in the inventory HTML, but support assets often need API lookup.

## HTML expectations

The preview should include:

- visible scene tag (for example `A2S1` / `A2S2`) in title, metadata, body, and Athabasca media tags when requested
- no inline `DRAFT` banner unless the user explicitly asks for visible draft status; use media metadata (`colorTag`, `ratingStars`, tags) for draft/review state
- per-group reference grids with inline thumbnails, `@imageN`, title, description/note, and asset id
- copy-paste-ready Seedance prompt blocks
- no separate post-prompt shot-detail section unless the user asks for audit tables; integrate important shot detail into the prompt itself
- no reference manifest by default when per-group reference grids already expose the `@imageN` mapping
- continuity anchors across the generations

## Upload expectations

- Stage under `~/.hermes/staging/<project-slug>/`, not `/tmp`.
- Store any reusable generator script in the repo `scripts/` directory.
- Upload through `POST /api/projects/:slug/media` with `phase=storyboard`, `category=generated`, and `sourceKind=generated`.
- For draft previews, immediately PATCH the returned asset with `colorTag: "red"` and useful tags such as the scene tag, `seedance`, and `prompt-preview`.
- Verify the remote URL with a real GET and marker checks for the scene tag, group headings, prompt count, per-prompt shot counts, representative `@imageN` values, and absence of known-bad strings (`Reference Image Manifest` when omitted, `bright green` if false, agent-facing meta-instructions, or unintended live-action camera-language in an animated prompt set).
