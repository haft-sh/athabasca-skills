# Pacing Revision Checklist

Use this when a user says a beat still feels too fast, too abrupt, or needs more runway.

## Convert the note into an editorial rule

Do not keep the feedback as vague prose like "slow it down."
Rewrite it as a rule with a comparison target when available.

Examples:
- "The handoff must not feel faster than the later landing/pullback section."
- "Use the first half of the beat as runway before the catch."
- "Prefer calmer entry over dramatic acceleration when both cannot fit."

## Update all semantic layers for the edited beat

Minimum sweep:
- `prompt.txt`
- `request.dry-run.json`
- packet YAML(s)
- keyframe YAML(s)
- cutspec YAML(s)
- review note(s)
- shot coverage map
- craft compile map
- compile receipt
- current pointers / registry

## Update timing, not just wording

For pacing changes, check whether these also need edits:
- frame windows
- cause/reaction frame offsets
- camera progress values
- trajectory points
- event names and ordering
- exit wording so the beat does not imply a sudden jump or arrival

## Clone-variant pitfall

When creating a new candidate by copying an older variant, expect stale values to survive in metadata:
- old variant names
- old paths
- old provider clauses
- old semantic clauses
- old hashes

Do a stale-string sweep before declaring the candidate consistent.

## Verification sweep

Before reporting success, verify:
- artifact hashes match receipt metadata
- registry receipt hash matches the actual receipt hash
- current pointers name the new candidate
- the old beat wording is gone from the new candidate where it matters
- no upload / provider call / prediction was executed

## Session note captured from this run

A strong user signal like "way way way more runway" means the prior slowdown was still too conservative. Treat repetition as evidence that the next pass should materially change the beat structure, not merely soften adjectives.
