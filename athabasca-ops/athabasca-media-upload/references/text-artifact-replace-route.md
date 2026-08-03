# Text Artifact Replace Route

Use when an Athabasca **project media asset already exists** and the user wants to update the underlying text/document artifact without creating a new asset row.

Route:
- `POST /api/projects/:slug/media/:assetId/replace`

Request:
- `multipart/form-data`
- exactly one of:
  - `file`
  - `sourceUrl`
- optional:
  - `title`
  - `provenanceNote`
  - `metadataJson`

Behavior:
- preserves:
  - `asset.id`
  - attachments
  - `storageKey`
  - `publicUrl`
- refreshes:
  - `contentType`
  - `sizeBytes`
  - `sha256`
  - `originalFilename`
  - `updatedAt`
- document-only guardrail:
  - current asset must have `kind=document`
  - replacement content must still infer `kind=document`

Recommended uses:
- HTML review docs
- Markdown research notes
- JSON manifests
- SVG diagrams
- XML/plain-text support artifacts

Do not use for:
- images
- video
- audio
- cases where the user wants a preserved checkpoint/history row instead of an in-place update

Decision rule:
1. If the artifact is not yet in Athabasca media, create it with `POST /api/projects/:slug/media`.
2. If it is a global/shared static asset with no project DB row, use the direct R2 stable-key path.
3. If it is an existing project-attached document asset and the user wants the same URL/asset to persist, use this replace route.

Verification:
- re-fetch the asset via `GET /api/media/:assetId`
- confirm unchanged `id` and `publicUrl`
- confirm updated `sha256` / `sizeBytes` / `contentType`
- for user-visible docs, fetch the public URL content and check concrete markers from the revised payload, not just a `200` or local file contents

## Practical pattern: in-place HTML prompt-preview cleanup

When editing an existing generated HTML review/prompt-preview page:
1. Download the current `asset.publicUrl` to a local staging file.
2. Make the minimal DOM/text edits locally, preserving the existing title, URL, and asset ID.
3. If reference cards are removed or added, update the copy-paste prompt blocks in the same file so `@imageN` cards and prompt text stay aligned. Renumber remaining references when this removes gaps unless the user explicitly wants stable numbering.
4. Use `POST /api/projects/:slug/media/:assetId/replace` with the edited file. Do not create a new media asset unless the user asks for a checkpoint/history copy.
5. Verify the remote URL body contains the expected new asset IDs/text and no longer contains removed prompt-reference lines.

### Ambiguity guard: prompt text near an HTML doc link

Do **not** infer that newly supplied prompt text should replace an existing HTML prompt-preview just because the conversation is near a doc-editing thread. If the user says a prompt was `generated manually`, mentions `mitte.ai`, or appears to be providing generation metadata for a video, first identify the media operation:
- existing/video asset attachment or upload with prompt stored in `generation`/`metadataJson`
- HTML prompt-preview edit
- new text artifact/checkpoint

If the requested mutation target is not explicit, ask before using the replace route. The replace route overwrites the existing document URL in place, so a wrong inference can delete recoverable prompt text from the public artifact.

   - the group badges/counts such as `3 refs` / `4 candidates`
   - the prompt definitions and shot text that refer to `@imageN` anchors, especially when a newly attached reference becomes the anchor for a specific shot
5. Use `POST /api/projects/:slug/media/:assetId/replace` with the edited file. Do not create a new media asset unless the user asks for a checkpoint/history copy.
6. Verify the remote URL body contains the expected new asset IDs/text and no longer contains removed prompt-reference lines.

Node/FormData one-off example from the repo root:
```js
const fs = require("fs");

(async () => {
  const base = process.env.ATHABASCA_BASE_URL || "http://localhost:3000";
  const token = process.env.ATHABASCA_API_TOKEN;
  const fd = new FormData();
  const filePath = "/tmp/revised-preview.html";

  fd.append(
    "file",
    new Blob([fs.readFileSync(filePath)], { type: "text/html;charset=utf-8" }),
    "revised-preview.html"
  );
  fd.append("provenanceNote", "In-place cleanup of generated prompt preview.");

  const res = await fetch(`${base}/api/projects/<slug>/media/<assetId>/replace`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: fd,
  });
  console.log(res.status, await res.text());
})();
```
