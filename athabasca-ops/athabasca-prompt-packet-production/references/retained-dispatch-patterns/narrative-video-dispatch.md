---
name: narrative-video-dispatch
description: Prepare and dispatch dialogue-aware, reference-conditioned narrative video groups without overloading a single generation.
version: 1.0.0
---

# Narrative Video Dispatch

Use this for multi-shot narrative I2V/T2V work where dialogue timing, character performance, reference roles, and continuity determine whether a paid generation is editorially usable.

## Core model

Separate the production plan into:

1. **Visual master shots** — compositional/editorial coverage, often silent or foley-led.
2. **Dialogue carriers** — one speaker, one thought, one camera/performance action, with enough duration for readable speech.
3. **Final audio mix** — the authoritative dialogue/foley layer assembled across selected visual coverage.

Do not make every 2-second visual shot carry completed spoken dialogue.

## Dialogue timing

- A 2-second shot is suitable for a short phrase only.
- Give full sentences and psychologically important beats a dedicated 3–8 second carrier.
- Split long speech at semantic turns, not arbitrary word counts.
- Use reaction, prop, or environment inserts as off-screen dialogue bridges.
- If visible lip sync matters, state the speaker, exact line, and mouth-performance framing explicitly.

## Grouping rule

Keep expanded carriers **inline with the human-facing group that owns the source beat**. Never hide them in a generic global appendix.

When adding carriers makes a group overly dense:

1. Keep the initial visual group lean.
2. Add a named adjacent **helper group** for the long dialogue and its immediate reaction/insert bridge.
3. Declare the helper's source-shot range, continuity handoff, and reference order.
4. Remove the expanded material from the original group; do not leave duplicate prompts in both places.

## Reference-role discipline

Before dispatch, assign each image one role and write it into the prompt:

- **Identity authority:** character face, costume, signature props.
- **Style authority:** materials, rendering treatment, palette, lighting language.
- **Geography authority:** location layout, axis, scale ruler.
- **Blocking-only authority:** composition, camera placement, foreground/background relationship.

A blocking image can still leak its style. If it looks visually incompatible, generate a style-aligned derivative first: use the blocking image for composition and the approved scene image for style. For surgical continuity repairs, use the latest successful derivative as primary reference plus the canonical prop/character reference as secondary; ask for one delta only.

## Preflight checklist

- Query live video capabilities and choose a supported provider/model/mode.
- Confirm the normalized route truly forwards every reference image in the intended order.
- Use durable project-media URLs, not local/cache paths.
- Resolve each reference asset through the media API before dispatch.
- Use a stable idempotency key for each paid intent.
- For Seedance, use audio on when dialogue/foley is needed and say `No Music`; this is not the same as silent video.
- Make speaker ownership and final expression explicit. If a character must not smile, say so directly: neutral/closed mouth, alert, serious, no triumph or relief.

## Post-run verification

- Verify the persisted public MP4, not only provider success.
- Probe the delivered file for duration, display geometry, and audio stream.
- A present audio stream does not mean dialogue was requested: compare the actual prompt. If the prompt asked for ambience/foley only, explain that dialogue absence is expected.
- Review sampled frames for identity, props, unintended text, expression drift, and reference-style leakage.
- Mark exploratory or failed-continuity clips yellow rather than treating them as canonical.

## Pitfalls

- Do not describe a scene reference as both a strict style authority and a blocking-only reference; choose deliberately.
- Do not rerun a paid clip with the same flawed reference stack merely by adding a stronger negative prompt.
- Do not silently crop a delivered video whose actual geometry differs from the requested ratio.
- Do not assume dialogue exists merely because `generateAudio` was enabled.
