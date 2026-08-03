# Replicate Provider Notes

## API

- **Base URL**: `https://api.replicate.com/v1`
- **Auth**: `Authorization: Token <REPLICATE_API_KEY>`

### Create prediction

```
POST /v1/predictions
Body: {
  version: "<model-version-id>",
  input: {
    prompt: "...",
    duration: 4,        // 4s / 8s / 10s
    aspect_ratio: "16:9", // 16:9 / 9:16 / 1:1
    image: "https://..."  // i2v only: URL to source image
  }
}
→ { id: "pred_...", status: "starting" }
```

### Poll for result

```
GET /v1/predictions/:id
→ { status: "succeeded" | "failed" | "processing", output: ["https://video.mp4"], error: {...} }
```

Poll interval: 5s. Max attempts: ~120 (10 minutes timeout).

## Seedance 2.0 on Replicate

- **Model ID**: `bytedance/seedance-2.0`
- Same model ID for both t2v and i2v — mode is determined by presence of `input.image`
- **i2v**: always supply `input.image` URL (upload through Athabasca first, use returned `asset.publicUrl`)
- **t2v**: `input.prompt` only
- Replicate returns video URL in `output[0]` on success
- Version pinning: fetch stable version from `https://replicate.com/model/bytedance/seedance-2.0` or pin to known version ID

## the user Seedance defaults (apply to Replicate too)

- `resolution: "480p"` — most affordable
- `generate_audio: true` — always on
- Append `"No Music"` to every prompt (music interferes with editing)
- Quality suffix: `4K, Ultra HD, Rich details, Sharp clarity, Cinematic texture, Natural colors, Stable picture No Music`
- Use short 4–8s granular takes instead of 15s multi-beat prompts
- Use "the man" / "the woman" instead of character names
- Runtime pitfall observed 2026-06-05: Replicate Seedance 2.0 rejected `duration: 3` with `Duration must be between 4 and 15 seconds, or -1 for intelligent duration` even though Athabasca capabilities advertised 1–15. If the user explicitly asks for 3s Seedance, use BytePlus Seedance (`provider: "byteplus"`, model `dreamina-seedance-2-0-260128`) or update capability validation before trying Replicate.

## Replicate vs fal.ai for Seedance

Same underlying Seedance 2.0 model. Replicate adds async polling overhead vs fal.ai's subscribe/notify pattern. Use Replicate when:
- the user specifically requests it
- fal.ai is at capacity or the user's fal.ai quota is exhausted

Use fal.ai as default for Seedance (established default, faster polling via webhook).