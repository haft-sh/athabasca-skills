# Pre-generation prompt preview workflow

Use this when the user asks to review or share prompts before sending a paid video job to Seedance or another provider.

## Goal

Create a durable Athabasca review artifact that contains the proposed prompt package, settings, assumptions, and review questions — without dispatching any generation job.

## Pattern

1. Resolve the project and source context from the project detail payload (script report, shot list, current project settings).
2. Draft the prompt preview as a concise Markdown package:
   - clear scope and any interpretation assumptions
   - provider/model/settings defaults
   - clip-by-clip prompts with duration and purpose
   - explicit note: nothing has been sent to the provider yet
   - review questions / decisions needed before generation
3. Save the preview as a project report/artifact rather than sending raw chat-only text.
4. Share the project link and the artifact title/phase so the user can find it in the UI.

## Current implementation note

If the public API does not expose a report-create route, a repo-local Bun script can call `upsertResearchReportForProjectSlug(slug, input)` from `src/server/db/bootstrap.ts`.

Caution: `upsertResearchReportForProjectSlug` is an older report helper with phase-like grouping semantics. Prefer durable media/Living Doc artifacts for prompt preview review unless the live API contract still requires a report write, and avoid overwriting an unrelated existing report.

## Prompt defaults for Seedance review packages

- Prefer short granular clips, 4–8 seconds.
- Use 9:16 when the project is vertical.
- Use 480p for iteration unless the user asks otherwise.
- Keep audio on for ambience/SFX/dialogue unless the user asks for silent/mute.
- Append the quality suffix and `No Music` to Seedance prompts.
- Use role descriptions (`the turtle`, `the guardian`, `the woman`) rather than proper names in Seedance prompts.

## Final response shape

Keep it short:

```text
Saved the prompt preview: [link]
Artifact: [title]
Notes: [scope assumption, nothing generated yet, where to review]
```
