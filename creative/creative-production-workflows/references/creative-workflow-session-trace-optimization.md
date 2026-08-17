# Whole-session trace optimization for creative workflows

Use this reference when a user wants to finish a real animation, film, design, or generative-media project and then use the complete agent session to optimize the broader workflow, including `SOUL.md`, skills, templates, and tool policy.

## Core sequence

Prefer:

1. Complete the real creative work.
2. Capture the entire redacted session lineage and artifact provenance.
3. Label the outcome and explicit user corrections.
4. Segment the trace into decision-centered episodes.
5. Establish a baseline on train/validation/holdout cases.
6. Optimize one workflow layer at a time.
7. Promote only verified improvements.

Do not optimize a completion-oriented persona from an ideation-only or unfinished trace. The finish line reveals whether the agent can review, revise, recover from failures, verify deliverables, and preserve approval state.

## Capture before cleanup

Capture the session before pruning messages, deleting failed runs, rewriting receipts, or reorganizing project files. Preserve:

- user prompts and corrections
- assistant responses
- tool calls and tool results
- compaction/logical lineage
- generated and edited artifacts
- prompts, provider/model settings, attempt limits, and receipts
- review notes and rejected candidates
- approval/canon state
- export/delivery verification
- costs or bounded-attempt information when available

Export secrets-redacted JSONL and a tool-oriented trace. Also export a logical Markdown lineage so pre-compaction ancestors remain human-readable. Never opt out of redaction for an optimization corpus. Generate checksums for the exported bundle.

Use `scripts/capture-creative-session.sh`:

```bash
scripts/capture-creative-session.sh <profile> <session-id> [label] [output-root]
```

If a project spans unrelated sessions, capture each session and group them under one project manifest. Logical lineage joins compaction ancestry; it does not merge unrelated sessions automatically.

## A raw trace is evidence, not a dataset

A transcript records what happened but not whether it was good. Before optimization, label:

- creative objective
- final artifact paths and hashes
- actual completion evidence
- owner approval/rejection and evidence
- what worked
- what failed and why
- direct user corrections
- workflow bottlenecks
- provider/tool failures
- spend/attempt notes
- noisy or sensitive regions to exclude

Do not train from an unlabeled trace. Preserve unsuccessful attempts when they reveal a decision boundary; exclude irrelevant operational noise rather than teaching the optimizer to imitate it.

## Segment by decisions, not message count

Turn the session into bounded episodes around meaningful decisions, for example:

1. Brief and intent framing
2. Reference and authority selection
3. Story, shot, or performance decision
4. Prompt/generation-plan compilation
5. Paid-action authorization
6. Provider execution and failure recovery
7. Output inspection and diagnosis
8. User critique and revision
9. Editorial/postproduction decision
10. Delivery verification and approval

Each episode should include:

- request
- context available at that moment
- candidate response and tool trace
- resulting artifact or state change
- user feedback or objective outcome
- dimension scores and hard failures
- evidence-backed failure explanation
- actionable behavioral mutation direction

Do not leak future information into an episode's task context. Review notes and later corrections belong to the evaluator/reflection side unless they were available to the agent at that moment.

## Optimize the whole workflow in stages

A complete trace can inform every layer, but avoid mutating all layers in the first run. Use this order:

1. **Persona evolvable block** — judgment, initiative, recommendation behavior, communication, and adaptability.
2. **Project-family skill/reference** — authority, canon, directory semantics, and project rules.
3. **Generation skill** — preflight, prompt compilation, bounded testing, receipts, and recovery.
4. **Review/QC skill** — media inspection, defect diagnosis, and revision selection.
5. **Templates/scripts/tool descriptions** — manifests, exports, receipts, verification, and deterministic probes.

Keep safety, current-action authorization, secrecy, canon, and evidence gates pinned. Staging lets reviewers attribute score changes to a particular workflow layer and revert regressions cleanly.

## Use corrections as high-value supervision

Direct user corrections are usually the strongest examples. Preserve the chain:

```text
initial request
→ agent decision/output
→ user correction
→ revised decision/output
→ why the revision was better
```

Convert corrections into behavioral feedback, not superficial wording changes. For example, “too polished and sentimental” should become concrete guidance about performance, timing, camera restraint, sound, or ambiguity rather than merely adding the words “awkward” and “unresolved.”

## Split and holdout discipline

Do not randomly split adjacent moments from one correction chain across train and holdout. Keep linked revisions together. Hold out entire creative situations, sequences, or projects so the evaluation measures general workflow judgment rather than memorization of one character, provider, or visual vocabulary.

A single completed project is an excellent anchor corpus, not sufficient proof of generality. Final promotion should include materially different tasks such as dialogue, documentary, music-driven work, non-generative production, and delivery/QC.

## GEPA evaluation

For GEPA or another reflective optimizer:

- run candidates through the real agent/tool surface when practical
- keep task model, reasoning settings, fixtures, and network policy fixed
- capture response and tool trace
- return scalar/dimension scores plus Actionable Side Information
- keep private holdout feedback invisible to the optimizer
- audit evaluator explanations against human judgment
- require explicit model-call budget authorization

Useful Actionable Side Information includes observed behavior, evidence, failure cause, and a concrete mutation direction. “Be more creative” is not actionable; “the candidate chose the easiest generation path despite the emotional concept being stronger; mutate it to test the high-risk concept with a bounded proof before falling back” is.

## Promotion gate

Promote a workflow change only when:

- pinned constraints remain intact
- validation improves by a predeclared margin
- no important holdout dimension materially regresses
- hard failures remain zero
- human review agrees with evaluator reasoning on a sample
- added complexity or prompt length produces measurable value
- the owner approves the diff

Keep every candidate, corpus version, evaluator version, and score report. Never overwrite the only baseline.
