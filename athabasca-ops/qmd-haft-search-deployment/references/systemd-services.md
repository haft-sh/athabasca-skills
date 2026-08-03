# Systemd Service Templates

## QMD→Haft Bridge Service

`/etc/systemd/system/qmd-haft-bridge.service`:

```ini
[Unit]
Description=QMD→Haft Bridge Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/haft-bbt/bridge
Environment=PATH=/usr/bin:/usr/local/bin:/home/ubuntu/.bun/bin
Environment=HOME=/home/ubuntu
Environment=BRIDGE_PORT=7799
Environment=VAULT_ROOT=/opt/haft-bbt/vault/haft-bbt
Environment=QMD_COLLECTION=obsidian-vault
Environment=QMD_BIN=/usr/bin/qmd
ExecStart=/home/ubuntu/.bun/bin/bun run /opt/haft-bbt/bridge/qmd-haft-bridge.ts
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## Haft Server Service

`/etc/systemd/system/haft-bbt-server.service`:

```ini
[Unit]
Description=Haft BBT Server
After=network.target qmd-haft-bridge.service
Wants=qmd-haft-bridge.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/haft-bbt/haft
Environment=PATH=/usr/bin:/usr/local/bin:/home/ubuntu/.bun/bin
Environment=HOME=/home/ubuntu
Environment=PORT=9001
Environment=VAULT_ROOT=/opt/haft-bbt/vault/haft-bbt
Environment=HAFT_QMD_SEARCH=true
Environment=HAFT_QMD_ENDPOINT=http://127.0.0.1:7799/search
Environment=NODE_ENV=production
ExecStart=/home/ubuntu/.bun/bin/bun run /opt/haft-bbt/haft/src/index.ts
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**Critical**: Use `bun run /opt/haft-bbt/haft/src/index.ts` (repo root entry point), NOT `apps/server/src/index.ts`. The root entry point serves both the SPA frontend and the API.

## Caddy Service

Caddy is installed via apt and managed by systemd automatically. Config at `/etc/caddy/Caddyfile`:

```
bbt.haft.sh {
    reverse_proxy localhost:9001
}
```

## Deployment Commands

```bash
# Copy service files
sudo cp /tmp/qmd-haft-bridge.service /etc/systemd/system/
sudo cp /tmp/haft-bbt-server.service /etc/systemd/system/
sudo systemctl daemon-reload

# Enable and start
sudo systemctl enable qmd-haft-bridge.service haft-bbt-server.service
sudo systemctl start qmd-haft-bridge.service
sudo systemctl start haft-bbt-server.service

# Check status
sudo systemctl status qmd-haft-bridge.service --no-pager
sudo systemctl status haft-bbt-server.service --no-pager

# View logs
journalctl -u qmd-haft-bridge -f
journalctl -u haft-bbt-server -f
```

## Transient Units for Long-Running Jobs

For one-off jobs like QMD indexing/embedding that must survive SSH disconnect:

```bash
sudo systemd-run --unit=qmd-index-bbt --uid=ubuntu --gid=ubuntu \
  --setenv=PATH="/usr/bin:/usr/local/bin:/home/ubuntu/.bun/bin" \
  --setenv=HOME="/home/ubuntu" \
  /usr/bin/qmd update

# Check status
systemctl status qmd-index-bbt --no-pager
journalctl -u qmd-index-bbt -f
```
