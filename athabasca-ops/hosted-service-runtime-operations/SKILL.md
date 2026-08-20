---
name: hosted-service-runtime-operations
description: Operate and verify public Linux-hosted application services behind TLS reverse proxies, including DNS cutovers, service environment configuration, browser-origin correctness, and durable endpoint handoff.
version: 1.0.0
---

# Hosted service runtime operations

## When to use

Use for a publicly hosted app on a Linux VM/EC2 instance when work involves:
- DNS cutovers or a changed origin IP
- systemd service health and deployment configuration
- Caddy/nginx-style TLS reverse proxies
- browser-session, CSRF, or same-origin failures visible only through the public hostname
- preparing a durable public endpoint such as an Elastic IP

## Operating model

Separate four facts before changing anything:
1. **Origin health** — the intended instance, service units, listener, and loopback health endpoint are healthy.
2. **DNS correctness** — the public hostname resolves to that intended origin.
3. **Proxy correctness** — TLS/proxy behavior reaches the local app without altering the security boundary.
4. **Browser contract** — a fresh browser receives the expected UI/session state from the public origin.

Do not call a deployment healthy from loopback output alone. Verify the public hostname and a real browser surface as appropriate.

## Reconciliation and handoff before maintenance

When a resize, migration, Elastic-IP request, or old DNS address creates uncertainty, do not start destructive cleanup from a single IP match. Build a compact evidence chain first:

1. Resolve the current hostname and probe public HTTPS.
2. Inventory instances, EIPs, volumes, load balancers, and snapshots using the owning account/region plus stable tags and names—not just the current DNS IP.
3. Probe the candidate host directly and, where safe, force the hostname to its candidate IP to compare TLS/Host-routed health and build identity.
4. Inspect active service units, configured production versus staging/source paths, and indexed/runtime counts on the host.
5. Use prior-session history as a lead only; verify all claimed addresses, resizes, and attachments live.
6. Before deleting data or cost-bearing resources, persist an operator handoff with the canonical hostname, instance identity, access command, active/staging paths, current services, rollback artifacts, and explicit non-actions.

Use hostnames, rather than literal public IPs, in durable monitor and access instructions. Distinguish a verified active host from an older address that was simply part of migration history.

## DNS cutover workflow

1. Resolve the public hostname using the system resolver and independent resolvers when available.
2. Inspect the candidate host's live public IP, listeners, service state, certificate, and an HTTPS probe forced to that IP.
3. Update the authoritative DNS record through the correct zone/account.
4. Verify API/control-plane record content, fresh resolver answers, public HTTPS, and direct-origin HTTPS.
5. Update monitors to use the hostname, not a literal public IP. The hostname is the durable monitoring contract; an Elastic IP is still preferable for stable ingress across instance replacement.

## Locate the actual host before provisioning access

A public hostname/IP is not reliable proof of the currently managed EC2 instance: DNS can point to an old origin, reverse proxy, load balancer, or replacement host.

1. Resolve and probe the hostname, but treat that only as **public-ingress evidence**.
2. In the expected AWS account and region, search EC2 by stable metadata first: `Name` tag/project/service-name patterns. Record instance ID, region, state, private/public IPs, and attached instance profile.
3. Compare the discovered instance endpoint with the hostname. If they differ, report an **origin-mapping mismatch**; do not conclude the server is absent merely because the hostname IP does not appear in an EC2 IP lookup.
4. Only after an instance ID is identified, inspect SSM registration and choose SSM or SSH access.
5. Keep public host, DNS/proxy mapping, compute identity, and operator-access path as separate evidence layers.

## Public browser-origin failures behind a reverse proxy

### Symptom

A browser request to a public HTTPS hostname returns an origin/session-bootstrap denial while a loopback backend is healthy.

### Safe diagnostic sequence

1. Reproduce the public request with browser-like metadata:
   - `Origin: https://<public-host>`
   - `Referer: https://<public-host>/`
   - `Sec-Fetch-Site: same-origin`
2. Inspect the proxy's rendered runtime configuration and confirm the public host routes to the intended local upstream.
3. Inspect the app's effective process environment. `systemctl show` may omit values loaded from `EnvironmentFile`; check the running process environment carefully without printing unrelated secrets.
4. Inspect application source/config documentation for a canonical configured public-origin setting.
5. Configure only that canonical origin, restart only the affected app service, and re-run the public probe.

### Correct success shape

For an unauthenticated browser, a successful repair often changes the response from **403 origin denied** to **401 session required**. That proves same-origin validation passed while authentication still remains enforced.

Always verify the negative path too: a request with an unrelated `Origin` must remain rejected. Do not treat a new 200 response from an unauthenticated synthetic request as mandatory or desirable.

### Security rule

Do not weaken the boundary by broadly trusting `Forwarded` or `X-Forwarded-*` headers. Configure an explicit canonical public origin in the app's service environment unless a separately authenticated proxy-trust design is already established and verified.

## Elastic IP workflow

1. Resolve the target instance ID, region, current public IP, and availability zone from EC2.
2. List existing Elastic IPs and confirm none can be safely reused.
3. Check the regional `EC2-VPC Elastic IPs` service quota before allocating.
4. If capacity exists, allocate a VPC EIP, tag it with name/project/role/purpose, associate it to the exact target instance, then update DNS and verify public traffic.
5. If the allocation is quota-blocked, request the smallest increase, report the pending request, and do not repurpose an EIP attached to another workload.
6. Once associated, verify the EIP association, DNS answer, public HTTPS, and hostname-based monitoring.

## Large-vault indexing and browser-projection verification

A successful reader/index rebuild is **not** proof that users can browse newly imported content. Large vaults can maintain separate reader/catalog and Explorer/browser projections; a stale Explorer projection can retain old folder counts or omit a newly imported collection.

After bulk imports, deduplication, or filesystem-level staged copies:

1. Rebuild with the **same runtime generation** serving the public app. A scratch checkout's CLI may not refresh every deployed read model.
2. Let a rebuild finish before restarting. If an SSH client disconnects, inspect the remote process/operation lease before launching another rebuild.
3. Verify three independent layers before saying changes are live:
   - reader manifest/catalog: expected page totals and source paths;
   - bounded Explorer listing: expected top-level collection and direct-child count;
   - fresh public browser: the collection is visibly present in the sidebar.
4. If a full-tree call stalls on a large vault, use its bounded children/listing endpoint for verification. Repair or upgrade the browser projection rather than treating a stale client tree as proof that the import failed.
5. Before changing runtime versions, preflight vault-layout compatibility and retain a rollback target. Confirm the updated process mounts the intended vault before using its UI as evidence.

Never report a bulk import as live from on-disk files or a reader-index count alone.

## Disabled-by-default capability releases

Use this pattern when a release must carry an optional private-provider capability while the public feature must remain off until a later approved activation.

1. Read the ticket's hard boundary before acting. A title saying “deploy” does not override explicit prohibitions on merge, deployment, activation, canaries, or rollback exercises.
2. Verify the **deployed** build and public route separately from the integration branch. Source history proves candidate capability; a live health fingerprint and route probe prove what users actually receive.
3. Validate that the release's default configuration disables the optional provider. Check semantic/hybrid requests for a truthful keyword fallback (`effectiveMode=keyword`, `degraded=true`, `semantic.state=disabled`) rather than treating a 200 response as activation success.
4. Keep provider endpoint, collection, vault path, credentials, request headers, and raw provider output out of public diagnostics and shared handoff evidence. Record only a pinned source revision, artifact checksum, build fingerprint, and bounded execution state.
5. Publish a reviewable operator handoff specifying: pinned dependencies, disabled default, health/keyword/disabled-state checks, rollback condition, and the independent gates that still keep activation ineligible.
6. Do not start costly private compute or run activation-only benchmarks unless the card specifically requires provider execution. Release-preparation verification is often satisfied by source, build, and disabled-state checks.

**Pitfall:** “Release-ready” and “activation-eligible” are distinct outcomes. Record them separately so a completed deployment-preparation task cannot unblock rollout automation by itself.

### Atomic compiled-binary deployment and proof

When a hosted service runs a compiled Bun artifact selected through a `current` symlink, use an artifact-first, rollback-capable deployment rather than rebuilding in place:

1. Verify the candidate source commit is the intended merged integration branch and compile from that exact checkout. Capture binary SHA-256 and size.
2. Preflight the host without printing secrets: service state, current resolved symlink target, disk capacity, sudo capability, pinned private-provider revision if relevant, and whether the feature-enable flag resolves to enabled or disabled.
3. Transfer the compiled artifact to a staging path; compare its target-side SHA-256 to the local expected checksum before installation.
4. Install into a commit-named immutable release directory, verify the installed checksum, retain the resolved old `current` target, then atomically repoint `current` and restart.
5. Treat convergence as a predicate on the expected **embedded commit** in loopback health, not merely a listening port. If it fails, restore the old symlink and restart immediately.
6. Verify the public hostname separately. For a disabled optional-provider release, make both keyword and semantic/hybrid requests and assert the exact truthful fallback fields—not just HTTP 200.
7. Persist privacy-safe evidence: source commit, embedded health commit, artifact checksum, pinned dependency revision, enabled/disabled state, bounded endpoint outcomes, and rollback target. Exclude provider endpoint, collection, vault path, environment values, credentials, raw results, and request headers.

**Version-label pitfall:** package semver and runtime health semver can drift even when the embedded commit is correct. Record both, but use the embedded full commit plus artifact checksum as release identity. Treat unexpected semver drift as follow-up release-metadata debt; do not silently substitute a version label for provenance.

## Semantic-provider activation reference

For private semantic-provider releases and controlled activation windows, use `references/semantic-provider-activation.md` before changing routing or provider capacity.

## DevSpace MCP service reference

For DevSpace-specific instance identity, systemd override pitfalls, the Caddy reverse proxy setup, and the 502 diagnostic path, see `references/devspace-mcp-service-specifics.md`.

## Private cross-host provider connectivity

A loopback-only semantic provider cannot be consumed by a separate application host without an explicit private transport. Before enabling the caller gate:

1. Enroll both hosts in an approved private network and prove caller-to-provider reachability over that network.
2. Bind any bridge/proxy only to the private interface, never `0.0.0.0` or a public address.
3. Enforce the caller peer plus the minimum provider paths and HTTP methods; do not proxy arbitrary traffic.
4. Verify the readiness contract from the caller and confirm it reports the expected application build identity.
5. Save a timestamped caller environment backup before changing semantic flags so rollback is a config restore plus restart, never a corpus/index operation.

A private readiness probe proves connectivity, not semantic eligibility. Run one real application semantic request and inspect execution metadata. If it returns `stale-index`, `timeout`, `unavailable`, or `overloaded`, immediately restore the saved keyword-only configuration and restart the caller. Treat this as a release gate result; never respond by relaxing the deadline or bypassing freshness checks.

### Validation mode can supersede an automatic latency rollback

A p95 gate is normally an activation policy, not a substitute for the operator's current intent. If the user explicitly changes the mode from strict gated activation to live validation:

1. Confirm the narrower authorization in writing: semantic may remain enabled for user testing; hybrid and private-boundary constraints remain unchanged.
2. Do **not** silently restore keyword-only merely because a latency benchmark misses the former threshold. Still roll back immediately for correctness or safety failures (`stale-index`, malformed output, privacy breach, unavailable provider without truthful fallback, etc.).
3. Restart with the authorized semantic configuration and verify health plus the effective semantic/hybrid flags before handing off the UI.
4. In the report, distinguish **functional validation pass** from **strict latency-gate pass**. Preserve the raw timings and name the former policy that was superseded.
5. Keep optimizing from measurements. A near-threshold warm path is not evidence to relax timeouts or weaken correctness controls.

## Persistent QMD provider performance pattern

A process-per-request QMD CLI can miss a strict semantic deadline even when a GPU and a certified index are available, because model initialization and automatic query expansion dominate the request. Before increasing a deadline, measure a bounded persistent-QMD alternative:

1. Keep the QMD daemon loopback-only and expose it only through the existing private-provider boundary.
2. Use QMD's structured REST query contract with one explicit `vec` search, a bounded candidate limit, and `rerank: false`; this avoids automatic expansion and reranking during the initial semantic lane.
3. Probe at least five sequential private requests and record result counts plus p95. A single warm response is not latency evidence.
4. Keep the caller/provider deadline unchanged. If p95 still misses the gate, leave semantic routing disabled rather than loosening timeouts.
5. Treat the persistent daemon and public-routing adapter as separate deployments: validate the daemon contract locally, then ship adapter changes through a reviewed PR before wiring the public server.

**Pitfall:** an SSM command can report aggregate success while a nested shell command emitted an error. After every remote binary swap, verify the intended checksum, unit `ExecStart`, active state, and a loopback readiness/request response; do not rely on SSM status alone.

For a measured semantic-latency investigation and safe caller-side prewarming approach, see `references/semantic-latency-triage.md`.

## Verification checklist

- [ ] Correct instance and current public IP verified live
- [ ] Service units active and expected ports listening
- [ ] Public hostname resolves to intended endpoint
- [ ] Direct-origin TLS/host-header probe succeeds
- [ ] Same-origin browser path is tested
- [ ] Reader/catalog includes the changed collection(s)
- [ ] Explorer/browser projection visibly includes the changed collection(s)
- [ ] Cross-origin rejection remains enforced when applicable
- [ ] Monitors use a hostname rather than a literal host IP
- [ ] Any EIP has a clear tag set and an association readback

## Pitfalls

- An account/API token that can create scoped credentials may not itself mutate DNS; determine its permission model before treating it as invalid.
- `systemctl show` can fail to reveal values supplied by an `EnvironmentFile`; inspect the running process environment for the one required key only.
- A healthy app service plus a stale DNS A record is still an outage.
- Do not report a browser-auth issue fixed merely because the backend changed from 403 to 401; also verify fresh navigation reaches the intended UI and leave user-mediated sign-in/session-artifact steps to the authorized operator.
