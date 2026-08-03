# OpenAI Codex Image Generation via Athabasca API

## Endpoint
`POST /api/projects/:slug/generate/image`

## Provider/Model
- `provider: "openai-codex"`
- `model: "gpt-image-2"` (not `gpt-image-2-medium`)

## Operational Constraints

1. **`stream: true` is required.**
   - The OpenAI Codex worker will reject the request with `400: Stream must be set to true` if `stream` is omitted or set to `false`.
   - Always include `"stream": true` in the request body.

2. **`referenceAssetIds` are not supported in v1.**
   - Passing `referenceAssetIds` returns `400: Reference images are not supported for openai-codex generation in v1`.
   - If you need reference-driven generation with GPT Image 2, use the Hermes-native `image_generate` tool with `reference_images` (resolved from Athabasca `publicUrl`s) and then persist the local result through the media API.

3. **Model name is `gpt-image-2`.**
   - Using `gpt-image-2-medium` returns `422: Model "gpt-image-2-medium" is not supported for text-to-image provider "openai-codex"`.

## Working Request Shape
```json
{
  "prompt": "...",
  "title": "...",
  "phase": "concept",
  "provider": "openai-codex",
  "model": "gpt-image-2",
  "aspectRatio": "square",
  "stream": true
}
```

## When to Use
- When the user explicitly asks for GPT Image 2 via the Athabasca API and does not need reference images.
- For simple text-to-image character/location refs where the prompt itself carries enough visual information.

## When NOT to Use
- When reference images are required (use Hermes-native `image_generate` + Athabasca media upload instead).
- When the user wants reference-based editing (use `google-gemini` provider via the same endpoint).
