---
name: athabasca-script-phase-source-supplied-intake
description: Populate the Athabasca script phase from a user-supplied scene or multiple draft variants, preserving provenance and writing the canonical script report via the live API.
triggers:
  - User gives a script, beat sheet, or deleted scene to add to an existing Athabasca project
  - Need to preserve multiple script variants or reference drafts in one canonical script artifact
  - Script artifacts should be written without mutating DB files directly
version: 1.0.0
---

# Athabasca script source intake

Use this when the user provides a scene/script and wants it added to an existing Athabasca project. The goal is to preserve the supplied text faithfully, write it to Athabasca through the API, and keep provenance clear for downstream shot-list work.

## Why this exists

Athabasca script output should be persisted through the live API as a durable project artifact/report, not by editing DB tables directly. Check the current OpenAPI contract before choosing the exact write route.

Because users often supply more than one draft or a revised reference version, this workflow keeps the drafts intact instead of collapsing them into a single paraphrase.

## Steps

1. Verify the API is live.
   - Example: `curl -sS http://localhost:3000/api/health`

2. Normalize the script artifact against current project needs.
   - The script should be explicit enough to map into shots later.

3. Preserve user wording as much as possible.
   - If the user gave multiple versions, keep them both.
   - Prefer headings like `Version 1`, `Version 2`, or `Reference Draft` rather than merging away differences.
   - Do not silently normalize joke timing, tone, or scene intent.

4. If the input is a source-supplied scene rather than external research, say so in the report.
   - A brief research-style note is fine.
   - The point is provenance: downstream phases should know the script came from the user.

5. If the user is **correcting a core premise or mechanics rule** rather than supplying a full new draft, write a concise script update artifact anyway.
   - This is especially important for sci-fi/comedy premise fixes that downstream visuals have already been assuming.
   - Capture the rule plainly (for example: device works both directions; character can understand TTS through the collar; operational modes have distinct semantics).
   - Prefer a short canonical update note over burying the change only in storyboard docs.

6. Write the script artifact through the live API.
   - Prefer the current project artifact/report endpoint from OpenAPI.
   - Include `title`, `summary`, `contentMarkdown`, and provenance.
   - Include images only when they are required context.

7. Verify the write by reading the project back.
   - `GET /api/projects/:slug`
   - Confirm the markdown still contains all supplied variants or the intended preserved text

8. If a research report already exists, do not overwrite it unless the user explicitly wants that.
   - Write the script artifact separately from unrelated research/concept artifacts.
   - Avoid overwriting unrelated project reports.

9. If the premise correction affects existing shot/storyboard artifacts, treat the script update as only half the job.
   - Update the relevant shot breakdown / storyboard artifact in the same pass so prose canon and visual canon stay aligned.

## Educational science explainer scripts

When the script is derived from a research artifact rather than directly supplied by the user, keep the research synthesis and the production script separate:

- Preserve bibliography, caveats, and deeper notes in the research artifact/report.
- Write the lean VO/visual beat draft in the script artifact/report.
- Avoid teleological language and direct-ancestor overclaims; phrase scientific uncertainty explicitly.
- Use “did you know” facts only when they reinforce the causal survival/adaptation sequence.

See `references/educational-science-explainer-script.md` for a reusable structure and accuracy checklist.

## Recommended content structure

Use a short top-level title, then preserve the source text:

- Title: `Deleted Scene: ...`
- Optional intro note: why the scene matters or how it should be used
- Versioned subsections for each supplied draft
- Scene headings and dialogue preserved verbatim
- Optional note for unresolved ambiguities or places where the user may want a later polish pass

## Example payload

```bash
python - <<'PY'
import json, urllib.request

slug = 'example-project'
payload = {
  'phase': 'script',
  'title': 'Deleted Scene: Scorpion Accuracy Department',
  'summary': 'Two preserved reference versions of the same deleted-scene joke.',
  'contentMarkdown': '# Deleted Scene...\n\n## Version 1...\n\n## Version 2...',
  'images': [],
}
req = urllib.request.Request(
  f'http://localhost:3000/api/projects/{slug}/research-report',
  data=json.dumps(payload).encode(),
  headers={'Content-Type': 'application/json'},
  method='POST',
)
with urllib.request.urlopen(req) as resp:
  print(resp.read().decode())
PY
```

## Pitfalls / experiential findings

- Do not write directly to `data/athabasca.db`; use the API.
- Do not paraphrase away the user's timing if the script is meant to be a comic beat sheet.
- Keep both versions when the user explicitly says they want both for reference.
- If the script report is meant to feed shot-list drafting, keep the formatting shot-readable: clear scene markers, time ranges, or beat separators help later extraction.
- If you also need to preserve provenance for later phases, pair this with a lightweight research/source intake report rather than stuffing those notes into the script itself.
- When a user asks to add a script and the project already contains research/concept/visual reports, write only the script-phase report unless they explicitly ask to revise the other phases too.

## Verification checklist

- `GET /api/projects/:slug` shows a report with `phase: "script"`.
- The report content still contains all intended script variants.
- The script remains readable for downstream shot-list work.
- Any separate research report remains untouched unless explicitly updated.
