# Premium audit deliverable patterns

Use this reference when a user wants more than critique text — especially when they want a single polished artifact they can review or share.

## Default deliverable shape

Prefer one self-contained HTML artifact that combines:
- executive summary
- screen-by-screen critique
- specific rewrite suggestions
- layout/hierarchy recommendations
- ranked implementation backlog
- captured screenshots of the real product surfaces
- generated concept mockups for the major flaws

For desktop app audits, the minimum screenshot set should usually include:
- onboarding or empty state
- main populated workspace
- menus / popovers / selectors
- representative scrolled states of dense panels or inspectors

## Visual proposal requirement

When the user asks for redesign proposals, include **before/problem** and **after/proposal** visuals for each major flaw when image generation capacity allows.

Treat generated images as concept illustrations unless you have a true image-editing path that preserves the original UI exactly.

For each visual pair, explain:
- what the current flaw is
- what changed in the proposal
- why the change improves clarity, hierarchy, or task flow

## Default major-flaw buckets for productivity/workspace apps

When the audit surfaces these problems, they usually warrant their own mockup pair:
1. unclear primary mode / weak statement of what the screen is for
2. overloaded navigation or left rail
3. over-dense inspector / details rail
4. confusing creation/import entry points
5. weak deep-scroll orientation in long working panes

## Packaging pattern preferred by JP

When producing a serious UI audit for JP, bias toward a single publishable artifact rather than scattered notes.

Default packaging order:
1. capture real screenshots first
2. critique the actual UI
3. generate concept mockups for the major flaws
4. combine critique + screenshots + mockups into one HTML report
5. if remote hosting is available, publish the final artifact to a shareable URL

## Fallback behavior when image generation is blocked

If the image backend is quota-limited or otherwise blocked:
- include every successful mockup you did generate
- clearly mark which visual pairs are missing
- state the concrete blocker (for example 429 usage limit)
- do not imply that a full visual set exists when it does not
- if needed, fall back to HTML/CSS mockup panels for the missing proposals so the user still gets a concrete redesign direction

## Optional publish step

If the user wants the result viewable outside the local machine and credentials are already present, upload the final HTML artifact (and any supporting bundle if needed) to the configured remote target after local verification. Keep the publish step separate from the critique itself so an upload failure does not contaminate the audit conclusions.
