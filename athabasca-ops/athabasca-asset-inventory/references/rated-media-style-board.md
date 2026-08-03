# Rated media style-board pattern

Use this when the user asks for a side-by-side HTML board of selected/favorited images rather than a shot-breakdown inventory.

## Trigger examples

- "I have N upscaled images I like... rated 2 stars or above... put them in an HTML document"
- "make a style board / contact sheet / side-by-side review board"
- "show all rated images with no color tags"

## Pattern

1. Query project media through Athabasca APIs or repo DB helpers, not filesystem guesses.
2. Filter by the user's exact media semantics:
   - `kind === "image"`
   - `category === "generated"` unless they ask for references too
   - `ratingStars >= requested threshold`
   - `colorTag == null` when they say none have color tags
3. Verify the count matches the user-stated count. If it does not, report the mismatch and the filter used.
4. Build a responsive HTML grid/contact sheet with:
   - full thumbnail linked to the public URL
   - board index / rank
   - title
   - stars
   - prompt index/title and selected quadrant when present in metadata
   - asset id
5. Upload the HTML back to the project as generated media and attach it to the project.
6. Verify the returned `publicUrl` is HTTP 200 before giving the user the link.

## Layout guidance

Use a dark gallery/contact-sheet layout, not the shot-inventory table layout. A CSS grid with `repeat(auto-fill, minmax(360px, 1fr))` works well for side-by-side style comparison. Keep the page optimized for visual scanning; metadata should be compact and below each image.

## Common pitfall

Do not include all generated images when the user says "the ones I like" and defines a rating/color filter. Ratings/color tags are editorial state in Athabasca; trust them over recency or title naming.