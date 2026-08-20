# DevSpace MCP service specifics

## Instance identity

- AWS instance name: `devspace-mcp-ca-west-1` (ID `i-0dbfea303646ccde2`)
- Private IP: `172.31.252.234`, Public (Elastic) IP: `40.176.172.153`
- Hostname: `ip-172-31-252-234` (EC2 internal)
- Tailscale hostname: `devspace-haft`
- Public endpoint: `https://mcp.haft.sh/mcp` (DNS → 40.176.172.153)
- Caddy reverse proxy on port 443 → upstream `127.0.0.1:7676`

## The Orchestrator is NOT DevSpace

The Orchestrator profile runs on a *different* EC2 instance (`ip-172-31-39-230` / `172.31.39.230`), not the DevSpace host. You cannot check or restart DevSpace services from the Orchestrator shell. Always verify which host you're on (`hostname`) before attempting service operations.

## systemd unit details

- Unit file: `/etc/systemd/system/devspace.service` (system-level, not user-level)
- Override: `/etc/systemd/system/devspace.service.d/override.conf`
- Service runs as `User=ubuntu`, `Group=ubuntu`
- **Requires sudo** to edit unit files or restart via systemctl

### Base ExecStart

The base unit points to the npm-installed global binary:
```
ExecStart=/usr/bin/node /usr/lib/node_modules/@waishnav/devspace/dist/cli.js serve
```

### Override conf (2026-08-20)

```ini
[Service]
WorkingDirectory=/home/ubuntu/Sites/devspace
```

The override was updated on 2026-08-20 to fix a crash-loop. The previous override pointed to a stale path (`/home/ubuntu/Sites/devspace-runtime-fork-main/dist/cli.js`) — that directory no longer exists.

### Pitfall: stale override path causes crash-loop

When the override.conf sets `ExecStart` to a path that doesn't exist, systemd keeps restarting the service. The exit code is `200/CHDIR` (cannot change to working directory) or `ENOENT` depending on which path is missing. Check `systemctl status devspace.service` — if it shows `activating (auto-restart)`, the override path is almost certainly wrong.

Fix:
```bash
sudo tee /etc/systemd/system/devspace.service.d/override.conf << 'EOF'
[Service]
WorkingDirectory=/home/ubuntu/Sites/devspace
EOF
sudo systemctl daemon-reload && sudo systemctl restart devspace.service
```

### Pitfall: node-pty / native deps

The devspace package depends on `node-pty` and `better-sqlite3` (native C++ addons). After a fresh `npm install`, run `npm run build` to compile them. If the service starts but MCP tools fail with native-module errors, rebuild:
```bash
cd /home/ubuntu/Sites/devspace && npm run build
sudo systemctl restart devspace.service
```

## Diagnostic path for 502 from mcp.haft.sh

1. `curl -s -o /dev/null -w "HTTP %{http_code}" https://mcp.haft.sh/mcp`
2. HTTP 502 = Caddy is up but upstream (devspace.service) is down
3. SSH to DevSpace host, check `systemctl status devspace.service`
4. If crash-looping, check override.conf paths
5. If service active but MCP returns 401, the service is healthy (just needs auth)

## Caddy configuration

Caddy serves `mcp.haft.sh` on port 443 and proxies to `127.0.0.1:7676`. Caddy itself runs as a system service (`caddy.service`), confirmed active.

## Relevant architecture docs

- `/home/ubuntu/Sites/haft/docs/2026-07-04-haft-deployment-architecture-diagram.md` — full architecture diagram
- `/home/ubuntu/Sites/haft/docs/security/2026-07-13-ec2-encryption-network-switchover-handoff.md` — Elastic IP stabilization
