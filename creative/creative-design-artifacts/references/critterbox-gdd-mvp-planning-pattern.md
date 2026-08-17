# Critterbox v0 GDD + MVP planning pattern

Use this pattern when JP wants to turn a broad game concept into a provisional design document and early implementation plan.

## Design stance

- Push for a tight MVP. For solo-dev/AI-assisted game projects, the main risk is scope and balance complexity, not asset production.
- Separate the fantasy from the implementable loop. For Critterbox, the validated initial loop is: map node → draft/reward → grid layout → deterministic battle → return to map.
- Prefer core-loop validation before art/UI polish.
- If web is proposed as the platform, treat it as a low-friction sharing/distribution choice unless JP says it is a hard requirement.

## GDD artifact shape

Persist a polished HTML GDD when the design discussion crosses from brainstorming into provisional decisions. The HTML should capture:
- core thesis
- MVP constraints
- win condition
- battle model
- board/formation model
- resource/status vocabulary
- initial content sketches
- open questions

For Critterbox, important class-level game-design decisions from the session:
- no trainer/face abstraction if a better fiction exists
- Army HP can represent the total health of all active critters
- critters may contribute HP without being individually killable in MVP
- geometry/squad icons can carry rules more cleanly than long conditional text
- visible percentage math should be avoided when simple named effects work: Haste, Slow, Freeze, Crit, cooldown -1s

## Implementation planning stance

For first playable plans:
- Recommend a pure deterministic simulation engine separated from the UI.
- Use a wireframe UI until the loop is fun.
- Keep backend out of the first prototype unless absolutely needed.
- For shareable early prototypes, TypeScript + Vite + React DOM is often a better first step than Phaser/Pixi because card/grid UI is not rendering-bound.
- Keep the engine platform-agnostic so web-first does not become web-only.

## Content-scope guardrail

AI can generate lots of cards/art, but that does not solve balance. Start with a tiny hand-curated card pool and one color/faction. Add more colors only after mirror matches are fun and debuggable.
