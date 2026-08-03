# Skill reconciliation notes

This change gathers the Athabasca skill learning that existed outside the tracked
`athabasca` `master` baseline when this repository was created:

- the untracked `athabasca-short-form-growth-lab` package from the main
  Athabasca checkout; and
- Athabasca-specific packages found in the Cliphouse Hermes-profile skill tree.

## Consolidation choices

The following profile-local packet-dispatch skills overlapped at the same user
intent. Their durable guidance is retained verbatim as named support references
under `athabasca-ops/athabasca-prompt-packet-production`, whose `SKILL.md` is
the sole discovery entrypoint:

- `prompt-packet-dispatch`
- `prompt-packet-revision-control`
- `production-prompt-dispatch`
- `narrative-video-dispatch`
- `reference-conditioned-video-dispatch`
- `reference-conditioned-video-prompt-fidelity`
- `reference-governed-video-dispatch`

Likewise, `athabasca-video-continuity-dispatch` is retained under the
`athabasca-video-continuity` umbrella. This preserves the accumulated
procedures without creating competing top-level triggers for the same work.

`athabasca-seedance-prompt-docs` is placed in `athabasca-ops` because it is a
project-attached packet/dispatch operation rather than a generic craft method.

The historic `ATHABASCA_SKILLS_AUDIT_2026-05-31*` scratch documents are not
included: they contain stale local-path assumptions and describe an earlier
migration, rather than a reusable skill or current repository policy.
