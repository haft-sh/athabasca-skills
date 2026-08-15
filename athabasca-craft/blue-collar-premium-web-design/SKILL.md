---
name: blue-collar-premium-web-design
description: Premium trade industry websites with GSAP and local copy.
version: 1.0.0
triggers:
  - User wants to create premium websites for trade industries
  - User mentions plumbing, HVAC, welding, electrical, or roofing sites
  - User wants "sizzle factor" or expensive-looking sites for blue-collar businesses
  - User asks for static HTML sites with GSAP animations
  - User wants real local copy for Billings, MT or similar markets
metadata:
  hermes:
    tags: [web-design, premium, blue-collar, trades, static-html, gsap, billings]
    related_skills: [athabasca-premium-web-design, cinematic-website-emulation]
---

# Blue Collar Premium Web Design

## Purpose

Guide for creating premium, agency-quality websites for trade/blue-collar industries in specific geographic markets. These sites are portfolio pieces designed to attract new clientele by demonstrating design capabilities.

## Key Principles

1. **Real Local Copy** — No lorem ipsum. Use actual service descriptions, phone numbers, and addresses for the target market.
2. **Premium Aesthetics for Trades** — These industries deserve the same design quality as tech or luxury brands.
3. **"Sizzle Factor"** — Sites must look expensive to impress potential clients and win new business.
4. **CSS-Only Visuals** — No external image dependencies. Use gradients, patterns, animations for visual interest.
5. **Single-File Architecture** — Each site is one `index.html` with inline CSS/JS for simplicity.

## Recommended Aesthetic Presets by Trade

| Trade | Preset | Why |
|-------|--------|-----|
| Plumbing | Institutional Dark (copper accents) | Copper pipes, premium feel |
| HVAC | Clean Blue/White (frost effects) | Ice, climate control, precision |
| Welding | Brutalist Signal (paper + red) | Industrial, raw, precise |
| Electrical | Neon Biotech (electric arcs) | Energy, power, futuristic |
| Roofing | Institutional Dark (mint glow) | Existing rooftop-pro style |

## Static HTML Site Structure

```
apps/<site-slug>/
├── index.html          # Single-file site with inline CSS/JS
├── site.config.json    # Cloudflare Pages project config
└── assets/             # Only if needed (images, videos)
```

## site.config.json Format

```json
{
  "site": "<site-slug>",
  "project": "<cloudflare-project-name>",
  "productionBranch": "main",
  "type": "static-pages"
}
```

## Required Elements

### Navigation
- Logo (text-based, no image)
- Service links
- Emergency/contact CTA button
- Scroll-triggered background change

### Hero Section
- 100vh height
- Bold headline with accent color
- Clear value proposition
- Primary CTA button
- Optional: phone number, stats, or diagram

### Services Grid
- 3-column grid (2 on tablet, 1 on mobile)
- Service cards with icons
- Hover effects (border glow, lift, color change)
- Real service descriptions

### Process/How It Works
- 3-4 step process
- Numbered steps
- Clear, concise descriptions

### CTA Section
- High contrast background
- Commanding headline
- Single, clear action
- Phone number prominent

### Footer
- Brand description
- Service links
- Service area (local cities)
- Contact information
- "System Operational" indicator

## GSAP Animation Patterns

### Hero Entrance
```javascript
gsap.from('.hero-label', { opacity: 0, y: 20, duration: 0.8, delay: 0.2 });
gsap.from('.hero h1', { opacity: 0, y: 30, duration: 1, delay: 0.4 });
gsap.from('.hero p', { opacity: 0, y: 20, duration: 0.8, delay: 0.6 });
gsap.from('.hero-cta', { opacity: 0, y: 20, duration: 0.8, delay: 0.8 });
```

### Service Cards Stagger
```javascript
gsap.from('.service-card', {
    scrollTrigger: { trigger: '.services-grid', start: 'top 80%' },
    opacity: 0, y: 40, stagger: 0.1, duration: 0.8
});
```

### Navigation Scroll Effect
```javascript
window.addEventListener('scroll', () => {
    const nav = document.querySelector('nav');
    if (window.scrollY > 50) {
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }
});
```

## Typography Pairings for Trades

| Trade | Display Font | Body Font | Mono Font |
|-------|--------------|-----------|-----------|
| Plumbing | Instrument Serif | Inter | JetBrains Mono |
| HVAC | DM Serif Display | Plus Jakarta Sans | Fira Code |
| Welding | DM Serif Display | Space Grotesk | JetBrains Mono |
| Electrical | Cormorant Garamond | Inter | Fira Code |

## Color Palettes

### Plumbing (Institutional Dark)
- Black: #0a1512
- Dark: #121f1a
- Copper: #b87333
- Copper Light: #d4956b
- Mint: #a8f0d8
- White: #f5f5f0
- Gray: #8a9a94

### HVAC (Clean Blue/White)
- Deep: #0a1a2e
- Navy: #0f2847
- Ice: #4fc3f7
- Ice Light: #81d4fa
- White: #f8fafc
- Gray: #94a3b8

### Welding (Brutalist Signal)
- Paper: #e8e4dd
- Cream: #f5f2ed
- Red: #e63b2e
- Black: #1a1a1a
- Gray: #6b6560

### Electrical (Neon Biotech)
- Void: #0a0a14
- Deep: #12121f
- Electric: #7b61ff
- Electric Light: #a78bfa
- Arc: #fbbf24
- White: #f8fafc
- Gray: #94a3b8

## Scrollytelling Pattern (for Electrical Sites)

The electrician site uses a cinematic scrollytelling pattern instead of the standard static layout. This creates a more dramatic, immersive experience.

### Key Differences from Standard Layout
1. **Single-viewport canvas** — Content layers are `position: fixed` with opacity transitions
2. **Virtual scroll engine** — Intercepts wheel events, maps to 0-1 timeline, lerps position
3. **CSS-only visuals** — Electric arc rings, floating particles, rotating animations
4. **Scroll-driven progress bar** — Shows position in the narrative

### CRITICAL: Body Overflow for Virtual Scroll Engines
```css
/* CORRECT - allows window.scrollTo() to work */
body {
  overflow-x: hidden;
  overflow-y: scroll;
  scrollbar-width: none; /* Firefox */
}
body::-webkit-scrollbar { display: none; } /* Chrome/Safari */
```

**WRONG** — will freeze the scroll engine:
```css
body { overflow: hidden; } /* BLOCKS window.scrollTo() */
```

**Why:** The scroll engine uses `window.scrollTo()` to sync native scroll with virtual position. `overflow: hidden` prevents this, so `window.scrollY` stays at 0 and the page appears frozen.

### App.tsx Pattern
- Remove any `document.body.style.overflow = 'hidden'` — CSS handles it
- ScrollEngine class intercepts wheel events and drives virtual scroll
- Layers use opacity transitions based on scroll progress
- No GSAP ScrollTrigger needed — custom scroll engine handles everything

## Deployment

All static sites deploy to Cloudflare Pages via `scripts/deploy_site.py`:

```bash
pnpm site:deploy <site-slug>
```

## Live Examples

| Site | URL | Preset |
|------|-----|--------|
| Summit Plumbing | https://summit-plumbing-mt.pages.dev | Institutional Dark |
| Glacier Mechanical | https://glacier-mechanical-mt.pages.dev | Clean Blue/White |
| Ironclad Welding | https://ironclad-welding-mt.pages.dev | Brutalist Signal |
| Current Electric | https://current-electric-mt.pages.dev | Neon Biotech (scrollytelling) |
