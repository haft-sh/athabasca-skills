---
name: athabasca-runtime-services
description: Manage, verify, and document the live Athabasca and Hermes runtime services on the dev host, especially user-level systemd services, Tailscale-reachable dashboard access, and README/runtime handoff updates.
triggers:
  - User asks to make Athabasca or Hermes services persistent on the dev host
  - User asks how Athabasca is currently running in production/dev on the Ubuntu box
  - User asks to document actual runtime/service details in the repo
  - Need to confirm whether Hermes dashboard or Athabasca app is reachable over localhost or Tailscale
---

# Athabasca runtime services

Use this when the task is about the **actual live services** on the Athabasca Ubuntu box: user-level systemd units, Hermes dashboard reachability, Athabasca Bun runtime state, or documenting those facts for collaborators.

## Core rule: verify live state before documenting

Do not trust README text, remembered ports, or prior setup notes.

Always inspect the running system first:
1. resolve the **target Linux user/account** the question is about
2. `systemctl --user status <service>`
3. `systemctl --user cat <service>`
4. socket listeners (`ss -ltnp`)
5. a real HTTP probe (`curl`)
6. only then update README/docs

If the user says "see `bun run restart` to confirm its own service," use that live command path rather than inferring the service name from docs.

## Target-user rule for user-level services

When the task mentions another person or account (for example `jt`, `deploy`, or a collaborator), do **not** start by checking the current operator's user just because that is the default shell account.

Resolve the target account first:
- confirm the passwd entry and home directory for the named user
- check `loginctl show-user <user> -p Linger -p RuntimePath -p State -p Sessions`
- inspect that user's units with `sudo -u <user> env XDG_RUNTIME_DIR=/run/user/<uid> systemctl --user ...`
- if you mention profile-specific services, make clear that `hermes-gateway-<profile>.service` is still under the same Linux user and is **not** evidence that some other human user is running the service

This matters because Hermes profiles (for example `cliphouse`) can create additional user services under one Linux account, while a collaborator may have a completely separate account and home directory.

## Current service model on the dev host

Typical live surfaces to verify:
- `athabasca-dev.service` — Bun dev server for the app
- `hermes-dashboard.service` — Hermes dashboard for remote desktop access

Do not assume both already exist. Verify.

## Hermes dashboard: remote-access rule

For Hermes Desktop Remote Gateway / remote dashboard usage, the user needs the **dashboard URL**, not the messaging gateway URL.

Operational implications:
- `hermes dashboard` default bind is localhost-only (`127.0.0.1:9119`)
- if the user wants access from another device over Tailscale/LAN, the dashboard must bind non-locally
- the usual command is:

```bash
hermes dashboard --host 0.0.0.0 --port 9119 --insecure --no-open
```

Verification pattern:
1. confirm service/listener exists
2. if browser access fails but localhost works, inspect bind address with `ss -ltnp | grep 9119`
3. if listener is `127.0.0.1:9119`, the fix is to restart with non-local bind
4. verify both `curl http://127.0.0.1:9119/` and `curl http://<tailscale-ip>:9119/`

## Common pitfall: manual process blocks systemd adoption

If you create `hermes-dashboard.service` while a manually started `hermes dashboard` is already running on the same port, the systemd unit will flap with `address already in use`.

Correct sequence:
1. create the user unit
2. `systemctl --user daemon-reload`
3. `systemctl --user enable --now hermes-dashboard.service`
4. if it fails to bind, inspect logs
5. stop the pre-existing manual dashboard process (for Hermes, `hermes dashboard --stop` is the clean path)
6. restart the systemd unit
7. verify the listener belongs to the service-managed PID

Do not report success just because the port is reachable; verify the **service** is healthy, not only the old manual process.

## Recommended user service shape for Hermes dashboard

Use a user-level systemd service under `~/.config/systemd/user/`.

Canonical unit shape:

```ini
[Unit]
Description=Hermes Dashboard
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/home/<user>
Environment=HOME=/home/<user>
ExecStart=/home/<user>/.local/bin/hermes dashboard --host 0.0.0.0 --port 9119 --insecure --no-open
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

Notes:
- `--insecure` is required for non-localhost binding
- user-level services work especially well when `loginctl show-user <user> -p Linger` reports `Linger=yes`
- if linger is enabled, phrase it accurately: the service survives logout and is not merely "restart on login"

## Repo-local Hermes plugin activation

When the task is to enable a custom Hermes plugin that lives in the repo (for example an Athabasca auth/plugin integration), prefer the **user-plugin symlink + CLI enablement** path over project-local plugin loading or hand-editing config first.

Recommended sequence:
1. identify the repo-local plugin directory (for example `.hermes/plugins/<plugin-name>`)
2. create a symlink into the active Hermes user plugin directory: `~/.hermes/plugins/<plugin-name>`
3. enable it with `hermes plugins enable <plugin-name>`
4. restart Hermes with `hermes gateway restart`
5. verify the plugin is now discoverable/enabled (`hermes plugins list`) before claiming success

Why this path:
- the repo-local directory stays the source of truth
- Hermes discovers it through the normal user-plugin path across entry points
- `hermes plugins enable <name>` is safer than manually editing `plugins.enabled` when the plugin may still be undiscoverable

Important pitfall:
- if the symlink/user-plugin write into `~/.hermes/plugins/` is blocked, denied, or not yet approved, **do not** only edit `plugins.enabled` and leave Hermes pointing at a non-existent plugin install. Stop and surface the blocker, or ask the operator to create the symlink first.
- verify the plugin key from the directory/manifest and enable that exact key.

## Athabasca app service verification

For the app service, prefer the repo's real operator path:

```bash
bun run restart
```

Then verify:
- active unit name
- actual `ExecStart`
- working directory
- env file if present
- listen socket (commonly `*:3000`)
- a real HTTP probe to the app root or health endpoint

When documenting runtime state, distinguish clearly between:
- example unit files checked into the repo
- the actual installed unit under `~/.config/systemd/user/`

## README / docs update rule

When the user asks to document runtime details, write the **actual observed values**, not placeholders:
- exact service names
- exact unit file path if useful
- exact startup commands
- exact listen addresses/ports
- exact remote URL over Tailscale
- exact restart/status/log commands operators should use

Include a note that Hermes dashboard session tokens are ephemeral across restarts.

## Hermes gateway dies when SSH ends: triage rule

If someone reports "my Hermes gateway ends when my SSH session ends," do **not** jump straight to "enable linger" and stop there.

Work the checks in this order:
1. confirm the **exact Linux user** they mean
2. `loginctl show-user <user> -p Linger -p RuntimePath -p State -p Sessions`
3. inspect whether the gateway is actually installed as a **user service** for that user (`systemctl --user status/cat hermes-gateway.service` or profile variant such as `hermes-gateway-cliphouse.service`)
4. if `Linger=yes` **and** the user unit is enabled/running, treat logout as a **less likely** root cause
5. check `journalctl --user -u <unit>` for the real stop/restart reason before recommending config changes

Important interpretation rule:
- if linger is on and the gateway is managed by `systemd --user`, a later stop/restart may be caused by network failures, provider/auth failures, explicit restarts, or the gateway process exiting on its own
- do not misattribute those to "SSH logout killed it" without log evidence

Useful things to look for in the logs:
- repeated Telegram reconnect / timeout errors
- model/provider credit or auth failures
- `Main process exited` followed by systemd restart
- explicit `Stopping ...` events that indicate a manual/service-triggered restart rather than session teardown

### Restarting a gateway from inside the running gateway

If you are operating from a Hermes session that is itself running through the target gateway/profile, `hermes gateway restart` may refuse with a restart-loop protection error.

In that case, do not report "restart failed" and stop. Use the user service manager directly:

```bash
systemctl --user restart hermes-gateway.service
# or profile-scoped unit, e.g.
systemctl --user restart hermes-gateway-cliphouse.service
```

Then verify with:
- `systemctl --user is-active <unit>`
- `systemctl --user show <unit> -p ActiveEnterTimestamp`

This is the reliable path when a profile env/config change must be applied from inside an active gateway-backed session.

Reference:
- `references/hermes-gateway-logout-triage.md`

## Verification checklist

Before closing the task, confirm all of the following:
- user unit exists on disk
- `systemctl --user daemon-reload` completed
- service is enabled
- service is active after startup
- socket listener matches the intended bind address/port
- HTTP probe succeeds on both localhost and the remote/Tailscale address where relevant
- README/docs were updated with live values, not assumptions
- any manually launched conflicting process was stopped if present

## Pitfalls

- Do not confuse Hermes dashboard with Hermes messaging gateway.
- Do not tell the user to use the gateway URL for Hermes Desktop remote access.
- Do not document a systemd service before checking whether the live machine already has a different unit definition.
- Do not leave a manual `hermes dashboard` process occupying the port after creating the service.
- Do not claim success from a reachable port alone; verify the systemd unit owns the listener.
- Do not describe linger-enabled user services as merely "starts on login".

## References

- `references/dev-host-runtime-services.md` — current observed service names, listeners, and operator commands on the Athabasca dev box
