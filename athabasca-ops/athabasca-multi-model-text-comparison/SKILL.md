---
name: athabasca-multi-model-text-comparison
description: Run the same text prompt across multiple LLMs for an Athabasca project, persist each model output as R2-backed project media, and synthesize the results into Research records.
version: 1.1.0
author: Hermes Agent (Athabasca)
metadata:
  hermes:
    tags: [athabasca, llm-comparison, research, r2, hermes-python-library, provenance]
    related_skills: [athabasca-media-upload, athabasca-project-init-and-reference-attach]
triggers:
  - User wants to compare multiple LLMs on the same writing or ideation prompt
  - Need provider/model provenance and per-model markdown artifacts
  - Need to persist comparison findings into an Athabasca project research report
---

# Athabasca Multi-Model Text Comparison

## Trigger

Use this when the user asks to:
- compare writing, ideation, critique, script, outline, or prompt responses across multiple LLMs
- ask several models the same prompt and persist the results in an Athabasca project
- run a "model bakeoff" or "multi-model text prompt" for Research/Concept/Script support

Always load and follow `athabasca-media-upload` with this skill. That skill is the persistence primitive for generated `.md`, `.txt`, and `.json` artifacts.

## Core Rules

1. Use Athabasca APIs for project/research/media state. Do not write directly to `data/athabasca.db`.
2. Use Hermes as a Python library (`AIAgent`) for repeatable text-to-text comparisons when possible. Prefer this over shelling out to `hermes chat -q`.
3. Disable tools, memory, and context for comparison agents unless the user explicitly asks for tool-using model responses.
4. Ask every model the exact same user prompt and shared system prompt.
5. Persist every model output to Cloudflare R2 via `POST /api/projects/:slug/media`.
6. The Research report is the synthesis. Individual model outputs are supporting media artifacts, not local tmp files and not just pasted into the report.
7. Do not stage artifacts in `/tmp` unless the user explicitly requests `/tmp`. Use a private non-canonical staging directory under `~/.hermes/work/athabasca/<project-slug>/multi-model-text/<timestamp>/`, upload immediately, then optionally delete local staging after verification.
8. Store only returned `asset.publicUrl` values in Athabasca Research records/report content. Local staging paths are provenance/debug details only and must not be canonical.

## Script

Repo utility:
- `scripts/run_multi_model_text_compare.py`

Normal usage requires a project slug so artifacts are uploaded through Athabasca media and stored in R2:
```bash
cd ~/.hermes/hermes-agent
source venv/bin/activate
python /home/nrsimha/Sites/athabasca/scripts/run_multi_model_text_compare.py \
  --project-slug womb-rental \
  --prompt-file /path/to/prompt.txt
```

Defaults:
- local staging: `~/.hermes/work/athabasca/<project-slug>/multi-model-text/<timestamp>/`
- API: `http://localhost:3000`
- upload: enabled
- `/tmp`: refused unless `--allow-tmp` is passed explicitly

Useful options:
- `--only <slug>` runs one model from the matrix, repeatable for multiple models
- `--runs-json <path>` supplies a custom model matrix
- `--output-dir <path>` overrides staging, but still refuses `/tmp` by default
- `--cleanup-local` removes the staging directory after successful upload
- `--skip-upload` is for local development tests only, not normal Athabasca use

## Recommended Workflow

### 1. Resolve or create project

If the project does not exist, create it with `POST /api/projects` following `athabasca-project-init-and-reference-attach` and the Init playbook.

For a comparison/ideation pass, usually set:
- `currentPhase`: `research`
- `phaseStatuses.research`: `drafted`
- `workflowProfile`: `advanced` unless the user asked otherwise

Verify:
```bash
curl -sS http://localhost:3000/api/health
curl -sS http://localhost:3000/api/projects
```

### 2. Probe providers/models before the expensive run

Check Hermes status/auth:
```bash
hermes status --all
hermes auth list
```

For OpenRouter, prefer the live model list. Use a local script that reads configured Hermes/OpenRouter credentials from the current runtime or Hermes provider helpers. Do not print or store API keys. Filter stdout to model IDs and provider metadata only.

If requested providers are unavailable, use the user-approved fallback pattern from the request (e.g. Gemini direct -> OpenRouter). Record the fallback reason in every artifact.

### 3. Use Hermes Python library, not `hermes chat -q`

Run from the Hermes Agent repo venv so imports and provider auth work:
```bash
cd ~/.hermes/hermes-agent
source venv/bin/activate
```

Minimal AIAgent pattern:
```python
from run_agent import AIAgent

DISABLED_TOOLSETS = [
    'web', 'browser', 'terminal', 'file', 'code_execution', 'vision',
    'image_gen', 'tts', 'skills', 'todo', 'memory', 'session_search',
    'clarify', 'delegation', 'cronjob', 'messaging', 'moa', 'rl',
    'homeassistant',
]

agent = AIAgent(
    model='anthropic/claude-opus-4.6',
    provider='openrouter',
    quiet_mode=True,
    disabled_toolsets=DISABLED_TOOLSETS,
    skip_memory=True,
    skip_context_files=True,
)
result = agent.run_conversation(
    user_message=prompt_text,
    system_message='You are a helpful assistant.',
)
response_text = result['final_response'].strip()
```

Why this route:
- avoids CLI spinners/reasoning noise in output files
- allows disabling memory/context for fairer comparisons
- makes provider/model/fallback metadata explicit
- easier to wrap into a reusable Athabasca workflow

Use `hermes chat -q` only as a diagnostic fallback if the library path breaks.

### 4. Stage locally outside `/tmp`

Create a staging directory outside `/tmp`:
```python
from datetime import datetime, timezone
from pathlib import Path
run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
stage_dir = Path.home() / '.hermes' / 'work' / 'athabasca' / project_slug / 'multi-model-text' / run_id
stage_dir.mkdir(parents=True, exist_ok=True)
```

Write each response as markdown:
```markdown
# <Model Label>

- Requested provider: ...
- Requested model: ...
- Actual provider: ...
- Actual model: ...
- Fallback reason: ...
- Generated at: ...

## Response

<model output>
```

Also write a `manifest.json` and `comparison-summary.md` in the staging dir for upload.

### 5. Upload every artifact to R2-backed Athabasca media

For each `.md`, `.txt`, or `.json` artifact, call `POST /api/projects/:slug/media` as multipart form data.

Recommended fields:
- `phase=research`
- `category=research`
- `sourceKind=generated`
- `title=<Project> multi-model comparison - <model label>`
- `provenanceNote=Generated by Hermes Python-library multi-model text comparison and uploaded to R2-backed Athabasca media.`
- `metadataJson` with workflow/run details
- `generation` with provider/model/prompt details when available

Parse response and save:
- `asset.id`
- `asset.publicUrl`
- `asset.sha256`
- `asset.storageKey`

These URLs become the canonical artifact links.

### 6. Create Research sources for each uploaded model output

After upload, create a research source per model response:
```json
{
  "sourceType": "note",
  "title": "Model response: Claude Opus 4.6",
  "publisher": "openrouter | anthropic/claude-opus-4.6",
  "url": "<asset.publicUrl>",
  "summary": "Brief excerpt or one-sentence characterization of the output.",
  "notes": "Requested provider/model, actual provider/model, fallback reason, asset id, sha256."
}
```

Also create one source for:
- the original prompt, uploaded as a text/markdown artifact
- the aggregate manifest/summary, uploaded as artifacts
- external source links referenced in the prompt, if any

### 7. Create structured Research insights

Extract 3-7 cross-model insights. Good `insightType` choices:
- `messaging`
- `narrative_arc`
- `visual`
- `risk`
- `constraint`
- `other`

Each insight needs:
- `title`
- `insight`
- `evidence` that cites the model outputs/source URLs
- `implications`
- `priority` 1-5

### 8. Create or update the Research report

Use `POST /api/projects/:slug/research-report`.

The report should synthesize, not dump raw outputs. Include:
- method
- provider/model matrix
- artifact URL table using `asset.publicUrl`
- fallback notes
- high-confidence convergence/divergence
- recommended next phase action

Do not paste all model responses into the report unless the user asks. Link to the R2-backed artifacts.

### 9. Verify

Verify media upload:
```bash
curl -sS "http://localhost:3000/api/projects/${SLUG}/media?phase=research"
```

Verify research records:
```bash
curl -sS "http://localhost:3000/api/projects/${SLUG}/research-sources"
curl -sS "http://localhost:3000/api/projects/${SLUG}/research-insights"
```

### 10. Cleanup local staging

After upload and verification, local staging is optional. Default behavior:
- keep only if the user asked for local filesystem copies
- otherwise delete local staging or leave it only under `~/.hermes/work/...` with a short note that R2 public URLs are canonical
- never use `/tmp` unless explicitly requested

## Provider Mapping Lessons From Womb Rental

Observed working mappings in April 2026:
- ChatGPT 5.4: `provider=openai-codex`, `model=gpt-5.4`
- Claude Opus 4.6: `provider=openrouter`, `model=anthropic/claude-opus-4.6`
- Gemini 3.1 fallback: `provider=openrouter`, `model=google/gemini-3.1-pro-preview`
- Kimi 2.6 fallback: `provider=openrouter`, `model=moonshotai/kimi-k2.6`
- Grok requested 4.3/4.2 fallback: live OpenRouter exposed `x-ai/grok-4.20` as the closest available match

Do not assume these remain current. Probe live model availability before running.

## Pitfalls

- `hermes chat -q` can include reasoning panes, session IDs, warnings, and shell noise. Prefer Python library for clean outputs.
- Long model runs can exceed foreground timeouts if run serially. Run per-model or use background/process management; write incremental artifacts after each model.
- Do not rely on `/api/projects/:slug/research-report` for artifact storage. It upserts the synthesis report; raw outputs belong in media assets and research sources.
- Do not store `~/.hermes/work/...` paths as canonical state. Use R2 `asset.publicUrl`.
- Avoid attaching local tmp paths in reports; if a path is useful for debugging, put it in local-only notes, not canonical report content.
- OpenRouter model IDs evolve. Use live model discovery for exact IDs.
- Provider auth can silently drift. Record fallback reasons clearly.

## Completion Response Template

When done, report:
- project slug
- number of model runs
- actual provider/model matrix and fallback notes
- number of uploaded media assets and their public URLs or a path to the uploaded-artifact table in the report
- research source/insight/report counts
- whether local staging was deleted or where it remains if retained
