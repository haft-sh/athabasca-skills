# Speaker-split derivative clips from Telegram-cached or uploaded video

Use this note when the user asks to split a clip into separate speaker beats and attach the parts back to Athabasca.

## What changed in this session

Initial mistake:
- a split near 11.0s was acceptable by rough ASR / timing cues but visually late
- the user explicitly corrected the method: use the video and the major frame/speaker-emphasis change, not audio

Key lesson:
- when the user asks for a precise cut based on who is speaking, visual speaker handoff beats audio transcript alignment
- the right method is to localize roughly, then inspect a dense contact sheet around the transition and cut on the first clearly shifted frame/emphasis beat

## Practical workflow

1. Identify the exact source clip.
   - If multiple Telegram-cached videos exist and the source is not obvious, ask for resend rather than guessing.
2. Narrow the search window.
   - Optional rough tools: `ffprobe`, `silencedetect`, ffmpeg `asr` with PocketSphinx if Whisper is unavailable.
   - Treat these only as coarse localization.
3. Generate a dense contact sheet around the suspected transition.
   - Example used here: 9.0s to 11.75s at 4 fps.
4. Ask vision to identify:
   - the last frame where the first speaker still visually leads
   - the first frame where the responder visibly becomes the active speaker / the camera emphasis shifts
5. Use the first clear responder frame as the practical cut.
6. Encode provenance honestly:
   - `splitBasis: visual_speaker_handoff`
   - `splitTimeSeconds: <cut>`
   - `derivedFromAssetId: <source>`
7. Upload both derivatives through Athabasca media API and verify attachments.

## Example command pattern

Create dense contact sheet around transition:

```bash
ffmpeg -y -ss 9.0 -i "$VIDEO" -t 2.75 \
  -vf "fps=4,scale=220:-1,drawtext=text='%{pts\\:hms}':x=8:y=h-26:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.7,tile=3x4:padding=12:margin=12:color=white" \
  -frames:v 1 /tmp/contact.jpg
```

Create corrected split once the visual cut is known:

```bash
ffmpeg -y -i "$SRC" -t 10.0 -c:v libx264 -preset veryfast -crf 18 -c:a aac -movflags +faststart captain.mp4
ffmpeg -y -i "$SRC" -ss 10.0 -c:v libx264 -preset veryfast -crf 18 -c:a aac -movflags +faststart soldier.mp4
```

## Session-specific outcome

Source clip:
- `asset_mow7su65vu0cm9jv`
- `video_eee09e3da401.mp4`

Refined visual finding:
- transition bracketed between `9.75s` and `10.00s`
- best practical cut: `10.00s`

Corrected uploaded derivatives:
- captain v2: `asset_mowfs9gpcfgk6m2h`
- soldier v2: `asset_mowfsax9o0ucbjkn`

## Wording guidance

Good:
- "I redid it using video only. The visual handoff is between 9.75s and 10.00s, so I used 10.0s."

Bad:
- "This is precise diarization."
- "The transcript proves the exact boundary."
