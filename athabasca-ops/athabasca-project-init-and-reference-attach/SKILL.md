---
name: athabasca-project-init-and-reference-attach
description: Create a new Athabasca project through the live API, verify the contract from OpenAPI, and attach an initial user-supplied reference image as project media.
triggers:
  - User wants to start a new Athabasca project from chat
  - User provides an image to use as a character/style/reference anchor for a new project
  - Need to seed initial project data and persist inbound media via Athabasca APIs
version: 1.0.0
---

# Athabasca project init + reference attach

Use this when a user starts a brand new Athabasca project in chat and has already provided enough initial project detail to create the project record. This workflow is specifically for creating the project through Athabasca's API (not by editing DB/files directly) and then persisting the supplied reference image through the media API so the DB remains the system of record.

## Why this exists

A few Athabasca conventions matter here:
- Project state must be mutated via API endpoints, not by editing DB rows or repo files directly.
- Uploaded/reference media should go through `POST /api/projects/:slug/media` so the file lands in R2 and the DB stores the resulting `publicUrl` + provenance.
- The live OpenAPI contract is the source of truth for exact payload shape/defaultable fields.

## Steps

1. Confirm the local Athabasca API is reachable.
   - Example:
     - `curl -sS http://localhost:3000/api/health`

2. Normalize the intake fields from the current project API contract.
   - Minimum semantic inputs: `name`, `shortDescription`, `objective`, `audience`
   - Useful recommendations: `runtimeTargetSeconds`, `aspectRatios`, `targetPlatforms`, `primaryCta`

3. Check the live API contract before posting.
   - Fetch `http://localhost:3000/api/openapi/json`
   - Inspect `paths['/api/projects']['post']`
   - This is important because some fields are technically optional in the schema even if they are operationally useful.

4. Create the project via `POST /api/projects`.
   - Use a JSON body.
   - Do not include deprecated project-level generation provider/model defaults. Generation requests choose `provider` and `model` explicitly at call time.
   - Avoid seeding phase-gated workflow state unless the live schema still requires a compatibility field.

5. Capture the returned identifiers.
   - Save/use at least:
     - `project.id`
     - `project.slug`

6. If the user supplied a reference image, upload it through `POST /api/projects/:slug/media` using multipart form data.
   - Required ingest rule: provide exactly one of `file` or `sourceUrl`.
   - Recommended fields for an initial character/style reference:
     - `phase=visual_dev` when useful as an organizational tag
     - `category=moodboard`
     - `sourceKind=telegram_upload` (or the relevant source kind)
     - `title`
     - `provenanceNote`
     - `attachment` JSON with:
       - `targetType=project`
       - `targetId=<project.id>`
       - `role=character_reference` (or similar)
       - `sortOrder`
       - `metadataJson`

7. Return the created project summary and the uploaded asset URL/ID to the user.
   - Be explicit about any assumptions you made for missing init fields.

## Concrete examples

### Create project

```bash
python - <<'PY'
import json, urllib.request
payload = {
  "name": "Loisirs",
  "shortDescription": "A high-end 30-second lifestyle commercial for a black women's golf umbrella.",
  "objective": "Create a premium, fashion-forward commercial that positions the product as a luxury lifestyle object.",
  "audience": "Style-conscious women and premium lifestyle consumers.",
  "runtimeTargetSeconds": 30,
  "aspectRatios": "16:9",
  "targetPlatforms": "web,social,brand",
  "primaryCta": "Discover the product.",
  "workflowProfile": "intermediate",
  "latestApprovalState": None,
}
req = urllib.request.Request(
    'http://localhost:3000/api/projects',
    data=json.dumps(payload).encode(),
    headers={'Content-Type': 'application/json'},
    method='POST'
)
with urllib.request.urlopen(req) as resp:
    print(resp.read().decode())
PY
```

### Attach local reference image

```bash
curl -sS -X POST http://localhost:3000/api/projects/<slug>/media \
  -F 'file=@/absolute/path/to/reference.jpg;type=image/jpeg' \
  -F 'phase=visual_dev' \
  -F 'category=moodboard' \
  -F 'sourceKind=telegram_upload' \
  -F 'title=Primary character reference' \
  -F 'provenanceNote=User-supplied character reference from chat.' \
  -F 'attachment={"targetType":"project","targetId":"<project_id>","role":"character_reference","sortOrder":0,"metadataJson":"{\"source\":\"telegram\"}"};type=application/json'
```

## Pitfalls

- Do not write directly to `data/athabasca.db`; use the API.
- Do not store local file paths as canonical project state; the media API uploads to R2 and returns the canonical `publicUrl`.
- Check the OpenAPI schema before posting; Athabasca payload details evolve.
- `projectMediaUploadBodySchema` enforces exactly one of `file` or `sourceUrl`.
- If persisting the initial brief with a helper script that can be rerun, make source creation idempotent. Upsert/update the project report freely, but check for an existing matching source URL/title before inserting a new `research_source`; otherwise retries create duplicate source rows that need manual cleanup.
- If using Telegram/media cached files, pass the local cached file path in multipart upload; once uploaded, report the returned `publicUrl`, not the temp cache path.
- For text-only brief scripts, remember that report upsert helpers can be idempotent while source creation usually is not. If you rerun the script after adding a note, verify and remove/avoid duplicate research source rows before telling the user persistence is complete.
- If the user has said some variation of "don't populate the DB for now", "conversation only", or otherwise asked to avoid persistence, treat that as a standing no-write constraint until the user explicitly rescinds it. Do not infer that a later phrase like "attach these to the project" automatically overrides the earlier no-write instruction; clarify or restate the constraint before uploading.
- When preparing visual references for later attachment, it is useful to pre-classify them in conversation with tentative media tag/phase, `category`, `role`, `title`, and `provenanceNote` so they can be persisted quickly once the user gives an explicit go-ahead.

## Text-only brief persistence

When the user starts a project with a substantial chat brief but no uploaded media, still persist the full brief as durable project state instead of only filling top-level `shortDescription` / `objective` fields.

- Prefer a phase report with `phase: "init"`, title like `Initial Project Brief`, and the user's structure preserved.
- Record supplied source URLs (YouTube track, article, reference page) as research sources, but make that step idempotent: check existing sources first or dedupe after verification.
- Verify via `GET /api/projects/:slug` that the init report exists and that the source URL appears only once.
- If the live OpenAPI contract does not expose the report-write endpoint, see `references/text-only-brief-report-persistence.md` for the narrow repo-local fallback using existing bootstrap helpers rather than hand-editing DB rows.

## Educational explainer research/script kickoff

When the user starts a project and immediately asks for substantive research plus a rough educational script, treat it as a combined init → research → script kickoff rather than stopping at the project container:

- Create the project via the API first.
- Log research sources before synthesis.
- Create durable research insights for the explanatory arc, misconception corrections, and production implications.
- Write the research synthesis as a `phase: "research"` report.
- Write the explainer draft separately as a `phase: "script"` report.
- Verify both reports exist before telling the user the script was persisted.

See `references/educational-explainer-research-to-script.md` for the validated pattern and verification snippet.

## Verification

- `GET /api/projects` or inspect the POST response to confirm the project exists.
- Confirm the returned project slug/current phase match expectations.
- Confirm the media upload response includes:
  - `asset.id`
  - `publicUrl`
  - attachment role/target
- Tell the user what assumptions were made during project init so they can correct them early.
