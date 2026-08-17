# Multi-speaker extraction recipes

Concise patterns for turning noisy YouTube dialogue scenes into clone-ready single-speaker samples.

## Pattern: tight + extended deliverables

When a source contains multiple usable windows, export two deliverables:

1. **tight**
   - shortest conservative set of clearly solo windows
   - intended for immediate upload to a cloning provider
   - default target: ~20–40s when possible

2. **extended**
   - more coverage from additional target-only windows
   - useful when a provider benefits from more speech or when the tight clip underperforms
   - may include more stylistic variety, but should still exclude clear contamination

This avoids a false binary between "too short" and "too risky".

## Pattern: captions -> trim -> ASR verify

Use captions only to find rough windows, then verify the final render with ASR.

Recommended flow:
1. Download auto-captions and audio with `yt-dlp`.
2. Mark candidate windows from captions.
3. Trim candidate target-only regions with `ffmpeg`.
4. Concatenate only the kept windows.
5. Normalize and downmix for upload convenience.
6. Run a quick ASR pass on the rendered output.
7. If ASR or listening suggests contamination, remove the suspect window from the tight version.

## Example ffmpeg trim + concat

```bash
ffmpeg -y -i source.wav -ss 0.15 -to 22.55 -c:a pcm_s16le s1.wav
ffmpeg -y -i source.wav -ss 60.65 -to 73.60 -c:a pcm_s16le s2.wav
printf "file '%s'\nfile '%s'\n" "$PWD/s1.wav" "$PWD/s2.wav" > concat.txt
ffmpeg -y -f concat -safe 0 -i concat.txt \
  -af "highpass=f=80,lowpass=f=8000,loudnorm=I=-16:TP=-1.5:LRA=11" \
  -ar 24000 -ac 1 output-tight.wav
ffmpeg -y -i output-tight.wav -codec:a libmp3lame -q:a 2 output-tight.mp3
```

## Example ASR verification

A fast sanity check with Whisper/Faster-Whisper can catch obvious wrong-speaker inclusions, bad joins, or subtitle-driven mistakes.

```python
from faster_whisper import WhisperModel
model = WhisperModel('tiny', device='cpu', compute_type='int8')
segments, info = model.transcribe('output-tight.wav', beam_size=5)
for s in segments:
    print(f'[{s.start:.2f}-{s.end:.2f}] {s.text}')
```

Use this as a *sanity check*, not as perfect diarization.

## Boundary heuristics

- Exclude ambiguous back-and-forth exchanges from the tight file.
- Prefer contiguous monologue stretches.
- If off-screen replies are possible, keep only the windows where the target voice is obviously alone.
- Cleaner beats longer.
