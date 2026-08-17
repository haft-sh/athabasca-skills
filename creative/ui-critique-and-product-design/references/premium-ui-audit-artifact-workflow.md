# Premium UI audit artifact workflow

Use this reference when the user wants more than critique text: a complete audit package with screenshots, redesign direction, and polished before/after concepts.

## When to use

Use this workflow when the user asks for any of the following:
- a full product UI audit rather than comments on one screenshot
- an HTML or shareable deliverable that combines findings in one place
- before/after redesign proposals
- generated concept images that illustrate the critique

## Recommended execution sequence

1. **Audit the live product, not just memory**
   - Capture the real current interface.
   - Include onboarding or empty state, primary populated workspace, menus/popovers/selectors, and important scrolled states.
   - If the product is empty, seed minimal representative fixtures so populated states are audit-able.

2. **Cover the full communication surface**
   - Do not stop at the obvious home screen.
   - Capture hidden or transient surfaces: command palettes, menus, import flows, new-item dialogs, selectors, inspector rails, and long-scroll states.

3. **Critique by screen and by system**
   - First critique each surface.
   - Then synthesize cross-cutting issues such as unclear product mode, overloaded navigation, weak hierarchy, dense inspector rails, or system-centric wording.

4. **Turn findings into deliverables**
   - Produce:
     - executive summary
     - screen-by-screen critique
     - concrete rewrite suggestions
     - redesign direction
     - prioritized implementation backlog

5. **Generate visual proposals when requested**
   - For each major flaw, generate:
     - a before/problem illustration
     - an after/proposal illustration
   - Pair each image with a short explanation of what the image demonstrates.

6. **Be precise about image-model limits**
   - If the backend is text-to-image only, describe the results as **concept mockups** or **proposal illustrations**.
   - Do not imply the model edited the original screenshot faithfully unless there is a real image-editing path.
   - If generation succeeds only partially due to quota or provider limits, say so explicitly and mark missing visuals as pending rather than pretending the set is complete.

7. **Package the output in one artifact**
   - Prefer a self-contained HTML report that combines:
     - screenshots
     - findings
     - rewritten copy
     - redesign recommendations
     - implementation backlog
     - generated before/after visuals
   - Publish or place the artifact where the user can open it directly.

8. **Verify the deliverable**
   - Open the generated artifact and inspect that the content actually renders.
   - Confirm the publish/copy target exists.
   - If anything is partial, label it clearly in the artifact itself, not only in chat.

## Common pitfalls

- Auditing only the first visible screen and missing menus, selectors, or deep-scroll states.
- Giving design opinions without translating them into copy, layout, or priority changes.
- Saying generated concepts are "edits" when they are only fresh text-to-image compositions.
- Delivering screenshots and prose separately instead of in one navigable artifact.
- Hiding quota or provider failures instead of marking the artifact as partial.

## Deliverable standard

A strong premium audit artifact should let a product team answer all of these without rereading the chat:
- What is the app trying to do?
- What currently works?
- What is broken or confusing?
- What should change first?
- What should the improved UI roughly look like?
