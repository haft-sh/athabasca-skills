# Athabasca MJ Batch Generation via API

When generating many reference images for a Seedance-for-Storyboard project, submit MJ prompts sequentially through the Athabasca API with staggered delays to avoid Discord 429 rate limits.

## Why Sequential + Delay?

Discord's `/interactions` endpoint rate-limits rapid submissions. Submitting multiple MJ jobs within ~5s of each other triggers HTTP 429. The fix is 5–8s delays between submissions. A single 14-prompt batch takes ~15–25 minutes end-to-end (30–90s per MJ generation + 5s delays).

## Generic Bash Pattern

```bash
#!/bin/bash
API="http://localhost:3000/api/projects/${PROJECT_SLUG}/generate/image"
RESULTS_DIR="$HOME/.hermes/staging/${PROJECT_SLUG}/mj-results"
mkdir -p "$RESULTS_DIR"

generate() {
  local label="$1"
  local prompt="$2"
  local ar="$3"   # landscape | square | portrait (NOT 16:9 etc)

  echo "[$(date +%H:%M:%S)] Generating: $label"

  local body=$(jq -n \
    --arg provider "midjourney" \
    --arg model "midjourney-v8.1" \
    --arg prompt "$prompt" \
    --arg ar "$ar" \
    '{provider: $provider, model: $model, prompt: $prompt, aspectRatio: $ar}')

  local response
  response=$(curl -sS --max-time 180 -X POST "$API" \
    -H "Content-Type: application/json" \
    -d "$body") || {
    echo "FAILED (curl): $label" >&2
    return 1
  }

  local ok=$(echo "$response" | jq -r '.ok // false')
  if [ "$ok" = "true" ]; then
    local id=$(echo "$response" | jq -r '.asset.id')
    local url=$(echo "$response" | jq -r '.asset.publicUrl')
    echo "OK: $label → $id"
    echo "$response" | jq '.' > "$RESULTS_DIR/${label}-ok.json"
  else
    local err=$(echo "$response" | jq -r '.error // "unknown"')
    echo "FAILED: $label → $err" >&2
    echo "$response" | jq '.' > "$RESULTS_DIR/${label}-error.json"
  fi
}

# Generate one at a time with delay
generate "ref-01-title" "prompt text..." "landscape"; sleep 5
generate "ref-02-character" "prompt text..." "square";   sleep 5
generate "ref-03-environment" "prompt text..." "landscape"
```

## Critical: aspectRatio Enum Values

The Athabasca API `aspectRatio` field accepts only:
- `"landscape"` — maps to `--ar 16:9`
- `"square"` — maps to `--ar 1:1`
- `"portrait"` — maps to `--ar 9:16`

**Do NOT** pass `"16:9"`, `"1:1"`, or `"9:16"` — these cause validation errors and the generation silently fails.

## Running in Background

For 10+ prompt batches, run as a background process with notification:
```bash
bash scripts/project-mj-batch.sh &
# Monitor with:
process(action="poll", session_id="proc_XXXX")
```

## Post-Batch: Parse Results

```bash
OK_COUNT=$(ls "$RESULTS_DIR"/*-ok.json 2>/dev/null | wc -l)
ERR_COUNT=$(ls "$RESULTS_DIR"/*-error.json 2>/dev/null | wc -l)
echo "Success: $OK_COUNT | Failed: $ERR_COUNT"
```

## When Generation Times Out But Grid Exists in Discord

Athabasca MJ generation can time out at the API level while the Discord job succeeded. If you suspect this:
1. Check Discord channel directly for the grid message
2. Download the image from Discord CDN immediately (URLs expire)
3. Upload to Athabasca via `POST /api/projects/:slug/media`
4. Store `discordMessageId`, `discordChannelId`, `mjButtons` in `metadataJson`
5. Attach to the relevant shot

See also: `athabasca-midjourney-prompting` skill references `mj-direct-discord-recovery-and-persistence.md`