'use client';

import { useEffect, useRef, useCallback, useSyncExternalStore } from 'react';
import { debounce } from '../utils/debounce';
import { useTheme } from './ThemeProvider';

// Hook for subscribing to reduced motion preference
function useReducedMotion(): boolean {
  const subscribe = useCallback((callback: () => void) => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    mediaQuery.addEventListener('change', callback);
    return () => mediaQuery.removeEventListener('change', callback);
  }, []);

  const getSnapshot = useCallback(() => {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }, []);

  // Server-side default: true (safe, no animation)
  const getServerSnapshot = useCallback(() => true, []);

  return useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
}

/**
 * AnimatedBackground - Particle animation background using design tokens
 *
 * Configuration values are defined inline (design-system is in codeflow-desktop repo):
 * - --color-particle: Base particle color
 * - --color-particle-connection: Connection line color
 *
 * This component respects the user's reduced motion preferences and
 * responds dynamically when the preference changes.
 */

// Animation configuration constants
const PARTICLE_COUNT = 50;
const CONNECTION_DISTANCE = 150;
const PARTICLE_MIN_RADIUS = 1;
const PARTICLE_MAX_RADIUS = 3;
const PARTICLE_MIN_OPACITY = 0.1;
const PARTICLE_MAX_OPACITY = 0.6;
const PARTICLE_SPEED = 0.5;
const CONNECTION_MAX_OPACITY = 0.15;

// Design token color values (RGB only for use with variable opacity)
// These match design token values (design-system is in codeflow-desktop repo)
const PARTICLE_COLORS = {
  light: { r: 59, g: 130, b: 246 },  // --color-primary-500 (#3b82f6)
  dark: { r: 147, g: 197, b: 253 },  // --color-primary-300 (#93c5fd)
};

class Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  opacity: number;

  constructor(canvasWidth: number, canvasHeight: number) {
    this.x = Math.random() * canvasWidth;
    this.y = Math.random() * canvasHeight;
    this.vx = (Math.random() - 0.5) * PARTICLE_SPEED;
    this.vy = (Math.random() - 0.5) * PARTICLE_SPEED;
    this.radius = Math.random() * (PARTICLE_MAX_RADIUS - PARTICLE_MIN_RADIUS) + PARTICLE_MIN_RADIUS;
    this.opacity = Math.random() * (PARTICLE_MAX_OPACITY - PARTICLE_MIN_OPACITY) + PARTICLE_MIN_OPACITY;
  }

  update(canvasWidth: number, canvasHeight: number) {
    this.x += this.vx;
    this.y += this.vy;

    if (this.x < 0 || this.x > canvasWidth) this.vx *= -1;
    if (this.y < 0 || this.y > canvasHeight) this.vy *= -1;
  }

  draw(ctx: CanvasRenderingContext2D, isDark: boolean) {
    const color = isDark ? PARTICLE_COLORS.dark : PARTICLE_COLORS.light;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(${color.r}, ${color.g}, ${color.b}, ${this.opacity})`;
    ctx.fill();
  }
}

export default function AnimatedBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationFrameRef = useRef<number | null>(null);
  const particlesRef = useRef<Particle[]>([]);
  const prefersReducedMotion = useReducedMotion();
  const { resolvedTheme } = useTheme();
  // Use ref to track theme in animation loop without causing re-renders
  const isDarkRef = useRef(resolvedTheme === 'dark');

  // Keep ref in sync with theme context
  useEffect(() => {
    isDarkRef.current = resolvedTheme === 'dark';
  }, [resolvedTheme]);

  const initParticles = useCallback((width: number, height: number) => {
    particlesRef.current = [];
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      particlesRef.current.push(new Particle(width, height));
    }
  }, []);

  const drawConnections = useCallback((ctx: CanvasRenderingContext2D, isDark: boolean) => {
    const color = isDark ? PARTICLE_COLORS.dark : PARTICLE_COLORS.light;
    const particles = particlesRef.current;

    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < CONNECTION_DISTANCE) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          const opacity = (1 - distance / CONNECTION_DISTANCE) * CONNECTION_MAX_OPACITY;
          ctx.strokeStyle = `rgba(${color.r}, ${color.g}, ${color.b}, ${opacity})`;
          ctx.lineWidth = 1;
          ctx.stroke();
        }
      }
    }
  }, []);

  // Animation effect - starts/stops based on reduced motion preference
  useEffect(() => {
    // Don't animate if user prefers reduced motion
    if (prefersReducedMotion) {
      // Clear canvas when reduced motion is enabled
      const canvas = canvasRef.current;
      if (canvas) {
        const ctx = canvas.getContext('2d');
        if (ctx) {
          ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
      }
      return;
    }

    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      initParticles(canvas.width, canvas.height);
    };

    // Debounce resize handler to prevent particle re-initialization thrashing
    const debouncedResize = debounce(resizeCanvas, 250);

    const animate = () => {
      // Use theme from context (via ref) instead of DOM class inspection
      const isDark = isDarkRef.current;

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      particlesRef.current.forEach(particle => {
        particle.update(canvas.width, canvas.height);
        particle.draw(ctx, isDark);
      });

      drawConnections(ctx, isDark);

      animationFrameRef.current = requestAnimationFrame(animate);
    };

    // Initial setup (not debounced)
    resizeCanvas();
    animate();

    window.addEventListener('resize', debouncedResize);

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      debouncedResize.cancel();
      window.removeEventListener('resize', debouncedResize);
    };
  }, [prefersReducedMotion, initParticles, drawConnections]);

  return (
    <canvas
      ref={canvasRef}
      className="pointer-events-none fixed inset-0 z-0"
      aria-hidden="true"
    />
  );
}
