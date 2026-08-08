# Micro-Interaction Catalog

Production-ready CSS and JS snippets for polished interactions.

---

## Button Interactions

### Magnetic Button with Fill

**CSS:**
```css
.magnetic-btn {
  position: relative;
  padding: 1rem 2rem;
  background: transparent;
  border: 1px solid var(--accent);
  color: var(--accent);
  overflow: hidden;
  transition: color 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.magnetic-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--accent);
  transform: translateX(-100%);
  transition: transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.magnetic-btn:hover {
  color: var(--bg);
}

.magnetic-btn:hover::before {
  transform: translateX(0);
}

.magnetic-btn span {
  position: relative;
  z-index: 1;
}
```

**React with GSAP:**
```jsx
const MagneticButton = ({ children, ...props }) => {
  const buttonRef = useRef();
  
  useEffect(() => {
    const btn = buttonRef.current;
    
    const handleMove = (e) => {
      const rect = btn.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      
      gsap.to(btn, {
        x: x * 0.3,
        y: y * 0.3,
        duration: 0.3,
        ease: 'power2.out'
      });
    };
    
    const handleLeave = () => {
      gsap.to(btn, {
        x: 0,
        y: 0,
        duration: 0.5,
        ease: 'elastic.out(1, 0.3)'
      });
    };
    
    btn.addEventListener('mousemove', handleMove);
    btn.addEventListener('mouseleave', handleLeave);
    
    return () => {
      btn.removeEventListener('mousemove', handleMove);
      btn.removeEventListener('mouseleave', handleLeave);
    };
  }, []);
  
  return (
    <button ref={buttonRef} className="magnetic-btn" {...props}>
      <span>{children}</span>
    </button>
  );
};
```

### Press State

```css
.btn-press {
  transition: transform 0.15s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.btn-press:active {
  transform: scale(0.97);
}
```

---

## Link Interactions

### Underline Draw

**CSS Only:**
```css
.link-underline {
  position: relative;
  text-decoration: none;
}

.link-underline::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 50%;
  width: 0;
  height: 1px;
  background: currentColor;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  transform: translateX(-50%);
}

.link-underline:hover::after {
  width: 100%;
}
```

**From Center to Edges:**
```css
.link-expand::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 1px;
  background: currentColor;
  transform: scaleX(0);
  transform-origin: center;
  transition: transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.link-expand:hover::after {
  transform: scaleX(1);
}
```

### Text Shift on Hover

```css
.link-shift {
  display: inline-block;
  transition: transform 0.2s ease;
}

.link-shift:hover {
  transform: translateY(-2px);
}
```

---

## Card Interactions

### 3D Tilt on Hover

**React Hook:**
```jsx
const useTilt = (ref, maxTilt = 5) => {
  useEffect(() => {
    const card = ref.current;
    if (!card) return;
    
    const handleMove = (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      
      const rotateX = ((y - centerY) / centerY) * -maxTilt;
      const rotateY = ((x - centerX) / centerX) * maxTilt;
      
      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    };
    
    const handleLeave = () => {
      card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
    };
    
    card.addEventListener('mousemove', handleMove);
    card.addEventListener('mouseleave', handleLeave);
    
    return () => {
      card.removeEventListener('mousemove', handleMove);
      card.removeEventListener('mouseleave', handleLeave);
    };
  }, [ref, maxTilt]);
};
```

### Lift and Shadow

```css
.card-lift {
  transition: 
    transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94),
    box-shadow 0.3s ease;
}

.card-lift:hover {
  transform: translateY(-4px);
  box-shadow: 
    0 20px 40px -10px rgba(0, 0, 0, 0.3),
    0 10px 20px -5px rgba(0, 0, 0, 0.1);
}
```

### Border Glow

```css
.card-glow {
  position: relative;
  border: 1px solid transparent;
  transition: border-color 0.3s ease;
}

.card-glow::before {
  content: '';
  position: absolute;
  inset: -1px;
  border-radius: inherit;
  padding: 1px;
  background: linear-gradient(
    135deg,
    var(--accent),
    transparent 50%
  );
  -webkit-mask: 
    linear-gradient(#fff 0 0) content-box,
    linear-gradient(#fff 0 0);
  mask: 
    linear-gradient(#fff 0 0) content-box,
    linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.card-glow:hover::before {
  opacity: 1;
}
```

---

## Navigation Interactions

### Active Indicator Slide

```jsx
const SlidingIndicator = ({ items, activeIndex }) => {
  const indicatorRef = useRef();
  
  useEffect(() => {
    const activeItem = document.querySelector(`[data-index="${activeIndex}"]`);
    if (activeItem && indicatorRef.current) {
      const rect = activeItem.getBoundingClientRect();
      const parentRect = activeItem.parentElement.getBoundingClientRect();
      
      gsap.to(indicatorRef.current, {
        x: rect.left - parentRect.left,
        width: rect.width,
        duration: 0.3,
        ease: 'power2.out'
      });
    }
  }, [activeIndex]);
  
  return (
    <nav className="nav-sliding">
      <div ref={indicatorRef} className="indicator" />
      {items.map((item, i) => (
        <a key={i} data-index={i} href={item.href}>
          {item.label}
        </a>
      ))}
    </nav>
  );
};
```

```css
.nav-sliding {
  position: relative;
  display: flex;
  gap: 2rem;
}

.nav-sliding .indicator {
  position: absolute;
  bottom: -4px;
  height: 2px;
  background: var(--accent);
  border-radius: 1px;
}
```

### Dropdown Stagger

```css
.dropdown-menu {
  opacity: 0;
  transform: translateY(-10px);
  pointer-events: none;
  transition: 
    opacity 0.2s ease,
    transform 0.2s ease;
}

.dropdown:hover .dropdown-menu {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}

.dropdown-item {
  opacity: 0;
  transform: translateY(-10px);
}

.dropdown:hover .dropdown-item {
  animation: staggerIn 0.3s ease forwards;
}

.dropdown:hover .dropdown-item:nth-child(1) { animation-delay: 0s; }
.dropdown:hover .dropdown-item:nth-child(2) { animation-delay: 0.05s; }
.dropdown:hover .dropdown-item:nth-child(3) { animation-delay: 0.1s; }
.dropdown:hover .dropdown-item:nth-child(4) { animation-delay: 0.15s; }

@keyframes staggerIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

---

## Custom Cursor

### Basic Custom Cursor

```jsx
const CustomCursor = () => {
  const cursorRef = useRef();
  const [isHovering, setIsHovering] = useState(false);
  
  useEffect(() => {
    let mouseX = 0, mouseY = 0;
    let cursorX = 0, cursorY = 0;
    
    const handleMouseMove = (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    };
    
    const animate = () => {
      cursorX += (mouseX - cursorX) * 0.15;
      cursorY += (mouseY - cursorY) * 0.15;
      
      if (cursorRef.current) {
        cursorRef.current.style.transform = 
          `translate(${cursorX}px, ${cursorY}px)`;
      }
      
      requestAnimationFrame(animate);
    };
    
    // Hover detection
    const hoverables = document.querySelectorAll('a, button, [data-hover]');
    hoverables.forEach(el => {
      el.addEventListener('mouseenter', () => setIsHovering(true));
      el.addEventListener('mouseleave', () => setIsHovering(false));
    });
    
    window.addEventListener('mousemove', handleMouseMove);
    animate();
    
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);
  
  return (
    <div 
      ref={cursorRef}
      className={`custom-cursor ${isHovering ? 'hovering' : ''}`}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: isHovering ? 60 : 20,
        height: isHovering ? 60 : 20,
        border: '1px solid var(--accent)',
        borderRadius: '50%',
        pointerEvents: 'none',
        zIndex: 9999,
        transition: 'width 0.2s, height 0.2s',
        mixBlendMode: 'difference'
      }}
    />
  );
};
```

**CSS (hide default cursor):**
```css
@media (pointer: fine) {
  * {
    cursor: none !important;
  }
  
  .custom-cursor {
    display: block;
  }
}

@media (pointer: coarse) {
  .custom-cursor {
    display: none;
  }
}
```

---

## Input Interactions

### Floating Label

```css
.input-float {
  position: relative;
}

.input-float input {
  width: 100%;
  padding: 1.5rem 1rem 0.5rem;
  border: 1px solid var(--border);
  background: transparent;
  transition: border-color 0.3s ease;
}

.input-float label {
  position: absolute;
  left: 1rem;
  top: 1rem;
  color: var(--muted);
  transition: all 0.2s ease;
  pointer-events: none;
}

.input-float input:focus,
.input-float input:not(:placeholder-shown) {
  border-color: var(--accent);
}

.input-float input:focus + label,
.input-float input:not(:placeholder-shown) + label {
  top: 0.3rem;
  font-size: 0.75rem;
  color: var(--accent);
}
```

### Focus Ring Animation

```css
.input-focus {
  position: relative;
}

.input-focus::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: var(--accent);
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  transform: translateX(-50%);
}

.input-focus:focus-within::after {
  width: 100%;
}
```

---

## Scroll-Linked Interactions

### Progress Indicator

```jsx
const ScrollProgress = () => {
  const [progress, setProgress] = useState(0);
  
  useEffect(() => {
    const handleScroll = () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      setProgress(scrollTop / docHeight);
    };
    
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);
  
  return (
    <div className="scroll-progress">
      <div 
        className="progress-bar"
        style={{ transform: `scaleX(${progress})` }}
      />
    </div>
  );
};
```

```css
.scroll-progress {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  z-index: 9999;
}

.progress-bar {
  height: 100%;
  background: var(--accent);
  transform-origin: left;
  transition: transform 0.1s linear;
}
```

### Scroll Velocity Tilt

```jsx
const VelocityTilt = () => {
  const ref = useRef();
  const velocityRef = useRef(0);
  
  useEffect(() => {
    let lastScrollY = window.scrollY;
    let lastTime = Date.now();
    
    const handleScroll = () => {
      const currentScrollY = window.scrollY;
      const currentTime = Date.now();
      const deltaY = currentScrollY - lastScrollY;
      const deltaTime = currentTime - lastTime;
      
      velocityRef.current = (deltaY / deltaTime) * 0.1;
      velocityRef.current = Math.max(-5, Math.min(5, velocityRef.current));
      
      if (ref.current) {
        ref.current.style.transform = `rotateX(${velocityRef.current}deg)`;
      }
      
      lastScrollY = currentScrollY;
      lastTime = currentTime;
    };
    
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);
  
  return <div ref={ref} className="velocity-tilt">...</div>;
};
```

---

## Image Interactions

### Zoom on Hover

```css
.img-zoom {
  overflow: hidden;
}

.img-zoom img {
  transition: transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.img-zoom:hover img {
  transform: scale(1.05);
}
```

### Reveal Mask

```css
.img-reveal {
  position: relative;
  overflow: hidden;
}

.img-reveal::after {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--bg);
  transform: translateX(0);
  transition: transform 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.img-reveal.revealed::after {
  transform: translateX(100%);
}
```

---

## Reduced Motion Support

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

**React Hook:**
```jsx
const useReducedMotion = () => {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);
  
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setPrefersReducedMotion(mediaQuery.matches);
    
    const handler = (e) => setPrefersReducedMotion(e.matches);
    mediaQuery.addEventListener('change', handler);
    
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);
  
  return prefersReducedMotion;
};
```
