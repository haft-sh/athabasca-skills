# Athabasca Image Generation Providers

Valid `provider` / `model` combinations for `POST /api/projects/:slug/generate/image`:

## Text-to-Image Providers

| Provider | Model | Label | Strengths |
|---|---|---|---|
| `fal-ai` | various (Flux, etc.) | — | Fast iteration, diverse models |
| `google-gemini` | `gemini-3.1-flash-image-preview` | Nano Banana 2 | Quick concept sketches, editing |
| `openai-codex` | `gpt-image-2` | GPT Image 2 | Precise spatial composition, character sheets, text-in-image, multi-subject scenes |
| `midjourney` | `midjourney-v8.1` | Midjourney v8.1 | Character-in-environment, cinematic atmosphere, lighting/mood, stylization |

## Key routing decisions

- **Character sheets** → `openai-codex` / `gpt-image-2`. Clean white backgrounds, multi-view grids, consistent identity across angles.
- **Complex spatial compositions** (reflections, hand-holding with visible props, back-to-camera) → `openai-codex` / `gpt-image-2`. Follows precise spatial instructions that MJ ignores.
- **Character-in-environment, cinematic stills** → `midjourney` / `midjourney-v8.1`. Best aesthetic quality, lighting, atmosphere.
- **Quick iteration / editing** → `google-gemini` / `gemini-3.1-flash-image-preview`.

## Common mistakes

- `provider: "openai"` — INVALID. Not in the enum. Use `openai-codex`.
- `model: "gpt-image-1"` — INVALID for `openai-codex`. Use `gpt-image-2`.
- `provider: "openai-codex"` + `model: "gpt-image-1"` — rejected: "Model gpt-image-1 is not supported for text-to-image provider openai-codex"

## API validation enum

```
"fal-ai" | "google-gemini" | "openai-codex" | "midjourney"
```

Source: `src/shared/generation-config.ts` — `textToImageModelOptions` and route Zod validators.
