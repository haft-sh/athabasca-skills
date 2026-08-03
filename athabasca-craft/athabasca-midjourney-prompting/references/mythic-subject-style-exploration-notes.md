# Mythic-subject style exploration notes — naming bias, queueing, and favorite tagging

Use this reference when exploring style directions for mythic, folkloric, or culturally anchored material and the user wants broad visual exploration rather than immediate cultural specificity.

## Prompt naming bias

Proper names can drag Midjourney toward a narrow pretrained visual cluster earlier than intended. During style exploration, do not put the character/location names into every prompt unless the user explicitly wants those cultural cues activated.

Practical pattern:
- In a 10–20 prompt exploration set, use generic role descriptions for most prompts, such as `the older sibling`, `the younger sibling`, `two mythic bird brothers`, or `the guardian figure`.
- Reserve proper names for a minority of prompts when continuity, lore recognition, or culturally specific testing is actually the point.
- In the prompt-set markdown, note which prompts are generic-role prompts versus named prompts so later review can distinguish naming bias from true style preference.

## Markdown prompt-set artifact workflow

For large prompt batches, create a durable `.md` prompt set first, upload it as an Athabasca document artifact, then generate from that exact file. This preserves the source of truth for reruns, edits, and provenance.

Recommended fields:
- `phase=visual_dev`
- `category=research`
- `sourceKind=generated`
- `artifactKind=midjourney_prompt_set_markdown`
- `promptCount`
- `scene`
- `workflow=visual-development-prompt-drafting`

If the user asks to overwrite the prompt file in place, use the project media document replace helper so the `asset.id` and public URL remain stable.

## Sequential Midjourney queue from markdown

For 10+ MJ prompts, run a sequential or lightly staggered queue rather than firing parallel requests. Discord-backed MJ submissions can rate-limit on bursts; a simple 8-second stagger worked well on a 20-prompt batch.

Queue script shape:
1. Parse `## NN — Title` headings and matching ```text blocks from the markdown prompt set.
2. Assert heading count equals prompt block count and expected count.
3. Call `generateAndPersistImage()` with provider/model/aspect ratio plus attachment metadata like `promptSetAssetId`, `promptIndex`, and `promptTitle`.
4. Write an incremental JSON log after every prompt so partial progress survives interruption.
5. Continue on per-prompt errors, then report `ok/failed` counts.

## Favorite tagging after review

When the user identifies standout style prompts or results, immediately encode that selection in Athabasca media metadata:
- green for approved or favorite grids
- 5★ for the clear standout / primary style candidate
- 4★ for strong runners-up and secondary ingredients
- descriptive tags such as `visual-dev-favorite`, `primary-style-candidate`, `runner-up-style`, `texture-reference`, `limited-palette`, and the specific style family

This lets future agents retrieve the useful visual language without rereading the whole conversation.
