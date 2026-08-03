# Seedance 2.0 via fal.ai — operator notes

## Async generation pattern

`fal.subscribe()` uses a long-poll with a built-in timeout that can expire before Seedance 2.0 finishes (15s video typically takes 90–150s). When `subscribe()` times out, **the generation may have actually succeeded** on fal.ai's side.

**Recommended pattern: submit + poll**

```typescript
import { fal } from "@fal-ai/client";

// Step 1: Submit (non-blocking)
const submitResult = await fal.queue.submit("fal-ai/seedance-2/image-to-video", {
  input: { /* ... */ }
});
const requestId = submitResult.request_id;

// Step 2: Poll for completion
async function pollStatus(requestId: string, intervalMs = 10000, maxAttempts = 60) {
  for (let i = 0; i < maxAttempts; i++) {
    const status = await fal.queue.status("fal-ai/seedance-2/image-to-video", {
      requestId,
      logs: true
    });
    
    if (status.status === "COMPLETED") {
      return await fal.queue.result("fal-ai/seedance-2/image-to-video", { requestId });
    }
    if (status.status === "FAILED") {
      throw new Error(JSON.stringify(status));
    }
    await new Promise(r => setTimeout(r, intervalMs));
  }
  throw new Error("Timed out polling");
}
```

If `fal.subscribe()` appears to fail but you suspect it actually completed, check the fal.ai web UI for the result before re-running.

## Multi-image input

Seedance 2.0 image-to-video accepts a primary `image_url` and a `second_image_url` for multi-reference generations. The `@image1` and `@image2` tokens in the prompt correspond to the first and second image respectively.

Parameters:
- `image_url` — primary reference image (maps to `@image1` in prompt)
- `second_image_url` — secondary reference image (maps to `@image2` in prompt)

Do NOT use `image_urls` as an array — that parameter was rejected with a 422 validation error.

## Defaults (the user preferences)

- **Resolution:** `480p` (most affordable)
- **Audio:** `generate_audio: true`
- **Prompt suffix:** Always append `No Music` to the end of prompts. Music interferes with editing; the user adds it in post.
- **Quality text suffix (optional):** `4K, Ultra HD, Rich details, Sharp clarity, Cinematic texture, Natural colors, Stable picture No Music` — the user uses this as a prompt engineering experiment; the quality keywords are text-only guidance for the model, the actual resolution is still set by the `resolution` parameter.

## Duration

Seedance 2.0 supports `duration: "15"` for 15-second generations. This is the primary lane length for the prenup project.
