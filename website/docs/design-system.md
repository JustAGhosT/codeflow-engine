# CodeFlow Website - Design System

This document captures the reverse-engineered design tokens, component inventory, and UX patterns used in the CodeFlow Website.

> **Note:** The canonical design system is maintained in the [`codeflow-desktop`](https://github.com/JustAGhosT/codeflow-desktop) repository. This document reflects the tokens and patterns as implemented in this website.

---

## Typography

### Font Families

| Token | Value | Classification |
|-------|-------|----------------|
| `--font-geist-sans` | Geist VF (variable font, 100–900 weight) | Intentional |
| `--font-geist-mono` | Geist Mono VF (variable font, 100–900 weight) | Intentional |

### Fallback Fonts

- **Sans-serif:** system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif
- **Monospace:** ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace

---

## Color Palette

### Core Colors

| Color Role | Light Mode | Dark Mode | Classification |
|------------|------------|-----------|----------------|
| Primary (accent) | `#3b82f6` (blue-600) | `#93c5fd` (blue-300) | Intentional |
| Secondary gradient | blue-600 → purple-600 | Same | Intentional |
| Background | slate-50 → slate-100 | slate-900 → slate-950 | Intentional |
| Surface | white/50–60% opacity | slate-800/50–60% opacity | Intentional |
| Foreground | slate-900 | slate-50 | Intentional |
| Text secondary | slate-600 | slate-400 | Intentional |
| Border | slate-200 | slate-700 | Intentional |

### Accent Colors

| Color Role | Light Mode | Dark Mode | Classification |
|------------|------------|-----------|----------------|
| Promo/Alpha banner | amber-500 → orange-500 | Same | Intentional |
| Alpha badge background | amber-100 | amber-900 | Intentional |
| Alpha badge text | amber-800 | amber-200 | Intentional |

---

## Spacing & Layout

### Container Widths

| Pattern | Values Used | Classification |
|---------|-------------|----------------|
| Page max-width | `max-w-7xl` (1280px), `max-w-4xl` (896px) | Inferred |

### Spacing Scale

| Pattern | Values Used | Classification |
|---------|-------------|----------------|
| Section padding (vertical) | `py-24` (96px), `py-12` (48px) | Inferred |
| Horizontal padding | `px-6` (24px) | Intentional |
| Component padding | `p-6` (24px), `p-8` (32px), `p-12` (48px) | Inferred |
| Gap spacing | `gap-4` (16px), `gap-6` (24px), `gap-8` (32px) | Inferred |

### Border Radius

| Pattern | Values Used | Classification |
|---------|-------------|----------------|
| Cards/Containers | `rounded-lg` | Intentional |
| Badges/Pills | `rounded-full` | Intentional |

---

## Component Inventory

### Intentional Components (Abstracted)

| Component | File | Variants | Notes |
|-----------|------|----------|-------|
| Header | `app/components/Header.tsx` | 4 pages (home/installation/integration/download) | Shared navigation component |
| ThemeProvider | `app/components/ThemeProvider.tsx` | light/dark/system | Context provider for theme management |
| ThemeToggle | `app/components/ThemeToggle.tsx` | 3 icon states | Sun/moon/system icons |
| PromoBanner | `app/components/PromoBanner.tsx` | Single variant | Alpha preview banner |
| AnimatedBackground | `app/components/AnimatedBackground.tsx` | Single variant | Respects reduced motion preference |
| AlphaBadge | `app/components/AlphaBadge.tsx` | Single variant | "Alpha" badge next to logo |

### Accidental Patterns (Not Abstracted)

| Pattern | Location | Instances | Recommendation |
|---------|----------|-----------|----------------|
| Feature Card | Inline in `app/page.tsx` | 3 instances | Should be extracted to component |
| CTA Section | Inline in `app/page.tsx` | Multiple styles | Should be standardized |
| Footer | Inline in page files | Duplicated across 4 pages | Should be extracted to component |

---

## UX Rules & Patterns

### Accessibility

| Pattern | Evidence | Classification |
|---------|----------|----------------|
| Skip link for accessibility | `app/layout.tsx:41-43`, `globals.css:23-44` | Intentional |
| Focus-visible styling | `globals.css:47-50` | Intentional |
| Reduced motion support | `AnimatedBackground.tsx:74-84` | Intentional |
| Theme persistence | localStorage in ThemeProvider | Intentional |
| Hydration mismatch prevention | ThemeProvider mounted state | Intentional |

### ARIA & Semantic HTML

| Feature | Status | Evidence |
|---------|--------|----------|
| Skip link | Present | `layout.tsx:41` |
| aria-label on external links | Present | `Header.tsx:60` |
| aria-current="page" | Present | `Header.tsx:28,37,43,49` |
| aria-hidden on decorative canvas | Present | `AnimatedBackground.tsx:175` |
| role="main" | Present | `layout.tsx:46` |
| Keyboard navigation | Implicit via native elements | Intentional |

---

## Button Styles

### Primary CTA

```css
rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 px-8 py-3 text-lg font-semibold text-white
hover:from-blue-700 hover:to-purple-700 hover:shadow-lg
```

### Secondary CTA

```css
rounded-lg bg-slate-800 px-8 py-3 text-lg font-semibold text-white
hover:bg-slate-700
/* Dark mode: */
dark:bg-slate-100 dark:text-slate-900 dark:hover:bg-slate-200
```

### Tertiary/Outline

```css
rounded-lg border-2 border-slate-300 bg-white/50 px-8 py-3 text-lg font-semibold text-slate-900
hover:border-slate-400
/* Dark mode: */
dark:border-slate-600 dark:bg-slate-800/50 dark:text-slate-50 dark:hover:border-slate-500
```

---

## Card Styles

### Feature Card

```css
rounded-lg border border-slate-200 bg-white/60 p-6 backdrop-blur-sm
/* Dark mode: */
dark:border-slate-700 dark:bg-slate-800/60
```

### Promo Card

```css
rounded-lg border-2 border-amber-500 bg-gradient-to-r from-amber-50/90 to-orange-50/90 p-8 backdrop-blur-sm
/* Dark mode: */
dark:from-amber-950/80 dark:to-orange-950/80
```

---

## Design–Code Consistency Issues

| Issue | Description | Severity |
|-------|-------------|----------|
| Design tokens referenced but undefined | `globals.css` references `--space-2`, `--color-surface`, etc. but no source file defines them | High |
| CSS custom properties incomplete | Comment says "design-system is in codeflow-desktop repo" — external dependency not mirrored | Medium |
| Footer duplication | Footer is copy-pasted across 4 page files instead of being a shared component | Medium |
| Feature cards not componentized | 3 identical card structures in `page.tsx` are inline | Low |
| Inconsistent button styles | Multiple gradient/solid/outline variants without clear system | Medium |

---

## Visual Regression / Testing Artifacts

| Artifact | Status |
|----------|--------|
| Storybook | Not present |
| Visual regression tests | Not present |
| Accessibility tests | Not present |
| Snapshot tests | Not present |

---

## Recommendations

1. **Extract Footer component** - Create a shared Footer component to eliminate duplication across pages
2. **Create FeatureCard component** - Abstract the repeated feature card pattern
3. **Define local design tokens** - Mirror essential design tokens from `codeflow-desktop` to avoid undefined variable references
4. **Standardize button variants** - Create a consistent button component with defined variants (primary, secondary, outline)
5. **Add Storybook** - Document components with Storybook for better design system visibility
6. **Add visual regression tests** - Implement visual regression testing to catch unintended UI changes
