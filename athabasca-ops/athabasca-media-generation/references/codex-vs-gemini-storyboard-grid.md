# Codex vs Gemini storyboard grid comparison notes

## Codex / GPT-Image-2 (Hermes-native)
- Tool: `image_generate` with provider=openai-codex, model=gpt-image-2-medium
- Output: local PNG at ~1536x1024 (landscape)
- Persists: manual curl upload to POST /api/projects/:slug/media
- Rate limit: plus-tier usage limit ~80 min reset window
- Grid style: polished, good at matching a prior approved storyboard aesthetic
- Panel numbers: readable but sometimes stylized/artistically placed
- Aspect ratio: native `landscape` = 1536x1024

## Gemini 3 Pro (Nano Banana Pro via Athabasca API)
- Endpoint: POST /api/projects/:slug/generate/image
- Provider: google-gemini, model=gemini-3-pro-image-preview
- Output: the userEG at ~2752x1536, auto-persisted to Athabasca media
- Rate limit: separate quota; no Codex 429 collision
- Grid style: slightly different render, comparable quality
- Panel numbers: supports, may place differently than Codex
- Aspect ratio: accepts "landscape"/"square"/"portrait" — NOT "16:9"
- References: accepts referenceAssetIds array
- Provenance: metadata includes seed, original size, provider, model

## When to use which
- Default: GPT-Image-2 for grid generation (best style continuity)
- Fallback: Gemini when Codex hits 429 rate limit
- Comparison: run same prompt through both for A/B selection
