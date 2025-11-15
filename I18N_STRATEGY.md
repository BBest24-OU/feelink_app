# Internationalization (i18n) Strategy

## Document Information
- **Version**: 0.1.0
- **Last Updated**: 2025-11-15
- **Status**: Implementation Guide
- **Languages**: Polish (pl), English (en)

---

## 1. Overview

This document outlines the comprehensive internationalization (i18n) strategy for FeelInk, ensuring the application is fully localized for Polish and English speakers from day one, with the architecture ready for additional languages in the future.

### 1.1 Core Principles

1. **Zero Hardcoded Strings**: NO text in source code
2. **Zero Hardcoded Styles**: Centralized theme management
3. **Locale-Aware Formatting**: Dates, numbers, currencies respect locale
4. **Scalable Architecture**: Easy to add new languages
5. **Performant**: Minimal bundle size impact

---

## 2. Technology Stack

### 2.1 Frontend i18n Library

**Recommendation: svelte-i18n**

```bash
npm install svelte-i18n
```

**Why svelte-i18n?**
- ✅ Native Svelte integration
- ✅ Small bundle size
- ✅ Runtime locale switching
- ✅ Plural forms support
- ✅ Date/number formatting
- ✅ Fallback language support
- ✅ TypeScript support

### 2.2 Alternative Options

| Library | Pros | Cons | Verdict |
|---------|------|------|---------|
| **svelte-i18n** | Native, lightweight, good DX | Smaller ecosystem | ✅ Recommended |
| **svelte-intl** | Similar features | Less maintained | ❌ |
| **Format.js** | Powerful, ICU format | Heavier, React-focused | ❌ |
| **i18next** | Most popular, huge ecosystem | Overkill for 2 languages | 🟡 Alternative |

---

## 3. File Structure

### 3.1 Directory Layout

```
feelink_app/
├── frontend/
│   ├── src/
│   │   ├── i18n/
│   │   │   ├── index.ts              # i18n initialization
│   │   │   ├── locales/
│   │   │   │   ├── en/
│   │   │   │   │   ├── common.json
│   │   │   │   │   ├── auth.json
│   │   │   │   │   ├── metrics.json
│   │   │   │   │   ├── insights.json
│   │   │   │   │   ├── reports.json
│   │   │   │   │   └── errors.json
│   │   │   │   └── pl/
│   │   │   │       ├── common.json
│   │   │   │       ├── auth.json
│   │   │   │       ├── metrics.json
│   │   │   │       ├── insights.json
│   │   │   │       ├── reports.json
│   │   │   │       └── errors.json
│   │   │   └── types.ts              # TypeScript types
│   │   ├── theme/
│   │   │   ├── index.ts              # Theme initialization
│   │   │   ├── tokens.ts             # Design tokens
│   │   │   ├── colors.ts             # Color palette
│   │   │   ├── typography.ts         # Font scales
│   │   │   └── spacing.ts            # Spacing system
│   │   └── ...
```

### 3.2 Namespace Organization

Organize translations by feature/domain to keep files manageable:

| Namespace | Purpose | Example Keys |
|-----------|---------|--------------|
| **common** | Shared across app | `button.save`, `button.cancel`, `nav.dashboard` |
| **auth** | Authentication | `login.title`, `register.email`, `password.reset` |
| **metrics** | Metric management | `categories.physical`, `types.range`, `form.create` |
| **insights** | Analytics & correlations | `correlation.strong`, `lag.days`, `significance.high` |
| **reports** | Report generation | `pdf.title`, `export.csv`, `date_range.label` |
| **errors** | Error messages | `validation.required`, `api.network_error` |

---

## 4. Implementation

### 4.1 Setup and Initialization

```typescript
// src/i18n/index.ts

import { register, init, getLocaleFromNavigator, locale } from 'svelte-i18n';

// Register locales
register('en', () => import('./locales/en/common.json'));
register('en', () => import('./locales/en/auth.json'));
register('en', () => import('./locales/en/metrics.json'));
register('en', () => import('./locales/en/insights.json'));
register('en', () => import('./locales/en/reports.json'));
register('en', () => import('./locales/en/errors.json'));

register('pl', () => import('./locales/pl/common.json'));
register('pl', () => import('./locales/pl/auth.json'));
register('pl', () => import('./locales/pl/metrics.json'));
register('pl', () => import('./locales/pl/insights.json'));
register('pl', () => import('./locales/pl/reports.json'));
register('pl', () => import('./locales/pl/errors.json'));

// Initialize
init({
  fallbackLocale: 'en',
  initialLocale: getLocaleFromNavigator(),
});

// Export locale store for app-wide access
export { locale };
```

### 4.2 Translation Files

#### English Example (locales/en/common.json)

```json
{
  "app": {
    "name": "FeelInk",
    "tagline": "Track your mental health, discover insights"
  },
  "nav": {
    "dashboard": "Dashboard",
    "metrics": "Metrics",
    "log": "Daily Log",
    "insights": "Insights",
    "reports": "Reports",
    "settings": "Settings"
  },
  "button": {
    "save": "Save",
    "cancel": "Cancel",
    "delete": "Delete",
    "edit": "Edit",
    "add": "Add",
    "export": "Export",
    "back": "Back",
    "next": "Next",
    "finish": "Finish",
    "confirm": "Confirm"
  },
  "time": {
    "today": "Today",
    "yesterday": "Yesterday",
    "last_7_days": "Last 7 days",
    "last_30_days": "Last 30 days",
    "last_90_days": "Last 90 days",
    "all_time": "All time",
    "custom_range": "Custom range"
  },
  "validation": {
    "required": "This field is required",
    "email_invalid": "Please enter a valid email",
    "password_min_length": "Password must be at least {min} characters",
    "number_min": "Value must be at least {min}",
    "number_max": "Value cannot exceed {max}",
    "date_future": "Date cannot be in the future"
  }
}
```

#### Polish Example (locales/pl/common.json)

```json
{
  "app": {
    "name": "FeelInk",
    "tagline": "Śledź swoje zdrowie psychiczne, odkrywaj wzorce"
  },
  "nav": {
    "dashboard": "Pulpit",
    "metrics": "Metryki",
    "log": "Dziennik",
    "insights": "Analizy",
    "reports": "Raporty",
    "settings": "Ustawienia"
  },
  "button": {
    "save": "Zapisz",
    "cancel": "Anuluj",
    "delete": "Usuń",
    "edit": "Edytuj",
    "add": "Dodaj",
    "export": "Eksportuj",
    "back": "Wstecz",
    "next": "Dalej",
    "finish": "Zakończ",
    "confirm": "Potwierdź"
  },
  "time": {
    "today": "Dzisiaj",
    "yesterday": "Wczoraj",
    "last_7_days": "Ostatnie 7 dni",
    "last_30_days": "Ostatnie 30 dni",
    "last_90_days": "Ostatnie 90 dni",
    "all_time": "Cały okres",
    "custom_range": "Własny zakres"
  },
  "validation": {
    "required": "To pole jest wymagane",
    "email_invalid": "Wprowadź poprawny adres email",
    "password_min_length": "Hasło musi mieć co najmniej {min} znaków",
    "number_min": "Wartość musi być co najmniej {min}",
    "number_max": "Wartość nie może przekraczać {max}",
    "date_future": "Data nie może być w przyszłości"
  }
}
```

#### Metrics Namespace Example (locales/en/metrics.json)

```json
{
  "categories": {
    "physical": "Physical Symptoms",
    "psychological": "Psychological Symptoms",
    "triggers": "Triggers",
    "medications": "Medications",
    "selfcare": "Self-Care",
    "wellness": "Wellness",
    "notes": "Notes"
  },
  "categories_description": {
    "physical": "Track physical symptoms like pain, fatigue, or tension",
    "psychological": "Monitor mood, anxiety, energy, and mental state",
    "triggers": "Record stressful events or situations",
    "medications": "Track medication intake and effectiveness",
    "selfcare": "Log self-care activities like meditation or journaling",
    "wellness": "Monitor sleep, exercise, diet, and overall wellness",
    "notes": "Free-form observations and reflections"
  },
  "value_types": {
    "range": "Range (min-max)",
    "number": "Number",
    "boolean": "Yes/No",
    "count": "Count",
    "text": "Text note"
  },
  "form": {
    "create_title": "Create New Metric",
    "edit_title": "Edit Metric",
    "name_label": "Metric Name",
    "name_placeholder": "e.g., Mood, Pain Level, Hours Slept",
    "category_label": "Category",
    "value_type_label": "Value Type",
    "min_value_label": "Minimum Value",
    "max_value_label": "Maximum Value",
    "description_label": "Description (optional)",
    "color_label": "Color",
    "icon_label": "Icon"
  },
  "list": {
    "title": "Your Metrics",
    "empty": "No metrics yet. Create your first one!",
    "active": "Active",
    "archived": "Archived"
  }
}
```

#### Insights/Correlations Example (locales/en/insights.json)

```json
{
  "correlation": {
    "title": "Discovered Relationships",
    "strength": {
      "strong": "Strong",
      "moderate": "Moderate",
      "weak": "Weak"
    },
    "direction": {
      "positive": "positive",
      "negative": "negative"
    },
    "confidence": {
      "very_high": "Very confident",
      "high": "Confident",
      "medium": "Somewhat confident",
      "low": "Not enough evidence"
    },
    "lag": {
      "same_day": "Same day effect",
      "days_later": "{count} {count, plural, one {day} other {days}} later",
      "no_delay": "No delay"
    },
    "description": {
      "positive_same_day": "When {metric1} increases, {metric2} tends to increase that same day.",
      "negative_same_day": "When {metric1} increases, {metric2} tends to decrease that same day.",
      "positive_lag": "When {metric1} increases, {metric2} tends to increase {lag} later.",
      "negative_lag": "When {metric1} increases, {metric2} tends to decrease {lag} later."
    }
  },
  "statistics": {
    "mean": "Average",
    "median": "Median",
    "min": "Minimum",
    "max": "Maximum",
    "std_dev": "Variability",
    "trend": "Trend"
  },
  "insufficient_data": {
    "title": "Not enough data yet",
    "message": "Track for at least {days} more {days, plural, one {day} other {days}} to discover correlations.",
    "current_days": "You have {count} {count, plural, one {day} other {days}} of data so far."
  }
}
```

### 4.3 Using Translations in Components

```svelte
<!-- Example: DailyLog.svelte -->

<script lang="ts">
  import { _ } from 'svelte-i18n';
  import { metrics } from '$stores/metrics';
  import Button from '$components/Button.svelte';

  let formData = {};

  function handleSubmit() {
    // ...
  }
</script>

<div class="daily-log">
  <h1>{$_('nav.log')}</h1>
  <p class="subtitle">{$_('time.today')}</p>

  <form on:submit|preventDefault={handleSubmit}>
    {#each $metrics as metric}
      <div class="metric-input">
        <label for={metric.id}>
          {$_(metric.nameKey)}  <!-- Translatable metric name -->
        </label>

        {#if metric.valueType === 'range'}
          <input
            type="range"
            id={metric.id}
            min={metric.minValue}
            max={metric.maxValue}
            bind:value={formData[metric.id]}
          />
        {/if}
      </div>
    {/each}

    <div class="actions">
      <Button type="submit">{$_('button.save')}</Button>
      <Button variant="secondary">{$_('button.cancel')}</Button>
    </div>
  </form>
</div>
```

### 4.4 Dynamic Translations with Interpolation

```svelte
<script>
  import { _, number } from 'svelte-i18n';

  let daysTracked = 12;
  let daysNeeded = 7;
  let daysRemaining = Math.max(0, daysNeeded - daysTracked);
</script>

{#if daysRemaining > 0}
  <p>
    {$_('insights.insufficient_data.message', { values: { days: daysRemaining } })}
  </p>
  <p>
    {$_('insights.insufficient_data.current_days', { values: { count: daysTracked } })}
  </p>
{/if}

<!-- Output (English): -->
<!-- Track for at least 5 more days to discover correlations. -->
<!-- You have 12 days of data so far. -->

<!-- Output (Polish): -->
<!-- Śledź jeszcze przez co najmniej 5 dni, aby odkryć korelacje. -->
<!-- Masz obecnie 12 dni danych. -->
```

### 4.5 Pluralization

```json
// locales/en/insights.json
{
  "correlation": {
    "lag": {
      "days_later": "{count} {count, plural, one {day} other {days}} later"
    }
  }
}

// locales/pl/insights.json
{
  "correlation": {
    "lag": {
      "days_later": "{count} {count, plural, one {dzień} few {dni} many {dni} other {dnia}} później"
    }
  }
}
```

```svelte
<script>
  import { _ } from 'svelte-i18n';
  let lag = 3;
</script>

<p>{$_('correlation.lag.days_later', { values: { count: lag } })}</p>

<!-- English: "3 days later" -->
<!-- Polish: "3 dni później" -->
```

---

## 5. Date & Number Formatting

### 5.1 Date Formatting

```svelte
<script lang="ts">
  import { date, locale } from 'svelte-i18n';

  let today = new Date();
  let entryDate = new Date('2025-11-10');
</script>

<!-- Short date -->
<p>{$date(today, { format: 'short' })}</p>
<!-- en: 11/15/25 -->
<!-- pl: 15.11.25 -->

<!-- Medium date -->
<p>{$date(entryDate, { format: 'medium' })}</p>
<!-- en: Nov 10, 2025 -->
<!-- pl: 10 lis 2025 -->

<!-- Long date -->
<p>{$date(today, { format: 'long' })}</p>
<!-- en: November 15, 2025 -->
<!-- pl: 15 listopada 2025 -->

<!-- Custom format -->
<p>{$date(today, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>
<!-- en: Saturday, November 15, 2025 -->
<!-- pl: sobota, 15 listopada 2025 -->
```

### 5.2 Number Formatting

```svelte
<script>
  import { number } from 'svelte-i18n';

  let correlationCoef = 0.8234;
  let pValue = 0.0012;
  let sampleSize = 1234;
</script>

<!-- Decimal (2 places) -->
<p>r = {$number(correlationCoef, { maximumFractionDigits: 2 })}</p>
<!-- en: r = 0.82 -->
<!-- pl: r = 0,82 -->

<!-- Scientific notation -->
<p>p = {$number(pValue, { notation: 'scientific', maximumFractionDigits: 2 })}</p>
<!-- en: p = 1.2E-3 -->
<!-- pl: p = 1,2E-3 -->

<!-- With thousands separator -->
<p>n = {$number(sampleSize)}</p>
<!-- en: n = 1,234 -->
<!-- pl: n = 1 234 -->
```

### 5.3 Relative Time

```typescript
// utils/relativeTime.ts

import { locale, _ } from 'svelte-i18n';
import { formatDistanceToNow } from 'date-fns';
import { pl, enUS } from 'date-fns/locale';

const locales = { en: enUS, pl: pl };

export function getRelativeTime(date: Date): string {
  const currentLocale = get(locale) || 'en';
  return formatDistanceToNow(date, {
    addSuffix: true,
    locale: locales[currentLocale]
  });
}
```

```svelte
<script>
  import { getRelativeTime } from '$utils/relativeTime';

  let lastSync = new Date('2025-11-15T10:30:00');
</script>

<p>Last sync: {getRelativeTime(lastSync)}</p>
<!-- en: "Last sync: 2 hours ago" -->
<!-- pl: "Last sync: 2 godziny temu" -->
```

---

## 6. Theme & Style Management

### 6.1 Design Tokens (No Hardcoded Values!)

```typescript
// src/theme/tokens.ts

export const designTokens = {
  // Color palette
  colors: {
    // Primary
    primary: {
      50: '#E8F5F4',
      100: '#C1E7E3',
      500: '#14B8A6',  // Main brand color
      600: '#0D9488',
      700: '#0F766E',
      900: '#134E4A',
    },
    // Semantic colors
    success: '#10B981',
    warning: '#F59E0B',
    error: '#EF4444',
    info: '#3B82F6',
    // Neutral
    neutral: {
      50: '#F9FAFB',
      100: '#F3F4F6',
      200: '#E5E7EB',
      300: '#D1D5DB',
      500: '#6B7280',
      700: '#374151',
      900: '#111827',
    },
    // Surface
    background: {
      primary: '#FFFFFF',
      secondary: '#F9FAFB',
      tertiary: '#F3F4F6',
    },
    text: {
      primary: '#111827',
      secondary: '#6B7280',
      tertiary: '#9CA3AF',
      inverse: '#FFFFFF',
    },
  },

  // Typography
  typography: {
    fontFamily: {
      sans: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
      mono: "'JetBrains Mono', 'Fira Code', monospace",
    },
    fontSize: {
      xs: '0.75rem',    // 12px
      sm: '0.875rem',   // 14px
      base: '1rem',     // 16px
      lg: '1.125rem',   // 18px
      xl: '1.25rem',    // 20px
      '2xl': '1.5rem',  // 24px
      '3xl': '1.875rem',// 30px
      '4xl': '2.25rem', // 36px
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
    lineHeight: {
      tight: 1.25,
      normal: 1.5,
      relaxed: 1.75,
    },
  },

  // Spacing
  spacing: {
    0: '0',
    1: '0.25rem',   // 4px
    2: '0.5rem',    // 8px
    3: '0.75rem',   // 12px
    4: '1rem',      // 16px
    5: '1.25rem',   // 20px
    6: '1.5rem',    // 24px
    8: '2rem',      // 32px
    10: '2.5rem',   // 40px
    12: '3rem',     // 48px
    16: '4rem',     // 64px
  },

  // Border radius
  borderRadius: {
    none: '0',
    sm: '0.125rem',  // 2px
    base: '0.25rem', // 4px
    md: '0.375rem',  // 6px
    lg: '0.5rem',    // 8px
    xl: '0.75rem',   // 12px
    '2xl': '1rem',   // 16px
    full: '9999px',
  },

  // Shadows
  shadow: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    base: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
  },

  // Breakpoints
  breakpoints: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },

  // Z-index
  zIndex: {
    dropdown: 1000,
    sticky: 1020,
    fixed: 1030,
    modalBackdrop: 1040,
    modal: 1050,
    popover: 1060,
    tooltip: 1070,
  },
};
```

### 6.2 CSS Custom Properties

```css
/* src/theme/global.css */

:root {
  /* Colors */
  --color-primary: #14B8A6;
  --color-primary-hover: #0D9488;
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-error: #EF4444;

  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #F9FAFB;
  --color-text-primary: #111827;
  --color-text-secondary: #6B7280;

  /* Typography */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;

  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;

  /* Border radius */
  --radius-sm: 0.125rem;
  --radius-base: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-base: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* Future: Dark mode */
[data-theme="dark"] {
  --color-bg-primary: #111827;
  --color-bg-secondary: #1F2937;
  --color-text-primary: #F9FAFB;
  --color-text-secondary: #D1D5DB;
}
```

### 6.3 Using Theme in Components

```svelte
<!-- ❌ BAD: Hardcoded values -->
<button style="background: #14B8A6; padding: 16px; border-radius: 8px;">
  Save
</button>

<!-- ✅ GOOD: Using theme -->
<button class="btn-primary">
  {$_('button.save')}
</button>

<style>
  .btn-primary {
    background: var(--color-primary);
    padding: var(--space-4);
    border-radius: var(--radius-lg);
    color: var(--color-text-inverse);
    font-size: var(--text-base);
    font-family: var(--font-sans);
  }

  .btn-primary:hover {
    background: var(--color-primary-hover);
  }
</style>
```

### 6.4 Tailwind CSS Integration (Recommended)

```javascript
// tailwind.config.js

import { designTokens } from './src/theme/tokens';

export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: designTokens.colors,
      fontFamily: designTokens.typography.fontFamily,
      fontSize: designTokens.typography.fontSize,
      spacing: designTokens.spacing,
      borderRadius: designTokens.borderRadius,
      boxShadow: designTokens.shadow,
      zIndex: designTokens.zIndex,
    },
  },
  plugins: [],
};
```

```svelte
<!-- Using Tailwind with centralized theme -->
<button class="bg-primary-500 hover:bg-primary-600 text-white px-4 py-2 rounded-lg">
  {$_('button.save')}
</button>
```

---

## 7. Language Switcher Component

```svelte
<!-- src/components/LanguageSwitcher.svelte -->

<script lang="ts">
  import { locale } from 'svelte-i18n';

  const languages = [
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'pl', name: 'Polski', flag: '🇵🇱' },
  ];

  function setLocale(lang: string) {
    locale.set(lang);
    localStorage.setItem('locale', lang);
  }
</script>

<div class="language-switcher">
  {#each languages as lang}
    <button
      class="lang-btn"
      class:active={$locale === lang.code}
      on:click={() => setLocale(lang.code)}
    >
      <span class="flag">{lang.flag}</span>
      <span class="name">{lang.name}</span>
    </button>
  {/each}
</div>

<style>
  .language-switcher {
    display: flex;
    gap: var(--space-2);
  }

  .lang-btn {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-2) var(--space-3);
    border: 1px solid var(--color-neutral-200);
    border-radius: var(--radius-md);
    background: var(--color-bg-primary);
    cursor: pointer;
    transition: all 0.2s;
  }

  .lang-btn:hover {
    background: var(--color-bg-secondary);
  }

  .lang-btn.active {
    background: var(--color-primary);
    color: white;
    border-color: var(--color-primary);
  }

  .flag {
    font-size: var(--text-lg);
  }

  .name {
    font-size: var(--text-sm);
    font-weight: var(--font-medium);
  }
</style>
```

---

## 8. Backend i18n (API Responses)

### 8.1 Error Messages

```python
# backend/i18n/messages.py

MESSAGES = {
    "en": {
        "auth.login.invalid_credentials": "Invalid email or password",
        "auth.register.email_exists": "Email already registered",
        "validation.required": "Field '{field}' is required",
        "validation.min_value": "Value must be at least {min}",
        "metric.not_found": "Metric not found",
        "entry.date_exists": "Entry for this date already exists",
    },
    "pl": {
        "auth.login.invalid_credentials": "Nieprawidłowy email lub hasło",
        "auth.register.email_exists": "Email już zarejestrowany",
        "validation.required": "Pole '{field}' jest wymagane",
        "validation.min_value": "Wartość musi być co najmniej {min}",
        "metric.not_found": "Metryka nie znaleziona",
        "entry.date_exists": "Wpis dla tej daty już istnieje",
    }
}

def get_message(key: str, lang: str = "en", **kwargs) -> str:
    """Get translated message."""
    template = MESSAGES.get(lang, MESSAGES["en"]).get(key, key)
    return template.format(**kwargs)
```

### 8.2 API Error Response

```python
from fastapi import HTTPException, Request

def get_user_language(request: Request) -> str:
    """Extract language from Accept-Language header."""
    accept_lang = request.headers.get("Accept-Language", "en")
    # Simple extraction (can be more sophisticated)
    lang = accept_lang.split(",")[0].split("-")[0]
    return lang if lang in ["en", "pl"] else "en"

@app.post("/api/v1/auth/login")
async def login(request: Request, credentials: LoginRequest):
    user = await authenticate(credentials.email, credentials.password)
    if not user:
        lang = get_user_language(request)
        raise HTTPException(
            status_code=401,
            detail=get_message("auth.login.invalid_credentials", lang)
        )
    # ...
```

---

## 9. Testing i18n

### 9.1 Translation Coverage Test

```typescript
// tests/i18n/coverage.test.ts

import { describe, it, expect } from 'vitest';
import enCommon from '$i18n/locales/en/common.json';
import plCommon from '$i18n/locales/pl/common.json';

describe('Translation Coverage', () => {
  function getKeys(obj: any, prefix = ''): string[] {
    return Object.keys(obj).reduce((keys, key) => {
      const fullKey = prefix ? `${prefix}.${key}` : key;
      if (typeof obj[key] === 'object' && obj[key] !== null) {
        return [...keys, ...getKeys(obj[key], fullKey)];
      }
      return [...keys, fullKey];
    }, [] as string[]);
  }

  it('Polish should have all English keys', () => {
    const enKeys = getKeys(enCommon);
    const plKeys = getKeys(plCommon);

    const missingKeys = enKeys.filter(key => !plKeys.includes(key));

    expect(missingKeys).toEqual([]);
  });

  it('English should have all Polish keys (no extras)', () => {
    const enKeys = getKeys(enCommon);
    const plKeys = getKeys(plCommon);

    const extraKeys = plKeys.filter(key => !enKeys.includes(key));

    expect(extraKeys).toEqual([]);
  });
});
```

### 9.2 TypeScript Type Safety

```typescript
// src/i18n/types.ts

import type enCommon from './locales/en/common.json';
import type enAuth from './locales/en/auth.json';

type TranslationKeys =
  | `common.${DeepKeys<typeof enCommon>}`
  | `auth.${DeepKeys<typeof enAuth>}`;

// Helper type to get nested keys
type DeepKeys<T> = T extends object
  ? {
      [K in keyof T]: K extends string
        ? T[K] extends object
          ? `${K}.${DeepKeys<T[K]>}`
          : K
        : never;
    }[keyof T]
  : never;

// Extend svelte-i18n types
declare module 'svelte-i18n' {
  export function _(key: TranslationKeys, options?: any): string;
}
```

---

## 10. Best Practices & Checklist

### ✅ DO:
- ✅ Use translation keys for ALL user-facing text
- ✅ Use design tokens for ALL styles
- ✅ Test both languages for every feature
- ✅ Use proper pluralization
- ✅ Format dates/numbers according to locale
- ✅ Keep translation files organized by feature
- ✅ Use meaningful, hierarchical keys (e.g., `metrics.form.name_label`)
- ✅ Provide context in comments for translators
- ✅ Use interpolation for dynamic values

### ❌ DON'T:
- ❌ Hardcode strings in components
- ❌ Hardcode colors, sizes, or spacing
- ❌ Concatenate translated strings
- ❌ Use English as a fallback in code (let i18n lib handle it)
- ❌ Translate in code (e.g., `isEnglish ? 'Save' : 'Zapisz'`)
- ❌ Use cryptic keys (e.g., `msg_001`)

---

## 11. Workflow & Maintenance

### 11.1 Adding New Translations

1. **Add to English first** (source language)
   ```json
   // locales/en/metrics.json
   {
     "form": {
       "new_field_label": "New Field"
     }
   }
   ```

2. **Add to Polish** (immediately!)
   ```json
   // locales/pl/metrics.json
   {
     "form": {
       "new_field_label": "Nowe Pole"
     }
   }
   ```

3. **Run coverage tests**
   ```bash
   npm run test:i18n
   ```

4. **Use in component**
   ```svelte
   <label>{$_('metrics.form.new_field_label')}</label>
   ```

### 11.2 Translation Workflow

```
Developer adds feature
       ↓
Add English translation keys
       ↓
Add placeholder Polish (or use English temporarily)
       ↓
Mark as TODO in translation file
       ↓
Professional translator reviews
       ↓
Update Polish translations
       ↓
Run tests
       ↓
Commit
```

### 11.3 Finding Missing Translations

```bash
# Run this script to find keys that need translation
npm run i18n:missing
```

```javascript
// scripts/find-missing-translations.js

import en from '../src/i18n/locales/en/common.json' assert { type: 'json' };
import pl from '../src/i18n/locales/pl/common.json' assert { type: 'json' };

function findMissing(source, target, path = '') {
  const missing = [];

  for (const key in source) {
    const currentPath = path ? `${path}.${key}` : key;

    if (!(key in target)) {
      missing.push(currentPath);
    } else if (typeof source[key] === 'object' && source[key] !== null) {
      missing.push(...findMissing(source[key], target[key], currentPath));
    }
  }

  return missing;
}

const missingInPolish = findMissing(en, pl);

if (missingInPolish.length > 0) {
  console.log('❌ Missing Polish translations:');
  missingInPolish.forEach(key => console.log(`  - ${key}`));
  process.exit(1);
} else {
  console.log('✅ All translations present!');
}
```

---

## 12. Related Documents

- [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)
- [REQUIREMENTS.md](./REQUIREMENTS.md)
- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [UI_UX_GUIDELINES.md](./UI_UX_GUIDELINES.md)

---

**Status**: Ready for implementation
**Next Steps**: Set up i18n infrastructure in codebase
