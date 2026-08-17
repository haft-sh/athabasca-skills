---
name: ui-critique-and-product-design
description: Use when critiquing, reviewing, or redesigning desktop/mobile app UIs from screenshots, mockups, wireframes, or flows. Focus on product goal clarity, wording, visual hierarchy, eye movement, interaction flow, usability, aesthetics, and concrete redesign recommendations.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ui, ux, product-design, critique, mobile, desktop, mockups, screenshots, hierarchy, copywriting]
    related_skills: [creative-design-artifacts]
---

# UI Critique and Product Design

## Overview

Use this skill when the user wants a serious product-design critique or redesign direction for an app UI, especially from screenshots, mockups, wireframes, or prototype frames. The goal is not generic taste commentary; it is to understand what the app is trying to help the user do, evaluate whether the interface communicates that clearly and efficiently, and produce specific recommendations the team could implement.

This skill draws on communication-oriented interface design principles associated with Kevin Mullet and Darrell Sano, Steve Krug's usability mindset, Steve Schoger's practical visual craft, and common modern product-design heuristics. Treat the interface as a communication system: what is this screen saying, in what order, with what emphasis, and how confidently does it guide the user toward the right action?

The output should be concrete, prioritized, and usable by builders. Prefer exact wording suggestions, hierarchy fixes, layout changes, and flow recommendations over vague statements like "make it cleaner" or "improve spacing."

## When to Use

Use when the user asks to:
- critique an app screen, mobile app, desktop app, or responsive UI
- review mockups, screenshots, wireframes, Figma exports, or design comps
- improve app UX, wording, hierarchy, navigation, conversion, or flow
- evaluate whether a screen communicates its purpose well
- compare alternate UI directions and choose the stronger one
- turn high-level feedback into concrete redesign recommendations

Especially relevant when the user provides:
- screenshots or mockups
- a rough product idea that needs design direction
- a current UI that feels confusing, cluttered, weak, generic, or visually flat

Do not use this skill as the primary route for:
- pixel-perfect front-end implementation only
- pure brand/logo design without product UI
- architecture diagrams or non-product visual artifacts

## Core Design Lens

Judge the UI through these questions, in roughly this order:

1. **Goal clarity** — What is the product trying to help the user do?
2. **Screen message** — What is this screen trying to communicate right now?
3. **Primary action clarity** — What should the user do next, and is that obvious?
4. **Visual hierarchy** — Does the interface emphasize the right things first, second, and third?
5. **Eye movement** — Does the layout guide attention intentionally, or scatter it?
6. **Flow and friction** — Can the user complete the core task with minimal confusion and effort?
7. **Language quality** — Are labels, headings, and CTAs specific, human, and confidence-building?
8. **Aesthetic coherence** — Does the UI feel deliberate, modern, and trustworthy without compromising clarity?

## Required Intake

Before critiquing, gather or infer:
- what the app does
- who the primary user is
- the main user task on this screen
- whether the screen is for mobile, desktop, or both
- whether the user wants critique only, rewrite suggestions, or redesign direction

If screenshots/mockups are provided, inspect them directly.

For **live product audits** rather than static mockups, capture a complete evidence set before critiquing:
- onboarding or empty-state flow
- primary populated workspace
- menus, popovers, and selectors
- scrolled states of long panels or inspectors

If the product is too empty to audit meaningfully, seed a small set of representative local fixtures so navigation, reading, metadata, and workflow surfaces become legible. Treat those as audit fixtures, not product work. See `references/live-product-ui-audit-workflow.md`.

If the user wants a premium deliverable rather than plain critique text, follow `references/premium-ui-audit-artifact-workflow.md` for the full capture -> critique -> mockup -> HTML artifact flow. For the current house style of deliverable packaging, also consult `references/premium-audit-deliverable-patterns.md`.

If product goal is missing:
1. infer the likely goal from the UI
2. label the inference as an assumption
3. proceed with critique against that assumption
4. note what would change if the assumed goal is wrong

Do not stall on missing perfect context when the screen itself gives enough signal to provide useful feedback.

## Critique Workflow

1. **State the product/job-to-be-done**
   - Summarize the app's apparent purpose in 1-3 sentences.
   - Identify the user's likely motivation and desired outcome.

2. **State the screen's communication task**
   - What must this screen tell the user?
   - What must the user notice first?
   - What action or decision should follow?

3. **Read the screen top-down and left-to-right**
   - Simulate first-glance scanning.
   - Note what grabs attention first, whether that is correct, and where the eye gets stuck.
   - Identify any competition among headings, cards, buttons, illustrations, metrics, or chrome.

4. **Evaluate the UI across the main dimensions below**
   - Use specific evidence from the screen.
   - Separate critical issues from polish issues.

5. **Recommend changes in priority order**
   - Start with changes that improve comprehension or task success.
   - Then address flow, then wording, then aesthetics/polish.

6. **Where useful, rewrite the UI**
   - Rewrite headlines, labels, helper text, empty states, and CTAs.
   - Prefer concrete microcopy over conceptual advice.

7. **If asked for redesign**
   - Propose a revised information hierarchy and layout direction.
   - Describe what to remove, combine, emphasize, or demote.

8. **If the user wants a premium audit artifact or proposal deck**
   - Generate high-quality concept mockups that illustrate the main flaws and proposed fixes.
   - For each major flaw, produce at least a **before/problem illustration** and an **after/proposal illustration**.
   - Treat generated images as concept visuals unless you have a true image-editing path; do not imply pixel-perfect fidelity to the original product if the model is text-to-image only.
   - Pair every generated mockup with a short explanation of what design issue it is demonstrating and what changed in the proposal.
   - For app audits, capture every major surface first: onboarding, primary workspace states, menus/popovers, and representative scrolled states of dense panels.
   - Follow `references/premium-visual-audit-deliverable.md` for the default deliverable shape, quality bar, and fallback behavior when image generation is quota-limited.
   - Prefer one self-contained HTML review artifact that combines screenshots, critique, generated before/after concepts, redesign proposals, and a ranked implementation backlog.
   - When feasible, make the deliverable directly viewable as a local HTML artifact, published Hypervault artifact, or shareable URL instead of only handing back raw notes or filesystem paths.
   - If image generation is partially blocked by quota or backend limits, include the successful images, clearly mark the missing ones, and state the concrete blocker rather than implying a full visual set exists.

## Main Critique Dimensions

### 1. Product Goal and UI Match

Ask:
- Does the interface reflect the actual purpose of the app?
- Does the UI over-index on decoration or secondary features instead of the core job?
- Is the screen optimized for what the user most urgently needs?

Common failure modes:
- the interface looks polished but does not make the app's purpose legible
- secondary metrics/features crowd out the main task
- the screen is designed as a mood board instead of a tool

### 2. Verbiage and Microcopy

Critique:
- page titles
- section headings
- navigation labels
- button text
- field labels
- helper text
- empty states
- error text
- onboarding language

Principles:
- prefer specific over abstract
- prefer user language over internal/product-team language
- make CTAs action-specific: "Create invoice" beats "Continue"
- remove redundant instructional text when the UI already communicates it
- keep labels short, but not cryptic
- avoid cleverness where clarity matters

Useful copy questions:
- Would a first-time user understand this without explanation?
- Does each CTA answer "what happens if I tap this?"
- Does the heading describe the outcome or just the feature bucket?

### 3. Visual Hierarchy

Inspect:
- scale differences
- weight differences
- contrast
- spacing groups
- card emphasis
- color emphasis
- density distribution
- placement of the primary action

Principles from communication-oriented design:
- stronger hierarchy means users can tell importance instantly
- related things should visually belong together
- differences should mean something, not merely decorate
- if everything is loud, nothing is loud

Look for:
- too many equally prominent cards/buttons
- weak separation between primary and secondary information
- headings that do not dominate enough
- accents used everywhere instead of selectively
- spacing that obscures grouping

### 4. Eye Movement and Scan Path

Evaluate how attention travels through the screen.

Ask:
- What do users see first?
- What do they see second?
- Is the path intentional?
- Is there a clean landing point?
- Are there distracting hot spots that steal attention?

Typical problems:
- oversized decorative elements outrank functional ones
- multiple colored objects compete at once
- cards form a visual grid with no clear starting point
- sidebars or sticky chrome dominate content
- weak whitespace rhythm causes a muddy scan pattern

### 5. Flow and Task Completion

Assess whether the user can complete the main job efficiently.

Inspect:
- navigation model
- step order
- decision count
- mode switching
- discoverability of next actions
- destructive-action safety
- mobile thumb reach / desktop efficiency

Questions:
- Is the next step obvious?
- Are users forced to think about structure instead of task?
- Are there unnecessary branches or friction points?
- Are actions placed where users need them?

Apply Krug-style standards:
- minimize needless thinking
- remove ambiguity at decision points
- prefer recognition over recall
- make the obvious path feel obvious

### 6. Information Architecture on the Screen

Examine whether content is broken into the right chunks.

Look for:
- too many peer-level sections
- poor grouping of controls and results
- settings mixed with execution surfaces
- summary/detail relationships that are unclear
- tabs or accordions that hide critical information

A strong screen usually has:
- one clear primary region
- a small number of meaningful secondary regions
- a clear distinction between context, action, and supporting detail

### 7. Aesthetics and Craft

Use taste in service of clarity, not as a separate art exercise.

Review:
- spacing consistency
- typography pairing and rhythm
- contrast and readability
- color restraint
- corner radius/shadow consistency
- icon style consistency
- alignment quality
- whether the design feels intentional or template-fragmented

Steve Schoger-style craft checks:
- use spacing to create hierarchy before adding lines/backgrounds
- use fewer colors, with clearer jobs for each
- make one element pop instead of five
- soften neutral UI noise
- let typography and whitespace do more work

### 8. Mobile vs Desktop Fitness

For **mobile** check:
- thumb-friendly CTA placement
- one-handed reach for primary actions
- vertical rhythm and chunking
- keyboard/form friction
- excessive density
- whether important content appears above the fold

For **desktop** check:
- whether wide layouts waste space or lose focus
- whether tables/dashboards support fast scanning
- whether the primary working area is large enough
- whether side panels improve work or just add clutter
- shortcut/efficiency opportunities for repeat users

### 9. Trust, Clarity, and Emotional Tone

Ask:
- Does the UI feel reliable?
- Is the tone appropriate for the task seriousness?
- Does the design reduce anxiety where users may hesitate?
- Are important states and consequences clear?

This matters especially for finance, health, productivity, admin, and creator tools.

## Recommended Output Format

When delivering critique, prefer this structure:

### A. Intent Read
- What the app appears to do
- What this screen appears to be for
- Assumptions, if any

### B. What is Working
- 3-5 strongest choices

### C. Main Issues
- ordered by severity/impact
- each issue should include:
  - what the problem is
  - why it matters
  - what to change

### D. Specific Rewrite Suggestions
- headings
- labels
- CTA text
- helper/error/empty-state text where relevant

### E. Layout / Hierarchy Recommendations
- what to promote
- what to demote
- what to group
- what to remove or simplify

### F. Optional Redesign Direction
- describe a better screen structure in words
- mention desktop/mobile differences if relevant

### G. Priority Stack
- **Must fix now**
- **Should improve next**
- **Polish later**

## Redesign Heuristics

When asked to suggest a better design direction:
- start by simplifying the task model, not decorating the existing structure
- make the primary action visually and spatially obvious
- reduce the number of competing visual zones
- move supporting detail below or beside the core task
- collapse repeated patterns
- rewrite labels before adding more UI
- use whitespace and typography to clarify structure before adding containers
- preserve user momentum: fewer choices, clearer defaults, easier recovery

## Tone of Critique

Be candid but constructive.

Good critique sounds like:
- "The screen visually emphasizes status cards before the action the user actually came to perform."
- "The CTA label is too generic; users cannot predict the outcome confidently."
- "This section adds noise without helping task completion and should likely be collapsed or removed."

Avoid critique that sounds like:
- "Looks nice but maybe tighten spacing."
- "Could be more modern."
- "I don't love this color."

Tie every opinion to communication, comprehension, trust, or task performance.

## Common Pitfalls

1. **Mistaking taste for critique.**
   Personal preference is not enough. Explain the usability or communication consequence.

2. **Ignoring the app's goal.**
   A beautiful screen can still fail if it does not support the user's main job.

3. **Giving only negative feedback.**
   Call out what works so the user knows what to preserve.

4. **Being too vague.**
   Every major criticism should lead to a concrete recommendation.

5. **Over-focusing on color and not enough on structure.**
   Hierarchy, flow, grouping, and wording usually matter more.

6. **Treating mobile and desktop the same.**
   Interaction cost, density, and reachability differ.

7. **Missing copy problems.**
   Bad wording often creates UX friction even when layout is decent.

8. **Redesigning everything at once.**
   Prioritize the changes with the highest effect on comprehension and task success.

## Verification Checklist

- [ ] I identified the app goal or stated my assumptions.
- [ ] I explained the screen's main communication task.
- [ ] I evaluated hierarchy, scan path, flow, copy, and aesthetics.
- [ ] I separated high-impact issues from minor polish.
- [ ] I gave concrete recommendations, not just opinions.
- [ ] I included specific wording suggestions where relevant.
- [ ] I accounted for mobile/desktop context if applicable.
- [ ] My critique is actionable for a builder or designer.
