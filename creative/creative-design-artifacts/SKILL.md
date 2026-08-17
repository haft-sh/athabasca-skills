---
name: creative-design-artifacts
description: "Use when producing static or HTML-based design artifacts: one-off HTML prototypes, brand/system-inspired mockups, DESIGN.md tokens, architecture diagrams, Excalidraw diagrams, and comparison sketches. Routes by artifact type and fidelity."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [design, html, diagrams, prototypes, design-systems, excalidraw, svg]
    related_skills: [creative-code-visuals]
---

# Creative Design Artifacts

## Overview

This umbrella covers design artifacts whose main output is a static/inspectable file: HTML mockups, brand/system-inspired web designs, DESIGN.md token specs, SVG/HTML architecture diagrams, Excalidraw JSON diagrams, and quick variant sketches. Route by fidelity and representation, then produce a real artifact file the user can open.

## When to Use

- Create a polished one-off HTML artifact: landing page, deck, prototype, poster, or report.
- Create 2-3 quick HTML mockup variants for comparison.
- Emulate a known web design system or product aesthetic.
- Author, validate, or export a `DESIGN.md` token/spec file.
- Draw cloud/infra/software architecture diagrams as dark-themed SVG/HTML.
- Produce hand-drawn Excalidraw JSON diagrams for flows, systems, or sequences.

## Router

| Need | Route |
| --- | --- |
| Polished single HTML artifact | Claude-style design artifact |
| Fast divergent variants | Sketch |
| Product/brand aesthetic mimicry | Popular web designs |
| Design token/spec authoring | DESIGN.md |
| Technical architecture diagram | Architecture diagram |
| Hand-drawn editable diagram | Excalidraw |

## Workflow

1. Determine the output representation: HTML/CSS, DESIGN.md markdown, SVG/HTML diagram, or Excalidraw JSON.
2. Determine fidelity: quick variants, polished artifact, or editable source.
3. Generate the actual file, not only a textual description.
4. Preview or validate structure where possible.
5. Return the file path/URL and a concise explanation of design choices.

## HTML Design Artifacts

For polished HTML, start from the user's context and purpose rather than generic vibes. Use real layout, typography, color, spacing, and component hierarchy. For quick sketches, produce multiple variants and make tradeoffs visible.

When the HTML artifact is meant to live inside a product or repository with a house HTML profile, validator, or publish pipeline, do not stop at visual correctness. Inspect the required metadata and structural conventions first (for example required `<meta>` fields, stable block IDs, and required `<section id="..." data-hv-section="...">` attributes), then validate the generated file against that contract before handing it off. A beautiful HTML file that fails the host app's publish/index validator is incomplete work.

Do not confuse semantic structure with actual design. If the task calls for a polished or Claude-style HTML doc, the file must include real presentational styling — typography, spacing, color, layout treatment, and responsive behavior — not just black text on white background with headings and tables. Before handing off, inspect the generated HTML for a real styling mechanism (`<style>` block or linked stylesheet) and verify that the rendered page looks intentionally designed rather than merely valid.

For planning/spec documents in particular, default to an editorial treatment: a strong hero/title section, readable measure, section rhythm, polished tables/cards, and mobile-safe spacing. If a user complains that an HTML plan "has no styles" or asks for a richer design pass, treat that as a failure of the artifact, not a subjective nice-to-have.

For generated **product UI mockups** (especially portfolio-style desktop/mobile app concepts), preserve the user's requested aesthetic but actively guard against drift into unreadable concept art. If a first pass is gorgeous but too abstract, run a second pass that explicitly pushes:
- stronger UI legibility
- more believable product realism
- faithful information architecture
- reduced haze / fake reflections / dramatic camera distortion

Keep both passes when the user may want to compare polish versus realism. See `references/ui-product-mockup-second-pass-pattern.md` for a reusable correction block.

When a session produces **many related mockups or reference images**, do not leave the comparison buried in chat scrollback. Produce a single review artifact — usually a self-contained HTML board — that groups variants by source/pass, labels them lightly, and makes side-by-side judgment easy. Prefer embedded images (data URLs) when the review file should remain portable or openable without the original local server/runtime.

Useful board sections for UI exploration:
- reference inputs
- native/generated first pass
- tightened or second-pass variants
- external polished exports
- broader brainstorming set

See `references/mockup-review-board-pattern.md` for the structure and portability rules.

## Popular Design Systems

Use brand/system-inspired templates when the user names a product aesthetic or asks for high-fidelity inspiration. Borrow layout language, spacing, motion/static cues, and typography spirit without claiming official affiliation.

## DESIGN.md

Use DESIGN.md when the deliverable is a design-token/spec document. Keep colors, typography, components, and token types structured and machine-readable enough to export or validate.

## Architecture and Excalidraw Diagrams

Use architecture diagrams for polished dark SVG/HTML system diagrams. Use Excalidraw when editability, hand-drawn style, or flow/sequence sketching matters. For diagrams, layout clarity beats decoration: group systems, label edges, and make data/control flow legible.

When a README or ops doc needs a big-picture infrastructure/deployment map, do not force a dense Mermaid diagram if it becomes hard to read. For multi-zone systems that mix repo structure, DNS, services, hosts, ports, CI/deploy flows, and future API calls, produce a polished self-contained HTML/SVG diagram under `docs/` and link to it from the README with a concise table. See `references/readable-infrastructure-architecture-diagrams.md` for the pattern, color semantics, and verification checklist.

## Game-design documents and MVP planning artifacts

When a broad game concept becomes provisional design direction, produce a real artifact rather than leaving the design buried in chat. See `references/critterbox-gdd-mvp-planning-pattern.md` for the Critterbox pattern.

Useful defaults for solo-dev/AI-assisted game concepts:
- Create a polished HTML GDD for design decisions and a separate Markdown implementation plan for execution.
- Push for a small playable loop before content scale or art polish.
- Treat web as a low-friction sharing target unless the user states it is a hard requirement.
- Prefer wireframe-first prototypes and pure/testable simulation logic when the core risk is gameplay design.

## Common Pitfalls

1. **Only describing the design.** Produce an artifact file.
2. **Using one variant when the ask is exploratory.** Sketch tasks should compare alternatives.
3. **Choosing SVG when editability is required.** Use Excalidraw JSON for editable hand-drawn diagrams.
4. **Copying brand too literally.** Use inspiration patterns, not counterfeit assets.
5. **Skipping preview/validation.** Open/render/check files when tools allow.

## Verification Checklist

- [ ] Artifact route selected.
- [ ] Actual output file written.
- [ ] File validates/renders or has structurally valid JSON/Markdown.
- [ ] Final response includes path/URL and any usage notes.
