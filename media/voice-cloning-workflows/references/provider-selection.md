---
name: voice-cloning-for-video-pipelines
description: Use when evaluating, selecting, or integrating voice cloning and emotive speech generation providers for a video creation pipeline that needs consistent character voices across renders.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [voice-cloning, tts, speech-to-speech, video-pipeline, provider-selection, emotive-audio]
    related_skills: [youtube-voice-clone-sample-extraction, songsee]
---

# Voice Cloning for Video Pipelines

## Overview

This skill is for provider research and pipeline design when the user wants **consistent character voices across multiple video generations**, not just a one-off TTS demo.

The key lesson: **clone quality and performance quality are different problems**. A provider can preserve vocal identity but still sound emotionally flat. For cinematic work, the strongest architecture is often a hybrid:

1. a **canonical cloned voice** per character
2. a **performance path** for emotional scenes, often using speech-to-speech / voice conversion
3. strict **render metadata + prompt/style defaults** so the same voice can be re-rendered consistently later

This skill is intentionally provider-agnostic but includes a practical shortlist and evaluation framework. Use the reference notes for current provider specifics.

Reference: `references/providers-2026-05.md`
Pricing/API notes from a later comparison pass live in `references/pricing-api-2026-05.md`.
Sample-cleanup recipes for salvaging interrupted or multi-speaker source clips live in `references/sample-cleanup-recipes.md`.

## When to Use

Use this when:
- the user asks which providers/models/services support **voice cloning**
- the user wants **emotive** or **cinematic** speech, not just intelligible narration
- the user needs **voice consistency across video gens**
- the user is comparing providers for a production system or agent pipeline
- the user is dissatisfied with a quick-clone provider and wants better acting/performance

Do not use this when:
- the task is only extracting a clean sample from YouTube; use `youtube-voice-clone-sample-extraction`
- the task is only generic TTS for utilitarian narration with no emotional bar
- the user only needs a transcript, dubbing translation, or STT

## Core Decision Rule

For video pipelines, always separate three questions:

1. **How good is the cloned identity?**
   - timbre
   - accent
   - cadence
   - speaker recognizability

2. **How good is the generated performance?**
   - believable emotion
   - pauses and breath timing
   - subtext / underplaying / intensity transitions

3. **How reproducible is the system?**
   - stable API
   - fixed voice IDs
   - controllable parameters
   - metadata that can be saved and replayed later

Do not let a flashy demo override these three checks.

## Default Recommendation Pattern

If the user wants a practical shortlist, default to:

1. **ElevenLabs** for strongest all-around production maturity
2. **Hume Octave** for emotional nuance testing
3. **Resemble AI** when speech-to-speech performance transfer matters
4. **Cartesia** when low latency and modern API ergonomics matter

Second-tier options worth testing but not first recommendation by default:
- PlayHT
- Speechify
- Azure Speech

If the user specifically says the current provider's performances are unconvincing, strongly consider that **text-only TTS may not be enough** and recommend testing speech-to-speech.

## Cost / API default heuristic

When the user asks whether testing will be expensive, answer from live pricing/docs rather than vibes.

Default guidance from current provider research:
- a disciplined first-pass benchmark is usually cheap; raw generation costs are often well under `$1` per provider for a 6-line pack
- the real gating cost is usually **feature access** (instant/pro cloning tier, clone slot fee, or paid plan), not the synthesis minutes themselves
- prefer providers with either a real free tier or low-friction PAYG for the first evaluation pass

Current practical cost posture:
- **ElevenLabs**: low-risk paid test; free tier exists but cloning requires paid access
- **Hume**: strong candidate for low-cost testing because free/starter plans exist, though exact clone availability may depend on tier/account UI
- **Resemble**: no classic free monthly bucket, but Flex/PAYG starts at `$0` upfront and usage is cheap; clone slots are the main extra cost
- **Cartesia**: free plan exists, but cloning features are gated above free

If the user asks “will this cost a lot to test?”, the usual answer is “probably not” unless they plan to train multiple pro clones or do many long rerenders.


### A. Pure cloned TTS

Flow:
- text -> cloned voice -> audio render

Best for:
- narration
- previs
- expository lines
- temporary voiceover

Weakness:
- often weak on dramatic micro-performance
- emotional tags alone rarely solve this

### B. Donor performance -> speech-to-speech / voice conversion -> canonical clone

Flow:
- actor scratch track or donor performance -> voice conversion into target character voice

Best for:
- hero dialogue
- emotional beats
- timing-sensitive lip-sync
- preserved rhythm, hesitations, breath, and emphasis

Use this when:
- the user says output sounds flat, robotic, or unconvincing
- emotional delivery matters more than raw convenience

### C. Hybrid production path

Flow:
- use cloned TTS for previs / animatic / boards
- re-render hero lines with speech-to-speech or performance-driven generation

This is the best default recommendation for a filmmaking pipeline.

## Provider Selection Heuristics

### ElevenLabs

Recommend when:
- user wants the safest first replacement for a mediocre provider
- they can gather good training data
- they want one vendor that can support clone + conversion workflows

Important points:
- distinguish **Instant Voice Cloning** vs **Professional Voice Cloning**
- prefer **PVC** when the goal is a canonical recurring character voice
- for emotional scenes, test **Voice Changer / speech-to-speech**, not just plain TTS

### Hume Octave

Recommend when:
- emotional nuance is the main concern
- the user is dissatisfied with synthetic acting quality
- long-form consistency and emotionally-aware delivery matter

Important points:
- Hume is unusually strong in positioning around semantic and emotional understanding
- test on whisper, intimate dialogue, escalation, and underplayed lines

### Resemble AI

Recommend when:
- preserving delivery and timing matters
- the user accepts a donor-performance workflow
- the pipeline can support speech-to-speech assets

Important points:
- often a better answer for cinematic lines than trying to over-prompt pure TTS
- especially valuable for hero dialogue

### Cartesia

Recommend when:
- low latency matters
- the team wants clean developer ergonomics
- the use case includes interactive voice systems as well as content generation

Important points:
- credible modern provider
- likely stronger on infra/performance than best-in-class dramatic acting

### PlayHT / Speechify / Azure

Use as comparison or enterprise candidates when needed.

General guidance:
- PlayHT: good exposed control knobs
- Speechify: credible self-serve + fine-tuned options
- Azure: enterprise reliability, broad controls, less obviously the top cinematic-clone choice

## Evaluation Framework

Always compare providers on the **same script set**.

### Suggested test set
- neutral exposition
- intimate low-intensity dialogue
- high-emotion confrontation
- whisper / secrecy / restraint
- irony or laugh-adjacent line
- multilingual or accent-sensitive line if relevant

### Score dimensions
- voice identity consistency
- performance believability
- timing control
- whisper realism
- emotional transitions within one line
- artifact rate
- lip-sync friendliness
- consistency across multiple rerenders

### Test both modes when possible
For each provider, test:
1. **text-only TTS**
2. **performance-driven / speech-to-speech path**

Do not rank providers from text-only tests if the user's real use case is dramatic dialogue.

## Recording / Sample Guidance

When choosing or preparing training material:
- clean audio beats long audio
- one speaker only
- avoid room echo, music, applause, and cross-talk
- record in the language and tone you want if possible
- capture the energy profile the clone should reproduce

### Salvaging imperfect source clips

If the user already has a promising clip but it contains a short interruption from another speaker, do not discard it immediately.

Default salvage move:
1. identify the contaminated time span precisely
2. cut that span out with `ffmpeg` using `atrim`
3. stitch the surrounding male-only sections with a **very short crossfade** (`acrossfade`, e.g. `0.05`–`0.10s`) so the seam is less abrupt
4. verify the new duration with `ffprobe`
5. if the result is intended for training/upload, also export a WAV copy after the edit

Use this only when the interruption is brief and the surrounding cadence still sounds natural after the cut. If the edit destroys sentence rhythm or leaves obvious musical/noise discontinuities, prefer extracting a different clean sample instead.

If the source is messy and from YouTube or interviews, extract a clean sample first with `youtube-voice-clone-sample-extraction`.
If the source is already local but needs a small contamination removed, use the ffmpeg cleanup recipe in `references/sample-cleanup-recipes.md`.

## Recommended Answer Shape

When the user asks for provider recommendations, structure the answer as:

1. **Bottom-line recommendation**
2. **Top shortlist**
3. **Best fit by use case**
4. **Important caveat: clone vs performance**
5. **Recommended evaluation plan**
6. **Suggested pipeline architecture**

Keep the conclusion opinionated. The user usually benefits more from a decisive shortlist than an exhaustive vendor dump.

## Common Pitfalls

1. **Confusing voice identity with acting quality.**
   A convincing clone can still deliver wooden performances.

2. **Evaluating only one neutral sentence.**
   That hides failure on whispering, escalation, or emotional transitions.

3. **Ignoring speech-to-speech when the complaint is performance.**
   This is often the real fix.

4. **Switching providers per scene.**
   That causes character drift. Pick a canonical provider unless there is a clear hero-line exception.

5. **Failing to save render metadata.**
   Without provider/model/voice/settings provenance, consistency is hard to maintain.

6. **Overvaluing emotion tags.**
   Emotion controls help, but they do not guarantee believable acting.

## Verification Checklist

- [ ] Recommendation distinguishes clone identity from performance quality
- [ ] Speech-to-speech is considered when emotion is a key requirement
- [ ] At least 3 serious providers are shortlisted with rationale
- [ ] The answer includes an evaluation method, not just vendor names
- [ ] The pipeline recommendation explains how to preserve voice consistency across renders
- [ ] If source material is messy, sample extraction is routed through the YouTube extraction skill
