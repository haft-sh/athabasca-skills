---
name: cinematic-image-prompt-composition
description: Use when transforming a rough idea, image prompt, scene description, or uploaded image into 10 distinct cinematic image prompts focused on composition, camera angle, framing, blocking, depth, and visual storytelling.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [creative, image-prompts, cinematic-composition, visual-storytelling, prompting]
    related_skills: []
---

# Cinematic Image Prompt Composition

## Overview

Use this skill to turn any user input — a simple idea, rough image prompt, scene description, or uploaded image — into **10 distinct cinematic image prompts**. The emphasis is composition, camera angle, framing, blocking, depth, and visual storytelling.

The output should feel like film stills from real scenes, not posters, portraits, staged photoshoots, or generic concept art.

## Base Style

Preserve the user's requested style when they provide one. Otherwise default to:

> cinematic realism, film stock grain, film still

## Input Handling

- If the user gives a written idea, expand it into cinematic visual scenes.
- If the user gives a rough prompt, keep the subject and mood but improve the composition.
- If the user gives an image, analyze the subject, setting, mood, lighting, pose, and visual idea, then create 10 new prompt variations inspired by it.
- Do not copy an uploaded image literally unless the user asks for direct replication.
- Do not change the core subject unless the user asks for alternatives.

## Output Requirements

Give exactly **10 prompts**.

Each prompt must include:

1. A short title.
2. A camera/composition concept.
3. A full image prompt.

Each prompt should explore a different visual language. Useful options include:

- extreme low angle
- high angle
- overhead top-down
- over-the-shoulder
- foreground obstruction
- reflection shot
- silhouette shot
- frame-within-a-frame
- deep vanishing point
- wide negative space
- compressed telephoto distance
- handheld close perspective
- diagonal movement
- symmetrical blocking
- asymmetrical balance
- subject partially hidden
- environmental scale
- POV composition
- layered foreground/midground/background

## Prompt Writing Rules

Write each prompt as one clean paragraph.

Prioritize:

- composition
- lens choice
- camera height
- subject placement
- foreground, midground, background
- lighting
- atmosphere
- visual storytelling

Avoid:

- generic words like “epic,” “beautiful,” or “cool” unless supported by specific visual details
- black bars unless the user asks for them
- “in the style of” living directors or artists
- brand names unless the user provides them
- explaining the prompts unless asked

## Cinematic Quality Rules

Every prompt should feel like a captured moment from a real film scene. The scene should imply story, tension, movement, or emotion.

Use imperfect realism:

- grain
- haze
- motion blur
- soft focus falloff
- natural lighting
- practical light sources
- weather
- dust
- reflections
- shadows
- environmental texture

Prefer mid-action or emotionally charged moments over static posing. Make the camera feel intentional.

## Default Negative Add-on

At the end of each full prompt, append:

> no clean digital sharpness, no CGI look, no poster composition, no centered portrait, no black bars

## Output Format

```markdown
1. **Title**
   **Composition: [brief camera/composition idea]**

   Prompt:
   [full cinematic prompt]

---

2. **Title**
   **Composition: [brief camera/composition idea]**

   Prompt:
   [full cinematic prompt]

---

Continue until 10.
```

## Batch / Contact-Sheet Use

When the user wants these prompts used as a visual exploration set, treat the 10 prompts as candidates. It is acceptable to discard one to fit a 3x3 board when the user asks for a grid or contact sheet; discard the prompt least likely to survive generation cleanly or the one that overlaps most with another composition. Reflection-heavy prompts are often good conceptually but more failure-prone for character continuity, so they are a reasonable first discard when no stronger preference exists.

If assembling a review grid, label cells with compact prompt numbers and titles so the user can refer to candidates quickly.

## Common Pitfalls

1. **Making poster prompts instead of film stills.** Avoid centered hero poses, graphic poster layout, logo-like symmetry, and promotional framing.
2. **Only changing adjectives.** Each of the 10 prompts needs a distinct camera/composition strategy.
3. **Overwriting the user's subject.** Preserve the core idea unless alternatives are requested.
4. **Bloated prompt paragraphs.** Detail should serve the shot, not pad the prompt.
5. **Living-artist references.** Use concrete cinematic language instead of naming living directors or artists.

## References

- Source/adaptation note: `references/source-oak200-cinematic-composition-prompt.md`

## Verification Checklist

- [ ] Exactly 10 prompts
- [ ] Each prompt has title, composition concept, and full prompt
- [ ] Each composition is meaningfully distinct
- [ ] Base style is preserved or replaced only by user-supplied style
- [ ] Each prompt feels like a film still, not a poster or portrait
- [ ] Negative add-on appears at the end of each full prompt
