# Seedance prompt preview HTML pitfalls

Use this when building or revising Athabasca HTML prompt previews for manual Seedance dispatch.

## Durable lessons

1. **Constrain reference-image layout explicitly in markup**
   - Do not rely only on the shared stylesheet for mixed-aspect reference cards.
   - Add explicit `width` attributes on `<img>` tags and matching inline sizing on the containing `<figure>` / wrapper.
   - Good pattern:
     - fixed-width card containers (for example ~320px for character sheet refs, ~420px for environment refs)
     - `img width="..."`
     - `style="width:...px; max-width:100%; height:auto; display:block; object-fit:contain;"`
   - Why: without hard constraints, tall character sheets and wide environment stills can overflow, collide with captions, and make the preview unreadable.

2. **Only the per-group prompt bodies are actually submitted to Seedance**
   - Do not place essential generation guidance only in a footer such as “Continuity Anchors”.
   - Fold all instructions that Seedance must obey directly into the group prompt preamble and shot descriptions.
   - Footer-only notes are fine for human readers but should be treated as non-submittable unless the downstream workflow explicitly includes them.

3. **Honor exact opening blocking from the supplied outline**
   - Before drafting shots, verify the first physical state in the source scene.
   - Example durable pitfall: do not silently convert “already meditating on the cushion” into “wakes up in bed.”
   - For intimate reset scenes, the opening blocking often carries the emotional thesis and should not be generalized.

4. **Use references as selective constraints, not literal costume copies**
   - Character-sheet references may be for proportions / silhouette / face acting only.
   - If the scene outline conflicts with wardrobe in the reference sheet, state the selective use explicitly in the prompt body and reference caption.

## Recommended QA before upload

- Read the preview as if only the `pre` blocks will be copied into Seedance.
- Confirm every essential continuity rule appears inside those blocks.
- Open the HTML once and visually confirm reference cards do not overflow or stack captions awkwardly.
- Verify the first shot matches the supplied outline's starting state exactly.
