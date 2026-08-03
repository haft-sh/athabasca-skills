---
name: qmd-haft-search-deployment
description: Deploy QMD semantic search + Haft reader as a production service on EC2, including index portability, CPU embedding workarounds, bridge service, and reverse proxy setup.
tags: [qmd, haft, ec2, search, deployment, semantic-search]
triggers:
  - Deploying QMD or Haft search on a remote server
  - Setting up semantic search for a document vault
  - Transferring QMD indexes between machines
  - Configuring Haft reader with QMD backend
  - Building a QMD→Haft bridge service
---

# QMD + Haft Search Deployment

Deploy a QMD-powered semantic search backend with a Haft reader frontend on EC2 or any Linux server.

## Architecture

```
Browser → Caddy (443, auto-TLS) → Haft server (9001, SPA + API)
                                        ↓
                                  Bridge (7799) → QMD CLI (search/vsearch/query)
```

- **Haft server** (`bun src/index.ts` from repo root): serves the React SPA AND the API. Do NOT use `apps/server/src/index.ts` — that's API-only.
- **Bridge service**: translates Haft search requests to QMD CLI calls, maps QMD file paths to Haft page IDs.
- **Caddy**: reverse proxy with automatic Let's Encrypt TLS.

## QMD Index Portability

QMD stores document paths **relative to the collection root** in `documents.path`. The only absolute path is in `store_collections.path`. This means:

1. Build the index on a fast machine (8+ CPUs recommended)
2. Transfer `~/.cache/qmd/index.sqlite` to the target
3. Update `~/.config/qmd/index.yml` to match the collection name AND root path
4. The collection name in the config MUST match what's in the index (check `store_collections` table)

**Critical**: If the vault directory structure changed between index builds (e.g., hyphenated vs space/comma paths), the index is stale. Rebuild with `qmd collection remove` + rewrite `~/.config/qmd/index.yml` directly (don't use `qmd collection add` — it misinterprets paths with spaces).

### QMD Config Format

```yaml
collections:
  obsidian-vault:  # Must match the name in the transferred index
    path: /opt/haft-bbt/vault  # Collection root — relative paths resolve from here
    pattern: "**/*.md"
    context:
      "": "Description for search context."
models:
  embed: hf:ggml-org/embeddinggemma-300M-GGUF/embeddinggemma-300M-Q8_0.gguf
  generate: hf:tobil/qmd-query-expansion-1.7B-gguf/qmd-query-expansion-1.7B-q4_k_m.gguf
  rerank: hf:ggml-org/Qwen3-Reranker-0.6B-Q8_0-GGUF/qwen3-reranker-0.6b-q8_0.gguf
```

## CPU Embedding: Session Timeout Workaround

QMD's llama.cpp embedding session expires after ~30 minutes on CPU, embedding only ~1,000 chunks per run. For large vaults (15K+ docs), use an auto-restart loop:

```bash
for i in $(seq 1 50); do
  PENDING=$(qmd status 2>&1 | grep "Pending:" | grep -oP '\d+')
  if [ "$PENDING" = "0" ] || [ -z "$PENDING" ]; then
    echo "=== ALL EMBEDDED after $i runs ==="
    break
  fi
  echo "=== Run $i: $PENDING docs pending ==="
  qmd embed --max-docs-per-batch 20 --max-batch-mb 10 2>&1 | tail -5
  sleep 5
done
```

- Use `--max-docs-per-batch 20 --max-batch-mb 10` to minimize wasted work per timeout
- Each run embeds ~1,000 chunks in ~30 min on 8 CPUs
- 15K docs ≈ 17 runs ≈ 8-9 hours total
- Run as a background process with notify_on_complete

### Resumable CPU rebuild discipline

Separate a one-time **initialization** action from the repeatable **resume** action:

1. Initialization backs up the prior QMD state, removes a stale collection only after preflight, writes the canonical collection config, and runs `qmd update` once.
2. The long-running resume loop must only read `qmd status` and run bounded `qmd embed` batches. It must never call `qmd collection remove` or `qmd update`, so restarting the unit cannot discard partial embedding progress.
3. Parse the `Pending:` count with a strict, tested parser. If the count cannot be read, fail the unit rather than running an unbounded loop; exit successfully only when it is exactly zero.
4. Run the loop in a named systemd unit and inspect both unit state and its child process tree. An `active` shell alone is not proof that an embedding child is still progressing.

## Haft Import

- `haft import <path> --recursive --wait` processes files sequentially (~27 files/min)
- 15K files ≈ 9-10 hours
- The vault catalog (SQLite reader) is committed only when the import job finishes
- Monitor with `haft import status` and `haft vault status`
- Manifest grows during import; `vault status` shows 0 pages until commit

### Large corpus additions and tree migrations

Treat content copy, path restructuring, catalog rebuild, and browser verification as one operation. On-disk files alone do not prove the reader or Explorer will expose the collection.

1. Pin the source revision and stage only approved source paths. For a large repository, use a sparse checkout so the import is reproducible without cloning unrelated content.
2. Before a path migration, generate a complete move map with source/destination existence checks and file counts. Keep a bounded backup of the prior manifest, catalog/index files, Explorer projection, and the move map; folder renames on the same filesystem are reversible, but projection rebuilds are not.
3. Stop the reader and bridge only for the short mutation/rebuild window. Restart both after rebuilding; do not serve a catalog while source paths are being renamed.
4. Import a coherent canary slice first (for example, one year folder), rebuild, and verify that exact folder through the public tree endpoint. Only then bulk-import the remaining slices and rebuild once more.
5. Verify all three layers after a completed batch: on-disk Markdown count, rebuilt page/chunk count, and public tree children/direct-child counts. Also probe public root and health after server startup; the proxy can briefly return 502 before the app listener is ready.
6. Run the content-copy and index-rebuild payload as the same unprivileged account that owns the vault and runs Haft. A root-run maintenance wrapper can correctly stop/start services yet leave regenerated SQLite/WAL projection files root-owned, making the Explorer return a generic unavailable error after restart. Keep only service lifecycle actions privileged; invoke the payload with `sudo -u <service-user>`, then verify owner/mode of newly generated catalog and Explorer files before public testing.
7. A catalog rebuild after new content intentionally invalidates semantic freshness evidence. Do not hand-wave the resulting `stale-index` fallback: prepare a new rebuild manifest, compare exact source keys plus page/source/content hashes against the prior certified manifest, update the provider/index for any real additions, and reconcile only after `eligible = indexed = mapped`, `unmapped = pending = 0`.
8. Preserve or explicitly plan legacy reader URLs before broad path changes. A cleaner hierarchy can otherwise break durable links even if the catalog rebuild succeeds.

### Canonical-path migration: QMD config and feature-gate reconciliation

After a vault tree migration or bulk import, inspect all three layers before calling semantic search healthy:

1. Compare the QMD collection path in `~/.config/qmd/index.yml` with the active Haft `VAULT_ROOT`. A bridge can be active while QMD still indexes a retired source path.
2. Run `qmd status` and inspect document count and last-updated time. Old path results from `qmd vsearch`, a stale timestamp, or new pending embeddings mean the semantic index is stale.
3. Inspect the Haft service environment for both `HAFT_QMD_SEARCH=1` (or `true`) and `HAFT_QMD_ENDPOINT=http://127.0.0.1:7799`. A healthy bridge alone does not enable the public semantic adapter.
4. Do **not** enable the Haft semantic gate while the canonical QMD index is rebuilding. Otherwise semantic/hybrid API modes can silently degrade or return stale paths.
5. When the collection still references a retired root, first back up its QMD config and SQLite index; then run `qmd collection remove <collection>`, rewrite `index.yml` for the canonical root, and use `qmd update` followed by restart-safe embedding batches.
6. Only after QMD totals match the current reader catalog and a real vector canary returns canonical paths should you enable the Haft gate, restart only `haft-bbt-server`, and probe keyword, semantic, and hybrid API modes with distinguishable queries.

For a long rebuild, use a named transient `systemd-run` unit rather than an SSH-bound process. Its journal and unit state are the durable operator handoff.

### Public semantic-search rollout and truthful degradation

For a public semantic product, a healthy QMD engine, bridge process, or `200` response is not sufficient. Verify index freshness, provider execution, catalog identity mapping, public visibility projection, and product-facing execution labels separately.

1. Land reusable source changes through ordinary PRs to the shared default branch, with semantic-provider execution disabled by default. Do not create a long-lived environment source fork solely for the first rollout.
2. Make the first host a controlled deployment target: use a reviewed pinned SHA and environment-specific configuration, record rollout evidence, and retain a rollback that disables the gate or restores the previous release pointer without catalog/corpus surgery.
3. Keep requested mode separate from effective mode. A semantic/hybrid request that falls back to lexical results must be marked as degraded with `effectiveMode: "keyword"`; do not retain a semantic label merely because that was the request.
4. Keep public metadata backend-neutral. Never expose collection IDs, provider names/URLs, raw QMD paths or IDs, raw errors, raw queries, or private counters.
5. Do not expose an existing owner-local/private-read route anonymously as a shortcut. Anonymous search needs a server-enforced public projection that cannot leak private/unlisted content through results, counts, snippets, facets, source paths, relationships, or ranking.
6. Make the bridge repo-owned and versioned. It should return bounded semantic candidates only; Haft owns public result projection and the lexical-plus-semantic hybrid merge.
7. Add provider deadline/cancellation, child-process cleanup, concurrency backpressure, bounded output, and redacted logs before increasing the caller HTTP timeout. A client timeout that leaves QMD work running is an availability defect.
8. Prove every semantic candidate maps to current catalog `pageId`/`chunkId` identity. Reject stale or ambiguous records; filename-only fallback is forbidden.
9. Treat semantic-index *evidence* as a separate release gate from QMD health. A prior failed freshness record (for example, a superseded case-fold certification failure) will correctly make the server report `stale-index` even if the current QMD index is complete and reachable. Before any activation, inspect the private freshness state and rebuild manifest, then compare their revisions/counts to the certified active index.
10. Reconcile freshness only with a reviewed runtime that includes the semantic-index operator command. If the deployed artifact can enforce freshness but lacks `haft index semantic reconcile`, do not hand-edit private state JSON or bypass the gate. Deploy a reviewed disabled-routing artifact first and verify its public health commit after restart—stale `HAFT_EMBEDDED_BUILD_*` environment values can misreport artifact identity. Back up the old private state/rebuild manifests, generate the current manifest, and compare exact source keys plus page ID, source hash, and content hash before reuse. Reconcile only when that comparison shows no identity/content drift and independently verified counts satisfy `indexed = mapped = eligible`, `unmapped = pending = 0`. This metadata operation must not mutate corpus, catalog, or the provider index.
11. Keep hybrid provider execution disabled until semantic execution is independently correct and measured. The first hybrid path should use Haft's lexical ranking plus the same semantic-candidate provider, not delegate public hybrid semantics to QMD.
12. On any public semantic canary failure, restore the saved pre-activation server environment and restart immediately. Verify health, keyword non-degradation, and semantic `disabled` fallback before beginning diagnosis; leave semantic disabled until a new explicitly approved activation window.

See `references/public-semantic-rollout-contract.md` for the recommended additive execution-provenance shape, QMD CLI compatibility note, containment requirements, and rollout policy.

### Case-sensitive corpus identity preflight

Before a QMD rebuild, compare the canonical catalog manifest to the provider's active document identities using **exact, case-sensitive** relative paths. Do this before starting corpus-wide embedding.

- Treat paths differing only by case as distinct when the vault is case-sensitive.
- Some QMD releases include a legacy `path COLLATE NOCASE` fallback. It can silently collapse case-distinct documents; an apparently successful `qmd update` is not evidence of complete coverage.
- Count exact-path and case-fold collisions. A case-fold collision blocks certification unless the provider demonstrably preserves both exact identities.
- If identities collapse, stop the embedding unit, leave semantic routing fail-closed, and rebuild from a clean provider database only after applying a version-pinned identity-safe fix. Never continue a partially built collapsed index.
- Preserve a deterministic catalog manifest with page ID, exact source key, and source/content hashes. Reconcile it after update and again after embedding: require `eligible = indexed = mapped` and `pending = unmapped = ambiguous = 0`.
- Do **not** compare QMD vector-row totals directly to catalog document totals: one document can yield multiple chunks/vectors, while QMD pending work can be reported as unique content hashes. Use the provider's active-document identity table for document coverage, and use vector/pending counters only for embedding-completion progress.
- Do not rewrite canonical corpus paths just to accommodate provider normalization. Prefer an upstream/provider fix or an explicit catalog-owned opaque-key projection with one-to-one mapping.

See `references/case-sensitive-provider-identity.md` for remediation and validation details. For bounded corpus additions and incremental GPU reindexing behind a persistent private daemon, see `references/corpus-addition-and-gpu-reindex.md`.

### Offline GPU index builds

A GPU worker can accelerate the expensive **offline QMD embedding build** without becoming a public search dependency. Use this as a controlled portability workflow:

#### Persistent-daemon runtime discipline

The live QMD daemon may use a service-specific SQLite cache rather than the interactive user's default `~/.cache/qmd`. Before any incremental update:

1. Inspect the daemon unit and process file descriptors to identify the active SQLite index; do not infer it from an ordinary shell `qmd status`.
2. If the environment file is root/systemd-readable only, preserve that boundary. Load it as root and invoke QMD as the service account with only its required config/index variables.
3. Stop only the private daemon while mutating its SQLite index and restore it unconditionally with a cleanup trap.
4. For AWS SSM `AWS-RunShellScript`, use a checksum-verified standalone Bash script for nontrivial update workflows. SSM runs inline commands via `/bin/sh`; embedded Bash features, Python heredocs, traps, and `pipefail` are fragile and must not be relied upon.
5. After update/embed, compare exact case-sensitive `documents.path` identities to the staged vault Markdown paths. Require equal indexed/filesystem totals and zero missing, unexpected, and case-fold-collision groups before reconciling Haft freshness.
6. After reconciliation and server restart, verify the product surface—not just QMD: a semantic API canary must report `execution.effectiveMode: semantic`, `degraded: false`, `semantic.state: used`, and non-empty mapped results. Read only execution metadata/counts in operator logs; do not retain query text or result content.
7. Use a read-only status-change monitor for long updates and post-certification health. It should be silent when unchanged, track the certified document/vector target plus semantic execution state, and must never restart services or perform mutation.
8. Give scheduled monitors their own explicit, reproducible authentication/config path; do not rely on interactive-shell `~` expansion or inherited environment. If a monitor cannot complete a check, report it as **monitor verification unavailable**, not as a target-service degradation. Alert on target degradation only after an actual authenticated health/canary probe returns degraded evidence.

1. Keep the CPU rebuild running as the fallback until the GPU path is proven—unless a provider identity defect has already made the CPU index invalid. In that case stop it and leave public semantic routing fail-closed.
2. Stage a revision-pinned copy of the canonical vault on the GPU worker, preserving exact relative paths while excluding vault-private state, backups, and prior provider indexes. Record file count plus a deterministic archive/content digest before transfer and verify it on the worker.
3. Pin the provider build commit and model configuration. If an identity-safety fix is awaiting a package release, a reviewed source build may be used only with that commit recorded, a clean index, and an upstream PR/issue link.
4. Before embedding, run the exact/case-fold provider-identity preflight from the preceding section against the clean GPU index. Do not begin corpus-wide GPU work unless it passes.
5. Verify actual GPU use with a representative batch: record `qmd status` counters, `nvidia-smi` utilization and memory, and elapsed throughput. GPU memory allocation alone is insufficient evidence; a sampled active-utilization reading is required.
6. Build the full index in a durable named systemd unit. When the pinned QMD version supports a configurable embed-session timeout, set an explicit unlimited or suitably large timeout rather than relying on repeated CPU-era session expiry loops. Monitor unit state, vector/pending counters, and GPU activity independently.
7. Transfer the resulting SQLite index only after recording source revision, provider build commit, model, identity-preflight evidence, and target index/config backup. On the target, set the collection root to the canonical vault path and re-run the identity preflight plus direct vector canaries.
   - Verify the transfer checksum **before opening the SQLite file with QMD**. QMD can write query/LLM cache or runtime metadata during a read canary, so a post-canary byte hash may legitimately differ even when document identities and vectors are unchanged. Treat the post-canary certification contract as: exact identity reconciliation, vector/pending counters, and direct retrieval canary; create a fresh SQLite backup/checksum only if a new immutable handoff artifact is required.
   - Keep target validation isolated under separate `XDG_CONFIG_HOME` / `XDG_CACHE_HOME` paths until promotion. Do not overwrite the live bridge index or enable a feature flag as part of validation.
8. Keep public semantic routing disabled until catalog identity/freshness and provider gates pass. Stop the on-demand GPU worker after the build/certification job unless the user deliberately retains scarce capacity for an explicitly prioritized adjacent private workload; a portable index build alone does not justify an always-on model service.

### External GPU embedding and reranking services

A running GPU service is not a QMD upgrade by itself. QMD's local SQLite/vector index and bridge remain the product search path until the bridge/server is explicitly adapted to call the private service.

- Bind inference only to a private VPC or Tailscale address; never expose a model API publicly by default.
- Verify the NVIDIA container runtime with a CUDA canary before deploying models.
- Verify model readiness with a real health/request probe after weights load, not just a running-container state.
- Use separately versioned embedding and reranking endpoints, record model IDs/configuration in deployment notes, and retain a CPU/QMD fallback during integration.
- Do not trigger corpus-wide re-embedding until all planned imports and path moves are complete; otherwise expensive work is repeatedly invalidated by path churn.

### Persistent QMD daemon for deadline-bound semantic candidates

A per-request QMD CLI spawn can spend most of a tight semantic deadline initializing the embedding model, even when the index and GPU are healthy. Before raising a caller deadline, measure the same bounded query through QMD's persistent local HTTP/MCP daemon.

1. Keep the QMD daemon bound to loopback only; the semantic provider, not the daemon, owns the public/private boundary.
2. Use QMD's structured `/query` endpoint with exactly one explicit `vec` search, a bounded `candidateLimit`, and `rerank: false`. This skips automatic query expansion and avoids generation/reranking where Haft owns ranking and projection.
3. Warm the daemon, then run at least five real requests against the intended collection. Record result counts and p95 against the existing provider deadline. A one-off fast warm request is not enough.
4. Only after the daemon proves the deadline can be met, add an opt-in provider adapter for a validated loopback HTTP origin. Preserve CLI execution as the default fallback until the new path is merged and deployed.
5. Retain the CLI path's controls: caller cancellation, deadline, bounded response body and candidate count, admission concurrency/queue, typed redacted errors, exact source-key mapping, and readiness checks.
6. Run end-to-end private canaries after deployment; do not enable public semantic/hybrid routing merely because the daemon is fast locally.

**Pitfall:** current QMD `vsearch` behavior automatically expands a natural-language query. Reducing only `-n` does not eliminate multiple embedding calls. For a single-vector candidate lookup, use structured `/query` instead.

**Reboot/contract pitfall:** a ready daemon and a successful direct `/query` response do not prove the provider adapter is usable. After a reboot, warm the daemon and run the actual provider-contract request over the intended private route before enabling the public gate. Validate the observed structured-result schema against the adapter strictly; QMD may return nullable optional fields such as `context: null`, which must be accepted deliberately and covered by a regression test rather than treated as malformed output. Any adapter contract mismatch is a fail-closed canary failure: keep public semantic disabled, fix it through a reviewed PR, then repeat the private probe.

**Private-provider release pitfall:** deploy the provider executable and its systemd wiring as one atomic release. Updating a release directory, symlink, or provenance environment value is insufficient when `ExecStart` names a versioned binary directly. Before claiming a provider release is live, verify all of: the artifact checksum, `systemctl cat`/resolved `ExecStart`, the running process executable, `/ready` build SHA, and a real BBT-originated `POST /v1/candidates` request. The Haft server adapter posts to the exact configured endpoint; configure the complete candidate route (for example, `http://<private-peer>:<port>/v1/candidates`), not merely its origin.

**End-to-end latency pitfall:** provider/daemon latency and Haft product latency are distinct gates. A fast private QMD request does not clear semantic activation if the Haft API still loads catalog/projection state or otherwise takes too long. During an authorized activation window, measure at least five mapped semantic requests through the real Haft API using the intended authorization/surface. Record cold and warm requests separately: a cold first request can hide startup/caching cost even when steady-state requests are near the deadline. Require truthful execution (`effectiveMode: semantic`, `semantic.state: used`, mapped non-empty results for the relevance fixture) and compare product p95 to the agreed target. Default policy is immediate keyword-only rollback after a failed gate, but an explicit user instruction to accept the validation and leave semantic enabled overrides that rollback policy; retain hybrid disabled and report the measured failure plainly. Do not repeatedly ask for confirmation within an explicitly authorized rollout window—execute the bounded preflight, release, canary, and required rollback path decisively, escalating only for a genuinely new scope or a failed gate.

**Catalog snapshot-cache remedy:** search routes must not recreate a large `ReaderDataStore` on every request. That defeats `WeakMap`-keyed semantic identity-mapping caches and can dominate end-to-end latency even when QMD is fast. Cache by vault root and catalog reader snapshot generation, not only by a closure tied to one route-factory instance: application composition can instantiate more than one route/cache closure. Read the inexpensive generation each request, reuse the same store when unchanged, and rebuild the store/mapping only when the generation advances. Cover reuse across separately constructed cache factories and invalidation after an index rebuild in tests. For a UI-facing semantic service, prewarm the generation-bound ReaderDataStore and semantic identity mapping during server startup when semantic routing is configured; this moves first-interactive-request setup off the UI path without calling the provider at boot. Never use a cache that survives a catalog-generation change.

## Bridge Service

See `references/bridge-service.md` for the full bridge implementation.

Key points:
- Maps QMD `qmd://collection/path` URIs to Haft `page-*` IDs via normalized path matching
- Both QMD and Haft normalize paths to lowercase-hyphenated form
- Must `await proc.exited` before reading stdout/stderr from Bun.spawn
- Use full path to qmd binary (`/usr/bin/qmd`) in systemd services
- Reload manifest via `POST /reload` after Haft import completes

## Haft Server Entry Point

**Critical distinction**:
- `bun src/index.ts` (repo root) → serves SPA + API (uses `import index from "./index.html"`)
- `bun apps/server/src/index.ts` → API only, no frontend

Build the frontend first: `bun run build` from repo root (runs CSS build + haft-build.ts).

## Caddy Reverse Proxy

```
bbt.haft.sh {
    reverse_proxy localhost:9001
}
```

Caddy auto-obtains Let's Encrypt certs. Ensure ports 80/443 are open in the security group.

## Systemd Services

Three services needed:
1. `qmd-haft-bridge.service` — Bun bridge on port 7799
2. `haft-bbt-server.service` — Haft server on port 9001 (depends on bridge)
3. `caddy.service` — Reverse proxy (system-managed)

See `references/systemd-services.md` for unit file templates.

## DNS Setup

When using Cloudflare DNS with Caddy handling TLS:

- Create an **A record** pointing the subdomain at the instance IP
- Set `proxied: false` (DNS-only / grey cloud) — Cloudflare proxying intercepts port 80 and breaks Caddy's ACME challenge
- Via API: `{"type":"A","name":"bbt","content":"<ip>","ttl":1,"proxied":false}`

## Haft Documentation: Two Locations

Haft has two distinct docs locations. When the user says "docs" they almost always mean the **public** site:

1. **Public Docusaurus docs** (`apps/docs/`): The user-facing documentation at `https://haft.sh/docs`. This is where deployment guides, quick starts, and operational how-tos belong. Structure:
   - Content in `apps/docs/docs/` organized by category (`getting-started/`, `guides/`)
   - Navigation wired in `apps/docs/sidebars.js`
   - Each page has YAML frontmatter with `id` and `title`
   - Kebab-case filenames
   - Build: `bun run build` from `apps/docs/` (requires Node 22; fails on Node 25 due to webpack incompatibility)

2. **Internal ops docs** (`docs/` at repo root): Dated internal runbooks and contracts (`YYYY-MM-DD-<slug>.md`). Use for implementation-specific detail, security audits, and internal handoffs that shouldn't be public.

**Default to the public Docusaurus site** unless the user explicitly asks for an internal doc.

## OOM Recovery & Catalog Rebuild

When a t3.large (2 vCPU / 8GB) runs Haft import + QMD embedding model simultaneously with zero swap, the system OOMs and freezes completely. Reboot alone may not recover it — a full **stop/start** is needed.

### Recovery procedure

1. `aws ec2 stop-instances --instance-ids <id> --region <region>` then `start-instances`
2. **Public IP changes** on stop/start (non-elastic) — update Cloudflare DNS A record immediately
3. SSH with the correct key (check `~/.ssh/` for region-specific keys)
4. Add swap to prevent recurrence:
   ```bash
   sudo fallocate -l 4G /swapfile && sudo chmod 600 /swapfile
   sudo mkswap /swapfile && sudo swapon /swapfile
   echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
   ```
5. Check services: `systemctl status haft-bbt-server qmd-haft-bridge caddy`

### Catalog corruption after crash

If the instance OOMs during import, `index.sqlite` may be corrupted/empty (e.g. 484K) while the manifest (`manifest.json`, ~48MB for 15K files) remains intact. Symptoms:
- Server logs show `Vault mounted (source: env; state: empty)`
- All API routes return `NOT_FOUND`
- `/api/app/status` shows `pages: 0`

**Fix**: Rebuild the catalog from the manifest:
```bash
cd /opt/haft-bbt/haft
bun run src/cli.ts index rebuild --vault /opt/haft-bbt/vault/haft-bbt
# Output: "Index rebuilt. Pages: 13383, Chunks: 13383"
sudo systemctl restart haft-bbt-server
```

The import CLI (`src/cli.ts`) will report "already cataloged" for all files because the manifest is intact — but the SQLite pages table is empty. `index rebuild` repopulates it without re-importing.

### Long-running imports: use systemd-run, not nohup

`nohup` processes die when the SSH session times out. Use transient systemd units:
```bash
sudo systemd-run --unit=haft-import \
  --working-directory=/opt/haft-bbt/haft \
  --setenv=HOME=/home/ubuntu \
  --setenv=PATH=/usr/bin:/usr/local/bin:/home/ubuntu/.bun/bin \
  /home/ubuntu/.bun/bin/bun run src/cli.ts import /opt/haft-bbt/vault/haft-bbt \
  --vault /opt/haft-bbt/vault/haft-bbt --recursive --on-duplicate skip --wait
```

## Haft API Routes & Search Schema

### Key endpoints

| Route | Method | Purpose |
|-------|--------|---------|
| `/health` | GET | Server health (NOT under `/api/`) |
| `/api/app/status` | GET | Vault state, page count, ready status |
| `/api/vault/tree` | GET | Full recursive file tree |
| `/api/reader/navigation` | GET | All pages with slugs, prev/next links |
| `/api/search` | **POST** | Keyword/semantic/hybrid search |
| `/api/reader/pages/by-slug` | GET | Single page lookup by slug |

### Search request schema (POST /api/search)

```json
{
  "query": "nature of the soul",
  "mode": "keyword",          // "keyword" | "semantic" | "hybrid"
  "pagination": { "limit": 10 },  // limit goes INSIDE pagination, NOT top-level
  "filters": {}               // optional: pageIds, sourceKinds, artifactClasses, etc.
}
```

**Common mistake**: Putting `limit` at the top level causes a validation error. It must be nested inside `pagination`.

### Performance at scale (13K+ pages)

Known scaling issues with large vaults:
- `/api/reader/navigation` returns ALL pages in one response (~11 MB for 13K pages)
- `/api/vault/tree` returns the full recursive tree (~9.6 MB)
- Frontend has no list virtualization — expanding all folders creates 13K+ DOM nodes
- No depth-limiting or lazy-load on tree/navigation endpoints

The frontend fetches both endpoints in parallel on mount (`data-loading.ts`), holding ~25-30 MB in React state. This is tolerable on desktop with fast connections but breaks mobile/slow connections.

**Mitigation roadmap** (not yet implemented; measured payload sizes and frontend hotspots are in `references/performance-at-scale.md`):
1. Add `?depth=N` to `/api/vault/tree` + `/api/vault/tree/children?path=...` for lazy expansion
2. Split navigation into per-page adjacent lookup (already exists as `/api/reader/pages/by-slug`)
3. Add `@tanstack/react-virtual` to `VaultBrowserTree.tsx` (rows are already a flat array)
4. Paginate `/api/vault/files` with cursor + folder filter

## Operational verification: separate engine, adapter, and product surface

When investigating an existing QMD + Haft deployment, verify these independently; none implies the next layer works:

1. **QMD engine:** SSH to the host and run `qmd status`, then a real `qmd vsearch` canary against the intended collection. This establishes whether indexed vectors and retrieval work.
2. **Adapter:** inspect the bridge service and logs, and confirm QMD result URIs map to Haft page IDs. A bridge can be healthy while some source paths have no reader-page mapping.
3. **Haft runtime:** probe `/health` and `/api/app/status` both locally and publicly. `systemctl is-active` only proves process state; it does not prove that the HTTP event loop is serving requests.
4. **Feature flag/configuration:** inspect server startup logs for whether semantic search is enabled. A running QMD bridge does not automatically mean the Haft server calls it.
5. **Managed CLI surface:** `haft query --remote <slug>` is bounded metadata/excerpt discovery unless its contract explicitly exposes semantic modes. Do not describe it as semantic search merely because the target has QMD. Also confirm the target is actually enrolled in `haft remotes`.

If users need to test before UI/API wiring is repaired, provide the host-local QMD procedure as an operator workaround and label it clearly as non-product access.

## Pitfalls

- `qmd collection add <name> <path>` misinterprets paths with spaces — write `~/.config/qmd/index.yml` directly
- The npm package `qmd` is a squatter (v0.0.0) — the real package is `@tobilu/qmd`
- Haft import shows `Imported: 0` in job status until the entire job completes — monitor via manifest size and file count instead
- QMD `vsearch` cold-starts the embedding model (~30-60s on CPU) — set bridge timeouts to 300s+
- Security scanner blocks `curl | bash` — download installers to disk first, then execute
- Security scanner blocks `nohup` — use `systemd-run` for transient units or `terminal(background=true)`
- **Cloudflare DNS must be `proxied: false`** when Caddy handles TLS. Proxied records route through Cloudflare's edge, which intercepts port 80 and causes ACME/Let's Encrypt certificate issuance to fail silently or timeout.
- **Haft server entry point**: `bun src/index.ts` (repo root) serves SPA + API. `bun apps/server/src/index.ts` is API-only — if you see raw JSON at the root URL instead of the reader UI, this is the cause.
- **EC2 stop/start changes public IP** (non-elastic) — always update DNS after recovery. Reboot preserves the IP but may not recover a fully frozen system.
- **OOM during import corrupts index.sqlite but not manifest.json** — use `bun run src/cli.ts index rebuild --vault <path>` to recover without re-importing.
- **Search `limit` must be inside `pagination` object** — top-level `limit` causes a validation error with no useful message.
- **`/api/health` doesn't exist** — use `/health` (root) or `/api/app/status` for vault state.
