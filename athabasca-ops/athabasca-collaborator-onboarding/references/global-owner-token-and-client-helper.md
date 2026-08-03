# Global owner token + Hermes-side Athabasca client helper

Session-derived operational notes:

## Global owner token pattern

Athabasca now supports a true owner/superadmin token shape:

- `projectScopes: []`
- `operationModes` includes `"owner"`
- token is created by an authenticated owner for their own user
- `expiresInDays: null` can be used for a non-expiring token

Expected behavior:
- bearer auth with this token can list all projects
- project access resolves as owner across current and future projects
- this is appropriate for owner-level Hermes automation, not for normal collaborators

## Hermes-side storage

Keep the token in the active Hermes profile env file, not in the repo:

- `~/.hermes/.env`
- variables:
  - `ATHABASCA_BASE_URL`
  - `ATHABASCA_API_TOKEN`
  - optional `ATHABASCA_PROJECT_SLUG`

Restart the Hermes gateway after adding or changing these env vars.

## Default Hermes plugin path

When no existing bridge module already owns Athabasca HTTP requests, use:

- `.hermes/plugins/athabasca-api`

This plugin should:
- inject `Authorization: Bearer <token>` on every request
- support generic authenticated API calls through `athabasca_request`
- support project-scoped calls through `athabasca_project_request`
- block raw terminal HTTP calls to Athabasca when available

Legacy compatibility helper:

- `~/.hermes/scripts/athabasca_client.py`

## Legacy convenience commands

Useful command surface:

- `list-projects`
- `get-project <slug>`
- `project-path <slug|-> [suffix]`
- `project-get <slug|-> [suffix]`
- `project-post <slug|-> [suffix] <JSON_BODY>`

`-` means: fall back to `ATHABASCA_PROJECT_SLUG` from env.

## Verification pattern

After enabling the plugin:
1. source `~/.hermes/.env`
2. call `athabasca_request` for `GET /api/projects`
3. confirm `status: 200`
4. call `athabasca_project_request` with a known slug to prove project-path auth works too

If the plugin is unavailable during migration, run `python3 ~/.hermes/scripts/athabasca_client.py list-projects` as the fallback check.
