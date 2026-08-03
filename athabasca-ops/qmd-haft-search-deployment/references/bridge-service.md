# QMD→Haft Bridge Service

Bun/TypeScript service that translates Haft search requests to QMD CLI calls and maps results back to Haft page IDs.

## How Path Mapping Works

QMD returns file URIs like `qmd://obsidian-vault/Books/BBT/Srimad-Bhagavatam, Canto 01/Chapter 01/SB 1.1.1.md`.
Haft manifest has `source.path` like `srimad-bhagavatam,-canto-01/chapter-01/sb-1-1-1.md` and `pageId` like `page-srimad-bhagavatam-canto-01-chapter-01-sb-1-1-1-md`.

Both normalize to the same lowercase-hyphenated form. The bridge:
1. Strips the `qmd://collection/` prefix from QMD file URIs
2. Normalizes both QMD paths and Haft source paths to `lowercase-hyphenated`
3. Looks up the normalized QMD path in a map built from the Haft manifest
4. Falls back to filename-only matching if full path doesn't match

## Full Implementation

```typescript
#!/usr/bin/env bun
import { readFileSync } from "fs";
import { join } from "path";

const PORT = parseInt(process.env.BRIDGE_PORT || "7799", 10);
const VAULT_ROOT = process.env.VAULT_ROOT || "/opt/haft-bbt/vault/haft-bbt";
const QMD_COLLECTION = process.env.QMD_COLLECTION || "obsidian-vault";
const QMD_BIN = process.env.QMD_BIN || "/usr/bin/qmd";

interface HaftPage { pageId: string; title: string; source: { kind: string; path: string } }
interface HaftManifest { pages: HaftPage[] }
interface QmdHit { docid: string; score: number; file: string; line: number; title: string; context: string; snippet: string }
interface HaftSearchRequest { query: string; mode: "keyword" | "semantic" | "hybrid"; filters?: Record<string, unknown>; limit?: number }
interface HaftSearchResult { pageId: string; chunkId?: string; score?: number; excerpt?: string; sectionType?: string }

let manifest: HaftManifest | null = null;
let pathToPageId: Map<string, string> = new Map();

function normalizePath(path: string): string {
  return path.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
}

function loadManifest() {
  const manifestPath = join(VAULT_ROOT, ".haft", "manifest.json");
  try {
    const raw = readFileSync(manifestPath, "utf-8");
    manifest = JSON.parse(raw) as HaftManifest;
    pathToPageId.clear();
    for (const page of manifest.pages) {
      pathToPageId.set(normalizePath(page.source.path), page.pageId);
      const filename = page.source.path.split("/").pop()?.toLowerCase() || "";
      if (filename) pathToPageId.set(`file:${filename}`, page.pageId);
    }
    console.log(`[bridge] Loaded manifest: ${manifest.pages.length} pages, ${pathToPageId.size} path mappings`);
  } catch (err) {
    console.error(`[bridge] Failed to load manifest: ${err}`);
    manifest = null;
  }
}

function qmdFileToHaftPageId(qmdFile: string): string | undefined {
  const match = qmdFile.match(/^qmd:\/\/[^/]+\/(.+)$/);
  if (!match) return undefined;
  const relativePath = match[1];
  const exactMatch = pathToPageId.get(normalizePath(relativePath));
  if (exactMatch) return exactMatch;
  const filename = relativePath.split("/").pop()?.toLowerCase() || "";
  return pathToPageId.get(`file:${filename}`);
}

async function searchQmd(request: HaftSearchRequest): Promise<QmdHit[]> {
  const { query, mode, limit = 50 } = request;
  const qmdCommand = mode === "keyword" ? "search" : mode === "semantic" ? "vsearch" : "query";
  const qmdArgs = [query, "-c", QMD_COLLECTION, "--json", "--limit", String(limit)];
  console.log(`[bridge] QMD ${qmdCommand}: ${query}`);

  const proc = Bun.spawn([QMD_BIN, qmdCommand, ...qmdArgs], { stdout: "pipe", stderr: "pipe" });

  // CRITICAL: await process exit BEFORE reading streams
  const exitCode = await proc.exited;
  const stdout = await new Response(proc.stdout).text();
  const stderr = await new Response(proc.stderr).text();

  if (exitCode !== 0) {
    console.error(`[bridge] QMD error (exit ${exitCode}): ${stderr.slice(0, 500)}`);
    return [];
  }
  try {
    const hits = JSON.parse(stdout) as QmdHit[];
    return Array.isArray(hits) ? hits : [];
  } catch (err) {
    console.error(`[bridge] Failed to parse QMD output: ${err}`);
    return [];
  }
}

function mapQmdHitsToHaft(hits: QmdHit[]): HaftSearchResult[] {
  const results: HaftSearchResult[] = [];
  for (const hit of hits) {
    const pageId = qmdFileToHaftPageId(hit.file);
    if (!pageId) { console.warn(`[bridge] No pageId for: ${hit.file}`); continue; }
    results.push({ pageId, score: hit.score, excerpt: hit.snippet, sectionType: "body" });
  }
  return results;
}

const server = Bun.serve({
  port: PORT,
  async fetch(req: Request): Promise<Response> {
    const url = new URL(req.url);
    if (url.pathname === "/health") {
      return Response.json({ status: "ok", manifestLoaded: manifest !== null, pageCount: manifest?.pages.length ?? 0, pathMappings: pathToPageId.size });
    }
    if (url.pathname === "/reload") {
      loadManifest();
      return Response.json({ status: "reloaded", pageCount: manifest?.pages.length ?? 0 });
    }
    if (url.pathname === "/search" && req.method === "POST") {
      try {
        const request = await req.json() as HaftSearchRequest;
        if (!request.query) return Response.json({ error: "Missing query" }, { status: 400 });
        const qmdHits = await searchQmd(request);
        const haftResults = mapQmdHitsToHaft(qmdHits);
        console.log(`[bridge] "${request.query}" → ${qmdHits.length} QMD hits → ${haftResults.length} Haft results`);
        return Response.json({ results: haftResults });
      } catch (err) {
        console.error(`[bridge] Search error: ${err}`);
        return Response.json({ error: "Search failed" }, { status: 500 });
      }
    }
    return Response.json({ error: "Not found" }, { status: 404 });
  },
});

loadManifest();
console.log(`[bridge] Listening on http://localhost:${PORT} | Vault: ${VAULT_ROOT} | Collection: ${QMD_COLLECTION} | QMD: ${QMD_BIN}`);
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `BRIDGE_PORT` | 7799 | HTTP listen port |
| `VAULT_ROOT` | /opt/haft-bbt/vault/haft-bbt | Haft vault path (for manifest.json) |
| `QMD_COLLECTION` | obsidian-vault | QMD collection name (must match index) |
| `QMD_BIN` | /usr/bin/qmd | Path to qmd binary |
