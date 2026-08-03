---
name: athabasca-media-generation
description: "Use when generating, comparing, or debugging project-scoped media through canonical generation APIs for still images and video, including direct Codex stills and reference-image edit workflows."
version: 1.2.0
author: Hermes Agent (Athabasca)
metadata:
  hermes:
    tags: [athabasca, media-generation, image-generation, video-generation, reference-images, codex, providers, provenance]
    related_skills: [athabasca-media-upload, athabasca-midjourney-prompting, athabasca-video-prompt, athabasca-video-review]
---

# Athabasca Media Generation

## Overview

Use this skill for project-scoped still-image and video generation. The job is to choose an explicit supported generation route, submit through Athabasca's normalized APIs, persist the result with provenance, and verify the returned project media asset before reporting success.

Keep provider quirks, outage workarounds, and one-off probes in `references/` instead of bloating this entry point.

## When to Use

- The user wants a still image or video generated for an Athabasca project.
- The user wants GPT Image 2 / Codex still generation with Athabasca persistence.
- The user wants reference-image edits using existing project media or newly uploaded sources.
- The user wants the same prompt/source compared across providers or models.
- A generation route is failing and you need to classify the failure.

Do not use this for generic media uploads with no generation step; use `athabasca-media-upload`.

## Core Principles

1. Use Athabasca's normalized project APIs, not direct provider calls, unless doing an explicitly labeled fallback/debug probe.
2. Pass `provider` and `model` explicitly for generation. Do not rely on deprecated project-level default provider fields.
3. Check live capabilities/schema/code before trusting stale provider notes.
4. Upload local, Telegram, cached, or third-party source media into Athabasca first; use project asset IDs/URLs as inputs.
5. Verify the returned Athabasca asset and public URL before reporting completion.
6. Treat phases as optional media tags only; do not assume phase-specific DB tables or phase-gated workflow state.

## Canonical Routes

- Still image: `POST /api/projects/:slug/generate/image`
- Video: `POST /api/projects/:slug/generate/video`

Removed or legacy routes such as top-level `/api/generate/image` or `/generate-image` are not valid operational paths.

## Preflight Checklist

Before submitting a generation request:

1. Resolve the project slug and source assets through the API.
2. Query capabilities/OpenAPI or inspect current adapter code when model support is uncertain.
3. Choose the exact `provider` and `model` for this request.
4. Normalize user-supplied files or URLs into Athabasca media first when they are generation inputs.
5. Set an `idempotencyKey` for retriable paid video generations.

## Image Generation

### Request shape

Typical normalized fields:

- `prompt`
- `provider`
- `model`
- `aspectRatio`: `landscape`, `square`, or `portrait`
- `referenceAssetIds` when supported by the selected provider/model
- `phase`: optional media tag, not a DB column
- `title`
- `provenanceNote`

For Midjourney, keep provider-specific ratio syntax such as `--ar 16:9` inside the prompt when needed, but still send the normalized `aspectRatio` enum in JSON.

### Provider routing defaults

- `openai-codex` / `gpt-image-2`: primary for GPT Image 2 when available.
- `google-gemini`: useful for spatial/UI/reference workflows when its current model capabilities fit.
- `midjourney`: style-heavy work, grids, character sheets, visual exploration.
- `replicate` / Seedream: strong fallback for targeted edits, faces, animals/creatures, and reference-heavy work.
- `fal-ai`: paid fallback/debug route; use deliberately and disclose when selected as a fallback.

Always prefer current live capability data over old reference notes.

### Image rules

- For recurring character/creature work, check for a canonical character sheet first.
- For minimal-delta edits, use the base image as the primary reference, canonical controls as secondary references, and state the only allowed changes.
- For GPT Image 2 `3x3 grid` or `contact sheet` requests, default to one generation that composes the grid directly unless the user explicitly asks for separate tiles or a manual contact sheet.
- When a stale warning claims a provider does not support references, live-probe the canonical route if safe before declaring it unsupported.

Key references:

- `references/image-generation-notes.md` — provider/model notes.
- `references/image-model-routing.md` — routing and reference-support matrix.
- `references/gpt-image-2-single-grid-generation.md` — one-request grid/contact-sheet workflow.
- `references/codex-reference-asset-live-probe.md` — live probe pattern for reference support.
- `references/canonical-prop-repair-with-gpt-image-2.md` — generic atomic image repair pattern.
- `references/operational-pitfalls.md` — edge-case recovery and debugging notes.

## Video Generation

### Required preflight

For video, query live capabilities before selecting provider/model/settings. Duration, resolution, mode support, aspect ratios, first/last-frame support, and audio behavior vary by provider and model.

### Video rules

- Default to the lowest-cost practical settings while iterating unless the user asks otherwise.
- Upload source stills/audio/reference media first and use canonical Athabasca URLs or asset IDs.
- Always use an `idempotencyKey` for retriable paid generations.
- Treat long video runs as long-running operations; do not infer failure from caller timeout alone.
- Separate provider-generation failure from Athabasca persistence or attachment failure.

Key references:

- `references/video-generation-notes.md` — video model/provider notes.
- `references/seedance-2-fal-notes.md` — direct fal.ai fallback/debug pattern only.
- `references/operational-pitfalls.md` — timeout, idempotency, and recovery notes.

## Comparison Workflow

When comparing models/providers:

1. Canonicalize shared source media once.
2. Query live constraints once per medium.
3. Decide whether the user wants exact-match, best-effort, or strongest-common-denominator comparison.
4. Submit one explicit request per provider/model.
5. Record requested settings, normalized settings, success/failure, provider error, and Athabasca asset URL.
6. Disclose fallback settings or unsupported combinations clearly.

## Media Triage APIs

When approving, rejecting, rating, or tagging generated assets:

- Update color/rating: `PATCH /api/projects/:slug/media/:assetId` with `{ "colorTag": "green"|"red"|"yellow"|"blue"|"purple"|null, "ratingStars": N }`
- Set/add/remove tags: `POST /api/projects/:slug/media/:assetId/tags` with `{ "set": [...] }`, `{ "add": [...] }`, or `{ "remove": [...] }`

Color conventions:

- Green: approved/canonical.
- Red: rejected/denied.
- Yellow: superseded/older version.

Use `athabasca-media-triage` for a full review queue.

## Verification Checklist

- [ ] Used the project-scoped generation endpoint for the medium.
- [ ] Passed explicit `provider` and `model`; did not rely on deprecated project provider defaults.
- [ ] Checked live capabilities/schema/code when support was uncertain.
- [ ] Uploaded non-canonical source media into Athabasca first.
- [ ] Submitted normalized request fields, not raw provider payloads.
- [ ] Verified returned Athabasca asset/public URL and attachment state before reporting completion.
- [ ] Moved edge-case or session-specific guidance into `references/` instead of the main skill body.
