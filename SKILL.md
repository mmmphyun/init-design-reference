---
name: init-design-reference
description: Scaffolds a production-grade UI design reference, pattern architecture (/reference), and deterministic closed-loop verification pipeline to prevent AI visual drift.
---

# Anti-Slop & Closed-Loop UI Framework

Scaffolds a `/reference` directory structure within the project root to enforce deterministic design constraints, anti-cliché standards, pattern recipes, and closed-loop visual verification.

Integrates proven design engineering standards from the open-source ecosystem (`shadcn/ui`, `emilkowalski/apple-design`, `MengTo/beautiful-shadows`, `addyosmani/accessibility`, `Superfuture/design-review`, `pbakaus/impeccable`, `jakubkrehel/skills`, `wshobson/interaction-design`). See `NOTICE.md` for license notices.

## 1. Directory Structure

```
reference/
  screenshots/          # UI target captures & audit runs (.gitignore applied)
    audit/              # Output from scripts/capture_ui.py
  notes/
    do-not-copy.md      # Strict AI cliché bans (no generic gradients, cards, or labels)
    layout.md           # Breakpoints & spacing rhythm
    interaction.md      # Transition timing & modal focus rules
    visual-direction.md # Gate 0 brief intake (Jakub Krehel) & curated aesthetic palettes
    accessibility.md    # WCAG 2.1 AA/AAA contrast & keyboard navigation mandates (Addy Osmani)
  tokens/
    colors.json         # Hex values for surface, text, accents
    spacing.json        # Rem-based vertical & horizontal rhythm
    typography.json     # Role-based typography & bilingual fallbacks
    radii.json          # Border radius tokens
    shadows.json        # Multi-layer ambient occlusion depth models (Meng To)
    motion.json         # Durations, Apple spring physics & gesture constraints (Emil Kowalski)
  patterns/             # Production-grade React/TSX + Tailwind component blocks
    layout-shells.md    # High-density cockpit & asymmetric hero layouts (shadcn unstyled slots)
    data-display.md     # 4-state data tables (Hobson) & anti-cliché telemetry cards
    forms-inputs.md     # Accessible validated inputs & filter toolbars (Addy Osmani)
    micro-interactions.md # Tactile press, spring sheets, hardware acceleration (Kowalski & Bakaus)
  fonts/
    README.md           # Local font handling guidelines
    font-license.md     # Licensing documentation
    preview.html        # Bilingual font stack rendering test
  DESIGN.md             # Core design principles & 3-Dial Taste Configuration
  COMPONENTS.md         # Component 4-state completeness rules & Radix composition (Hobson)
  REVIEW_CHECKLIST.md   # Superfuture 5-Pillar visual rubric & Feedback Translation Dictionary
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

## 3. The 5-Gate Implementation Lifecycle (Single-Agent JIT Paging)

To eliminate context pollution and prevent regression into default AI aesthetics, execute through 5 deterministic gates in the main conversation thread:

### Gate 0: Brief Intake & Token Synthesis (Jakub Krehel & frontend-design)
- Read `reference/notes/visual-direction.md`.
- Confirm 4 anchor points with the user:
  1. **Concrete Subject & Audience**: Dictates domain vernacular and materials.
  2. **Primary Job of the Screen**: High-throughput scanning vs single-action focus vs exploration.
  3. **Single Signature Anchor**: Spend boldness in ONE place; keep surrounding surfaces quiet.
  4. **Taste Dial Mapping**: Select target dials for `reference/DESIGN.md`.
- *Output*: Populate `reference/DESIGN.md` dials and copy target palette to `reference/tokens/colors.json`.

### Gate 1: `/craft` (Semantic Skeleton - shadcn/ui Unstyled Architecture)
- Read `reference/patterns/layout-shells.md`.
- Construct semantic DOM hierarchy (`<header>`, `<main>`, `<aside>`, `<table>`) without aesthetic styling.
- Zero decorative colors or background fills. Focus exclusively on information architecture, responsive grid slots, and Radix/ARIA accessibility roles.

### Gate 2: `/bind` (Token & Craft Binding - Meng To & Emil Kowalski)
- Consult `reference/DESIGN.md` dials and read `reference/tokens/*.json` + `reference/patterns/micro-interactions.md`.
- Bind styles exclusively using semantic CSS tokens (`bg-surface`, `text-foreground`, `shadow-elevation-1` to `shadow-elevation-4`).
- Apply `active:scale-[0.98]` tactile press physics and Apple spring curves (`ease-apple-snappy`, `ease-apple-spring`).
- **Surface Hierarchy**: 단일 컴포넌트 바인딩 시 기본 배경은 Level 1(`bg-surface`), 상위 캔버스는 Level 0(`bg-background`) 기본 컨벤션을 적용하여 중첩 대비를 보장한다.
- **Strict Rule**: Zero hardcoded hex colors (`#6366f1`), arbitrary padding (`p-[18px]`), or generic Tailwind color palettes (`bg-slate-900`).

### Gate 3: `/critique` (Deterministic Lint Audit - Paul Bakaus & Addy Osmani)
- Execute the offline, deterministic AST/Regex linter:
  ```powershell
  python scripts/lint_ui.py src/
  ```
- Must resolve all reported `[ERROR]` findings (AI gradients, uppercase tracking, layout thrashing, naked outline-none, missing alt tags) before proceeding.

### Gate 4: `/harden` (4-States, Vision Verification & Superfuture Critique)
1. **Mandatory 4-State Coverage (William Hobson)**: Verify `Loading` (skeleton with `aria-busy`), `Empty` (actionable CTA), `Error` (`role="alert"` with retry), and `Populated` are explicitly implemented.
2. **Motion Guardrails**: Animate ONLY `transform` and `opacity`. Cap micro-interactions to <= 350ms. Obey `prefers-reduced-motion`.
3. **Closed-Loop Vision Verification**:
   - Start local dev server (`npm run dev`).
   - Run headless auditor to capture viewports:
     ```powershell
     python scripts/capture_ui.py --url http://localhost:3000
     ```
   - Evaluate screenshots against the **Superfuture 5-Pillar Visual Critique Rubric** in `reference/REVIEW_CHECKLIST.md` (Typographic Hierarchy, Spacing Rhythm, Surface & Noise, Affordance, AI Cliché Residuals).
4. **Natural Language Feedback Iteration**:
   - When the user gives aesthetic feedback ("너무 휑해", "장난감 같아"), consult the **Feedback Translation Dictionary** in `reference/REVIEW_CHECKLIST.md` to deterministically adjust tokens and dials.

---

## 4. Companion Bridges & Tools

- `scripts/lint_ui.py`: Fast offline anti-pattern & accessibility detector (ported from `pbakaus/impeccable` & `addyosmani/accessibility`).
- `scripts/capture_ui.py`: Playwright headless screenshot & console error auditor.
- `scripts/sync_figma.py`: Synchronizes remote Figma Variables directly into `reference/tokens/*.json`.
- `scripts/verify_repo.py`: Repository self-integrity and architectural verification suite.
