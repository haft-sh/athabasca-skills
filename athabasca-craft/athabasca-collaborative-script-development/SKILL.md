---
name: athabasca-collaborative-script-development
description: Co-develop film scripts from rough outlines through structured ideation, critique, and collaborative refinement into shooting scripts.
triggers:
  - User provides a story outline and wants help developing it into a script
  - User asks for "director's hat" feedback or creative critique
  - User wants to iterate on dialogue, structure, comedic beats, or visual storytelling
  - User says "help me ideate" or "give me feedback on this concept"
---

# Athabasca Collaborative Script Development

Use this when a user wants to co-develop a film script from scratch through iterative creative collaboration. This covers the full arc from rough outline → structured critique → collaborative refinement → shooting script → Athabasca persistence.

## Why this exists

Athabasca's script phase typically handles intake of user-supplied scripts or agent-generated scripts from prompts. But when the user wants to *co-create* a script through creative back-and-forth, a different workflow applies. This skill captures the pattern for collaborative script development where the user and agent iterate together.

## The Workflow

### Phase 1: Save the initial outline
When the user provides a rough outline or concept:
1. Save it as a `.md` file in `docs/briefs/` with a descriptive name
2. Use a clean structure: title, type, duration, premise, scene breakdown
3. Don't over-format — capture the user's voice and intent

### Phase 2: Structured creative critique
Put on the "director's hat" and provide numbered feedback covering:
- **What's working** — affirm strong elements (premise, structure, specific lines)
- **What needs work** — identify weak points with specific alternatives
- **Technical suggestions** — pacing, timing, shot composition, sound design
- **Dialogue options** — offer 2-3 alternatives for key lines with reasoning
- **Twists/escalations** — suggest ways to heighten comedy, tension, or emotional impact
- **Thematic depth** — point out deeper satirical or emotional layers the user may not have considered

Format critique as numbered points with bold headers. Be specific, not vague. Offer concrete alternatives, not just "make this better."

### Phase 3: User decisions
The user responds with decisions on each point. Common patterns:
- "Yes, do X" — implement the suggestion
- "I like option B" — choose from offered alternatives
- "I want Y instead" — override with their own idea
- "Skip this" — leave as-is

### Phase 4: Synthesize into shooting script
Turn the outline + decisions into a proper shooting script with:
- **Cast list** — character descriptions, not just names
- **Scene breakdown** — numbered scenes with location/time headers
- **Dialogue** — formatted with character names and stage directions
- **Action lines** — visual and physical beats
- **Production notes** — sound design, visual style, pacing
- **Thematic note** — the deeper meaning or satirical target

Use screenplay-adjacent formatting (not strict Final Draft format — readable markdown is fine).

### Phase 5: Persist to Athabasca
Upload both artifacts to the project:
1. **Brief outline** — `phase=init`, `category=research`, `sourceKind=generated`
2. **Shooting script** — `phase=init`, `category=generated`, `sourceKind=generated`

Use descriptive titles and provenance notes that capture the collaborative nature.

## Critique Format Examples

### Weak critique (avoid)
> "The dialogue could be punchier."

### Strong critique (do this)
> **The ending needs a stinger.** "Whatever, I'll come in" is a strong last line, but the cut to black feels abrupt. Options:
> - **Option A:** As the door closes, a notification pops up: *"💡 Tip: Upgrade to Premium for uninterrupted intimacy!"*
> - **Option B:** The woman's voice glitches mid-sentence as the door closes — revealing she's buffering too
> 
> I'd go with A or B. They land the satirical point without overstaying.

## Shooting Script Structure

```markdown
# TITLE

### A Short Film
**Duration:** ~75 seconds  
**Format:** First-person POV  
**Tone:** Satirical comedy  
**Status:** Shooting Script v1  

---

## CAST

- **CHARACTER** — description, key traits, what we see/hear

---

## SCENE 1 — SCENE NAME

**INT/EXT. LOCATION — TIME**

Action description. Visual details.

**CHARACTER**
Dialogue line.

*(stage direction)*

---

## SOUND DESIGN NOTES

- Bullet points for audio cues, music, ambient sound

## VISUAL NOTES

- Bullet points for cinematography, color, composition

## THEMATIC NOTE

The deeper joke or emotional core.
```

## Pitfalls

- **Don't wait for a perfect outline before critiquing.** Rough is fine — the collaboration is the point.
- **Offer alternatives, not just problems.** "This line is weak" is useless. "Try: [option A] or [option B]" is valuable.
- **Respect the user's voice.** If they write funny dialogue, keep their tone in your suggestions. Don't overwrite their style with yours.
- **Timing matters for comedy.** When suggesting pacing, give specific timecodes or beat counts: "hold for 3 seconds" not "pause dramatically."
- **Sound design is half the film.** Always include audio notes — they're often where the best jokes live.
- **Save locally first, then upload.** Don't try to upload directly from conversation — write the `.md` file, then use the media API.

## Example Session Flow

1. User: "Here's an outline for a comedy about VR dating" → save as `docs/briefs/vr-girlfriend-outline.md`
2. Agent: "Here's my director's critique..." → 10 numbered points with alternatives
3. User: "I like points 1, 3, 7. For point 5, do X instead."
4. Agent: synthesize into `docs/briefs/vr-girlfriend-script.md` with full shooting script
5. Agent: upload both to Athabasca as project media

## Related Skills

- `athabasca-script-phase-source-supplied-intake` — for when the user supplies a finished script
- `athabasca-comedy-writing-room` — for sketch comedy specifically; contains the comedy theory toolkit, scorecard, subgenre modes, and punch-up menu. Use this when the script is comedic/satirical and needs sharp escalation logic, satirical target diagnosis, or punch-up work.
- `athabasca-media-upload` — for the persistence pattern
- `athabasca-project-init-and-reference-attach` — for project creation alongside script development
