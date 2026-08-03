# BytePlus Seedance 2.0 privacy moderation and wiring validation

Use this note when a new BytePlus Seedance route appears in Athabasca capabilities but a live generation still fails.

## Confirmed pattern

A newly wired BytePlus provider can pass these checks:
- `GET /api/health`
- `GET /api/generation/video-capabilities`
- request validation against live capabilities

and still fail on the first real generation for one of two very different reasons:

1. **Service environment not reloaded yet**
   - Symptom: generation log shows missing `BYTEPLUS_ARK_API_KEY`
   - Meaning: the long-running Athabasca service did not pick up the key yet, even if the env file already contains it
   - Fix: restart the long-running service, then retry with a **new idempotency key**

2. **Upstream privacy moderation on real-person references**
   - Confirmed upstream error from BytePlus:
     - `InputImageSensitiveContentDetected.PrivacyInformation`
     - message like: `The request failed because the input image may contain real person.`
   - Meaning: the request reached BytePlus correctly; this is not a transport/auth/wiring failure
   - Observed on `reference-to-video` with multiple face-bearing reference images

## Operational interpretation

Do **not** treat a privacy-moderation rejection as a provider wiring failure.

Classify outcomes this way:
- missing key before upstream submit -> service env / restart problem
- upstream privacy error after submit -> provider moderation is active and the integration path works
- successful asset persistence -> full end-to-end success

## Best validation probe for a newly added BytePlus provider

To test whether the provider is wired correctly without confounding moderation:
- use an **object-only** or **no-face** prompt/reference set, or
- use a clearly **synthetic / AI-generated** character reference instead of a real-person-looking photo

Avoid using real-person face references for the first wiring test. Otherwise a correct integration can look broken because moderation fires before any useful output is produced.

## Reporting guidance

When BytePlus returns `InputImageSensitiveContentDetected.PrivacyInformation`, report:
- provider/model
- mode
- whether the request reached upstream
- that moderation/privacy blocked the reference image(s)
- that no Athabasca asset was created

Do not claim:
- the provider is unwired
- the API key is bad
- the prompt itself is the main issue

## Practical follow-up options

When a face-led BytePlus Seedance request is blocked:
1. retry only after changing the reference strategy, not by resubmitting the same payload
2. validate the integration with a no-face/object-only probe
3. if the creative goal requires a person, prefer:
   - synthetic character sheets
   - stylized stand-ins
   - another provider/surface with a workflow explicitly meant for authorized human likeness use
