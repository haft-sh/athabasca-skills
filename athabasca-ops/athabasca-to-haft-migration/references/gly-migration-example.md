# GLY migration example

This reference captures a real Athabasca -> Haft migration-prep run for the `gly` project.

## Source and destination

- Athabasca project slug: `gly`
- Athabasca base URL: `http://100.84.189.23:3000`
- Haft workspace: `~/Sites/haft/main`
- Intended remote site: `https://gly.haft.sh`

## Script used

`/home/nrsimha/Sites/haft/main/scripts/migrate-athabasca-gly.ts`

## Verified export results

The export pass produced:

- 318 total Athabasca assets
- 241 images
- 34 videos
- 43 document assets
- 5 living docs
- 275 remote-only media references
- 48 downloaded/importable source documents

Bundle root:

`/home/nrsimha/Sites/haft/main/tmp/athabasca-gly-migration/gly`

## Important Haft behaviors discovered

### 1. `target-folder=imports/athabasca/gly` is rejected

Haft import-path policy treats `imports`, `manifest`, and `exports` as internal/generated scaffold segments.

Working target folder:

`athabasca/gly`

### 2. Raw HTML import can fail

Observed failure message:

`Uploaded HTML could not be normalized into a safe Haft import artifact.`

Working workaround:

- preserve raw HTML snapshot in the migration bundle
- generate a markdown mirror with extracted text + provenance
- import the markdown mirror into Haft instead of the raw HTML blob

### 3. Binary media should stay out of the normal local import lane

Because the user wanted images/videos to remain remote-only, the correct output was:

- `remote-media-manifest.json`
- `remote-media-manifest.ndjson`
- `remote-media-index.md`

rather than a fake local media ingest.

## Verified local import result

A scratch Haft vault import succeeded after the target-folder and HTML-mirror fixes:

- Imported: 51
- Skipped: 0

Scratch vault path used:

`/tmp/gly-haft-test-vault`

## Remote import command template

```bash
cd ~/Sites/haft/main
haft remote add gly-prod --url https://gly.haft.sh --token-stdin
haft import --remote <remote-slug> '/home/nrsimha/Sites/haft/main/tmp/athabasca-gly-migration/gly/docs-import/athabasca/gly' --target-folder 'athabasca/gly' --recursive
```

## What this reference is good for

Use this as a concrete example when:

- preparing another Athabasca -> Haft migration
- debugging why a Haft import skipped everything
- deciding whether to mirror raw HTML as markdown
- explaining why remote-only media needs a manifest lane instead of the normal binary import flow
