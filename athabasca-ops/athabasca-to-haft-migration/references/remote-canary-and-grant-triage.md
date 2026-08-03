# Haft remote canary and delegated-grant failure triage

Use this reference when a local Athabasca→Haft document bundle imports successfully, but the first remote canary fails.

## Safe canary sequence

```bash
haft whoami --json
haft remotes --json
haft import --remote <remote-slug> \
  /path/to/one/html-derived-mirror.md \
  --target-folder 'athabasca/<project>-sanity-check' \
  --wait --json
```

Choose a representative HTML-derived artifact, not a trivial project overview. A Seedance prompt preview or asset inventory exercises long text, headings, symbols, and structured content.

After a successful mutation:

1. Capture the durable job/artifact identifier.
2. Read the imported artifact back through the narrowest available route.
3. Open the public/custom destination and visually inspect rendering.
4. If rich HTML fidelity is required, repeat with one normalized raw HTML artifact. The Markdown mirror only proves the fallback lane.
5. Batch import only after both required lanes pass.

## Failure classification

### Content normalization failure

Typical signal:

```text
document_upload_invalid_html
Uploaded HTML could not be normalized into a safe Haft import artifact.
```

Action: preserve raw HTML in the migration bundle, generate/import a Markdown mirror, and separately improve/test the raw HTML normalizer if fidelity is required.

### Destination trust failure

Typical signal:

```text
HTTP 403
code=route.gate-denied
centralDiagnosticCode=auth.central-grant.bad-signature
```

This occurs before document normalization. Trying another document or switching between equivalent remote records does not test the HTML path.

Action:

- stop before batch import
- verify no remote job/artifact was created
- reconcile the destination verifier with HQ delegated-grant signing configuration/public JWKS
- redeploy or restart through the normal managed-destination path
- re-run the single canary after trust verification

A CLI account can be authenticated and advertise `artifact.import` while the destination still rejects the exchanged target-bound grant. Treat the actual canary mutation as the authorization proof.

## Reporting language

State the layers separately:

- **CLI identity:** authenticated or not
- **Remote capability projection:** advertised or absent
- **Canary mutation:** accepted or denied
- **Artifact verification:** readable/renderable, created-but-unverified, or not created
- **HTML conclusion:** tested, not reached, or fallback-only

Never claim HTML normalization is fixed when authorization failed before the importer received the document.
