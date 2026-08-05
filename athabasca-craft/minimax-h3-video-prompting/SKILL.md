---
name: minimax-h3-video-prompting
description: Write high-control MiniMax H3 prompts for multimodal video, native sound, multi-shot title sequences, and anime crime motion design.
version: 0.1.0
---

# MiniMax H3 Video Prompting

Use this skill when authoring creative prompts for MiniMax H3 video generation through Athabasca. This is a craft skill: it governs how to express visual intent, reference relationships, shot structure, sound, and motion-design logic in H3's natural-language style. It does not define API routes, provider credentials, model IDs, durations, resolutions, or validation rules.

## Source boundary

This skill is grounded in MiniMax's public H3 announcement and the supplied private Notion guide.

Verified H3 capabilities described publicly:
- unified context across text, images, video, and audio
- natural-language description of relationships between references and the target video
- text-to-video and generalized reference/editing workflows
- native stereo sound
- native multi-shot modeling
- up to 15 seconds and 2K output in the announcement
- in-context regeneration intended to preserve fine detail and text better than a detached upscaler

The supplied Notion page was not machine-readable in the authoring environment. Do not quote or present its private examples as verified specification unless the operator can provide the relevant page text or screenshots. The anime crime title-sequence guidance below is an original production translation of the requested visual direction, not a reproduction of the source example.

## Core premise

H3 should be prompted less like a conventional single-shot image-to-video model and more like a multimodal creative collaborator. State:

1. what each input reference is responsible for
2. how the references relate to one another
3. what should be generated from those relationships
4. the editorial structure of the sequence
5. the camera, motion, typography, and sound behavior
6. the desired visual finish

Do not merely attach images and hope the model infers their roles. Write the relationship explicitly.

## H3 prompt architecture

For a single shot, use this order:

1. **Reference contract** — identify each image, video, or audio reference and its role.
2. **Target frame and action** — state the dominant visible subject and one primary motion beat.
3. **Camera and layout** — specify framing, camera path, depth layers, and screen direction.
4. **Graphic system** — describe typography, symbols, wipes, linework, panels, or compositing behavior.
5. **Material and palette** — specify the anime rendering language, ink, halftone, paper, neon, metal, or other physical cues.
6. **Sound relationship** — describe diegetic sound, voice, ambience, impacts, and musical energy when audio is desired.
7. **Timing and transition** — state the beat progression and the transition into or out of the shot.
8. **Finish** — specify resolution/quality only when it belongs in the creative prompt; operational settings belong to the Athabasca request.

For a multi-shot prompt, begin with a sequence-level contract, then enumerate shots. H3 is designed for broader task generalization, but each shot must still have one dominant editorial job.

## Reference language

Use explicit relational sentences:

- `Use @Image1 as the character-design and silhouette authority.`
- `Use @Image2 as the rain-slick city palette and background architecture reference.`
- `Use @Video1 only for the lateral tracking movement and timing of the passing lights.`
- `Use @Audio1 as the rhythm and impact reference; generate new synchronized stereo sound rather than copying the source literally.`
- `Combine the character identity from @Image1 with the graphic crime-title language of @Image2, while preserving the camera movement from @Video1.`

Distinguish authority from inspiration. Say what must be preserved and what may be transformed:

`Preserve the face proportions, coat silhouette, and red scarf from @Image1. Translate the lighting, rain, and typography energy from @Image2 into a new composition.`

Do not use vague phrases such as `make it like the references`.

## Motion discipline

H3 may understand complex sequences, but controllability still improves when the prompt has a clear hierarchy:

- one dominant action per shot
- one primary camera move per shot
- one editorial transition per shot
- explicit screen direction when motion crosses cuts
- explicit speed changes: hold, creep, snap, whip, accelerate, decelerate
- describe the cause and consequence of graphic motion

Prefer:

`The detective's eye snaps toward the passing red neon reflection; the camera makes a short lateral track, then freezes for the title lock-up.`

Avoid:

`The detective walks, turns, fights, jumps across rooftops, and dissolves into smoke while the camera spins through the city.`

If the sequence genuinely requires many beats, divide them into numbered shots with approximate beat durations. Do not hide a storyboard inside one undifferentiated paragraph.

## Anime crime title sequence: creative grammar

Use this pattern for an opening-title or interstitial sequence with noir, manga, or anime-crime energy.

### Sequence identity

The sequence should feel like a designed title system, not random anime footage. Establish:

- a coherent recurring protagonist silhouette
- a limited palette, usually ink black plus one hot accent and one cool counter-color
- a repeatable graphic motif: dossier stamps, evidence lines, rain streaks, cigarette smoke, redacted bars, map grids, shell casings, train windows, surveillance frames, or fractured glass
- a consistent typography treatment
- editorial rhythm built from holds, snaps, hard cuts, graphic wipes, and brief impact frames

### Visual stack

Build each shot in layers:

1. **Subject layer** — face, hand, weapon silhouette, coat, eye, shoe, or object clue.
2. **Spatial layer** — alley, train carriage, interrogation room, rooftop, archive, or abstract void.
3. **Atmospheric layer** — rain, smoke, dust, light leaks, ink wash, halftone, chromatic bloom.
4. **Graphic layer** — title typography, case numbers, arrows, redaction bars, circles, diagrams, frame lines.
5. **Transition layer** — match cut, whip pan, ink spread, shutter, scanline, hard flash, or paper tear.

Tell H3 which layer is stable and which is animated. Example:

`Keep the character silhouette and title typography crisp and legible. Animate only the rain, drifting smoke, passing reflections, and a controlled lateral camera move.`

### Typography

When exact text matters, quote it exactly and define its placement, scale, orientation, and material behavior:

`The title reads exactly “NIGHT CASE” in condensed white uppercase lettering, aligned vertically along the right edge, briefly occluded by rain and then revealed by a red light sweep.`

Keep typography instructions short and isolated. Do not bury the exact string in decorative prose. If the model cannot reliably render the final title, generate a clean title-safe plate and composite type downstream rather than sacrificing the shot.

### Shot pattern

A strong 10–15 second title sequence can use this editorial skeleton:

- **Shot 1 — signal:** abstract clue or graphic mark establishes palette and sound pulse.
- **Shot 2 — reveal:** character fragment appears through reflection, smoke, or shadow.
- **Shot 3 — evidence:** prop or location clue receives a designed insert treatment.
- **Shot 4 — pursuit:** one directional camera move creates kinetic contrast.
- **Shot 5 — lock-up:** subject silhouette and title resolve into a readable graphic tableau.

This is a starting grammar, not a mandatory five-shot count. Use fewer shots when the target is a single coherent hero beat.

## Native audio prompting

Treat audio as part of the shot's physical design, not a generic soundtrack request. Specify relationships:

- `Rain is close and granular; distant traffic is low and diffuse.`
- `A dry camera-shutter click lands exactly on the graphic cut.`
- `The red title flash is accompanied by a short metallic impact and a brief low-frequency pulse.`
- `Footsteps remain screen-directionally consistent with the character moving left to right.`
- `Use restrained noir tension with sparse percussion and no vocals.`

When a supplied audio reference exists, say whether H3 should match rhythm, vocal character, timing, or only atmosphere. Do not ask for a perfect copy unless that is genuinely intended and permitted.

## Prompt templates

### Single-shot multimodal template

`Use @Image1 as the [identity/composition] authority and @Image2 as the [palette/environment/graphic] reference. Preserve [specific anchors] from @Image1 while transforming [specific elements] from @Image2 into a new shot. [Subject] performs [one dominant action]. [Camera move and framing]. [Atmosphere and graphic treatment]. [Typography, if any, quoted exactly]. [Sound relationship, if requested]. End on [transition or tableau].`

### Multi-shot title-sequence template

`Create a coherent anime crime opening-title sequence using the attached references as a shared visual system. @Image1 controls [character identity]. @Image2 controls [environment/palette]. @Video1 controls [motion reference]. @Audio1 controls [rhythm/sound relationship]. Preserve [continuity anchors] across every shot. Use a limited [palette] with recurring [graphic motif] and [typography system].

Shot 1 — [time/beat]: [single editorial job, subject, camera, graphic layer, sound, transition].
Shot 2 — [time/beat]: [single editorial job, subject, camera, graphic layer, sound, transition].
Shot 3 — [time/beat]: [single editorial job, subject, camera, graphic layer, sound, transition].
Resolve on [final title tableau].`

### Anime crime title-sequence starter

`Create a tightly designed anime crime title sequence from the attached references. @Image1 is the exact character-identity and silhouette authority; @Image2 is the rain-soaked city, palette, and graphic-design reference; @Video1 is a reference only for lateral tracking speed and passing-light rhythm. Preserve the protagonist's face proportions, dark coat silhouette, and red scarf across every shot. Use ink-black shadows, electric cyan reflections, and one controlled vermilion accent, with halftone texture, sharp cel shading, rain on glass, dossier lines, and redacted evidence bars as recurring motifs. Begin on a close insert of a rain-covered case file, snap to the protagonist's eye in a train-window reflection, track laterally past cyan-lit pillars, then hard-cut to a full silhouette beneath a vermilion title lock-up. Keep the graphic layers crisp and deliberately composed; animate rain, reflections, smoke, and camera movement with precise timing. The title reads exactly “NIGHT CASE” in condensed white uppercase lettering. Generate restrained native stereo noir sound: rain, train rumble, one camera-shutter click on the title cut, and a short metallic impact on the final lock-up.`

## Athabasca workflow

1. Inspect the shot or sequence intent, approved stills, character continuity, and any existing storyboard.
2. Decide whether this is one shot, a multi-shot H3 sequence, or a title-system exploration.
3. Inventory every reference and assign its authority explicitly.
4. Write the relationship between references and target output in natural language.
5. Separate sequence-level style rules from shot-level actions.
6. Keep each shot's action and camera move legible.
7. Add audio only when requested or creatively material; describe synchronization and spatial behavior.
8. Review typography separately; exact copy belongs in quotes.
9. Hand the resulting prompt to the Athabasca video-generation workflow for live model capabilities, settings, idempotency, persistence, and verification.
10. Do not encode provider API payloads or model limitations in the creative prompt skill.

## Quality checklist

Before dispatch, verify:

- Every reference has a named role.
- Preservation versus transformation is explicit.
- The main subject and dominant action appear early.
- Each shot has one primary camera move.
- Screen direction and transitions are clear.
- The anime/crime look is expressed through palette, material, lighting, and graphic systems rather than generic `cinematic` language.
- Typography is exact, short, and isolated.
- Audio is described as synchronized physical relationships, not just `epic music`.
- Character identity and recurring motifs remain stable across shots.
- The prompt does not pretend to guarantee exact text, perfect continuity, or a specific output setting.
- Operational settings are supplied through Athabasca's live capabilities and API path, not invented here.

## Failure modes and repairs

**References feel ignored** — restate each reference's role and the exact relationship to the target; put the highest-priority identity reference first.

**Sequence becomes generic anime footage** — define the graphic system, recurring motif, palette limits, title typography, and editorial transitions.

**Character drifts between shots** — repeat the concrete identity anchors at sequence level and preserve the same silhouette, wardrobe, and accent color.

**Motion is chaotic** — reduce each shot to one action, one camera move, and one transition.

**Typography is garbled** — shorten the title instruction, isolate the exact text, and consider a downstream compositing pass.

**Audio feels disconnected** — tie sound events to visible impacts, cuts, movement direction, and environmental distance.

**Prompt is too long** — remove lore and adjectives before removing reference roles, camera grammar, timing, or continuity anchors.

## Sources

- MiniMax H3 public announcement: https://www.minimax.io/blog/minimax-h3
- Supplied MiniMax H3 Notion guide: https://app.notion.com/p/MiniMax-H3-The-Next-Gen-Open-Weight-Multimodal-Generation-Model-3acbb3a8c3ae81618844cb0a3904e247
