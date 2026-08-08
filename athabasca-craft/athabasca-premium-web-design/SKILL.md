---
name: athabasca-premium-web-design
description: Audit, critique, and upgrade websites to agency-quality, "sizzle-factor" digital experiences. Uses production-grade animation (GSAP, Motion, scroll effects), 3D isometric visuals, cinematic micro-interactions, and a 100-point quality rubric to transform sites from generic to memorable.
version: 1.0.0
triggers:
  - User wants to critique, audit, or upgrade a website's design quality
  - User wants to make a site feel premium, agency-quality, or "sizzle"
  - User references motion, animation, scroll effects, or 3D for a website
  - User wants to add "wow factor" or "polish" to a landing page
  - User shows a website that feels generic, templated, or needs differentiation
  - User wants recommendations for GSAP, Motion.dev, or production animation
  - User asks for web design inspiration, especially isometric/technical visuals
metadata:
  hermes:
    tags: [athabasca, web-design, premium, animation, gsap, motion, scroll-effects, 3d, isometric, critique, audit, sizzle]
    related_skills: [claude-design, excalidraw, architecture-diagram, manim-video, motion-graphics-storytelling]
---

# Athabasca Premium Web Design

## Purpose

Transform websites from **functional to unforgettable**. This skill acts as a creative director and technical architect for premium web experiences — the kind that make visitors pause, scroll slowly, and remember the brand.

Use this when:
1. **Auditing** existing sites against a quality rubric
2. **Critiquing** design decisions and identifying missed opportunities
3. **Specifying** upgrades with concrete animation, 3D, and interaction patterns
4. **Building** new sites that feel expensive, intentional, and agency-grade

The philosophy: **Flashy but fitting**. Animations should amplify the message, not distract from it. Every effect should feel like it "belongs" to the brand's story.

## Prime Directive

**"Agency quality means every pixel is considered, every animation is weighted, and every interaction reinforces the brand's authority."**

Generic sites feel assembled. Premium sites feel *authored*.

## The Three-Layer Quality Model

Before critiquing or building, understand which layer needs attention:

### Layer 1: Visual Foundation (Static)
- Typography hierarchy and pairing
- Color palette restraint and intent
- Spacing system and breathing room
- Image quality and consistency
- Layout confidence (grid, asymmetry, negative space)

### Layer 2: Interaction Polish (Motion)
- Micro-interactions on buttons/links
- Scroll-triggered reveals
- Hover states with weight and timing
- Loading states and transitions
- Cursor/attention feedback

### Layer 3: The "Sizzle" (Signature)
- 3D isometric elements (for technical/architectural sites)
- Full-section scroll animations
- Canvas/WebGL integrations
- Video integration with scroll scrubbing
- Custom cursor effects

Most sites fail at Layer 1. Some reach Layer 2. The memorable ones own Layer 3 with restraint.

## The Premium Web Audit Rubric

Score any website 0-100 across 10 dimensions (10 points each):

| Dimension | 0-3 | 4-6 | 7-10 | What to Look For |
|-----------|-----|-----|------|------------------|
| **Typography Authority** | Generic system fonts, no hierarchy | One decent font pair, basic sizes | Editorial pairing, dramatic scale, intentional weights | Headlines that command; body that breathes; monospace for data |
| **Color Restraint** | Rainbow gradients, no system | Basic palette, safe choices | Chromatic confidence: 1-2 accents max, purposeful neutrals | Dark modes feel expensive; every color earns its place |
| **Spatial Confidence** | Cramped, no breathing room | Adequate padding, safe grids | Generous negative space, intentional asymmetry | Premium = unused space; luxury needs room |
| **Animation Weight** | None or jarring defaults | Basic hovers, some fades | Custom easing, staggered reveals, scroll choreography | GSAP/Motion.dev quality; never CSS defaults |
| **Micro-Interaction Detail** | Basic color change on hover | Scale or opacity shifts | Magnetic buttons, text shifts, stateful feedback | The small moments that feel *considered* |
| **Scroll Experience** | Static blocks, no reveal | Basic fade-ins | Staggered entrances, parallax depth, scroll-driven progress | Motion should reward scrolling |
| **3D/Technical Visuals** | Flat stock imagery only | Basic CSS transforms | Isometric diagrams, 3D product views, scroll-rotating elements | Technical products deserve dimensional treatment |
| **CTA Clarity** | Buried buttons, weak contrast | Clear but generic | Commanding presence, magnetic pull, contextual relevance | The button should feel inevitable |
| **Responsive Craft** | Broken mobile, desktop-only | Functional mobile | Mobile-first elegance, touch-optimized interactions | Premium on every device |
| **Brand Coherence** | Scattered, inconsistent | Recognizable | Every element reinforces a singular aesthetic vision | You'd know this brand in the dark |

**Scoring Guide:**
- **90-100:** Exceptional; publish and study
- **75-89:** Strong foundation; minor polish needed
- **60-74:** Viable but ordinary; significant upgrades needed
- **45-59:** Weak; rebuild the premise
- **0-44:** Start over

## Design Aesthetic Presets

When specifying or critiquing, reference these archetypes:

### Preset A: "Institutional Dark" (Hyperliquid Style)
- **Identity:** Control room meets editorial luxury
- **Palette:** Deep forest black (#0a1512), mint/cyan glow (#a8f0d8), off-white text
- **Typography:** Editorial serif (Freight, Canela) + clean sans (Inter, SF Pro)
- **Signature:** 3D isometric architecture diagrams, glowing geometric forms
- **Best for:** Technical infrastructure, developer tools, financial platforms

### Preset B: "Cinematic Light" (Pear Style)
- **Identity:** Film studio aesthetic, slow reveals, intentional pacing
- **Palette:** Warm whites, subtle gradients, single accent color
- **Typography:** Dramatic display serif + technical monospace
- **Signature:** Scroll-driven video scrubbing, full-bleed imagery
- **Best for:** Creative agencies, portfolios, storytelling brands

### Preset C: "Neon Biotech"
- **Identity:** Genome lab inside Tokyo nightclub
- **Palette:** Deep void (#0a0a14), plasma purple (#7b61ff), ghost white
- **Typography:** Sora, Instrument Serif, Fira Code
- **Signature:** Bioluminescent glow effects, scanning animations
- **Best for:** AI/ML products, biotech, futuristic tech

### Preset D: "Organic Luxury"
- **Identity:** Botanical research meets high fashion
- **Palette:** Moss green (#2e4036), clay accent (#cc5833), cream background
- **Typography:** Plus Jakarta Sans + Cormorant Garamond italic
- **Signature:** Living textures, growth animations, natural motion curves
- **Best for:** Wellness, sustainability, premium lifestyle

### Preset E: "Brutalist Signal"
- **Identity:** Control room for the future — raw, precise
- **Palette:** Paper (#e8e4dd), signal red (#e63b2e), pure black
- **Typography:** Space Grotesk + DM Serif Display
- **Signature:** Sharp geometry, data visualization, no decorative fluff
- **Best for:** Industrial, developer-focused, precision engineering

## Production-Grade Animation Stack

### Required Tools (Use These, Not Defaults)

| Effect Type | Library | Why |
|-------------|---------|-----|
| Scroll-triggered | GSAP ScrollTrigger | Pinning, scrubbing, progress-based animation |
| Complex sequences | GSAP Timeline | Choreographed multi-element reveals |
| Simple springs | Motion (Framer Motion for web) | React-native feel, gesture support |
| 3D/Isometric | Three.js / React Three Fiber | Interactive 3D, camera control |
| SVG path animation | GSAP DrawSVGPlugin | Line drawings, connector animations |
| Text reveals | GSAP SplitText | Character/word/line stagger control |

### Never Use
- CSS `@keyframes` for complex sequences
- `jquery.animate` (outdated, poor performance)
- Generic page transition libraries without customization
- Unoptimized Lottie files for simple animations

## Signature Animation Patterns

### Pattern 1: "Architectural Reveal" (for Technical Sites)
**What:** 3D isometric diagram that builds layer-by-layer on scroll
**Tech:** Three.js + GSAP ScrollTrigger
**Timing:** Each layer reveals every 20% of scroll progress
**Easing:** `power2.inOut` for smooth, professional feel
**Example Use:** Platform architecture, API layers, tech stack visualization

### Pattern 2: "The Magnetic Island"
**What:** Navbar that morphs from transparent to floating pill on scroll
**Tech:** GSAP + IntersectionObserver
**States:** 
- Hero: Transparent, light text, no background
- Scrolled: `bg-opacity-60 backdrop-blur-xl`, border, primary text
**Easing:** `power2.out` for smooth transition

### Pattern 3: "Staggered Text Entrance"
**What:** Headlines that reveal word-by-word or line-by-line
**Tech:** GSAP SplitText + ScrollTrigger
**Timing:** 0.08s stagger between elements
**Movement:** `y: 40 → 0`, `opacity: 0 → 1`
**Easing:** `power3.out`

### Pattern 4: "Diagnostic Shuffler"
**What:** Three overlapping cards that cycle vertically with spring physics
**Tech:** Motion or GSAP with spring easing
**Animation:** `cubic-bezier(0.34, 1.56, 0.64, 1)` for bounce
**Timing:** 3-second cycle, infinite
**Use:** Feature highlights, value propositions

### Pattern 5: "Telemetry Typewriter"
**What:** Live monospace feed that types messages character-by-character
**Tech:** GSAP or custom React with requestAnimationFrame
**Details:** Blinking accent-colored cursor, "Live Feed" label with pulsing dot
**Use:** Data processing, real-time features, technical credibility

### Pattern 6: "Cursor Protocol"
**What:** Animated SVG cursor that moves through a UI grid, clicks, activates
**Tech:** SVG path + GSAP MotionPath
**Sequence:** Enter → Move to cell → Press (scale 0.95) → Highlight → Move to button → Fade
**Use:** Scheduling, workflow visualization, product demos

### Pattern 7: "Stacking Archive"
**What:** Full-screen cards that stack as you scroll, with blur and scale on previous cards
**Tech:** GSAP ScrollTrigger with `pin: true`
**Effect:** New card enters → Previous scales to 0.9, blurs 20px, fades to 0.5
**Use:** Process steps, case studies, portfolio pieces

### Pattern 8: "Scanning Laser"
**What:** Horizontal line that traverses a grid or waveform
**Tech:** SVG line + GSAP translateX
**Details:** Subtle glow, occasional data points revealed
**Use:** Analysis, scanning, audio visualization

## Cinematic Micro-Interaction Catalog

Every interactive element needs intentionality:

### Buttons
- **Magnetic hover:** Element subtly follows cursor within 20px radius
- **Press state:** `scale(0.97)` with `cubic-bezier(0.25, 0.46, 0.45, 0.94)`
- **Fill animation:** Background color slides in from left on hover
- **Text shift:** Label moves `y: -2px` on hover

### Links
- **Underline draw:** Line draws from center outward on hover
- **Lift:** `translateY(-2px)` with shadow increase
- **Color morph:** Smooth transition to accent color

### Cards
- **Tilt on hover:** Subtle 3D rotation following cursor position (max 5deg)
- **Lift and shadow:** `translateY(-4px)` + shadow expansion
- **Border glow:** Accent-colored border appears or intensifies

### Navigation
- **Active indicator:** Animated underline or dot that moves between items
- **Dropdown reveal:** Staggered fade-up of menu items (0.05s between)
- **Mobile menu:** Full-screen takeover with theatrical reveal

## The Scroll Experience Blueprint

### Hero Section (100dvh)
- Full-bleed background image or video
- Heavy gradient overlay (primary-to-black)
- Content positioned deliberately (not just centered)
- Staggered entrance: background → headline → subhead → CTA
- Consider scroll-linked video scrubbing for cinematic effect

### Feature Sections
- Alternating asymmetrical layouts (don't just stack everything center)
- Scroll-triggered reveals with stagger
- Mix of static and animated content — not everything needs to move
- 3D isometric diagrams for technical products
- "Sticky" elements that hold while content scrolls past

### CTA Sections
- High contrast background shift
- Commanding typography scale
- Single, clear action
- Social proof or urgency elements

### Footer
- Deep background color, generous padding
- Rounded top corners (`rounded-t-[4rem]`) for visual "lift"
- Grid layout with clear hierarchy
- "System Operational" indicator or similar personality detail

## Technical Implementation Standards

### Performance Budget
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3s
- Cumulative Layout Shift: < 0.1
- Animation frame rate: Consistent 60fps

### Accessibility Requirements
- `prefers-reduced-motion` media query respected — disable all non-essential animations
- Focus states visible and styled
- Keyboard navigation fully supported
- Color contrast WCAG AA minimum
- Screen reader announcements for dynamic content

### Code Quality
- Use `gsap.context()` within `useEffect` for all animations
- Always return `ctx.revert()` in cleanup functions
- Avoid animating `width`, `height`, `top`, `left` — use `transform`
- Throttle scroll listeners
- Lazy-load heavy animation libraries

## The Audit Workflow

### Step 1: First Impression (10 seconds)
- What's the immediate emotional response?
- Does it feel templated or authored?
- Is the value proposition clear without scrolling?

### Step 2: Static Quality Check
- Typography: Does it feel editorial?
- Color: Is the palette restrained?
- Space: Is there confident negative space?
- Images: Are they purposeful or filler?

### Step 3: Motion Assessment
- Are there any meaningful animations?
- Do they feel weighted or default?
- Is scroll rewarding or static?
- Are micro-interactions present?

### Step 4: The "Sizzle" Gap Analysis
- What signature element is missing?
- Could 3D/isometric visuals strengthen the message?
- Are there missed opportunities for scroll storytelling?
- Does the CTA command attention?

### Step 5: Score and Prioritize
- Score against the rubric
- Identify the highest-impact upgrades
- Balance flash with fit — every effect should serve the brand

## Output Formats

### For Audits:
```markdown
## Premium Audit: [Site Name]

**Overall Score:** XX/100

**Dimension Breakdown:**
| Dimension | Score | Notes |
|-----------|-------|-------|
| Typography Authority | X/10 | ... |
| ... | ... | ... |

**Strongest Element:** ...
**Biggest Gap:** ...

**Priority Upgrades:**
1. [High impact, concrete recommendation]
2. [Medium impact, technical specification]
3. [Nice-to-have with implementation notes]

**Animation Specifications:**
- [Pattern name] for [section]: [technical details]
```

### For New Builds:
```markdown
## Design Direction: [Project]

**Aesthetic Preset:** [A/B/C/D/E]

**Signature Elements:**
- [Pattern 1] for [purpose]
- [Pattern 3] for [purpose]

**Animation Stack:**
- GSAP ScrollTrigger for [specific use]
- Motion for [specific use]

**Rubric Targets:**
- Typography Authority: 9/10 (serif/sans pairing, dramatic scale)
- Animation Weight: 9/10 (custom easing, staggered reveals)
- [etc.]
```

## Anti-Patterns (Never Do These)

1. **"Everything moves"** — Visual chaos, no hierarchy
2. **Generic scroll libraries** — Same fade-in everyone uses
3. **Decorative animation** — Motion that doesn't serve understanding
4. **Stock photo overload** — No visual identity
5. **Wall of text** — No typographic hierarchy
6. **Rainbow gradients** — No color discipline
7. **Ignored mobile** — Premium only on desktop
8. **No loading states** — Jarring content appearance
9. **Accessibility afterthought** — `prefers-reduced-motion` ignored
10. **CTA burial** — Making conversion difficult

## References

See `references/` directory for:
- `animation-pattern-library.md` — Detailed GSAP/Motion implementations
- `rubric-scorecard.md` — Printable audit worksheet
- `3d-isometric-guide.md` — Three.js integration patterns
- `micro-interaction-catalog.md` — CSS/JS snippets for common effects
- `performance-checklist.md` — Optimization guidelines
