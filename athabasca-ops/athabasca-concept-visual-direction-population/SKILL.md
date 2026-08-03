---
name: athabasca-concept-visual-direction-population
description: Populate Athabasca concept and visual-development records for an existing project by writing concept brainstorm/final docs, concept + visual_dev reports, and a visual direction via the live API.
triggers:
  - User wants an Athabasca project's concept and visual direction populated from a chat brief
  - Need to turn a commercial/story idea into canonical Athabasca concept + visual_dev backend records
  - Existing project already exists and needs downstream concept artifacts
version: 1.0.0
---

# Athabasca concept + visual-direction population

Use this when a project already exists in Athabasca and the user has described a concept/visual direction in chat. The goal is to translate that brief into the canonical concept and visual-development artifacts through the API, not by editing DB/files directly.

## Why this exists

Athabasca concept and visual-development work should be stored as distinct durable artifacts/media records:
- Concept phase wants:
  - brainstorm concept route doc
  - final concept route doc
  - concept-phase report
- Visual development wants:
  - at least one visual direction record
  - visual_dev phase report
  - durable media references stored through the media layer

The live OpenAPI contract is generally reliable for payload shape, but there is one important experiential caveat documented below.

## Steps

1. Verify the server is up.
   - Example: `curl -sS http://localhost:3000/api/health`

2. Check the live project/API contract and existing project artifacts before writing.

3. Confirm the live contract from OpenAPI.
   - Inspect:
     - `paths['/api/projects/{slug}/concept-routes']['post']`
     - `paths['/api/projects/{slug}/visual-directions']['post']`
     - `paths['/api/projects/{slug}/research-report']['post']`

4. If the user supplied a near-complete script or beat sheet in chat, record that source before writing concept artifacts.
   - Create a `research-source` with `sourceType: "note"` (or the closest truthful source type) describing the chat-delivered script/scene text.
   - Create a `source-excerpt` containing the canonical script or beat text, usually with:
     - `reportPhase: "research"`
     - `excerptType: "primary_text"`
     - a citation/note making it explicit that the text came from user chat intake
   - Write a lightweight `research` report explaining that this is a source-supplied/provisional kickoff rather than an external research pass.
   - This preserves provenance and gives downstream concept/shot-list work a truthful canonical source, even when the user wants to jump straight to concept or shot list.

5. Write the concept brainstorm doc.
   - Endpoint: `POST /api/projects/:slug/concept-routes`
   - Payload:
     - `kind: "brainstorm"`
     - `contentMarkdown`: 3–5 routes, each with rationale/pros/risks

5. Write the final concept route.
   - Endpoint: `POST /api/projects/:slug/concept-routes`
   - Payload:
     - `kind: "final"`
     - `contentMarkdown`: chosen route as source of truth

6. Write the concept report.
   - Endpoint: `POST /api/projects/:slug/research-report`
   - Payload:
     - `phase: "concept"`
     - `title`
     - `summary`
     - `contentMarkdown`
     - `images`: include retained reference URLs when they materially help the report
   - Make an explicit recommendation; do not leave the route undecided.

7. Create a visual direction record.
   - Endpoint: `POST /api/projects/:slug/visual-directions`
   - Payload:
     - `name`
     - `description`
     - `inspirationNotes`
     - `sortOrder`

8. Write the visual development report.
   - Endpoint: `POST /api/projects/:slug/research-report`
   - Payload:
     - `phase: "visual_dev"`
     - `title`
     - `summary`
     - `contentMarkdown`
     - `images`: include retained reference URLs when they materially help the report

9. Verify the project detail and media inventory.
   - `GET /api/projects/:slug`
   - `GET /api/projects/:slug/media?phase=visual_dev`
   - Confirm:
     - concept docs include `brainstorm` and `final`
     - reports include `concept` and `visual_dev`
     - visual direction exists
     - existing reference media is still present

## Recommended content structure

### Brainstorm doc
Include 3–5 routes with:
- route name
- one-paragraph premise
- pros
- risks
- explicit recommendation

### Final concept route
Keep it short and decisive:
- premise
- protagonist/product relationship
- emotional center
- tonal rules

### Concept report
Should explain:
- why the chosen route won
- strategic fit for brand/product/runtime
- key beats
- key risks
- what still needs research or approval

### Visual direction record + report
Capture:
- character silhouette/hair/wardrobe
- environment and palette
- material language
- camera/composition cues
- continuity constraints
- explicit "do not drift into" risks

## Concrete example flow

```bash
python - <<'PY'
import json, urllib.request

base = 'http://localhost:3000'
slug = 'loisirs'

def post(path, payload):
    req = urllib.request.Request(
        base + path,
        data=json.dumps(payload).encode(),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(req) as resp:
        print(resp.read().decode())

post(f'/api/projects/{slug}/concept-routes', {
  'kind': 'brainstorm',
  'contentMarkdown': '# Brainstorm ...',
})

post(f'/api/projects/{slug}/concept-routes', {
  'kind': 'final',
  'contentMarkdown': '# Final concept ...',
})

post(f'/api/projects/{slug}/research-report', {
  'phase': 'concept',
  'title': 'Concept recommendation',
  'summary': 'Why the selected route wins.',
  'contentMarkdown': '# Concept report ...',
  'images': [],
})

post(f'/api/projects/{slug}/visual-directions', {
  'name': 'Luxury Shelter / Urban Threshold',
  'description': 'Short visual thesis.',
  'inspirationNotes': 'Longer notes.',
  'sortOrder': 0,
})

post(f'/api/projects/{slug}/research-report', {
  'phase': 'visual_dev',
  'title': 'Visual territory draft',
  'summary': 'Visual direction summary.',
  'contentMarkdown': '# Visual report ...',
  'images': [],
})
PY
```

## Linked references

- `references/canonical-asset-management.md` — Convention for marking visual assets as canonical (green colorTag = official reference), API endpoints for colorTag/ratingStars/tags, PATCH limitations, review-first discipline, superseded workflow.

## Visual Development Review Workflow

When the user asks to review visual development assets (locations, characters, props):

### Priority order for locking canonicals
1. **Hero props** first (recurring objects like the typewriter — these appear in many shots)
2. **Locations** next (writing room, living room, kitchen, hallway)
3. **Characters** (if not already locked)
4. **Detail/insert shots** last (close-ups of specific props, phone screens, etc.)

### Review queue rules
- **Review existing assets first.** Do not generate new images during a review queue unless the user explicitly asks.
- **Show one asset at a time** with its URL delivered as native media (not a link).
- **Skip already-canonical assets** (green-tagged) unless the user asks to revisit.
- **Skip non-generated assets** (moodboard photos, external references) — only generated images are canonical candidates.
- After the full review queue, ask the user what needs iteration before generating anything new.

### Iterative refinement pattern
When the user approves a direction but wants corrections:
1. Generate a new MJ grid and/or GPT Image 2 version with the corrected prompt
2. Show comparison (MJ grid as native media + GPT single image)
3. If the user picks an MJ quadrant, upscale it via Discord interactions
4. If the user wants edits to a specific result, use GPT Image 2 edit with `referenceAssetIds` (or Hermes `image_generate` with `reference_images` if Codex is available)
5. When the refined version is approved, mark it 🟢 green and mark superseded versions 🟡 yellow

## Pitfalls / experiential findings

- Do not mutate Athabasca state directly in the DB; use the API.
- Keep the recommendation explicit. The concept phase expects a chosen route, not just brainstorming.
- Preserve provenance language when the concept is based on user brief + uploaded references rather than a completed research pass.
- Current learned behavior: `POST /api/projects/:slug/research-report` can safely include non-empty `images` arrays, including image URLs that already exist in the same project's media library. This used to 500 because `media_assets.public_url` had a uniqueness constraint; that constraint was removed and a regression test was added.
- If this flow starts 500ing on an older checkout, inspect whether the local DB still has the stale `media_assets_public_url_unique` index. Symptom: insert into `media_assets` fails when a report image reuses an already-ingested URL.
- Prefer durable references to be ingested first through `POST /api/projects/:slug/media`, then reused in report `images` payloads so the media layer remains canonical and reports can embed the same URLs.
- After writing artifacts, verify with `GET /api/projects/:slug` and `GET /api/projects/:slug/media?phase=visual_dev` (and `?phase=concept` if you embedded concept references) rather than assuming the writes surfaced correctly in the detail view.

## Verification checklist

- Project detail includes both concept route docs.
- Project detail includes concept and visual_dev reports.
- Visual direction record exists with expected name/notes.
- Any uploaded visual reference is still available through the media endpoint.
- User is told which parts are provisional versus approved.
