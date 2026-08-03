# Hosted Haft destination readiness and upgrade preflight

Use this before importing Athabasca content into a managed `*.haft.sh` destination.

## Identity the actual destination first

Do not infer that a configured CLI remote points at the user's custom domain.

1. Resolve the custom hostname to its public IP.
2. Match that IP to the EC2 instance and record instance ID, region, Name tag, and service unit.
3. Run `haft remotes --json` and compare every remote's `apiOrigin` with the intended hostname.
4. Treat a canary sent to a different origin as evidence about that other destination only.

A configured remote labelled `dev` can be a separate machine even when `<remote-host>` is reachable in the browser.

## Confirm binary provenance

On the destination, capture:

- binary path from `systemctl cat <service>` / `systemctl show`
- `haft version`
- SHA-256, size, mtime, and service start timestamp
- current public release from `haft update --check --json`
- current upstream default-branch commit separately

Distinguish:

- **latest published release**: what `haft update --check` advertises
- **latest repository commit**: current `origin/master` or `origin/main`

The published release may legitimately lag the repository. Report both.

## Upgrade older server binaries safely

An old binary may predate `haft update`. If so:

1. Obtain the published release manifest and use the platform archive URL, not an assumed raw-executable URL.
2. Verify the archive SHA-256 from the manifest before extraction.
3. Extract and execute `candidate version` before replacing anything.
4. Preserve the current binary as a rollback copy.
5. Stop the service, atomically replace the binary, start the service, and poll a local health/auth endpoint.
6. Roll back immediately if startup or health verification fails.
7. Verify the public hostname after local health succeeds.

Do not assume a manifest's raw executable URL is actually published merely because the manifest lists it; verify with an HTTP request. The compressed archive may be the available artifact.

## Central-grant migration preflight

A pre-Epic managed destination can have a healthy local `auth-state.json` with `source=local-bootstrap` while lacking the newer local-host-identity record required by central delegated grants.

Before enabling central-grant environment variables:

1. Read `/api/auth/status` and note local claim source/status.
2. Confirm the destination is represented in HQ and appears in `haft remotes --json` with the intended `apiOrigin`.
3. Confirm the HQ server/vault claim IDs correspond to the destination's centrally persisted host identity.
4. Confirm current public JWKS is installed and schema-valid.
5. Only then enable `HAFT_CENTRAL_GRANTS_ENABLED=true` and `HAFT_CENTRAL_JWKS_PATH=...`.

If startup reports `No local host identity is stored for this vault`, roll back the central-grant drop-in but keep the updated binary if it is otherwise healthy. This means the binary update succeeded while managed-destination enrollment remains incomplete.

Never invent claim IDs, copy local-bootstrap IDs into central identity, or patch HQ tables merely to make the verifier start. A proper enrollment flow must create/recover central claims, persist returned central identity locally, install JWKS, and verify a target-bound grant exchange.

## Canary order

After destination enrollment:

1. Re-run `haft remotes --json`; the intended custom hostname must appear.
2. Import one representative HTML-derived document into a dedicated sanity-check folder.
3. Verify durable job status and read the artifact back.
4. Inspect rendered output through the actual custom hostname.
5. Only then import the complete document bundle.

A local importer pass proves bundle compatibility but not remote destination rendering.

## Deployment scripting pitfall

Avoid relying on a shell `ERR` trap whose rollback function returns success. In Bash, a successful trap can allow later statements to continue after an early failure, producing a misleading successful SSM command. Prefer an explicit shape:

```bash
if ! deploy; then
  rollback
  exit 1
fi
verify
```

The rollback must restore the previous binary and configuration, restart the service, and still exit non-zero for the failed deployment attempt.
