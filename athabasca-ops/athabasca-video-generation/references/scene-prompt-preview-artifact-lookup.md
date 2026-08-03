# Scene prompt-preview artifact lookup

Use this when the user asks for a prompt-preview link for a specific project/act/scene before Seedance generation.

## Why

A prompt-preview request is usually a review workflow, not a generation request. The first job is to find or create the durable Athabasca artifact that the user can review, then stop until approval.

## Workflow

1. Resolve the project slug from the project name via `GET /api/projects` when needed.
2. Query `GET /api/projects/:slug/media` before creating anything new.
3. Filter for existing HTML/Markdown/document artifacts using title, tags, phase, category, source kind, content type, and metadata. Search likely terms:
   - `prompt preview`
   - `Seedance`
   - `Act 2 Scene 2`
   - scene slug/scene title if known
4. If an existing matching preview is found, share that link and state that nothing has been sent to Seedance.
5. If no matching preview exists, create a new durable prompt-preview artifact/report with:
   - scope assumptions
   - proposed provider/settings
   - clip-by-clip prompts
   - review questions
   - explicit “not yet generated” note
6. Attach/upload the new artifact through Athabasca project media/report APIs, then share the public link/title.
7. Do not submit `POST /api/projects/:slug/generate/video` until the user approves the preview or provides edits.

## Final response shape

```text
Prompt preview: [link]
Artifact: [title]
Status: Review only — nothing has been sent to Seedance yet.
```
