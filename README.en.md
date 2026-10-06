# init-design-reference

English | [한국어](README.md)

A next-generation design reference and engineering framework that stops AI UI style drift through **Closed-Loop Vision Verification** and **Deterministic Anti-Slop Engineering** for AI coding agents (Google Antigravity, Claude Code, Cursor, etc.).

---

## 1. Motivation & Core Mechanism

### Why AI-Generated UIs Always Look the Same (Attention Drift & Prior Regression)
When tasked with frontend code, LLMs routinely converge toward generic purple/indigo gradients, rounded SaaS card soup, and habit-driven `tracking-widest uppercase` labels. As conversations grow, prompt instructions suffer attention drift, regressing to the statistical median of training data.

`init-design-reference` eliminates this at the foundational level across **4 Engineering Pillars**:
1. **Tokens & 3-Dial Taste Knobs (`DESIGN.md`, `tokens/*.json`)**: Adopts `leonxlnx/taste-skill` numeric dials (`DESIGN_VARIANCE`, `VISUAL_DENSITY`, `MOTION_INTENSITY`, scaled 1–10).
2. **Proven Component Recipes (`patterns/*.md`)**: Production React/TSX + Tailwind blocks for dense data tables, shells, forms, and spring physics.
3. **Deterministic Linter (`scripts/lint_ui.py`)**: Complete port of `pbakaus/impeccable` rules, mechanically blocking AI clichés, hardcoded hex, and layout thrashing offline.
4. **Closed-Loop Vision Feedback (`scripts/capture_ui.py`)**: Uses Playwright to capture desktop/mobile viewports and collect console errors for vision-model self-correction.

---

## 2. Directory Layout

```
reference/
  screenshots/          # UI target captures & audit runs (.gitignore applied)
    audit/              # Output from scripts/capture_ui.py
  notes/
    do-not-copy.md      # Strict AI cliché bans (no generic gradients, cards, or labels)
    layout.md           # Breakpoints & spacing rhythm
    interaction.md      # Transition timing & modal focus rules
    visual-direction.md # Surface hierarchy & signature elements
    accessibility.md    # WCAG 2.1 AA & contrast mandates
  tokens/
    colors.json         # Hex values for surface, text, accents
    spacing.json        # Rem-based vertical & horizontal rhythm
    typography.json     # Role-based typography & bilingual fallbacks
    radii.json          # Border radius tokens
    shadows.json        # Depth tokens
    motion.json         # Durations, easing, and Emil Kowalski spring physics
  patterns/             # Production React/TSX + Tailwind component blocks
    layout-shells.md    # High-density cockpit & asymmetric hero layouts
    data-display.md     # Full-state data tables & anti-cliché telemetry cards
    forms-inputs.md     # Accessible validated inputs & filter toolbars
    micro-interactions.md # Tactile scale(0.98) press, sheet physics, acceleration
  fonts/
    README.md           # Local font handling guidelines
    font-license.md     # Licensing documentation
    preview.html        # Bilingual font stack rendering test
  DESIGN.md             # Core design principles & 3-Dial Taste Configuration
  COMPONENTS.md         # Component 4-state completeness rules
  REVIEW_CHECKLIST.md   # Pre-commit UI verification checklist
```

---

## 3. Installation & Presets

### Global Agent Installation
```powershell
# Windows (PowerShell)
irm https://raw.githubusercontent.com/mmmphyun/init-design-reference/main/install.ps1 | iex

# macOS / Linux (Bash)
curl -fsSL https://raw.githubusercontent.com/mmmphyun/init-design-reference/main/install.sh | bash
```

### Domain Presets (`--preset`)
```powershell
# Default Modern SaaS (Variance: 5, Density: 7, Motion: 4)
python "scripts/adapter.py" "reference"

# B2B High-Density Telemetry (Variance: 3, Density: 9, Motion: 2)
python "scripts/adapter.py" "reference" --preset b2b-dense

# Asymmetric Editorial Showcase (Variance: 8, Density: 3, Motion: 5)
python "scripts/adapter.py" "reference" --preset editorial-minimal

# Technical Developer Tool (Variance: 4, Density: 8, Motion: 1)
python "scripts/adapter.py" "reference" --preset technical-mono

# Fluid Tactile Spring Motion (Variance: 6, Density: 5, Motion: 9)
python "scripts/adapter.py" "reference" --preset apple-fluid
```

---

## 4. The 4-Phase Implementation Lifecycle

All frontend work must execute through 4 deterministic gates:

1. **Gate 1: `/craft` (Semantic Skeleton)**: Semantic DOM hierarchy without aesthetic color styling. ARIA roles and responsive layout slots only.
2. **Gate 2: `/bind` (Tokens & Patterns Binding)**: Map only semantic classes from `tokens/*.json` and `patterns/*.md`. Zero hardcoded hex codes.
3. **Gate 3: `/critique` (Deterministic Audit)**:
   ```powershell
   python scripts/lint_ui.py src/
   ```
   Requires 0 errors before proceeding.
4. **Gate 4: `/harden` (State Coverage & Vision Verification)**:
   - Full 4-state coverage (Loading Skeleton, Empty State, Error Alert, Populated).
   - Playwright headless audit:
     ```powershell
     python scripts/capture_ui.py --url http://localhost:3000
     ```
   - Vision inspection of captured screens in `reference/screenshots/audit/`.

---

## 5. Companion Bridges & Ecosystem

- **UI Linter (`scripts/lint_ui.py`)**: Offline anti-pattern detector ported from `pbakaus/impeccable`.
- **Headless Capture (`scripts/capture_ui.py`)**: Playwright screenshot & console error auditor.
- **Figma Sync Bridge (`scripts/sync_figma.py`)**: Synchronizes Figma Variables into `reference/tokens/*.json`.

### Recommended Companion Skills
- **Advanced Motion Auditing**: [`emilkowalski/skills`](https://github.com/emilkowalski/skills)
- **Live Figma Node Context**: [`figma-mcp-server`](https://github.com/GLips/Figma-Context-MCP)

---

## License & Credits

- Distributed under the [MIT License](LICENSE).
- Rules, motion parameters, and dial architecture draw from pioneering open-source work by:
  - **Emil Kowalski** ([emilkowalski/skills](https://github.com/emilkowalski/skills), MIT) - Micro-motion & spring physics
  - **Paul Bakaus** ([pbakaus/impeccable](https://github.com/pbakaus/impeccable), Apache 2.0) - Deterministic anti-pattern rules & lifecycle
  - **Leon Linz** ([leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill), MIT) - 3-Dial Taste framework
