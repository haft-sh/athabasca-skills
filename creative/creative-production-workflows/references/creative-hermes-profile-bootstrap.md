# Dedicated Hermes profile for creative production

Use this procedure when a user wants a primary Hermes profile dedicated to film, animation, visual development, generative media, editorial, or sound.

## Profile creation strategy

Choose the clone mode deliberately:

- `--clone` copies config, `.env`, `SOUL.md`, and skills, but not the full credential/runtime state.
- `--clone-all` is the right starting point when the new profile must inherit working OAuth credential pools and the full tool/skill environment.

Example:

```bash
hermes profile create <profile> \
  --clone-all \
  --clone-from <source-profile> \
  --description "Primary creative-production profile for animation, filmmaking, visual development, editorial, sound, and delivery verification."
```

Do not leave the cloned operational/software persona in place. Replace the new profile's `SOUL.md` with a creative-production persona before declaring it ready.

## Recommended creative persona coverage

Keep the always-loaded persona compact and behavioral. It should establish:

- a north star for emotional and production outcomes
- a coherent role such as director-producer, not a long list of job titles
- a decision hierarchy for intent, story, performance, motion/edit, finish, and packaging
- an adaptive loop such as Frame → Inspect → Decide → Make → Evaluate → Learn
- story-before-spectacle and bottleneck-first judgment
- authority separation for identity, environment, composition, motion, lighting, and style
- explicit states such as proposal, experiment, candidate, approved, canonical, and delivered
- recommendation behavior: choose, rank, and explain rather than dumping options
- generation approval, spend, provenance, verification, and fabrication gates

Detailed brief-to-delivery workflows, provider procedures, and media-QC commands belong in class-level skills. Project-specific directory rules and current state belong in workspace instructions or project-family references.

Workspace instructions (`AGENTS.md`, `RUNBOOK.md`, `SESSION_CAPSULE.md`, manifests, approvals) remain higher authority than the persona. For GEPA-ready persona evolution, see `references/creative-persona-gepa-optimization.md`.

## Configuration pass

After cloning, review rather than blindly retaining the source profile's config:

1. Set the intended model/provider.
2. Set a useful creative workspace as `terminal.cwd` when one is clearly primary.
3. Remove unrelated `skills.external_dirs` inherited from another project.
4. Preserve the baseline enabled/disabled skill state unless the user requests a capability or a real workflow proves it is needed.
5. Remove inherited operational toolsets that cause irrelevant behavior in creative sessions.
6. Verify image and video provider configuration separately from tool enablement.
7. Set an intentional credential-pool strategy.

For a profile that must consistently prefer the first/highest-priority OAuth credential, use:

```yaml
credential_pool_strategies:
  <provider>: fill_first
```

`round_robin` rotates credentials and therefore does not mean “keep using the credential shown first.”

Do not mass-enable ComfyUI, TouchDesigner, local-model, audio, segmentation, transcription, or media-utility skills simply because the profile is creative. Enable a capability when the user asks for it, a project requires it, and its provider/dependency path is actually usable. A “fat” profile should mean rich, focused class-level skills—not maximum context surface.

## Custom class-level skills

A strong creative profile benefits from a small set of rich class-level skills rather than many narrow project notes:

- film development and preproduction
- generative animation and provider-run provenance
- postproduction and technical QC
- an optional project-family skill that points to live authority files and preserves workspace boundaries

Project-specific run IDs, hashes, and current candidate state belong in the project's files or a reference under the project-family skill, not in the generic workflow body.

## Primary-profile and alias setup

Set the sticky primary profile:

```bash
hermes profile use <profile>
```

Verify the root Hermes active-profile marker, not merely the profile selected by the current process. A running session can remain pinned to its original `HERMES_HOME` even after the sticky default changes.

For a clean verification from an isolated/profile-scoped shell, run with the real user home and remove profile overrides:

```bash
HOME=<real-user-home> env -u HERMES_HOME -u HERMES_PROFILE hermes profile
```

If profile creation places the convenience wrapper under a profile-isolated home, create or repair the wrapper in the real user's `~/.local/bin`:

```bash
#!/usr/bin/env bash
exec /absolute/path/to/hermes -p <profile> "$@"
```

Make it executable and verify it with `<profile-alias> profile`.

## Verification

A profile is ready only after all of these are proven:

```bash
hermes -p <profile> profile
hermes -p <profile> auth list <provider>
hermes -p <profile> config check
hermes -p <profile> tools list
```

Then boot a real one-shot session with one of the custom skills preloaded:

```bash
hermes -p <profile> chat -Q -s <creative-skill> -q "Reply with a fixed verification phrase."
```

Verify:

- expected profile and model
- intended credential is first under the chosen strategy
- custom skill is discoverable and loads
- intended workspace is active
- config check is clean
- image-generation provider is actually configured
- video-generation provider credentials are actually present if paid video generation is expected

An enabled `image_gen` or `video_gen` toolset does not prove the backing provider is ready. Report the difference explicitly.

## Session and Desktop caveat

Changing the sticky primary profile does not rewrite the identity of an already-running CLI, gateway, or chat session. Start a fresh session or select the new profile in Hermes Desktop. Avoid restarting a production gateway merely to prove profile creation unless the user asked for that cutover.

## Pitfalls

- Treating “fat profile” as “enable every creative skill” instead of rich focused skills loaded on demand.
- Embedding a mandatory end-to-end production workflow in `SOUL.md`, making bounded tasks heavy.
- Using `--clone` and assuming OAuth pools were copied.
- Cloning a software-operations `SOUL.md` and forgetting to replace it.
- Leaving unrelated project skill directories attached.
- Using `round_robin` while promising one OAuth credential will remain primary.
- Treating tool enablement as provider readiness.
- Verifying from a shell whose `HOME` or `HERMES_HOME` is still profile-isolated, then misreading the sticky default.
- Declaring the new profile active in the current chat without starting a new session.
