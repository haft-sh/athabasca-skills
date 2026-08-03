# Midjourney Polling Fallback: MJ Private API

## Problem
Discord channel message polling is fragile due to:
- URL rewriting (`s.mj.run` breaks prompt matching)
- Unicode em dash stripping by Discord
- Stale grid reuse from nonce collisions
- Bot-only endpoint restrictions (`GET /channels/:id/messages/:msg_id`)

## Alternative: MJ `recent-jobs` API

Direct query to Midjourney's own job system, bypassing Discord entirely.

```
GET https://www.midjourney.com/api/app/recent-jobs/?amount=50&jobType=null&orderBy=new&jobStatus=completed&userId=${MJ_USER_ID}&dedupe=true&refreshApi=0
```

### Known values
- `userId = 239593244479488001` (the automated MJ account's user ID)
- `amount`: number of recent jobs to return (max tested: 50)
- `jobStatus`: `completed`, `running`, `pending`, `failed`
- `orderBy`: `new`, `old`

### Response shape
Returns an array of job objects with:
- `id`: job identifier
- `prompt`: the full prompt string
- `imageUrl`: completed image URL
- `status`: job status
- `createdAt`: timestamp
- `type`: job type (imagine, upscale, variation, reroll)

### Usage pattern
1. After submitting `/imagine` via Discord interactions API, poll this endpoint instead of Discord channel messages
2. Match by prompt substring (the descriptive body, not leading URLs)
3. Extract `imageUrl` directly from the job object
4. Download and persist to R2

### Tradeoffs
- **Pro**: No Discord URL rewriting issues, no em dash stripping, no stale grid matching
- **Con**: Private API — could break without notice; requires the MJ account's userId; may have rate limits
- **Con**: Does not provide button `custom_id`s for future upscaling — you'd still need Discord message polling for that

### When to use
- As fallback when Discord polling is unreliable
- For quick validation/prototyping where upscaling isn't needed
- For batch status checks without Discord API complexity

### Auth
No auth header needed — the endpoint is public for any userId. However, rate limiting may apply if hit aggressively.
