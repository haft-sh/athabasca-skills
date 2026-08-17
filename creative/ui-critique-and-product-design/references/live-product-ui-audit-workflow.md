# Live Product UI Audit Workflow

Use this when the user wants a UI audit of a real running app rather than a static mockup.

## Goal

Produce evidence-backed critique from the actual product surfaces, including onboarding, primary workspace states, menus/popovers, and scrolled panel states.

## Workflow

1. **Capture the empty-state / onboarding path if it exists.**
   - If the app normally opens into a populated workspace, launch an isolated instance or separate profile/home directory so onboarding can be captured too.
   - For local-first apps, a clean config/home is often enough to reveal first-run setup.

2. **Capture the normal populated workspace.**
   - Seed minimal representative content if the product would otherwise be visually empty.
   - Prefer a small set of realistic fixtures that exercise navigation, reading, metadata, search, or details panels.

3. **Capture every major surface class, not just the main screen.**
   - onboarding / empty state
   - primary workspace
   - menus
   - popovers / dropdowns
   - creation/import flows
   - settings or selectors if they materially affect orientation
   - deep-scroll states of long panels

4. **Capture scroll states explicitly.**
   - For multi-panel apps, take separate evidence of scrolled left-nav, main-content, and right-inspector states.
   - Deep-scroll screenshots often reveal orientation, density, and section-labeling problems that top-of-page screenshots hide.

5. **Use deterministic capture tooling when possible.**
   - Browser screenshots or Playwright captures are preferable to ad hoc manual descriptions.
   - Save a numbered screenshot set so later critique can refer to surfaces consistently.

6. **Audit by surface, then synthesize.**
   - First critique each major surface individually.
   - Then produce a product-level summary with recurring themes, priority ordering, and rewrite suggestions.

## Practical notes

- If the live app is too empty to audit meaningfully, creating a few local sample documents/artifacts can be the right move; call out that they are audit fixtures, not product changes.
- Menus and popovers are easy to miss in audits; capture them deliberately.
- For apps with independent scroll containers, do not rely on page-level scrolling alone.
- Keep the final summary focused on class-level design issues: mode clarity, hierarchy, flow, copy, trust, and density — not only one screenshot at a time.

## Good final deliverables

- numbered screenshot set
- written audit by surface
- cross-surface summary
- prioritized fix list
- suggested copy rewrites for the most confusing labels or actions
