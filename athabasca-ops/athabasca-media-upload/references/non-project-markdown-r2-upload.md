# Non-project markdown upload to stable R2 key

Use this pattern when the user wants a markdown document shared by URL but explicitly says it does **not** need to be associated with an Athabasca project.

## When to use

- files under `docs/plans/`
- review notes / architecture plans
- shareable markdown artifacts that should not create Media UI rows

## Recommended key shape

```text
shared/plans/<filename>.md
```

Example:

```text
shared/plans/2026-06-02-invite-only-multi-user-auth-and-project-access-control.md
```

## Upload path

Use Athabasca's direct R2 helper, not project media APIs:

```ts
import { uploadFileToR2 } from "./src/server/storage/r2";

await uploadFileToR2({
  localPath: "./docs/plans/<filename>.md",
  key: "shared/plans/<filename>.md",
  contentType: "text/markdown",
});
```

Expected behavior:
- stable public URL
- no project association
- no Media UI row
- overwriting the same key updates the same URL in place

## Verification

Minimum verification:
1. confirm upload helper returned the expected `publicUrl`
2. fetch the public URL with a real `GET` or ranged `GET`
3. inspect body text for expected headings / newly-added phrases

Do **not** stop at local file checks alone.

## Why this matters

A successful local overwrite is not enough if the remote object failed to update or a stale object is still being served. For edited planning docs, verify the remote body contains the new section names or phrases before reporting success.
