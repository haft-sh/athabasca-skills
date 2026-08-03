# Cartesia Sonic 3.5 Voice Changer Bytes Notes

Captured from the initial Athabasca speech-to-speech planning session on 2026-05-07.

## Sources consulted

- Cartesia overview: `https://docs.cartesia.ai/get-started/overview`
- Voice Changer Bytes endpoint: `https://docs.cartesia.ai/api-reference/voice-changer/bytes`
- Sonic 3.5 model page: `https://docs.cartesia.ai/build-with-cartesia/tts-models/sonic-3-5`
- Cartesia docs index: `https://docs.cartesia.ai/llms.txt`

## Endpoint

```text
POST https://api.cartesia.ai/voice-changer/bytes
```

Purpose: takes an audio file of speech and returns audio bytes of the same speech/intonation in a different target voice.

Request type: `multipart/form-data`.

Response: `audio/*` file bytes, not JSON.

## Required headers

```text
Authorization: Bearer <CARTESIA_API_KEY>
Cartesia-Version: 2026-03-01
```

Docs list version options:
- `2024-06-10`
- `2024-11-13`
- `2025-04-16`
- `2026-03-01`

Use `2026-03-01` for Sonic 3.5-era implementation unless the live API requires otherwise.

## Form fields

Required/core:

```text
clip=@example-file
voice[id]=<target voice id>
output_format[container]=raw|wav|mp3
output_format[sample_rate]=8000|16000|22050|24000|44100|48000
```

For `raw` and `wav`:

```text
output_format[encoding]=pcm_f32le|pcm_s16le|pcm_mulaw|pcm_alaw
```

For `mp3`:

```text
output_format[bit_rate]=<integer>
```

Recommended Athabasca default:

```json
{
  "container": "wav",
  "sampleRate": 24000,
  "encoding": "pcm_s16le"
}
```

## Sonic 3.5 facts

Sonic 3.5 is Cartesia's current streaming TTS model family. Docs describe:
- high naturalness
- accurate transcript following
- low latency
- 42 languages

Model IDs from docs:
- `sonic-3.5` — stable base model that routes to latest stable snapshot
- `sonic-3.5-2026-05-04` — stable snapshot listed during research
- `sonic-latest` — beta/latest, not recommended for production consistency

Important implementation uncertainty:
- The `/voice-changer/bytes` docs do not show a `model_id` field in the extracted cURL example.
- Athabasca should still expose `model=sonic-3.5` for normalized capabilities/provenance, but the Cartesia worker should not send an upstream model field until OpenAPI/live probing confirms it is supported.

## Athabasca design decisions from planning

Recommended normalized routes:

```text
GET /api/generation/audio-capabilities
POST /api/projects/:slug/generate/audio
```

Recommended Phase 1 request shape:

```json
{
  "mode": "speech-to-speech",
  "provider": "cartesia",
  "model": "sonic-3.5",
  "sourceAssetId": "asset_...",
  "voiceId": "a5136bf9-224c-4d76-b823-52bd5efcffcc",
  "outputFormat": {
    "container": "wav",
    "sampleRate": 24000,
    "encoding": "pcm_s16le"
  },
  "shotId": "shot_...",
  "phase": "clips",
  "title": "Cartesia Sonic 3.5 voice change"
}
```

Scope boundaries:
- In scope: speech-to-speech from existing Athabasca asset IDs; audio/video source assets; persisted generated audio.
- Out of scope initially: voice creation/cloning, TTS, SSE/WebSocket streaming, UI-heavy controls.

## Environment note

the user stated `CARTESIA_API_KEY` exists in `.bashrc`. Athabasca dev service reads env from:

```text
~/.config/athabasca/athabasca-dev.env
```

Do not assume a key present in the interactive shell is present in the long-running systemd service. Copy once with replacement semantics, then restart `athabasca-dev.service`.
