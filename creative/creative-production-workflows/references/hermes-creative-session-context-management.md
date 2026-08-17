# Hermes Creative Session Context Management

Use this reference when a long animation, filmmaking, or generative-media session becomes slow or expensive near context compression.

## Core distinction

A Hermes **skill** can improve working habits—phase boundaries, session capsules, trace capture, artifact lineage—but it does not replace or accelerate Hermes' automatic context compressor. Faster or alternative automatic compression requires either:

- `auxiliary.compression` provider/model configuration, or
- a Hermes Context Engine plugin selected through `context.engine`.

Do not install a large generic “session compression” skill expecting lower compressor latency. It adds prompt material and may increase context pressure without changing the runtime compressor.

## Diagnose before changing

Establish live facts:

1. Read the target profile's `compression`, `auxiliary.compression`, `model`, and `context` configuration.
2. Inspect agent logs for exact `context compression started` and `context compression done` lines.
3. Record:
   - wall-clock duration
   - source and resulting message counts
   - rough tokens before/after
   - resolved compression provider/model
   - runtime threshold and main-model context length
   - failure, timeout, fallback, or context-length warnings
4. Check the fresh-session fixed prompt and tool-schema footprint. A large always-loaded tool surface raises every request's context and makes compression arrive sooner.
5. Check installed Context Engine plugins separately from skills.

Do not estimate latency from the UI alone when timestamps are available.

## Why compression can be slow

The built-in compressor first prunes old tool results cheaply, then sends the middle conversation section to an auxiliary LLM for a structured summary. With `auxiliary.compression.provider: auto` and no model override, Hermes resolves the main provider and main model. A large creative session can therefore ask an expensive reasoning model to summarize hundreds of thousands of tokens on the critical path.

The configured summary model must have enough context for the compression payload. A cheap model with a smaller context window can fail or force a lossy fallback. Verify model context capacity before benchmarking it.

## Optimization order

### 1. Phase-boundary sessions with project-owned lineage

At natural production boundaries—brief, previsualization, generation, review/revision, postproduction, delivery—checkpoint durable state and begin a fresh session. This is usually the fastest and cheapest intervention.

Do not make a manually maintained prose capsule the only bridge. A robust `/new` boundary uses project-owned storage with:

- a stable `project_id`
- immutable redacted session exports
- append-only lineage events
- stable `decision_id`, `artifact_id`, and `run_id` values
- artifact hashes and provenance
- explicit approval/canon evidence
- a compact materialized current-state snapshot
- a per-session event cursor range
- a rebuildable retrieval index

Before `/new`, flush deterministic file/tool/provider evidence, propose semantic decision/correction events from only the unprocessed delta, materialize current state, write a session-close event, and export/checksum the outgoing trace. On the next session, load current state, link the new session-start event to the prior close event, and retrieve deeper history on demand.

Raw traces and append-only evidence remain authoritative. Summaries, capsules, and indexes are projections that may be rebuilt and must never silently promote approval or canon.

A multi-session project still forms one optimization corpus. Export every relevant session and link episodes through project ID, event ranges, artifacts, decisions, hashes, approvals, and outcomes. Do not keep one enormous session solely to obtain a “whole trace.”

### 2. Slim the fixed context

Keep the creative profile lean:

- enable only tools used by the production workflow
- avoid broad skill stacks
- keep `SOUL.md` focused on identity and decisions
- put procedures in focused skills and project state in workspace files
- avoid repeatedly loading large references or raw tool outputs

This reduces normal-turn latency and delays compression. It may not directly reduce the middle-section summary payload by the same amount, so measure both turn latency and compression latency.

### 3. Benchmark a dedicated compressor

Use an explicit fast, low-cost model only when its context window can safely hold the compression payload. Benchmark against a fixed redacted session export before making it the profile default.

For OpenAI Codex auxiliary compression, per-task reasoning is configured under `extra_body.reasoning`, not through the main agent's reasoning setting. A strong creative-lineage starting candidate is:

```yaml
auxiliary:
  compression:
    provider: openai-codex
    model: gpt-5.6-luna
    extra_body:
      reasoning:
        effort: low
```

A reasoning-disabled candidate uses:

```yaml
extra_body:
  reasoning:
    enabled: false
```

On the Codex auxiliary path, `enabled: false` omits the explicit reasoning request but does not guarantee that the backend performs zero hidden reasoning. Prefer `low` as the predictable baseline when decision causality and approval state matter; benchmark disabled reasoning as a challenger. Do not assume a model tier or lower reasoning level is faster until the same archived payload proves it.

Compare:

- compression wall time
- input/output tokens and real billing mode
- retained decisions, constraints, corrections, artifact paths, and approval state
- false approval or canon transitions
- post-compression task success and fresh-session recovery
- summary drift after repeated compressions

Do not compare summary prose alone. The correct metric is whether work continues accurately and efficiently afterward.

### 4. Manual focused compression

`/compress <focus>` on a smaller context may finish faster and preserve the next production phase better. It can also increase total compression frequency and cost. Use deliberately near phase boundaries, not as a reflex after every turn.

### 5. Context Engine plugin

Use a plugin when the desired architecture is incremental or retrieval-based rather than one-shot summarization. Candidate strategies include:

- incremental structured state
- persistent decision/artifact graph
- retrieval over archived turns
- deterministic pruning plus selective summarization
- agent-callable context search

A Context Engine plugin is a software component with lifecycle and correctness tests, not a prose skill.

## Evaluation criteria for creative work

Compression quality must preserve:

- creative objective and intended emotional effect
- current shot/sequence state
- reference authority boundaries
- explicit user corrections and taste signals
- accepted and rejected candidates
- artifact paths, versions, hashes, prompts, and provider settings
- spend/attempt authorization
- canon and approval state
- unresolved blockers and exact next action

A shorter summary that drops these is not an improvement.

## Session evidence pattern

One observed long creative/profile-building session compressed approximately 316k rough request tokens to 139k, reduced 278 messages to 153, and took about 98 seconds because `auto` selected the main reasoning model. The durable lesson is not those exact values; it is to inspect resolved routing and timestamps, then benchmark a dedicated long-context auxiliary model or use phase boundaries.

## Common pitfalls

1. **Installing a compression skill as a runtime fix.** Skills affect agent behavior; the compressor is configured or replaced at the runtime/plugin layer.
2. **Selecting a cheap model without checking context length.** The entire middle section may be sent in one call.
3. **Raising an already-high trigger.** This reduces frequency but makes each event larger and raises overflow risk.
4. **Optimizing only latency.** A fast summary that loses approvals, corrections, or artifact lineage creates more downstream friction.
5. **Keeping one giant session for training lineage.** Multiple exported sessions can form one project corpus without paying giant-context costs.
6. **Treating every correction as compression-worthy memory.** Preserve consequential decisions and repeated preferences; leave transient wording and tool noise behind.

## Verification checklist

- [ ] Exact compression duration and resolved model came from logs.
- [ ] Billing mode was distinguished from direct-API list-price estimates.
- [ ] Candidate auxiliary model has sufficient context.
- [ ] Fixed tool/skill prompt footprint was measured.
- [ ] Phase-boundary sessions preserve trace and artifact lineage.
- [ ] Benchmark checks post-compression task continuity, not only summary appearance.
- [ ] No runtime configuration was changed without an explicit decision on speed, cost, and quality trade-offs.
