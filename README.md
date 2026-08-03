# Athabasca Skills

Canonical, version-controlled skill library for Athabasca creative craft, production operations, and system work.

## Layout

- `athabasca-craft/` — writing, visual design, prompt authoring, and review
- `athabasca-ops/` — project, media, generation, and production operations
- `athabasca-system/` — Athabasca application and schema/frontend operations

Each skill is a self-contained directory with a `SKILL.md` entrypoint and optional `references/`, `templates/`, `scripts/`, or `assets/` support files.

The repository deliberately does **not** include a `.hermes/skills` prefix. That prefix belongs to an individual consuming checkout or Hermes profile; this repository is the canonical source that can be mounted or synced into those locations.

## Usage with Hermes Agent

Clone this repo, then register it as an external skill directory:

```bash
hermes config set skills.external_dirs '["~/Sites/athabasca-skills"]'
```

This command replaces the current `skills.external_dirs` value. If you already use other external skill libraries, include all desired directories in the JSON array.

## Migration provenance

The initial commit is an exact export of the tracked `.hermes/skills` tree from `the maintainer/athabasca` `origin/master` at `4649719d94142309be752531492f4dba04b13d3e` (2026-08-03). Follow-up changes are reconciled separately so the baseline remains auditable.
