# GPT Image 2 Provider Routing — Canonical Rule (June 2026)

## The Rule

**`openai-codex` is the PRIMARY provider for GPT Image 2.** the user's OpenAI subscription includes unlimited image generation — no per-image cost. `fal-ai` is a **paid fallback** that requires explicit the user approval before any use.

This rule has **zero exceptions** for routine work. Even when `referenceAssetIds` is required (Codex doesn't support it in v1), you must state the constraint and get the user's explicit permission before routing to `fal-ai`.

## Backup Chain

```
openai-codex (primary, free) → fal-ai (⚠️ paid, the user approval required) → replicate → byteplus
```

All three fallback providers (`fal-ai`, `replicate`, `byteplus`) serve `openai/gpt-image-2` — identical model, identical output quality.

## Why This Matters

| Provider | Cost | Rate Limits |
|---|---|---|
| `openai-codex` / `gpt-image-2` | Free (via the user's OpenAI subscription) | Plan-level (5-hour and weekly rolling caps) |
| `fal-ai` / `openai/gpt-image-2` | Per-image (~$0.01–$0.41 depending on quality tier) | Per-request credits |
| `replicate` / `openai/gpt-image-2` | Per-image | Polling-based, 120s timeout |
| `byteplus` / `openai/gpt-image-2` | Per-image | Polling-based, 120s timeout |

## The `referenceAssetIds` Exception

`openai-codex` does not support `referenceAssetIds` in v1. When a composite or edit pass requires a reference image:

1. State the constraint: "This shot needs an edit pass with `referenceAssetIds`. `openai-codex` doesn't support that, so the capability path routes through `fal-ai`."
2. Ask explicitly: "Can I use `fal-ai` for this shot? It costs ~$0.04–$0.41 per image."
3. Only proceed after the user approves.

**Do not silently default to `fal-ai`** because it's the only way to make the API call work. The constraint is real but the paid cost requires permission.

## Provider/Model Reference

| Provider | Model | Primary? | Reference Support |
|---|---|---|---|
| `openai-codex` | `gpt-image-2` | ✅ Primary | ❌ No refs in v1 |
| `fal-ai` | `openai/gpt-image-2` | ❌ Paid fallback | ✅ Via `/edit` endpoint |
| `replicate` | `openai/gpt-image-2` | ❌ Backup | ❌ No |
| `byteplus` | `openai/gpt-image-2` | ❌ Backup | ❌ No |
| `replicate` | `bytedance/seedream-5-lite` | Animal likeness | ✅ Up to 14 refs |

## Common Mistake to Avoid

❌ **Wrong:** "GPT Image 2 via `fal-ai` is preferred for composite work."
✅ **Correct:** "GPT Image 2 via `openai-codex` is primary. `fal-ai` is the paid fallback — get the user's approval."

This mistake was introduced in PR #125 and corrected in the same PR. Any skill that says `fal-ai` is preferred or primary for GPT Image 2 work is wrong.
