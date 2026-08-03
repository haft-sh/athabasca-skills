# Wan 2.7 reference-to-video input notes

Session-derived fix from Shot 3 comparison regeneration on 2026-05-07.

## Confirmed working pattern

For `provider=alibaba-cloud` + `model=wan2.7-r2v`, Athabasca must send:

```json
{
  "model": "wan2.7-r2v",
  "input": {
    "prompt": "...",
    "media": [
      { "type": "reference_image", "url": "https://.../character.jpg" },
      { "type": "reference_video", "url": "https://.../timing-reference.mp4" }
    ]
  },
  "parameters": {
    "resolution": "720P",
    "duration": 7,
    "size": "1280*720"
  }
}
```

## Important failure signatures

Observed bad payload/error sequence while debugging:

1. Using `input.reference_urls` for `wan2.7-r2v` failed with:
   - `Field required: input.media`

2. Switching to `input.media` but using `type: "video"` failed with:
   - `Input should be 'reference_image', 'reference_video' or 'first_frame': input.media.1.type`

3. Working fix:
   - use `type: "reference_image"` for still references
   - use `type: "reference_video"` for video references

## Audio-conditioning workaround

If the creative intent depends on a voice line or audio timing, and the route exposes `referenceVideoUrls` rather than raw audio conditioning for `reference-to-video`:

1. download the canonical uploaded audio asset
2. build a black-screen 16:9 MP4 wrapper with ffmpeg
3. upload that wrapper back into Athabasca via `/api/projects/:slug/media`
4. pass the uploaded MP4 in `referenceVideoUrls`

Example ffmpeg command used successfully:

```bash
ffmpeg -y \
  -f lavfi -i color=c=black:s=1280x720:r=24 \
  -i captain-dialogue.mp3 \
  -c:v libx264 -pix_fmt yuv420p -preset veryfast \
  -c:a aac -b:a 192k \
  -shortest captain-dialogue-black-16x9.mp4
```

## Verification checklist

- capability endpoint still advertises `wan2.7-r2v` under `alibaba-cloud`
- uploaded reference video is Athabasca-hosted, not a tmp/local path
- generated clip lands in phase `clips`
- `shotId` produces a shot attachment
- public URL returns HTTP 200
