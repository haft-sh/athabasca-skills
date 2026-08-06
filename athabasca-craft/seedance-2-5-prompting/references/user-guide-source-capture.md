# Seedance 2.5 Source Capture: User Guide Details

This reference records the separate product/user-guide material from the public document `【Dreamina】Seedance 2.5 User Guide`, modified August 4. It complements the prompt-focused guide captured in the parent skill.

Source: https://bytedance.larkoffice.com/wiki/NjnWwvf4BiFYFLk2RzrcEgaunGf

## Product positioning

The user guide presents Seedance 2.5 as a professional digital film set built around creator control and broader narrative space. It is the successor to Seedance 2.0's multimodal creation workflow and is intended to support longer, more authentic, more obedient generation and editing.

The guide directs users to the official Dreamina website for the released model experience:

https://dreamina.capcut.com/ai-tool/home

## Parameter and function categories

The guide organizes practical use around:

1. Parameter setting
2. Function interaction
3. Prompt-word suggestions

Prompt construction is not separated from function use: prompts should state the desired output and then provide the materials, event structure, edits, and controls needed by the selected function.

## Video extension and continuous creation

The user guide states:

- a single extension can support up to 30 seconds of extension generation;
- after generating a video within 30 seconds, the user can continue with multiple nested extensions;
- the highlighted maximum continuous result is 60 seconds in that extension workflow.

Prompting implication:

- identify the predecessor video explicitly;
- say to continue from the final frame or final state;
- preserve character, wardrobe, geography, camera axis, light direction, screen direction, and audio continuity;
- describe the first new action immediately after the continuation point;
- state the new end state;
- do not assume an extension will infer continuity from an asset attachment alone.

These product limits are distinct from the prompt guide's general discussion of long videos and from any current Athabasca API capabilities. Verify live limits before dispatch.

## Long videos

The user guide highlights an Ultra Long Video mode capable of generating up to 180 seconds. This should be treated as a product-mode capability, not a guarantee that every API route or model adapter exposes 180 seconds.

For an ultra-long prompt:

- define the global premise and visual system first;
- divide the narrative into timestamped chapters or stages;
- establish the state at the beginning and end of each stage;
- identify recurring subjects and props;
- restate continuity anchors at chapter boundaries;
- specify transitions and pacing changes;
- avoid treating a 180-second request as one unstructured paragraph.

## Timestamp text control

The user guide highlights timestamp-based control. Use literal timeline blocks when sequence order or duration matters:

`[00–08s] Establish the room and the character's starting position.`

`[08–16s] The character crosses to the desk, opens the drawer, and finds the envelope.`

`[16–24s] Hold on the reaction while the camera pushes in.`

`[24–30s] Resolve on the envelope centered in frame and cut to black.`

Each block should include concrete visible content, camera behavior, dialogue or sound when relevant, and the transition or state handed to the next block. Timestamp text should control pacing; it should not replace the action description.

## Language boundaries

The guide highlights breaking language boundaries. When language matters, state it explicitly:

- spoken language for each line;
- whether dialogue is translated, preserved, dubbed, or newly generated;
- accent or vocal quality;
- whether on-screen text remains in the source language or is replaced;
- whether the prompt itself may use a different language from the generated dialogue.

Quote critical dialogue exactly. Do not rely on a character name or a vague instruction such as “speak naturally.”

## Subtitle and background-music removal

The guide highlights removal of irrelevant subtitles and background music. Use scoped, positive editing language:

`Remove the burned-in subtitles from the lower third while preserving the actor's face, clothing, background, dialogue, ambience, and camera motion.`

`Remove only the background music. Preserve dialogue, room tone, footsteps, impacts, and environmental sound.`

If a clean plate or reconstruction is required, describe the visible replacement: wall texture, lighting, reflections, shadows, and motion continuity.

## Base-generation effects

The guide highlights optimization of base-generation effects. Prompt effects as motivated scene events:

- where the effect begins;
- what causes it;
- how it moves;
- what surfaces it illuminates or affects;
- when it fades or resolves;
- which subject remains the focal point.

Example:

`At 00:06, the device emits a localized blue pulse. The pulse reflects on the metal table and lights the character's hands, then fades as the device closes. Keep the rest of the room's warm practical lighting unchanged.`

## Multimodal reference optimization

The user guide highlights comprehensive multimodal reference optimization. Use all supplied reference types deliberately:

- image: identity, costume, environment, prop, composition, palette;
- video: movement, timing, acting, camera path, choreography;
- audio: voice, rhythm, ambience, music, sound effects, spatial character.

No reference should be left semantically unused. If a reference is attached but intentionally subordinate, state its narrow role rather than letting it compete with the primary authority.

## Background-music detachment and removal

Treat music as a separable audio layer when the task calls for it:

- detach music while retaining dialogue and effects;
- remove music while preserving ambience;
- replace music while retaining the original edit and other stems;
- add a new music bed without changing dialogue timing or visual pacing.

State exactly which audio elements are preserved and which are changed.

## Transfer Ideas

The user guide highlights “Transfer Ideas”: transfer a creative property from a reference while preserving the target content.

Specify the transferred property:

- lighting rhythm;
- camera movement;
- editing cadence;
- color treatment;
- staging idea;
- atmosphere;
- sound design;
- acting or gesture pattern.

Example:

`Transfer the slow lateral camera movement and cyan-red lighting rhythm from @video1 to the characters and room in @image1. Preserve the identities, wardrobe, and room geography from the image references.`

Do not say only “make it like @video1.”

## Partial elimination and editing

Localize the edit to one object, region, person, or time interval. Name what must be reconstructed and what must remain unchanged:

`From 00:04 to 00:07, remove the blue sign in the upper-right background and reconstruct the wall texture and shadow behind it. Preserve the actor, camera motion, reflections, dialogue, and every other object.`

The narrower the scope, the less likely the edit will rewrite unrelated content.

## Space-perspective modification

For viewpoint changes:

1. identify the layout authority;
2. name the new camera viewpoint;
3. preserve object positions, scale relationships, lighting direction, and geography;
4. change only the perspective unless additional changes are requested.

Example:

`Use @image1 as the room-layout authority. Re-render the same room from a high corner perspective aimed toward the desk. Preserve the window, shelf, desk, props, light direction, and object scale.`

## Tone-reference upgrade

Use a tone reference for mood, lighting, color, texture, or emotional register—not for literal content replacement:

`Use @image1 for the story content and @image2 only for tone. Preserve the subjects and composition from @image1 while adopting @image2's restrained amber shadows, cool highlights, and quiet tension.`

## Multi-person reference upgrade

When multiple people must appear together:

- map each person to a distinct reference;
- state which image controls each identity;
- define the spatial relationship and interaction;
- preserve wardrobe and proportions per person;
- state the camera and blocking so the model does not merge identities.

Example:

`Character A is the woman from @image1. Character B is the man from @image2. Place them together at the table from @image3. Character A stands on the left and Character B remains seated on the right. Preserve each face, hairstyle, wardrobe silhouette, and body proportion.`

## Green-screen editing

For green-screen or keyed-background workflows:

- identify the foreground subject or footage;
- identify the replacement environment;
- state whether the green background should be removed or used as a compositing cue;
- preserve subject edges, shadows, hair detail, motion, and lighting integration;
- describe the new background's perspective and light relationship.

Example:

`Use the actor from @video1 as the keyed foreground. Replace the green screen with the street environment from @image1. Preserve the actor's edges, hair movement, shadows, camera motion, and dialogue; match the street perspective and cool evening light to the actor.`

## Clay Renderer

The user guide highlights a professional Clay Renderer workflow and links a separate Clay Renderer Plugin User Guide. The described workflow connects Maya/Blender camera routes and white-model action/movement references to Dreamina for higher-quality rendering.

Prompting implications:

- treat the uploaded clay or white-model video as a motion/camera authority;
- specify whether the target is a material/style transformation or a faithful render;
- preserve camera path, timing, pose, blocking, and staging when those are the purpose of the reference;
- define the target material, lighting, environment, and character appearance separately;
- do not assume that a clay reference controls final character identity unless explicitly stated.

Example:

`Use @video1 as the Maya/Blender clay-animation authority for camera path, timing, blocking, and body motion. Render the same choreography as a finished cinematic scene with the character design from @image1, preserving the camera route and pose timing while replacing the clay material with wet painted ceramic and soft studio reflections.`

## Seamless video transitions

For transitions between clips, identify the outgoing clip, incoming clip, match anchor, and transition behavior:

`Extend from the final frame of @video1 into the opening composition of @video2. Match the character's hand position and left-to-right screen direction. Use a continuous camera move through the doorway; preserve the lighting direction and room geography across the transition.`

A transition prompt should state what is matched: pose, object, movement direction, camera axis, light, color, or sound.

## Multi-grid storyboard

A multi-grid storyboard can serve as a planning or visual-reference structure. Treat each panel as a named shot or scene role, not as an undifferentiated collage:

`The attached storyboard grid contains six panels. Panel 1 establishes the alley, Panel 2 controls the protagonist close-up, Panel 3 controls the hand insert, Panel 4 controls the pursuit camera, Panel 5 controls the title card, and Panel 6 controls the final tableau. Generate the sequence in that order with hard cuts between panels.`

If using a grid as a reference, state whether the model should preserve panel order, shot composition, character identity, or only the overall visual plan. For identity-critical references, prefer separate crops when possible.

## User-guide checklist

Before authoring a Seedance 2.5 prompt or packet, check:

- [ ] The selected product function is clear: generation, extension, long video, edit, transfer, perspective, green screen, Clay Renderer, transition, or storyboard.
- [ ] All image, video, and audio references have semantic roles.
- [ ] The prompt identifies the main subject and action/event.
- [ ] The timeline has explicit stages and end states when longer than a simple shot.
- [ ] Extension prompts name the predecessor final state and continuity anchors.
- [ ] Edit prompts identify master video, narrow edit scope, and preserved content.
- [ ] Language and dialogue behavior are explicit.
- [ ] Subtitles/BGM instructions are scoped to the intended layer.
- [ ] Effects have timing, cause, physical behavior, and resolution.
- [ ] Perspective changes preserve geography and scale unless intentionally changed.
- [ ] Multi-person references map identity one person at a time.
- [ ] Green-screen prompts address edges, shadows, perspective, and lighting.
- [ ] Clay references identify whether they control camera/motion or final appearance.
- [ ] Transition prompts identify the match anchor and screen direction.
- [ ] Multi-grid panels have named roles and ordered use.
- [ ] Live Athabasca capabilities are checked before choosing API settings.
