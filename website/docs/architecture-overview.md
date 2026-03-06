# CodeFlow Website - Architecture Overview

This document describes the architectural patterns, structure, and design decisions for the CodeFlow Website.

---

## Architecture Style

**Primary Pattern:** Static Site / Jamstack Architecture

| Attribute | Value |
|-----------|-------|
| Architecture Type | Static Site Generation (SSG) |
| Deployment Model | Edge-deployed static assets |
| Backend | None (client-side only) |
| Data Fetching | Build-time only |
| Interactivity | Client-side JavaScript |

### Rationale

The CodeFlow Website is a marketing site with no dynamic data requirements. Static site generation provides:

- **Performance**: Pre-rendered HTML served from CDN edge locations
- **Security**: No server-side attack surface
- **Scalability**: Unlimited scalability via CDN
- **Cost**: Minimal hosting costs (Azure Static Web Apps free tier)
- **Reliability**: No server uptime concerns

---

## Application Structure

### Directory Layout

```text
codeflow-website/
├── app/                      # Next.js App Router
│   ├── components/           # Shared React components
│   │   ├── AlphaBadge.tsx
│   │   ├── AnimatedBackground.tsx
│   │   ├── Header.tsx
│   │   ├── PromoBanner.tsx
│   │   ├── ThemeProvider.tsx
│   │   └── ThemeToggle.tsx
│   ├── config/               # Application configuration
│   │   └── constants.ts
│   ├── fonts/                # Local font files
│   ├── download/             # /download route
│   │   └── page.tsx
│   ├── installation/         # /installation route
│   │   └── page.tsx
│   ├── integration/          # /integration route
│   │   └── page.tsx
│   ├── globals.css           # Global styles
│   ├── layout.tsx            # Root layout
│   └── page.tsx              # Home page (/)
├── docs/                     # Project documentation
├── public/                   # Static assets
├── .github/                  # GitHub configuration
│   └── workflows/
│       └── ci.yml            # CI/CD pipeline
└── [config files]            # Root configuration
```

### Routing Architecture

| Route | File | Purpose |
|-------|------|---------|
| `/` | `app/page.tsx` | Home/landing page |
| `/download/` | `app/download/page.tsx` | Download options |
| `/installation/` | `app/installation/page.tsx` | Installation guide |
| `/integration/` | `app/integration/page.tsx` | Integration guide |

**Routing Pattern**: File-system-based routing via Next.js App Router

---

## Component Architecture

### Component Hierarchy

```text
RootLayout (app/layout.tsx)
├── ThemeProvider
│   ├── Skip Link (accessibility)
│   ├── AnimatedBackground
│   ├── PromoBanner
│   └── <main>
│       ├── Header
│       │   ├── Logo + AlphaBadge
│       │   ├── Navigation
│       │   └── ThemeToggle
│       └── Page Content
│           ├── Hero Section
│           ├── Feature Cards (inline)
│           ├── CTA Sections (inline)
│           └── Footer (inline)
```

### Component Categories

| Category | Components | Status |
|----------|------------|--------|
| Layout | RootLayout, Header | Abstracted |
| Theme | ThemeProvider, ThemeToggle | Abstracted |
| Decoration | AnimatedBackground, PromoBanner, AlphaBadge | Abstracted |
| Content | Feature Cards, CTA Sections, Footer | Not abstracted (inline) |

### State Management

| State | Scope | Storage | Component |
|-------|-------|---------|-----------|
| Theme | Global | localStorage | ThemeProvider |
| Mounted State | Component | React state | ThemeProvider |
| Animation State | Component | React state | AnimatedBackground |

**Pattern**: React Context for global state (theme), local state for component behavior.

---

## Data Flow Architecture

### Build-Time Data Flow

```text
Source Files → Next.js Build → Static HTML/CSS/JS → CDN → Browser
```

| Stage | Description |
|-------|-------------|
| Source | TypeScript/TSX components, CSS |
| Build | Next.js static export generates `/out` directory |
| Deploy | GitHub Actions uploads to Azure Static Web Apps |
| Serve | Azure CDN serves static assets globally |

### Runtime Data Flow

```text
Browser → Load Static HTML → Hydrate React → Client-side Interactivity
```

| Stage | Description |
|-------|-------------|
| Initial Load | Pre-rendered HTML displayed immediately |
| Hydration | React attaches event handlers |
| Interactivity | Theme toggle, animations, navigation |

---

## Styling Architecture

### CSS Strategy

| Layer | Technology | Scope |
|-------|------------|-------|
| Reset/Base | Tailwind CSS | Global |
| Utilities | Tailwind CSS | Component |
| Custom | globals.css | Global |
| Component | Inline Tailwind classes | Component |

### Design Token Architecture

```text
External Design System (codeflow-desktop)
         ↓
    [Not mirrored]
         ↓
Inline Tailwind Classes (this repo)
         ↓
Component Styles
```

**Current State**: Design tokens are referenced but defined externally. Components use Tailwind utility classes directly.

**Risk**: Undefined CSS custom properties in `globals.css` may cause styling inconsistencies.

---

## Deployment Architecture

### CI/CD Pipeline

```text
GitHub Repository
      │
      ▼
┌─────────────────────────────────────┐
│        GitHub Actions CI            │
├─────────────────────────────────────┤
│  ┌───────┐  ┌──────┐  ┌──────┐     │
│  │ Build │  │ Test │  │ Lint │     │
│  └───┬───┘  └──┬───┘  └──┬───┘     │
│      │         │         │          │
│      └────────┬┴─────────┘          │
│               │                     │
│         ┌─────▼─────┐               │
│         │  Deploy   │               │
│         │(main only)│               │
│         └─────┬─────┘               │
└───────────────│─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│     Azure Static Web Apps           │
│  ┌─────────────────────────────┐    │
│  │   Global CDN Distribution   │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

### Deployment Environments

| Environment | Branch | URL | Trigger |
|-------------|--------|-----|---------|
| Production | main | Azure SWA URL | Push to main |
| Preview | PR branches | Auto-generated | Pull request |

---

## Risk Surfaces

### Security Risks

| Risk | Severity | Mitigation Status |
|------|----------|-------------------|
| XSS via user input | Low | No user input forms |
| CSRF | N/A | No state-changing operations |
| Dependency vulnerabilities | Medium | No automated scanning |
| Secrets exposure | Low | GitHub Secrets used |
| CSP bypass | Medium | CSP not configured |

### Performance Risks

| Risk | Severity | Mitigation Status |
|------|----------|-------------------|
| Large bundle size | Low | Static export, tree shaking |
| Render blocking | Low | Font display: swap |
| Animation jank | Low | Reduced motion support |
| CDN cache miss | Low | Long TTL on static assets |

### Scalability Risks

| Risk | Severity | Notes |
|------|----------|-------|
| Traffic spikes | Very Low | CDN handles unlimited scale |
| Build time | Low | Small codebase |
| Content updates | Low | Rebuild required for changes |

### Maintainability Risks

| Risk | Severity | Mitigation Status |
|------|----------|-------------------|
| Duplicated components | Medium | Footer, Feature Cards not abstracted |
| Undefined design tokens | High | External dependency not mirrored |
| No test coverage | High | Testing infrastructure missing |
| Documentation gaps | Medium | Being addressed |

---

## Multi-Repository Architecture

The CodeFlow Website is part of a larger multi-repository ecosystem:

```text
┌─────────────────────────────────────────────────────────────┐
│                    CodeFlow Ecosystem                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐     ┌─────────────────────────────┐   │
│  │ codeflow-engine │────▶│ Core AI/Automation Engine   │   │
│  └─────────────────┘     └─────────────────────────────┘   │
│                                                             │
│  ┌─────────────────┐     ┌─────────────────────────────┐   │
│  │codeflow-website │────▶│ Marketing Site (this repo)  │   │
│  └─────────────────┘     └─────────────────────────────┘   │
│                                                             │
│  ┌─────────────────┐     ┌─────────────────────────────┐   │
│  │codeflow-desktop │────▶│ Desktop App + Design System │   │
│  └─────────────────┘     └─────────────────────────────┘   │
│                                                             │
│  ┌─────────────────┐     ┌─────────────────────────────┐   │
│  │codeflow-infra   │────▶│ Azure Infrastructure (IaC)  │   │
│  └─────────────────┘     └─────────────────────────────┘   │
│                                                             │
│  ┌─────────────────┐     ┌─────────────────────────────┐   │
│  │codeflow-vscode  │────▶│ VS Code Extension           │   │
│  └─────────────────┘     └─────────────────────────────┘   │
│                                                             │
│  ┌─────────────────┐     ┌─────────────────────────────┐   │
│  │codeflow-azure-  │────▶│ Azure Bootstrap Scripts     │   │
│  │setup            │     └─────────────────────────────┘   │
│  └─────────────────┘                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Cross-Repository Dependencies

| Dependency | Source Repo | Target Repo | Type |
|------------|-------------|-------------|------|
| Design Tokens | codeflow-desktop | codeflow-website | Implicit (not synced) |
| Infrastructure | codeflow-infrastructure | codeflow-website | Deployment target |

---

## Architectural Decisions

### ADR-001: Static Site Generation

**Decision**: Use Next.js static export instead of server-side rendering.

**Context**: Marketing website with no dynamic content requirements.

**Consequences**:
- (+) No server infrastructure to manage
- (+) Optimal performance via CDN edge caching
- (+) Reduced hosting costs
- (-) Full rebuild required for content changes
- (-) No server-side personalization

### ADR-002: App Router over Pages Router

**Decision**: Use Next.js App Router (app directory) instead of Pages Router.

**Context**: New project starting with Next.js 16.x.

**Consequences**:
- (+) Modern React patterns (Server Components ready)
- (+) Improved layouts and nested routing
- (+) Better TypeScript integration
- (-) Newer API with less community resources

### ADR-003: Tailwind CSS for Styling

**Decision**: Use Tailwind CSS utility classes instead of CSS-in-JS or modules.

**Context**: Rapid development of marketing site with design flexibility needs.

**Consequences**:
- (+) Fast iteration on designs
- (+) Consistent spacing/sizing scale
- (+) Small production bundle (purged CSS)
- (-) Verbose class names in JSX
- (-) Design system abstraction requires discipline

---

## Future Considerations

### Potential Enhancements

| Enhancement | Priority | Complexity |
|-------------|----------|------------|
| Component library extraction | Medium | Medium |
| Design token synchronization | High | Low |
| Test infrastructure | High | Medium |
| Error tracking integration | Medium | Low |
| Analytics integration | Low | Low |
| Internationalization | Low | High |

### Scaling Considerations

The current architecture supports the marketing site use case well. If requirements change to include:

- **User authentication**: Consider adding Azure AD B2C
- **Dynamic content**: Consider ISR (Incremental Static Regeneration) or API routes
- **E-commerce**: Would require significant architectural changes
