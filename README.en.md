# init-design-reference

English | [한국어](README.md)

A next-generation design engineering framework that stops AI UI style drift through **Deterministic Anti-Slop Linting** and **Closed-Loop Vision Verification** for AI coding agents (Google Antigravity, Claude Code, Cursor, etc.).

---

## 1. Real-World Engineering Proof

### ① Zero-Touch Token Reverse-Traceability (Next.js 15 App Router)
Demonstrated 0-diff component modification: Updating only `.design/tokens/colors.json` and regenerating CSS bridges modifies live production rendering without changing a single line of TSX code. Verified via headless Playwright capture.

| Baseline Rendering (`assets/baseline.png`) | Updated Token Rendering (`assets/updated.png`) |
|:---:|:---:|
| ![Baseline](assets/baseline.png) | ![Updated](assets/updated.png) |
| `--surface`: `#12151c` (Cockpit Carbon)<br>`--accent`: `#10b981` (Phosphor Emerald) | `--surface`: `#171717` (Terminal Panel)<br>`--accent`: `#f59e0b` (Amber Phosphor CRT) |

```console
$ git diff --stat app/components/MetricCard.tsx
# 0 files changed, 0 insertions(+), 0 deletions(-) -> Perfect 0-diff achieved
```

---

### ② Deterministic Static Linter & Self-Healing Loop
Lightweight regex-based static linter (`scripts/lint_ui.py`) detects accessibility flaws and hardcoded tokens, converging to `0 errors` via agent self-healing.

```console
$ python scripts/lint_ui.py app/components/MetricCard.tsx

--- UI Lint Findings ---
[ERROR] app/components/MetricCard.tsx:71 (a11y-naked-outline-none)
       outline-none detected on element without focus-visible:ring replacement (WCAG 2.4.7).
[ERROR] app/components/MetricCard.tsx:102 (hardcoded-hex)
       Hardcoded hex color detected (#1e293b). Use semantic tokens from colors.json.
[WARN]  app/components/MetricCard.tsx:102 (layout-thrashing-animation)
       Layout thrashing animation detected (transition-all). Animate ONLY transform and opacity.
[ERROR] app/components/MetricCard.tsx:105 (a11y-missing-alt)
       <img> tag missing alt attribute (WCAG 1.1.1).
[WARN]  app/components/MetricCard.tsx:107 (cliche-tracking-uppercase)
       Generic AI 'uppercase tracking-widest' eyebrow label detected.

Scan complete: 1 files inspected. Findings: 3 errors, 2 warnings.
Lint FAILED. Rectify errors or align with reference/ tokens and patterns.

# -> After 1 autonomous self-healing loop by the agent:
$ python scripts/lint_ui.py app/components/MetricCard.tsx
Scan complete: 1 files inspected. Findings: 0 errors, 2 warnings.
Lint PASSED.
```

---

### ③ Design Specification Static Hard-Guard (`--verify-spec`)
Statically verifies that Taste dials (1-10 bounds) and core required color tokens (`background.surface`, `background.primary`, `accent.primary`, `border.default`) exist with valid hex formats, preventing defect propagation before frontend code generation.


```console
$ python scripts/adapter.py --verify-spec
[HARD-GUARD FAIL] .design\DESIGN.md is missing one of DESIGN_VARIANCE, VISUAL_DENSITY, MOTION_INTENSITY.
# -> Returns non-zero exit code on spec mismatch so the caller can normalize configuration
```

---

## 2. Motivation & Core Mechanism

### Why AI-Generated UIs Always Look the Same (Attention Drift & Prior Regression)
When tasked with frontend code, LLMs routinely converge toward generic purple/indigo gradients, rounded SaaS card soup, and habit-driven `tracking-widest uppercase` labels. As conversations grow, prompt instructions suffer attention drift, regressing to the statistical median (Slop) of training data.

`init-design-reference` eliminates this across **4 Engineering Pillars**:
1. **Tokens & 3-Dial Taste Knobs (`DESIGN.md`, `.design/tokens/*.json`)**: Adopts `leonxlnx/taste-skill` numeric dials (`DESIGN_VARIANCE`, `VISUAL_DENSITY`, `MOTION_INTENSITY`, scaled 1–10).
2. **Proven Component Recipes (`.design/patterns/*.md`)**: Production React/TSX + Tailwind blocks for dense data tables, shells, forms, and spring physics.
3. **Deterministic Linter (`scripts/lint_ui.py`)**: Regex-based static analysis inspired by `pbakaus/impeccable` patterns, mechanically blocking key accessibility defects (WCAG) and hardcoded tokens with `[ERROR]`, while flagging generic AI clichés and layout-thrashing risks as non-blocking `[WARN]`.
4. **Closed-Loop Vision Feedback (`scripts/capture_ui.py`)**: Uses Playwright to capture desktop/mobile viewports and collect console errors for vision-model self-correction.

---

### Framework Support & Architecture Neutrality
- **Tier 1 Supported Stacks**: React / Next.js, Vue / Nuxt, Svelte / SvelteKit, Vanilla CSS.
- **Build Tool Separation**: Vite is categorized as a bundler/build tool rather than a framework; actual framework conventions govern code generation.
- **Core Principles vs Pattern Examples**:
  - **Universal Core Support**: Semantic DOM, ARIA accessibility, design token SSOT, 4-state lifecycle, and motion physics remain strictly framework-neutral across all stacks.
  - **Code Pattern Scope**: Full production recipes are provided in React/TSX as baseline. Vue 3 and Svelte 5 implementations are provided for core interactive and input patterns (`micro-interactions.md`, `forms-inputs.md`). For other patterns, agents follow the headless composition idioms in `COMPONENTS.md` using the target framework's primitives.
- **Bridge Support Scope**:
  - Automatically generated: Tailwind v4 (`theme.css` via `@theme`), Tailwind v3 (`tailwind.preset.js` via `presets` & `tokens.css`), Vanilla CSS (`tokens.css` via `:root`).
  - Unsupported runtime engines (CSS-in-JS like styled-components, Emotion, Panda CSS): Reference `:root` CSS variables in `tokens.css`.

---

## 3. Directory Layout (.design Goldilocks Architecture)

```
.design/                # Project runtime design repository (supports legacy reference/ fallback)
  screenshots/          # UI target captures & audit runs (.gitignore applied)
    audit/              # Output from scripts/capture_ui.py
  tokens/               # Full design tokens preserved for project runtime
    colors.json         # Hex values for surface, text, accents
    spacing.json        # Rem-based vertical & horizontal rhythm
    typography.json     # Role-based typography & official CDN font imports
    radii.json          # Border radius tokens
    shadows.json        # Depth models (Meng To ambient occlusion)
    motion.json         # Durations, Apple spring physics & gesture constraints (Emil Kowalski)
    theme.css           # Runtime CSS bridge (Tailwind v4 / Vanilla CSS)
    tailwind.preset.js  # Runtime preset bridge (Tailwind v3)
  patterns/             # Production component recipes (React/TSX, Vue 3, Svelte 5)
    layout-shells.md    # High-density cockpit & asymmetric hero layouts
    data-display.md     # 4-state data tables & anti-cliché telemetry cards
    forms-inputs.md     # Accessible validated inputs & filter toolbars
    micro-interactions.md # Tactile press, spring curves, hardware acceleration
  DESIGN.md             # Single design constitution & 3-Dial Taste Configuration
```

> **Zero Repo Pollution**: Static guidelines (`notes/*.md`, `REVIEW_CHECKLIST.md`) remain isolated in the global skill and are referenced Just-In-Time (JIT) during component interaction and motion binding (`notes/interaction.md`) without cluttering the project codebase.

---

## 4. Installation & Preset Scaffolding

### Global Skill Installation
```powershell
# Windows (PowerShell)
irm https://raw.githubusercontent.com/mmmphyun/init-design-reference/main/install.ps1 | iex

# macOS / Linux (Bash)
curl -fsSL https://raw.githubusercontent.com/mmmphyun/init-design-reference/main/install.sh | bash
```

### Domain Preset Scaffolding (`--preset`)
```powershell
# Balanced modern SaaS baseline (Variance: 5, Density: 7, Motion: 4)
python "scripts/adapter.py"

# High-density B2B data cockpit & telemetry (Variance: 3, Density: 9, Motion: 2)
python "scripts/adapter.py" --preset b2b-dense

# Workspace Monorepo Target (--app)
python "scripts/adapter.py" --preset b2b-dense --app apps/web

# Explicit CSS Entrypoint Override (--css)
python "scripts/adapter.py" --css src/styles/main.css

# Airy asymmetric showcase & landing (Variance: 8, Density: 3, Motion: 5)
python "scripts/adapter.py" --preset editorial-minimal

# Terminal/developer tool aesthetic (Variance: 4, Density: 8, Motion: 1)
python "scripts/adapter.py" --preset technical-mono

# Tactile spring physics & fluid gestures (Variance: 6, Density: 5, Motion: 9)
python "scripts/adapter.py" --preset apple-fluid
```

---

## 5. Autonomous 5-Gate Self-Driving Loop

Agents strictly adhere to the 5-Gate Golden Boundary:

1. **Gate 0: Smart Alignment (High-Touch Dialog & Hard-Guard)**:
   - Identify existing project identity & track the 7-Decision Matrix (confirmed / existing project / undefined / assumption).
   - Detect workspace monorepos and clarify ambiguous CSS entrypoints.
   - Adaptive Deep Probe dynamically synthesizes 3 Taste dials (1~10) and brand tokens.
   - **User Approval Gate (Strict Lock)**: Execution of `adapter.py` and file generation is strictly blocked until explicit user confirmation.
   - Run `python scripts/adapter.py --verify-spec` to enforce specification validity (dials 1~10 and required tokens).
2. **Phase 1: Semantic Skeleton (Craft)**: Structural hierarchy and pure ARIA roles without decorative styling (React, Vue, Svelte, HTML common).
3. **Phase 2: Token & Surface Binding (Bind)**: Bind exclusively to `.design/tokens/*.json` semantic classes and CSS variables (zero hardcoded hex).
4. **Phase 3: Deterministic Lint & Self-Healing (Critique)**:
   ```powershell
   python scripts/lint_ui.py src/
   ```
   Autonomously patches objective `[ERROR]` violations (a11y and missing tokens) within 3 retries until 0 errors are achieved.
5. **Phase 4: Completeness & Vision Verification (Harden)**:
   - Implement Loading (skeleton), Empty, Error, and Populated states for asynchronous data views.
   - Execute Playwright headless audit:
     ```powershell
     python scripts/capture_ui.py
     ```
   - On styling feedback (colors, spacing, fonts), update tokens in `tokens/*.json`. On layout/structural feedback, modify framework component code (TSX / Vue / Svelte / HTML).

---

## License & Credits

- Licensed under the [MIT License](LICENSE).
- Rooted in the pioneering research of open-source visionaries:
  - **Emil Kowalski** ([emilkowalski/skills](https://github.com/emilkowalski/skills), MIT) - Micro-interactions & spring physics
  - **Paul Bakaus** ([pbakaus/impeccable](https://github.com/pbakaus/impeccable), Apache 2.0) - Deterministic anti-pattern rules & lifecycle
  - **Leon Linz** ([leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill), MIT) - 3-Dial Taste framework
  - **Addy Osmani** - Accessibility & semantic web contracts

See [NOTICE.md](NOTICE.md) for full license texts and attributions.
