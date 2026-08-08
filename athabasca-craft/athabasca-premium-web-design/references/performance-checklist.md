# Performance & Accessibility Checklist

Before shipping premium web experiences, verify these critical items.

---

## Performance Budget

| Metric | Target | Maximum |
|--------|--------|---------|
| First Contentful Paint (FCP) | < 1.0s | 1.5s |
| Largest Contentful Paint (LCP) | < 1.5s | 2.5s |
| Time to Interactive (TTI) | < 2.0s | 3.0s |
| Cumulative Layout Shift (CLS) | < 0.05 | 0.1 |
| First Input Delay (FID) | < 50ms | 100ms |
| Total Blocking Time (TBT) | < 200ms | 300ms |
| Time to First Byte (TTFB) | < 200ms | 600ms |

---

## Animation Performance

### ✅ DO

- [ ] Use `transform` and `opacity` for animations (GPU accelerated)
- [ ] Use `will-change` sparingly and remove after animation
- [ ] Throttle scroll listeners to 60fps (16ms)
- [ ] Use `requestAnimationFrame` for smooth animations
- [ ] Clean up GSAP ScrollTriggers on component unmount
- [ ] Lazy-load heavy animation libraries
- [ ] Test on low-end devices
- [ ] Use CSS animations for simple transitions

### ❌ DON'T

- [ ] Animate `width`, `height`, `top`, `left` (triggers layout)
- [ ] Animate `filter: blur()` during scroll
- [ ] Use `setState` in mousemove handlers without throttling
- [ ] Create unlimited ScrollTriggers without cleanup
- [ ] Animate expensive properties simultaneously
- [ ] Ignore 60fps target on complex scenes

---

## Reduced Motion

### ✅ MUST SUPPORT

- [ ] Detect `prefers-reduced-motion` media query
- [ ] Provide instant or simple alternatives for all animations
- [ ] Respect system preference automatically
- [ ] Test with reduced motion enabled

### Implementation

```javascript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (prefersReducedMotion) {
  // Instant state changes
  gsap.set(elements, { opacity: 1, y: 0, x: 0 });
} else {
  // Full animations
  gsap.from(elements, { y: 40, opacity: 0, duration: 0.8 });
}
```

---

## Accessibility Checklist

### Focus Management

- [ ] All interactive elements have visible focus states
- [ ] Focus order matches visual order
- [ ] No focus traps without escape mechanism
- [ ] Skip-to-content link present
- [ ] Focus indicators visible against all backgrounds

### Keyboard Navigation

- [ ] All functionality available via keyboard
- [ ] Tab order is logical and predictable
- [ ] Dropdown menus operable with arrow keys
- [ ] Modal dialogs trap focus and close on Escape
- [ ] No keyboard-only dead ends

### Screen Readers

- [ ] Proper heading hierarchy (h1 → h2 → h3)
- [ ] Alt text on all meaningful images
- [ ] Decorative images hidden from AT
- [ ] Form labels properly associated
- [ ] Status messages announced via ARIA live regions
- [ ] Skip links for repetitive content
- [ ] Landmark regions (main, nav, aside, footer)

### Color & Contrast

- [ ] WCAG AA compliance (4.5:1 for normal text, 3:1 for large text)
- [ ] WCAG AAA compliance for critical text (7:1)
- [ ] Color not sole means of conveying information
- [ ] Focus indicators meet 3:1 contrast ratio
- [ ] Tested with color blindness simulators

---

## Image Optimization

### Format Strategy

| Image Type | Recommended Format | Fallback |
|------------|-------------------|----------|
| Photographs | AVIF | WebP → JPEG |
| Logos/Icons | SVG | (none needed) |
| Illustrations | SVG or AVIF | PNG |
| Screenshots | AVIF | WebP → PNG |

### Sizing Requirements

- [ ] Responsive images with `srcset`
- [ ] Correct `sizes` attribute
- [ ] Lazy loading for below-fold images
- [ ] `width` and `height` attributes to prevent layout shift
- [ ] Blur-up placeholder for hero images

### Implementation

```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img 
    src="image.jpg" 
    alt="Descriptive text"
    width="800"
    height="600"
    loading="lazy"
    decoding="async"
  >
</picture>
```

---

## Font Loading

### Strategy

- [ ] Self-host fonts when possible
- [ ] Use `font-display: swap` to prevent invisible text
- [ ] Preload critical fonts
- [ ] Subset fonts to only needed characters
- [ ] Limit font weights/styles (max 4-6 variants)

### CSS

```css
@font-face {
  font-family: 'Custom Font';
  src: url('/fonts/custom.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
```

---

## Code Splitting

### Bundle Strategy

- [ ] Route-based code splitting
- [ ] Component-level lazy loading for heavy features
- [ ] Dynamic imports for non-critical features
- [ ] Vendor bundle separation

### Implementation

```javascript
// Lazy load heavy 3D scene
const Heavy3DScene = lazy(() => import('./Heavy3DScene'));

<Suspense fallback={<Placeholder />}>
  <Heavy3DScene />
</Suspense>

// Dynamic import for optional features
const analytics = await import('./analytics');
```

---

## Caching Strategy

### Static Assets

- [ ] Immutable cache for versioned assets (1 year)
- [ ] Proper cache headers for different asset types
- [ ] Service Worker for offline support (optional)

### HTML

- [ ] Revalidate with stale-while-revalidate pattern
- [ ] ETags for conditional requests

---

## 3D/Animation Library Loading

### Priorities

1. **Critical path:** No 3D on initial load
2. **After LCP:** Load animation libraries
3. **On interaction:** Load 3D scenes
4. **Prefetch:** Next route's assets

### Loading Strategy

```javascript
// Defer heavy libraries
const [gsap, ScrollTrigger] = await Promise.all([
  import('gsap').then(m => m.default),
  import('gsap/ScrollTrigger').then(m => m.ScrollTrigger)
]);

gsap.registerPlugin(ScrollTrigger);
```

---

## Testing Checklist

### Device Testing

- [ ] iOS Safari (latest)
- [ ] Android Chrome (latest)
- [ ] macOS Safari
- [ ] Windows Chrome/Edge
- [ ] iPad/tablet

### Network Testing

- [ ] Fast 4G
- [ ] Slow 4G (1.6 Mbps)
- [ ] 3G (400ms latency)

### Accessibility Testing

- [ ] VoiceOver (macOS/iOS)
- [ ] NVDA (Windows)
- [ ] Keyboard-only navigation
- [ ] Reduced motion preference
- [ ] High contrast mode
- [ ] 200% zoom

### Animation Testing

- [ ] Consistent 60fps
- [ ] Smooth on low-end devices
- [ ] No jank on scroll
- [ ] Reduced motion alternatives work
- [ ] No memory leaks (long-running sessions)

---

## Tools

### Performance
- Lighthouse (CI integration)
- WebPageTest
- Chrome DevTools Performance panel
- `web-vitals` library for RUM

### Accessibility
- axe DevTools
- Lighthouse accessibility audit
- Screen reader testing
- Keyboard navigation testing

### Animation
- Chrome DevTools Animations panel
- Chrome DevTools Rendering panel
- `gsap.context()` for cleanup verification

---

## Pre-Launch Verification

```markdown
- [ ] Performance budget met
- [ ] Accessibility audit passed
- [ ] Animation performance verified
- [ ] Reduced motion support implemented
- [ ] Responsive testing complete
- [ ] Cross-browser testing complete
- [ ] Image optimization complete
- [ ] Font loading optimized
- [ ] SEO meta tags present
- [ ] Favicon and PWA icons ready
- [ ] Analytics integrated (if required)
- [ ] Error boundaries implemented
- [ ] Loading states designed
- [ ] 404 page styled
```
