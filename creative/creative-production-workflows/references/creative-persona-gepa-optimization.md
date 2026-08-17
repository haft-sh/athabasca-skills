# GEPA-ready creative persona optimization

Use this reference when improving a creative-production `SOUL.md` or other always-loaded agent persona, especially when the user wants GEPA or another reflective prompt optimizer.

## Start with architecture, not wording

A persona should contain stable identity and decision behavior. Detailed procedures belong in class-level skills; project state belongs in workspace files or skill references.

A strong creative profile is usually **lean in always-loaded context and rich on demand**:

- `SOUL.md`: north star, role, decision hierarchy, adaptive operating loop, judgment, collaboration, truth, and non-negotiables.
- Class-level skills: film development, generative production, postproduction/QC, provider workflows.
- Project-family skill/reference: authority sources, canon boundaries, directory semantics, and reusable project rules.
- Live project files: current candidates, run IDs, receipts, approvals, hashes, and pending gates.

Do not confuse a “fat” creative profile with a maximal skill enablement count. Rich focused skills are useful; broadly enabling unrelated creative/model stacks adds noise and can cause irrelevant routing.

## Persona design pattern

Prefer this shape:

1. **North star** — the outcome the profile protects.
2. **Role** — a coherent identity, not a list of job titles.
3. **Decision hierarchy** — what wins when story, spectacle, schedule, and technical constraints conflict.
4. **Adaptive loop** — e.g. Frame → Inspect → Decide → Make → Evaluate → Learn.
5. **Creative judgment** — specific anti-generic behavior and bottleneck-first testing.
6. **Collaboration** — recommendation style, evidence language, and correction handling.
7. **Truth and authority** — state labels, source precedence, verification.
8. **Non-negotiables** — spend, publication, privacy, canon, and fabrication gates.

Avoid embedding a mandatory end-to-end production checklist in the persona. It makes small tasks heavy and competes with specialized skills.

## GEPA boundary design

Do not evolve the entire persona without constraints. Divide it into:

- **Pinned text:** north star, authority rules, verification requirements, and non-negotiables.
- **Evolvable text:** operating loop, creative judgment, recommendation behavior, and communication style.

Use explicit markers or an assembly function so the optimizer mutates only the intended block. Reject any candidate that removes or weakens pinned constraints regardless of aggregate score.

## Evaluation corpus

Build behaviorally diverse cases rather than paraphrases of one task. Cover at least:

- vague creative direction
- inspection of a real asset before critique
- conflicting reference authority
- under-specified paid generation
- story/performance versus spectacle
- failed provider run and honest receipts
- export/delivery verification
- direct user correction
- identity or continuity failure diagnosis
- canon promotion with ambiguous asset identity
- ideation that requires a ranked recommendation
- live project status versus stale memory
- publication or upload authorization
- sound/picture bottleneck diagnosis
- creative ambition versus production risk
- missing source that cannot be inspected

Split cases into train, validation, and private holdout. Never show holdout feedback to the optimizer.

## Rubric

Use weighted dimensions such as:

- intent alignment
- creative judgment
- actionability
- grounding and verification
- authority and safety
- communication
- adaptability

Add hard failures for fabricated completion, unauthorized spend/upload/publication, secret exposure, canon promotion without approval, and ignoring explicit source authority.

Penalize unnecessary process, persona sprawl, generic “cinematic” language, and passive option dumps.

## Actionable Side Information

GEPA benefits from reflective feedback, not scalar reward alone. Each evaluation should return:

- observed behavior
- dimension scores
- hard failures
- evidence from the response/tool trace
- failure cause
- a concrete behavioral mutation direction

“Be more concise” is weak feedback. “The candidate converted a bounded ideation request into a nine-stage workflow; mutate it to choose a direction first and load process only when execution requires it” is actionable.

## Runtime evaluation

Evaluate the candidate through the actual agent surface when possible:

- disposable profile or isolated persona assembly
- fixed task model and reasoning settings
- clean session per case
- fixture assets or deterministic mocked tool results
- outbound spend, publication, and external mutation disabled
- response and tool trace captured

A direct single-turn LLM benchmark can test tone and judgment, but it does not prove tool-selection or verification behavior.

## Completed-project traces

For whole-workflow optimization, prefer a completed real project over an unfinished ideation trace. Capture the redacted logical session lineage, artifacts, failed attempts, user corrections, approval state, and delivery evidence; then label the outcome and segment the trace into decision episodes. Do not feed one raw transcript directly to GEPA or mutate `SOUL.md`, skills, QC, and templates together in the first run.

Use `references/creative-workflow-session-trace-optimization.md` and `scripts/capture-creative-session.sh` for the reusable procedure.

## GEPA usage

The official `gepa-ai/gepa` package supports `optimize_anything` for arbitrary text artifacts. Use the persona's evolvable block as the seed candidate and the runtime evaluator as the objective function.

Start with a small metric-call budget only after evaluator quality is proven. Increase the budget after human/evaluator agreement is acceptable. Treat model-call spend as an external action that needs a declared budget.

Do not copy a profile's OAuth access or refresh token into an external optimizer. Configure GEPA through a supported, separately authorized provider credential path.

## Promotion gate

Promote an evolved candidate only when:

- pinned constraints are intact
- validation improves by a predeclared margin
- no important holdout dimension regresses
- hard failures remain zero
- human review agrees with evaluator explanations on a sample
- added length has a measurable behavior benefit
- the owner approves the candidate diff

Keep candidate lineage. Never overwrite the only baseline or promoted version.
