# Educational explainer: research-to-script kickoff pattern

Use when a user starts a new Athabasca project and immediately asks for literature research plus a rough educational explainer script.

## Pattern validated in Beaver Evolution

1. Create the project via `POST /api/projects` with enough init context:
   - `name`, `shortDescription`, `objective`, `audience`
   - `runtimeTargetSeconds` from requested range midpoint when useful
   - `targetPlatforms` such as `YouTube`
   - `currentPhase` can be set to the most advanced phase actually populated, e.g. `script`, while `phaseStatuses` marks `init`, `research`, and `script` as `drafted`.
2. Use scholarly/web research tools to collect sources before synthesis.
   - Prefer primary/peer-reviewed sources for evolutionary/scientific claims.
   - Use accessible sources such as Animal Diversity Web for student-facing morphology/behavior facts, but label them as reference/context rather than core evolutionary evidence.
3. Persist sources with `POST /api/projects/:slug/research-sources` before writing the synthesis.
4. Extract durable, production-useful insights with `POST /api/projects/:slug/research-insights`:
   - `narrative_arc` for the explanatory sequence
   - `messaging` for misconception corrections
   - `other` for domain facts that do not fit audience/market categories
5. Write the research synthesis as `POST /api/projects/:slug/research-report` with `phase: "research"`.
6. Write the rough explainer script as a separate `research-report` with `phase: "script"`.
7. Verify with `GET /api/projects/:slug` and confirm both reports exist.

## Content guidance

- Preserve epistemic caution: distinguish consensus, strong inference, and hypotheses.
- For evolutionary explainers, avoid direct-ancestor overclaims unless a source explicitly supports them. Prefer: “relative,” “stem lineage,” “sister lineage,” or “shows this trait was present by…”
- Convert research into a student-friendly trait sequence: survival pressure → adaptation/behavior → downstream ecological effect.
- Keep a bibliography in the research report even if the script stays lean.
- If the user asks follow-up “did you know” questions, answer from sources and consider appending a later research addendum only if asked to persist revisions.

## Verification snippet

```bash
python - <<'PY'
import urllib.request, json
slug = 'project-slug'
with urllib.request.urlopen(f'http://localhost:3000/api/projects/{slug}') as r:
    data = json.load(r)
for rep in data['project'].get('researchReports', []):
    if rep.get('phase') in ('research', 'script'):
        print(rep.get('phase'), '|', rep.get('title'), '|', rep.get('id'), '| chars', len(rep.get('contentMarkdown') or ''))
PY
```
