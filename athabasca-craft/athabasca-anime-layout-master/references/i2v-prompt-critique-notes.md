# I2V Prompt Critique — Comedic Reversal Sequences

## Core lesson

Overloaded prompts are the primary failure mode for image-to-video (i2v) models, especially for sequences built around comedic reversal.

An i2v model splits attention between the reference image and the text prompt. A dense multi-beat prompt gets mostly ignored. A tight single-beat prompt stays coherent.

**The principle:** one emotional job per lane. One beat. One camera move.

---

## Five failure patterns in i2v prompts

### 1 — Multi-beat stacking

Bad:
> "Full-body kneeling → cut to sincere face → cut back to wide"

This encodes several editorial intentions as one generation. The model blurs performance and muddies the emotional read.

Fix: Split into separate lanes. Let editorial handle the cut stack.

### 2 — Over-long prompts for i2v

For text-to-video: aim for 120–280 words.
For i2v: aim for 50–80 words maximum.

The reference image already carries identity, composition, wardrobe, and much of the visual language. Restating it in long prose competes with the source frame.

Fix: Cut by 25–40%. Keep only beat + camera move + 2–3 style cues + identity lock phrase.

### 3 — Same visual language before and after the reversal

Before the reversal, romantic or sincere sequences often want softness, warmth, shallow depth of field, and expressive backlight. After the reversal, using the same grammar weakens the turn.

Fix: Shift the post-reversal grammar:
- stiffer framing, slightly more frontal
- slightly less dreamy bokeh, more practical depth
- the disruptive prop framed as a compositional intrusion

Not horror — just bureaucratic or practical clarity entering an otherwise emotional frame.

### 4 — Skipping the emotional gap

The joke often lands in the dead air between joy and confusion. If the sequence rushes straight from the snap into explanation, the comedic beat collapses.

Fix: Give the reversal its own lane(s):
- hand or gesture suspended after the turn
- expression transitions from joy to confusion
- the counterpart's unchanged face gets its own lane

### 5 — Not weaponizing the prop

If the gag depends on contrast between a sacred romantic object and an absurd practical object, the practical object must read as visually wrong inside the frame.

Fix: Frame it as a compositional violation:
- bright rectangular slab disrupting organic romantic shapes
- tabs, dense text, or edges treated as visible graphic objects
- pages or objects physically separating the characters
- the romantic object reduced from sacred object to sidelined object

---

## The comedic reversal sequence template

For a romantic-comedy sketch with a peak-romance-then-puncture structure:

| Phase | Dominant emotion | Visual grammar | Number of lanes |
|-------|------------------|----------------|-----------------|
| Sincere approach | Warmth, anticipation | Soft, shallow DOF, warm backlight | 2–3 |
| Peak moment | Absolute sincerity | Iconic, low angle, grandeur | 2–3 |
| Snap / reversal | Comic shock | Sharp, decisive, static hold | 1 |
| Reaction gap | Frozen joy → confusion | Slow push-in, reaction hold | 2–3 |
| Unchanged face | Oblivious sincerity | Static hold, close-up | 1–2 |
| Absurdity reveal | Bewilderment | Shifted grammar: stiffer, frontal | 2–3 |
| Tag | Comic aftertaste | Wide hold, contrast between them | 1 |

Minimum viable lane count for a comedic reversal is usually around ten lanes. If a sequence feels muddy, the answer is often more lane separation rather than more prompt prose.

---

## How to critique i2v prompts for this structure

Ask in order:

1. How many beats does this lane try to do? If more than one, split it.
2. How long is the text? If more than 80 words for i2v, cut it.
3. Does the visual language shift after the reversal? If not, shift it.
4. Is the emotional gap covered by a dedicated lane? If not, add it.
5. Is the disruptive prop framed as a visible object or only as atmosphere? If only atmosphere, rewrite it to feel intrusive.

---

## Generic worked example

A weak revision usually has these problems:
- one lane trying to do kneeling + face close-up + wide in one generation
- another lane trying to do reveal + insert + handoff + low angle simultaneously
- no dedicated lane for the suspended beat after the snap
- no dedicated lane for the counterpart's unchanged reaction

A stronger revision usually does this instead:
- split overloaded lanes into one-shot emotional jobs
- trim prompts by roughly 25–40%
- add a dedicated post-snap hold
- add a dedicated unchanged-face reaction
- shift the post-turn visual grammar so the tonal break is visible, not just implied

The point of the example is structural, not story-specific.