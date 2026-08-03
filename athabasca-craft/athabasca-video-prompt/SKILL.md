---
name: athabasca-video-prompt
description: Write compact Athabasca video prompts for image-to-video and text-to-video generation, optimized for motion clarity, camera control, and reference-image consistency.
version: 1.1.0
---

# Athabasca Video Prompt

Use this skill when Athabasca needs a video prompt for text-to-video or image-to-video generation.

This is a prompt-authoring skill, not a provider/model routing skill. Do not encode provider/model permutations here. When actually generating video, use `athabasca-video-generation` and Athabasca's live capabilities endpoint for provider/model/settings selection.

This skill is based on practical prompt-writing heuristics. Treat it as creative guidance, not a formally verified vendor specification.

## Goal

Turn an Athabasca shot, still frame, or image reference into a production-ready video prompt that preserves identity, keeps motion simple, and avoids text overriding the visual reference.

## Core prompt assumptions

Most video models respond better when prompts are structured into five concrete blocks:

1. SUBJECT
2. ACTION
3. CAMERA
4. STYLE
5. QUALITY SUFFIX

The goal is not literary prose. The goal is controllable motion and stable visual intent.

Empirical performance notes:
- The model ignores roughly 80 percent of essay-style prompts.
- Slot one (`@Image1`) receives 40 to 50 percent more attention weight than any other reference slot.
- Multiple actions confuse the model — one verb per generation, no exceptions.
- Negative prompts are rejected by the model; always use positive framing.
- Individual face crops for reference produce far better identity consistency than turnaround grid sheets (which cause mosaic confusion — the model reads each panel as a separate character).

## Non-negotiable rules

- Use positive framing only.
- Do not use negative prompts.
- Prefer one clear action verb per generation.
- Do not stack multiple primary camera moves.
- For image-to-video, keep prompts short so text does not overwrite the reference image.
- For image-to-video, start with `@Image1 as the first frame.` when a reference image is present.
- When continuity matters, use the identity lock phrase exactly: `Same person as @Image1. Do not alter facial proportions, eye shape, or hairstyle.`
- In Athabasca workflows, preserve the approved shot identity, environment, palette, wardrobe, props, and artifact-specific intent already established upstream.

## Prompt length targets

### Text-to-video

Target 120 to 280 words.

- Below roughly 30 words: results become random.
- Above roughly 280 words: instructions are more likely to be dropped.

### Image-to-video

Target 50 to 80 words maximum. Hard cap at 80.

Reason: the reference image already carries identity, composition, wardrobe, and much of the visual language. The model splits attention between text and image — with a long prompt the text overwrites the visual reference and the character drifts from the frame you gave it. Less text means the source image stays dominant.

## The five-block structure

### 1) SUBJECT

Define:
- who or what is in frame
- wardrobe or physical appearance
- setting
- mood

Be specific and physical.

Good:
`A man in a dark wool coat stands at the edge of a rain-soaked rooftop, shoulders tense, jaw clenched, city lights scattered behind him.`

Guidance:
- Prefer concrete visual facts over backstory.
- Use wardrobe, posture, texture, environment, and emotional read.
- For image-to-video, keep this minimal or omit identity details already established by `@Image1`.
- In Athabasca, prefer the current approved shot context over broad exploratory lore.

### 2) ACTION

Use one motion only.

Good:
`He slowly turns to face the camera.`

Bad:
`He turns, walks forward, reaches out, and speaks.`

Rules:
- One verb per generation.
- Add a speed modifier when useful: slowly, gently, rapidly, hesitantly.
- If the scene needs multiple beats, split it into multiple generations.
- For shot continuity, choose the single most important beat already implied by the current shot record or reference frame.

### 3) CAMERA

Specify framing, movement, and lens feel.

Common movement terms:
- slow dolly push-in
- lateral tracking shot
- static locked-off frame
- slow pan left
- orbital movement around subject
- crane up
- handheld drift
- Steadicam follow
- POV shot

Common framing terms:
- extreme close-up
- medium shot waist up
- wide establishing
- over-the-shoulder
- low angle looking up
- high angle looking down

Rules:
- Use one primary camera move.
- At most one optional secondary camera modifier.
- Speed matters. `slowly` and `rapidly` produce meaningfully different results.
- If the source image already implies framing, reinforce it rather than fighting it.

### 4) STYLE

Use one aesthetic anchor plus lighting plus color or texture cues.

Avoid weak generic labels such as only `cinematic`. The model has seen ten million images tagged cinematic — it produces generic stock-footage output.

Prefer reinforced style pairs and material cues, for example:
- motivated warm lighting
- natural film grain
- shallow depth of field
- lifted blacks
- practical light sources visible in frame
- warm tungsten bounce
- volumetric dust particles
- negative fill

Lighting keywords ranked by empirically observed strength:
1. `motivated lighting` — strongest cinematic cue
2. `practical light sources visible in frame` — instant realism
3. `warm tungsten bounce` — intimate interiors
4. `volumetric dust particles` — atmospheric depth
5. `negative fill` — shapes faces with shadow and contrast

Film stock anchors that consistently hit:
- `Kodak Vision3 500T` — warm cinematic tones
- `ARRI Alexa color science` — high-end digital
- `35mm film grain` — indie texture

Guidance:
- Pick one primary aesthetic anchor.
- Then specify lighting and color behavior.
- Use details that materially affect image formation.
- In Athabasca, preserve phase-appropriate style and approved look-dev continuity instead of reinventing the visual language shot to shot.

### 5) QUALITY SUFFIX

Append this exact suffix unless there is a strong reason to override it:

`4K, Ultra HD, Rich details, Sharp clarity, Cinematic texture, Natural colors, Stable picture.`

## Reference-image guidance

Some providers support multiple image references, but behavior differs by model and should be governed by Athabasca capability metadata and adapter validation. As a prompt-writing default, assume the first image is the most important visual anchor.

### Priority rule

`@Image1` receives the most attention. Put the most important reference there.

### Character consistency

For stronger identity consistency across scenes, use:
- front view
- three-quarter view
- profile view

Use separate crops, not a multi-panel turnaround sheet.

Do not use grid sheets for identity reference. The model may interpret each panel as a different character.

### Image-to-video opening formula

Start with:
`@Image1 as the first frame.`

Then describe:
- the action
- environmental behavior
- camera behavior
- style reinforcement if needed

Do not re-describe the character heavily in text if the character is already visible in `@Image1`.

### Identity lock phrase

When the same character must persist across shots, add:

`Same person as @Image1. Do not alter facial proportions, eye shape, or hairstyle.`

## Athabasca-specific workflow guidance

Use this skill after reviewing the strongest available upstream evidence:
- current shot record
- current canonical still-generation prompt if one exists
- approved concept / visual-dev artifacts
- adjacent shot continuity
- any attached storyboard or still frame intended as the animation source

If you are instructing Hermes to actually generate the video, not just write the prompt, use `athabasca-video-generation` for routing/settings. In this prompt skill, only make sure the prompt assumes canonical Athabasca media where possible:
- source images should be persisted through Athabasca first if local or ephemeral
- prompts should refer to the approved source frame/reference rather than reinventing identity
- provider/model/settings should come from live capabilities, not this prompt document

Priority order when sources conflict:
1. current target shot intent
2. approved source frame or reference image
3. approved concept / look-dev guidance
4. adjacent shot continuity
5. broader exploratory notes

If a still is already approved, do not rewrite identity from scratch. Animate the approved frame.

For image-to-video in Athabasca:
- describe only the motion beat, environmental motion, and camera motion needed for this clip
- preserve the existing composition unless the task explicitly calls for reframing
- avoid lore, backstory, or broad scene re-description
- keep wording compact enough that the source image stays dominant
- if the source image is coming from a public URL, prefer an Athabasca-hosted `publicUrl` over a third-party site so providers can fetch it reliably

## Writing workflow

When authoring a video prompt:

1. Determine mode: text-to-video or image-to-video.
2. If image-to-video, identify what the reference image already establishes and avoid restating it.
3. Extract the single most important action beat.
4. Choose one primary camera move.
5. Choose one aesthetic anchor and 2 to 4 lighting/texture cues.
6. Add the quality suffix if appropriate for the target model/prompt style.
7. Trim aggressively.
8. Remove negatives and replace them with positive equivalents.

Routing, provider choice, model choice, duration, resolution, audio support, and reference-image field behavior are handled by `athabasca-video-generation` and Athabasca code/capabilities, not this prompt skill.

## Positive replacements

Prefer:
- `Stable picture` instead of `no shaking`
- `Sharp clarity` instead of `no blur`
- `Natural colors` instead of `not oversaturated`

## Output modes

### If the user asks for a final prompt only

Return only the prompt text.
No markdown.
No labels.
No commentary.

### If the user asks for help developing the prompt

You may provide:
- a short rationale
- 2 to 3 prompt variants
- a recommended final version

## Templates

### Text-to-video template

`[SUBJECT]. [ACTION]. [CAMERA]. [STYLE]. 4K, Ultra HD, Rich details, Sharp clarity, Cinematic texture, Natural colors, Stable picture.`

### Image-to-video template

`@Image1 as the first frame. [ACTION]. [CAMERA]. [STYLE]. Same person as @Image1. Do not alter facial proportions, eye shape, or hairstyle. 4K, Ultra HD, Rich details, Sharp clarity, Cinematic texture, Natural colors, Stable picture.`

## Example: text-to-video

`A woman in a structured black suit stands alone in a dim hotel hallway, one hand resting on a brass door handle, expression unreadable, warm practical sconces reflecting off polished wood panels. She slowly looks over her shoulder toward the camera. Slow dolly push-in, medium shot waist up, subtle lens compression. ARRI Alexa color science, motivated warm lighting, negative fill, soft film grain, lifted blacks, restrained amber and walnut palette. 4K, Ultra HD, Rich details, Sharp clarity, Cinematic texture, Natural colors, Stable picture.`

## Example: image-to-video

`@Image1 as the first frame. She slowly raises her gaze and turns her head slightly toward the window as sheer curtains move in a faint breeze. Slow dolly push-in, close medium framing. Kodak Vision3 500T, motivated morning window light, shallow depth of field, soft film grain, natural skin tones. Same person as @Image1. Do not alter facial proportions, eye shape, or hairstyle. 4K, Ultra HD, Rich details, Sharp clarity, Cinematic texture, Natural colors, Stable picture.`

## Failure modes

Common reasons prompts fail:
- too many actions in one clip
- too many camera instructions
- overlong image-to-video prompts
- re-describing character identity already established by the reference image
- generic style language with no lighting or texture cues
- use of negative prompting
- drifting away from the approved Athabasca source still or shot intent

## Decision rules

If forced to choose, prioritize in this order:
1. motion clarity
2. identity consistency
3. camera coherence
4. source-frame fidelity
5. style specificity
6. extra descriptive detail

## Pitfall: never fabricate prompts from summary docs

If you are given a link to an Athabasca-generated HTML prompt preview (e.g. a `project-slug/generated/project-slug-*.html` document containing lanes with `@image1`, `@image2`, timing blocks), **you must read the actual page content, not a summary**.

**What happened:** `web_extract` runs an LLM summarizer on large pages. For these HTML prompt docs, the summarizer collapses each lane's full prompt into high-level bullet points and **drops the actual prompt text**. If you trust the summary and improvise a prompt to fill the gap, you waste money on a generation that ignores the real beat structure, timing, and `@image2` references.

**Correct approach:**
1. Use `browser_navigate` to load the HTML doc and read the full prompt blocks from the page.
2. If `browser_navigate` is unavailable, ask the user to paste the actual prompt text.
3. **Never fabricate prompt content** — if the source is incomplete or missing, stop and ask. The cost of an honest "I don't have the prompt" is zero; the cost of a wrong generation is real money.

**Signals that a summary is incomplete:**
- Only high-level descriptions ("Focus: X", "Visuals: Y") with no actual timing blocks like `[0–4s] Begin on @image1`
- No `@image1`/`@image2` reference markers in the extracted text
- Only bullet points where the original document clearly has structured prompt blocks

## Manual multi-reference UI workflow

When working in manual UIs such as Mitte.ai or Replicate that support multiple `reference_images` addressed as `@image1`, `@image2`, etc., switch out of the stateless single-image mindset.

Key rule:
- never ask for a facial-performance beat unless the attached references include that face

If a lane asks for:
- a reaction close-up
- eyes shifting
- tears forming
- confusion arriving
- a smile changing

then attach both:
1. a character-sheet / face anchor for that person
2. at least one scene still with the right wardrobe, lighting, and environment

Recommended pattern for face-sensitive lanes:
- `@image1` = female lead character sheet
- `@image2` = male lead character sheet
- `@image3+` = scene stills for blocking / props / wardrobe / lighting continuity

Prefer multi-reference 15-second coverage lanes when:
- the lane needs both inserts and face reactions
- single-image i2v would force the model to invent a face from a hand-only or object-only reference
- the UI supports enough references to anchor identity and scene continuity together

Coverage matters more than chronology in this mode. Write longer lanes around editorial jobs such as:
- romance setup
- proposal + ring beauty
- reversal
- legal-document reveal
- reaction-processing
- final tableau
- insert / glue coverage

Reference: `references/seedance-multi-reference-manual-ui.md`

## Practical editing heuristic

When a prompt is not working:
- cut it by 20 to 40 percent
- remove all but one action
- keep one camera move
- strengthen lighting cues
- reduce character description if using `@Image1`
- compare against the approved source still and remove any text that tries to reinvent it
- if using manual multi-reference UI lanes, check first whether the lane is asking for a face beat without an attached face reference before rewriting the prose
