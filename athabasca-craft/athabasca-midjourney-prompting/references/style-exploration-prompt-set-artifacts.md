# Style exploration prompt-set artifacts

Use this pattern when the user asks for many text-only Midjourney prompts exploring the same scene across different visual treatments.

## When it applies

- User asks for 10+ prompts, permutations, or “go crazy” style exploration.
- Same base scene/composition should remain stable while style varies.
- Output should be saved as a durable `.md` artifact and shared by R2 link.

## Prompt-set structure

1. Start the Markdown with project, scene, use, and format.
2. Include brief prompting notes:
   - target model/version, usually `--v 8.1`
   - aspect ratio, usually `--ar 16:9` for cinematic frames
   - text-only/no image references if requested
   - tuning knobs for `--s` and `--c`
3. Keep each prompt paste-ready in a fenced `text` code block.
4. Label variants by visual direction, not just numbers:
   - `Norstein mist-memory cutout`
   - `Karel Zeman engraved fantasy adventure`
   - `Monochrome ink wash fever dream`
5. Preserve the same core composition in every prompt, then vary only style, palette, medium, region/tradition, and emotional temperature.
6. If the user asks for artist/style diversity, aim for a deliberate mix:
   - a few named artist inspirations
   - regional/traditional visual languages
   - modern graphic treatments
   - monochrome and high-color extremes
   - at least one hybrid of the strongest user-preferred references
7. End with a recommended first batch of 4–6 prompts and concise tuning notes.

## Upload/persistence

- Save locally under `artifacts/<project>-<scene>-mj-style-prompts.md`.
- Upload/attach the Markdown to the project as a document artifact, usually:
  - `phase=visual_dev`
  - `category=research`
  - `sourceKind=generated`
  - `metadataJson.artifactKind="midjourney_prompt_set_markdown"`
  - project attachment role like `visual_dev_prompt_set`
- Verify by reading the project media listing and fetching the R2 URL body.

## Prompt QA

Before uploading, check:

- every prompt has parameters at the end
- no `--no` parameter for V8.1
- no image-reference URLs when the user asked for text-only prompts
- core scene remains recognizably the same across variants
- named artists are not the only style mechanism; at least some prompts describe style without names
