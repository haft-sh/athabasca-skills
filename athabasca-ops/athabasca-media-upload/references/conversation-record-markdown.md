# Conversation record Markdown artifacts

Use this reference when the user asks to preserve a Telegram/Hermes research conversation as a durable Athabasca artifact.

## Goal

Create a concise but useful `.md` record from the conversation, upload it through `POST /api/projects/:slug/media`, and attach it to the project (usually `phase=research`) so the R2 URL and Athabasca media asset become the durable reference.

## Recommended artifact shape

Include:
- project name/slug and artifact purpose
- creative brief and major user questions
- source-backed research synthesis
- script/beat decisions made in chat
- important caveats and uncertainty labels
- bibliography/source list if discussed
- existing project/report IDs only when they help cross-reference current Athabasca state

Avoid:
- raw full transcript dumps unless explicitly requested
- secrets, local-only paths, temporary command output, or unrelated tool logs
- treating the markdown file as canonical project state; it is supporting media, not the source of truth

## Upload fields

```bash
curl -sS -X POST "http://localhost:3000/api/projects/<slug>/media" \
  -F "file=@/tmp/<slug>-conversation-record.md;type=text/markdown; charset=utf-8" \
  -F "phase=research" \
  -F "category=research" \
  -F "sourceKind=generated" \
  -F "title=<Project> research conversation record" \
  -F "provenanceNote=Hermes-generated Markdown record of the research/script-development conversation, uploaded to R2 and attached to the project research phase." \
  -F 'metadataJson={"workflow":"conversation-record","artifactType":"research_conversation_markdown","projectSlug":"<slug>","source":"Telegram conversation with Hermes"}'
```

## Verification

1. Inspect the upload response and capture:
   - `asset.id`
   - `asset.publicUrl`
   - `asset.contentType`
   - `asset.attachments`
2. Re-fetch with `GET /api/media/:assetId` and confirm:
   - `phase` matches intended phase
   - `category` is valid (`research` for research support artifacts)
   - attachment exists when the user asked to attach it
   - `contentType` includes `charset=utf-8`
3. Verify the public R2 object with a ranged GET instead of relying only on HEAD:
   - Some R2/public URL configurations may return `403` for HEAD while `GET`/ranged `GET` works.
   - Use `Range: bytes=0-200` and confirm the first bytes decode as UTF-8 markdown.

## Reporting

Keep the user-facing confirmation terse:
- asset id
- phase/category
- R2 URL
- attachment target/role
- verification result
