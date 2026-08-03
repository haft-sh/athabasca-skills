---
name: athabasca-visual-continuity
description: Maintain faithful recurring-character identity, roster integrity, spatial orientation, and delivery framing in reference-conditioned Athabasca still generation.
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [athabasca, image-generation, visual-continuity, character-identity, reference-images, qa]
    related_skills: [athabasca-media-generation, athabasca-media-upload]
---

# Athabasca visual continuity

Use this when a project still contains recurring characters and the user cares about faithful identity, exact positions in an ensemble, expression intent, or image corrections that must preserve an otherwise useful composition.

## Operating principle

Treat reference images as **role-specific controls**, not an undifferentiated pile. A composition frame, a canonical identity sheet, and a costume/wardrobe sheet do different jobs. Explicitly say which reference controls what in the prompt.

Do not report success from prompt submission alone. Visual QA must verify the generated pixels against the requested roster, positions, orientation, and character sheet.

## Character-reference correction passes

When a user says a generated character reference has the **right pose/background but wrong identity, color, style, or missing props**, preserve the successful layout instead of restarting from a generic prompt.

1. Upload any user-attached style image to the target project before generation; cached chat paths are not canonical inputs.
2. Use an explicit two-reference hierarchy:
   - **Identity/style authority:** controls skin/fur color, face, materials, costume, rendering style, and signature props.
   - **Composition authority:** controls pose, front/side orientation, full-body framing, and white/seamless background only.
3. State unwanted and desired reads directly: e.g. “not black, not a shadow silhouette; warm olive-green turtle skin.”
4. Name every required prop and require it to be fully visible, unobstructed, and within frame; specify hands/sides where ambiguity could cause omissions.
5. Visually inspect the output before calling it complete. Verify color, identity/style match, pose/orientation, background, and each required prop separately.
6. After the user approves the corrected reference, green-tag it, rate it, add `canonical-reference`, `recurring`, and a character-specific tag, then replace its predecessor as the identity reference in active prompt packets. Keep the environment/scale image as a secondary reference only.

This is a minimal-delta correction workflow: the composition reference must not dilute the canonical character identity.

## Reference hierarchy

### Initial ensemble generation

1. Use the composition reference plus approved identity sheets.
2. Name the exact roster and require each character **once**.
3. State the clock positions or other spatial map in plain language.
4. Include an explicit no-extra/no-duplicate rule.

### Correction pass

Use the smallest reference set that can correct the defect:

- **Composition lock:** latest acceptable group image.
- **Identity lock:** canonical sheet for the character being corrected.
- **Replacement identity:** add only the sheet for a missing character when repairing a duplicate/missing roster error.

Do not keep all historical character sheets in a micro-correction by default. Excess simultaneous references can contaminate faces, cause identity drift, or create duplicate characters.

Prompt the reference roles explicitly: “Reference 1 controls composition; reference 2 controls this character’s identity only.”

## Priority-character prompting

When one character is narratively or commercially important:

- place them at an exact clock position / frame location;
- state they are large, unobstructed, and sharply visible;
- list their non-negotiable visual cues from the approved sheet: face/snout silhouette, eyewear, eyes, helmet fit, skin/fur color, and signature wardrobe detail;
- state the required expression and the failure modes to avoid.

Concrete language outperforms vague continuity language. For example: “small two-nostril turtle snout, oversized black square glasses, large brown eyes” is useful; “same Turbo vibe” is not.

A nuanced child-character performance can be specified as: cute but determined, focused eyes, subtle closed mouth, controlled concern; not scared, grotesque, angry, or goofy.

## Radial / clock-face compositions

“Upright” is ambiguous in a radial huddle. Define facial orientation relationally:

- which feature is closest to the **inner circle / sky center**;
- which feature is closest to the **outer frame**;
- whether the character is speaking, and whether an open mouth must read as a command rather than a grin.

Example: “At 12 o’clock, Gary’s eyes are nearest the central sky; his mouth and chin are nearest the top outer edge.”

## Mandatory QA checklist

Before presenting a generated ensemble as final, inspect the image and verify:

- [ ] enumerate visible players/characters by clock position;
- [ ] exact requested roster, one instance each;
- [ ] no duplicate / missing character;
- [ ] priority character matches the named canonical sheet in face and signature features;
- [ ] requested position and radial inner/outer orientation are correct;
- [ ] all expressions match the emotional brief;
- [ ] no faceguard, hands, or crop obscures priority features;
- [ ] final dimensions match the user’s requested aspect ratio.

If any one material criterion fails, call it out and run a minimal correction pass rather than presenting it as final.

## Provider-comparison QA

A successful generation response and a persisted project asset are not quality approval. When comparing two or more edit providers, inspect each candidate against **every** requested repair and report pass/fail separately before recommending one.

For text- or schedule-heavy set dressing, verify pixels rather than prompt intent:

- the key requested phrase is fully readable and exact;
- an arrow or outline lands on one unambiguous, numbered target cell/object;
- chronological marks (such as a countdown) form the requested continuous sequence with no unexplained gaps;
- realistic inserts (such as athletes in a poster) have believable anatomy, wardrobe, and action at the intended viewing scale.

A candidate can be the best available result yet still need a micro-correction. State that distinction plainly; do not call a broad callout equivalent to a specifically numbered target date.

## 16:9 delivery discipline

Native model presets may return a non-16:9 landscape raster even when the prompt says 16:9. Confirm the **actual persisted raster** by downloading or inspecting the canonical `publicUrl`; generation response metadata can report nominal dimensions that differ from the stored PNG. If a derivative crop is needed:

1. choose a deliberate crop that preserves priority faces and the composition’s visual center;
2. inspect the cropped result, not only the source;
3. persist the crop to R2;
4. attach it as project media with provenance linking `derivedFromAssetId`, source reference IDs, and the correction workflow;
5. only yellow-tag flawed candidates after the corrected replacement exists.

## Storyboard-grid frame extraction

When the user approves selected panels from a generated storyboard grid and asks to save them individually, prefer deterministic cropping over regeneration.

1. Resolve and download the canonical full-resolution grid from its Athabasca `publicUrl`; do not crop a Telegram preview or screenshot.
2. Inspect the downloaded raster dimensions before calculating cells. Generation-response width/height metadata may not match the final persisted object, so the pixels are authoritative.
3. Map panel numbers in reading order. For a 3×3 sheet: `index = panelNumber - 1`, `row = index // 3`, `column = index % 3`.
4. Calculate proportional boundaries from the actual raster (`round(column * width / 3)` through `round((column + 1) * width / 3)`) rather than fixed cell sizes, because dimensions may not divide evenly.
5. Trim only the observed grid-divider thickness, usually 2–4 pixels. Preserve the panel number and all frame content unless the user explicitly asks for number removal or repainting.
6. Verify each crop for correct panel, no neighboring-panel leakage, expected aspect ratio, and intact composition.
7. Persist every derivative through `POST /api/projects/:slug/media` with `phase=storyboard`, `category=generated`, `sourceKind=generated`, and metadata including `artifactKind: storyboard_frame`, `derivedFromAssetId`, `sourcePanel`, and `workflow: storyboard-grid-panel-extraction`.
8. If local multipart upload is unavailable, upload the crop to a deliberate R2 staging key and import it using the project-media endpoint's `sourceUrl`; the returned project asset URL is canonical, not the staging URL.
9. Verify the created project attachment and perform a real public `GET` for each final URL before reporting success.

Do not regenerate an approved panel when a lossless crop fulfills the request. Do not report local files or standalone R2 objects as project-saved assets.

## Pitfalls

- Do not claim a canonical sheet was used unless it was actually included as a reference asset.
- Do not assume a provider followed a “no duplicates” prompt; count characters visually.
- Do not declare a raw `landscape` output to be 16:9 without dimension verification.
- Do not overcorrect the whole cast when the defect is localized to one identity, position, or facial orientation.
- Do not use a composition frame as a character identity anchor when an approved identity sheet exists.
- **Continuity-anchor status:** do not silently promote the last frame of a yellow/non-canonical generated clip into the next packet’s `@image1`. A user must explicitly choose it as a temporary bridge, or a clean approved outgoing frame must be selected first. For impact/recovery beats, a real predecessor frame is more reliable than text-only continuity across a cut.
- **Corrected-reference publication:** never rely on an in-place overwrite of an image URL when a user needs the corrected pixels immediately. A browser/CDN may continue to serve stale content even if the origin object changed. Instead create a new immutable project-media asset, green-tag it with appropriate canonical tags, update active prompt-packet/reference bindings to its new asset ID and public URL, verify those public pixels, then yellow-tag the superseded reference only after the new asset is connected.
