# Mockup review board pattern

Use this when a design session has accumulated several related mockups, references, or refinement passes and the user needs one artifact for comparison.

## Goal

Create a single review surface that helps the user judge:
- hierarchy
- legibility
- product realism
- consistency across desktop/mobile
- which variant should drive implementation

## Preferred output

A **self-contained HTML file** with:
- sectioned groups
- light labels only
- embedded images
- a short comparison rubric
- sticky section nav when the board is long

Prefer self-contained HTML over a chat-only recap when:
- there are many images
- the user wants to compare first-pass vs second-pass work
- the board may be opened away from the original runtime
- the source app/server may not be running later

## Recommended grouping

Good default sections:
1. reference inputs
2. native/generated first pass
3. tightened or second-pass variants
4. external polished exports
5. broader brainstorming set

## Portability rule

If the review file should survive outside the local runtime, **embed images as data URLs** instead of linking to server routes.

Why:
- local dev servers may be down later
- file:// previews cannot rely on same-origin app routes
- a self-contained artifact is easier to send, archive, or re-open months later

## Suggested card metadata

For each image card, include only concise evaluation aids:
- section/source group
- title
- variant label (first pass / tightened / second pass / export / reference)
- one short note explaining why it exists
- original vault path or source path

Avoid turning the board into a slide deck. The board is for judgment, not presentation theatrics.

## Suggested rubric block

A small rubric near the top works well. Typical prompts:
- Does import-first browsing feel obvious immediately?
- Is the file tree stronger than generic notes-app navigation?
- Does the reader stay calm, premium, and artifact-centric?
- Do desktop and mobile feel like the same product family?
- Which variants are beautiful **and** plausible enough to guide implementation?

## Pitfalls

### 1. Depending on live app asset routes
If the HTML points at localhost or app-specific asset endpoints, the board becomes fragile. Prefer embedded assets when portability matters.

### 2. Over-labeling the cards
Users usually want to judge the images, not read a deck. Keep metadata minimal.

### 3. Mixing unrelated explorations without sections
If multiple image families are present, group them explicitly so the board supports comparison rather than confusion.

### 4. Losing the refinement story
When there are first-pass and second-pass variants, keep both and label them. The tradeoff between beauty and realism is often the point.
