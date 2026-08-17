---
name: voice-cloning-workflows
description: Voice-cloning workflow umbrella — choose providers, prepare clean source material, evaluate clone identity vs performance, and build reproducible video-pipeline voice workflows.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [voice-cloning, tts, speech-to-speech, audio-cleanup, youtube, provider-selection]
---

# Voice Cloning Workflows

Use this skill for the full class of voice-cloning work: provider selection, sample preparation, cleanup, and reproducible render workflows.

## Subareas covered
- **Provider/pipeline design** — choosing the right clone + performance architecture
- **Sample extraction/cleanup** — deriving clean single-speaker reference clips from YouTube or messy source audio
- **Evaluation** — testing identity retention, emotional performance, and rerender consistency

Detailed absorbed material lives in:
- `references/provider-selection.md`
- `references/providers-2026-05.md`
- `references/pricing-api-2026-05.md`
- `references/sample-cleanup-recipes.md`
- `references/youtube-sample-extraction.md`
- `references/multi-speaker-extraction-recipes.md`

## Core decision rule
Separate three questions every time:
1. **Clone identity** — does it sound like the intended speaker?
2. **Performance quality** — does it act believably, or just pronounce words clearly?
3. **Reproducibility** — can the workflow be rerun later with stable settings and provenance?

## Default workflow
### 1. Get or prepare a clean source sample
- Prefer single-speaker, low-noise clips.
- If the source is YouTube or multi-speaker, extract the cleanest 10-90s reference first.
- Cleaner beats longer.

### 2. Choose the right generation architecture
- **Pure cloned TTS** for narration/previs.
- **Speech-to-speech / voice conversion** for emotional hero lines.
- **Hybrid pipeline** for productions that need both speed and acting quality.

### 3. Evaluate with a fixed test pack
Compare providers on the same lines: neutral exposition, intimate dialogue, high-emotion line, whisper/restraint, and any accent/language-sensitive lines.

### 4. Save provenance
Record provider, model, voice ID, sample source, and important settings so later rerenders stay consistent.

## Default recommendation posture
- Start with a practical shortlist, not an exhaustive vendor dump.
- If the user says the output is flat, test speech-to-speech rather than endlessly prompt-tuning text-only TTS.
- Route YouTube or contaminated sample work through the extraction/cleanup references before evaluating provider quality.

## Verification checklist
- [ ] Sample quality evaluated before blaming the provider
- [ ] Clone identity vs acting quality kept distinct
- [ ] At least one clean reference clip exists
- [ ] Evaluation plan uses the same script pack across providers
- [ ] Metadata/provenance captured for reproducibility
