# UI Review & Verification Checklist
<!-- Derived from Superfuture/design-review (MIT License) & addyosmani/web-quality-skills (MIT License) -->

Complete this checklist prior to submitting or committing UI code changes.

---

## 1. Pre-Commit Verification Checklist

- [ ] **Token Adherence**: Colors, spacing, and typography conform strictly to `.design/tokens/` (or `reference/tokens/`).
- [ ] **Anti-Cliché Audit**: Verified absence of prohibited patterns in `.design/notes/do-not-copy.md`.
- [ ] **Deterministic Lint**: `python scripts/lint_ui.py <src>` returns 0 errors.
- [ ] **Responsive Breakpoints**: Verified visual integrity at `375px` (mobile) and `1440px` (desktop).
- [ ] **Multilingual Typography**: Korean and English mixed strings render without baseline distortion or font clipping.
- [ ] **Accessibility (WCAG 2.1 AA)**:
  - [ ] Contrast ratio >= 4.5:1 for normal body text.
  - [ ] Visible focus rings on all interactive elements via `:focus-visible`.
  - [ ] Screen-reader accessible labels on icon-only buttons.
- [ ] **Hobson 4-State Completeness**: Verified `Loading`, `Empty`, `Error`, and `Populated` states on all dynamic components.
- [ ] **Performance & Motion**: Spatial transitions restricted to GPU-accelerated properties (`transform`, `opacity`); state transitions restricted to targeted paint properties (`color`, `background-color`, `border-color`, `box-shadow`); micro-interaction duration <= 350ms; strict `prefers-reduced-motion` compliance.
- [ ] **Critical Data Integrity & Functional Visibility (High-Density / Enterprise)**:
  - [ ] Zero truncation on critical domain identities (ID, Code, Key, Host/IP, Account fully visible).
  - [ ] Functional indicator/gauge bar height >= 6px (`h-1.5`) with high-contrast alert states.
  - [ ] Standard units enforced (e.g., `GiB`, `cores`, `ms`, `USD`, `Mbps`), no informal abbreviations.
  - [ ] Adaptive vertical budget: no dead space > 100px on fixed viewports; rows vertically balanced.
  - [ ] Critical state rows have elevated prominence (left border indicator or tint).
  - [ ] Production view isolated from development state-simulation controls.

---

## 2. Superfuture Heuristic Visual Critique Rubric

Evaluate headless Playwright captures against these 5 pillars during Gate 4 verification:

| Pillar | Inspection Criteria | Pass Standard | Failure Mode & Remediation |
| :--- | :--- | :--- | :--- |
| **1. Typographic Hierarchy** | Font size scale & line height rhythm | Maximum 3 distinct type sizes per component view; line-height >= 1.4 for body | Font size soup; consolidate to `text-xs`, `text-sm`, `text-xl` |
| **2. Spacing Rhythm** | Consistency of gap, padding, and margins | Strict adherence to `spacing.json` scale factors (multiples of 4px / 0.25rem) | Arbitrary spacing (`p-[13px]`, `gap-5` mixed with `gap-6`); normalize to token |
| **3. Surface & Noise** | Card nesting and border cage density | Surfaces differentiated by tonal step (`bg-surface` vs `bg-background`), not 4 nested border boxes | "Card inside card inside card"; strip inner borders, use tonal contrast |
| **4. Affordance & Contrast** | Primary vs Secondary action hierarchy | Clear visual prominence for primary CTA; secondary actions use quiet surfaces | Competing colored buttons; convert secondary buttons to `variant="secondary"` |
| **5. AI Cliché Residuals** | Unintentional generative AI artifacts | Zero purple gradients, no floating ambient blobs, no unnecessary trailing arrows (`->`) | AI default slop; replace with solid tokens and crisp architectural lines |
| **6. Critical Data & Indicator Integrity** | Preattentive alert prominence & Zero truncation | Indicator height >= 6px (`h-1.5`); zero `...` truncation on critical identifiers; standard units | Anemic 1-2px lines; truncated identifiers (`ORD-92...`); dead space > 100px |

---

## 3. Natural Language Feedback Translation Dictionary
*(Translates vague, emotional non-designer feedback into deterministic token and dial adjustments)*

| User Natural Language Feedback | Root Cause Diagnosis | Deterministic Action in `.design/` |
| :--- | :--- | :--- |
| **"너무 휑하고 빈약해 보여"** | Low information density, over-spaced padding | 1. Increase `VISUAL_DENSITY` by +2 in `DESIGN.md`<br>2. Reduce base padding in `spacing.json` by 0.25rem<br>3. Expose telemetry metadata/badges into empty slots |
| **"너무 장난감 같아 / 가벼워 보여"** | Bubble-like rounding, playful bouncing animation | 1. Reduce border radii in `radii.json` to `<= 4px`<br>2. Lower `MOTION_INTENSITY` by -2 in `DESIGN.md`<br>3. Remove gradient fills; convert to crisp 1px solid borders |
| **"글자가 눈에 안 들어와 / 가독성 불량"** | Poor contrast, excessive tracking, line height mismatch | 1. Enforce 7:1 contrast ratio between text and surface in `colors.json`<br>2. Lock body line-height to `1.5`<br>3. Strip any `uppercase tracking-widest` labels |
| **"지루하고 AI가 만든 것 같아"** | Statistical median layout, default centered SaaS hero | 1. Increase `DESIGN_VARIANCE` by +2 in `DESIGN.md`<br>2. Deploy an asymmetric grid from `patterns/layout-shells.md`<br>3. Introduce one bold signature visual element per `visual-direction.md` |
| **"너무 어지럽고 복잡해"** | Visual noise from over-nesting borders and dividers | 1. Remove 50% of card borders; use surface tonal shift instead<br>2. Consolidate font sizes into strictly 3 scale levels<br>3. Hide secondary actions behind a single overflow menu |
