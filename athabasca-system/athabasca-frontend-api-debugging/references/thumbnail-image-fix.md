# ThumbnailImageById Fix — May 2026

## Bug
`ThumbnailImageById.tsx` called `/api/media-assets/${assetId}` — no such route existed.

## Root Cause
New component written against an assumed route path. Actual Athabasca detail endpoint is at `/api/media/:assetId` in `src/server/api/routes/system.ts`.

## Fix: 2 files

### 1. Fix URL — ThumbnailImageById.tsx
```typescript
// BEFORE
const response = await fetch(`/api/media-assets/${assetId}`);
// AFTER
const response = await fetch(`/api/media/${assetId}`);
```

### 2. Add import — App.tsx line ~15
```typescript
import { ThumbnailImageById } from "./components/ThumbnailImageById";
```

## Response Envelope
`/api/media/:assetId` returns `{ ok: true, asset }` — component correctly unwraps `data.asset`. No change needed there.

## Full Fixed Component
```typescript
import { useQuery } from "@tanstack/react-query";

interface ThumbnailImageByIdProps {
  assetId: string;
}

async function fetchAssetById(assetId: string) {
  const response = await fetch(`/api/media/${assetId}`);
  if (!response.ok) return null;
  const data = await response.json();
  return data.asset as { id: string; publicUrl: string; previewImageUrl: string | null } | null;
}

export function ThumbnailImageById({ assetId }: ThumbnailImageByIdProps) {
  const { data: asset } = useQuery({
    queryKey: ["asset", assetId],
    queryFn: () => fetchAssetById(assetId),
    staleTime: 5 * 60 * 1000,
  });

  const src = asset?.previewImageUrl ?? asset?.publicUrl ?? null;

  if (!src) {
    return (
      <div className="project-card-thumbnail-placeholder">
        <span className="material-symbols-outlined" style={{ fontSize: 40, opacity: 0.3 }}>movie</span>
      </div>
    );
  }

  return <img src={src} alt="" className="project-card-thumbnail-img" />;
}
```

## Used In
- `src/App.tsx` line 1512 — project card thumbnail for projects with `thumbnailAssetId`