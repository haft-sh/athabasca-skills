# GPT Image 2 vs Seedream: Reference Images & Content Policy

## Quick Decision Tree

**Real person likeness needed?** → Use Seedream (GPT Image 2 will block it)  
**Fictional character with reference?** → GPT Image 2 or Seedream both work  
**No reference image?** → GPT Image 2 for photorealism, Midjourney for atmosphere

---

## GPT Image 2 via fal-ai: Reference Image Support

fal-ai's GPT Image 2 model supports image-to-image generation via the `/edit` endpoint. When `referenceAssetIds` is provided in the Athabasca API call, the system automatically routes to `https://fal.run/openai/gpt-image-2/edit` with `image_urls` parameter.

### Usage

```json
POST /api/projects/:slug/generate/image
{
  "provider": "fal-ai",
  "model": "openai/gpt-image-2",
  "referenceAssetIds": ["asset_mpq..."],
  "prompt": "Using this person, create a turnaround sheet...",
  "aspectRatio": "landscape"
}
```

### Implementation

- `fal-worker.ts` checks for `referenceImageUrls` param + `model === "openai/gpt-image-2"` → switches to `/edit` endpoint
- `image-generation.ts` loads reference assets and passes `publicUrl` array to fal-worker
- GPT Image 2 and Seedream 4.5 Edit both support reference images on fal-ai — FLUX does not

---

## GPT Image 2 Content Policy: Strict Real-Person Blocking

GPT Image 2's content checker blocks real-person likeness generation across **ALL providers** (openai-codex, fal-ai, replicate, byteplus). This is a platform-level OpenAI restriction, not provider-specific.

### What gets flagged:
- **Explicit names**: "George R.R. Martin", "Leonardo DiCaprio", any recognizable public figure
- **"This exact person" language**: "using this exact person", "keep his exact likeness", "this face"
- **Reference images of real people**: Even with generic text prompts, the image itself can trigger detection
- **Celebrity names in any context**: "Hugh Hefner style robe" → flagged

### What passes (but still limited):
- Generic appearance descriptions without naming the person
- Reference image + generic prompt about clothing/pose/environment (sometimes works, often doesn't)
- Short, neutral prompts that don't emphasize "likeness" or "exact match"

**Bottom line:** If you need a real person's likeness, GPT Image 2 will likely fail. Use Seedream instead.

---

## Seedream Models: The Real-Person Workaround

ByteDance's Seedream models are significantly more permissive with real-person likeness. All three providers (fal-ai, Replicate, BytePlus) offer Seedream variants that accept reference images and generate likeness without content policy blocks.

### Provider Comparison

| Provider | Model | Reference Images | Cost/Image | Best For |
|----------|-------|------------------|------------|----------|
| **fal-ai** | `fal-ai/bytedance/seedream/v4.5/edit` | Up to 10 | $0.04 | Multi-reference blending, complex compositions |
| **Replicate** | `bytedance/seedream-5-lite` | Up to 14 | $0.035 | Best likeness accuracy, sequential batches |
| **BytePlus** | `seedream-4-0-250828` | 1 | $0.03 | Simple likeness from single reference |

### Seedream 5.0 Lite (Replicate) — Recommended for Character Sheets

```json
POST /api/projects/:slug/generate/image
{
  "provider": "replicate",
  "model": "bytedance/seedream-5-lite",
  "referenceAssetIds": ["asset_mpq..."],
  "prompt": "Film costume department reference sheet. White background. Four full-body standing poses. [Clothing and accessories only]. Even studio lighting.",
  "aspectRatio": "landscape"
}
```

**Why it works:**
- Accepts up to 14 reference images for complex likeness work
- Sequential batch generation (`sequential_image_generation: "auto"`) can produce multiple views in one call
- Natural human proportions (unlike Gemini's toy-like output)
- 2K or 3K output resolution

### Seedream 4.5 Edit (fal-ai) — Good for Multi-Reference

```json
POST /api/projects/:slug/generate/image
{
  "provider": "fal-ai",
  "model": "fal-ai/bytedance/seedream/v4.5/edit",
  "referenceAssetIds": ["asset_mpq1", "asset_mpq2"],
  "prompt": "Blend these two people into a new character...",
  "aspectRatio": "landscape"
}
```

**Use case:** When you need to combine features from multiple reference images (e.g., "face from photo A, body type from photo B").

### Seedream 4.0 (BytePlus) — Budget Option

```json
POST /api/projects/:slug/generate/image
{
  "provider": "byteplus",
  "model": "seedream-4-0-250828",
  "referenceAssetIds": ["asset_mpq..."],
  "prompt": "Generate a portrait of this person...",
  "aspectRatio": "landscape"
}
```

**Limitation:** Only accepts 1 reference image. Use when cost matters more than flexibility.

---

## Critical Prompt Pitfalls

### 1. "Character" Keyword → Toy Proportions

Using the word "character" in prompts triggers a "character design" rendering mode that produces action-figure proportions (oversized head, stubby limbs).

**Wrong:**
```
"Character turnaround sheet for George, age 64, white beard..."
```

**Right:**
```
"Film costume department reference sheet. White background. Four full-body standing poses. Heavyset older man, white beard, wire-frame glasses, fisherman cap..."
```

**Test:** Removing "character" from the same prompt immediately fixes proportions in Seedream 4.5 and 5.0.

### 2. Verbose Prompts with Reference Images

When you have a reference photo, write SHORT prompts describing only what's different from the reference. The image does the heavy lifting; the text steers the delta.

**Wrong (verbose):**
```
"Create a turnaround sheet of this exact person, a heavyset older man age 64 with a full white beard and mustache, wearing wire-frame glasses and a black fisherman cap with braided cord..."
```

**Right (concise):**
```
"Film costume department reference sheet. White background. Four full-body standing poses. Same person as reference, wearing light blue shirt, dark jeans, brown shoes. Even studio lighting."
```

### 3. Naming Real People

Even in Seedream, avoid explicit celebrity names in prompts. Describe the style/aesthetic instead.

**Wrong:**
```
"Man wearing a Hugh Hefner-style silk robe"
```

**Right:**
```
"Man wearing a luxurious burgundy silk smoking jacket with gold piping, shawl lapels, and matching silk belt tie"
```

---

## Workflow: Real-Person Character Sheet Generation

1. **Find reference photo** — Wikimedia Commons, official author photos, press kits
2. **Upload to Athabasca** — `POST /api/uploads` with `category: "moodboard"`, `sourceKind: "web_import"`
3. **Analyze with vision_analyze** — Extract precise visual details (clothing, accessories, distinctive features)
4. **Generate with Seedream** — Use `replicate` + `bytedance/seedream-5-lite` + `referenceAssetIds`
5. **Write SHORT prompt** — Focus on clothing/pose/environment, let reference carry likeness
6. **Avoid "character" keyword** — Use "costume department reference" or "photographic reference"
7. **Iterate if needed** — Adjust prompt, not reference (reference is the anchor)

---

## Provider Routing Summary

| Shot Type | Best Provider | Model | Why |
|-----------|---------------|-------|-----|
| Real-person likeness | Replicate | `bytedance/seedream-5-lite` | Best accuracy, 14 references, 3K output |
| Multi-reference blend | fal-ai | `fal-ai/bytedance/seedream/v4.5/edit` | Up to 10 references |
| Budget likeness | BytePlus | `seedream-4-0-250828` | Cheapest, single reference |
| Fictional character sheet | openai-codex | `gpt-image-2` | Photorealism, but blocks real people |
| Atmosphere/mood | midjourney | `midjourney-v8.1` | Artistic quality, not reference sheets |
| Precise spatial composition | google-gemini | `gemini-3.1-flash-image-preview` | Complex layouts, but toy proportions |

---

## Key Workflow Rules

1. **ALWAYS use the Athabasca API** — never curl fal.ai, Replicate, or BytePlus directly. The API handles auth, R2 persistence, provenance tracking, and attachment. Direct curling produces orphaned images with no provenance record.

2. **When Codex quota is exceeded**, the GPT Image 2 fallback chain is:
   ```
   openai-codex → fal-ai → replicate → byteplus
   ```
   But remember: **all four have the same content policy restrictions**. If one blocks real-person likeness, they all will. Switch to Seedream instead.

3. **Seedream models share credentials with video generation** (Seedance/Kling on fal-ai, Replicate, BytePlus). No additional API keys needed.

4. **Review before generating** — When the user asks to "review the images," show existing assets in order and wait for explicit "generate new" instruction. Don't auto-generate variations.