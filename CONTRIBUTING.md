# Contributing

## Public-content standard

This repository is a reusable public library, not an operational notebook.

Before submitting a skill or reference, replace or remove:

- personal names, handles, initials, and private contact details;
- hostnames, private addresses, machine names, local filesystem paths, credentials, and service tokens;
- project names, character names, client names, internal asset IDs, and project-specific URLs;
- examples that only make sense in one production.

Use neutral placeholders such as `<project-slug>`, `<asset-id>`,
`$ATHABASCA_HOST`, `<operator-host>`, and `Character A` instead. Keep the
reusable rule, failure mode, command shape, and verification step.

Public provider documentation links are appropriate when they are necessary to
verify a provider capability or API contract. Do not include private dashboards,
project media URLs, or deployment-specific endpoints.

## Skill shape

- Keep `SKILL.md` focused on a real class of work and its decision rules.
- Put detailed examples, incident notes, templates, and commands under
  `references/`, `templates/`, or `scripts/`.
- Merge overlapping discovery entrypoints into a single umbrella skill and keep
  useful specialized material as support references.
- Include a `version` field in new or materially revised skill frontmatter.

## Review checklist

- [ ] No personal, machine-specific, or project-specific residue
- [ ] Entry-point `name` matches its containing directory
- [ ] Examples use generic placeholders and describe their assumptions
- [ ] Commands do not expose credentials or a real deployment target
- [ ] The package does not duplicate an existing umbrella skill
