# Character, costume, and scene-reference generation notes

## Context

Use this note when generating stills that transform an existing character reference into a new sheet, costume concept, or scene reference while preserving identity through Athabasca's normalized image route.

Canonical route used successfully:

```text
POST /api/projects/:slug/generate/image
provider: openai-codex
model: gpt-image-2
referenceAssetIds: [...]
```

## Proven reference-conditioning patterns

### 1) 2D character → 3D character sheet

Use three references when available:
1. source character identity reference
2. approved target character-sheet layout / proportions reference
3. premium 3D render style reference

Prompt structure:
- first reference = strict identity lock: species, colors, face, proportions, outfit/accessories
- second reference = sheet layout: white background, large central pose plus support poses/views, no labels
- third reference = render style: polished 3D, soft studio lighting, tactile materials
- explicitly forbid identity drift from nearby characters or unrelated wardrobe cues

### 2) Character sheet → costume concept

Use at least:
1. canonical character sheet / latest approved identity
2. optional style-quality reference
3. optional prior successful costume variant for delta edits

Prompt as a delta against prior success:
- preserve identity and silhouette first
- specify costume changes as numbered requirements
- for helmet/prop details, be literal about where the prop is worn, held, or grounded
- for morphology changes, state visible body-shape targets explicitly

### 3) Costume concept + environment → scene reference

Use two references:
1. character/costume lock
2. environment target

Prompt split:
- preserve identity and costume language from reference 1
- translate environment reference 2 into the same target style when needed
- specify pose, prop contact, and spatial relationship unambiguously
- repeat must-hit prop placement constraints at the end

## Scene-reference prompting tips

- Use `aspectRatio: "landscape"` for cinematic scene references unless the user requests otherwise.
- Include the relevant script excerpt when the image is a scene reference; this improves staging fidelity.
- State which assets are identity/style/environment references in `provenanceNote`.
- After generation, verify the URL with a real GET, inspect the must-hit beats, then tag with character, location, scene, prop, and `scene-reference` tags.
