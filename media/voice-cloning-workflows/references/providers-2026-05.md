# Voice cloning provider notes — 2026-05

Condensed notes from a provider-research pass focused on **voice consistency across video generations** and **emotive audio generation**.

## Most practical shortlist

### ElevenLabs
- Strongest overall production default.
- Docs distinguish **Instant Voice Cloning (IVC)** from **Professional Voice Cloning (PVC)**.
- PVC trains a dedicated custom model; docs describe it as intended for highest fidelity and note ~3-6 hour fine-tuning time.
- Exposes useful controls including stability / similarity / style settings.
- Also offers **Voice Changer / speech-to-speech**, which is important for emotional scenes.
- Best use: canonical recurring character voices, especially if good training data is available.

### Hume Octave
- Best candidate when the complaint is weak acting, not weak identity match.
- Docs emphasize semantic + emotional understanding, long-form consistency, and emotionally aware delivery.
- Supports voice cloning, voice design, and testing clones in TTS / conversational products.
- Clone creation can start from short audio, but the main draw is **emotional nuance**.
- Best use: intimate dialogue, emotionally complex reads, underplayed dramatic lines.

### Resemble AI
- Strong due to **speech-to-speech**.
- Docs describe converting a donor recording into a target voice while preserving delivery and timing.
- Supports prompt steering on the convert tag for tone/accent/style guidance.
- Best use: hero lines where rhythm, breath, and delivery matter more than convenience.

## Credible second-tier options

### Cartesia
- Strong API ergonomics and very low latency positioning.
- Docs market Sonic 3.5 as fast + emotive.
- Supports cloning and pro voice cloning.
- Important caveat from docs: current instant cloning defaults to **high-similarity**, which may also reproduce background noise.
- Docs recommend ~10s as the sweet spot for that mode and typically `enhance=false` when cloning unless the source is noisy.
- Best use: interactive or realtime-heavy systems, or teams that heavily value API ergonomics.

### PlayHT
- Good set of explicit control knobs in API docs.
- Exposes `emotion`, `voice_guidance`, `style_guidance`, `text_guidance`.
- Docs explicitly note tradeoffs between similarity and expressiveness/stability.
- Best use: controlled A/B testing and systems that want exposed generation parameters.

### Speechify
- Supports zero-shot cloning from short samples and fine-tuned cloning from hours of speaker audio.
- Docs explicitly mention emotion control.
- Best use: another credible benchmark, especially if English-first or mixed with multilingual testing.

### Azure Speech
- HD voices emphasize emotion/style/conversational behavior and strong enterprise integration.
- More of an enterprise TTS/control-plane option than the obvious first pick for cinematic voice clones.
- Best use: organizations with Azure alignment, compliance constraints, or enterprise procurement needs.

## Fish Audio notes
- Fish advertises many emotion tags / styles and short-sample cloning.
- If the output already feels unconvincing, do not assume more prompt tuning will fix the core acting model.
- Emotion-tag breadth is not the same thing as believable dramatic performance.

## Pipeline lesson

If the user says a provider sounds flat or unconvincing:
- do **not** respond with a provider list only
- explicitly recommend testing **speech-to-speech / voice conversion**
- position the likely best architecture as:
  1. canonical clone for identity
  2. text-only TTS for previs and routine lines
  3. performance-driven rerenders for hero dialogue

## Suggested provider order for first evaluation
1. ElevenLabs PVC + Voice Changer
2. Hume Octave clone
3. Resemble speech-to-speech
4. Cartesia
5. PlayHT

## Useful doc anchors cited in research pass
- ElevenLabs voice cloning overview and professional voice cloning docs
- ElevenLabs text-to-speech voice settings and voice changer docs
- Hume Octave TTS overview and voice cloning docs
- Resemble speech-to-speech docs
- Cartesia overview and clone-voices docs
- PlayHT streaming TTS docs
- Speechify models / voice cloning docs
- Azure Speech HD voices docs
