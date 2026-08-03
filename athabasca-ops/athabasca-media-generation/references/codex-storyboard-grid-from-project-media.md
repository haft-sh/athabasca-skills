# Codex GPT Image storyboard grid from Athabasca project media

Use this when the user wants a storyboard contact sheet / 3x3 grid generated with Hermes-native `image_generate` using GPT Image 2 via OpenAI Codex, while sourcing references from Athabasca media assets.

## Pattern

1. Resolve every Athabasca `asset_...` id through the media API:
   - `GET /api/media/:assetId`
   - collect `asset.publicUrl`, `title`, `kind`, `contentType`, and any character metadata.
2. If the user points at a markdown shot-list artifact, resolve it too and use its content or prior assistant output as the scene source.
3. Build the prompt as a single storyboard-grid instruction:
   - state exact grid layout, e.g. `one square image containing nine equal panels in a 3 by 3 grid`
   - identify each reference by role: `reference 1 = primary character`, `reference 2 = secondary character`, etc.
   - provide panel-by-panel instructions in reading order
   - preserve character identity, uniform colors, species, location continuity, and visual style
   - explicitly say `no speech bubbles, no text captions, no watermarks` unless captions are desired
4. Call Hermes `image_generate` with:
   - `provider=openai-codex` implicitly via the configured GPT Image 2 backend
   - `aspect_ratio=square` for a 3x3 grid unless the user asks otherwise
   - `reference_images=[publicUrl1, publicUrl2, ...]`
5. Verify the resulting local image visually before reporting success:
   - nine panels exist
   - key requested panels landed
   - critical characters are recognizable
   - location/lighting continuity is present
6. Persist the generated local PNG through Athabasca:
   - `POST /api/projects/:slug/media`
   - `phase=storyboard`
   - `category=generated`
   - `sourceKind=generated`
   - `attachment={"targetType":"project","targetId":"<projectId>","role":"storyboard_grid"}`
7. Store provenance in `metadataJson`:
   - source markdown asset id / URL
   - reference asset ids
   - `provider=openai-codex`
   - GPT Image model/quality from the tool result when available
   - concise prompt summary
8. Verify the uploaded asset via `GET /api/media/:assetId` and optionally `curl -I` the public URL.

## Prompt skeleton

```text
Create a single 3x3 storyboard grid image for <project/scene>. Use the attached references as design anchors: <ref 1 role>, <ref 2 role>, <ref 3 role>. Preserve character identity, uniform colors, species, and the established visual style. Produce rough clean storyboard panels, not final polished key art. No speech bubbles, no text captions, no watermarks.

Layout: one square image containing nine equal panels in a 3 by 3 grid. Each panel should be a distinct storyboard frame in reading order.

Panel 1: ...
Panel 2: ...
...
Panel 9: ...

Overall continuity: <style, lighting, palette, location, costume, key guardrails>.
```

## Pitfalls

- Do not pass Athabasca asset IDs directly as `reference_images`; resolve them to public URLs first.
- Do not assume `image_generate` persists output into Athabasca. It returns a local file path; upload it through the media API.
- A source markdown artifact can describe eight shots while a 3x3 grid needs nine panels. Split a natural insert/detail beat into two panels rather than inventing a story-changing new beat.
- GPT Image may satisfy grid and character references while drifting on exact panel intent. Verify visually and report concise caveats.
