# Document Versioning Pattern

When amending shot breakdowns, prompt lists, or other canonical documents in Athabasca:

## Workflow

1. **Download existing version** from R2 public URL to `/tmp/`
2. **Make targeted patches** using the `patch` tool (find-and-replace specific sections)
3. **Renumber downstream references** — when removing/adding items, update all subsequent numbered references (shot numbers, section headers, table rows, manifest entries)
4. **Upload as new asset** with version marker in title (e.g., "v2", "amended")
5. **Tag old version yellow** (`colorTag: "yellow"`) = superseded
6. **Tag new version green** (`colorTag: "green"`) = canonical
7. **Include supersession metadata** in `metadataJson`:
   ```json
   {
     "supersedesAssetId": "asset_xxx",
     "version": 2,
     "changes": "Brief description of what changed"
   }
   ```

## Key Pitfalls

- **Don't patch existing assets in place** — always create a new asset and mark the old one as superseded. This preserves version history.
- **Renumber everything** — when removing shot 109, shots 110-161 become 109-160. Miss one renumbering and cross-references break.
- **Check all reference points** — a shot number might appear in headers, inline notes, continuity anchors, and manifest tables. Search for the old number across the entire document before uploading.
- **Remove orphaned reference images** — when removing a shot that depended on a reference image (e.g., @image20), also remove that reference from: the reference manifest table, any group's reference images grid, and any Seedance prompt text that cites it. Orphaned references confuse future generation runs.
- **Category is `misc`** — Athabasca media API validates `category` against `research|moodboard|generated|inbox|misc`. Documents use `misc`.

## Example

```bash
# Download
curl -sS -o /tmp/shot-breakdown.md "https://media.example.com/<project-slug>/misc/existing.md"

# Patch
# (use patch tool for targeted edits)

# Upload new version
curl -sS -X POST "http://localhost:3000/api/projects/<project-slug>/media" \
  -F "file=@/tmp/shot-breakdown.md" \
  -F "phase=storyboard" \
  -F "category=misc" \
  -F "title=Shot Breakdown v2" \
  -F 'metadataJson={"supersedesAssetId":"asset_old","version":2}'

# Tag
curl -X PATCH ".../media/asset_new" -d '{"colorTag":"green","ratingStars":5}'
curl -X PATCH ".../media/asset_old" -d '{"colorTag":"yellow"}'
```
