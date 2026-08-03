# Runtime persistence checklist

Use this when Athabasca helper tools should persist across Hermes gateway restarts for a profile.

## Canonical checks

```bash
# Plugin symlink resolves to repo-local source
readlink -f ~/.hermes/plugins/athabasca-api

# Profile config contains persistent enablement
HOME=/home/nrsimha hermes --profile cliphouse config path
HOME=/home/nrsimha hermes --profile cliphouse plugins list --plain --no-bundled

# Profile env contains Athabasca values
HOME=/home/nrsimha hermes --profile cliphouse config env-path

# Gateway unit is loading the env file
systemctl --user show hermes-gateway-cliphouse.service \
  --property=EnvironmentFiles,Environment --no-pager
```

## Persistent systemd drop-in pattern

```ini
# ~/.config/systemd/user/hermes-gateway-cliphouse.service.d/env.conf
[Service]
EnvironmentFile=/home/nrsimha/.hermes/profiles/cliphouse/.env
```

## Proof that the wiring is fixed

Use the helper tools themselves, not just config inspection:
- `athabasca_request(GET /api/health)`
- `athabasca_request(GET /api/projects)`
- `athabasca_request(GET /api/generation/video-capabilities)`

## Failure interpretation

- `Missing ATHABASCA_BASE_URL` / `Missing ATHABASCA_API_TOKEN` = plugin loaded, runtime env missing
- HTTP 401/403/404 from Athabasca = helper tool wiring is working; investigate auth/scope/route next
