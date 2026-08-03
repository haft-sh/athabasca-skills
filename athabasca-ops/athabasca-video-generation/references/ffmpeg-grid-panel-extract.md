# ffmpeg Panel Extraction from Storyboard Grids

When running i2v comparisons using a storyboard grid as source rather than a single reference image, extract the target panel first.

## Pattern

1. Download the grid image
2. Determine grid dimensions such as 3×3 or 2×2
3. Use `ffmpeg -vf "crop=W:H:X:Y"` to extract the target panel
4. Upload the extracted panel to Athabasca via `POST /api/uploads`
5. Use the returned `asset.publicUrl` or asset ID in the generation request

## Coordinates for a 3×3 Grid

| Panel | X offset | Y offset |
|-------|----------|----------|
| S1 top-left | `0` | `0` |
| S2 top-center | `W/3` | `0` |
| S3 top-right | `2*W/3` | `0` |
| S4 mid-left | `0` | `H/3` |
| S5 mid-center | `W/3` | `H/3` |
| S6 mid-right | `2*W/3` | `H/3` |
| S7 bot-left | `0` | `2*H/3` |
| S8 bot-center | `W/3` | `2*H/3` |
| S9 bot-right | `2*W/3` | `2*H/3` |

## Generic Example Commands

```bash
# 1. Download grid
curl -sL "https://media.example.com/project/generated/storyboard-grid.png" -o /tmp/storyboard-grid.png

# 2. Check dimensions
file /tmp/storyboard-grid.png
# Example: PNG image data, 1024 x 1024, 8-bit/color RGB

# 3. Extract S1 (top-left) from a 3x3 grid
ffmpeg -i /tmp/storyboard-grid.png -vf "crop=341:341:0:0" -frames:v 1 -y /tmp/storyboard-panel-s1.png 2>&1 | tail -2

# 4. Upload
curl -sS http://localhost:3000/api/uploads \
  -F "file=@/tmp/storyboard-panel-s1.png" \
  -F "projectSlug=project-slug" \
  -F "phase=storyboard" \
  -F "category=generated" \
  -F "sourceKind=generated" \
  -F "title=Storyboard panel extract - S1" \
  -F "provenanceNote=Extracted panel S1 from a storyboard grid for i2v comparison"
```

## Key Constraints

- `sourceKind` only accepts valid enum values such as `telegram_upload`, `web_import`, `generated`, `manual`, or `api_upload`; do not invent a new one like `"extracted"`
- The upload endpoint is `/api/uploads`, not `/api/upload`
- For JSON generation requests, prefer a temp `.json` file and `curl -d @/tmp/file.json` to avoid escaping bugs
- Generation `duration` must be a JSON number, not a quoted string

## Anti-Bloat Rule

Keep only the extraction method here. Do not preserve one production's full grid URLs, shot titles, or panel inventory in this reference file.