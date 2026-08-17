# Pricing / API notes — 2026-05

Condensed from a live pricing/API pass focused on cheap first-pass evaluation for cinematic voice-clone + performance testing.

## Main takeaway

A small benchmark pack is usually cheap.

For ~6 lines / ~72 seconds of total output per provider:
- raw generation spend is often only a few cents to a few dimes
- the real gating cost is usually feature access:
  - instant/pro voice cloning tier
  - per-voice clone slot fees
  - subscription minimums

## ElevenLabs

### API
- Yes: TTS API and speech-to-speech / voice changer API are documented.

### Pricing / quota posture
- Free plan exists with monthly credits.
- Public pricing pages currently show:
  - Free: 10k credits/month on the main pricing page
  - API pricing summary also shows free included character allowances depending on model family
- Practical gating:
  - Instant Voice Cloning requires paid access (`Starter` class plan)
  - Professional Voice Cloning requires a higher plan (`Creator` class plan)

### Metered costs
- TTS multilingual: about `$0.10 / 1K chars`
- Voice changer: about `$0.12 / minute`

### Evaluation posture
- Good first paid benchmark candidate.
- Cheapest serious path is usually a low paid tier, not free.

## Hume

### API
- Yes: TTS, voice cloning docs, and voice conversion API are public.
- Voice conversion endpoint accepts uploaded audio and preserves timing/emotion from the donor performance.

### Pricing / quota posture
- Free plan exists.
- Public pricing currently indicates roughly:
  - Free: 10k TTS chars, 5 EVI minutes
  - Starter: low-cost entry tier
- Important caveat:
  - voice cloning docs say availability depends on subscription tier
  - pricing table suggests broad inclusion, so verify actual account entitlement before promising free clone creation

### Metered costs
- Creator-tier TTS overage: around `$0.15 / 1K chars`
- Lower-tier EVI speech costs are around `$0.07 / minute`

### Evaluation posture
- Strong candidate for cheap emotional-performance testing.
- Tier ambiguity around cloning should be checked in account UI before planning around free use.

## Resemble AI

### API
- Yes: documented TTS + speech-to-speech endpoint.
- Full API access is part of Flex/PAYG.

### Pricing / quota posture
- No classic “big free monthly bucket” found.
- But PAYG/Flex starts with `$0` upfront and loaded credits.
- Credits do not expire on Flex.

### Clone-related costs
- Rapid clone: about `$2 / month per voice`
- Pro clone: about `$5 / month per voice`

### Metered costs
- TTS: `$0.0005 / sec`
- Voice changer / STS: `$0.0005 / sec`

Rule of thumb:
- about `$0.03 / minute`
- about `$1.80 / hour`

### Evaluation posture
- Cheap for donor-performance testing.
- Main cost is voice-slot persistence, not generation.

## Cartesia

### API
- Yes: cloning APIs and docs are public.

### Pricing / quota posture
- Free plan exists with credits.
- Important gating:
  - free is useful for platform/API evaluation
  - instant voice cloning is gated above free
  - pro voice cloning is gated higher still

### Metered costs
- Instant clone speech: `1 credit / character`
- Voice changer: `15 credits / second`
- Pro voice clone training: `1M credits` on successful training
- PVC speech: `1.5 credits / character`

### Evaluation posture
- Reasonable for API evaluation.
- Less ideal than PAYG competitors if the real goal is cheap clone testing with minimal commitment.

## Speechify

### API
- Yes: REST API and SDKs are exposed.

### Pricing / quota posture
- Free starter bucket exists.
- Voice cloning is not included on free; it appears on PAYG.

### Evaluation posture
- Good for cheap generic API testing.
- Less compelling as a first dramatic-performance contender than Eleven/Hume/Resemble.

## Azure Speech

### API
- Yes.

### Pricing / quota posture
- Free Speech tier exists.
- But it is not the easiest or clearest cheap path for cinematic voice-clone evaluation.

### Evaluation posture
- Better treated as enterprise comparison, not first-pass benchmark default.

## Cheap first-pass shopping list

A pragmatic low-cost test basket:
- ElevenLabs low paid tier
- Hume free or starter
- Resemble Flex + one rapid clone

Expected total outlay for a meaningful first comparison is typically in the low tens of dollars, not hundreds, assuming:
- only a few providers
- one clone each
- short benchmark lines
- no multiple PVC trainings

## When costs jump

Testing becomes materially expensive when you:
- train multiple pro/PVC voices
- keep lots of clone slots alive over time
- rerender many long takes repeatedly
- benchmark with long-form scenes instead of short lines
