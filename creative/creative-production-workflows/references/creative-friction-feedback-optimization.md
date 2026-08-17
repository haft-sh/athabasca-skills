# Friction-driven optimization for creative agents

Use this reference when the owner wants a creative agent that works smoothly with them: fewer repeated instructions, avoidable corrections, unnecessary questions, unrequested actions, and wasted tool/model calls on the path to an accepted artifact.

## Optimize for accepted work, not agreeable prose

The objective is:

> Minimize owner effort, time, repetition, and avoidable recovery required to reach an accepted creative artifact—without weakening judgment, useful pushback, verification, or authority gates.

Correction phrases are high-value anchors:

- “this didn't work”
- “this is wrong”
- “not what I meant”
- “fix this”
- “I already said…”
- “this is too polished/generic/busy”
- “this is unnecessary”
- “just do it”

Preserve the sequence:

```text
owner intent
→ agent interpretation/action
→ artifact or result
→ correction signal
→ recovery behavior
→ accepted result or further correction
```

The preceding attempt is a candidate negative example; the correction supplies preference information; the recovery window shows whether the agent adapted efficiently.

## Detection is not labeling

Use `scripts/extract-creative-friction.py` on a secret-redacted Hermes session export. It flags candidate episodes from `references/creative-friction-taxonomy.json`.

The detector is deliberately high-recall. Human review must classify each candidate as one of:

- true friction
- normal creative iteration
- taste refinement
- agent error
- tool/provider failure
- missing owner context
- changed creative direction
- external constraint
- productive disagreement
- false positive

A phrase like “fix this” may be an ordinary request. Aesthetic iteration is not automatically failure.

## Root-cause labeling

For true friction, label the mechanism rather than merely restating the complaint:

- misread intent
- failed to inspect available evidence
- weak creative judgment
- passive option dump
- unnecessary question
- unnecessary process
- unrequested action
- forgotten constraint
- stale assumption
- poor tool choice
- avoidable tool execution error
- unverified success claim
- bad state tracking or handoff
- verbosity/structure mismatch

Keep provider outages and external failures separate from persona failures. Optimize the agent's recovery behavior, not the existence of the outage.

## Resolution metrics

Track operational metrics alongside the creative-quality rubric:

- additional owner turns to resolution
- repeated-instruction count
- unnecessary-question count
- avoidable failed tool-call count
- unrequested-work count
- time to first useful artifact
- time to accepted artifact
- first-pass acceptance
- model/provider calls and cost to resolution

Do not optimize for the absence of correction language. That can produce an overcautious agent that suppresses exploration or avoids committing to a creative choice. Optimize for low-cost correction and non-recurrence of the same failure.

## GEPA evaluator design

Use three channels:

1. **Creative quality** — intent, taste, actionability, grounding, and artifact quality.
2. **Interaction friction** — recovery turns, repeated instructions, unnecessary work/questions, and avoidable failures.
3. **Hard constraints** — authorization, secrecy, canon, provenance, and truthful completion.

Return actionable side information:

```json
{
  "observed_behavior": "",
  "friction_label": "",
  "root_causes": [],
  "resolution_metrics": {},
  "creative_quality": {},
  "hard_failures": [],
  "evidence": [],
  "mutation_direction": ""
}
```

Mutation directions must describe behavior. Prefer “inspect the named/latest asset before asking the owner to identify it” over “be less annoying.”

## Episode boundaries

For each correction anchor, include:

- the previous owner turn
- the agent response and relevant tool calls/results
- the correction message
- the recovery response and tools
- the next owner feedback when available
- linked artifact/result identifiers

Keep later correction and acceptance information on the evaluator side; do not leak it into the task context shown to the candidate.

## Split discipline

Keep one correction chain in one split. Do not place the failed attempt in training and its near-identical recovery in holdout. Hold out entire situations or projects so the optimizer must generalize the owner's working preferences.

## Promotion gate

A candidate is better only when it:

- preserves or improves creative quality
- reduces measured friction on validation
- avoids material holdout regression
- keeps hard failures at zero
- remains easy to correct
- does not become passive, sycophantic, or afraid to recommend
- earns owner approval on representative A/B comparisons
