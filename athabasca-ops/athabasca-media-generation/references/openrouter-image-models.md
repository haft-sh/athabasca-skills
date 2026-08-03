# OpenRouter Image Generation Models — Quick Reference

## Available Models

| Display Name | OpenRouter Model ID | Reference Image | Best For |
|---|---|---|---|
| Nano Banana Pro | `google/gemini-3-pro-image-preview` | ❌ No | Prompt-driven concept art; strong reasoning + multimodal |
| Seedream 4.5 | `bytedance-seed/seedream-4.5` | ❌ No | Composition, typography, text rendering; $0.04/image flat |

## Request Template

```python
import json, base64, urllib.request
from dotenv import dotenv_values

env = dotenv_values("/path/to/.env")          # key lives in profile .env
OR_KEY = env.get("OPENROUTER_API_KEY", "")

body = {
    "model": "bytedance-seed/seedream-4.5",    # or google/gemini-3-pro-image-preview
    "modalities": ["image"],
    "messages": [{"role": "user", "content": PROMPT}]
}

req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=json.dumps(body).encode(),
    headers={
        "Authorization": f"Bearer {OR_KEY}",
        "Content-Type": "application/json",
    },
    method="POST"
)
with urllib.request.urlopen(req, timeout=120) as resp:
    result = json.loads(resp.read())
```

## Response Extraction

```python
# Images are in message.images, NOT message.content
msg = result["choices"][0]["message"]
images = msg.get("images") or []

if images:
    data_url = images[0]["image_url"]["url"]   # "data:image/jpeg;base64,/9j/..."
    _, b64 = data_url.split(",", 1)
    raw = base64.b64decode(b64)
    Path("output.jpg").write_bytes(raw)
```

**Why not `content`?** — OpenRouter text models embed base64 images in `content`. Image models (Seedream, Gemini 3 Pro Image Preview) use the dedicated `images` array. Checking `content` first is the wrong extraction order.

## API Key Loading

```python
# ❌ os.environ.get() — fails in subprocesses / heredocs
import os
os.environ.get("OPENROUTER_API_KEY")   # None

# ✅ dotenv_values — reads the profile .env file
from dotenv import dotenv_values
env = dotenv_values("/home/nrsimha/.hermes/profiles/cliphouse/.env")
OR_KEY = env["OPENROUTER_API_KEY"]
```

## Nano Banana Pro (Gemini 3 Pro Image Preview) Notes

- Provider: Google AI via OpenRouter
- Context: 66K total / 32.8K max output
- Input: ~$2/M tokens · Output: ~$12/M tokens (high variance due to image generation)
- Strengths: multimodal reasoning, natural language-driven image generation, identity preservation (up to 5 subjects), 2K/4K outputs, Google Search grounding
- Does NOT accept reference images — purely text-to-image
- Athena native route uses `google-gemini` provider which maps to this model; prefer the native route for animated storyboard/grid projects

## Seedream 4.5 Notes

- Provider: ByteDance via OpenRouter
- Flat rate: **$0.04 per output image** regardless of size
- Context: 4K
- Strengths: composition, typography, small text rendering, portrait refinement, editing consistency
- Does NOT accept reference images — purely text-to-image
- Useful when you want high-quality composition without reference conditioning

## Reference Image Edit Workflow

Both models on OpenRouter are text-to-image only. For edits from existing assets, the workflow is:

1. Generate a new image from the model with the edit prompt
2. Upload the result to Athabasca via `POST /api/projects/:slug/media`
3. Store `sourceAssetId` in `metadataJson` for provenance

If reference-image editing is required, use the Hermes `image_generate` tool (which DOES support `reference_images`) as the fallback path.