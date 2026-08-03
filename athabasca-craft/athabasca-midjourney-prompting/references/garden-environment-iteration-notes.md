# Environment-anchor overlock notes

Use this reference when an environment anchor preserves continuity but keeps forcing the image back into the wrong location.

## Pattern
The reference is technically helping, but it is helping the wrong thing: atmosphere and continuity survive while destination geometry does not.

## Response options
- run a clean text-only destination pass
- use a different environment anchor that shares mood but not layout
- route to Gemini or another model when spatial layout matters more than painterly continuity
- verify `aspectRatio` uses Athabasca's enum values (`landscape`, `portrait`, `square`) rather than raw `16:9` strings

## Rule of thumb
If the image feels emotionally right but physically wrong across multiple attempts, stop treating it as a prompt-tuning problem. It is usually an anchor-selection problem.
