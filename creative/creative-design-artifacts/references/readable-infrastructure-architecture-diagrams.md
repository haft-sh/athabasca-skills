# Readable infrastructure architecture diagrams

Use this pattern when a README or ops doc needs a big-picture architecture/deployment diagram and Mermaid becomes too dense to read.

## When to switch away from Mermaid

Switch to a polished HTML/SVG architecture artifact when:

- the diagram has more than ~3 deployment zones or host groups
- it mixes repo structure, DNS, services, deploy flows, and runtime traffic
- Mermaid edge routing creates crossing lines or visually crowded labels
- the user says the Mermaid diagram is hard to read
- the diagram is intended as README source material but needs a clearer rendered companion

Keep Mermaid only for small flowcharts or when GitHub inline rendering matters more than legibility.

## Recommended deliverables

1. **README**: concise architecture summary + environment/deployment table + link to the richer diagram.
2. **HTML/SVG artifact** under `docs/YYYY-MM-DD-<topic>-architecture-overview.html`: polished, self-contained, inspectable.
3. Optional small source note/doc with verified host facts if the diagram was built from live infrastructure.

## Visual structure

For infrastructure diagrams, layout clarity beats decoration:

- group by zones: repository, DevSpace/CI/orchestration, Haft Local production, Haft HQ production, public DNS/hostnames
- separate code ownership from runtime hosts
- label each host with instance name, instance id, and public IP when relevant
- label services with systemd unit + localhost port
- use color families consistently:
  - cyan = public traffic / DNS / reverse proxy path
  - amber = deploy/CI flow
  - purple dashed = future or optional managed-service calls
  - green = local/installable product layer
  - purple = hosted/control-plane layer
- keep arrows few and meaningful; avoid line spaghetti
- add 2–3 short footer notes explaining the conceptual split

## README integration rule

Do not embed a large hard-to-read Mermaid diagram directly in README just because GitHub can render it. Prefer a small table and link to the polished artifact when the diagram is operationally complex.

Suggested README wording:

```md
For the full deployment map, see [`docs/YYYY-MM-DD-...-architecture-overview.html`](docs/YYYY-MM-DD-...-architecture-overview.html).

At a high level:

| Layer | Hostname | Service |
|---|---|---|
| Haft Local dev | `dev.example.com` | `haft-dev.service` |
| Haft Local prod | `prod.example.com` | `haft.service` |
| Haft HQ | `example.com` | `haft-hq.service` |
```

## Publishing/viewing through Haft

If the user asks to "move the diagram to Haft" or make it visible inside a Haft instance, treat the HTML/SVG file as a standalone renderable artifact:

1. Prefer the user's active/local vault when available (commonly `~/.haft/vaults/default/content/`) instead of pushing to a public/prod vault. Use prod only when the user explicitly asks for a public/prod-hosted artifact or the local vault is inaccessible.
2. Put the exact `.html` file under the active vault's `content/` directory when byte-for-byte preservation matters.
3. If the artifact should render inside Haft's rendered view, make it a valid Haft HTML profile before indexing: include `hv:profile=haft-html-profile-v0`, stable `hv:page-id`/`hv:slug`, `hv:script-policy=none`, at least one `data-hv-block-id`, and `<section id="..." data-hv-section="...">` wrappers. Otherwise the shell may show "Rendered view unavailable" even though the file indexed.
4. Rebuild the vault index (`bun run index:rebuild -- <vault-root>` from the app checkout or equivalent).
5. Capture the indexed `pageId`, slug, title, profile metadata, and hash from the manifest/catalog.
6. Prefer the Haft shell URL with rendered view for the user-facing link, for example `https://<haft-host>/#/<slug>?view=rendered`.
7. In production/public EC2 mode, direct `/api/vault/content/*` and `/preview/artifact/*` routes may be `private-read`/route-gated for unauthenticated callers. Do not present those direct routes as the public viewing link unless you have verified they render for the intended user.

## Verification

Before handing off:

- parse the HTML with Python `html.parser` or equivalent
- assert key labels/hostnames are present in the artifact text
- if facts came from live infra, list which values were verified (DNS, EC2 tags, systemd unit, Caddy route, health endpoint)
- when moved into Haft, verify both index/catalog presence and the actual user-facing viewing surface; a successful index rebuild alone is not enough
