# Hermes gateway logout triage

Use this when someone says a Hermes gateway dies when their SSH session ends.

## Fast interpretation

`Linger=yes` is necessary for user services to survive logout, but it is **not** proof that every later restart/exit is caused by logout.

If all three are true:
- `loginctl show-user <user>` reports `Linger=yes`
- the gateway is installed as a `systemd --user` unit
- the unit is enabled/active

then treat "SSH logout killed it" as an unproven hypothesis and inspect logs next.

## Minimal check sequence

1. `getent passwd <user>` — confirm the actual Linux account/home
2. `loginctl show-user <user> -p Linger -p RuntimePath -p State -p Sessions`
3. `sudo -u <user> env XDG_RUNTIME_DIR=/run/user/<uid> systemctl --user status <unit>`
4. `sudo -u <user> env XDG_RUNTIME_DIR=/run/user/<uid> systemctl --user cat <unit>`
5. `sudo -u <user> env XDG_RUNTIME_DIR=/run/user/<uid> journalctl --user -u <unit> -n 100 --no-pager`

Profile note:
- `hermes-gateway-<profile>.service` still belongs to the Linux user running it; it is not evidence that a different human user's account owns the process.

## What to look for in logs

Common real causes that mimic logout breakage:
- Telegram polling/network timeouts and reconnect loops
- provider/model credit exhaustion or auth failures
- a clean SIGTERM from systemd because the service was manually restarted
- the gateway process exiting with status 1 and being restarted by systemd

## Communication rule

When reporting back:
- separate **linger state** from **gateway health**
- say explicitly whether linger is already on
- if linger is on, name the more likely cause from the logs instead of repeating generic linger advice
