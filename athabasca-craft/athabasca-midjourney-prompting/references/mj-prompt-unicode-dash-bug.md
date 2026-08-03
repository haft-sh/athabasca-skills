# MJ Prompt Poller — Unicode Em Dash Bug

**Discovered:** 2026-05-14
**File:** `src/server/workers/midjourney-provider.ts`
**Function:** `normalizePromptForMatch`

## Symptom

Athabasca logs `Timed out waiting for Midjourney image after 180s` but the grid image exists in Discord and has U1-U4/V1-V4 buttons. The poller never matched the prompt.

## Root Cause

Discord strips unicode dashes from message content before echoing back. A submitted prompt like:

```
...desert stone gateway — Turto has bright...
```

Gets echoed in the Discord message as:

```
...desert stone gateway Turto has bright...
```

The `normalizePromptForMatch` function strips leading image URLs, `**` markdown, `--` parameters, collapses whitespace, and lowercases — but it did NOT normalize unicode dash characters. So:

- **Normalized submitted prompt:** `...gateway — turto has...` (em dash still present)
- **Normalized Discord content:** `...gateway turto has...` (em dash gone)
- **Result:** `includes()` returns `false` → poller continues → timeout

## The Fix

Add unicode dash normalization to `normalizePromptForMatch`:

```typescript
function normalizePromptForMatch(value: string): string {
  return stripLeadingImagePromptUrls(value)
    .replace(/\*\*/g, "")
    // Normalize unicode dashes to space (Discord strips them before echoing)
    .replace(/[\u2014\u2013\u2012\u2015]/g, " ")
    // Remove -- parameters
    .replace(/--\S+(?:\s+\S+)?/g, "")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase();
}
```

## Characters Affected

| Code Point | Name | Appearance |
|---|---|---|
| U+2014 | Em dash | — |
| U+2013 | En dash | – |
| U+2012 | Figure dash | ‒ |
| U+2015 | Horizontal bar | ― |

Any prompt containing these characters is at risk. The prompt authoring skill often uses `—` (em dash) as a natural separator in descriptive text, making this a common failure mode, not an edge case.

## Debug Checklist When MJ "Timeouts" Appear

1. `curl` the Discord channel messages: `GET /channels/:id/messages?limit=5`
2. Look for a Midjourney Bot message with the prompt text and U1-U4 buttons
3. If found, compare submitted prompt `—` vs Discord echo (missing `—`)
4. Patch `normalizePromptForMatch` if not already fixed
5. Download the image from the Discord CDN URL immediately (URLs expire)
6. Persist through Athabasca media API

## Patch Safety Note

When applying sequential patches to `midjourney-provider.ts` in the same turn, always `read_file` the affected function first. Overlapping patches on the same `old_string` region create duplicate function bodies with syntax errors. The file needs a clean read between patch rounds.
