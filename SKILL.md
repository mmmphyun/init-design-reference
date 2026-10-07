---
name: init-design-reference
description: Scaffolds a production-grade UI design reference, pattern architecture (.design), and deterministic closed-loop verification pipeline to prevent AI visual drift.
---

# Anti-Slop & Closed-Loop UI Framework

Scaffolds a `.design/` directory structure within the project root to enforce deterministic design constraints, anti-cliché standards, pattern recipes, and closed-loop visual verification.

Integrates proven design engineering standards from the open-source ecosystem (`shadcn/ui`, `emilkowalski/apple-design`, `MengTo/beautiful-shadows`, `addyosmani/accessibility`, `Superfuture/design-review`, `pbakaus/impeccable`, `jakubkrehel/skills`, `wshobson/interaction-design`). See `NOTICE.md` for license notices.

## 1. Directory Structure (.design Goldilocks Architecture)

```
.design/                # Project design repository (supports legacy reference/ fallback)
  screenshots/          # UI target captures & audit runs (.gitignore applied)
    audit/              # Output from scripts/capture_ui.py
  tokens/               # Full design tokens preserved for project runtime
    colors.json         # Hex values for surface, text, accents
    spacing.json        # Rem-based vertical & horizontal rhythm
    typography.json     # Role-based typography & official CDN font imports
    radii.json          # Border radius tokens
    shadows.json        # Multi-layer ambient occlusion depth models (Meng To)
    motion.json         # Durations, Apple spring physics & gesture constraints (Emil Kowalski)
    theme.css           # Runtime CSS bridge (Tailwind v4 / Vanilla CSS variables)
    tailwind.preset.js  # Runtime preset bridge (Tailwind v3)
  patterns/             # Production-grade React/TSX + Tailwind component recipes
    layout-shells.md    # High-density cockpit & asymmetric hero layouts
    data-display.md     # 4-state data tables & anti-cliché telemetry cards
    forms-inputs.md     # Accessible validated inputs & filter toolbars
    micro-interactions.md # Tactile press, spring curves, hardware acceleration
  DESIGN.md             # Single design constitution & 3-Dial Taste Configuration
```

> **Zero Repo Pollution**: Static guidelines (`notes/*.md`, `fonts/` guides, `REVIEW_CHECKLIST.md`, `COMPONENTS.md`) remain isolated in the global skill and are referenced Just-In-Time (JIT) without cluttering the project codebase.

## 2. Initialization & Preset Scaffolding

Run the framework adapter with an optional domain preset (defaults to `.design`, falls back to existing `reference`):

```powershell
# Windows
python "$env:USERPROFILE/.gemini/config/skills/init-design-reference/scripts/adapter.py" --preset b2b-dense

# macOS / Linux
python "$HOME/.gemini/config/skills/init-design-reference/scripts/adapter.py" --preset b2b-dense
```

### Available Presets (`--preset`)
- `default`: Balanced modern SaaS baseline (Variance 5, Density 7, Motion 4)
- `b2b-dense`: High-density data cockpit & telemetry (Variance 3, Density 9, Motion 2)
- `editorial-minimal`: Airy asymmetric showcase & landing (Variance 8, Density 3, Motion 5)
- `technical-mono`: Terminal/developer tool aesthetic (Variance 4, Density 8, Motion 1)
- `apple-fluid`: Tactile spring physics & fluid gestures (Variance 6, Density 5, Motion 9)

Use `--force` or `-f` to overwrite existing templates.

---

## 3. Smart Alignment & Autonomous 5-Gate Self-Driving Loop

The development lifecycle enforces a strict **Golden Boundary**:
- **Gate 0 (High-Touch)**: Plain-language collaborative alignment & user confirmation gate.
- **Gates 1~4 (Zero-Touch Self-Driving)**: Fully autonomous orchestration loop (Skeleton -> Bind -> Self-Healing Lint -> Vision Capture) executed without human interruption.

```
[User Brief]
     │
     ▼
【Gate 0: Smart Alignment Tiki-Taka】 (High-Touch Dialog)
  - 2-Turn Plain-Language Inquiries (Subject/Vibe/Brand Color)
  - 4-Anchor Mapping Table -> Preset & Dial Proposal
  - User Confirmation Gate (Approval Required)
     │
     ▼
【Gate 0: Deterministic Hard-Guard】
  - adapter.py --verify-spec (Blocks progression if dials/tokens are missing)
     │
     ▼
【Gates 1~4: Autonomous Self-Driving Orchestration Loop】 (Zero-Touch)
  - Gate 1 (/craft)     : Semantic DOM skeleton (0 styling, pure ARIA)
  - Gate 2 (/bind)      : Token & Surface hierarchy binding (Level 0/1)
  - Gate 3 (/critique)  : lint_ui.py self-healing loop (Max 3 retries)
  - Gate 4 (/harden)    : 4-State completeness, dev server mount & capture_ui.py
     │
     ▼ (Rendered Viewport Capture Delivered)
[User Visual Feedback] ──(Token Reverse-Traceability)──► Adjust tokens/*.json (0-diff TSX)
```

### Gate 0: Smart Alignment & Token Synthesis (High-Touch)
1. **Plain-Language Intake (for Non-Experts)**:
   - Ask up to 3 non-technical questions if requirements are underspecified:
     - "누가 어떤 상황에서 주로 쓰나요? (B2B 전문가 도구 / 대중용 모바일 서비스 / 개발자 터미널)"
     - "원하는 전체적인 분위기는 어떤가요? (산뜻하고 트렌디한 토스·애플 / 차분하고 전문적인 다크 콕핏 / 종이 같은 미니멀)"
     - "반드시 살리고 싶은 브랜드 포인트 컬러나 시그니처가 있나요?"
2. **4-Anchor Mapping & Dial Proposal (Anchor & Tune)**:
   - Match the user's intent to the nearest anchor preset, then propose 3-dial tuning:
     - 토스/애플 감성 B2C: `apple-fluid` (Variance 6, Density 5, Motion 9)
     - AWS/엔터프라이즈 데이터 콕핏: `b2b-dense` (Variance 3, Density 9, Motion 2)
     - 노션/에디토리얼 타이포그래피: `editorial-minimal` (Variance 8, Density 3, Motion 5)
     - 개발자 터미널/CLI 툴: `technical-mono` (Variance 4, Density 8, Motion 1)
3. **User Approval Gate (Strict Lock)**:
   - Propose the matched preset, 3 dials, and visual rationale to the user, then request explicit confirmation.
   - **MANDATORY**: Do NOT execute `adapter.py` or write files prior to receiving explicit user confirmation, even if the user provided clear domain keywords in their initial brief.
4. **Deterministic Hard-Guard**:
   - Scaffold the design repository and run the specification hard-guard:
     ```powershell
     python scripts/adapter.py --preset <selected-preset>
     python scripts/adapter.py --verify-spec
     ```
   - If `--verify-spec` returns exit code 1 (missing dials or semantic tokens), pipeline execution is halted until corrected.

---

### Gate 1~4: Autonomous Self-Driving Orchestration Loop (Zero-Touch)

Upon Gate 0 approval, execute Gates 1 through 4 continuously without asking intermediate questions.

#### Gate 1: `/craft` (Semantic Skeleton)
- Construct semantic DOM hierarchy (`<header>`, `<main>`, `<aside>`, `<table>`, `<article>`).
- Apply **zero styling or decorative colors**. Focus exclusively on structural hierarchy, responsive flex/grid layouts, and Radix/ARIA accessibility roles (`role="table"`, `aria-expanded`).

#### Gate 2: `/bind` (Token & Surface Binding)
- Bind styles exclusively using semantic CSS tokens (`bg-surface`, `text-foreground`, `border-border-default`, `shadow-elevation-1` to `shadow-elevation-4`).
- **Surface Hierarchy Mandate**: Enforce Level 0 Canvas (`bg-background`) vs Level 1 Surface (`bg-surface`) contrast. Embedded panels and cards must sit on Level 1.
- **Font & CSS Bridge Rule**: Ensure `@import "../.design/tokens/theme.css";` is placed at Line 1 of the global CSS before any other CSS rules to prevent W3C `@import` dropping. Monospace font stacks must include Korean glyph fallbacks (`Pretendard`, `D2Coding`) to prevent Windows OS GulimChe fallback.
- **Strict Rule**: Zero hardcoded hex colors (`#6366f1`), arbitrary padding (`p-[18px]`), or generic Tailwind colors (`bg-slate-900`).

#### Gate 3: `/critique` (Deterministic Lint & Self-Healing Loop)
- Execute the offline AST/Regex linter:
  ```powershell
  python scripts/lint_ui.py src/
  ```
- **Self-Healing Loop**: If any `[ERROR]` is reported (hardcoded hex, uppercase tracking, naked outline-none, missing alt), the agent must immediately parse the line number, auto-fix the code, and re-run `lint_ui.py`. Repeat up to 3 times until 0 errors are achieved.

#### Gate 4: `/harden` (4-State Completeness & Closed-Loop Vision Verification)
1. **Mandatory 4-State Coverage**: Verify `Loading` (skeleton with `aria-busy`), `Empty` (actionable CTA), `Error` (`role="alert"` with retry), and `Populated` are implemented.
2. **Mount & Headless Capture**:
   - Start the local dev server (`npm run dev`).
   - For isolated components, temporarily mount to the top-level route (`app/page.tsx` or `src/App.tsx`).
   - Run the headless auditor (auto-detects active port 3000, 5173, 8080):
     ```powershell
     python scripts/capture_ui.py
     ```
3. **Closed-Loop Feedback Rule (Token Reverse-Traceability)**:
   - Present captured viewport screenshots (`.design/screenshots/audit/desktop_1440.png`) to the user.
   - When the user provides visual feedback ("배경이 너무 어두워", "여백을 넓혀줘"), **DO NOT edit TSX component files directly**.
   - Modify the corresponding token in `.design/tokens/*.json`, regenerate CSS bridges with `python scripts/adapter.py`, and trigger a headless re-capture to prove that styling updates via pure design tokens.

---

## 4. Companion Bridges & Tools

- `scripts/adapter.py`: Scaffolds `.design/` architecture, generates CSS/Tailwind bridges, and runs `--verify-spec` hard-guard.
- `scripts/lint_ui.py`: Fast offline anti-pattern & accessibility detector with dynamic token recommendation.
- `scripts/capture_ui.py`: Playwright headless screenshot & console error auditor with automatic port discovery.
- `scripts/sync_figma.py`: Synchronizes remote Figma Variables directly into `.design/tokens/*.json`.
- `scripts/verify_repo.py`: Repository self-integrity, architecture decoupling, and hard-guard test suite.
