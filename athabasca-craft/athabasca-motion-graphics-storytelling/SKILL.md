---
name: athabasca-motion-graphics-storytelling
description: Use when designing or critiquing motion graphics for Athabasca explainers, documentaries, maps, data stories, or educational videos. Focuses on directing the eye, narrative staging, shot-by-shot visual hierarchy, and editorial-grade motion rather than decorative animation.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [athabasca, motion-graphics, explainer-videos, documentary, visual-storytelling, animation]
    related_skills: [hyperframes, manim-video, design-md, athabasca-anime-layout-master]
---

# Athabasca Motion Graphics Storytelling

## Overview

This skill is for **professional-grade motion graphics direction**, especially for YouTube explainers, documentary inserts, maps, timelines, annotated diagrams, data stories, and educational sequences used in Athabasca projects.

The core idea: **motion graphics are not animated slides**. They are editorial storytelling in time. Every frame needs a focal point, every beat needs a visual question, and every movement must help the audience understand *what to look at, in what order, and why it matters now*.

If a composition has labels in every corner, persistent competing captions, or simultaneous motion across multiple unrelated regions, it will feel like a moving infographic instead of a directed sequence.

## When to Use

Use this skill when:
- Designing a motion-graphics sequence from script or research
- Converting an infographic, map, chart, or storyboard into animation
- Building YouTube explainer or documentary visuals
- Critiquing why a piece feels flat, cluttered, static, or confusing
- Planning layout/animation before using HyperFrames, After Effects, Manim, SVG, or HTML/CSS
- The user wants the piece to feel cinematic, intentional, or editorial rather than merely informational

Do **not** use this skill for:
- Pure software setup or renderer-specific CLI usage (load `hyperframes`, `manim-video`, etc.)
- Character acting animation as the primary problem
- Static infographic design with no temporal storytelling

## Non-Negotiable Principles

### 1. One focal point per beat
At any meaningful instant, the viewer should know the **primary thing to look at** within about half a second.

Bad signs:
- Captions in multiple corners
- Two or more equally loud callouts
- Simultaneous motion in unrelated regions
- Full-screen persistent labels plus animated center action

Rules:
- Declare a single focal subject for each beat
- Secondary information must either wait, dim, or remain visually subordinate
- Use scale, contrast, isolation, blur, masking, or motion to force priority

### 2. Motion must reveal thought, not decorate layout
Animation should answer one of these:
- What changed?
- Where should I look next?
- How are these two things connected?
- What is the causal sequence?
- What should I compare?

If motion does none of that, cut it.

### 3. Stage information over time
Do not place all information on screen at once and then wiggle it.

Preferred pattern:
1. establish context
2. isolate the subject
3. reveal the change or path
4. annotate only what is now relevant
5. transition or clear space before the next idea

### 4. Design for eye flow, not just frame beauty
A beautiful frame can still fail in motion if the eye has no path.

Use:
- directional motion
- gaze cues
- arrows/lines that emerge in sequence
- progressive disclosure
- lighting/contrast emphasis
- camera reframing or crop changes

### 5. Editorial integrity beats slickness
For documentary and explainer work, avoid ad-like polish when it reduces trust or obscures seriousness.
Style should support tone, accuracy, and comprehension.

## The Motion Graphics Narrative Ladder

For each sequence, define these before animating:

1. **Claim** — what is this beat trying to teach?
2. **Visual proof** — what concrete image/map/chart/object demonstrates it?
3. **Focal path** — where should the eye go first, second, third?
4. **Transform** — what is moving/changing/revealing?
5. **Exit condition** — what leaves or quiets down before the next beat?

If you cannot answer all five, the beat is underdesigned.

## The 7-Step Workflow

### 1. Extract visual beats from the script
Convert the script into a beat list. Each beat should be one idea only.

Template:
- Beat ID
- Narration line
- Viewer takeaway
- Visual evidence
- Focal point
- Motion verb: reveal / compare / trace / count / split / zoom / morph / label / orbit / isolate
- Exit strategy

If one narration sentence implies two separate visual tasks, split the beat.

### 2. Decide the visual grammar
Pick a dominant grammar for the sequence:
- **Map/path** — migration, spread, routes, fronts, diffusion
- **Cutaway diagram** — anatomy, machinery, layered systems
- **Timeline** — historical progression, branching lineage
- **Comparison frame** — before/after, species A vs species B
- **Build-up composition** — complex idea assembled piece by piece
- **Editorial collage** — many-source documentary montage

Do not mix grammars casually in one short beat.

### 3. Compose the hero frame for each beat
Before animation, design the frame at peak information density.

Checklist:
- one dominant region
- clear reading order
- enough negative space around the main subject
- no corner text fighting center action
- labels close to the thing they label
- text short enough to read in one glance

### 4. Assign motion roles
Every animated element must have one role:
- **Anchor** — stable context, like a map base or frame
- **Guide** — directs attention, like a path, spotlight, underline, crop, or arrow
- **Evidence** — the actual content being explained
- **Annotation** — text or icon that names/clarifies
- **Transition** — clears the stage or reframes the next idea

Too many simultaneous guides or annotations means the scene is over-directed.

### 5. Sequence the reveal
Default ordering:
1. anchor/context
2. focal subject
3. transformation/path
4. annotation
5. implication or comparison
6. clear/reset

This is why many weak explainers feel static: they start at step 4 and never truly perform steps 2-3.

### 6. Control pacing like an editor
Use timing to signal seriousness and comprehension load.

Heuristics:
- Give the audience a beat to recognize context before changing it
- Slow down at conceptually dense moments
- Speed up through obvious connective tissue
- Stagger text and graphics instead of entering together
- Let important states settle long enough to be understood

A common failure mode is constant medium-speed motion everywhere. It feels busy but not directed.

### 7. Cut visual noise aggressively
Before rendering, ask of every element:
- Is it teaching?
- Is it guiding?
- Is it setting tone?
- Is it necessary for continuity?

If not, remove it.

## Documentary / Explainer-Specific Patterns

### Maps
- Keep the base map quiet; the route is the star
- Prefer a **clean base plate** with no baked arrows, route cues, beaver mascots, legends, or pre-solved explanatory furniture when you intend to animate the logic yourself
- If the supplied art already contains arrows or route marks, either regenerate / repaint a quiet plate or make those baked cues the only route language; do **not** layer a second contradictory path system on top
- Reveal routes progressively, not all at once
- Label only the currently relevant regions
- Use push-in / crop / spotlight to localize attention
- When showing a corridor like Beringia, isolate it visually before discussing consequences
- Route graphics must hug the geography they claim to represent. If the line reads like an airline arc over open water instead of terrestrial movement, redesign it or remove it
- For sea-level stories, strongly consider a **paired base-plate transform**: low-water plate first, then a matching high-water plate after the closure event. Let coastline change do explanatory work instead of piling on arrows and text
- If discussing a split, first show connection, then closure, then resulting divergence
- Treat the **corridor event** as the focal beat; species labels and summary text should arrive only after the closure/opening itself reads clearly
- If you need more than one major caption box plus two labels to explain a single map beat, the beat is probably overloaded and should be split into multiple shots

See `references/map-explainer-patterns.md` for practical map-beat structures.

### Data stories
- One comparison at a time
- Use a strong takeaway headline, not generic labels
- If an artistic hook is used, follow with an analytical view that cashes out the claim
- Avoid charts that need a paragraph of explanation before they make sense

### Diagrams / anatomy / systems
- Reveal from large structure to specific mechanism
- Highlight only one subsystem at once
- Use translucency/masking to simplify the field
- Keep terminology adjacent to the highlighted part

### Timelines / evolutionary stories
- Show lineage as a directed path, not a dense tree dump
- Collapse less relevant branches
- Use spacing to imply time and separation
- Bring traits in when they arise; do not frontload all derived features

## Layout Rules That Prevent “Animated Infographic” Syndrome

- Never keep four active text blocks on screen unless the entire purpose is comparison
- Avoid persistent title + persistent legend + persistent caption + persistent labels all competing simultaneously
- Prefer **one active caption zone** per beat
- Put text near the evidence whenever possible
- Use full-screen text only for transitions, chaptering, or singular takeaways
- If the eye has to travel diagonally across the screen multiple times to understand a beat, redesign it

## Motion Heuristics

### Good movement often looks like:
- reveal
- trace
- peel back
- focus pull
- push in
- pin / lock onto a subject
- handoff from one element to the next
- delayed secondary motion
- clear settle after arrival

### Weak movement often looks like:
- every element fading in together
- perpetual drifting for “energy”
- decorative parallax with no narrative role
- shape morphs unrelated to the idea
- looping motion under dense reading tasks

## Tone and Materiality

Match the motion language to the subject:
- science education: precise, legible, curiosity-forward
- documentary tragedy: restrained, respectful, unsentimental
- playful natural history: tactile, warm, illustrative, but still disciplined
- technical explainer: cleaner timing, less flourish, stronger hierarchy

The more serious or evidence-heavy the subject, the more restraint you usually want.

## Critique Rubric

When reviewing a sequence, score each 1-5:
- focal clarity
- reading order
- narrative progression
- relevance of motion
- density control
- tonal fit
- information retention
- transition quality

If focal clarity or reading order scores below 4, redesign before polishing.

## Red Flags

- “Looks nice as a still, but confusing in motion”
- “Everything is moving”
- “Nothing is moving but labels keep appearing”
- “I don’t know where to look”
- “The captions explain the scene, but the scene itself doesn’t”
- “The map/chart is there, but the actual argument is not visually staged”
- **Four-corner trap:** active explanatory text in multiple corners while the main action happens elsewhere
- **Moving infographic syndrome:** a static information layout with minor decorative animation rather than a directed sequence

## One-Shot Repair Recipes

### If the scene feels static
- Reduce persistent text
- Add a guided reveal of the key evidence
- Reframe or zoom to create sequence
- Turn labels into timed callouts rather than always-on furniture

### If the scene feels cluttered
- Pick one caption zone
- Remove half the labels
- Dim or crop background context
- Break one beat into two shorter beats

### If the eye has no path
- Add a dominant motion cue
- Sequence reveals instead of simultaneous entry
- Increase contrast on the subject, reduce on everything else
- Use one directional gesture: left→right, center→edge, zoom-in, or trace-along-path

### If it feels like a slideshow
- Replace generic fades with causal movement
- Animate the relationship, not just the objects
- Use transitions that perform a narrative handoff
- Let the next shot inherit position, direction, or shape from the previous one

## Verification Checklist

- [ ] Every beat has exactly one declared focal point
- [ ] The eye path is intentional and describable in one sentence
- [ ] Text is localized to the evidence or limited to one active caption area
- [ ] Motion reveals causality/comparison/change rather than decorating layout
- [ ] Dense beats are split into separate moments when needed
- [ ] Tone matches subject matter and editorial stakes
- [ ] Quiet elements are actually quiet
- [ ] Final review includes frame-by-frame QA for clutter, hierarchy, and ambiguity

## References

See `references/research-notes.md` for source-backed design notes and `references/beat-sheet-template.md` for a practical planning template.
