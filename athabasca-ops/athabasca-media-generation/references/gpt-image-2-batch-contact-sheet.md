# GPT Image 2 Batch Contact Sheet Pattern

Use this when the user asks to run a set of still-image prompts through GPT Image 2 and present the results as a grid/contact sheet.

## Pattern

1. Resolve every supplied `asset_...` reference through `GET /api/media/:assetId` first.
2. Submit each still through `POST /api/projects/:slug/generate/image` with:
   - `provider: "openai-codex"`
   - `model: "gpt-image-2"`
   - `aspectRatio: "landscape"` / `square` / `portrait` as appropriate
   - `referenceAssetIds` in the requested continuity order
   - concise title including the batch index and prompt title
   - provenance naming the source references and prompt-set skill when applicable
3. Batch in small parallel waves when useful; GPT Image 2 calls often take ~2-3 minutes.
4. Verify each returned asset before using it in a contact sheet:
   - `GET /api/media/:assetId` succeeds
   - `asset.publicUrl` downloads successfully
   - if either lookup/download fails, retry that prompt once rather than building the sheet from a broken asset
5. If the user asks for 3x3 and you have 10 prompts, discard the least useful/riskier/most redundant prompt. Reflection-heavy concepts are often a reasonable discard because they are visually interesting but can harm character continuity.
6. Build a local 3x3 contact sheet only after all nine image URLs are verified. Label each tile with compact prompt number/title.
7. Persist the contact sheet through `POST /api/projects/:slug/media`, not just a local file. Store `metadataJson.sourceAssetIds`, `referenceAssetIds`, provider/model, workflow, and the discarded prompt.
8. Verify the uploaded grid via `GET /api/media/:assetId` and a ranged GET/download of the public URL before reporting completion.

## Pitfalls

- Do not treat a created generation response as enough for downstream grids; public object availability and media lookup can still fail for an individual asset.
- Do not memorialize transient Codex empty results as a permanent provider limitation. The durable lesson is: retry the affected prompt once, preferably with a slightly simplified prompt.
- If Python `urllib` gets a 403 from R2/remote media, use `curl -L` with a browser-like user-agent for downloads before concluding the URL is unusable.
