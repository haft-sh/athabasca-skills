---
name: creative-production-workflows
description: "Use when generating, editing, or ideating creative work, building a dedicated creative Hermes profile, optimizing a creative agent from session traces and correction signals, or reducing long-session context friction. Routes lean profile bootstrap, GEPA-ready workflow evolution, context-efficient production sessions, ComfyUI media workflows, humanizing, ideation, and authorized prompt stress testing."
version: 1.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [creative, comfyui, image-generation, writing, ideation, prompt-engineering]
    related_skills: [hermes-agent]
---

# Creative Production Workflows

## Overview

This is the umbrella for creative production and creative prompt systems: generating media, improving prose voice, brainstorming project ideas, and preserving specialized prompt/test harnesses as support files rather than separate one-off entry points.

The shared pattern is to turn an ambiguous creative request into a concrete artifact, inspect the right constraints, execute with the configured toolchain, and verify the output rather than merely describing it.

## When to use

Use for:
- creating or upgrading a dedicated Hermes profile for animation, filmmaking, visual development, editorial, sound, or generative media
- optimizing long creative sessions when context compression becomes slow, costly, or lossy
- ComfyUI install/launch/health checks, workflow execution, model/node management, and image/video/audio generation through workflow JSON
- rewriting or humanizing text to remove AI writing patterns and add voice
- constraint-driven brainstorming for software/art/writing/project ideas
- prompt stress-testing or jailbreak/red-team prompt harnesses when explicitly authorized and safe

## Route by creative task

| Task | Route | Support detail |
|---|---|---|
| Generate media with ComfyUI | ComfyUI workflow execution | `references/comfyui.md`, ComfyUI scripts/workflows |
| Build a dedicated film/animation Hermes profile | Lean creative profile bootstrap | `references/creative-hermes-profile-bootstrap.md` |
| Evolve or benchmark a creative persona | GEPA-ready persona optimization | `references/creative-persona-gepa-optimization.md` |
| Optimize a whole creative workflow from a completed session | Capture, label, segment, then optimize layers in stages | `references/creative-workflow-session-trace-optimization.md`, `scripts/capture-creative-session.sh` |
| Reduce user-agent friction from correction signals | Extract candidate correction episodes, human-label root cause, and optimize for faster accepted work | `references/creative-friction-feedback-optimization.md`, `scripts/extract-creative-friction.py` |
| Reduce long-session compression latency/cost | Measure resolved compressor routing; prefer phase boundaries, lean fixed context, and benchmarked auxiliary models before plugins | `references/hermes-creative-session-context-management.md` |
| Make prose sound less AI-written | Humanizer | `references/humanizer.md` |
| Generate project ideas | Ideation | `references/ideation.md` |
| Authorized prompt red-team/jailbreak testing | Prompt stress testing | `references/godmode.md`, scripts/templates |

## Dedicated creative Hermes profiles

When a user wants a primary Hermes identity for animation, filmmaking, visual development, editorial, sound, or generative media, build a **lean always-loaded profile with rich focused skills**. Do not equate “fat” with mass-enabling every creative/model skill. Preserve the baseline skill state unless the user requests a capability or the workflow proves it is needed.

Keep stable identity and decision behavior in `SOUL.md`; keep detailed production procedures in class-level skills and current project state in workspace files/references. Use the profile-bootstrap procedure for clone mode, OAuth-pool preservation, credential strategy, provider readiness, sticky-primary verification, profile-isolated shell pitfalls, and a real skill-loaded boot test.

For persona refinement or automated prompt evolution, use a pinned/evolvable split, behavioral corpus, weighted rubric, actionable side information, and private holdout promotion gate.

When a real creative project is available, finish it before broad workflow optimization. Capture the full redacted session lineage and artifacts, label the outcome, and segment the trace around decisions rather than feeding one raw transcript directly to GEPA. Optimize persona, project rules, generation, QC, and templates in staged runs so gains and regressions remain attributable.

Treat direct corrections such as “this didn't work,” “this is wrong,” “not what I meant,” “too much,” or “fix this” as high-value friction anchors—not automatic failure labels. Extract the preceding attempt and recovery window, then human-label whether the event was agent-caused friction, normal iteration, taste refinement, provider failure, changed direction, productive disagreement, or a false positive. Optimize for fewer repeated instructions and faster accepted artifacts while preserving creative judgment and making the agent easy to correct.

For long production sessions, separate **behavioral context management** from **runtime compression**. Skills can guide phase-boundary capsules and trace capture, but they do not speed Hermes' internal compressor. Diagnose exact compression timestamps, rough before/after tokens, and resolved auxiliary routing before changing anything. Prefer phase-boundary sessions and a lean fixed prompt; then benchmark a dedicated long-context auxiliary model. Use a Context Engine plugin only when incremental or retrieval-based context management is worth a real implementation and test surface.

Treat `/new` as a session boundary, not a new project. Before ending a productive session, flush deterministic artifact/run evidence and candidate semantic decisions into project-owned append-only lineage, materialize a compact current-state snapshot, record the session's event range, and export the immutable redacted trace. The next session should load the snapshot, link to the previous close event, and retrieve deeper context on demand. Summaries and indexes are rebuildable projections; raw traces, hashes, explicit user evidence, and append-only events remain authoritative. Multiple exported sessions can therefore remain one GEPA project corpus without preserving one giant session.

See:
- `references/creative-hermes-profile-bootstrap.md`
- `references/creative-persona-gepa-optimization.md`
- `references/creative-workflow-session-trace-optimization.md`
- `references/creative-friction-feedback-optimization.md`
- `references/hermes-creative-session-context-management.md`
- `scripts/capture-creative-session.sh`
- `scripts/extract-creative-friction.py`

## ComfyUI workflow

1. Detect whether ComfyUI CLI/server/GPU/model prerequisites are available.
2. Use official comfy-cli for lifecycle where possible.
3. Use direct REST/WebSocket API for workflow execution and monitoring.
4. Work from API-format workflow JSON.
5. Extract controllable parameters before running.
6. Run with explicit parameters and monitor output/logs.
7. Verify generated files exist and inspect them when relevant.

Support files include reusable scripts under `scripts/` and workflow JSON under `references/comfyui-workflows/`.

## Humanizing text

When revising prose, remove common AI-isms and add a real voice:
- avoid vague grand claims and promotional framing
- replace outline-like transitions with specific movement
- preserve the user's intent and facts
- calibrate to a sample if the user provides one
- return the revised text, not a lecture about style

## Constraint-driven ideation

When the user wants ideas but lacks direction:
1. Pick or match a constraint.
2. Interpret it broadly.
3. Generate three concrete ideas with stack/time estimates.
4. If the user picks one, build it or turn it into a plan.

## Authorized prompt stress testing

Only use jailbreak/red-team harnesses for allowed testing, evaluation, or research contexts. Keep outputs framed as testing methods and refusal/robustness evaluation rather than instructions to cause harm.

## Verification checklist

- [ ] Dedicated creative profiles keep the always-loaded persona lean and procedures in focused skills.
- [ ] Broad skill stacks were not enabled merely to make the profile look “fat.”
- [ ] Persona optimization uses pinned constraints, train/validation/holdout cases, and actionable evaluator feedback.
- [ ] Whole-session traces are secret-redacted, outcome-labeled, and segmented by decisions before optimization.
- [ ] Correction/friction anchors were human-labeled; normal iteration and provider failures were not misclassified as persona failure.
- [ ] Friction optimization measures faster accepted work without suppressing useful correction, creative pushback, or decisive recommendations.
- [ ] Persona, project rules, generation, QC, and templates are optimized in staged runs rather than mutated together initially.
- [ ] Long-session compression diagnosis used real timestamps and resolved auxiliary routing; a generic skill was not mistaken for a runtime compressor.
- [ ] `/new` boundaries flush project-owned append-only lineage, record session event ranges, preserve immutable redacted traces, and reload a compact state snapshot.
- [ ] Phase-boundary sessions preserve project/GEPA lineage instead of forcing one giant session.
- [ ] Dedicated compressor candidates were checked for context capacity, per-task reasoning configuration, and benchmarked for post-compression continuity—not only latency.
- [ ] Creative output format matches the user's requested artifact.
- [ ] For generated media, real files/URLs were produced and checked.
- [ ] For prose edits, meaning and factual claims were preserved.
- [ ] For ideation, ideas are concrete enough to start building.
- [ ] Red-team prompt tooling is only used in an authorized/safe context.
