---
name: athabasca-audio-generation
description: Generate and persist Athabasca audio through normalized project APIs, starting with Cartesia Sonic 3.5 speech-to-speech voice changing from existing media asset IDs.
version: 1.0.0
metadata:
  hermes:
    tags: [athabasca, audio, generation, speech-to-speech, cartesia, media]
    related_skills: [athabasca-media-upload, athabasca-video-generation, athabasca-media-attachment-finder]
---

# Athabasca Audio Generation

Use this when the user asks to generate, transform, voice-change, dub, or otherwise create **audio** for an Athabasca project, especially from an existing `asset_...` media ID.

This skill is class-level: provider quirks belong in Athabasca code, validation, capabilities, and tests. The agent should use direct provider calls only for discovery/debug fallback, then migrate recurring behavior into normalized Athabasca APIs.

## Core principles

1. Prefer the Athabasca abstraction over direct provider calls.
2. Accept source media by Athabasca asset ID whenever possible, not local paths.
3. Persist generated audio through Athabasca media APIs/R2; never leave canonical output on provider storage, Telegram cache, `/tmp`, or local-only files.
4. Track provenance with generation logs, source asset IDs, provider/model, voice ID, output format, and attachment targets.
5. Keep provider constraints in code-backed capability metadata and regression tests.

## Target normalized workflow

The desired product shape mirrors image/video generation:

1. Query live/static audio capabilities:
   ```bash
   curl -sS http://localhost:3000/api/generation/audio-capabilities | jq .
   ```
2. Resolve provider/model from capabilities.
3. Resolve source media by asset ID:
   ```bash
   curl -sS http://localhost:3000/api/media/<assetId> | jq .
   ```
4. Submit generation through the normalized project route:
   ```text
   POST /api/projects/:slug/generate/audio
   ```
5. Server-side adapter maps normalized request to upstream provider payload.
6. Server persists returned bytes as an Athabasca audio media asset.
7. If `shotId` is supplied, attach generated audio to the shot and default the asset phase to `clips` unless overridden.
8. Verify returned `asset.publicUrl` and generation log before reporting success.

## Recommended Phase 1 API shape

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
  "title": "Cartesia Sonic 3.5 voice change",
  "provenanceNote": "Voice-changed from source asset asset_... using Cartesia Sonic 3.5."
}
```

Recommended output default: WAV, 24 kHz, `pcm_s16le`. This is editing/model-input friendly. MP3 can be supported for compact previews, but should not be the default unless the user asks.

## Cartesia Sonic 3.5 speech-to-speech notes

Primary endpoint of interest:

```text
POST https://api.cartesia.ai/voice-changer/bytes
```

Request:
- `multipart/form-data`
- `Authorization: Bearer $CARTESIA_API_KEY`
- `Cartesia-Version: 2026-03-01`
- form fields:
  - `clip`: source audio file
  - `voice[id]`: target voice ID
  - `output_format[container]`: `raw | wav | mp3`
  - `output_format[sample_rate]`: `8000 | 16000 | 22050 | 24000 | 44100 | 48000`
  - `output_format[encoding]`: required for `raw`/`wav`; `pcm_f32le | pcm_s16le | pcm_mulaw | pcm_alaw`
  - `output_format[bit_rate]`: required for `mp3`

Response:
- direct `audio/*` bytes, not JSON.

Important uncertainty:
- The extracted Cartesia docs for `/voice-changer/bytes` do **not** show a `model_id` form field, even though Sonic 3.5 is the desired product model family. Until OpenAPI/live probing confirms a model field, expose `model=sonic-3.5` in Athabasca capabilities/provenance but do not send an upstream model field.

Implementation pitfall:
- Do not manually set `Content-Type` for multipart `fetch`; let `FormData` set the boundary.

## Source asset handling

Preferred input is `sourceAssetId`.

- If source asset kind is `audio`: fetch `asset.publicUrl` and send its bytes (or normalize if the provider rejects the format).
- If source asset kind is `video`: reuse/refactor Athabasca’s audio derivation logic to extract/normalize a temporary WAV clip before voice changing.
- Reject unsupported kinds before provider calls.
- Verify the source asset belongs to the target project.
- Avoid persisting extracted intermediate audio unless the user requested it or debugging/provenance makes it useful.

Related existing API:

```text
GET /api/media/:assetId
POST /api/media/:assetId/derive-audio
```

The derivation endpoint is a useful reference for ffmpeg extraction and attachment behavior, but the normalized audio generation route should not require manually creating a separate intermediate asset for ordinary speech-to-speech runs.

## Environment setup

the user noted `CARTESIA_API_KEY` exists in `.bashrc`; the Athabasca systemd service needs it in its env file.

The current dev service reads:

```text
~/.config/athabasca/athabasca-dev.env
```

Safe one-time update pattern:

```bash
mkdir -p ~/.config/athabasca
python3 - <<'PY'
from pathlib import Path
import os
path = Path.home() / '.config/athabasca/athabasca-dev.env'
lines = path.read_text().splitlines() if path.exists() else []
key = os.environ.get('CARTESIA_API_KEY')
if not key:
    raise SystemExit('CARTESIA_API_KEY is not set in this shell')
lines = [line for line in lines if not line.startswith('CARTESIA_API_KEY=')]
lines.append(f'CARTESIA_API_KEY={key}')
path.write_text('\n'.join(lines) + '\n')
PY
systemctl --user restart athabasca-dev.service
```

## Verification checklist

Before reporting success:

- `GET /api/generation/audio-capabilities` lists `cartesia / sonic-3.5`.
- Generation route returns `{ ok: true, asset, generationInfo, logId }`.
- Returned asset has `kind: "audio"`, `category: "generated"`, `sourceKind: "generated"`.
- `asset.publicUrl` returns HTTP `200` or `206`.
- Generation log is queryable with `kind=audio` if the schema supports it.
- If `shotId` was provided, shot attachment exists; generated audio should live in `clips` by default.

## Failure classification

- Missing `CARTESIA_API_KEY`: service environment problem; check/restart systemd env, not shell env alone.
- Source asset missing/wrong project: Athabasca request validation error.
- Source asset not audio/video: Athabasca validation error before provider call.
- Unsupported output container/sample rate/encoding: capability validation bug if provider call was attempted.
- Cartesia non-2xx: provider/upstream error; persist upstream status/body in generation logs.
- Successful provider bytes but no media asset: Athabasca persistence bug.
- Media asset exists but no shot attachment: attachment/persistence bug, not provider failure.

## References

- `references/cartesia-sonic35-voice-changer-bytes.md` — condensed docs and design notes from the first Cartesia speech-to-speech planning session.
