# UI/UX Design Guidelines

## Document Information
- **Version**: 0.1.0
- **Last Updated**: 2025-11-15
- **Status**: Design System Specification
- **Theme**: Light (Dark mode planned for Phase 2)

---

## 1. Design Philosophy

### 1.1 Core Principles

**"Simple in Use, Sophisticated in Results"**

1. **Clarity over Complexity**: Clean, uncluttered interface
2. **Speed First**: Fast load times, instant interactions, <60s daily logging
3. **Mobile-First**: Optimized for daily mobile use
4. **Professional Trust**: Clinical-grade aesthetic that builds confidence
5. **Accessible by Default**: WCAG 2.1 AA compliance from day one
6. **Data-Focused**: Visualizations are beautiful AND useful

### 1.2 Design Values

| Value | What it means | Example |
|-------|---------------|---------|
| **Simplicity** | Remove cognitive load | No more than 2 actions per screen |
| **Consistency** | Predictable patterns | Same button styles everywhere |
| **Efficiency** | Respect user's time | Autocomplete, smart defaults, quick forms |
| **Transparency** | Clear feedback | Loading states, success/error messages |
| **Empathy** | Understand mental health context | Gentle language, supportive tone |

---

## 2. Visual Design System

### 2.1 Color Palette

#### Primary Colors

```css
--primary-50:  #E8F5F4;   /* Lightest tint */
--primary-100: #C1E7E3;
--primary-200: #9AD9D3;
--primary-300: #73CBC3;
--primary-400: #4CBDB3;
--primary-500: #14B8A6;   /* ← Main brand color (Teal) */
--primary-600: #0D9488;
--primary-700: #0F766E;
--primary-800: #115E59;
--primary-900: #134E4A;   /* Darkest shade */
```

**Usage:**
- Primary buttons
- Links
- Active states
- Progress indicators
- Key metrics highlights

**Rationale:**
- Teal/cyan: Calming, professional, medical trust
- Not red (anxiety-inducing)
- Not overly bright (gentle on eyes)

#### Semantic Colors

```css
/* Success - Green */
--success-50:  #ECFDF5;
--success-500: #10B981;   /* Main */
--success-700: #047857;

/* Warning - Amber */
--warning-50:  #FFFBEB;
--warning-500: #F59E0B;   /* Main */
--warning-700: #B45309;

/* Error - Red (muted) */
--error-50:  #FEF2F2;
--error-500: #EF4444;     /* Main */
--error-700: #B91C1C;

/* Info - Blue */
--info-50:  #EFF6FF;
--info-500: #3B82F6;      /* Main */
--info-700: #1D4ED8;
```

#### Neutral Palette (Grays)

```css
--neutral-50:  #F9FAFB;   /* Lightest background */
--neutral-100: #F3F4F6;   /* Secondary background */
--neutral-200: #E5E7EB;   /* Borders, dividers */
--neutral-300: #D1D5DB;   /* Disabled state */
--neutral-400: #9CA3AF;
--neutral-500: #6B7280;   /* Secondary text */
--neutral-600: #4B5563;
--neutral-700: #374151;   /* Body text */
--neutral-800: #1F2937;
--neutral-900: #111827;   /* Headings */
```

#### Metric Category Colors

```css
--category-physical:      #EC4899;  /* Pink */
--category-psychological: #8B5CF6;  /* Purple */
--category-triggers:      #EF4444;  /* Red */
--category-medications:   #3B82F6;  /* Blue */
--category-selfcare:      #10B981;  /* Green */
--category-wellness:      #F59E0B;  /* Amber */
--category-notes:         #6B7280;  /* Gray */
```

### 2.2 Typography

#### Font Families

```css
/* Primary font - Inter (clean, modern, highly legible) */
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI',
             'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;

/* Monospace - for data, numbers, code */
--font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
```

**Why Inter?**
- Open source, free
- Optimized for UI/screens
- Excellent readability at small sizes
- Wide language support (PL/EN)
- Variable font support for performance

#### Type Scale

```css
--text-xs:   0.75rem;   /* 12px - Small labels, captions */
--text-sm:   0.875rem;  /* 14px - Secondary text, metadata */
--text-base: 1rem;      /* 16px - Body text (default) */
--text-lg:   1.125rem;  /* 18px - Emphasized body */
--text-xl:   1.25rem;   /* 20px - Small headings */
--text-2xl:  1.5rem;    /* 24px - Section headings */
--text-3xl:  1.875rem;  /* 30px - Page titles */
--text-4xl:  2.25rem;   /* 36px - Hero text */
```

#### Font Weights

```css
--font-normal:    400;  /* Body text */
--font-medium:    500;  /* Subtle emphasis */
--font-semibold:  600;  /* Buttons, labels */
--font-bold:      700;  /* Headings */
```

#### Line Heights

```css
--leading-tight:   1.25;  /* Headings */
--leading-normal:  1.5;   /* Body text */
--leading-relaxed: 1.75;  /* Long-form content */
```

#### Typography Usage

```css
/* Headings */
h1 {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  line-height: var(--leading-tight);
  color: var(--neutral-900);
}

h2 {
  font-size: var(--text-2xl);
  font-weight: var(--font-semibold);
  line-height: var(--leading-tight);
  color: var(--neutral-900);
}

/* Body */
body {
  font-size: var(--text-base);
  font-weight: var(--font-normal);
  line-height: var(--leading-normal);
  color: var(--neutral-700);
}

/* Small text */
.text-small {
  font-size: var(--text-sm);
  color: var(--neutral-500);
}
```

### 2.3 Spacing System

**8px Grid System** - All spacing is a multiple of 8px (0.5rem)

```css
--space-0:  0;
--space-1:  0.25rem;  /*  4px - Tight spacing */
--space-2:  0.5rem;   /*  8px - Small gaps */
--space-3:  0.75rem;  /* 12px - Compact */
--space-4:  1rem;     /* 16px - Default */
--space-5:  1.25rem;  /* 20px */
--space-6:  1.5rem;   /* 24px - Section spacing */
--space-8:  2rem;     /* 32px - Large gaps */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px - Page sections */
--space-16: 4rem;     /* 64px - Major sections */
```

**Usage:**
- Padding: Use 4, 6, 8 for component internal spacing
- Margins: Use 6, 8, 12 for spacing between components
- Gaps: Use 2, 4, 6 for grid/flex gaps

### 2.4 Border Radius

```css
--radius-none: 0;
--radius-sm:   0.125rem;  /*  2px - Subtle */
--radius-base: 0.25rem;   /*  4px - Default */
--radius-md:   0.375rem;  /*  6px - Inputs */
--radius-lg:   0.5rem;    /*  8px - Cards */
--radius-xl:   0.75rem;   /* 12px - Large cards */
--radius-2xl:  1rem;      /* 16px - Modals */
--radius-full: 9999px;    /* Pills, avatars */
```

### 2.5 Shadows

```css
--shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
/* Usage: Subtle borders alternative */

--shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1),
             0 1px 2px 0 rgba(0, 0, 0, 0.06);
/* Usage: Small cards, dropdowns */

--shadow-base: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
               0 2px 4px -1px rgba(0, 0, 0, 0.06);
/* Usage: Cards, buttons hover */

--shadow-md: 0 10px 15px -3px rgba(0, 0, 0, 0.1),
             0 4px 6px -2px rgba(0, 0, 0, 0.05);
/* Usage: Raised cards, popovers */

--shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
             0 10px 10px -5px rgba(0, 0, 0, 0.04);
/* Usage: Modals, drawers */

--shadow-xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
/* Usage: Major overlays */
```

---

## 3. Component Library

### 3.1 Buttons

#### Primary Button

```svelte
<button class="btn btn-primary">
  {$_('button.save')}
</button>

<style>
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: var(--space-3) var(--space-6);
    font-size: var(--text-base);
    font-weight: var(--font-semibold);
    line-height: 1;
    border-radius: var(--radius-lg);
    border: none;
    cursor: pointer;
    transition: all 150ms ease;

    /* Touch target size ≥44×44px (WCAG) */
    min-height: 44px;
    min-width: 44px;
  }

  .btn-primary {
    background: var(--primary-500);
    color: white;
  }

  .btn-primary:hover {
    background: var(--primary-600);
    box-shadow: var(--shadow-base);
  }

  .btn-primary:active {
    background: var(--primary-700);
  }

  .btn-primary:disabled {
    background: var(--neutral-300);
    cursor: not-allowed;
  }
</style>
```

#### Button Variants

| Variant | Use Case | Example |
|---------|----------|---------|
| **Primary** | Main action | "Save Entry" |
| **Secondary** | Alternative action | "Cancel" |
| **Tertiary** | Less important action | "Skip" |
| **Danger** | Destructive action | "Delete Metric" |
| **Ghost** | Subtle action | Icon buttons |

### 3.2 Form Inputs

#### Text Input

```svelte
<div class="input-group">
  <label for="metric-name" class="label">
    {$_('metrics.form.name_label')}
  </label>
  <input
    id="metric-name"
    type="text"
    class="input"
    placeholder={$_('metrics.form.name_placeholder')}
    bind:value={metricName}
  />
  {#if error}
    <span class="error-message">{error}</span>
  {/if}
</div>

<style>
  .input-group {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
  }

  .label {
    font-size: var(--text-sm);
    font-weight: var(--font-medium);
    color: var(--neutral-700);
  }

  .input {
    padding: var(--space-3) var(--space-4);
    font-size: var(--text-base);
    line-height: var(--leading-normal);
    color: var(--neutral-900);
    background: white;
    border: 1px solid var(--neutral-300);
    border-radius: var(--radius-md);
    transition: all 150ms ease;

    /* Mobile optimization */
    min-height: 44px;
    font-size: 16px; /* Prevents zoom on iOS */
  }

  .input:focus {
    outline: none;
    border-color: var(--primary-500);
    box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.1);
  }

  .input::placeholder {
    color: var(--neutral-400);
  }

  .error-message {
    font-size: var(--text-sm);
    color: var(--error-500);
  }
</style>
```

#### Range Slider

```svelte
<div class="slider-group">
  <label class="label">
    {$_('metrics.mood')}
    <span class="value">{value}</span>
  </label>
  <input
    type="range"
    min={min}
    max={max}
    step="1"
    bind:value={value}
    class="slider"
  />
  <div class="slider-labels">
    <span>{min}</span>
    <span>{max}</span>
  </div>
</div>

<style>
  .slider {
    width: 100%;
    height: 8px;
    background: var(--neutral-200);
    border-radius: var(--radius-full);
    appearance: none;
  }

  .slider::-webkit-slider-thumb {
    appearance: none;
    width: 24px;
    height: 24px;
    background: var(--primary-500);
    border-radius: 50%;
    cursor: pointer;
    box-shadow: var(--shadow-sm);
  }

  .slider::-webkit-slider-thumb:hover {
    background: var(--primary-600);
    box-shadow: var(--shadow-base);
  }

  .slider-labels {
    display: flex;
    justify-content: space-between;
    font-size: var(--text-xs);
    color: var(--neutral-500);
  }
</style>
```

### 3.3 Cards

```svelte
<div class="card">
  <div class="card-header">
    <h3 class="card-title">{$_('metrics.list.title')}</h3>
  </div>
  <div class="card-body">
    <!-- Content -->
  </div>
</div>

<style>
  .card {
    background: white;
    border: 1px solid var(--neutral-200);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    overflow: hidden;
  }

  .card-header {
    padding: var(--space-6);
    border-bottom: 1px solid var(--neutral-200);
  }

  .card-title {
    font-size: var(--text-xl);
    font-weight: var(--font-semibold);
    color: var(--neutral-900);
  }

  .card-body {
    padding: var(--space-6);
  }
</style>
```

### 3.4 Navigation

#### Bottom Navigation (Mobile)

```svelte
<nav class="bottom-nav">
  {#each navItems as item}
    <a
      href={item.href}
      class="nav-item"
      class:active={$page.url.pathname === item.href}
    >
      <Icon name={item.icon} size={24} />
      <span class="nav-label">{$_(item.label)}</span>
    </a>
  {/each}
</nav>

<style>
  .bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    background: white;
    border-top: 1px solid var(--neutral-200);
    padding: var(--space-2) 0;
    z-index: var(--z-sticky);

    /* iOS safe area */
    padding-bottom: calc(var(--space-2) + env(safe-area-inset-bottom));
  }

  .nav-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-1);
    padding: var(--space-2);
    color: var(--neutral-500);
    text-decoration: none;
    transition: color 150ms;
  }

  .nav-item.active {
    color: var(--primary-500);
  }

  .nav-label {
    font-size: var(--text-xs);
    font-weight: var(--font-medium);
  }
</style>
```

---

## 4. Layout & Responsiveness

### 4.1 Breakpoints

```css
/* Mobile first approach */
--breakpoint-sm: 640px;   /* Small tablets */
--breakpoint-md: 768px;   /* Tablets */
--breakpoint-lg: 1024px;  /* Desktop */
--breakpoint-xl: 1280px;  /* Large desktop */
```

### 4.2 Container Widths

```css
.container {
  width: 100%;
  margin: 0 auto;
  padding: 0 var(--space-4);
}

@media (min-width: 640px) {
  .container {
    max-width: 640px;
    padding: 0 var(--space-6);
  }
}

@media (min-width: 768px) {
  .container {
    max-width: 768px;
  }
}

@media (min-width: 1024px) {
  .container {
    max-width: 900px;  /* Narrow for readability */
  }
}
```

### 4.3 Mobile-First Layout

```svelte
<div class="page-layout">
  <header class="page-header">
    <!-- Header -->
  </header>

  <main class="page-content">
    <!-- Main content -->
  </main>

  <nav class="page-nav">
    <!-- Mobile bottom nav -->
  </nav>
</div>

<style>
  .page-layout {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background: var(--neutral-50);
  }

  .page-header {
    padding: var(--space-4);
    background: white;
    border-bottom: 1px solid var(--neutral-200);
  }

  .page-content {
    flex: 1;
    padding: var(--space-4);
    padding-bottom: calc(64px + var(--space-4)); /* Bottom nav clearance */
    overflow-y: auto;
  }

  .page-nav {
    /* Bottom navigation - fixed */
  }

  /* Desktop: Side navigation */
  @media (min-width: 768px) {
    .page-layout {
      flex-direction: row;
    }

    .page-nav {
      position: static;
      width: 240px;
      border-right: 1px solid var(--neutral-200);
      border-top: none;
    }

    .page-content {
      padding-bottom: var(--space-4);
    }
  }
</style>
```

---

## 5. Data Visualization

### 5.1 Chart Colors

```css
/* Chart color palette - distinct, accessible */
--chart-1: #3B82F6;  /* Blue */
--chart-2: #10B981;  /* Green */
--chart-3: #F59E0B;  /* Amber */
--chart-4: #EF4444;  /* Red */
--chart-5: #8B5CF6;  /* Purple */
--chart-6: #EC4899;  /* Pink */
--chart-7: #14B8A6;  /* Teal */
--chart-8: #F97316;  /* Orange */
```

### 5.2 Chart Style Guidelines

```javascript
// Chart.js configuration
const chartConfig = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'bottom',
      labels: {
        font: {
          family: 'Inter',
          size: 14,
        },
        padding: 16,
        usePointStyle: true,
      },
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      padding: 12,
      cornerRadius: 8,
      titleFont: {
        family: 'Inter',
        size: 14,
        weight: 600,
      },
      bodyFont: {
        family: 'Inter',
        size: 13,
      },
    },
  },
  scales: {
    x: {
      grid: {
        color: 'rgba(0, 0, 0, 0.05)',
      },
      ticks: {
        font: {
          family: 'Inter',
          size: 12,
        },
      },
    },
    y: {
      grid: {
        color: 'rgba(0, 0, 0, 0.05)',
      },
      ticks: {
        font: {
          family: 'Inter',
          size: 12,
        },
      },
    },
  },
};
```

---

## 6. Accessibility (a11y)

### 6.1 WCAG 2.1 AA Requirements

✅ **Color Contrast**
- Normal text: ≥4.5:1
- Large text (≥18px or ≥14px bold): ≥3:1
- UI components: ≥3:1

✅ **Touch Targets**
- Minimum size: 44×44 pixels
- Spacing: ≥8px between targets

✅ **Keyboard Navigation**
- All interactive elements focusable
- Visible focus indicators
- Logical tab order

✅ **Screen Readers**
- Semantic HTML
- ARIA labels where needed
- Alt text for images/charts

### 6.2 Focus Styles

```css
/* Global focus indicator */
*:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}

button:focus-visible {
  outline: 3px solid var(--primary-500);
  outline-offset: 2px;
}

/* Skip to main content */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--primary-500);
  color: white;
  padding: var(--space-3) var(--space-6);
  text-decoration: none;
  z-index: 9999;
}

.skip-link:focus {
  top: 0;
}
```

### 6.3 ARIA Examples

```svelte
<!-- Button with icon -->
<button
  aria-label={$_('button.delete')}
  on:click={handleDelete}
>
  <Icon name="trash" aria-hidden="true" />
</button>

<!-- Loading state -->
<button aria-busy="true">
  <span class="sr-only">{$_('common.loading')}</span>
  <Spinner aria-hidden="true" />
</button>

<!-- Progress -->
<div
  role="progressbar"
  aria-valuenow={currentStep}
  aria-valuemin={1}
  aria-valuemax={totalSteps}
  aria-label={$_('onboarding.progress')}
>
  {currentStep} / {totalSteps}
</div>

<!-- Screen reader only text -->
<style>
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
  }
</style>
```

---

## 7. Micro-interactions & Animation

### 7.1 Animation Principles

- **Subtle**: Enhance, don't distract
- **Fast**: 150-300ms for most transitions
- **Purposeful**: Communicate state changes
- **Respectful**: Honor `prefers-reduced-motion`

### 7.2 Transition Timing

```css
--transition-fast:   150ms;  /* Hover, focus */
--transition-base:   250ms;  /* Default */
--transition-slow:   350ms;  /* Page transitions */
--transition-easing: cubic-bezier(0.4, 0, 0.2, 1); /* Smooth easing */
```

### 7.3 Common Animations

```css
/* Fade in */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Slide up */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Usage */
.card {
  animation: slideUp 250ms var(--transition-easing);
}

/* Respect reduced motion */
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

---

## 8. Loading & Empty States

### 8.1 Loading Spinner

```svelte
<div class="spinner" aria-label="Loading">
  <div class="spinner-ring"></div>
</div>

<style>
  .spinner {
    display: inline-block;
    width: 40px;
    height: 40px;
  }

  .spinner-ring {
    width: 100%;
    height: 100%;
    border: 4px solid var(--neutral-200);
    border-top-color: var(--primary-500);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }
</style>
```

### 8.2 Empty States

```svelte
<div class="empty-state">
  <Icon name="inbox" size={48} color="var(--neutral-300)" />
  <h3 class="empty-title">{$_('metrics.list.empty')}</h3>
  <p class="empty-description">
    {$_('metrics.list.empty_description')}
  </p>
  <Button on:click={createFirstMetric}>
    {$_('metrics.form.create_first')}
  </Button>
</div>

<style>
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--space-12) var(--space-6);
    text-align: center;
  }

  .empty-title {
    margin-top: var(--space-4);
    font-size: var(--text-lg);
    font-weight: var(--font-semibold);
    color: var(--neutral-700);
  }

  .empty-description {
    margin-top: var(--space-2);
    max-width: 320px;
    color: var(--neutral-500);
  }
</style>
```

---

## 9. Mobile Optimization

### 9.1 Touch-Friendly Design

```css
/* Minimum touch target size */
.touchable {
  min-width: 44px;
  min-height: 44px;
  padding: var(--space-3);
}

/* Adequate spacing between touch targets */
.button-group {
  display: flex;
  gap: var(--space-2); /* 8px minimum */
}
```

### 9.2 iOS Specific Optimizations

```css
/* Prevent zoom on input focus */
input, select, textarea {
  font-size: 16px; /* iOS zooms if <16px */
}

/* Safe area insets */
.page {
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}

/* Disable iOS input styling */
input[type="text"],
input[type="email"],
input[type="password"],
textarea {
  -webkit-appearance: none;
  appearance: none;
}
```

### 9.3 Performance

```svelte
<!-- Lazy load images -->
<img
  src={imageUrl}
  loading="lazy"
  decoding="async"
  alt={altText}
/>

<!-- Optimize fonts -->
<link
  rel="preload"
  href="/fonts/inter-var.woff2"
  as="font"
  type="font/woff2"
  crossorigin
/>
```

---

## 10. Design Checklist

### ✅ Every Component Must:
- [ ] Use design tokens (no hardcoded values)
- [ ] Support both PL and EN languages
- [ ] Meet WCAG AA color contrast
- [ ] Have 44×44px touch targets (mobile)
- [ ] Be keyboard navigable
- [ ] Have clear focus states
- [ ] Work on 320px width minimum
- [ ] Have loading states
- [ ] Have error states
- [ ] Have empty states
- [ ] Be responsive
- [ ] Respect `prefers-reduced-motion`

---

## 11. Figma Design File Structure

```
FeelInk Design System
├── 🎨 Foundations
│   ├── Colors
│   ├── Typography
│   ├── Spacing
│   ├── Shadows
│   └── Border Radius
├── 🧩 Components
│   ├── Buttons
│   ├── Inputs
│   ├── Cards
│   ├── Navigation
│   ├── Charts
│   └── Modals
├── 📱 Screens - Mobile
│   ├── Onboarding
│   ├── Dashboard
│   ├── Daily Log
│   ├── Metrics
│   ├── Insights
│   └── Settings
└── 💻 Screens - Desktop
    └── (same as mobile)
```

---

## 12. Related Documents

- [I18N_STRATEGY.md](./I18N_STRATEGY.md) - Internationalization
- [ARCHITECTURE.md](./ARCHITECTURE.md) - Technical architecture
- [REQUIREMENTS.md](./REQUIREMENTS.md) - Functional requirements

---

**Status**: Design system ready for implementation
**Next Steps**: Create component library in Svelte
