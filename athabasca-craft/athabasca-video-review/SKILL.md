---
name: athabasca-video-review
description: Review generated Athabasca videos by inspecting frames and, when present, audio/dialogue; produce a concise director-oriented verdict with the next actionable correction.
version: 1.1.0
---

# Athabasca Video Review

Use this when the user asks to review, compare, or diagnose generated Athabasca clips.

This skill is for critique and diagnosis, not generation. Keep final answers brief unless the user explicitly asks for a detailed breakdown.

## Goal

Turn a generated video into a concrete production review:

- locate or download the actual clip
- inspect representative visual frames
- inspect audio/dialogue when relevant
- compare against the current request, shot intent, and prompt
- identify what worked, what drifted, and the next correction

## Source of truth order

When reviewing a clip, use this precedence:

1. explicit current user request about what the clip should do
2. target shot intent
3. approved source still / first-frame / last-frame references
4. current canonical video prompt
5. adjacent shot continuity
6. broader project lore or exploratory notes

Do not overfit to vague mood language if the user gave a concrete motion, acting, or dialogue beat.

## Required workflow

### 1) Find the clip

For Telegram/Hermes workflows, check local caches first:

- `~/.hermes/cache/videos/`
- `~/.hermes/video_cache/` legacy fallback
- `~/.hermes/cache/documents/` or `~/.hermes/document_cache/` if sent as a file/document

If multiple candidates exist, prefer the most recently modified file in the current session window, or match a filename suffix the user supplied.

If the clip is an Athabasca media URL, download it to a temporary review directory rather than reviewing hypothetically.

### 2) Probe streams

Use `ffprobe` to capture duration, resolution, frame rate, and whether an audio stream exists:

```bash
ffprobe -v error \
  -show_entries format=duration \
  -show_entries stream=codec_type,width,height,avg_frame_rate,codec_name,channels,sample_rate,duration \
  -of json clip.mp4
```

Keep these facts in reasoning. Include them in the final answer only if relevant.

### 3) Extract representative frames

Extract 4–5 frames or a contact sheet with `ffmpeg`.

Default sampling:

- start / early
- early-middle
- middle
- late-middle
- late

Bias samples toward the requested beat if it happens at a specific time.

Example:

```bash
mkdir -p /tmp/athabasca-video-review/frames
ffmpeg -y -i clip.mp4 -vf "fps=1,scale=640:-1" -frames:v 5 /tmp/athabasca-video-review/frames/frame_%02d.jpg
ffmpeg -y -pattern_type glob -i "/tmp/athabasca-video-review/frames/*.jpg" \
  -filter_complex "tile=5x1:padding=8:margin=8" -frames:v 1 /tmp/athabasca-video-review/contact.jpg
```

Use vision analysis on representative frames or the contact sheet when the vision backend is working.

### 3b) Fallback when vision tooling is unavailable

If the vision model/tool is broken, unavailable, or returning provider/model errors, do **not** bluff a semantic frame read. Fall back to objective checks and clearly label the review as partial.

Useful fallback checks:

- compare requested framing vs actual encoded dimensions from `ffprobe`
- compare source still vs extracted first frame with `ffmpeg` `ssim` when first-frame adherence matters
- compare first vs last frame with `ssim` to detect major composition/camera drift in supposedly locked-off shots
- confirm whether an audio stream exists and whether levels look sane
- call out persistence/attachment anomalies separately from creative quality issues

Example SSIM checks:

```bash
# source still vs generated first frame
ffmpeg -y -i source.jpg -i first.jpg \
  -filter_complex "[0:v]scale=1176:784[ref];[1:v]scale=1176:784[test];[ref][test]ssim" \
  -frames:v 1 -f null -

# first frame vs last frame to detect drift
ffmpeg -y -i first.jpg -i last.jpg \
  -filter_complex "[0:v]scale=1176:784[a];[1:v]scale=1176:784[b];[a][b]ssim" \
  -frames:v 1 -f null -
```

Interpretation guidance:

- wrong encoded aspect ratio is a hard factual miss if the request specified framing
- high source→first-frame SSIM with low first→last SSIM often indicates good start-frame adherence but substantial shot drift
- if the fallback evidence is insufficient for performance/emotion claims, say so explicitly instead of over-claiming

### 4) Inspect audio when present or requested

Do this when:

- the clip has an audio stream
- the prompt requested dialogue, voice, ambience, silence, timing, or vocal performance
- the user asks about speech, sighs, growls, timing, or sound quality

Extract audio:

```bash
ffmpeg -y -i clip.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/athabasca-video-review/audio.wav
```

If a local transcription tool is available, transcribe and note timestamps. If not, still check for audio presence/levels and listen/analyze if tooling permits.

Quick level check:

```bash
ffmpeg -i /tmp/athabasca-video-review/audio.wav -af volumedetect -f null - 2>&1 | grep -E 'mean_volume|max_volume'
```

Evaluate:

- whether the requested line is present and intelligible
- whether it occurs at the correct visual beat
- whether the tone matches the prompt
- whether unwanted vocalizations occur: sigh, grunt, growl, laugh, extra words
- whether ambience supports rather than overwhelms the scene

## Visual review dimensions

Check only the dimensions relevant to the prompt:

- action fidelity: requested motion/action is visible and dominant
- performance fidelity: intended emotion, micro-expression, body language, and acting arc
- motion logic: passive vs active, sinking vs swimming, falling vs diving, stillness vs frantic movement
- continuity: subject, wardrobe, props, environment, palette, composition
- camera/staging: framing, lockoff/movement, subject placement, readability
- materials/environment: bubbles, foam, splash, dust, smoke, cloth, hair, lighting behavior
- production failures: watermark, text artifacts, anatomy failures, extra limbs, disappearance, style drift

## Output style for the user

the user prefers concise, director-oriented critique. Default to a short verdict and a few actionable points, not a frame-by-frame essay.

Preferred structure:

```text
Verdict: [one sentence]

What works:
- [1]
- [2]

What misses:
- [1]
- [2]

Next correction: [one concrete prompt/directing change]
```

For audio/dialogue clips, use:

```text
Verdict: [one sentence]

Visual:
- [key visual/performance point]

Audio:
- [line/timing/tone issue]

Next correction: [one concrete prompt/directing change]
```

For two-clip comparisons:

```text
Verdict: [Model/clip A or B wins and why]

- Clip A: [one performance/action read]
- Clip B: [one performance/action read]
- Main mismatch: [one sentence]

Next correction: [specific wording or directing change]
```

## Diagnosis heuristics

- Right environment but wrong body behavior: action wording is weak or source posture implies the wrong motion.
- Splash/impact works but settle/end-state fails: prompt overemphasizes impact or duration is too short.
- Swimming instead of sinking: passive motion and no-propulsion constraints need to be stronger.
- Identity drift: prompt may be too long or re-describing identity instead of preserving the reference.
- Dialogue too early/extra vocalization: model audio timing is unreliable; consider silent/ambient generation and post/VO for final timing.

## Prompt correction principles

Recommend a prompt revision when failure is action/staging/performance comprehension, timing, or continuity. Do not rewrite the full prompt unless the user asks.

Good corrections are concrete:

- countable physical beats: `small repeated nods, then freeze, then one subtle head shake`
- explicit timing: `silent for the first two seconds, then says only "Amazing"`
- clear passive/active constraints: `limp downward descent, no swimming, no arm propulsion`
- positive tone direction: `calm natural speaking voice; no sigh, grunt, growl, or extra words`
