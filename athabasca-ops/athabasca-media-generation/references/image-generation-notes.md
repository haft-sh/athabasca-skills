# Image generation notes absorbed from `athabasca-image-generation`

## Canonical route

`POST /api/projects/:slug/generate/image`

Do not use the removed `/api/projects/:slug/generate-image` route.

## Provider selection

| Provider | Best for | Reference support | Notes |
|---|---|---|---|
| `fal-ai` + `openai/gpt-image-2` | Prop shots, clean stills, text-heavy edits with references | ✅ `referenceAssetIds` (via `/edit` endpoint) | ⚠️ **Paid fallback.** Use only when `openai-codex` is exhausted OR when `referenceAssetIds` is required (openai-codex doesn't support it in v1). the user must explicitly approve before using. Will flag `content_policy_violation` on face/selfie prompts — see fallback chain below. |
| `google-gemini` | Reference edits, inline reference workflows | ✅ `referenceAssetIds` | Models: `gemini-3-pro-image-preview`, `gemini-3.1-flash-image-preview`. Can return empty on edit tasks — see pitfalls. |
| `replicate` + `bytedance/seedream-5-lite` | Faces, selfies, real-person likeness, edits when GPT/Gemini fail | ✅ `referenceImageUrls` (up to 14) | **No content policy restrictions on faces.** Supports 3K output. Fallback for face/selfie generation and edits. |
| `fal-ai` + `fal-ai/bytedance/seedream/v4.5/text-to-image` | Fast non-referenced generation | Edit variant supports refs | Alternative Seedream path via fal.ai |
| `openai-codex` / `gpt-image-2` | Clean single stills without references | ❌ No references in v1 | **Primary.** Free via the user's OpenAI subscription. Use first. `referenceAssetIds` not supported — route through `fal-ai` only after getting the user's explicit approval. |
| `midjourney` | Style-heavy work, grids, character-sheet-like outputs | N/A (grid-based) | Discord/BYOA flow, slower generation |

## Typical request fields

- `prompt`
- `provider`
- `model`
- `aspectRatio`
- `phase`
- `title`
- `provenanceNote`
- `referenceAssetIds` when supported

## GPT Image 2 via fal.ai

> ⚠️ **Paid provider.** `openai-codex` is primary. Use `fal-ai` only when Codex quota is exhausted **AND** the user explicitly approves, OR when `referenceAssetIds` is required (Codex doesn't support it in v1) — in which case, state the constraint and get the user's approval.

- Provider: `fal-ai`, model: `openai/gpt-image-2`
- Supports `referenceAssetIds` (via `/edit` endpoint internally) — the current capability path for referenced generation when the user approves the paid fallback
- `openai-codex` provider does NOT support references in v1; when references are truly needed, state the constraint and ask the user for explicit approval before routing to `fal-ai`
- Good for clean single stills, text-heavy edits, and prop close-ups with environment continuity
- **Will fail with `content_policy_violation` on prompts involving faces, selfies, or real-person descriptions.** This is OpenAI's upstream policy, not a prompt issue. Do NOT retry with reworded prompts — switch provider.

## Content policy fallback chain (faces & selfies)

When GPT Image 2 flags a face/selfie prompt with `content_policy_violation`:

1. **Gemini** (`google-gemini` + `gemini-3-pro-image-preview`) — try first, supports `referenceAssetIds`, good quality. But can fail with "returned no inline image data" on edit tasks.
2. **Seedream 5 Lite** (`replicate` + `bytedance/seedream-5-lite`) — reliable fallback, supports up to 14 reference images via `referenceAssetIds`, 3K output. **No content policy restrictions.** the user's confirmed good quality for face/selfie work.
3. **Seedream 4.5** (`fal-ai` + `fal-ai/bytedance/seedream/v4.5/text-to-image`) — alternative path via fal.ai.

For **edits of existing face images** (e.g., changing glasses on a selfie):
- GPT Image 2 edit: almost always fails on faces
- Gemini edit: both `gemini-3-pro-image-preview` and `gemini-3.1-flash-image-preview` can return empty — unreliable for edits
- **Seedream 5 Lite is the reliable edit path for face images** — frame it as "recreate with one change" rather than "edit"

## Character detail verification pitfall

**Always check the reference character sheet image before writing prompts for character-dependent shots.** Common errors:
- Glasses color/style: "black horn-rimmed" vs actual "light tan/brown thin frames" — easy to fabricate from memory
- Robe pattern/color details
- Hat style specifics
- Accessories (slippers, jewelry)

Rule: if the character sheet is a `referenceAssetId`, describe the outfit as "matching the character sheet reference" rather than re-describing details from memory. The model will pull from the image.

## Google Gemini image models

- Provider: `google-gemini`
- Supported models: `gemini-3-pro-image-preview`, `gemini-3.1-flash-image-preview`
- `gemini-2.5-flash-image` is NOT a valid model name — will be rejected by the API
- Supports `referenceAssetIds` for reference-driven edits
- **Pitfall:** Both models can return `"Google Gemini returned no inline image data"` on edit tasks — this is not a prompt issue, it's a Gemini-side failure. Fall back to Seedream 5 for edits.
- **Pitfall:** Gemini generation calls that time out on the client side (180s) may still succeed server-side. Always check the media library for the asset before retrying.

## Seedream 5 Lite via Replicate

- Provider: `replicate`, model: `bytedance/seedream-5-lite`
- Supports `referenceAssetIds` (up to 14 reference images) — maps to `image_input` parameter
- Aspect ratios: `1:1`, `16:9`, `9:16` (mapped from `square`, `landscape`, `portrait`)
- Output: up to 3K resolution
- **No content policy restrictions on faces/selfies** — primary fallback for GPT Image 2
- Good quality for face generation, selfies, and character-based shots
- Generation time: ~60-90s
- Prompt framing for edits: use "recreate the first reference image with one change: [describe change]" rather than "edit" language

## Prop generation pattern (canonical environment matching)

When generating prop images that need to belong in an established environment:

1. **Always reference the canonical environment asset** via `referenceAssetIds` — pass the green-tagged location/room asset so the prop inherits matching surfaces, materials, and lighting
2. **Place the prop on the correct surface** — e.g. "on the cream couch cushion from the reference image", not on invented furniture. The prop must sit on surfaces visible in the canonical establishing shot
3. **Match the lighting** — check the reference environment's lighting (ambient daytime vs directional golden hour) and specify it explicitly in the prompt. Common correction: "even ambient daytime natural light, no harsh directional shadows"
4. **Frame as close-up prop shot** — zoom in tight on the prop as the sole subject, with just enough of the canonical surface (couch fabric, countertop) visible to anchor it to the environment
5. **Use `fal-ai` + `openai/gpt-image-2` for prop work with `referenceAssetIds`** — this is the only current path for referenced prop generation. ⚠️ Get the user's explicit approval before using this paid provider.
6. **If a character is visible in the shot, reference their character sheet** — include the character sheet as a `referenceAssetId` and specify "wearing the outfit from the character sheet" rather than describing individual wardrobe items. Missed details (robe color, slippers, glasses style) are common errors when describing from memory.

## Midjourney notes

- Uses Discord interactions API via BYOA wiring
- Successful interaction submit may return HTTP 204
- Poll channel messages for completed image/grid
- Preserve button/custom-id details in asset metadata when available
- User-token access has endpoint quirks; some single-message fetches fail where list polling works
- Token expiry is operationally common; 401 usually means refresh token

## Cross-links

- Load `athabasca-media-generation` for reference-edit workflows, Codex persistence constraints, and provider-selection guidance
- Load `athabasca-midjourney-prompting` for prompt authoring patterns
