# Seedance Prompt List Generator Pattern

Python script pattern for building a complete HTML prompt list from shot metadata.

## What It Does

1. Reads shot breakdowns from a local or cached source
2. Groups shots into logical batches for review and dispatch
3. Generates one complete HTML document with:
   - table of contents navigation
   - group sections
   - reference manifest
   - continuity table
4. Links to shared CSS or embeds a stable style block
5. Writes the result to a temporary local HTML file
6. Re-uploads or persists the final document through the Athabasca media/API workflow

## Core Patterns

**Shot grouping helper:**
```python
def shot_block(num, title, era, action): ...
```

**Group builder:**
```python
G.append(grp("A", "group-a", "Cold Open", '<span class="tag">Shots 001–014</span>', ...))
```

**Reference manifest:**
```python
manifest_rows = [
    (1, "Character identity anchor", "A, B, D", "Seedance", "primary face/wardrobe lock"),
    (2, "Environment anchor", "A, C, G", "Midjourney", "approved room baseline"),
]
```

**Assembly:**
```python
full_html = header + "\n".join(G) + "\n" + manifest_html + "\n" + cont_html + "\n" + footer
with open("/tmp/seedance-prompt-list.html", "w") as f:
    f.write(full_html)
```

## Modifying for New Shots

1. Edit or add to the shot-block list
2. Add or update group sections
3. Update the manifest and continuity table as needed
4. Re-run the generator script
5. Persist the refreshed HTML through the normal document/media path

## Live-Action Cinematic Style Language

When the intended output is live-action cinematic, use language such as:
- ARRI Alexa, anamorphic lenses, naturalistic lighting
- macro lens, wide-angle, handheld
- shallow depth of field
- hyper-realistic

## No "Anime Style" Rule

A composition skill may borrow anime storyboard logic, but that does **not** imply anime rendering style. If the target production is live action, do not use prompt language like:
- "anime-style"
- "anime aesthetic"
- "manga frame"

Instead translate composition language into cinematic equivalents such as:
- cinematic storyboard layout
- deadpan visual comedy framing
- editorial reaction coverage

## HTML Group Card Div Structure

Each group card should follow this structure:

```html
<div class="group-card" id="group-X">
  <div class="group-header">...</div>
  <p>... shot range text ...</p>
  <div class="note">...</div>
  <!-- INSERT REFERENCE CARDS HERE -->
  <h4>Seedance Prompt — Expanded</h4>
  <div class="seedance-prompt">...</div>
  <a href="#top">...</a>
</div>
```

**Critical:** When inserting reference image cards, place them after the note's closing `</div>` and before the `<h4>Seedance Prompt` heading. Match a pattern like:

```python
r'(</div>)\s*(<h4>Seedance Prompt — Expanded</h4>)'
```

Insert between the two capture groups. Do not consume the `</div>` itself or the note block will stay unclosed and nested group cards will collapse visually down the page.

## Anti-Bloat Rule

Do not turn this reference into a project-specific HTML dump. Keep the structural pattern here. Keep one production's full manifest, shot inventory, or generated HTML artifact somewhere else.