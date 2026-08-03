# Image Model Routing Table

## Reference Image Support by Provider/Model

| Provider | Model | Supports `referenceAssetIds`? | Notes |
|---|---|---|---|
| `google-gemini` | `gemini-3-pro-image-preview` | ✅ Yes | Good for generation from references. **UNRELIABLE for targeted edits** — frequently returns "no inline image data" on edit-style prompts (change one element in an existing image). |
| `google-gemini` | `gemini-3.1-flash-image-preview` | ✅ Yes | Faster, lower quality. Same edit failure mode as Pro. |
| `openai-codex` | (default) | ❌ No | Clean single stills, text-heavy edits. No references in v1 |
| `fal-ai` | `openai/gpt-image-2` | ✅ Yes (via `/edit` endpoint) | ⚠️ **Paid fallback.** `openai-codex` is primary. Use `fal-ai` for GPT Image 2 with references only after getting the user's explicit approval. |
| `fal-ai` | `fal-ai/bytedance/seedream/v4.5/text-to-image` | ❌ No | Seedream T2I, no references |
| `fal-ai` | `fal-ai/bytedance/seedream/v4.5/edit` | ✅ Yes | Seedream edit with references |
| `fal-ai` | `fal-ai/flux-2-pro` | ❌ No | FLUX 2 Pro, no references |
| `replicate` | `bytedance/seedream-5-lite` | ✅ Yes (up to 14) | **Best edit engine.** No content policy on faces. 3K output. Superior at targeted edits (change one element while preserving everything else). Also excellent for face/selfie generation. Use as primary edit tool when GPT Image 2 hits content policy or Gemini returns empty. |
| `midjourney` | (default) | ❌ No | Discord/BYOA flow, style-heavy |

## Key Distinctions

- **GPT Image 2 with references**: `openai-codex` does not support `referenceAssetIds` in v1. ⚠️ When references are needed, the only capability path is `provider: "fal-ai"` + `model: "openai/gpt-image-2"`. State the constraint and get the user's explicit approval before using this paid fallback.
- **Gemini with references**: Use `provider: "google-gemini"` + `model: "gemini-3-pro-image-preview"`. Model ID must be exact — `gemini-2.5-flash-image` is rejected.
- **Seedream Edit**: Use `provider: "fal-ai"` + `model: "fal-ai/bytedance/seedream/v4.5/edit"` for Seedream-based reference edits.
- **Seedream 5 Lite (Replicate)**: Use `provider: "replicate"` + `model: "bytedance/seedream-5-lite"` for face/selfie generation and edits. Supports up to 14 reference images, 3K output, no content policy restrictions. Primary fallback when GPT Image 2 returns `content_policy_violation` and Gemini edit returns empty.

## Aspect Ratio

All providers accept the normalized enum: `landscape | square | portrait`.
For Midjourney specifically, also include `--ar 16:9` (or other MJ ratio syntax) inside the prompt text.
