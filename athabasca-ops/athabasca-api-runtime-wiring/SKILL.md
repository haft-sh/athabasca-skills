---
name: athabasca-api-runtime-wiring
description: Make Athabasca helper tools persist across Hermes sessions by wiring the repo-local plugin, profile config, and gateway runtime env correctly.
version: 1.0.0
---

# Athabasca API runtime wiring

Use this when Athabasca helper tools like `athabasca_request` or `athabasca_project_request` are missing, partially working, or not persistent across Hermes gateway / profile restarts.

## Trigger

- The user says to use `athabasca_request` / `athabasca_project_request`
- A session should have Athabasca API helpers, but they are absent
- The helper tools are callable but return `Missing ATHABASCA_BASE_URL` or `Missing ATHABASCA_API_TOKEN`
- The goal is to make Athabasca plugin access persist for every future session in a profile

## Core distinction: three separate layers

Do not collapse these into one diagnosis.

1. **Plugin code discoverability** — Hermes must be able to find the Athabasca plugin.
2. **Plugin enablement** — the active profile must enable the plugin in config.
3. **Runtime env wiring** — the actual Hermes gateway/CLI process must load `ATHABASCA_BASE_URL` and `ATHABASCA_API_TOKEN`.

A failure at layer 3 can look like “the plugin is broken” even when the tool is loaded correctly.

## Persistent setup for a profile

### 1) Keep the repo-local plugin as source of truth

Preferred layout:

```bash
mkdir -p ~/.hermes/plugins
ln -sfn /home/nrsimha/Sites/athabasca/.hermes/plugins/athabasca-api ~/.hermes/plugins/athabasca-api
```

Use the repo-local plugin directory as the canonical source so plugin code stays versioned with the Athabasca repo.

### 2) Persist enablement in the profile config

The profile must keep the plugin in `config.yaml`:

```yaml
plugins:
  enabled:
    - athabasca-api
```

Do not rely only on one-time interactive state. Verify the profile config actually contains the plugin so future sessions inherit it.

### 3) Persist env loading in the gateway runtime

For profile-scoped Hermes gateway services, make sure the systemd unit loads the profile `.env` file. A working persistent pattern is a user-unit drop-in like:

```ini
# ~/.config/systemd/user/hermes-gateway-<profile>.service.d/env.conf
[Service]
EnvironmentFile=/home/<user>/.hermes/profiles/<profile>/.env
```

This is the missing layer when:
- the plugin is enabled
- the tools exist
- but calls fail with `Missing ATHABASCA_BASE_URL` or `Missing ATHABASCA_API_TOKEN`

## Verification sequence

1. Confirm the plugin symlink resolves to the repo-local plugin.
2. Confirm `plugins.enabled` contains `athabasca-api` in the target profile config.
3. Confirm the profile `.env` contains:
   - `ATHABASCA_BASE_URL`
   - `ATHABASCA_API_TOKEN`
4. Confirm the running gateway service sees the env file:

```bash
systemctl --user show hermes-gateway-<profile>.service \
  --property=EnvironmentFiles,Environment --no-pager
```

5. Verify the helper tool with a cheap authenticated call such as:
   - `GET /api/health`
   - `GET /api/projects`
   - `GET /api/generation/video-capabilities`

## Diagnosis rule: loaded tool vs missing env

Interpret failures accurately:

- If the tool is absent from the session/tool registry, this is a **plugin discovery/enablement** problem.
- If the tool is callable but returns `Missing ATHABASCA_BASE_URL` or `Missing ATHABASCA_API_TOKEN`, this is a **runtime env wiring** problem.
- If the tool reaches Athabasca and returns HTTP auth/project errors, the plugin wiring is already working; move on to API auth or project-scope diagnosis.

## Gateway restart pitfall

`hermes gateway restart` may be blocked from inside the running gateway process to prevent restart loops.

When fixing gateway runtime wiring:
- prefer a shell outside the active gateway session
- or update the systemd unit/drop-in and restart from an external shell
- do not assume an in-chat restart attempt is a valid proof of failure

## Media-upload note

For Athabasca binary media uploads, remember that `athabasca_request` / `athabasca_project_request` are JSON-oriented API helpers. Use them for lookups and verification, but use a real multipart client for `POST /api/projects/:slug/media` file uploads.

## References

- `references/runtime-persistence-checklist.md` — concrete commands and the systemd `EnvironmentFile` drop-in pattern for persistent Athabasca helper-tool wiring

## Pitfalls

- Do not claim the plugin is missing when the real error is missing base URL/token env.
- Do not stop after enabling the plugin in config if the systemd gateway service does not source the profile `.env`.
- Do not assume a gateway restart from inside the gateway process will succeed.
- Do not use raw terminal HTTP calls to the Athabasca host once the plugin is wired; use the helper tools for authenticated JSON routes.
