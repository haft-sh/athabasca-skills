# Replicate Seedance validation pattern

Use this when the user wants to validate that a newly wired Replicate video provider is actually working end-to-end through Athabasca.

## Goal
Separate three different failure classes:
1. Athabasca routing / adapter / polling failure
2. Provider moderation / sensitive-content gating
3. Persistence / attachment mismatch after successful generation

## Proven pattern from the Prenup i2v probe

### Probe 1: face-containing proposal beat
- Provider: `replicate`
- Model: `bytedance/seedance-2.0`
- Mode: `image-to-video`
- Resolution: `480p`
- Result: upstream terminal moderation-style error
- Error shape:
  - `ModelError: The input or output was flagged as sensitive. Please try again with different inputs. (E005)`

Interpretation:
- Do **not** immediately conclude the Replicate provider wiring is broken.
- This proves the request reached Replicate and Athabasca received a structured upstream failure back.
- Classify first as likely moderation / likeness-sensitive-content gating unless contradicting evidence appears.

### Probe 2: no-face insert shot
- Same provider/model/settings family
- Use a reference frame with hands / props only and no visible faces
- Result: successful completion, returned provider job id, persisted Athabasca asset, public video URL verified `200`

Interpretation:
- This validates Athabasca -> Replicate submission, async polling, response parsing, asset persistence, and public URL delivery.
- If the no-face insert succeeds after a face shot fails with `E005`, treat the earlier failure as content-policy/moderation-adjacent rather than transport or adapter failure.

## Recommended validation sequence
1. Start with the exact target request if the user wants a realistic production probe.
2. If that fails with a moderation-style upstream error, do **one** lower-risk follow-up probe only when the user authorizes it.
3. Prefer a no-face insert shot for the follow-up probe.
4. Keep the same provider/model/resolution family so the comparison isolates content sensitivity rather than settings drift.
5. Use an idempotency key for every submit.
6. Do not auto-regenerate on timeout/failure if the user explicitly says the UI may still be working.

## Success checklist
A successful provider-validation probe should confirm all of:
- `POST /api/projects/:slug/generate/video` returns `ok: true`
- generation metadata includes provider/model and a provider job id when available
- Athabasca persisted a video asset with `publicUrl`
- `publicUrl` returns HTTP `200`

## Important caveat
A successful generation can still return `attachments: []`.

Interpretation:
- provider wiring may be correct
- persistence may be correct
- attachment behavior may still need separate debugging

Do not collapse those into one diagnosis.

## Reporting language
Prefer concise wording like:
- "Replicate path is wired enough to submit and receive upstream responses."
- "This specific shot appears moderation-gated, not transport-broken."
- "Successful no-face insert validates provider polling + persistence; attachment remains a separate concern if `attachments: []`."