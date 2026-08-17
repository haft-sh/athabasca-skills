---
name: youtube-voice-clone-sample-extraction
description: Use when a user provides a YouTube link and wants a clean single-speaker 10-90s reference file for voice cloning, with other speakers removed.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [youtube, voice-clone, speaker-isolation, yt-dlp, ffmpeg, audio-editing]
    related_skills: [youtube-content, whisper]
---

# YouTube Voice Clone Sample Extraction

## Overview

This workflow turns a multi-speaker YouTube clip into an upload-ready reference sample for voice cloning.

Goal: produce a **clean single-speaker file** in the provider's accepted duration range, usually by combining transcript-guided timestamp discovery with conservative `ffmpeg` trimming.

The main lesson from prior use: **cleaner beats longer**. A 20-30 second single-speaker sample is usually better than a 35-45 second sample with even brief bleed-through from another voice.

## When to Use

Use this when:
- the user gives a YouTube URL
- they want to clone or reference one speaker's voice
- the source contains multiple speakers and non-target speech must be excluded
- the target platform wants roughly 10-90 seconds of speech

Do not use this when:
- the user only wants a transcript or summary
- the source audio is already local and clearly segmented by speaker
- proper diarization is required across long recordings; use a fuller ASR/diarization pipeline instead

## Default Strategy

1. Download **captions/subtitles** first to find candidate timestamps.
2. Download **audio-only** source.
3. Identify candidate target-speaker windows.
4. Prefer **one contiguous target-only segment** if available.
5. If needed, stitch multiple target-only segments.
6. When the source is messy, produce **two deliverables**:
   - a **tight** clone-ready sample (most conservative, shortest clean target-only windows)
   - an optional **extended** sample (more coverage, slightly higher contamination risk)
7. Normalize to mono and a modest sample rate for upload convenience.
8. Verify duration and listen for non-target voice bleed-through.
9. Run a quick ASR pass on the rendered output to catch obvious wrong-speaker inclusions or bad cuts before handing it off.

Reference cleanup and extraction patterns: `references/multi-speaker-extraction-recipes.md`

## Commands

### 1) Fetch auto-captions with yt-dlp

```bash
export PATH="$HOME/.hermes/profiles/cliphouse/home/.local/bin:$PATH"
yt-dlp --skip-download --write-auto-sub --sub-langs en --convert-subs vtt \
  -o "/tmp/voiceclone.%(ext)s" "https://www.youtube.com/watch?v=VIDEO_ID"
```

This produces a VTT file such as `/tmp/voiceclone.en.vtt`.

### 2) Download audio-only source

```bash
yt-dlp -f ba --extract-audio --audio-format wav \
  -o "/tmp/voiceclone.%(ext)s" "https://www.youtube.com/watch?v=VIDEO_ID"
```

This yields a WAV source such as `/tmp/voiceclone.wav`.

### 3) Inspect captions for candidate windows

Read the VTT and locate target-speaker runs. If captions are noisy, use them only as rough guides.

Fallbacks:
- `youtube-content` for transcript retrieval
- `whisper` for better transcription if auto-captions are poor

### 4) Trim target-only segments

Single segment:

```bash
ffmpeg -y -i /tmp/voiceclone.wav \
  -ss 00:01:10.72 -to 00:01:37.05 \
  -af "highpass=f=80, lowpass=f=8000, loudnorm=I=-16:TP=-1.5:LRA=11" \
  -ar 24000 -ac 1 output-clean.wav
```

Multiple segments + concat:

```bash
ffmpeg -y -i /tmp/voiceclone.wav -ss START1 -to END1 -c:a pcm_s16le segment1.wav
ffmpeg -y -i /tmp/voiceclone.wav -ss START2 -to END2 -c:a pcm_s16le segment2.wav
printf "file '%s'\nfile '%s'\n" "$PWD/segment1.wav" "$PWD/segment2.wav" > concat.txt
ffmpeg -y -f concat -safe 0 -i concat.txt \
  -af "highpass=f=80, lowpass=f=8000, loudnorm=I=-16:TP=-1.5:LRA=11" \
  -ar 24000 -ac 1 output-clean.wav
```

Optional MP3 export:

```bash
ffmpeg -y -i output-clean.wav -codec:a libmp3lame -q:a 2 output-clean.mp3
```

### 5) Verify duration

```bash
ffprobe -v error -show_entries format=duration,size -of json output-clean.wav
ffprobe -v error -show_entries format=duration,size -of json output-clean.mp3
```

## Selection Heuristics

- Prefer **clear solo speech** over dramatic overlap.
- Prefer **mid-sentence continuity** from one speaker over many tiny fragments.
- Avoid applause, music hits, crowd reactions, and cross-talk when possible.
- If you detect even a short non-target line, cut it out rather than keeping it for duration.
- Aim for **20-40 seconds** when available; shorter clean samples often clone better than longer contaminated ones.
- When the source contains several usable regions, default to shipping:
  - one **tight** file for immediate clone upload
  - one **extended** file for fallback testing if the provider benefits from more material
- Treat auto-captions as a *window finder*, then verify the final render with ASR; do not trust captions alone for speaker purity.
- If a segment is ambiguous because another actor may be replying off-screen, exclude it from the tight version unless the target voice clearly remains solo.

## Common Pitfalls

1. **Using captions as if they were exact speaker diarization.**
   Auto-captions are often inaccurate. Treat timestamps as approximate.

2. **Keeping mixed-speaker lines because they are brief.**
   For voice cloning, even a short wrong-speaker phrase can pollute the sample.

3. **Optimizing for length instead of purity.**
   If forced to choose, ship a shorter clean target-only clip.

4. **Cutting too tight on the boundaries.**
   Leave a small natural lead-in/out around the target line, but not enough to capture another speaker.

5. **Skipping verification.**
   Always inspect duration and do a final listen before handing off.

## Verification Checklist

- [ ] Source URL recorded
- [ ] Captions or transcript inspected for candidate speaker windows
- [ ] Final clip contains target speaker only
- [ ] Final duration is within the platform's allowed range
- [ ] WAV exists for maximum compatibility
- [ ] Optional MP3 exists for quick preview/sharing
- [ ] Notes include kept timestamps and any uncertainty about caption quality
- [ ] Final output was spot-checked with a quick ASR/transcription pass
- [ ] If multiple candidate windows existed, a conservative **tight** version was exported
