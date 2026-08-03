# GPT Image 2 single-grid generation

Use this note when the user asks for GPT Image 2 to make a `3x3 grid`, `contact sheet`, `grid of candidates`, or to `fit prompts into a grid`.

## User-intent rule

For the user, a GPT Image 2 3x3-grid request means: **one GPT Image 2 generation that composes the full 3x3 grid image directly**.

Do **not** interpret it as:
1. generate nine separate images, then
2. download them, tile them locally, and
3. upload the assembled contact sheet.

That assembled-tile workflow is only appropriate if the user explicitly asks for a contact sheet from already-generated images.

## Prompt pattern

Submit a single project-scoped image generation request:

```json
{
  "provider": "openai-codex",
  "model": "gpt-image-2",
  "aspectRatio": "landscape",
  "referenceAssetIds": ["asset_base_or_character", "asset_style_or_environment"],
  "prompt": "Create one 3x3 grid/contact sheet image. Each panel is a distinct cinematic composition variation..."
}
```

In the prompt, specify:
- one coherent output image containing a 3x3 grid
- exactly nine panels
- each panel should be separated by thin gutters or clear visual boundaries
- each panel gets one brief composition instruction
- shared character/reference/style constraints apply to all panels
- no text labels unless the user asks for labels

## When to assemble locally instead

Only assemble tiles manually when:
- the images already exist and the user asks for a review contact sheet
- the model output needs comparison after separate provider/model runs
- the task is asset inventory/review UX, not generation

## Provenance note

Make provenance explicit:

```text
Single GPT Image 2 3x3 grid generation using [reference assets]; prompts/panel directions derived from [prompt set].
```

If a local contact sheet was assembled from separate generations, do not describe it as a GPT Image 2 grid generation; call it an assembled contact sheet.
