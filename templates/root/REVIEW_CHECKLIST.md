# UI Review & Verification Checklist

Complete this checklist prior to submitting or committing UI code changes.

---

## 1. Pre-Commit Verification Checklist

- [ ] **Token Adherence**: Colors, spacing, and typography conform strictly to `reference/tokens/`.
- [ ] **Anti-Cliché Audit**: Verified absence of prohibited patterns in `reference/notes/do-not-copy.md`.
- [ ] **Deterministic Lint**: `python scripts/lint_ui.py <src>` returns 0 errors.
- [ ] **Responsive Breakpoints**: Verified visual integrity at `375px` (mobile) and `1440px` (desktop).
- [ ] **Multilingual Typography**: Korean and English mixed strings render without baseline distortion or font clipping.
- [ ] **Accessibility (WCAG 2.1 AA)**:
  - [ ] Contrast ratio >= 4.5:1 for normal body text.
  - [ ] Visible focus rings on all interactive elements via `:focus-visible`.
  - [ ] Screen-reader accessible labels on icon-only buttons.
- [ ] **State Handling**: Verified `loading`, `empty`, and `error` states on all data-driven components.
- [ ] **Performance & Bundle**: No raw font binaries or high-resolution screenshots committed to source trees.

---

## 2. Natural Language Feedback Translation Dictionary
*(Translates vague, emotional non-designer feedback into deterministic token and dial adjustments)*

| User Natural Language Feedback | Root Cause Diagnosis | Deterministic Action in `/reference` |
| :--- | :--- | :--- |
| **"너무 휑하고 빈약해 보여"** | Low information density, over-spaced padding | 1. Increase `VISUAL_DENSITY` by +2 in `DESIGN.md`<br>2. Reduce base padding in `spacing.json` by 0.25rem<br>3. Expose telemetry metadata/badges into empty slots |
| **"너무 장난감 같아 / 가벼워 보여"** | Bubble-like rounding, playful bouncing animation | 1. Reduce border radii in `radii.json` to `<= 4px`<br>2. Lower `MOTION_INTENSITY` by -2 in `DESIGN.md`<br>3. Remove gradient fills; convert to crisp 1px solid borders |
| **"글자가 눈에 안 들어와 / 가독성 불량"** | Poor contrast, excessive tracking, line height mismatch | 1. Enforce 7:1 contrast ratio between text and surface in `colors.json`<br>2. Lock body line-height to `1.5`<br>3. Strip any `uppercase tracking-widest` labels |
| **"지루하고 AI가 만든 것 같아"** | Statistical median layout, default centered SaaS hero | 1. Increase `DESIGN_VARIANCE` by +2 in `DESIGN.md`<br>2. Deploy an asymmetric grid from `patterns/layout-shells.md`<br>3. Introduce one bold signature visual element per `visual-direction.md` |
| **"너무 어지럽고 복잡해"** | Visual noise from over-nesting borders and dividers | 1. Remove 50% of card borders; use surface tonal shift instead<br>2. Consolidate font sizes into strictly 3 scale levels<br>3. Hide secondary actions behind a single overflow menu |
