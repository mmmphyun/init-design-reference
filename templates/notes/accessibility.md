# Accessibility Guidelines (WCAG 2.1 AA)

## 1. Contrast Ratios
- **Normal Text**: Minimum 4.5:1 contrast against background.
- **Large Text (>= 18pt or 14pt bold)**: Minimum 3.0:1 contrast.
- **UI Components & Graphical Objects**: Minimum 3.0:1 against adjacent colors.

## 2. Keyboard & Assistive Technology
- **Visible Focus**: Clear, unhidden `:focus-visible` indicator on all actionable elements.
- **Screen Reader Context**: Ensure icon-only buttons (`<button>`, `<a>`) include `aria-label` or `<span class="sr-only">`.
- **Form Controls**: Every input must have an explicitly associated `<label>` element.
