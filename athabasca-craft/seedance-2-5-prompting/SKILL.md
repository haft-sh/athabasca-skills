---
name: seedance-2-5-prompting
description: Write Dreamina Seedance 2.5 prompts for multimodal references, long-form progression, editing, extension, audio, and precise timeline control.
version: 0.2.0
---

# Dreamina Seedance 2.5 Prompting

Use this skill when authoring creative prompts for Dreamina Seedance 2.5 through Athabasca. This is a model-specific craft skill: it describes how to express creative intent in Seedance 2.5's prompt language. It does not define Athabasca API routes, credentials, provider adapters, model IDs, or request validation.

## Source basis

This skill is based on two related public ByteDance/Feishu documents: the prompt-focused guide and the separate product/user guide.

- Wiki view: https://bytedance.larkoffice.com/wiki/NjnWwvf4BiFYFLk2RzrcEgaunGf
- Docx view: https://bytedance.larkoffice.com/docx/A88jd0B47oAd8zxWp5ycZFMfnxh

The product/user-guide capture is preserved in `references/user-guide-source-capture.md`. It records the user guide's function categories, extension and long-video behavior, timestamp control, language handling, audio/BGM operations, multimodal reference optimization, transfer, partial editing, perspective modification, tone and multi-person reference upgrades, green-screen editing, Clay Renderer, seamless transitions, and multi-grid storyboard guidance.

The Docx view is the prompt-focused “Dreamina Seedance 2.5 Prompt Guide,” last updated August 5. The Wiki view is the separate “【Dreamina】Seedance 2.5 User Guide,” modified August 4. Together they cover both prompt composition and product/function workflows. The prompt guide states that Seedance 2.5 supports text-only generation, image/video/audio references, and editing of existing videos. It presents prompting as a flexible natural-language combination of subject, action/event, environment, visual style, camera/cuts, and audio.

Operational capabilities mentioned in the guide include video extension/continuous creation, long videos up to 180 seconds in the product workflow, timestamp text control, multilingual prompting, removal of irrelevant subtitles and background music, base-generation effects, multimodal reference transfer, partial elimination/editing, space-perspective modification, tone-reference upgrading, and audio editing. Treat the live Athabasca capabilities endpoint and adapter code as authoritative for what is currently exposed through the API.

## Core prompt formula

Start with the generation goal, then add only the dimensions that matter:

`Subject + Action or Event + Scene and Environment + Visual Style + Camera Movement/Cut + Audio`

The guide treats environment, style, camera, and audio as optional extensions to the subject/action foundation. Use them when they materially control the result; do not add decorative boilerplate just to fill every slot.

### Basic template

`<Subject> performs <primary action or event> in <scene and environment>. The visuals feature <visual style>. Use <shot size, camera angle, camera movement, or cuts>. <Audio or dialogue direction>.`

### Practical ordering

1. State what is being generated.
2. Name the subject and the primary action or event.
3. Establish the environment and spatial relationships when they matter.
4. Define the visual treatment: lighting, color, materials, texture, and mood.
5. Define framing, camera movement, focus, and cuts.
6. Add dialogue, voice, ambience, effects, or music only when needed.
7. For longer or edited work, state the progression, preserved elements, and end state.

## Reference materials: roles before prose

Seedance 2.5 can use image, video, and audio references, but references should be assigned jobs explicitly. Do not attach a collection of assets and expect the model to infer which one controls identity, which one controls motion, and which one controls environment.

For every reference, define:

- identity or subject authority
- environment or spatial authority
- wardrobe and prop authority
- pose, composition, or framing authority
- motion or camera authority
- sound, rhythm, voice, or atmosphere authority
- whether the reference is to be preserved, transferred, combined, or merely used as inspiration

### Reference-role template

`Use @image1 as the identity and facial-proportion reference for Character A. Use @image2 as the environment and lighting reference. Use @video1 only for the camera movement and timing. Use @audio1 for the vocal rhythm and ambience. Preserve Character A's face and wardrobe from @image1 while transferring the spatial composition from @image2 into a new shot.`

### Material selection rules

- Use the minimum reference set that fully anchors the scene.
- Select references by scene, not by a global attachment habit.
- Group references by type when it helps the model: subjects, environments, props, motion, and audio.
- Create a centralized profile for important recurring subjects: identity, face, body proportions, wardrobe, signature props, and acting baseline.
- Reuse the profile across scenes, then add only the environment and shot-specific references required by the current scene.
- State conflicts explicitly. If a character sheet controls identity but the target scene has different clothing, say that the sheet controls identity and proportions, while the scene reference controls wardrobe and lighting.

### Multi-reference scene mapping

For a sequence with multiple characters, map each subject individually before describing the scene:

`Character A is the woman from @image1. Character B is the man from @image2. The room is from @image3. The red suitcase is from @image4. Use @video1 only for the handheld push-in. In the generated scene, Character A and Character B occupy the same room and interact with the suitcase.`

Do not write a bare list such as `References: @image1, @image2, @image3`. The model needs the semantic relationship.

## Subject and event clarity

The subject/action pair is the foundation. Use concrete visible behavior rather than dramatic shorthand.

Weak:

`The character experiences a major emotional reversal.`

Stronger:

`The woman smiles toward the doorway, then her smile stops as she notices the opened envelope in the man's hand.`

For a single short generation, lead with one dominant action. For a longer generation, describe a sequence of stages and end states rather than a pile of disconnected verbs.

## Long-form videos: stages and end states

For 30-second or longer work, organize events as a progression. The guide specifically recommends stages and end states.

Use this structure:

- **Start state:** what is already true in the opening frame
- **Stage 1:** first visible change
- **Stage 2:** consequence or escalation
- **Stage 3:** reversal, reveal, or transformation
- **End state:** the exact final pose, composition, object state, or title tableau

### Long-video template

`Start with [opening state and composition]. From [time] to [time], [stage 1]. Then [stage 2], causing [visible consequence]. From [time] to [time], [stage 3 or reveal]. End with [specific final state]. Preserve [identity, environment, prop, or palette] throughout. Use [camera progression], [visual treatment], and [audio progression].`

Do not describe a long video as a vague montage. State what changes and what must remain stable.

### Timestamp and pacing control

Use timestamp blocks when order, duration, or pacing matters:

`[00–05s] Establish the room and the character's starting pose.`

`[05–11s] The character crosses to the table and opens the case.`

`[11–18s] A red light sweeps across the room as the hidden object is revealed.`

`[18–24s] Hold on the character's reaction; the camera slowly pushes in.`

`[24–30s] Resolve on the object centered in frame, then cut to black.`

Timestamp language is an editorial control, not a substitute for describing the visible action. Keep each interval internally coherent and ensure the end of one interval creates the starting condition for the next.

## Extension and continuous creation

When extending a video, identify the source video and define the exact continuation point:

`Extend the attached video from its final frame. Preserve the character, wardrobe, lighting direction, camera axis, and screen direction. Continue with [new action]. Begin immediately from the existing end state and resolve on [new end state].`

Do not ask for an extension that silently resets the scene. State what must carry through:

- subject identity
- pose and body orientation
- environment geography
- light direction and color
- camera height and axis
- motion direction
- sound bed and transition point

When the extension is intended to be continuous, say `continue directly from the final frame` and describe the first new beat before describing later events.

## Editing existing video

For edit tasks, identify three things:

1. **Master video** — the video to edit
2. **Edit scope** — the exact time range, subject, object, background, audio, or visual property to change
3. **Content to preserve** — everything that must remain untouched

### General editing template

`Use @video1 as the master video. Edit only [time range / subject / region / property]. Replace or transform it into [desired result]. Preserve the original camera movement, timing, identity, lighting, background geography, sound, and all content outside the specified scope.`

### Subject replacement

`Use @video1 as the master video. Replace only the person in [time range] with the subject from @image1. Preserve the original pose, screen position, camera movement, background, lighting, timing, and audio. The replacement must follow the original motion and remain integrated with the scene.`

### Background replacement

`Use @video1 as the master video. Replace only the background behind the subject with the environment from @image1. Preserve the subject's identity, pose, wardrobe, edges, shadows, camera movement, timing, foreground objects, and audio.`

### Partial elimination or editing

Localize the edit aggressively:

`Remove only the blue sign in the upper-right background from 00:04 to 00:07. Reconstruct the wall and light behind it. Preserve the actor, camera movement, reflections, shadows, dialogue, and every other object.`

Do not say `clean up the scene` when only one element should change.

## Audio and special text syntax

Treat audio as a separate controllable layer. Specify:

- dialogue text exactly when the line matters
- language and accent when relevant
- voice age, gender presentation, delivery, emotion, pace, and loudness
- ambience and spatial distance
- sound effects and their synchronization points
- music presence, absence, genre, instrumentation, and energy
- whether existing audio should be preserved, removed, replaced, detached, or mixed

### Dialogue reinforcement

Quote important dialogue literally and reinforce its delivery:

`The woman says in Mandarin, quietly and without singing: “我知道你藏在哪里。” Her voice is close, breathy, and controlled. Keep the line synchronized to her visible mouth movement.`

For multilingual work, state the desired output language rather than relying on context. The guide highlights language-boundary handling; preserve exact dialogue and specify translation or language changes explicitly when requested.

### Audio editing examples

`Remove the background music from @video1 but preserve dialogue, room tone, footsteps, and sound effects.`

`Detach the dialogue track from @video1 and replace it with the supplied voice reference from @audio1. Preserve the original ambience and effects.`

`Keep the existing video and dialogue. Add a low distant train rumble and a single metallic impact exactly when the door closes.`

Never use a generic `make the audio cinematic` instruction when the real need is a precise stem or synchronization change.

## Visual style and camera language

Describe image formation, not only mood labels. Useful controls include:

- lighting direction and quality
- palette and contrast
- material and surface behavior
- texture such as film grain, halftone, ink, haze, or polished glass
- depth and spatial layers
- shot size and angle
- camera movement and acceleration
- focus subject and rack-focus timing
- cuts, wipes, match cuts, and transition behavior

Example:

`Low-angle medium-wide frame, 35mm lens feel, slow dolly forward through rain-streaked glass, the detective remains sharp while cyan city reflections slide across the foreground. Hard cut on the camera-shutter click to a centered red title card.`

For multi-shot work, define the sequence's visual system once, then specify the shot-level deviation or action. Avoid re-inventing palette and lighting in every timestamp block.

## Special capability patterns

### Reference transfer

State which quality is transferred and which qualities are preserved:

`Transfer the lighting rhythm and camera movement from @video1 to the character and room in @image1 and @image2. Preserve the character identity, wardrobe, and room geography from the images.`

### Space and perspective modification

Define the source space, the desired new viewpoint, and what must remain fixed:

`Use @image1 as the room layout authority. Re-render the same room from a high corner perspective looking toward the desk. Preserve the desk, window, shelf positions, light direction, and object scale; change only the camera viewpoint.`

### Tone reference upgrade

Use a tone reference as a controlled style input, not a request to copy content:

`Use @image1 as the story content and @image2 only as a tone and color reference. Preserve the subjects and composition from @image1 while adopting the restrained amber shadows, cool highlights, and quiet tension of @image2.`

### Base-generation effects

Describe the effect's source, behavior, timing, and interaction with the scene:

`A localized blue glow begins inside the device at 00:06, spills onto the character's hands, and fades as the device closes. The glow is a motivated light source with soft reflections on nearby metal; the rest of the scene remains naturally lit.`

Avoid effects that have no owner, timing, or physical consequence.

## Prompting rules for Athabasca

1. Inspect the current shot, approved stills, reference assets, and adjacent continuity before authoring.
2. Assign every reference a role and preserve the reference ordering expected by the dispatch surface.
3. Keep canonical identity, environment, palette, wardrobe, and props explicit.
4. For short clips, prioritize one dominant action and one camera idea.
5. For 30-second or longer work, use timestamped stages with explicit start and end states.
6. For extensions, start from the predecessor's final state and name every continuity anchor.
7. For edits, define the master video, narrow edit scope, and preservation set.
8. Quote exact dialogue and on-screen text when they matter.
9. Describe audio as dialogue, ambience, effects, music, or stem operations—not vague atmosphere.
10. Use positive, visible instructions. Replace vague negative lists with the desired treatment.
11. Keep model-facing copy dispatchable and stateless; do not rely on a broader script or prior conversation.
12. Use Athabasca's live capabilities and normalized generation skill for provider/model/settings selection. Do not hardcode undocumented Seedance 2.5 API fields here.

## Review checklist

- [ ] The generation goal is stated first.
- [ ] Subject and primary action/event are concrete.
- [ ] Each reference has an explicit role.
- [ ] Reference preservation versus transfer is unambiguous.
- [ ] Scene geography and end state are clear.
- [ ] Camera, focus, and cuts are specified when composition matters.
- [ ] Long videos have stages, timestamps, and a final state.
- [ ] Extensions state the continuation point and continuity anchors.
- [ ] Edits identify master video, edit scope, and preserved content.
- [ ] Dialogue is quoted exactly when required.
- [ ] Audio operations distinguish dialogue, ambience, effects, music, and removal/detachment.
- [ ] The prompt does not depend on hidden script context.
- [ ] API settings are left to Athabasca capabilities and generation routing.

## Common failure modes

**References are blended or assigned incorrectly** — map each subject and material individually, then select references by scene.

**Long video becomes a sequence of unrelated shots** — add timestamped stages, state transitions, and a specific end state.

**Extension resets the scene** — explicitly begin from the final frame and repeat camera axis, screen direction, lighting, geography, and identity anchors.

**Edit changes more than requested** — narrow the edit scope and enumerate the content to preserve.

**Dialogue is ignored or mispronounced** — quote the exact line, specify language and delivery, and tie it to visible mouth movement.

**Audio cleanup removes useful sound** — specify the exact stem to remove or replace and list the stems to preserve.

**Style transfer overwrites content** — say which reference controls tone and which reference controls identity, composition, and environment.

**Prompt is too abstract** — replace mood words with visible actions, spatial relationships, light behavior, camera instructions, and synchronized sound events.

## Related skills

- `athabasca-video-prompt` — general compact video prompt craft
- `athabasca-video-generation` — normalized Athabasca generation, capabilities, persistence, and verification
- `athabasca-seedance-prompt-docs` — HTML prompt packets, reference cards, grouping, and review artifacts
- `athabasca-visual-continuity` — recurring identity and visual continuity

## Source-capture reference

For the complete product/user-guide detail behind this skill, read `references/user-guide-source-capture.md`. Keep the main entrypoint focused on decision rules and use the reference for the one-time captured capability details and templates.
