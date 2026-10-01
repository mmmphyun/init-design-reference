# UI Review & Verification Checklist

Complete this checklist prior to submitting or committing UI code changes:

- [ ] **Token Adherence**: Colors, spacing, and typography conform strictly to `reference/tokens/`.
- [ ] **Anti-Cliché Audit**: Verified absence of prohibited patterns in `reference/notes/do-not-copy.md`.
- [ ] **Responsive Breakpoints**: Verified visual integrity at `375px`, `768px`, and `1280px`.
- [ ] **Multilingual Typography**: Korean and English mixed strings render without baseline distortion or fallback degradation.
- [ ] **Accessibility (WCAG 2.1 AA)**:
  - [ ] Contrast ratio >= 4.5:1 for normal body text.
  - [ ] Visible focus rings on all interactive elements via `:focus-visible`.
  - [ ] Screen-reader accessible labels on icon-only buttons.
- [ ] **State Handling**: Verified `loading`, `empty`, and `error` states on all data-driven components.
- [ ] **Performance & Bundle**: No raw font binaries or high-resolution screenshots committed to source trees.
