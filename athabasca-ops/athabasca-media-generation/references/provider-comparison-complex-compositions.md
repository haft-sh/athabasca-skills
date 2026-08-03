# Provider Comparison for Complex Compositions

Empirical findings from visual development sessions (May 2026) generating shot types across Midjourney V8.1, Gemini (Nano Banana 2), and GPT Image 2.

## Valid Provider/Model Names for Athabasca `generate/image` API

| Provider ID | Model ID | Label | Reference Images | Real-Person Likeness |
|---|---|---|---|---|
| `google-gemini` | `gemini-3.1-flash-image-preview` | Nano Banana 2 | ✅ (inline base64) | ✅ |
| `google-gemini` | `gemini-3-pro-image-preview` | Nano Banana Pro | ✅ (inline base64) | ✅ |
| `openai-codex` | `gpt-image-2` | GPT Image 2 | ❌ | ❌ (blocked) |
| `midjourney` | `midjourney-v8.1` | Midjourney v8.1 | ❌ | ✅ |
| `fal-ai` | `openai/gpt-image-2` | GPT Image 2 (via fal) | ✅ (via /edit) | ❌ (blocked) |
| `fal-ai` | `fal-ai/bytedance/seedream/v4.5/edit` | Seedream 4.5 Edit | ✅ (up to 10) | ✅ |
| `replicate` | `openai/gpt-image-2` | GPT Image 2 (via replicate) | ❌ | ❌ (blocked) |
| `replicate` | `bytedance/seedream-5-lite` | Seedream 5.0 Lite | ✅ (up to 14) | ✅ |
| `byteplus` | `openai/gpt-image-2` | GPT Image 2 (via byteplus) | ❌ | ❌ (blocked) |
| `byteplus` | `seedream-4-0-250828` | Seedream 4.0 | ✅ (1 ref image) | ✅ |

**Common mistakes:**
- `openai` is NOT a valid provider — use `openai-codex`
- `gpt-image-1` is NOT a valid model — use `gpt-image-2`

## Critical: Real-Person Likeness — Use Seedream, Not GPT Image 2

OpenAI's content policy blocks generating images of recognizable real people through GPT Image 2 **on any provider** (fal-ai, replicate, byteplus all share this restriction). This means:
- `fal-ai` + `openai/gpt-image-2` + reference of a real person → **blocked**
- `replicate` + `openai/gpt-image-2` + reference of a real person → **blocked**
- `byteplus` + `openai/gpt-image-2` + reference of a real person → **blocked**
- Gemini (`google-gemini`) does NOT share this restriction → ✅ works
- Seedream (ByteDance models on any provider) does NOT share this restriction → ✅ works

**When the user asks for a character sheet or reference edit of a real person (e.g., Character A R.R. Martin), use Seedream.** Workflow:
1. Upload reference photo to Athabasca media → get `asset_id`
2. Call `POST /api/projects/:slug/generate/image` with `provider=fal-ai`, `model=fal-ai/bytedance/seedream/v4.5/edit`, `referenceAssetIds=["asset_..."]`
3. Fallback chain if fal Seedream is slow: replicate → byteplus

**Seedream prompt language:** Avoid explicit "this exact person" phrasing in the text prompt; rely on the reference image to carry the likeness. Neutral descriptive prompts work better than identity-confirming ones.

**Dimension handling:** Seedream APIs return `width: null, height: null` in responses. The fal-worker uses a size-label → pixel-dimensions lookup table as a fallback rather than relying on API-returned dimensions.

## Provider Strengths by Composition Type

### Gemini (`google-gemini` / `gemini-3.1-flash-image-preview`) — Spatial Precision

**Excels at:**
- **Character turnaround sheets** on white background — 5/5 quality, clean 4-panel grid (front, 3/4, profile, full body)
- **"From behind" compositions** — correctly renders subject walking away, back to camera
- **Multi-person compositions with specific props** — hands holding with G-Shock watch + Hawaiian shirt visible (5/5)
- **Full-body framing** — respects "head to toe" instruction even with wide-angle
- **Glass/transparent surfaces** — can place figures visible through glass
- **Real-person likeness generation** — not blocked by OpenAI content policy

**Weaknesses:**
- Less atmospheric/cinematic than MJ — more "photography" than "film still"
- Occasional empty results (returned no image on ~15% of attempts)
- No style reference / `--sref` equivalent

**When to use Gemini:**
- Character sheets, turnaround references
- Shots requiring precise spatial relationships (behind, holding hands with specific accessories)
- Full-body compositions with lens distortion
- Any shot where "from behind" or "back to camera" is critical
- **Real-person likeness (when Seedream is unavailable or slow)**
- **Default fallback when Codex rate-limits or fails**

### Midjourney V8.1 — Mood & Atmosphere

**Excels at:**
- **Atmospheric night portraits** — warm lighting, bokeh, cinematic film grain
- **Character consistency across grids** — face stays stable across 4 quadrants
- **Lens distortion effects** — barrel distortion, fisheye on close-ups (4/4 on distortion quality)
- **Style references** — `--sref` for locking visual language across shots
- **Mood/tone** — "uncanny-valley beautiful," "slightly too perfect" phrasing works well
- **Real-person likeness** — not blocked by OpenAI content policy

**Weaknesses:**
- **"From behind" compositions fail** — subject always faces camera regardless of prompt language
- **Full-body framing fails** with wide-angle — produces close-up fisheye selfies instead
- **Reflection compositions fail** — treats glass as transparent, not reflective
- **Complex prop visibility** — G-Shock watch, Hawaiian shirt not rendered when asked

**When to use MJ:**
- Hero portrait shots (the "Premium" tier beauty shots)
- Atmosphere/mood exploration
- Close-up with lens distortion
- When you have style references to lock

### GPT Image 2 (`openai-codex` / `gpt-image-2`) — Role-Separated Multi-Reference Compositions

**Important distinction:**
- The **Athabasca `/generate/image` wrapper with `provider=openai-codex`** now uses the same robust raw SSE parsing pattern as Hermes Agent's OpenAI Codex image provider and works for prompt-only GPT Image 2 generation.
- The **direct Codex Responses API** remains the stronger pattern for multi-reference character/still compositions when role-separated `input_text` / `input_image` parts are required. See `references/codex-direct-reference-edit-via-responses-api.md`.

**Excels at:**
- **Two-character two-shots** — with role-separated references (e.g., reference 1 = environment, reference 2 = character A, reference 3 = character B), Codex maintains character identity across multiple anchors better than wrapped API calls.
- **Precision instruction following** — when the prompt is specific about pose, gesture, and staging, Codex responds more precisely than MJ.
- **Insert/gesture shots** — close iconic inserts (hand on chest, hand on shell) where anatomy specificity matters.

**Weaknesses:**
- Rate-limited (HTTP 429) under burst batch usage
- For prompt-only stills, use Athabasca `/generate/image` with `provider=openai-codex`; it uses the shared robust SSE parser.
- For multi-reference / role-separated inputs, use the direct Codex Responses API pattern when the normalized API cannot express the required `input_image` parts.
- **Blocked for real-person likeness** — content policy restriction shared across all providers using GPT Image 2

**When to use GPT Image 2 / Codex:**
- User explicitly requests it and multi-reference edits are needed
- Two-character staging where both identities must be preserved simultaneously
- Precision insert shots with specific anatomy instructions
- Prompt-only stills: use Athabasca `/generate/image` with `provider=openai-codex`
- Multi-reference / role-separated stills: use the direct Codex Responses API pattern if the normalized endpoint cannot express the reference parts

**Fallback when Codex 429s:** Switch to `google-gemini` via `/api/projects/:slug/generate/image` immediately. Do not retry Codex in the same batch.

## Provider Selection Decision Tree

```
Is the shot of a REAL PERSON'S LIKENESS (character reference sheet)?
  → Seedream: fal-ai (primary), replicate (backup), byteplus (third backup)

Is the shot a character sheet / turnaround (fictional character)?
  → Gemini (5/5 clean white bg results)

Is the shot "from behind" or "back to camera"?
  → Gemini (MJ consistently fails this)

Does the shot need specific props visible (watch, shirt pattern, etc.)?
  → Gemini (handles prop + spatial combo correctly)

Is the shot a full-body with wide-angle distortion?
  → Gemini (MJ produces close-ups instead)

Is the shot a two-character two-shot with precise identity constraints?
  → Codex direct Responses API (multi-reference, role-separated)

Is the shot a precision insert/gesture requiring specific anatomy?
  → Codex direct Responses API

Is the shot an atmospheric portrait / mood exploration?
  → MJ V8.1 (superior cinematic quality)

Is the shot a close-up with lens distortion?
  → MJ V8.1 (strong barrel distortion on faces)

Do you have style references to lock?
  → MJ V8.1 (--sref workflow)

Is the shot a reflection in glass/mirror?
  → Gemini (try "through glass" composition; MJ and Codex both fail reliably here)

Is Codex rate-limited (HTTP 429)?
  → Gemini via /api/projects/:slug/generate/image (immediate fallback, do not retry)
```

## Batch Generation Strategy

When generating multiple shot types simultaneously:
1. Fire all MJ jobs in parallel (they handle concurrency well)
2. Fire Codex direct API jobs sequentially with 3–5 second delays between them (avoids 429)
3. Fire Gemini jobs with 3–5 second delays between them
4. **Always plan a Gemini or Seedream fallback** for any Codex slot — Codex will 429 unpredictably on burst batches
5. Don't mix providers in the same foreground terminal call unless using Gemini via `/generate/image` (which is async-friendly)
6. Expect ~15–20 seconds per MJ grid, ~35–45 seconds per Gemini single image, ~60–90 seconds per Codex direct API call, ~25–40 seconds per Seedream edit

## R2 Asset URL Pattern

Athabasca stores generated assets with double-timestamp filenames:
```
{project}/{category}/{prefix}_{timestamp1}_{timestamp2}.{ext}
```

When downloading, always fetch the URL from `GET /api/media/:assetId` rather than constructing URLs — the timestamp pattern is not predictable and wrong URLs return HTML error pages (not images), which breaks `vision_analyze`.

## Vision Tool Rate Limits

Vision tool hits rate limits independently from image generation rate limits. If `vision_analyze` repeatedly fails during batch review:
1. Download all candidate images locally first: `curl -sS "<url>" -o /tmp/provider-comparison-upscales/<file>`
2. Do one combined batch vision call with all URLs listed, rather than per-shot calls
3. Or use the browser's built-in vision (the assistant model sees images natively when `image_url` is provided)
4. Check file sizes locally as a sanity check before uploading: files < 50 KB are likely HTML error pages, not images