---
name: init-design-reference
description: Scaffolds a production-grade UI design reference, pattern architecture (/reference), and deterministic closed-loop verification pipeline to prevent AI visual drift.
---

# Anti-Slop & Closed-Loop UI Framework

Scaffolds a `/reference` directory structure within the project root to enforce deterministic design constraints, anti-cliché standards, pattern recipes, and closed-loop visual verification.

## 1. Directory Structure

```
reference/
  screenshots/          # UI target captures & audit runs (.gitignore applied)
    audit/              # Output from scripts/capture_ui.py
  notes/
    do-not-copy.md      # Strict AI cliché bans (no generic gradients, cards, or labels)
    layout.md           # Breakpoints & spacing rhythm
    interaction.md      # Transition timing & modal focus rules
    visual-direction.md # Gate 0 brief intake & curated aesthetic palettes
    accessibility.md    # WCAG 2.1 AA & contrast mandates
  tokens/
    colors.json         # Hex values for surface, text, accents
    spacing.json        # Rem-based vertical & horizontal rhythm
    typography.json     # Role-based typography & bilingual fallbacks
    radii.json          # Border radius tokens
    shadows.json        # Depth tokens
    motion.json         # Durations, easing, and spring physics
  patterns/             # Production-grade React/TSX + Tailwind component blocks
    layout-shells.md    # High-density cockpit & asymmetric hero layouts
    data-display.md     # Full-state data tables & anti-cliché telemetry cards
    forms-inputs.md     # Accessible validated inputs & filter toolbars
    micro-interactions.md # Tactile press, sheet physics, hardware acceleration
  fonts/
    README.md           # Local font handling guidelines
    font-license.md     # Licensing documentation
    preview.html        # Bilingual font stack rendering test
  DESIGN.md             # Core design principles & 3-Dial Taste Configuration
  COMPONENTS.md         # Component 4-state completeness rules
  REVIEW_CHECKLIST.md   # Pre-commit UI verification & Feedback Translation Dictionary
```

## 2. Initialization & Preset Scaffolding

Run the framework adapter with an optional domain preset:

```powershell
# Windows
python "$env:USERPROFILE/.gemini/config/skills/init-design-reference/scripts/adapter.py" "reference" --preset b2b-dense

# macOS / Linux
python "$HOME/.gemini/config/skills/init-design-reference/scripts/adapter.py" "reference" --preset b2b-dense
```

### Available Presets (`--preset`)
- `default`: Balanced modern SaaS baseline (Variance 5, Density 7, Motion 4)
- `b2b-dense`: High-density data cockpit & telemetry (Variance 3, Density 9, Motion 2)
- `editorial-minimal`: Airy asymmetric showcase & landing (Variance 8, Density 3, Motion 5)
- `technical-mono`: Terminal/developer tool aesthetic (Variance 4, Density 8, Motion 1)
- `apple-fluid`: Tactile spring physics & fluid gestures (Variance 6, Density 5, Motion 9)

Use `--force` or `-f` to overwrite existing templates.

---

## 3. The 5-Gate Implementation Lifecycle

To eliminate context gaps and prevent regression into default AI aesthetics, all frontend generation MUST execute through 5 deterministic gates:

### Gate 0: Brief Intake & Token Synthesis (Derived from `frontend-design`)
Before coding, if no design specification exists, the agent MUST confirm 3 anchor points with the user:
1. **Concrete Subject & Audience**: (e.g., senior clinical researcher vs retail mobile buyer).
2. **Primary Job of the Screen**: (e.g., high-throughput scanning vs single-action checkout).
3. **Single Signature Anchor**: (Spend boldness in ONE place; keep everything else quiet).
*Output*: Populate `reference/DESIGN.md` dials and choose a curated palette from `reference/notes/visual-direction.md` into `reference/tokens/colors.json`.

### Gate 1: `/craft` (Semantic Skeleton)
- Construct semantic DOM hierarchy (`<header>`, `<main>`, `<aside>`, `<table>`) without aesthetic styling.
- Zero decorative colors. Focus exclusively on information architecture, responsive grid slots, and Radix/ARIA accessibility roles.

### Gate 2: `/bind` (Token & Pattern Binding)
- Consult `reference/DESIGN.md` for target Taste dials (`DESIGN_VARIANCE`, `VISUAL_DENSITY`, `MOTION_INTENSITY`).
- Bind styles exclusively using `reference/tokens/*.json` variables and `reference/patterns/*.md` recipes.
- **Strict Rule**: Zero hardcoded hex colors (`#6366f1`), arbitrary padding (`p-[18px]`), or generic Tailwind color palettes (`bg-slate-900`). Use semantic tokens only (`bg-surface`, `text-foreground`).

### Gate 3: `/critique` (Deterministic Lint Audit)
- Execute the offline, deterministic AST/Regex linter:
  ```powershell
  python scripts/lint_ui.py src/
  ```
- Must resolve all reported `[ERROR]` findings (AI gradients, uppercase tracking, layout thrashing) before proceeding.

### Gate 4: `/harden` (States, Vision Verification & Feedback Iteration)
1. **Mandatory 4-State Coverage**: Verify Loading Skeleton, Empty State, Error Message, and Populated View are explicitly implemented.
2. **Motion Guardrails**: Animate ONLY `transform` and `opacity`. Apply `scale-[0.98]` tactile press physics.
3. **Closed-Loop Vision Verification**:
   - Start the local development server (e.g., `npm run dev`).
   - If Playwright is not installed, prompt to install it (`pip install playwright && npx playwright install chromium`).
   - Run the headless auditor to capture viewports:
     ```powershell
     python scripts/capture_ui.py --url http://localhost:3000
     ```
   - Inspect captured screens in `reference/screenshots/audit/` using agent vision tools.
4. **Natural Language Feedback Iteration**:
   - When the user gives vague aesthetic feedback ("너무 휑해", "장난감 같아"), consult the **Feedback Translation Dictionary** in `reference/REVIEW_CHECKLIST.md` to deterministically adjust tokens and dials.

---

## 4. Companion Bridges & Tools

- `scripts/lint_ui.py`: Fast offline anti-pattern detector (ported from `pbakaus/impeccable`).
- `scripts/capture_ui.py`: Playwright headless screenshot & console error auditor.
- `scripts/sync_figma.py`: Synchronizes remote Figma Variables directly into `reference/tokens/*.json`.
