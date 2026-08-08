# Animation Pattern Library

Production-ready GSAP/Motion patterns with exact implementation details.

## Pattern: Staggered Text Reveal

**Purpose:** Headlines that reveal word-by-word or line-by-line on scroll

**GSAP Implementation:**
```javascript
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { SplitText } from 'gsap/SplitText';

gsap.registerPlugin(ScrollTrigger, SplitText);

const headline = document.querySelector('.headline');
const split = new SplitText(headline, { type: 'words,lines' });

gsap.from(split.words, {
  y: 40,
  opacity: 0,
  duration: 0.8,
  ease: 'power3.out',
  stagger: 0.08,
  scrollTrigger: {
    trigger: headline,
    start: 'top 80%',
    toggleActions: 'play none none reverse'
  }
});
```

**React/Motion Implementation:**
```jsx
import { motion } from 'framer-motion';

const words = headline.split(' ');

<motion.h1>
  {words.map((word, i) => (
    <motion.span
      key={i}
      initial={{ y: 40, opacity: 0 }}
      whileInView={{ y: 0, opacity: 1 }}
      transition={{ 
        duration: 0.8, 
        delay: i * 0.08,
        ease: [0.25, 0.46, 0.45, 0.94]
      }}
      viewport={{ once: true, margin: '-20%' }}
    >
      {word}{' '}
    </motion.span>
  ))}
</motion.h1>
```

**Timing:** 0.08s stagger between elements
**Easing:** `power3.out` or `[0.25, 0.46, 0.45, 0.94]`
**Trigger:** Start at 'top 80%' of viewport

---

## Pattern: Magnetic Button

**Purpose:** Button subtly follows cursor within radius on hover

**Implementation:**
```javascript
const button = document.querySelector('.magnetic-btn');

button.addEventListener('mousemove', (e) => {
  const rect = button.getBoundingClientRect();
  const x = e.clientX - rect.left - rect.width / 2;
  const y = e.clientY - rect.top - rect.height / 2;
  
  gsap.to(button, {
    x: x * 0.3,
    y: y * 0.3,
    duration: 0.3,
    ease: 'power2.out'
  });
});

button.addEventListener('mouseleave', () => {
  gsap.to(button, {
    x: 0,
    y: 0,
    duration: 0.5,
    ease: 'elastic.out(1, 0.3)'
  });
});
```

**React Hook:**
```jsx
const useMagnetic = (ref, strength = 0.3) => {
  useEffect(() => {
    const element = ref.current;
    if (!element) return;
    
    const handleMove = (e) => {
      const rect = element.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      
      gsap.to(element, {
        x: x * strength,
        y: y * strength,
        duration: 0.3,
        ease: 'power2.out'
      });
    };
    
    const handleLeave = () => {
      gsap.to(element, {
        x: 0,
        y: 0,
        duration: 0.5,
        ease: 'elastic.out(1, 0.3)'
      });
    };
    
    element.addEventListener('mousemove', handleMove);
    element.addEventListener('mouseleave', handleLeave);
    
    return () => {
      element.removeEventListener('mousemove', handleMove);
      element.removeEventListener('mouseleave', handleLeave);
    };
  }, [ref, strength]);
};
```

**Magnetic Radius:** 20-30px feel natural
**Easing on release:** `elastic.out(1, 0.3)` for satisfying snap-back

---

## Pattern: Scroll-Linked Progress

**Purpose:** Section progress indicator, image sequence scrubbing

**Implementation:**
```javascript
const section = document.querySelector('.pinned-section');
const progressBar = document.querySelector('.progress-fill');

gsap.to(progressBar, {
  scaleX: 1,
  ease: 'none',
  scrollTrigger: {
    trigger: section,
    start: 'top top',
    end: 'bottom bottom',
    scrub: 0.5,
    onUpdate: (self) => {
      console.log('Progress:', self.progress);
    }
  }
});
```

**Video Scrubbing:**
```javascript
const video = document.querySelector('video');

ScrollTrigger.create({
  trigger: '.video-section',
  start: 'top top',
  end: 'bottom bottom',
  pin: true,
  scrub: true,
  onUpdate: (self) => {
    if (video.duration) {
      video.currentTime = self.progress * video.duration;
    }
  }
});
```

**Scrub Value:** 0.3-0.5 for smooth but responsive
**Pinning:** Use sparingly — too many pinned sections feel heavy

---

## Pattern: Card Stack Scroll

**Purpose:** Full-screen cards that stack on scroll with blur/scale

**Implementation:**
```javascript
const cards = gsap.utils.toArray('.stack-card');

cards.forEach((card, i) => {
  if (i === cards.length - 1) return;
  
  ScrollTrigger.create({
    trigger: card,
    start: 'top top',
    end: 'bottom top',
    pin: true,
    pinSpacing: false,
    onUpdate: (self) => {
      const progress = self.progress;
      gsap.set(card, {
        scale: 1 - (progress * 0.1),
        filter: `blur(${progress * 20}px)`,
        opacity: 1 - (progress * 0.5)
      });
    }
  });
});
```

**Card Container:**
```css
.stack-container {
  position: relative;
}

.stack-card {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  z-index: var(--z-index);
}
```

**Z-Index:** Increment for each card (1, 2, 3, etc.)
**Scale on Scroll:** 0.9-0.95 feels natural
**Blur:** 15-20px max to maintain legibility

---

## Pattern: SVG Path Draw

**Purpose:** Animated line drawings, connector animations

**Implementation:**
```javascript
const path = document.querySelector('.draw-path');
const length = path.getTotalLength();

path.style.strokeDasharray = length;
path.style.strokeDashoffset = length;

gsap.to(path, {
  strokeDashoffset: 0,
  duration: 2,
  ease: 'power2.inOut',
  scrollTrigger: {
    trigger: path,
    start: 'top 70%',
    toggleActions: 'play none none reverse'
  }
});
```

**With DrawSVGPlugin (GSAP Club):**
```javascript
gsap.from('.draw-path', {
  drawSVG: 0,
  duration: 2,
  ease: 'power2.inOut',
  scrollTrigger: {
    trigger: '.draw-path',
    start: 'top 70%'
  }
});
```

**Duration:** 1.5-2s feels deliberate
**Easing:** `power2.inOut` for natural drawing feel

---

## Pattern: Parallax Depth

**Purpose:** Multi-layer scroll speed for depth perception

**Implementation:**
```javascript
const layers = document.querySelectorAll('.parallax-layer');

layers.forEach((layer, i) => {
  const speed = (i + 1) * 0.1;
  
  gsap.to(layer, {
    y: () => window.innerHeight * speed,
    ease: 'none',
    scrollTrigger: {
      trigger: '.parallax-section',
      start: 'top bottom',
      end: 'bottom top',
      scrub: true
    }
  });
});
```

**Speed Ranges:**
- Background: 0.2 (slower)
- Mid: 0.5 (normal)
- Foreground: 0.8 (faster)

---

## Pattern: Cursor Follower

**Purpose:** Custom cursor that follows mouse with lag

**Implementation:**
```javascript
const cursor = document.querySelector('.cursor');
let mouseX = 0, mouseY = 0;
let cursorX = 0, cursorY = 0;

document.addEventListener('mousemove', (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;
});

function animate() {
  cursorX += (mouseX - cursorX) * 0.15;
  cursorY += (mouseY - cursorY) * 0.15;
  
  cursor.style.transform = `translate(${cursorX}px, ${cursorY}px)`;
  requestAnimationFrame(animate);
}

animate();
```

**Lag Factor:** 0.1-0.2 feels smooth
**Size:** 20-40px typically
**State Changes:** Scale up on hoverable elements

---

## Pattern: Shuffling Cards

**Purpose:** Three cards that cycle vertically with spring physics

**Implementation:**
```javascript
const cards = ['Card 1', 'Card 2', 'Card 3'];
let currentIndex = 0;

function cycleCards() {
  const topCard = document.querySelector('.card-top');
  
  gsap.to(topCard, {
    y: -100,
    opacity: 0,
    duration: 0.4,
    ease: 'power2.in',
    onComplete: () => {
      currentIndex = (currentIndex + 1) % cards.length;
      // Update card content and reset position
      gsap.set(topCard, { y: 100, opacity: 0 });
      gsap.to(topCard, {
        y: 0,
        opacity: 1,
        duration: 0.5,
        ease: 'back.out(1.7)'
      });
    }
  });
}

setInterval(cycleCards, 3000);
```

**Spring Easing:** `back.out(1.7)` or `cubic-bezier(0.34, 1.56, 0.64, 1)`
**Cycle Time:** 3 seconds between changes
**Overlap:** 0.1s of simultaneous visibility

---

## Performance Notes

**Always:**
- Use `transform` and `opacity` for animations (GPU accelerated)
- Throttle scroll events
- Use `will-change` sparingly
- Clean up ScrollTriggers on unmount

**Never:**
- Animate `width`, `height`, `top`, `left` (triggers layout)
- Use `filter: blur()` on large areas during scroll
- Create unlimited ScrollTriggers without cleanup

**Reduced Motion:**
```javascript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (prefersReducedMotion) {
  // Disable or simplify animations
  gsap.set(elements, { opacity: 1, y: 0 });
} else {
  // Run full animation
}
```
