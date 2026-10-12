# Interaction & Motion Guidelines
<!-- Conceptual architecture inspired by general interface motion principles; implemented via native repository tokens. -->

This guide defines the interaction contracts and motion judgment standards for UI components.
It bridges high-level intent from Gate 0 with deterministic token execution in `.design/tokens/motion.json`.

---

## 1. Hierarchy of Motion Decision (User Intent First)

Interface motion must follow user intent and established project conventions before applying any recipe.

1. **Gate 0 Alignment**:
   - Strictly adhere to the confirmed `Interaction Vibe` and `MOTION_INTENSITY` dial (1-10) established in Gate 0.
   - If user requested subdued, calm, or instant interaction (`MOTION_INTENSITY <= 3`), do NOT introduce spring bounce, playful oscillation, or gratuitous spatial translation.
   - If critical motion direction is **[Undetermined]**, ask the user rather than inventing subjective aesthetic defaults.
   - Routine implementation details (e.g. choosing between 150ms and 200ms within the confirmed budget) are resolved autonomously.
2. **Preserve Existing Systems**:
   - If the project already defines animation tokens, CSS variables, Framer Motion/Tailwind configurations, or primitive components (Radix, Ark, Headless UI), preserve and reuse them.
   - Never inject redundant tokens, duplicate curves, or third-party motion libraries when existing primitives suffice.
3. **Recipes as Options, Not Defaults**:
   - The patterns below are contextual guidance. They are never mandatory styling defaults.
   - When a pattern is unnecessary, omit it completely.

---

## 2. Universal Motion Property Contract

To prevent layout thrashing and maintain 60/120fps rendering, all transitions must strictly adhere to the motion contract:

| Category | Allowed Properties | Transition Class / Usage | Prohibited |
| :--- | :--- | :--- | :--- |
| **Spatial Motion** | `transform`, `opacity`, `filter` | `transition-transform`, `transition-opacity` | Animate `top`, `left`, `bottom`, `right`, `width`, `height`, `margin`, `padding` |
| **State Feedback** | `color`, `background-color`, `border-color`, `box-shadow`, `outline-color` | `transition-colors`, `transition-shadow` | Catch-all `transition-all` |

### Timing & Duration Budget
- **Micro-Interactions**: Maximum duration is **350ms** (`maxMicroInteractionDuration`).
- **Tactile Press**: Immediate feedback within **100ms** (`duration.press`, `active:scale-[0.98]`).
- **Enter vs. Exit Asymmetry**: Exit transitions must be faster (~100-150ms) than enter transitions (~200-250ms) to maintain responsive perceived performance.

---

## 3. Core Interaction Patterns & Boundaries

The initial scope covers four common interaction scenarios. Each defines when it is useful, when to omit it, and how to govern its motion.

### 1. Anchored Overlays (Menus, Tooltips, Popovers)
- **When Useful**:
  - Contextual help (tooltips) or localized action lists (dropdown menus) anchored to a triggering button.
  - Directional enter transitions (fade + subtle 2-4px translation along the anchor axis) reinforce spatial origin.
- **When to Omit**:
  - Touch-first mobile viewports where anchored flyouts cause clipping; prefer bottom sheets or inline disclosures.
  - Critical primary actions that belong directly on the main surface.
- **Motion Principle**:
  - Enter: Fast fade with minimal scale or axis shift (`150ms`, decelerated).
  - Exit: Instant or rapid fade-out (`100ms`).
  - Spring profile: High stiffness, no bounce (`springs["tooltip-pop"]` or snappy).

### 2. Modal Dialogs & Sheets
- **When Useful**:
  - Focused workflows, confirmations, or complex detail inspection requiring user attention.
- **When to Omit**:
  - Lightweight notifications or non-blocking feedback; use inline banners or subtle status indicators instead.
- **Motion Principle**:
  - Backdrop: Fade-in opacity (`duration.fast` or `duration.normal`).
  - Surface: Modal scales slightly up from 95% or slides up from viewport edge; Sheet slides from screen edge along its axis.
  - Spring profile: Smooth damping without residual wobble (`springs["modal-sheet"]`).
  - Keyboard & Focus: Must trap focus while open, close on `Escape` or backdrop click, and restore focus to trigger.

### 3. Collapsible & Expandable Regions (Accordions, Disclosures)
- **When Useful**:
  - Progressive disclosure of secondary details, FAQ items, or high-density table sub-rows.
- **When to Omit**:
  - Primary navigation links, critical form fields, or short content where toggling adds unnecessary interaction friction.
- **Motion Principle**:
  - Content height: Prefer CSS grid row transition (`grid-template-rows: 0fr -> 1fr`) or discreet opacity cross-fade rather than animating geometric `height` directly.
  - Indicator: Rotate chevron via `transform: rotate(...)` (`duration.fast`).

### 4. Status Feedback (Errors, Success Validation)
- **When Useful**:
  - Form validation errors, asynchronous save confirmations, toast alerts.
- **When to Omit**:
  - Static persistent error messages present on initial page render.
- **Motion Principle**:
  - Enter: Crisp fade-in with micro-slide (2-3px) to draw attention without jarring displacement.
  - Shake/Bounce: Strictly reserved for high-salience validation blocks; NEVER use aggressive shaking if `MOTION_INTENSITY <= 4` or under reduced-motion.
  - Colors: Transition paint properties via `transition-colors` (`border-status-error`, `text-status-error`).

---

## 4. Accessibility & Reduced Motion (`prefers-reduced-motion`)

All interactive surfaces must respect user motion preferences without compromising functional parity.

```css
@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Reduced Motion Guarantees
1. **Functional State Preservation**: Menus, dialogs, disclosures, and validation banners must open, close, and change states immediately. Content visibility and logic are never tied to animation completion.
2. **Eliminate Spatial Translation**: Strip scale transformations, slides, bouncy overshoot, and continuous loops.
3. **Instant or Cross-Fade Feedback**: Replace directional spatial animations with instantaneous appearance or subtle opacity/color changes.
