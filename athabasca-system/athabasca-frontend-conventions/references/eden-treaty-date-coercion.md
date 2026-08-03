# Eden Treaty Date Coercion Pitfall

## The bug

Eden Treaty (`@elysiajs/eden`) silently converts date-like string fields into JavaScript `Date` objects at the transport layer. This happens **even when the Zod response schema declares `z.string()`** and the TypeScript type says `string`.

### Example

Server stores: `"2026-05-28 09:54:54"` (SQLite `CURRENT_TIMESTAMP`)
Zod schema: `createdAt: z.string()`
TypeScript type: `createdAt: string`
**Eden delivers**: `Date` object (`Thu May 28 2026 09:54:54 GMT+0530...`)

## How it breaks things

Any frontend code that calls `String(value)` or `localeCompare()` on a date field gets:
```
String(new Date("2026-05-28 09:54:54"))
// → "Thu May 28 2026 09:54:54 GMT+0530 (India Standard Time)"
```

Alphabetical sort on these strings groups by **day-of-week prefix** (Mon, Thu, Wed...) instead of chronologically. `localeCompare("Thu May 28...", "Wed May 27...")` returns negative → Thursday sorts before Wednesday → newest-first is broken.

## How to debug it

1. Check the raw API response with `fetch()` — dates appear as strings (server is correct)
2. Check the React Query cache via fiber traversal — dates appear as `Date` objects
3. The mismatch is Eden's transport-layer coercion

## The fix

Use numeric timestamp comparison with an `instanceof Date` guard:

```ts
// Safe date comparison for Eden Treaty responses
function toMs(raw: unknown): number {
  if (raw instanceof Date) return raw.getTime();
  return new Date(String(raw ?? "")).getTime() || 0;
}

// In sort:
cmp = toMs(a.createdAt) - toMs(b.createdAt);
```

The `instanceof Date` check is required because:
- TypeScript says `string` (it's wrong at runtime)
- `a.createdAt as unknown` is needed to satisfy the type checker for `instanceof`
- Fallback `new Date(String(...))` handles the case where it IS still a string

## Prevention

When writing any sort, filter, or comparison on `createdAt`/`updatedAt` fields in frontend code:
- **Never** use `String()` + `localeCompare()` or string `<`/`>` operators
- **Always** convert to numeric timestamps first
- This applies to any field that SQLite populates with `CURRENT_TIMESTAMP`
