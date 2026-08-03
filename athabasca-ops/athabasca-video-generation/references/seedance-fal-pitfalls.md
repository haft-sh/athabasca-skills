# Seedance 2.0 via fal.ai — Agent Pitfalls

## Async subscribe vs submit+poll

`fal.subscribe()` **can timeout while the job succeeds server-side**. This was confirmed in practice: a 300s subscribe call timed out (exit 124) while the job was actively `IN_PROGRESS` and completed ~90s later on fal.ai's side.

**Recommended pattern for Seedance:**

1. Submit to queue (non-blocking):
```js
const submitResult = await fal.queue.submit("fal-ai/seedance-2/image-to-video", { input: { ... } });
// submitResult.request_id is the polling key
```

2. Poll every 10s via raw curl (reliable, no Bun timeout chain):
```bash
curl -sS "https://queue.fal.run/fal-ai/seedance-2/requests/{request_id}/status?logs=true" \
  -H "Authorization: Key $FAL_KEY"
# Poll until status = "COMPLETED" or "FAILED"
```

3. Fetch result:
```bash
curl -sS "https://queue.fal.run/fal-ai/seedance-2/requests/{request_id}" \
  -H "Authorization: Key $FAL_KEY"
```

**Why not `fal.subscribe()` for Seedance?** The subscribe call wraps queue.submit + queue.poll internally but uses its own timeout. For 15s Seedance clips (2-5 min generation), this timeout can fire before the job completes, leaving the agent thinking it failed when it actually succeeded.

## Single reference image constraint

fal.ai's Seedance 2.0 API supports **exactly two image inputs**:
- `image_url` (required) — the starting frame
- `end_image_url` (optional) — the ending frame for start-to-end transitions

There is **no `image_urls` array**, no `second_image_url`, no multi-reference support. The prompt's `@image1` / `@image2` markers are just text — the model only ever sees the starting image.

**Implication for prompt design:**
- Each Seedance generation uses exactly one reference image
- For multi-shot sequences, split into separate lanes (one gen per reference still)
- `end_image_url` can bridge two stills when you want a controlled transition between them

## Defaults (user preference)

- `resolution: "480p"` — most affordable, always default to this
- `generate_audio: true` — always on
- Append quality suffix + `"No Music"` to the end of every Seedance prompt:
  ```
  4K, Ultra HD, Rich details, Sharp clarity, Cinematic texture, Natural colors, Stable picture No Music
  ```
  The quality suffix is text-only (model ignores "4K" at 480p), but the user wants it included. "No Music" prevents Seedance from adding music that interferes with editing — music is added in post.

## Prompt strategy: short granular takes

**Do NOT use 15s multi-beat prompts.** Seedance struggles with long prompts that chain multiple shots/cuts. Instead:

- Split multi-image lanes into separate 4-8s takes
- Each lane gets one reference image and one coherent shot
- Cleaner interpolation, less character/setting drift
- The editor assembles the takes together

Typical durations: 3s (inserts) to 8s (establishing), with 5s being the sweet spot.

## Naming convention for i2v prompts

Use **"the man"** and **"the woman"** instead of character names ("Adrian", "Elena") in Seedance prompts. Character names can trigger drift or invented specifics. Keep descriptive visual cues (wardrobe, age range, emotional state) but drop proper names.

## Timeout expectations

Seedance 2.0 image-to-video for 15s clips typically completes within 2–5 minutes. With the submit+poll pattern, poll every 10s and wait up to 10 minutes before declaring a timeout.

## Node/Bun runtime

`@fal-ai/client` is ESM-only. Use `bun -e '...'` (not `bun run -e`, which tries to resolve a script file). The package is installed in the Athabasca repo (`/home/nrsimha/Sites/athabasca`). Run scripts from that directory so Node/Bun can resolve `node_modules`.

## Result structure

On success, the result contains:
```json
{
  "video": {
    "url": "https://...",
    "content_type": "video/mp4",
    "file_name": "video.mp4",
    "file_size": 4539430
  },
  "seed": 1025329039
}
```

If the call succeeds but `result.data` appears empty, check the fal.ai dashboard at fal.ai/dashboard — the job may have completed and the subscribe callback missed it due to a network blip.
