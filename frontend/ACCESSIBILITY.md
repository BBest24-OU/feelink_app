# Accessibility Guidelines - FeelInk

## Overview

FeelInk is committed to providing an inclusive experience for all users, including those with disabilities. This document outlines our accessibility standards and implementation details.

## WCAG 2.1 Level AA Compliance

We aim to meet [WCAG 2.1 Level AA](https://www.w3.org/WAI/WCAG21/quickref/) standards. Key areas of focus:

### 1. Perceivable

#### Text Alternatives
- **Images**: All images include appropriate `alt` attributes
- **Loading Spinners**: Marked with `aria-hidden="true"` with screen-reader-only text
- **Icons**: Decorative icons use `aria-hidden="true"`, functional icons have labels

#### Color Contrast
- **Text**: Minimum 4.5:1 contrast ratio for normal text
- **Large Text**: Minimum 3:1 contrast ratio for text 18pt+ or 14pt+ bold
- **Interactive Elements**: Minimum 3:1 contrast for UI components

#### Visual Presentation
- Text can be resized up to 200% without loss of functionality
- Line height minimum 1.5 for paragraphs
- No content relying solely on color to convey meaning

### 2. Operable

#### Keyboard Navigation
All interactive elements are keyboard accessible:

**Focus Management**:
- Visible focus indicators on all interactive elements
- Focus ring: `focus:ring-2 focus:ring-primary-500 focus:ring-offset-2`
- Skip links for navigation (to be implemented)

**Keyboard Shortcuts**:
- `Tab`: Move to next interactive element
- `Shift + Tab`: Move to previous interactive element
- `Enter`: Activate buttons and links
- `Space`: Activate buttons and checkboxes
- `Escape`: Close modals and dropdowns

**Component-Specific Navigation**:
- **Forms**: Tab through inputs in logical order
- **Buttons**: Activatable with Enter and Space
- **Interactive Cards**: Tab-focusable when clickable, activatable with Enter/Space
- **Dropdowns**: Arrow keys for navigation (to be implemented)
- **Modals**: Focus trapped within modal, Escape to close

#### Time Limits
- No time limits on user interactions
- Session timeouts provide warnings and extension options

#### Motion and Animation
- Respects `prefers-reduced-motion` for users with vestibular disorders
- Critical animations can be disabled via settings

### 3. Understandable

#### Language
- Page language declared: `<html lang="en">` or `<html lang="pl">`
- Language changes marked with `lang` attribute
- Simple, clear language used throughout

#### Forms
- **Labels**: All inputs have associated `<label>` elements
- **Required Fields**: Marked with `required` attribute and visual indicator
- **Error Messages**:
  - Displayed with `role="alert"` and `aria-live="assertive"`
  - Clear, actionable error messages
  - Associated with relevant form fields
- **Help Text**: Provided for complex inputs

#### Navigation
- Consistent navigation across all pages
- Clear page titles describing content
- Breadcrumbs for hierarchical navigation

### 4. Robust

#### Semantic HTML
- Proper heading hierarchy (`<h1>` → `<h2>` → `<h3>`)
- Semantic elements: `<main>`, `<nav>`, `<article>`, `<section>`, `<aside>`
- Lists use `<ul>`, `<ol>`, `<li>` appropriately
- Tables use proper markup: `<table>`, `<thead>`, `<tbody>`, `<th>`, `<td>`

#### ARIA
Used judiciously to enhance semantics:
- `role="status"`: Loading indicators
- `role="alert"`: Error messages, critical notifications
- `role="button"`: Interactive divs (prefer actual `<button>` when possible)
- `aria-label`: Accessible names for interactive elements
- `aria-live`: Dynamic content updates
- `aria-busy`: Loading states
- `aria-hidden`: Decorative elements

## Component Accessibility

### Loading Component
```svelte
<div role="status" aria-live="polite" aria-busy="true">
  <div aria-hidden="true"><!-- Spinner --></div>
  <span class="sr-only">Loading...</span>
</div>
```

### Button Component
- Native `<button>` element
- Disabled state: `disabled` attribute + visual indication
- Focus visible: `focus:ring-2`
- `type` attribute always specified

### Card Component (Interactive)
- `role="button"` when clickable
- `tabindex="0"` for keyboard navigation
- Keyboard event handlers for Enter and Space
- Focus indicator visible
- Optional `aria-label` for context

### Form Inputs
- Associated `<label>` for every input
- `required` attribute for required fields
- Error states communicated visually and programmatically
- Help text linked with `aria-describedby`

### Error Messages
```svelte
<div role="alert" aria-live="assertive">
  {errorMessage}
</div>
```

### Modals (Future Implementation)
- Focus trap within modal
- Escape key to close
- Focus returns to trigger element on close
- `role="dialog"` or `role="alertdialog"`
- `aria-modal="true"`
- `aria-labelledby` pointing to title
- Background content inert (`aria-hidden="true"`)

## Screen Reader Support

### Tested With
- **NVDA** (Windows) - Primary
- **JAWS** (Windows) - Secondary
- **VoiceOver** (macOS/iOS) - Secondary
- **TalkBack** (Android) - Secondary

### Screen-Reader-Only Content
Use `.sr-only` class for content visible only to screen readers:

```css
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
```

## Testing Checklist

### Manual Testing
- [ ] All pages navigable with keyboard only
- [ ] Focus indicators visible on all interactive elements
- [ ] All images have appropriate alt text
- [ ] Form labels associated with inputs
- [ ] Error messages announced by screen readers
- [ ] Heading hierarchy logical and sequential
- [ ] Color contrast meets WCAG AA standards
- [ ] Text resizable to 200% without overflow
- [ ] No content flashing more than 3 times per second

### Automated Testing
Tools to use:
- **axe DevTools**: Browser extension for automated testing
- **Lighthouse**: Accessibility audit in Chrome DevTools
- **WAVE**: Web accessibility evaluation tool
- **Pa11y**: Automated accessibility testing (CI/CD)

### Screen Reader Testing
- [ ] Login flow
- [ ] Registration flow
- [ ] Daily log entry
- [ ] Metrics management
- [ ] Dashboard navigation
- [ ] Analytics/correlations viewing

## Known Issues and Future Improvements

### Current Limitations
1. **Skip Links**: Not yet implemented
2. **Focus Management**: Need focus trap for future modal components
3. **Keyboard Shortcuts**: Custom shortcuts not yet implemented
4. **High Contrast Mode**: Not fully optimized

### Planned Improvements
1. Add skip navigation links
2. Implement comprehensive keyboard shortcut system
3. Add preference for reduced motion
4. Improve high contrast mode support
5. Add ARIA live regions for dynamic content updates
6. Implement focus management for SPA routing
7. Add accessibility settings page

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [A11y Project Checklist](https://www.a11yproject.com/checklist/)

## Contact

For accessibility concerns or suggestions, please open an issue on the GitHub repository.
