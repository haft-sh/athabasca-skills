# Living Docs round-trip proof pattern

Use this when a Living Docs parser/serializer spike needs to move from unit parsing to a credible Phase 0 proof.

## Goal

Prove the controlled document pipeline, not just string parsing:

1. Parse a representative Prompt Preview HTML artifact.
2. Apply structured patch operations.
3. Serialize public-safe HTML.
4. Read back the embedded public manifest.
5. Re-parse the serialized HTML.
6. Verify security and metadata invariants.

## Useful code contracts

Add a small manifest extraction helper rather than relying only on substring assertions:

```ts
parseEmbeddedLivingDocManifest(html: string): LivingDocManifest | null
```

It should locate only inert public manifest scripts, for example:

```html
<script type="application/athabasca+json" data-ath-manifest="living-doc">...</script>
```

Then JSON-parse and validate the manifest with the same manifest validator used by the serializer/parser path.

## Regression test shape

A strong focused regression test should do all of this in one flow:

- parse a reduced real-DOM Prompt Preview fixture (`section.group-card`, `article.ref-card`, `code asset_...`, `Seedance Prompt` `<pre>`)
- patch one prompt field with `setText`
- replace one reference asset with `replaceAssetRef`
- serialize with `serializePromptPreviewHtml`
- extract the embedded manifest and assert the patch is present
- re-parse the serialized HTML and assert the patch is still visible through normal parser heuristics
- assert no active imported scripts or event handlers survive, while allowing only the inert manifest script

Example invariant checks:

```ts
expect(html).not.toMatch(/<script\b(?![^>]*type="application\/athabasca\+json")/i);
expect(html).not.toMatch(/\son[a-z]+\s*=/i);
```

## Proof script shape

For a disposable full-artifact proof, add a small script under `scripts/` that:

- reads the local full Prompt Preview HTML fixture/artifact
- parses it into a manifest
- patches one prompt field and one asset reference
- serializes to `tmp/living-docs/<name>-roundtrip-proof.html`
- extracts the embedded manifest
- re-parses the output
- prints compact counts: source path, output path, group count, refs/candidates per group, embedded manifest block count, reparsed block count

Keep generated proof files under `tmp/` and ignore `tmp/` in git. The script itself can stay committed as a repeatable verification helper.

## Verification checklist

Run, in order:

```bash
bun test src/server/living-docs/__tests__/parser.test.ts
bun run scripts/living-docs-roundtrip-proof.ts
bun run typecheck
```

Then inspect the output HTML for the important markers:

```bash
rg -n "data-ath-doc|data-ath-manifest|<script|onclick=|onload=|javascript:|<patched asset id>|<patched text marker>" tmp/living-docs/<name>-roundtrip-proof.html
```

A good proof output should show:

- `data-ath-doc="living-doc"`
- the patched prompt text marker
- the replacement `data-ath-asset-id`
- exactly the inert manifest script
- no imported executable script/event-handler/dangerous URL remnants

## Pitfall

Do not call Phase 0 complete from parser unit tests alone. A credible spike needs a real or representative artifact round trip and a generated proof HTML artifact. If publishing to R2/API is not implemented yet, report the local proof honestly as the completed sub-target and leave upload/publish as the next integration step, not a fabricated pass.