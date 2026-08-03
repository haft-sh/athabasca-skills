# Athabasca dev host runtime services

Observed durable runtime pattern from the Ubuntu dev box:

## Hermes dashboard

- user service: `hermes-dashboard.service`
- unit path: `~/.config/systemd/user/hermes-dashboard.service`
- startup command:

```bash
/home/nrsimha/.local/bin/hermes dashboard --host 0.0.0.0 --port 9119 --insecure --no-open
```

- listener after successful service takeover: `0.0.0.0:9119`
- Tailscale remote URL: `http://100.84.189.23:9119`

### Important takeover pitfall

If a manual `hermes dashboard` process is already running on port 9119, the new systemd unit can fail with:

```text
ERROR: [Errno 98] error while attempting to bind on address ('0.0.0.0', 9119): address already in use
```

Reliable recovery:

```bash
hermes dashboard --stop
systemctl --user restart hermes-dashboard.service
systemctl --user status hermes-dashboard.service
ss -ltnp | grep ':9119'
```

## Athabasca app

- user service: `athabasca-dev.service`
- working directory: `/home/nrsimha/Sites/athabasca`
- env file: `/home/nrsimha/.config/athabasca/athabasca-dev.env`
- preflight:

```bash
/home/nrsimha/.bun/bin/bun run scripts/check-local-db.ts
```

- startup command:

```bash
/home/nrsimha/.bun/bin/bun --hot src/index.ts
```

- listener observed: `*:3000`
- package shortcut for restart:

```bash
cd /home/nrsimha/Sites/athabasca && bun run restart
```

## Documentation pattern

When asked to update repo docs, capture the live operator surface directly:
- service names
- actual `ExecStart`
- exact remote URL
- restart/status/log commands
- note that Hermes dashboard session token changes on restart
