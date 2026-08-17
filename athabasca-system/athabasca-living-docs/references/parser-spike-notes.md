# Living Docs Parser Spike Notes

Use this when moving from a Living Docs plan into first implementation work.

## Start with the reusable core

Before DB schema, Elysia routes, or React editor UI, build a small server-side core that can be tested without the app runtime:

- manifest types and validation
- prompt-preview HTML import into a v1 manifest
- structured patch application for `setText` and `replaceAssetRef`
- serializer that emits inert public HTML
- public manifest projection separate from any future private draft manifest

This gives the later API/UI work a stable contract and avoids mixing parser uncertainty with migrations or frontend state.

## Fixture strategy

Preferred fixture: an existing prompt-preview HTML media asset or R2 URL for the project under test.

If the real public fixture cannot be fetched in the current environment:

1. Do not claim the real fixture passed.
2. Add a compact representative fixture in the focused test file.
3. Exercise the same contracts: prompt groups, prompt text, settings, reference/candidate assets, `data-ath-*` metadata, and hostile script/event-handler input.
4. Leave real-fixture verification as an explicit follow-up once network/API access is available.

## Dependency posture

Check `package.json` and existing code before adding HTML parsing dependencies. Athabasca may not already have `cheerio`, `jsdom`, or server-side DOM tooling.

For the controlled prompt-preview shape, a narrow deterministic parser is acceptable for a spike if:

- it is isolated in one module
- it treats imported HTML as untrusted input
- tests cover the expected document shape and sanitizer behavior
- the production plan still allows replacing the parser if broader arbitrary HTML support becomes necessary

## Real Prompt Preview DOM shape

Existing GLY/Seedance prompt-preview artifacts may not use the synthetic `data-ath-*` / `<figure>` shape. The parser spike should also support the production-style DOM used by generated prompt previews:

- prompt groups as `<section class="group-card" id="group-a">` with headings like `Group A — ...`
- reference and candidate areas delimited by `<h3>Reference Images</h3>` and `<h3>Candidate Images</h3>`
- image cards as `<article class="ref-card">` / `<article class="ref-card candidate-card">`, not just `<figure>`
- asset IDs stored in `<code>asset_...</code>` inside each card
- labels often in `<h5>` links, with image URLs on nested `<img src="...">`
- prompt text in a `<pre>` following a heading like `Seedance Prompt — Expanded / Copy Paste`

When network access is unavailable but a local generated artifact exists under `artifacts/` or another untracked work area, use it for a sanity parse; then add a reduced real-DOM fixture in the focused test file so the regression does not depend on untracked files.

A good real-artifact sanity check is to print, per group, prompt length plus reference/candidate counts. For the GLY A2S2 v1 artifact, expected shape was three groups with non-empty prompts and counts around `A: 5 refs/6 candidates`, `B: 3 refs/7 candidates`, `C: 4 refs/6 candidates`.

## Minimum focused tests

Cover at least:

- parses prompt-preview groups into a v1 manifest
- preserves title, document type, artifact type, and source URL/media metadata where available
- extracts prompt text, settings, references, and candidates
- parses the real Prompt Preview article-card DOM shape, not only a synthetic annotated fixture
- applies one `setText` operation
- applies one `replaceAssetRef` operation
- serializes public HTML with embedded inert manifest JSON
- strips imported `<script>` blocks, event handlers, and `javascript:` URLs from serialized output

Run focused tests first, then full typecheck. TypeScript strictness, especially `noUncheckedIndexedAccess`, commonly catches unsafe regex capture assumptions in parser code.
