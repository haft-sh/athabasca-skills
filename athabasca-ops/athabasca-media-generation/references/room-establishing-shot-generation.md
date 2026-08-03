# Room establishing-shot generation notes

Use this note for room or environment establishing plates where the output should be an environment-only reference image grounded in storyboard grids and a shot list.

## Proven pattern

Inputs:
- storyboard grids or visual boards
- shot-list markdown
- desired output: wide room establishing shot, no characters, all scene-critical props visible

Prompt content that mattered:
- explicitly say **environment-only** and repeat negatives: no characters, no people, no mascot forms
- include full room geography from the shot list in traversal order
- name required props and wall details explicitly
- specify the emotional design of the room, not just object inventory
- call out unwanted fantasy leakage when the room should stay grounded

## Model / approach results

### GPT Image 2 via native Codex route
Best result for strict environment-only plates when references are available.

### Midjourney with `referenceAssetIds`
Do **not** send Midjourney image references through `referenceAssetIds` in the current Athabasca route; use public asset URLs pasted at the front of the prompt instead.

### Midjourney with image URLs in prompt
Useful for style and room exploration, but may return a grid or reintroduce characters despite negatives. Treat as exploration unless it truly satisfies the empty-room constraint.

### Midjourney pure text
Athabasca timeout does not prove upstream failure. Check Discord or latest project media before rerunning blindly.

## Verification checklist
- [ ] no characters or living mascot forms
- [ ] single establishing composition unless a grid was explicitly requested
- [ ] wide enough to establish blocking and geography
- [ ] required props and wall/story details visible
- [ ] room mood matches the requested emotional design

If a candidate fails the no-character constraint, report it as exploration/reference only, not final.
