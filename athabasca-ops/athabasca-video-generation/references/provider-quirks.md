# Provider quirks and failure classification

## Alibaba Cloud / DashScope video

### Wan 2.7 reference-to-video (`wan2.7-r2v`)

Observed working normalized mapping from Athabasca to Alibaba:

- `mode: reference-to-video`
- send `input.media`, not `input.reference_urls`
- mixed reference payload should use typed entries:
  - `reference_image`
  - `reference_video`
- `parameters.size` should still be set from normalized resolution + aspect for `wan2.7-r2v`

Working conceptual payload shape:

```json
{
  "model": "wan2.7-r2v",
  "input": {
    "prompt": "...",
    "media": [
      { "type": "reference_image", "url": "https://...image.jpg" },
      { "type": "reference_video", "url": "https://...reference.mp4" }
    ]
  },
  "parameters": {
    "resolution": "720P",
    "duration": 7,
    "size": "1280*720"
  }
}
```

Failure signatures seen during live debugging:

- `Field required: input.media`
  - cause: adapter sent `input.reference_urls`
- `Input should be 'reference_image', 'reference_video' or 'first_frame': input.media.1.type`
  - cause: adapter used `video` instead of `reference_video`

Interpretation:
- treat both as adapter / payload-shape bugs, not prompt-quality failures
- if a prompt is otherwise valid and these exact upstream errors appear, fix Athabasca code/tests before retrying generation

### Audio-conditioned comparison workaround for r2v

When comparing an image-conditioned i2v clip against `wan2.7-r2v`, a practical reference-video workaround is:

1. download the dialogue audio reference
2. wrap it in a black 16:9 MP4 with ffmpeg
3. upload that wrapper through Athabasca media APIs
4. use it as `referenceVideoUrls[0]`
5. keep the actual visual identity/composition image in `referenceImageUrls`

This gives `wan2.7-r2v` a legal reference-video input without making a non-canonical local file the generation source.

Example ffmpeg pattern is documented in `references/black-screen-audio-wrapper.md`.
