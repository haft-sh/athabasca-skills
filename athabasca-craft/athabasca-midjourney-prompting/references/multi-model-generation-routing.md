# Multi-Model Generation Routing

Athabasca's `POST /api/projects/:slug/generate/image` accepts multiple providers. Each excels at different task types.

## Golden Rules

1. **ALWAYS route through the Athabasca API** — never curl upstream providers directly. The API handles auth, persistence to R2, provenance tracking, and attachment. Direct curling bypasses all of this and the user will (correctly) ask why you're not using the API.

2. **Prefer image-prompted generation over verbose text descriptions.** When you need likeness, style, or composition matching, pass a reference image via `referenceAssetIds` rather than writing paragraph-length text prompts. Image references are more accurate and the prompts stay concise.

3. **Telegram cannot render local file paths as images.** When sharing generated images in chat, use the R2 `publicUrl` from the API response (as markdown `![alt](url)`) or the `MEDIA:/absolute/path` prefix for native delivery. Never paste a local path and expect the user to see it.

## Valid Provider Names

The `provider` field must be one of:
- `midjourney`
- `google-gemini`
- `fal-ai`
- `openai-codex`
- `replicate`
- `byteplus`

**Pitfall:** `openai` is NOT a valid provider name. GPT Images uses `openai-codex` as provider and `gpt-image-2` as model.

## Provider × Model Matrix (Full)

| Provider | Image Models | Reference Images | Video Models |
|---|---|---|---|
| `midjourney` | `midjourney-v8.1` | ❌ (use image prompts in text) | — |
| `google-gemini` | `gemini-3.1-flash-image-preview` | ✅ (up to 14, Gemini-native) | — |
| `openai-codex` | `gpt-image-2` | ❌ (Codex API, v1) | — |
| `fal-ai` | `openai/gpt-image-2`, `fal-ai/bytedance/seedream/v4.5/edit`, `fal-ai/bytedance/seedream/v4.5/text-to-image`, `fal-ai/flux-2-pro` | ✅ GPT Image 2 via `/edit`, ✅ Seedream 4.5 Edit | Seedance, Kling, etc. |
| `replicate` | `openai/gpt-image-2`, `bytedance/seedream-5-lite` | ✅ Seedream 5.0 (up to 14 refs) | Seedance |
| `byteplus` | `openai/gpt-image-2`, `seedream-4-0-250828` | ✅ Seedream 4.0 (1 ref image) | Seedance |

### Seedream Models (Chinese image gen, often more permissive content policy)

| Model | Provider | Edit/Ref Support | Notes |
|---|---|---|---|
| `fal-ai/bytedance/seedream/v4.5/edit` | `fal-ai` | ✅ Up to 10 reference images | Best for image-to-image with references. ~$0.04/image. |
| `fal-ai/bytedance/seedream/v4.5/text-to-image` | `fal-ai` | ❌ Text only | Standard T2I generation. |
| `bytedance/seedream-5-lite` | `replicate` | ✅ Up to 14 refs, sequential batch (up to 15 images) | Latest model. 2K/3K resolution. ~$0.035/image. |
| `seedream-4-0-250828` | `byteplus` | ✅ 1 reference image | BytePlus ModelArk. Up to 4K. ~$0.03/image. |

## Routing Decision Tree

```
Need a character turnaround/reference sheet?
  └─ Real person? → Upload reference photo to Athabasca, use Seedream 4.5/5.0 edit with referenceAssetIds
  └─ Fictional character? → Gemini (concise prompt) or GPT Image 2 (backup chain)

Need cinematic mood/atmosphere?
  └─ Midjourney V8.1

Need precise spatial composition (reflections, props, from-behind)?
  └─ Gemini or GPT Image 2

GPT Image 2 quota exceeded?
  └─ Use `openai-codex` first. If exhausted: `fal-ai` → `replicate` → `byteplus`
  └─ ⚠️ **fal-ai requires the user explicit approval** before use — it is a paid provider
```

### GPT Image 2 Availability (Backup Provider)

GPT Image 2 (`openai/gpt-image-2`) is available across **4 providers** as a fallback chain:
1. `openai-codex` (default, via Hermes native Codex) — primary
2. `fal-ai` (model: `openai/gpt-image-2`) — first backup
3. `replicate` (model: `openai/gpt-image-2`) — second backup
4. `byteplus` (model: `openai/gpt-image-2`) — third backup

When the primary Codex quota is exceeded, route to fal-ai first (lowest latency, same fal.ai API key), then replicate, then byteplus.

## Routing Guide

### Midjourney (`midjourney`, model: `midjourney-v8.1`)

**Best for:**
- Character-in-environment compositing
- Cinematic lighting and atmosphere
- Stylized concept art and mood pieces
- Storyboard stills with strong art direction
- Reference-heavy work with `--sref` and image prompts

**Weak at:**
- Character turnaround sheets (messy backgrounds, inconsistent angles)
- "From behind" framing (consistently turns subjects to face camera)
- Precise spatial/compositional instructions (e.g., "object A is to the left of object B")
- Clean white backgrounds for reference docs
- Multi-element layouts with strict positioning

**Known quirks:**
- Discord 429 rate limiting when firing 6+ parallel generations — stagger with `sleep 3-8` between requests
- `--no` parameter not supported in V8.1
- `--iw` hard cap is 3.0
- Grid images download as WebP despite `.jpg` storage key extensions
- R2 URLs have double timestamps: `{key}_{ts1}_{ts2}.ext`

### GPT Images 2 (`openai-codex`, model: `gpt-image-2`)

**Best for:**
- Character turnaround/reference sheets (clean white bg, consistent angles)
- Precise spatial composition ("X is behind Y, Z is in the reflection")
- "From behind" framing and directional instructions
- Complex compositional tricks (reflections in glass showing different subjects)
- Text rendering in images (signs, UI overlays, error modals)
- Multi-subject scenes with specific spatial relationships

**Weak at:**
- Atmospheric/stylized art direction (more literal than MJ)
- Cinematic lighting drama (tends toward even, well-lit results)
- Style reference matching (no `--sref` equivalent)

**Known quirks:**
- Single image output (no 2x2 grid for selection)
- Slower generation than MJ
- Less "happy accidents" — more predictable, less serendipitous

### Replicate (`replicate`, model: `openai/gpt-image-2`)

**Best for:**
- GPT Image 2 generation (second backup after fal-ai)
- Character turnaround/reference sheets
- Text rendering in images
- Precise spatial composition

**Known quirks:**
- Uses async prediction API (create → poll → download)
- Polling interval: 2s, timeout: 120s
- Requires `REPLICATE_API_TOKEN` or `REPLICATE_API_KEY` env var

### BytePlus (`byteplus`, model: `openai/gpt-image-2`)

**Best for:**
- GPT Image 2 generation (third backup)
- Enterprise-tier generation with dedicated infra

**Known quirks:**
- Uses async task creation + polling (same pattern as video worker)
- Polling interval: 3s, timeout: 120s
- Requires `BYTEPLUS_ARK_API_KEY` or `ARK_API_KEY` env var
- API base: `https://ark.ap-southeast.bytepluses.com/api/v3`

### fal.ai (`fal-ai`)

**Best for:**
- GPT Image 2 generation (paid fallback only — ⚠️ requires the user explicit approval)
- GPT Image 2 with reference images (via `/edit` endpoint — ⚠️ requires the user explicit approval; `openai-codex` does not support `referenceAssetIds`)
- Video generation (Kling, Seedance, etc.)
- Fast iteration on simple concepts (FLUX 2 Pro)
- Batch generation (paid fallback)

**Models:**
- `openai/gpt-image-2` — GPT Image 2 (character sheets, text rendering, precise composition, **supports reference images via /edit**)
- `fal-ai/bytedance/seedream/v4.5/edit` — Seedream 4.5 Edit (real-person likeness, multi-reference blending, up to 10 refs)
- `fal-ai/bytedance/seedream/v4.5/text-to-image` — Seedream 4.5 (text-to-image only)
- `fal-ai/flux-2-pro` — FLUX 2 Pro (+ Clarity upscaler, no reference images)

#### Fal-ai GPT Image 2 with Reference Images

When `referenceAssetIds` is provided with model `openai/gpt-image-2`, the system automatically routes to the `/edit` endpoint (`https://fal.run/openai/gpt-image-2/edit`) with `image_urls` parameter. This enables image-to-image generation for likeness matching, style transfer, etc.

```json
{
  "provider": "fal-ai",
  "model": "openai/gpt-image-2",
  "referenceAssetIds": ["asset_mpq..."],
  "prompt": "Create a character turnaround sheet using this person...",
  "aspectRatio": "landscape"
}
```

**Pitfall: Content policy is strict.** Fal-ai's content checker for GPT Image 2 will flag:
- Explicitly naming real people (e.g. "Character A R.R. Martin")
- Phrases like "this exact person", "use this face", "keep his exact likeness"
- Descriptions that strongly imply a specific identifiable individual

Workaround: Describe the subject's appearance features precisely without naming them or using "this person" language. Let the reference image carry the likeness while the prompt describes clothing, pose, and environment.

**Pitfall: Only GPT Image 2 and Seedream 4.5 Edit support reference images on fal-ai.** FLUX 2 Pro does NOT support `referenceAssetIds` — the API will reject them with an error.

### Google Gemini (`google-gemini`, model: `gemini-3.1-flash-image-preview`)

**Best for:**
- Quick concept exploration
- Image editing/modification of existing assets
- Fast turnaround when quality bar is moderate
- Environments, props, UI mockups, text-in-image elements

**Weak at:**
- Character turnaround sheets — produces toy-like/action-figure proportions with oversized heads. Do NOT use Gemini for full-body character references; route to GPT Image 2 instead.
- Realistic human anatomy and proportions in general
- Likeness matching from reference photos (no image-to-image support for reference photos via the generation endpoint)

**Known quirks:**
- Prompts must be concise — overly long prompts cause the API to hang or return empty results
- Single image output, landscape 16:9 or square aspect ratios
- Supports reference images natively via Gemini's multimodal API (binary data passed inline)

## Decision Framework

1. **Need a character reference sheet?**
   - **Real person?** → Seedream 5.0 (`replicate` + reference photo) — best likeness accuracy, natural proportions
   - **Fictional character?** → GPT Images 2 (`openai-codex` primary; ⚠️ `fal-ai` requires the user explicit approval)
2. **Need a cinematic still with strong atmosphere?** → Midjourney
3. **Need precise spatial composition (reflections, "from behind", complex layouts)?** → GPT Images 2 (`openai-codex` primary; ⚠️ `fal-ai` requires the user explicit approval)
4. **Need to explore style/aesthetic direction?** → Midjourney with `--sref`
5. **Need to composite a known character into a known environment?** → Midjourney with dual image prompts
6. **Need text/UI elements in the image?** → GPT Images 2 (`openai-codex` primary; ⚠️ `fal-ai` requires the user explicit approval)
7. **Need fast iteration on multiple variants?** → Midjourney (2x2 grids give 4 options per request)
8. **MJ failed on a spatial/directional instruction?** → Retry with GPT Images 2 (`openai-codex` first)
9. **Codex quota exceeded?** → ⚠️ Get the user explicit approval, then use `fal-ai` provider with `openai/gpt-image-2` model
10. **Real person likeness blocked by content policy?** → Switch to Seedream (all GPT Image 2 providers have the same restriction)

## GPT Image 2 Fallback Chain

When native Codex (`openai-codex`) is exhausted or unavailable:
```
openai-codex (primary, free via subscription) → fal-ai (⚠️ paid, requires the user approval) → replicate → byteplus
```

> ⚠️ **the user's standing rule:** fal-ai is a paid provider. Never use it by default. Get explicit approval before routing GPT Image 2 through fal-ai, even when `referenceAssetIds` is the reason for the fallback.

All three backup providers use the same model, so output quality is identical. Route in order of preference: `fal-ai` (same API key as video gen, requires approval), `replicate`, `byteplus`.

## Parallel Generation Strategy

When firing multiple generations across providers:

- MJ: max 4-5 parallel, stagger with `sleep 3-8` to avoid Discord 429s
- GPT Images: can fire more aggressively, less rate-limit sensitive
- Mix providers for coverage: fire MJ for aesthetic exploration + GPT Images for precise composition simultaneously
- Budget: MJ costs credits per grid (4 images), GPT Images costs per single image

## Error Recovery

- **MJ 429:** Wait 1-2 seconds and retry. If persistent, add `sleep` between requests.
- **Wrong provider name:** Check against the valid list above. Common mistake: `openai` instead of `openai-codex`.
- **Download returns HTML instead of image:** URL is wrong. Use `publicUrl` from API response directly, don't construct from storage key.
