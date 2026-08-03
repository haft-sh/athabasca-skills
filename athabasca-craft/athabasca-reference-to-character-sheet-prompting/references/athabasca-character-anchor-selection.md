# Athabasca character anchor selection pattern

Use this when a user compares several character sheets and selects one as the final continuity anchor for a character.

## Pattern

1. Resolve the selected asset first:
   - `GET /api/media/:assetId`
   - Confirm it is the intended project and visible at `asset.publicUrl`.
2. Preserve existing `metadataJson` fields.
3. Patch the asset metadata through the project media endpoint:
   - `PATCH /api/projects/:slug/media/:assetId`
   - body: `{ "metadataJson": <merged object> }`
4. Recommended merged fields:
   - `characterName`
   - `characterRole` such as `male_lead` or `female_lead`
   - `characterAnchorStatus: "final"`
   - `isFinalCharacterSheet: true`
   - `finalizedForContinuityPass: true`
   - `supersedesAlternateAssetIds: [...]` when there were rejected alternatives
   - `decisionNote` with the user selection provenance
5. Verify with a fresh `GET /api/media/:assetId` and a `curl -I` against the public URL.

## Example

```bash
curl -sS http://127.0.0.1:3000/api/media/asset_... > /tmp/asset.json
python3 - <<'PY'
import json
asset=json.load(open('/tmp/asset.json'))['asset']
meta=json.loads(asset.get('metadataJson') or '{}')
meta.update({
  'characterName': 'Adrian',
  'characterRole': 'male_lead',
  'characterAnchorStatus': 'final',
  'isFinalCharacterSheet': True,
  'finalizedForContinuityPass': True,
  'supersedesAlternateAssetIds': ['asset_alternate...'],
  'decisionNote': 'the user selected this character sheet as the final male lead continuity anchor.',
})
open('/tmp/patch.json','w').write(json.dumps({'metadataJson': meta}))
PY
curl -sS -X PATCH \
  http://127.0.0.1:3000/api/projects/prenup/media/asset_... \
  -H 'Content-Type: application/json' \
  --data-binary @/tmp/patch.json
```

## Why this matters

Do not leave final character choices only in chat. The next storyboard regeneration pass should be able to discover the authoritative character anchors from project media metadata without rereading the conversation.
