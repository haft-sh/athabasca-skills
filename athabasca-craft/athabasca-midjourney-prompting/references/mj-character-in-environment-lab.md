# Character-in-environment lab

**Date:** 2026-05-14

Use this reference when placing a known character into a known environment and Midjourney keeps preserving one anchor while dissolving the other.

## Inputs that mattered
- one clean character-sheet or identity reference
- one clean environment reference
- a text prompt that repeats the identity anchors and the scene role

## Core finding

A character-sheet-only image prompt can produce beautiful results that ignore scene geography. An environment-only reference can preserve layout but lose identity. The strongest general pattern was:

1. environment URL first
2. character URL second
3. text prompt that restates identity, wardrobe, mood, and the specific action in the environment
4. `--iw 2.0` as the default starting point

## What tended to fail
- character reference only
- overly stylized prompts with weak environment nouns
- high stylization when identity lock was the real priority
- prompts that assume the model will infer scale or blocking from one reference alone

## Working rule

When the user wants both identity and a specific place, use dual references rather than hoping the text prompt can recover the missing anchor.

See `references/mj-character-in-environment-lab-r2.md` for the follow-up round focused on environment variation, grounded lighting, and scale perception.
