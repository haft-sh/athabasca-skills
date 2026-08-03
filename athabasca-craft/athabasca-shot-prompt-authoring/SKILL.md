---
name: athabasca-shot-prompt-authoring
description: Author a canonical shot prompt from shot metadata using a repo-backed scaffold, continuity rules, and Nano Banana-aligned cinematography language.
version: 0.3.3
---

# Shot Prompt Authoring

Use this skill when a shot already exists in a shot list and you need to author or refresh the canonical image-generation prompt for that shot.

## Goal

Turn the shot record into a single final, canonical image-generation prompt that is ready to save via `POST /api/projects/:slug/shots/:shotId/prompt`.

`Final` here means the prompt should describe the intended deliverable frame itself, not brainstorm alternatives, not moodboard exploration, and not a loose bucket of possible ideas. The output should read like the best current production instruction for generating this exact shot.

This skill is intentionally generic: it should work for commercials, trailers, films, animation, concept frames, and storyboards without assuming a specific project or mythology.

## Required inputs

Read the current shot and adjacent context first.

Minimum fields to inspect:
- `frame`
- `action`
- `purpose`
- `notes`
- nearby shot continuity
- approved project concept / visual development guidance when available
- target medium or rendering style when known (storyboard, concept art, photoreal still, anime frame, painterly frame, etc.)
- any existing approved storyboard frame, prompt, look-dev image, styleframe, or reference still tied to this shot or adjacent beats

To find the final guidance rather than brainstorm material:
1. Start with the shot record itself (`frame`, `action`, `purpose`, `notes`).
2. Then look for the highest-confidence approved artifacts closest to the shot: locked storyboard frames, selected look-dev, approved concept art, continuity notes, prior saved prompts, adjacent canonical shots.
3. Treat exploratory ideation, discarded variants, and broad moodboard material as weak evidence unless the shot metadata explicitly points to them.
4. When sources conflict, prefer the most specific approved artifact nearest to the shot over earlier or broader ideation.
5. If no clear final guidance exists, write the best faithful prompt from the shot record and log the gap in `warnings` instead of pretending the direction is settled.

## Output contract

Return a JSON object only:

```json
{
  "prompt": "required final prompt string",
  "warnings": ["optional warning"],
  "referenceNotes": ["optional continuity or provenance note"]
}
```

Rules:
- `prompt` is required and must be a single polished final generation prompt.
- `prompt` should represent one best current instruction for the shot, not multiple options or exploratory variants.
- `warnings` is optional and should only be present when the shot metadata is ambiguous, contradictory, or missing key visual information.
- `referenceNotes` is optional and should capture continuity constraints, provenance reminders, or adjacent-shot links that explain why the prompt was written this way.

Important separation of concerns:
- `prompt` is only for image-visible instructions the model can actually render.
- `referenceNotes` is where you may record provenance, adjacent-shot rationale, editorial continuity logic, or why certain cues were preserved.
- Do not let internal evaluation language leak into `prompt`.

## Nano Banana-aligned prompt architecture

Default formula:
- `[Subject] + [Action] + [Setting/context] + [Composition/camera] + [Lighting/material/style] + [Critical continuity anchors] + [Short guardrails only if they prevent drift]`

Translate the shot into visible image instructions, not editorial commentary.

Preferred order inside `prompt`:
1. Name the primary subject early.
2. State the visible action in-frame.
3. Describe the environment and spatial relationships.
4. Specify framing, angle, lens feel, and composition.
5. Specify lighting, atmosphere, color behavior, and material texture.
6. State the target medium or visual finish.
7. Add only the continuity anchors that matter for this frame.
8. Add short positive guardrails, and only a few negative exclusions when failure risk is high.

Default enforcement for Athabasca shot prompts:
- Unless the shot metadata truly makes it impossible, every final prompt must include at least:
  - one concrete camera/framing cue (`wide shot`, `medium close-up`, `top-down`, `24mm wide-angle`, `85mm portrait lens`, `deep focus`, etc.)
  - one concrete spatial/staging cue (`vast negative space`, `layered foreground/midground/background`, `subject small but central`, `compressed profile against a flat wall of mist`, `symmetrical escort formation`, etc.)
- If exact focal length would be fake precision, use lens feel instead (`wide-angle lens`, `standard lens`, `telephoto compression`, `macro intimacy`).
- Do not omit camera/space language just because the rest of the prompt is already descriptive. In Athabasca, these cues are usually load-bearing.
- If the source material does not support a stronger lens choice, infer the weakest useful camera grammar from the shot itself and preserve that in `referenceNotes` if needed.

The prompt should sound like a production-ready still-generation instruction, not a screenplay paragraph and not a bag of keywords.

## What to remove from prompts

Do not include non-visual production commentary inside the image prompt unless it can be translated into something visible.

Usually remove or rewrite:
- `dramatic function`
- `duration feeling`
- editorial intent like `this should set up the next scene`
- lore dumps or backstory that do not change the frame
- repeated boilerplate in every shot when it does not help this specific image
- proper names, trademarked terms, and named places when descriptive visual language can do the job better

Bad:
- `Primary dramatic function: establish helplessness and isolation.`
- `Duration feeling: 4-5 seconds.`
- `A powerful teenage boy sinking through a deep river in a mythic epic scene.`

Better:
- `An exceptionally well-built teenage boy appears small and isolated in vast underwater negative space.`
- `An exceptionally well-built teenage boy sinks through a deep river, bare-chested in a short saffron dhoti with simple gold armlets, isolated in vast underwater negative space.`

Proper-name rule:
- Avoid proper names unless the name is visually indispensable and already approved as a continuity anchor.
- Default to descriptive identity cues instead: age, build, skin tone when relevant, hair, attire, props, role, and emotional bearing.
- Replace named rivers, cities, brands, and franchise terms with visible environmental description unless the exact name materially changes the frame.
- Treat proper names as a drift risk: they can add unwanted baggage, trigger policy filters, or cause the model to invent specifics you did not ask for.
- **i2v / Seedance prompt exception**: when authoring prompts for image-to-video generation (Seedance 2.0, etc.), always use "the man" and "the woman" instead of character names. Character names like "Adrian" or "Elena" provide no visual information to the video model and can trigger drift. Descriptive cues (wardrobe, posture, emotional state) are the only identity signals the model can actually use.

## Prompt-writing guidance distilled from the Nano Banana guides

Strong prompts usually do these things:
- stay concrete about subject, action, setting, and composition
- front-load the most important visual nouns and constraints
- use cinematic and photographic language when framing matters
- describe what should dominate the image instead of only saying what to avoid
- add material and texture cues when they matter to the look
- prefer descriptive subject language over proper names when the named identity is not visually essential
- use reference-image instructions explicitly when references exist
- keep prompts readable and efficient rather than overly literary
- preserve at least one explicit lens/focus cue and one explicit spatial-composition cue in the final prompt

Weak prompts usually do these things:
- bury the subject under abstract mood language
- include too much meta explanation instead of visual consequence
- repeat global style boilerplate in every shot
- use vague negatives like `not bad` / `not weird` / `not camp fantasy` without saying what should appear instead
- mention camera language vaguely (`cinematic`, `dynamic`) without concrete framing or lens cues
- describe costume, mood, and ornament richly while leaving the camera/space logic implicit

## Cinematography and composition language

When the shot data supports it, add concrete visual direction such as:
- framing: extreme wide shot, wide shot, full shot, medium shot, close-up, extreme close-up, over-the-shoulder
- camera angle: eye-level, low-angle, high-angle, top-down, worm's-eye, Dutch angle
- lens feel: 24mm wide-angle, 35mm, 50mm standard lens, 85mm portrait lens, macro lens, f/1.8 shallow depth of field
- focus / depth: shallow depth of field, deep focus, foreground blur, selective focus
- staging: centered composition, asymmetrical composition, strong silhouette, layered foreground/midground/background, negative space
- motion feel when relevant to a still: frozen mid-action, subtle motion blur, locked-off tableau, handheld immediacy
- lighting: golden hour backlight, silver surface light, three-point softbox setup, chiaroscuro, practical neon, rim light, volumetric haze, teal-magenta rim lighting
- finish: filmic contrast, muted teal grade, 1980s color film grain, clean commercial studio lighting
- materiality: oxidized gold, navy blue tweed, carved stone, wet silk, ceramic glaze, etched silver leaf, weathered leather

For Athabasca shot prompts, camera grammar is not optional decoration.

Rules:
- Every final prompt should contain at least one lens/focus cue and at least one space/staging cue unless the shot is genuinely too underspecified.
- If you must omit one of those, add a `warnings` entry explaining what is missing.
- Prefer simple concrete language over film-school jargon. `24mm wide-angle lens, deep vertical negative space` is better than `cinematic, dynamic, immersive`.
- When choosing between extra costume detail and missing camera grammar, keep the camera grammar.
- If the shot is a storyboard still, prefer readable spatial geometry over ornate adjective stacking.
- If the shot is already dense, cut redundant mood words before cutting lens/space cues.

## Positive framing and guardrails

Prefer positive constraints over long negative-prompt dumps.

Bad:
- `not horror-chaos, not camp fantasy, not ugly, not distorted`

Better:
- `ceremonial procession, calm expressions, symmetrical spacing, regal ornament, restrained body language`

Use explicit negatives only when the model is likely to drift into a common failure mode.
Examples:
- `no blood, no gore, no snarling, no attack pose`
- `no text`
- `no extra limbs`

## Reference-image instructions

When references exist, say so clearly in `referenceNotes` and, if helpful, in the prompt.

Preferred pattern:
- identify which reference governs what
- instruct the model to preserve composition, costume, palette, or subject identity
- say `translate` or `preserve`, not `copy`

Examples:
- `Preserve the costume silhouette and jewelry hierarchy from the approved look-dev frame.`
- `Use the storyboard frame as the composition anchor; preserve the low-angle descent and negative space.`
- `Translate the attached underwater lighting reference into this mythic setting without changing the character design.`

## Continuity rules

- Preserve character identity, wardrobe, props, environment, and time-of-day continuity across adjacent shots.
- Prefer canon from project research, concept route, look-dev, storyboards, or approved references over improvisation.
- If `notes` or neighboring shots imply a recurring visual motif, keep it stable in `referenceNotes` and reflect it in the prompt.
- Keep the prompt specific enough to generate the intended frame, but avoid overloading it with unrelated lore or backstory.
- When the metadata is underspecified, keep the prompt faithful to `purpose` and log the gap in `warnings` instead of inventing major story facts.
- If a prior still, storyboard frame, or reference image exists, treat it as a continuity anchor and mention the preserved traits in `referenceNotes`.

Continuity must be translated into visible cues.

Do not write abstract continuity language inside `prompt`, for example:
- `preserving continuity with the preceding wide descent shot`
- `matching the ceremonial descent tone`
- `maintaining adjacent-shot logic`
- `consistent with the previous frame`

Those are useful internal judgments for Hermes, but mostly meaningless to the image model unless translated into explicit visual instructions.

Instead, convert continuity into concrete visible constraints such as:
- repeated framing geometry
- the same costume silhouette
- the same jewelry hierarchy
- the same palette or lighting behavior
- the same blocking direction
- the same body orientation or motion state
- the same environmental density, negative space, or camera height

Good:
- `wide underwater frame with the boy small in vast vertical negative space, silver surface light above, the same red-orange dhoti and simple gold armlets`

Bad:
- `preserving continuity with the previous shot`

## Authoring heuristics

- Default to one dense but readable paragraph for `prompt`.
- Name the primary subject early.
- Put the most decision-critical visual constraints near the front.
- Lock the image grammar before polishing the prose: shot size, angle, lens/focus, and spatial staging should be decided before texture adjectives multiply.
- If a draft lacks an explicit lens/focus cue or an explicit space/staging cue, it is not done.
- Prefer one decisive camera choice over multiple alternatives. Avoid `frontal or slight top-down`, `four to six attendants`, `wide or medium-wide` unless the ambiguity is intentional and unavoidable.
- When the composition depends on scale relationships, state them plainly: `small in frame`, `subject centered within vast negative space`, `foreground silhouette framing`, `stacked depth columns`, `tight profile crop`.
- Write the shot that should be generated now, not alternative possibilities you considered along the way.
- If sources include both exploratory and approved material, absorb the exploratory material only insofar as it helps interpret the approved direction; do not let it override the final shot intent.
- If the shot is for a storyboard, prefer readable staging and action clarity over hyper-detailed surface texture.
- If the shot is for concept art or key art, lean harder into lighting, atmosphere, material detail, and composition.
- If exact text must appear in-frame, quote it exactly and mention typography only when important.
- If an aspect ratio is known and materially important to composition, include it.
- If 2K/4K output or a delivery format matters, keep that in workflow notes or request metadata unless it materially affects the visual design.
- Strip any sentence fragment that only tells Hermes how to judge continuity unless it has been rewritten as a visible frame instruction.

### i2v / Seedance prompt constraints

When authoring prompts for image-to-video generation (Seedance 2.0 on fal.ai specifically):

- **Short granular takes**: 4–8s per prompt, not 15s. Each prompt should describe one coherent shot/movement, not a chain of cuts or beats. Seedance struggles with long multi-beat prompts and will drift or ignore later beats.
- **Single reference image**: each generation references exactly one still. If the sequence needs multiple shots, split into separate lanes.
- **Quality suffix**: append `4K, Ultra HD, Rich details, Sharp clarity, Cinematic texture, Natural colors, Stable picture No Music` to the end of every Seedance prompt.
- **Duration tags optional**: `[0–5s]` prefix tags are fine for human readability but Seedance ignores them — the `duration` API parameter controls actual length.

### Seedance group prompt preamble format

When authoring a multi-shot group prompt for Seedance (as used in storyboard generation workflows), begin the prompt block with a declarative preamble that assigns reference images to scene roles before listing individual shots:

```
I want you to generate the following scenes for our live-action cinematic satirical comedy film.

The setting is the spartan writing room in @image2. Character: @image1. Typewriter: @image3. Manuscript stack: @image4.
14 shots. Duration per shot: ~1.1s. Transition: hard cuts between all shots.

Shot 1 — [Title]
[shot detail...]
```

**Key rules:**
- The preamble must assign each `@imageN` to a **role** (setting, character, prop) — a bare list of IDs without role assignment is insufficient
- Each role assignment includes a brief descriptive phrase in brackets (e.g., `@image2 [spartan writing room]`)
- Shot count and duration are explicit in the preamble line
- Transition type (hard cuts, crossfade, etc.) is stated
- For live-action cinematic style, explicitly say "live-action cinematic" not "anime" or "anime-style"

### Verbose/direct shot format for Seedance groups

When the full group prompt document is being built (not just a single shot prompt), use the **expanded verbose format** per shot:

```
Shot 003 — Title
Frame: description of what fills the frame.
Camera: angle, position, perspective.
Composition: subject placement, foreground/midground/background layers.
Lighting: quality, direction, color.
Focus: what is sharpest.
Emotion: the dramatic read.
Prompt core: <blockquote>generation-ready prompt text</blockquote>
```

The `prompt core` block is what gets sent to the model; the metadata fields above it are structural context for human review and copy-paste. This verbose format yields better results because every visual dimension is explicitly anchored.

### Shot numbering for stateless Seedance dispatch

When generating the aggregate prompt document, **each group starts at Shot 001**. Seedance is stateless and only sees the current group's prompt. Global shot numbers (001–161) appear in group headers for human reference, but internal `Shot NNN` labels are local to each group.

## Good and bad examples

### Example 1: replacing meta commentary with visible instructions

Bad:
- `A cinematic still frame from a mythic epic. Primary dramatic function: establish helplessness and isolation. Duration feeling: 4-5 seconds. The boy is underwater.`

Better:
- `An exceptionally well-built teenage boy sinks vertically through deep blue-black river water, wrists and ankles bound with reeds, his body small in a wide underwater frame with vast negative space around him, silver shafts of surface light above, drifting particles, somber mythic tone, 24mm wide-angle lens, volumetric haze, realistic anatomy, no gore, no text.`

Why it is better:
- the subject appears immediately
- the emotion is translated into visible scale and negative space
- camera and lighting are concrete
- no useless still-image commentary remains

### Example 2: replacing vague negatives with positive staging

Bad:
- `Serpentine attendants around the bound boy, not horror-chaos, not camp fantasy, sacred dread.`

Better:
- `Ceremonial naga escort surrounding the bound boy in calm symmetrical formation, priestess centered at the apex, restrained expressions, regal ornament, ordered spacing, jewel-lit darkness, solemn underwater procession.`

Why it is better:
- it tells the model what to draw, not just what to avoid
- abstract tone is converted into staging and body language

### Example 2b: replacing meta continuity language with visible continuity

Bad:
- `Close underwater shot preserving continuity with the preceding wide descent shot and the ceremonial descent tone.`

Better:
- `Close underwater shot of the same bound teenage boy descending head-up through dark blue-black water, keeping the same silver surface light, sparse drifting particles, solemn expression, and restrained red-orange cloth and simple gold armlets established in the wider descent image.`

Why it is better:
- it converts continuity into actual renderable cues
- it does not assume the model knows what `preceding shot` means
- it preserves the relevant palette, costume, lighting, and emotional staging directly in-frame

### Example 3: bite/attack-shot failure prevention

Bad:
- `Extreme close shot of the snake bite, ordained transformation, not gore.`

Better:
- `Extreme close-up of the boy's shoulder as a ceremonial serpent bite approaches, fangs just at the edge of contact, calm controlled motion, sacred ritual tension, soft gleam on scales, jewel-lit darkness, realistic skin and scale texture, no blood, no gore, no snarling, no attack pose, no text.`

Why it is better:
- the frame is specific
- the failure modes are named only where needed
- the ritual tone is preserved through visible cues

### Example 4: replacing proper names with visual identity

Bad:
- `A powerful teenage boy sinks through a deep river in restrained mythic illustrated-epic visual language.`

Better:
- `An exceptionally well-built teenage boy sinks through a deep river, bare-chested in a short red-orange dhoti with simple gold armlets and a modest necklace, rendered in restrained mythic Indian epic visual language with clear comic-to-cinematic costume readability.`

Why it is better:
- it keeps the visually useful body and costume information
- it removes names that can trigger drift, policy friction, or unasked-for iconography
- it gives the model concrete appearance cues instead of relying on lore recognition

## Pre-save checklist

Before returning the JSON object, verify:

1. Subject first
- Is the main subject named in the opening phrase?

2. Visible action
- Does the prompt describe what is happening in the frame right now?

3. Concrete setting
- Can a model clearly place the subject in an environment?

4. Cinematic control
- Did you specify framing and angle?
- Did you include at least one concrete lens/focus cue?
- Did you include at least one concrete space/staging cue?
- If not, the prompt is incomplete unless `warnings` explains why.

5. Lighting and materiality
- Did you include the most important lighting and texture cues?

6. Continuity
- Does the prompt preserve approved costume, props, environment, palette, and blocking through explicit visible cues rather than meta continuity language?

7. Positive framing
- Did you describe what should dominate the image instead of relying on vague negatives?

8. Drift prevention
- If the shot has a known failure mode, did you add a short precise guardrail?

9. Proper-name discipline
- Did you remove proper names unless they are truly required for continuity or visual specificity?

10. No meta clutter
- Did you remove dramatic-function notes, duration notes, and non-visual editorial commentary?

11. Readability
- Is the prompt one clean, production-ready instruction rather than a bloated paragraph?

If the answer to any of 1-7 is no, revise before saving.

## Save workflow

After authoring:
1. Return the JSON object above.
2. Save `prompt` as `latestPrompt` through the canonical API.
3. Set `promptContextVersion` from the current shot when saving.
4. Treat the saved result as the manual canonical prompt.
