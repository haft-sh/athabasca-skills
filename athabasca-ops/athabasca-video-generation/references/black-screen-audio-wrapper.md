# Black-Screen Audio Wrapper for i2v Input

## When to use

When the user wants to use an audio track as the sole creative input to an image-to-video (i2v) model — e.g., Kling, Seedance, or similar — and needs a valid video file as the "first frame" carrier.

The model sees a single black frame and generates motion driven entirely by the audio track (if audio-conditioned) or by the prompt.

## Recipe

```bash
# Probe audio duration first
ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 audio.mp3

# Generate 640x360 (16:9) black video with audio track
ffmpeg -y \
  -f lavfi -i color=c=black:s=640x360:r=24 \
  -i audio.mp3 \
  -c:v libx264 -pix_fmt yuv420p -tune stillimage \
  -c:a aac -b:a 128k \
  -shortest \
  output.mp4
```

## Key flags

| Flag | Why |
|---|---|
| `-tune stillimage` | x264 optimizes for a static frame — tiny file, one keyframe |
| `-shortest` | Truncates video to match audio duration |
| `r=24` | Standard frame rate; i2v models expect typical video rates |
| `pix_fmt yuv420p` | Required for H.264 compatibility with all players/models |

## Resolution options

- **640x360** — default, smallest/fastest, good for most i2v models
- **1280x720** — if the model expects 720p minimum (e.g., Kling requires 720p)
- **1920x1080** — only if explicitly requested

## Verification

```bash
ffprobe -v error -show_entries stream=codec_name,width,height,duration \
  -of json output.mp4
```

Confirm:
- Video: h264, correct resolution, duration ≈ audio duration
- Audio: aac (or original codec if copied), same duration

## Upload to Athabasca

After generating, upload via `POST /api/projects/:slug/media` with:
- `phase=clips` (or `visual_dev` for reference)
- `category=misc`
- `sourceKind=manual`
- `title=...`
- `provenanceNote=Black-screen audio wrapper for i2v generation`
