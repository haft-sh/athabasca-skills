# Sample Cleanup Recipes for Voice-Cloning Inputs

Use these when a source clip is mostly good but contains a short interruption, cross-talk fragment, or contaminating speaker span.

## When this is worth doing

Good candidate:
- one dominant speaker
- interruption is short and well-bounded
- the remaining cadence still makes sense after removal
- the clip is otherwise strong in tone/timbre

Bad candidate:
- interruption overlaps important consonants or word endings
- music/noise floor changes drastically across the cut
- removing the segment ruins sentence timing
- many interruptions exist; extract another sample instead

## Minimal ffmpeg recipe: remove a contaminated span and stitch the rest

Example: remove `30s` to `37s` from an MP3 and lightly crossfade the join.

```bash
in=input.mp3
out=cleaned.mp3

ffmpeg -y -i "$in" \
  -filter_complex "[0:a]atrim=start=0:end=30,asetpts=PTS-STARTPTS[a0];\
                   [0:a]atrim=start=37,asetpts=PTS-STARTPTS[a1];\
                   [a0][a1]acrossfade=d=0.08:c1=tri:c2=tri[a]" \
  -map "[a]" -c:a libmp3lame -b:a 128k "$out"
```

Notes:
- `atrim` isolates the good sections.
- `asetpts=PTS-STARTPTS` resets timestamps before concatenation.
- `acrossfade=d=0.08` gives a short smoothing overlap; usually `0.05`–`0.10s` is enough.
- For clone training material, keep the crossfade short so you hide the seam without smearing diction.

## Verify the result

```bash
ffprobe -v error -show_entries format=duration,size -of json cleaned.mp3
```

Listen for:
- clipped consonants at the join
- sudden room-tone change
- unnatural rhythm collapse
- audible duplicate syllables from too-long crossfade

## Export a training-friendly WAV copy

Many voice-cloning flows prefer WAV after cleanup.

```bash
ffmpeg -y -i cleaned.mp3 -ar 24000 -ac 1 cleaned.wav
```

Adjust sample rate/channel count to the provider's preferred ingest format if needed.

## Practical guidance

- Preserve the strongest uninterrupted performance beats, not necessarily the longest contiguous take.
- If the user explicitly names the bad span, trust that as the first cut point, then refine by ear if needed.
- For local clips, this repair path is often faster than re-extracting from scratch.
