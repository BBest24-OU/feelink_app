# Design Guidelines - Feelink

## Overview
This document defines the visual design system and guidelines for the Feelink application. All developers and designers must follow these guidelines to maintain consistency across the application.

**Last Updated:** 2025-11-18
**Status:** Active

---

## 🎨 Design Philosophy

Feelink follows a **minimalist, clean, and professional** design approach that prioritizes:
- Clarity and readability
- Consistency across all components
- User-focused functionality over visual decoration
- Accessibility and usability

---

## 🎯 Core Principles

### 1. Minimalism First
- Use clean, simple layouts with plenty of white space
- Avoid unnecessary visual decorations
- Focus on functionality and usability
- Let content breathe

### 2. No Rainbow Colors
- **DO NOT** use gradient backgrounds or rainbow color schemes
- Stick to the defined color palette
- Use subtle accent colors sparingly
- Maintain professional appearance

### 3. Consistent Iconography
- **ONLY use icons from Lucide library** (`lucide-svelte`)
- Never use emoji, custom SVGs, or other icon libraries
- Consistent icon sizing: 16px (mobile), 18px (desktop), 20-24px (large actions)
- Icons should always have semantic meaning

---

## 🎨 Color Palette

### Primary Colors
```
Primary (Blue):   #4F46E5  (primary-600)
Secondary (Teal): #0D9488  (secondary-600)
```

### Neutral Colors
```
Gray Scale:
- gray-50:  #F9FAFB
- gray-100: #F3F4F6
- gray-200: #E5E7EB
- gray-500: #6B7280
- gray-600: #4B5563
- gray-700: #374151
- gray-800: #1F2937
- gray-900: #111827
```

### Status Colors
```
Success:  #10B981 (green-500)
Warning:  #F59E0B (amber-500)
Error:    #EF4444 (red-500)
Info:     #3B82F6 (blue-500)
```

### Usage Rules
- Use primary color for main actions and brand elements
- Use secondary color sparingly for secondary actions
- Use gray scale for backgrounds, borders, and text
- Reserve status colors for alerts, notifications, and feedback
- **NO gradients** - use solid colors only

---

## 🔤 Typography

### Font Family
```css
font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

### Font Sizes
```
text-xs:   0.75rem  (12px)
text-sm:   0.875rem (14px)
text-base: 1rem     (16px)
text-lg:   1.125rem (18px)
text-xl:   1.25rem  (20px)
text-2xl:  1.5rem   (24px)
text-3xl:  1.875rem (30px)
```

### Font Weights
```
font-normal:   400
font-medium:   500
font-semibold: 600
font-bold:     700
```

---

## 🧩 Component Guidelines

### Buttons
```typescript
// Variants
primary:   solid primary color background
secondary: solid secondary color background
danger:    solid red background
ghost:     transparent background

// NO GRADIENTS allowed
```

### Cards
```css
Background: white
Border: 1px solid gray-100
Border radius: 0.75rem (rounded-xl)
Shadow: subtle (shadow-sm)
Hover: slight shadow increase (shadow-md)
```

### Inputs
```css
Border: 1px solid gray-300
Focus: ring-2 ring-primary-500
Border radius: 0.5rem (rounded-lg)
Padding: px-4 py-2
```

### Navigation
```css
Background: white
Border: 1px solid gray-200 (bottom only)
Shadow: shadow-sm
Position: sticky top-0
```

---

## 🎭 Icon System

### Icon Library: Lucide Only
**IMPORTANT:** All icons in the Feelink application **MUST** use the Lucide icon library.

#### Installation
```bash
npm install lucide-svelte
```

#### Usage
```svelte
<script>
  import { IconName } from 'lucide-svelte';
</script>

<IconName size={18} />
```

#### Common Icons Used in Feelink
```typescript
// Navigation
LayoutDashboard  - Dashboard
PenLine          - Daily Log
FileText         - Entries
Activity         - Metrics
Lightbulb        - Insights
Link2            - Correlations

// Actions
LogOut           - Logout
Plus             - Add/Create
Edit             - Edit
Trash2           - Delete
Save             - Save
X                - Close/Cancel
Check            - Confirm
Search           - Search
Filter           - Filter
Settings         - Settings

// Status
AlertCircle      - Error/Warning
CheckCircle      - Success
Info             - Information
AlertTriangle    - Warning
```

#### Icon Sizing
```
Mobile:  size={16}
Desktop: size={18}
Large:   size={20} or size={24}
```

#### Rules
- ✅ **DO** use Lucide icons for all UI elements
- ✅ **DO** maintain consistent sizing within context
- ✅ **DO** use semantic, meaningful icons
- ❌ **DON'T** use emoji
- ❌ **DON'T** use other icon libraries (Font Awesome, Material Icons, etc.)
- ❌ **DON'T** create custom SVG icons unless absolutely necessary
- ❌ **DON'T** mix different icon styles

---

## 📐 Spacing System

### Spacing Scale (Tailwind)
```
space-1:  0.25rem  (4px)
space-2:  0.5rem   (8px)
space-3:  0.75rem  (12px)
space-4:  1rem     (16px)
space-6:  1.5rem   (24px)
space-8:  2rem     (32px)
space-12: 3rem     (48px)
```

### Common Usage
```
Gap between items:        space-x-2 or space-y-2
Padding in cards:         p-6
Padding in buttons:       px-4 py-2
Margin between sections:  mb-8
```

---

## 🎬 Animations & Transitions

### Transition Duration
```css
transition-all duration-200  /* Standard */
```

### Hover Effects
```css
/* Buttons */
hover:bg-primary-700 hover:shadow

/* Cards */
hover:shadow-md hover:border-gray-200

/* Links/Navigation */
hover:text-gray-900 hover:bg-gray-50
```

### Rules
- Keep transitions subtle and fast (200ms)
- Only animate meaningful state changes
- Don't overuse animations

---

## 📱 Responsive Design

### Breakpoints
```
sm:  640px   /* Small devices */
md:  768px   /* Medium devices */
lg:  1024px  /* Large devices */
xl:  1280px  /* Extra large devices */
```

### Mobile-First Approach
```svelte
<!-- Base styles apply to mobile -->
<div class="text-sm md:text-base lg:text-lg">

<!-- Show/hide based on screen size -->
<div class="hidden md:block">Desktop only</div>
<div class="md:hidden">Mobile only</div>
```

---

## ✅ Accessibility

### Focus States
- All interactive elements must have visible focus states
- Use `focus:ring-2 focus:ring-primary-500`

### Color Contrast
- Maintain WCAG AA compliance (4.5:1 for text)
- Test with color contrast checker

### Keyboard Navigation
- All functionality accessible via keyboard
- Logical tab order
- Visible focus indicators

---

## 🚫 Don'ts - Common Mistakes

### ❌ Don't Use
- Gradients on backgrounds
- Rainbow color schemes
- Multiple icon libraries
- Emoji instead of icons
- Custom fonts (use system fonts)
- Heavy shadows or 3D effects
- Busy patterns or textures
- Overly bright or neon colors

### ❌ Don't Do
- Mix different design styles
- Use inconsistent spacing
- Override component defaults without reason
- Add unnecessary decorations
- Use too many colors in one view
- Create visual clutter

---

## ✅ Do's - Best Practices

### ✅ Do Use
- Lucide icons exclusively
- Solid, subtle colors from the palette
- Consistent spacing and sizing
- White space effectively
- Clear visual hierarchy
- Meaningful micro-interactions

### ✅ Do
- Follow component patterns
- Keep layouts clean and minimal
- Test on different screen sizes
- Maintain consistency
- Think about accessibility
- Focus on usability first

---

## 📝 Code Examples

### Good Example - Button with Icon
```svelte
<script>
  import { Plus } from 'lucide-svelte';
</script>

<button class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 flex items-center space-x-2">
  <Plus size={18} />
  <span>Add Entry</span>
</button>
```

### Bad Example - Using Emoji
```svelte
<!-- ❌ DON'T DO THIS -->
<button class="px-4 py-2 bg-gradient-to-r from-primary-600 to-secondary-600 text-white rounded-lg">
  <span>➕</span>
  <span>Add Entry</span>
</button>
```

### Good Example - Navigation Item
```svelte
<script>
  import { LayoutDashboard } from 'lucide-svelte';
</script>

<a href="#/dashboard" class="flex items-center space-x-2 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-50">
  <LayoutDashboard size={18} />
  <span>Dashboard</span>
</a>
```

---

## 🔄 Review & Updates

This document should be reviewed and updated when:
- New components are added to the design system
- Design decisions change
- User feedback requires adjustments
- New patterns emerge

---

## 📞 Questions?

If you're unsure about a design decision:
1. Check this document first
2. Look at existing components for patterns
3. Prioritize simplicity and consistency
4. When in doubt, ask the team

---

**Remember:** Feelink is about clarity, focus, and helping users track their well-being. The design should support this mission by staying out of the way and letting the content shine.
