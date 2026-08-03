# MJ Batch Generation + Visual Eval + Upscale Pipeline

End-to-end workflow for generating 10+ reference images via Midjourney, evaluating grids, selecting best quadrants, upscaling, and persisting to Athabasca.

Validated May 2026 on George project (14 MJ references + 6 Gemini character sheets).

## Phase 1: Batch Generation

Write a shell script (`scripts/<project>-mj-batch.sh`) that fires all prompts sequentially with 5s delays:

```bash
generate() {
  local label="$1" prompt="$2" ar="$3"
  curl -sS --max-time 120 -X POST "http://localhost:3000/api/projects/<slug>/generate/image" \
    -H "Content-Type: application/json" \
    -d "{\"provider\":\"midjourney\",\"model\":\"midjourney-v8.1\",\"prompt\":$prompt,\"aspectRatio\":$ar}"
}

generate "image02-room" "prompt text..." "landscape"
sleep 5
generate "image03-prop" "prompt text..." "square"
# ...
```

**Critical:** Use Athabasca `aspectRatio` enum values: `landscape`, `square`, `portrait` — NOT `16:9`, `1:1`, `9:16`. The API validates against the enum and rejects raw ratios.

Run as background process with `notify_on_complete`:
```bash
bash scripts/<project>-mj-batch.sh  # background=true, notify_on_complete=true
```

Store results in `~/.hermes/staging/<project>/mj-results/` with `<label>-ok.json` or `<label>-error.json`.

## Phase 2: Visual Evaluation

Download all grids locally (save as `.webp` — MJ grids are WebP regardless of extension):
```python
for f in results:
    curl -sS -L -o f"{label}.webp" asset["publicUrl"]
```

Use `vision_analyze` on each grid. Ask for per-quadrant ratings (1-10) on:
- Composition adherence to prompt
- Lighting quality / mood
- Detail accuracy (props, architecture, etc.)
- Cinematic quality
- Any issues (extra people, wrong mood, AI hallucinations)

Build a summary table:

| # | Subject | Best Q | Score | Notes |
|---|---------|--------|-------|-------|
| 2 | Room | TL | 10/10 | Perfect perspective |
| ... | | | | |

Present to user for approval before upscaling.

## Phase 3: Recover mjButtons

API-generated grids frequently have empty `metadataJson.mjButtons`. Recover from Discord:

```typescript
// Fetch recent messages (limit=50)
const messages = await fetch(`https://discord.com/api/v9/channels/${CHANNEL_ID}/messages?limit=50`);

// Match by prompt content substring in message content
const match = messages.find(m => 
  m.components?.length > 0 && 
  m.content?.toLowerCase().includes(keyword)
);

// Extract button custom_ids
for (const row of match.components) {
  for (const btn of row.components) {
    if (btn.custom_id.startsWith("MJ::JOB::upsample::")) 
      buttons[`U${btn.custom_id.split("::")[3]}`] = btn.custom_id;
  }
}
```

Save to `mj-buttons.json` for batch upscale submission.

## Phase 4: Submit Upscales

Submit best-quadrant upscaling via Discord interactions API:

```typescript
await fetch("https://discord.com/api/v9/interactions", {
  method: "POST",
  headers: { Authorization: TOKEN, "Content-Type": "application/json" },
  body: JSON.stringify({
    type: 3,
    application_id: "936929561302675456",
    channel_id: CHANNEL_ID,
    message_id: gridMsgId,
    session_id: makeSessionId(),
    nonce: makeNonce(),
    data: { component_type: 2, custom_id: buttons["U1"] }  // or U2/U3/U4
  })
});
// Response: 204 No Content
```

Stagger submissions by 1.5s to avoid Discord 429 rate limits.

## Phase 5: Download + Persist Upscales

**Critical detection fix:** Upscaled messages in Discord have `comp=3` (they retain U/V buttons), NOT `comp=0`. Filtering for `comp=0` will miss all upscales.

Instead, match by snowflake ID proximity:
```typescript
// Upscaled message has: 1 attachment + prompt text in content
// Match by snowflake ID > grid message ID
const upscaled = messages.find(m => 
  m.attachments?.length === 1 &&
  m.id > gridMessageId &&
  m.content?.includes(promptSnippet)
);
```

Download attachments (save as `.webp`), then upload to Athabasca:

```bash
curl -X POST http://localhost:3000/api/projects/<slug>/media \
  -F file=@upscale.webp \
  -F phase=storyboard \
  -F category=generated \
  -F sourceKind=generated \
  -F 'title=@imageN: Subject Name (UN)' \
  -F 'provenanceNote=Midjourney V8.1 upscale, best quadrant UN. ...' \
  -F 'metadataJson={"artifactKind":"mj_upscale","refNum":N,"quadrant":"UN","model":"midjourney-v8.1","style":"live-action-cinematic"}'
```

## Phase 6: Character Sheets (Non-MJ)

Route character turnaround sheets to Gemini (or GPT Image 2 when available):
- **Gemini:** Use **concise prompts** (under 50 words). Long prompts silently fail with "no inline image data."
- **GPT Image 2:** Best for character sheets but rate-limited on Plus plan. Check `resets_at` timestamp.
- **MJ:** Poor at character sheets (messy backgrounds, no clean white). Avoid.

Concise Gemini pattern:
```
Character turnaround sheet, white background. Heavyset man 77, white beard, glasses, bathrobe, bunny slippers. Four views: front, left 3/4, right 3/4, back. Full body. Even studio lighting.
```

## Script Persistence

Save batch scripts in the project repo (`scripts/`), not `/tmp`. `/tmp` gets cleaned periodically. Scripts are project-specific reference material worth keeping for future iterations or similar projects.

## Timing Expectations

- MJ grid generation: ~15s per prompt (via BYOA Discord)
- 14 grids: ~4 minutes total
- Upscale submission: ~2 seconds per interaction
- Upscale rendering: ~30-60s per image
- Download + Athabasca upload: ~3s per image
- Gemini generation: ~20s per prompt
- Total pipeline for 20 references: ~15-20 minutes
