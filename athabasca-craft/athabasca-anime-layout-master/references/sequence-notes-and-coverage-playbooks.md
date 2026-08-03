# Sequence Notes, Storyboard Shorthand, and Coverage Playbooks

## Purpose

This reference turns the skill from a single-shot critic into a **sequence-capable storyboard assistant**.

Use it when the user is planning multiple shots, revising a cut, or needs concise production-style notation for boards, animatics, shot lists, or editorial planning.

## 1) Recommended continuity note format

For each storyboard panel or shot, record the following in compact form:

- **Shot ID**: `S03A`, `P12`, `B07`, etc.
- **Shot size / angle**: `MCU LA`, `WS HA`, `OTS MS`
- **Axis**: `AXIS: A↔B`, `AXIS: door→captain`, `AXIS HOLD`
- **Screen direction**: `DIR: L→R`, `DIR: R→L`, `DIR HOLD`
- **Eyeline**: `EYE: A looks 10° down SR`, `B looks 15° up SL`
- **Blocking beat**: `BLK: A steps in / B yields half-step / C remains seated`
- **Continuity locks**: prop hand, seated/standing state, door open %, blood state, coat open/closed
- **Cut intent**: `CUT ON turn`, `CUT ON reaction`, `CUT AFTER reveal`, `HOLD for dread`
- **Editorial role**: `GEO`, `REACTION`, `INSERT`, `GLUE`, `POWER SHIFT`, `RESET LINE`

### Minimal compact template

```text
S03A — MCU OTS, HA
AXIS: captain↔soldier | DIR: L→R | EYE: soldier up SR
BLK: captain leans in, soldier holds ground
LOCKS: captain right hand on rail, soldier helmet on, sea behind captain
CUT: on captain’s half-smile
ROLE: power shift / reaction setup
```

## 2) Storyboard shorthand / annotation conventions

### Shot sizes
- `ECU` — extreme close-up
- `CU` — close-up
- `MCU` — medium close-up
- `MS` — medium shot
- `MFS` — medium full shot
- `FS` — full shot
- `WS` / `LS` — wide / long shot
- `EWS` / `ELS` — extreme wide / extreme long shot
- `2S` — two-shot
- `3S` — three-shot
- `OTS` — over-the-shoulder
- `POV` — point of view
- `INS` — insert
- `C/A` — cutaway
- `EST` — establishing

### Camera angle / position
- `EL` — eye level
- `LA` — low angle
- `HA` — high angle
- `BEV` / `TOP` — bird’s-eye / top shot
- `NADIR` — from below
- `DUTCH` — dutch angle
- `PROFILE` — side profile
- `FRONTAL` — straight-on

### Camera movement
- `PAN L/R`
- `TILT U/D`
- `DOLLY IN/OUT`
- `TRUCK L/R`
- `ARC L/R`
- `CRANE U/D`
- `HANDHELD`
- `LOCKOFF`
- `RACK FOCUS`
- `ZOOM IN/OUT`

### Editorial / sound / transition notes
- `CUT`
- `MATCH ACT`
- `MATCH EYE`
- `HARD CUT`
- `SMASH CUT`
- `J-CUT`
- `L-CUT`
- `HOLD`
- `SFX`
- `VO`
- `OS` / `O.S.` — off-screen / off-screen voice
- `BG` — background action or ambience cue

### Direction shorthand
- `SL` / `SR` — screen left / screen right
- `L→R` / `R→L` — movement vector
- `AXIS HOLD`
- `CROSS LINE`
- `RESET AXIS`

### Board drawing cues
- arrows for actor movement
- separate arrow style for camera movement
- frame-within-frame marks for zoom / punch-in intention
- circled object or face when a focal read must not be missed
- dashed path when motion is implied over the cut rather than shown continuously

## 3) Sequence-level planning rules

### A) Every sequence needs a geography strategy
Decide early:
- what the dominant axis is
- whether it changes
- what neutral or reset shot can bridge that change
- what landmarks keep orientation stable

### B) Don’t stack shots that solve the same job
If three adjacent shots all deliver the same emotional distance and same editorial function, one is probably redundant.
Each shot should ideally add one of:
- new information
- new emotional access
- new power geometry
- new speed / rhythm
- editorial glue

### C) Build reverses as families, not isolated drawings
A reverse should feel pre-related to its counterpart by:
- camera height
- lens family / perspective force
- eyeline offset
- horizon logic
- movement logic

## 4) Coverage playbooks by scene type

## Dialogue scene

### Minimum safe package
- geography shot or equivalent relational two-shot
- one setup preserving both characters’ spatial relation
- singles or OTS reverses
- at least one reaction shot
- at least one insert / cutaway if emotional timing may need reshaping

### Priorities
- eyelines
- screen direction
- power shifts
- interruption timing
- who owns the silence

### Useful variants
- balanced 2S for parity
- unbalanced OTS for dominance
- profile split by architecture for emotional distance
- delayed reaction cut when subtext matters more than the spoken line

## Action scene

### Minimum safe package
- clear geography opener
- directional run / attack vector
- impact beat coverage
- spatial reset shot when the fight turns
- inserts for weapon hand, trigger, foot plant, object grab, wound, or obstacle

### Priorities
- axis clarity
- movement vector continuity
- readable silhouettes
- cause/effect legibility
- match on action

### Common failure
Beautiful impact frames that cannot be connected because no bridging motion or reset geography exists.

## Emotional / intimate scene

### Minimum safe package
- one relational setup establishing distance
- one performance-dominant closer framing
- one reaction beat or withheld reaction beat
- one insert or environmental cutaway if pacing may need breath

### Priorities
- when to cut to reaction
- when not to cut
- breath rhythm
- tiny gesture continuity
- prop touch / hand continuity

### Common failure
Overshooting with too many equivalent close-ups, flattening the emotional progression.

## Suspense / dread scene

### Priorities
- negative space direction
- off-screen implication
- slow eye-trace control
- environmental anchors
- cut timing based on anticipation rather than impact

### Useful coverage
- holdable wides
- inserts with delayed payoff
- reverses that preserve uncertainty rather than fully resolve space

## Comedy beat

### Priorities
- timing precision
- reaction hierarchy
- frontal deadpan when useful
- cutaways used as punctuation
- maintaining enough continuity so the joke lands, but allowing slight stiffness for comic effect

## 5) Sequence diagnosis prompts

When reviewing a series of shots, ask:
1. Where is the axis in each beat?
2. Do any cuts accidentally reverse motion or gaze?
3. Which shot establishes geography, and is it enough?
4. Which shot is the editor supposed to use for the emotional turn?
5. Is there repair coverage if performance timing changes in edit?
6. Are prop and hand states stable?
7. Is there any redundant shot that repeats function instead of escalating it?
8. If the line is crossed, is there a neutral bridge or visible transition?

## 6) What the skill should output for sequence requests

When the user asks for a sequence, animatic pass, or shot list, include:
- shot-by-shot list
- each shot’s editorial role
- axis and screen direction
- continuity locks
- likely cut points
- where inserts / cutaways are advisable
- where geography must be reset
- which beat should dominate the cut

## 7) Hard-cut bias

If the project prefers **hard cuts**, design shots with stronger continuity discipline:
- clearer eyeline logic
- more exact match-on-action points
- cleaner directional flow
- more deliberate reaction placement
- fewer transitions that rely on dissolves or stylized smoothing
