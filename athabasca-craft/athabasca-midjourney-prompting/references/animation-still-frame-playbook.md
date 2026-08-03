# Animation Still Frame Prompt Playbook

Use this reference when Midjourney prompts are intended to become storyboards, keyframes, starting frames for video generation, or Athabasca visual-development assets.

## Goal

A good animation still is not only beautiful. It is:

- readable at thumbnail size
- emotionally specific
- clear about camera, geography, and action
- stable enough to sit in a sequence
- useful as a starting frame for animation or image-to-video

## Prompt skeleton

```text
[character/subject] [single decisive action or pose], [location], [shot size], [camera angle], [composition/eye trace], [lighting], [color palette], [animation/rendering language], [continuity locks] --ar 16:9 --v 8.1 --s 180
```

## Strong still-frame language

- cinematic animation still
- storyboard-ready keyframe
- wide establishing frame
- clean readable silhouette
- medium shot, eye-level camera
- low-angle hero frame
- high-angle vulnerable frame
- over-the-shoulder composition
- foreground/midground/background depth
- strong diagonal composition
- clear eye trace to [focus]
- soft volumetric light
- warm rim light
- moonlit interior
- painterly background design
- production-ready environment concept
- gentle hand-painted texture

## Shot type prompts

### Establishing shot

```text
wide establishing animation still of [location], [important story detail], high three-quarter camera angle, strong foreground/midground/background depth, clear path for the viewer's eye, [time of day] lighting, [palette], production-ready background design --ar 16:9 --v 8.1 --s 220
```

### Emotional close-up

```text
close-up animation still of [character], [micro-expression], [small visible action], simple background shapes, shallow depth feeling, soft side light, clear readable eyes, emotionally intimate, [style] --ar 16:9 --v 8.1 --s 160
```

### Hero frame

```text
low-angle cinematic animation still of [character] [heroic action/pose], [environment], strong silhouette against [sky/light source], dramatic rim light, dynamic diagonal composition, mythic but emotionally grounded --ar 16:9 --v 8.1 --s 240
```

### Vulnerability frame

```text
high-angle cinematic animation still of [character] alone in [space], small figure surrounded by [environment], negative space emphasizing self-doubt, cool muted palette, soft atmospheric light, quiet emotional storytelling --ar 16:9 --v 8.1 --s 180
```

### Comedic beat

```text
medium-wide animation still of [character] caught in [funny clear situation], readable body language, simple staging, bright playful lighting, clean silhouette, background characters reacting, charming expressive timing --ar 16:9 --v 8.1 --s 220
```

## Continuity locks to include only when visible

- same costume / helmet / prop
- same time of day
- lighting direction
- weather state
- character screen direction
- location geography
- prop placement
- injury/dirt/wetness state
- distance relationship between characters

Example:

```text
the character walking left to right along the sideline, same oversized blue football helmet and scuffed shell, wet grass still glistening from morning mist, stadium lights behind him, medium-wide side profile composition, continuity with dawn football field sequence --ar 16:9 --v 8.1 --s 180
```

## What to avoid

- multi-action prompts: `he runs, jumps, falls, then smiles`
- vague film terms without visible details: `cinematic masterpiece`
- poster composition when you need a story frame
- mixing too many media styles
- overdescribing invisible backstory
- relying on `--no` instead of positive framing

## Prompt variant set for production

For any important shot, generate at least three variants:

1. **Safe production still** — most faithful to storyboard.
2. **Emotional push** — stronger expression/lighting/silhouette.
3. **Graphic composition** — stronger shape design or camera angle.

Optional fourth:

4. **Style-reference variant** — tuned for `--sref` and `--sw`.
