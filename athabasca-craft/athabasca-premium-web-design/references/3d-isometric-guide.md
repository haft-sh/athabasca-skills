# 3D Isometric Integration Guide

Technical implementation patterns for 3D isometric visuals that elevate technical websites.

## When to Use 3D Isometric

**Ideal For:**
- Platform architecture diagrams (layered infrastructure)
- API documentation (endpoint hierarchies)
- Blockchain/Web3 stack visualization
- Product ecosystems (connected services)
- Data flow illustrations
- Process/workflows with multiple stages

**Skip When:**
- Simple product pages (overkill)
- Content-heavy editorial sites (distracting)
- Mobile-first experiences (performance concerns)
- Brands requiring ultra-fast load times

---

## Approach 1: CSS 3D Isometric (Lightweight)

**Best for:** Simple diagrams, hover interactions, lightweight performance

**Implementation:**
```css
.isometric-container {
  transform-style: preserve-3d;
  transform: rotateX(60deg) rotateZ(-45deg);
}

.isometric-block {
  position: absolute;
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #a8f0d8, #7bdcb8);
  transform: translateZ(var(--depth));
  box-shadow: 
    inset 0 0 20px rgba(255,255,255,0.2),
    0 0 40px rgba(168, 240, 216, 0.3);
}

.isometric-block::before {
  /* Top face */
  content: '';
  position: absolute;
  top: -50px;
  left: 0;
  width: 100%;
  height: 50px;
  background: linear-gradient(135deg, #c8f8e8, #a8f0d8);
  transform: skewX(-45deg);
  transform-origin: bottom;
}

.isometric-block::after {
  /* Side face */
  content: '';
  position: absolute;
  top: 0;
  left: 100%;
  width: 50px;
  height: 100%;
  background: linear-gradient(135deg, #5ad4a8, #7bdcb8);
  transform: skewY(-45deg);
  transform-origin: left;
}
```

**Pros:** No JS, GPU-accelerated, works on mobile
**Cons:** Limited interactivity, static geometry
**Performance:** ★★★★★

---

## Approach 2: Three.js with React Three Fiber (Full Control)

**Best for:** Interactive diagrams, scroll-driven animations, complex scenes

**Installation:**
```bash
npm install three @react-three/fiber @react-three/drei
```

**Basic Isometric Scene:**
```jsx
import { Canvas } from '@react-three/fiber';
import { OrbitControls, RoundedBox, Text } from '@react-three/drei';
import { useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

function IsometricBlock({ position, label, color, onScrollProgress }) {
  const meshRef = useRef();
  
  useEffect(() => {
    if (meshRef.current) {
      gsap.to(meshRef.current.scale, {
        x: onScrollProgress,
        y: onScrollProgress,
        z: onScrollProgress,
        duration: 0.5,
        ease: 'power2.out'
      });
    }
  }, [onScrollProgress]);
  
  return (
    <group position={position}>
      <RoundedBox
        ref={meshRef}
        args={[2, 2, 2]}
        radius={0.1}
        smoothness={4}
      >
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={0.2}
          roughness={0.3}
          metalness={0.1}
        />
      </RoundedBox>
      <Text
        position={[0, 1.5, 0]}
        fontSize={0.3}
        color="white"
        anchorX="center"
        anchorY="middle"
      >
        {label}
      </Text>
    </group>
  );
}

function IsometricStack() {
  const groupRef = useRef();
  const [scrollProgress, setScrollProgress] = useState(0);
  
  useEffect(() => {
    ScrollTrigger.create({
      trigger: '#isometric-section',
      start: 'top center',
      end: 'bottom center',
      scrub: true,
      onUpdate: (self) => setScrollProgress(self.progress)
    });
  }, []);
  
  // Calculate individual layer progress
  const layer1Progress = Math.min(scrollProgress * 3, 1);
  const layer2Progress = Math.max(0, Math.min((scrollProgress - 0.33) * 3, 1));
  const layer3Progress = Math.max(0, Math.min((scrollProgress - 0.66) * 3, 1));
  
  return (
    <Canvas
      camera={{ position: [10, 10, 10], fov: 45 }}
      style={{ background: '#0a1512' }}
    >
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} intensity={1} />
      <pointLight position={[-10, -10, -10]} intensity={0.3} color="#a8f0d8" />
      
      <group ref={groupRef} rotation={[0, Math.PI / 4, 0]}>
        <IsometricBlock
          position={[0, -3, 0]}
          label="Foundation"
          color="#2e4036"
          onScrollProgress={layer1Progress}
        />
        <IsometricBlock
          position={[0, 0, 0]}
          label="Core"
          color="#5ad4a8"
          onScrollProgress={layer2Progress}
        />
        <IsometricBlock
          position={[0, 3, 0]}
          label="Apps"
          color="#a8f0d8"
          onScrollProgress={layer3Progress}
        />
      </group>
      
      <OrbitControls
        enableZoom={false}
        enablePan={false}
        minPolarAngle={Math.PI / 4}
        maxPolarAngle={Math.PI / 4}
      />
    </Canvas>
  );
}

export default IsometricStack;
```

**Isometric Camera Setup:**
```javascript
// Classic isometric angles
const ISOMETRIC_ANGLE = Math.atan(1 / Math.sqrt(2)); // ≈ 35.264°

<Canvas camera={{
  position: [
    distance * Math.cos(ISOMETRIC_ANGLE),
    distance * Math.sin(ISOMETRIC_ANGLE),
    distance * Math.cos(ISOMETRIC_ANGLE)
  ],
  fov: 45
}}>
```

---

## Approach 3: Spline Integration (Design-First)

**Best for:** Teams with designers, rapid iteration, pre-built scenes

**Installation:**
```bash
npm install @splinetool/react-spline
```

**Usage:**
```jsx
import Spline from '@splinetool/react-spline';

function Scene() {
  const splineRef = useRef();
  
  const handleScroll = (progress) => {
    if (splineRef.current) {
      // Trigger Spline events based on scroll
      splineRef.current.emitEvent('scroll', progress);
    }
  };
  
  return (
    <Spline
      ref={splineRef}
      scene="https://prod.spline.design/your-scene-url/scene.splinecode"
      onLoad={(spline) => {
        // Access Spline API
        console.log(spline.getVariables());
      }}
    />
  );
}
```

**Pros:** Visual editor, no code needed for scenes, professional output
**Cons:** External dependency, less control, larger bundle

---

## Scroll-Driven 3D Animation

**Pattern: Layer-by-Layer Reveal**

```jsx
function ScrollDrivenIsometric() {
  const containerRef = useRef();
  const [layerProgress, setLayerProgress] = useState([0, 0, 0]);
  
  useEffect(() => {
    gsap.registerPlugin(ScrollTrigger);
    
    const triggers = [];
    
    // Layer 1: Foundation (0-33%)
    triggers.push(ScrollTrigger.create({
      trigger: containerRef.current,
      start: 'top top',
      end: '33% top',
      scrub: 0.5,
      onUpdate: (self) => {
        setLayerProgress(prev => [self.progress, prev[1], prev[2]]);
      }
    }));
    
    // Layer 2: Core (33-66%)
    triggers.push(ScrollTrigger.create({
      trigger: containerRef.current,
      start: '33% top',
      end: '66% top',
      scrub: 0.5,
      onUpdate: (self) => {
        setLayerProgress(prev => [prev[0], self.progress, prev[2]]);
      }
    }));
    
    // Layer 3: Apps (66-100%)
    triggers.push(ScrollTrigger.create({
      trigger: containerRef.current,
      start: '66% top',
      end: 'bottom top',
      scrub: 0.5,
      onUpdate: (self) => {
        setLayerProgress(prev => [prev[0], prev[1], self.progress]);
      }
    }));
    
    return () => triggers.forEach(t => t.kill());
  }, []);
  
  return (
    <div ref={containerRef} style={{ height: '300vh' }}>
      <div style={{ position: 'sticky', top: 0, height: '100vh' }}>
        {/* Three.js Canvas with layerProgress props */}
      </div>
    </div>
  );
}
```

---

## Hyperliquid-Style Glowing Effect

**Shader Material for Bloom:**
```javascript
import { shaderMaterial } from '@react-three/drei';
import * as THREE from 'three';

const GlowMaterial = shaderMaterial(
  {
    color: new THREE.Color('#a8f0d8'),
    coefficient: 0.5,
    power: 4.0,
  },
  // Vertex shader
  `
    varying vec3 vNormal;
    varying vec3 vPosition;
    void main() {
      vNormal = normalize(normalMatrix * normal);
      vPosition = (modelViewMatrix * vec4(position, 1.0)).xyz;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  // Fragment shader
  `
    uniform vec3 color;
    uniform float coefficient;
    uniform float power;
    varying vec3 vNormal;
    void main() {
      float intensity = pow(coefficient - dot(vNormal, vec3(0.0, 0.0, 1.0)), power);
      gl_FragColor = vec4(color, 1.0) * intensity;
    }
  `
);
```

**Post-Processing Bloom:**
```jsx
import { EffectComposer, Bloom } from '@react-three/postprocessing';

<Canvas>
  <Scene />
  <EffectComposer>
    <Bloom
      intensity={1.5}
      luminanceThreshold={0.9}
      luminanceSmoothing={0.025}
    />
  </EffectComposer>
</Canvas>
```

---

## Performance Optimization

**Critical for 3D Web:**

1. **InstancedMesh for repeated elements:**
```javascript
import { InstancedMesh } from '@react-three/drei';

<InstancedMesh
  geometry={boxGeometry}
  material={material}
  count={100}
>
  {positions.map((pos, i) => (
    <Instance key={i} position={pos} />
  ))}
</InstancedMesh>
```

2. **Level of Detail (LOD):**
```javascript
import { useLOD } from '@react-three/drei';

const [ref, level] = useLOD({
  distances: [0, 10, 20],
  geometries: [highPoly, mediumPoly, lowPoly]
});
```

3. **Occlusion Culling:**
```javascript
import { useThree } from '@react-three/fiber';

const { gl } = useThree();
gl.setPixelRatio(Math.min(window.devicePixelRatio, 2));
```

4. **Lazy Loading:**
```javascript
import { Suspense, lazy } from 'react';

const Lazy3DScene = lazy(() => import('./Heavy3DScene'));

<Suspense fallback={<div>Loading...</div>}>
  <Lazy3DScene />
</Suspense>
```

---

## Connection Lines (Animated SVG Overlay)

**For connecting 3D blocks with animated lines:**

```jsx
import { useRef, useEffect } from 'react';

function ConnectionLines({ start, end, progress }) {
  const pathRef = useRef();
  
  // Convert 3D world positions to 2D screen space
  const start2D = worldToScreen(start);
  const end2D = worldToScreen(end);
  
  // Isometric curve control points
  const midX = (start2D.x + end2D.x) / 2;
  const midY = (start2D.y + end2D.y) / 2 - 50; // Arch upward
  
  const path = `M ${start2D.x} ${start2D.y} Q ${midX} ${midY} ${end2D.x} ${end2D.y}`;
  
  useEffect(() => {
    if (pathRef.current) {
      const length = pathRef.current.getTotalLength();
      pathRef.current.style.strokeDasharray = length;
      pathRef.current.style.strokeDashoffset = length * (1 - progress);
    }
  }, [progress]);
  
  return (
    <svg style={{ position: 'absolute', pointerEvents: 'none' }}>
      <path
        ref={pathRef}
        d={path}
        stroke="#a8f0d8"
        strokeWidth="2"
        fill="none"
        opacity={0.6}
      />
    </svg>
  );
}
```

---

## Responsive Considerations

**Mobile Fallback Strategy:**

```jsx
function IsometricSection() {
  const [isMobile, setIsMobile] = useState(false);
  
  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth < 768);
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);
  
  if (isMobile) {
    return <StaticDiagram />; // CSS-based or SVG
  }
  
  return <Full3DScene />;
}
```

**Reduced Motion:**

```jsx
const prefersReducedMotion = useMediaQuery('(prefers-reduced-motion: reduce)');

if (prefersReducedMotion) {
  return <StaticIsometric />;
}
```

---

## Reference Sites for 3D Inspiration

- **hyperfoundation.org** — Layered blockchain architecture
- **stripe.com/connect** — Animated flow diagrams
- **linear.app** — Subtle depth, minimal 3D
- **vercel.com** — Geometric precision
- **raycast.com** — Product ecosystem visualization
