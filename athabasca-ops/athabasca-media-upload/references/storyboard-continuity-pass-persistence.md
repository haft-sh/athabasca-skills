# Storyboard continuity pass persistence

Use this reference when an Athabasca project has approved/final character or location reference assets and the user wants a full shot sequence regenerated or reviewed for continuity.

## Reusable pattern

1. Resolve the project slug and shot list via the API.
2. Identify final anchor assets before generation:
   - character sheet/reference IDs
   - location/environment references
   - prior selected or upscaled shot references, if they are being used as staging anchors
3. If the user selects an existing image as the final character/reference anchor, do not re-upload it. Patch that existing asset with merged metadata such as:
   - `characterRole`
   - `characterAnchorStatus: "final"`
   - `isFinalCharacterSheet: true`
   - `finalizedForContinuityPass: true`
   - `supersedesAlternateAssetIds`
   - `decisionNote`
4. Generate each shot using the selected reference stack and consistent scene/location cues. Keep shot prompts frame-specific: one decisive emotional beat, camera size/angle, visible prop state, costume/location continuity, and comedic or dramatic intent.
5. Inspect or vision-check generated local files before upload when quality matters.
6. Upload every accepted shot image through `POST /api/projects/:slug/media` with durable provenance:
   - `phase=storyboard`
   - `category=generated`
   - `sourceKind=generated`
   - title includes shot number and pass/version
   - `metadataJson` includes `workflow`, `continuityPass`, shot number/id, reference asset IDs, provider/model, prompt summary, and any superseded prior image IDs
7. Explicitly attach each returned asset to its shot using `POST /api/projects/:slug/shots/:shotId/media`; `metadataJson.shotId` alone is not enough.
8. Create a contact sheet for review when there are multiple stills. Upload it as project media with role/metadata like `contact_sheet`, `workflow: storyboard_continuity_pass`, and the ordered list of shot asset IDs.
9. Verify before reporting success:
   - `GET /api/media/:assetId` returns each asset
   - shot list `mediaAttachments` include the intended asset IDs
   - public URLs return `200` or `206`
   - contact sheet URL also resolves
10. Delivery convention in Telegram: send the contact sheet as native media (`MEDIA:/tmp/...`) and provide concise asset IDs/URLs for traceability.

## Review focus

Report continuity and storytelling quality, not just upload status. Check:
- face/wardrobe consistency for recurring characters
- location/time-of-day continuity
- whether each shot preserves the scripted emotional beat
- whether prop state progresses correctly across the beat sequence
- whether inserts/close-ups intentionally de-emphasize face identity

For short comedic sketches, explicitly call out whether the setup, reversal, and final button read clearly across the image sequence.