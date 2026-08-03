# Midjourney Polling Bug: Stale Grid Returns

## Problem

When generating multiple Midjourney images sequentially via the Athabasca BYOA provider,
subsequent API calls returned the *previous* grid image instead of the new one.

## Root Cause

`pollForGridImage()` in `src/server/workers/midjourney-provider.ts` matched messages by:

```typescript
if (contentLower.includes(promptSnippet) || msg.content?.includes("--")) {
```

This is fatally loose because **every MJ message contains `--`** (params like `--ar 16:9`).
So on the second generation, the poller found the first generation's grid (only seconds old)
and returned it immediately.

## Why nonce matching didn't work

Midjourney echoes the nonce in the initial "Thinking..." interaction response, but:
- The final grid message does **not** contain the nonce
- The progress embed messages also don't contain it
- The grid is delivered as a separate message without the nonce in content

## Working fix: submit-time gating

Record `submitTime` after POST 204, then:
1. Wait 5s for MJ to start processing
2. On poll, skip any message with timestamp < submitTime - 3s (clock skew margin)
3. The first message at or after submitTime locks us to our job
4. After lock, accept the first grid attachment on any subsequent message

```typescript
const submitTime = Date.now();
await new Promise((r) => setTimeout(r, 5_000));

let seenInitialResponse = false;
// In poll loop:
if (!seenInitialResponse) {
  if (msgTime < submitTime - 3_000) continue;
  seenInitialResponse = true;
  // ... check this message for grid
}
// Phase 2: after lock, accept first grid attachment
if (msg.attachments?.[0]?.url) return { imageUrl: msg.attachments[0].url, ... };
```

## Symptoms

- Generation returns in ~4-5s instead of 10-15s
- Identical SHA256 hash as previous generation
- Same file content as prior image

## Location

`src/server/workers/midjourney-provider.ts` → `pollForGridImage()`

## Date

Validated and patched: 2026-05-13
