# Stale Browser Cache Debugging

A "syntax error" appearing on a page immediately after a clean build is almost always a **stale browser cache**, not a new bug introduced by the build.

## The Pattern

1. Build succeeds: `bun run build` exits 0, no errors
2. Page loads in browser — shows a syntax error or blank content
3. Console may show React error or parser error
4. Developer assumes the new code is broken

## How to Verify

**Hard refresh** (not just refresh):
- macOS: `Cmd + Shift + R`
- Windows/Linux: `Ctrl + Shift + R`

Or open DevTools → Network tab → disable cache → reload.

## The Signal in This Session

The page was loading correctly. The only console errors were:
- `%cDownload the React DevTools...` (info, harmless)
- `[Bun] Hot-module-reloading socket connected...` (info, harmless)

There were **zero JS errors**. The "syntax error" was a stale cache artifact from before the last build.

## Rule

When a page looks broken after a clean build:
1. Hard refresh first — before debugging the code
2. Check console for actual JS errors (not just warnings)
3. If no errors appear and the page still looks wrong, open DevTools Network tab and confirm all assets are loading fresh

**Never start bisecting or reverting code on a stale-cache report.**