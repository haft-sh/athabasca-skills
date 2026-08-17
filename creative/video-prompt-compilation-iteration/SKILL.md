---
name: video-prompt-compilation-iteration
description: Use when revising AI-generated trailer/video prompt compiles from human feedback. Translate creative notes into consistent multi-artifact edits and verification.
---

# Video Prompt Compilation Iteration

Use this when a user is iterating on an AI-generated video/trailer compile built from layered prompt artifacts: prompt summaries, packet YAMLs, keyframe YAMLs, cutspecs, coverage maps, compile receipts, and candidate-direction docs.

This skill is for **creative iteration with technical consistency**: taking subjective feedback like pacing, readability, motion, runway, legibility, and emotional performance, then applying it across every artifact that claims to describe the same beat.

## When to use

- The user says a section is too fast, too slow, too abrupt, too legible/illegible, or emotionally wrong.
- The user compares one section against another section and wants matching cadence.
- You are creating a new candidate variant instead of changing an approved baseline.
- The compile stack contains redundant representations of the same beat and can drift if edited incompletely.

## Core rule

Treat human creative feedback as a **cross-artifact contract**, not a single-prompt tweak.

If the user says a beat is "still way too fast" and names a slower reference section, convert that into an explicit comparative rule such as:

- "This handoff must not feel faster than SH020."
- "Use the first half of the beat as runway before the catch."
- "Prefer calmer entry over more dramatic acceleration if both cannot fit."

That rule must appear anywhere the beat is described semantically, not just in one top-level prompt.

## Workflow

1. **Extract the exact delta.**
   - Identify the target beat(s).
   - Identify the comparison beat if the user gave one.
   - Convert the note into a concrete motion rule: later catch, longer runway, slower climb, reduced acceleration, calmer camera rise, etc.

2. **Preserve lineage.**
   - Create a new immutable candidate variant rather than rewriting the previously reviewed candidate in place.
   - Add or update a revision-direction note that states the new rule in plain language.

3. **Propagate the change through the full artifact stack.**
   Update all relevant layers, typically:
   - `prompt.txt`
   - `request.dry-run.json`
   - packet YAML(s)
   - keyframe YAML(s)
   - cutspec YAML(s)
   - review note(s)
   - coverage / craft maps
   - compile receipt / registry / current pointers

4. **Change semantics and timing together.**
   Do not only swap descriptive prose. If the request is about pacing, also update:
   - frame windows
n   - cause/reaction timing
   - camera progress
   - root trajectory
   - event ordering
   - payoff timing

5. **Sweep for stale lineage metadata.**
   After cloning a variant, search for old variant IDs, old paths, stale semantic clauses, stale provider clauses, and stale hashes. Recompute hashes after final edits.

6. **Verify before reporting success.**
   Confirm:
   - artifact hashes match receipt metadata
   - registry points to the new receipt hash
   - current pointers name the new candidate
   - old semantic wording is gone from the new candidate where it matters
   - no provider call/upload was accidentally executed

## Pacing-specific translation patterns

### If the user says a handoff is too fast
Translate toward:
- longer low-entry runway
- later catch / later climb commitment
- slower camera rise
- clearer pre-ascent readability
- fewer abrupt vertical jumps

### If the user compares against another section
Use the comparison as a hard editorial benchmark, not a loose inspiration.

Write the rule explicitly in the candidate direction and in the beat summaries, e.g.:
- "Match the cadence of the later pullback/rise section."
- "Do not let SH019 read faster than SH020."

## Pitfalls

- **Do not update only `prompt.txt`.** The compile may still contain stale claims in packets, keyframes, cutspecs, maps, or receipts.
- **Do not preserve old semantic clauses in maps.** Coverage/craft maps can silently contradict the newly edited beat.
- **Do not treat 'slower' as vague.** Convert it into explicit timing structure: delayed catch, longer runway, calmer rise, later payoff.
- **Do not overwrite the approved active compile** when the user is still reviewing candidate pacing.
- **Do not claim consistency until hashes and pointers are rechecked.**

## Output expectations

When reporting back, state:
- the new candidate direction file
- the new candidate variant root
- the specific beats changed
- the exact pacing rule now encoded
- what was verified
- whether the active approved compile changed (usually it should not)

## References

- `references/pacing-revision-checklist.md` — checklist for translating motion/pacing feedback into a consistent candidate-variant update and verification sweep.
