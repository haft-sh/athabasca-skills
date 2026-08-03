# Media ID Fast Path

Use when the user provides a concrete Athabasca media asset ID like `asset_...`.

## Preferred route

`GET /api/media/:assetId`

Returns the enriched asset payload directly, including:
- top-level asset metadata
- `attachments`
- `generation`

## Why this exists

This avoids ad hoc SQL for routine inspection tasks like:
- finding the backing project for an asset
- reading `publicUrl`
- checking whether the asset is video/audio/document
- discovering attachment target context
- reading generation prompt/provider/model metadata

## Typical follow-on actions

After lookup, common actions are:
1. extract audio from `publicUrl`
2. upload a derived file back to the same project
3. inspect `generation.prompt` or provider/model provenance
4. attach/detach from shots or project contexts

## Escalate beyond the fast path only when
- the route is failing
- the needed field is not present in the response
- the user asks for broader project-wide context rather than one asset
