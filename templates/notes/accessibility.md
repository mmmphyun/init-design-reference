# Accessibility Architecture Standards (WCAG 2.1 AA / AAA)
<!-- Derived from addyosmani/web-quality-skills (MIT License, Copyright (c) 2025 Addy Osmani) -->

Production standards enforcing keyboard navigation contracts, cognitive contrast guarantees, and assistive technology parity.

## 1. Contrast Ratios & Visual Perception
- **Normal Text (< 18pt or < 14pt bold)**: Mandatory minimum **4.5:1** contrast against adjacent surface.
- **Large Text (>= 18pt or >= 14pt bold)**: Mandatory minimum **3.0:1** contrast.
- **Essential UI Components & Active Borders**: Minimum **3.0:1** contrast against surface background.
- **Motion Reduction**: All animations, springs, and transitions MUST obey `@media (prefers-reduced-motion: reduce)`.
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, ::before, ::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
    }
  }
  ```

---

## 2. Keyboard Navigation Contracts
- **Focus Ring Contract**:
  - NEVER use `outline-none` without an explicit replacement `focus-visible:ring-2` with `focus-visible:ring-offset-2`.
  - Focus indicators must have at least 3.0:1 contrast against both the component and the canvas background.
- **Interactive Key Bindings**:
  - `Enter` / `Space`: Activate buttons and toggle checkboxes/switches.
  - `Escape`: Immediately close sheets, popovers, and modal dialogs; restore focus to the trigger element.
  - `Tab` / `Shift+Tab`: Forward/reverse sequential navigation without keyboard traps.
  - `Arrow Keys`: Navigate within composite widgets (tabs, radio groups, menu dropdowns).

---

## 3. Assistive Technology & ARIA Semantic Contracts
- **Landmark Regions**:
  - Every application shell must declare `<header>`, `<main>`, `<nav>`, and optional `<aside>`.
  - Exactly one `<main>` landmark per document view.
- **Dynamic State Announcements**:
  - Async data fetching containers must declare `aria-busy="true"` during load and `aria-busy="false"` on completion.
  - Search count results and filtering updates must utilize `<div aria-live="polite">`.
  - Error messages must declare `role="alert"` and be linked to inputs via `aria-describedby`.
- **Icon-Only Control Rule**:
  - Buttons or links containing only an SVG/Icon MUST provide an explicit `aria-label` or `<span className="sr-only">Description</span>`.

---

## 4. Modal & Sheet Focus Trapping Contract
- Modals must include `role="dialog"`, `aria-modal="true"`, and an associated `aria-label` or `aria-labelledby`.
- While open, body scrolling must be locked (`overflow: hidden`), and keyboard focus must be trapped within the modal container.
