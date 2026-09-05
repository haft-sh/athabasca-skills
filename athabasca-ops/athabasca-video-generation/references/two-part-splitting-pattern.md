# Two-Part Splitting Pattern for >15s Seedance 2.5 Generations

## Problem

Seedance 2.5 (`dreamina-seedance-2-5-260628`) supports max 15 seconds. For longer narrative sequences, split into two coordinated 15s parts.

## Pattern

### Part selection

Split at a natural narrative break. Common splits:
- **Arrival/setup → payoff/resolution** (e.g., tryout drills → coach approval)
- **Setup/action → result/reaction** (e.g., action beats → aftermath)
- **First half of story → second half** (e.g., 30s scene split into two 15s halves)

### Reference stack

Both parts share the same reference images. The Part 2 prompt must re-establish the reference stack (no implicit carryover from Part 1).

### Prompt structure

Each part prompt should:
1. State `Part N of 2` in the opening line
2. Include the full reference stack (no abbreviations)
3. Include all global locks (style, identity, wardrobe, field)
4. Describe only the beats for that part
5. Part 2 should naturally continue from Part 1's end state without resetting geography or blocking

### Dispatch

**Parallel dispatch** (preferred for speed): dispatch both parts simultaneously. Both use unique idempotency keys. The tool wrapper may time out on one or both — this is expected.

**Sequential dispatch** (fallback): dispatch Part 1, wait for result, then dispatch Part 2 with continuity references from Part 1's last frame.

### Timeout handling

Seedance 2.5 15s generations at 480p typically take 4–6 minutes. The Hermes `athabasca_request` tool times out at 420s. When this happens:
1. Do NOT resubmit (risk of duplicate paid generation)
2. Poll `GET /api/projects/:slug/media?limit=5` sorted by newest
3. If the asset appears in the catalog, it completed asynchronously
4. If not in catalog after 8+ minutes, check `GET /api/projects/:slug/generation-logs` for pending status

### Idempotency

Use distinct idempotency keys for Part 1 and Part 2. Example: `{scene}-part1-{hash}` and `{scene}-part2-{hash}`.

## Example (GLY Scene 7)

**Part 1** covers: arrival, Shell Breath, clean handoff, repeat rep, pass catch, team run.
**Part 2** covers: ladder station, tackle-fit station, coach approval.

Both use the same 9-image reference stack. Part 2 re-states the full stack in its prompt.
