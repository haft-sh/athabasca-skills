# Wikimedia Commons — Direct Image Download

Wikimedia Commons blocks direct `curl` hotlinks with HTML error pages. To download:

## Step 1: Find the actual upload URL

1. Navigate to the file page in browser: `https://commons.wikimedia.org/wiki/File:.jpg`
2. Open browser DevTools console (`F12` → Console)
3. Run:
   ```js
   [...document.querySelectorAll('a')].filter(a => a.href.includes('upload.wikimedia.org')).map(a => a.href).join('\n');
   ```
4. Copy the full-resolution URL (e.g., `https://upload.wikimedia.org/wikipedia/commons/a/a4/File.jpg`)

## Step 2: Download with user-agent

```bash
curl -sS -L -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
  -o local-copy.jpg \
  "https://upload.wikimedia.org/wikipedia/commons/[hash]/[filename]"
```

**Thumbnails** are under `/thumb/` path:
```bash
curl -sS -L -A "Mozilla/5.0" -o image.jpg \
  "https://upload.wikimedia.org/wikipedia/commons/thumb/[hash]/[filename]/1280px-[filename]"
```

## Key insight

The Wikimedia redirector (`https://commons.wikimedia.org/wiki/Special:FilePath/...`) doesn't give you the raw URL directly. The browser console extraction is the reliable path to the actual CDN URL.