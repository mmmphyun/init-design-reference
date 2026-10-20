---
name: init-design-reference
description: Scaffolds a production-grade UI design reference, pattern architecture (.design), and deterministic closed-loop verification pipeline to prevent AI visual drift.
---

# Anti-Slop & Closed-Loop UI Framework

Scaffolds a `.design/` directory structure within the project root to enforce deterministic design constraints, anti-cliché standards, pattern recipes, and closed-loop visual verification.

Integrates proven design engineering standards from the open-source ecosystem (`shadcn/ui`, `emilkowalski/apple-design`, `MengTo/beautiful-shadows`, `addyosmani/accessibility`, `Superfuture/design-review`, `pbakaus/impeccable`, `plugin87/ux-ui-agent-skills`, `vercel-labs/web-interface-guidelines`, `jakubkrehel/skills`, `wshobson/interaction-design`). See `NOTICE.md` for license notices.

### Framework Support & Architecture Neutrality
- **Tier 1 Supported Stacks**: React / Next.js, Vue / Nuxt, Svelte / SvelteKit, Vanilla CSS.
- **Build Tool Separation**: Vite is categorized as a bundler/build tool, not a framework. Framework-specific conventions take precedence.
- **Core Principles vs Pattern Examples**:
  - **Universal Core Support**: Semantic DOM, ARIA accessibility, design token SSOT, 4-state lifecycle, and motion physics remain strictly framework-neutral across all stacks.
  - **Code Pattern Scope**: Full production recipes are provided in React/TSX as baseline. Vue 3 and Svelte 5 implementations are provided for core interactive and input patterns (`micro-interactions.md`, `forms-inputs.md`). For other patterns, agents follow the headless composition idioms in `COMPONENTS.md` using the target framework's primitives.
- **Unknown / Legacy Stacks**: Apply framework-neutral semantic HTML and CSS Custom Properties (`:root`). Escalate critical ambiguities (target app, styling entrypoint) to Gate 0.
- **Bridge Support Scope**:
  - Automatically generated: Tailwind v4 (`theme.css`), Tailwind v3 (`tailwind.preset.js` & `tokens.css`), Vanilla CSS (`tokens.css`).
  - Unsupported runtime engines (CSS-in-JS like styled-components, Emotion, Panda CSS): Manually reference `:root` CSS variables exported in `tokens.css`.

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
  patterns/             # Production-grade component recipes (React/TSX, Vue 3, Svelte 5)
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
# Standard Single App
python "$env:USERPROFILE/.gemini/config/skills/init-design-reference/scripts/adapter.py" --preset b2b-dense

# Workspace Monorepo Target
python "$env:USERPROFILE/.gemini/config/skills/init-design-reference/scripts/adapter.py" --preset b2b-dense --app apps/web

# Explicit CSS Entrypoint Override
python "$env:USERPROFILE/.gemini/config/skills/init-design-reference/scripts/adapter.py" --css src/styles/main.css
```

### Available Presets (`--preset`)
- `default`: Balanced modern SaaS baseline (Variance 5, Density 7, Motion 4)
- `b2b-dense`: High-density data views & telemetry (Variance 3, Density 9, Motion 2) — **Data Preservation Mandate**: "핵심 데이터 무단 생략 금지 + 단위 면적당 유효 정보 수용 극대화", 주요 보조 지표 및 상태값 필수 수납, `max-w-7xl` 인위적 폭 제한 지양 및 `w-full` 전폭 확장, 수치 우측 정렬(`text-right`), 위험도/우선순위(Severity/Priority-first) 정렬
- `editorial-minimal`: Airy asymmetric showcase & landing (Variance 8, Density 3, Motion 5)
- `technical-mono`: Terminal/developer tool aesthetic (Variance 4, Density 8, Motion 1)
- `apple-fluid`: Tactile spring physics & fluid gestures (Variance 6, Density 5, Motion 9)

Use `--force` or `-f` to overwrite existing templates. `--app <dir>` specifies the workspace subproject, and `--css <path>` specifies the CSS entrypoint.

---

## 3. Smart Alignment & Autonomous 5-Gate Self-Driving Loop

The development lifecycle enforces a strict **Golden Boundary**:
- **Gate 0 (High-Touch)**: Plain-language collaborative alignment & user confirmation gate.
- **Gates 1~4 (Zero-Touch Self-Driving)**: Fully autonomous orchestration loop (Skeleton -> Bind -> Self-Healing Lint -> Vision Capture) executed without human interruption.

```
[User Brief]
     │
     ▼
【Gate 0: Smart Alignment Deep Probe】 (High-Touch Dialog)
  - Turn-Budgeted Probe (권장 2~3턴, 턴당 1~2개 질문, 미정 항목 연장 가능)
  - 7-Decision Matrix Tracking (확인 / 프로젝트 추출 / 미정 / 가정)
  - Dynamic Theme Synthesis (3 Dials 1~10 + Token Composition)
  - Synthesis Briefing & User Approval Gate
     │
     ▼
【Gate 0: Deterministic Hard-Guard】
  - adapter.py --preset <base> --dials <v,d,m>
  - adapter.py --verify-spec (Blocks progression if dials/tokens are missing)
     │
     ▼
【Phase 1~4: Autonomous Self-Driving Orchestration Loop】 (Zero-Touch)
  - Phase 1 (Craft)     : Semantic DOM skeleton (0 styling, pure ARIA)
  - Phase 2 (Bind)      : Token & Surface hierarchy binding (Level 0/1)
  - Phase 3 (Critique)  : lint_ui.py self-healing loop (Max 3 retries, a11y, UX contracts & token errors)
  - Phase 4 (Harden)    : 4-State, capture_ui.py (Target size, contrast, overflow receipt) & Heuristic Critique
     │
     ▼ (Rendered Viewport Capture Delivered)
[User Visual Feedback] ──(Token & Structure Separation)──► Style -> tokens/*.json / Structure -> Component TSX
```

### Gate 0: Deep Listening & Dynamic Theme Synthesis (High-Touch Probe)

1. **7-Decision Matrix & Existing Project Inspection**:
   - 에이전트는 기존 프로젝트가 있을 경우 먼저 정체성을 파악한다:
     - 검사 대상: 루트 및 하위 워크스페이스 `package.json`, `pnpm-workspace.yaml`, `AGENTS.md`, `.design/DESIGN.md`, `tokens/*.json`, `tailwind.config.*`, 전역 CSS, 대표 화면 컴포넌트.
     - **스택 탐지 및 모호성 해결**: React/Next.js, Vue/Nuxt, Svelte/SvelteKit, Vanilla CSS 여부 및 빌드 도구(Vite)를 구분한다. 다중 앱 모노레포(`apps/*`)이거나 CSS 엔트리포인트 후보가 복수일 경우 임의로 특정 앱을 단정하지 않고 사용자 확인 또는 CLI 옵션(`--app`, `--css`)으로 해결한다.
   - 7대 결정 항목 매트릭스를 추적 관리한다:
     1. **대상 사용자와 사용 맥락 (Context)**
     2. **핵심 작업 및 주요 화면 (Hero Action / Screen)**
     3. **시각 스타일 및 참고 레퍼런스 (Visual Direction & References)**: 원하는 톤앤매너, 배경 밝기(다크 vs 라이트 vs 웜톤), 타이포그래피 성격(산세리프 vs 세리프 vs 모노), 벤치마크 서비스나 지향하는 심미적 분위기.
     4. **상호작용 감각과 모션 (Interaction Vibe)**
     5. **콘텐츠/정보 밀도 (Visual Density)**
     6. **지원 기기 및 뷰포트 범위 (Device Scope)**
     7. **브랜드/접근성 제약 (Constraints & Brand)**
   - 각 항목의 상태를 **[사용자 확인] / [기존 프로젝트에서 확인] / [미정] / [에이전트 가정]**으로 분류한다.
   - **기존 디자인 시스템 전수 매핑 및 단일 원천(SSOT) 프로토콜 (Legacy Design System Mapping)**:
     - 기존 프로젝트에 `.design/tokens/*.json`이 없더라도 `tailwind.config.*`의 커스텀 테마나 전역 CSS의 커스텀 속성(`--*`)이 존재하는 경우:
     - **전수 토큰 식별**: 색상(배경, 텍스트, 액센트, 보더)과 폰트뿐 아니라, 기존 시스템에 명시된 간격 스케일(`spacing`), 보더 반경(`radii`), 입체감/그림자(`shadows`), 모션 곡선(`motion`)까지 전수 식별하여 **[기존 프로젝트에서 확인]**으로 기록한다.
     - **토큰 전사 및 SSOT 동기화**: 스캐폴딩 후 임의의 프리셋 기본값으로 덮어쓰지 않고, 식별된 기존 값을 대응하는 토큰 파일(`.design/tokens/colors.json`, `typography.json`, `spacing.json`, `radii.json`, `shadows.json`, `motion.json`)에 전사 주입한다. 기존에 미정의된 영역에 한해서만 프리셋 기본값을 보완재로 채택한다.
     - **브리지 동기화**: 수동 매핑 완료 후 `python scripts/adapter.py --bridge-only`를 실행하여 런타임 CSS 브리지(`theme.css`, `tokens.css`)를 재생성한다.

2. **Reference-First & Observable Deep Probe (설문지형 일괄 질문 엄격 금지)**:
   - **레퍼런스 우선 분석**: 사용자가 레퍼런스 화면, 기존 제품, 브랜드 가이드, 싫어하는 사례를 제공하면 질문보다 분석을 우선하여 시각 규칙을 추출한다.
   - **레퍼런스 부재 시 맥락 기반 제안**: 레퍼런스가 없으면 도메인별 고정 공식을 자동 적용하지 말고, 제품 목적과 콘텐츠에 맞는 시각 방향과 그 이유를 먼저 제안한다.
   - 턴당 **최대 1-2개의 핵심 질문**만 제시하며, 결과를 실질적으로 바꿀 **[미정]** 항목에 대해서만 질문한다(권장 2-3턴, 단일 주제 꼬리질문 최대 1회).
   - **관찰 가능한 선택(Observable Choices)으로 질문**: "차분한", "유기적인", "미니멀한" 같은 추상적 형용사에 의존하지 말고 화면에서 관찰 가능한 차이로 합의한다:
     - 표면과 구분 방식: 배경-카드 명도 대비 중심 vs 밝은 단일 배경과 1px 구분선 중심
     - 콘텐츠 폭과 밀도: 전폭(`w-full`) 다중 지표 노출 vs 고정 폭(`max-w-*`) 핵심 작업 집중
     - 강조색 역할: 주요 CTA 버튼에만 제한 vs 상태 지표·경보 중심 활용

3. **Context-Driven Theme Synthesis & Dial Recording**:
   - **다이얼의 역할 한정**: 3대 다이얼(`DESIGN_VARIANCE`, `VISUAL_DENSITY`, `MOTION_INTENSITY`)은 요구사항을 요약 기록하는 보조값이다. 다이얼 숫자를 색·모서리·비대칭·애니메이션에 기계적으로 대응시키거나 화면을 숫자에 억지로 맞추지 않는다.
   - **분야 이름 기반 자동 팔레트 선택 금지**: 도메인 이름만 보고 프리셋 팔레트를 정답처럼 적용하지 않는다. 기존 브랜드나 사용자 방향이 항상 우선한다.
   - **동적 색상 팔레트 생성 (Color Palette MCP 활용 권장)**:
     - 사용자가 브랜드 키 컬러(Hex)나 구체적 시각 근거를 제시한 경우 `color-palette-mcp`(`generate_palette`, `generate_dynamic_colors`, `extend_palette_for_project`)를 호출하여 시맨틱 색상 체계를 생성한다.
     - **시맨틱 토큰 매핑 규약**: MCP 출력 스케일(50-900)을 `.design/tokens/colors.json` 시맨틱 슬롯(`background.primary`, `background.surface`, `text.primary`, `accent.primary`, `border.default`, `status.*`)에 매핑한다.
     - **접근성 검증**: 본문 텍스트 대 표면 간 최소 4.5:1 (WCAG 2.1 AA) 대비율을 충족하도록 보정한다.

4. **Synthesis Briefing & User Approval Gate**:
   - 합의된 시각 선택(표면 대비, 위계, 색상 근거), 보조 다이얼 기록값(짧은 의미 설명 포함), 그리고 **[에이전트 가정]** 사항을 브리핑하고 최종 확인을 구한다.
   - **MANDATORY**: 사용자 승인(Approval) 이전에는 `adapter.py` 실행이나 파일 생성을 하지 않는다.

5. **Deterministic Hard-Guard & Token Injection**:
   - 승인 후 스캐폴딩 실행:
     ```powershell
     python scripts/adapter.py --preset <base-preset> --dials <v,d,m>
     ```
   - **Token Injection Mandate**: 기존 프로젝트 토큰이 없는 신규 스캐폴딩의 경우, 사용자와 합의된 고유 브랜드 컬러 및 폰트를 `.design/tokens/colors.json`, `typography.json`에 직접 반영하고 CSS 브리지를 재생성(`python scripts/adapter.py --bridge-only`)한다. 기존 프로젝트에 커스텀 디자인 시스템(CSS 변수, Tailwind 테마)이 확립된 경우 앞선 전수 매핑 프로토콜에 따라 기존 값을 토큰 파일들에 전사하여 완전히 보존한다.
   - 스펙 검증 하드가드 실행:
     ```powershell
     python scripts/adapter.py --verify-spec
     ```
   - `--verify-spec` 실패 시(다이얼 누락, 1~10 범위 초과, 비정상 hex 등) 즉시 보정한다.

---

### Phase 1~4: Autonomous Self-Driving Orchestration Loop (Zero-Touch)

Gate 0 승인 즉시 Phase 1부터 Phase 4까지 중간 질문 없이 한 호흡으로 연속 실행한다. 단, 화면 구조, 핵심 도메인 식별자, 브랜드/접근성 제약 등 사전 인터뷰에서 드러나지 않은 새로운 중대 결정([미정])이 발생한 경우에 한하여 예외적으로 사용자에게 에스컬레이션하여 확인을 구한다. 그 외의 세부 구현 선택은 자율 실행한다.

#### Phase 1: Semantic Skeleton (Craft)
- Semantic DOM 계층 구조(`header`, `main`, `aside`, `table`, `article`) 구축 (React, Vue, Svelte, HTML 공통).
- **장식용 스타일/색상 배제**. 구조적 계층, 반응형 Flex/Grid, W3C ARIA 접근성 역할(`role="table"`, `aria-expanded`)에 집중.
- **고밀도 화면 규칙 (사용자가 확정한 Density >= 8)**: 사용자가 고밀도 구성을 선택한 경우에 한하여 전폭(`w-full`) 레이아웃을 사용하고 불필요한 공백 방치를 지양한다. 여유로운 밀도를 선택한 일반 뷰에서는 적절한 최대 폭(`max-w-*`)을 유지한다.
- **Zero-Truncation Policy**: 핵심 도메인 식별자(ID, 코드, 식별 번호 등)에 무분별한 `truncate`를 걸어 식별을 방해하는 행위를 지양한다.

#### Phase 2: Token & Surface Binding (Bind)
- 시맨틱 CSS 토큰(`bg-surface`, `text-foreground`, `border-border-default` 등)으로 스타일 바인딩 (프레임워크 템플릿 문법에 맞춤 바인딩).
- **Surface 계층 구조**: Level 0 Canvas(`bg-background`)와 Level 1 Surface(`bg-surface`) 간의 대비를 보장한다.
- **Font & CSS Bridge Rule**: 토큰 브리지 import(`@import "../.design/tokens/theme.css";` 또는 해당 CSS 파일 위치 기준 상대 경로)가 전역 CSS 최상단(Line 1)에 위치하도록 보장한다. Monospace 폰트 스택에는 한글 폴백(`Pretendard`, `D2Coding`)을 필수로 포함한다.
- **조건부 디자인 기본값 적용**:
  - **수치 우측 정렬**: 다중 행에서 열 단위로 자릿수·크기를 비교해야 하는 테이블 수치 열에 `text-right`를 적용한다(단일 요약값이나 문장 결합형 수치는 맥락에 맞게 정렬).
  - **카드 사용 절제**: 서로 다른 정보 그룹을 분리하는 데 실제로 도움이 될 때만 카드를 사용하며, 단순 목록을 관성적으로 동일한 카드로 쪼개지 않는다.
- **모션 및 상호작용 바인딩 (Motion Contract)**:
  - 컴포넌트 상호작용 설계 시 `templates/notes/interaction.md`를 JIT 참조한다.
  - 공간 이동은 GPU 가속 속성(`transform`, `opacity`, `filter`), 상태 피드백은 페인트 속성(`color`, `background-color`, `border-color`, `box-shadow`)으로 한정하며 `prefers-reduced-motion` 대등성을 보장한다.
- **Strict Rule (하드 제약)**: 하드코딩된 hex 코드(`#6366f1`) 또는 임의의 Tailwind 기본 색상(`bg-slate-900`) 직접 사용 금지.

#### Phase 3: Deterministic Lint & Self-Healing Loop (Critique)
- 정적 린터 실행:
   ```powershell
   python scripts/lint_ui.py src/
   ```
- **린트 범위 및 Self-Healing**: 하드코딩 색상, 레이아웃 스래싱뿐 아니라 비시맨틱 인터랙션(`<div onClick>`), 아이콘 버튼의 접근성 이름 누락, 붙여넣기 차단(`onPaste + preventDefault`), 라벨 없는 폼 컨트롤, 화면 확대 차단 메타 태그를 기계적으로 탐지한다. `[ERROR]` 발생 시 자동 교정 후 재검사(최대 3회)하되, **린트 통과(0 errors)를 좋은 디자인이나 작업 완성으로 간주하지 않는다.**

#### Phase 4: Completeness, DOM UX Audit & Visual Feedback Loop (Harden)
1. **조건부 4-State 커버리지**: 원격 비동기 데이터 패칭이나 컬렉션 조회가 발생하는 비동기 데이터 뷰에 한하여 `Loading`(스켈레톤), `Empty`(CTA), `Error`(재시도), `Populated` 4상태를 구현한다. 순수 정적/레이아웃 컴포넌트는 해당되지 않는다.
2. **Mount, Headless Capture & Deterministic DOM UX Audit**:
   - 로컬 개발 서버 확인, 헤드리스 캡처 및 결정론적 DOM UX 감사 실행:
     ```powershell
     python scripts/capture_ui.py
     ```
   - **결정론적 영수증(`ux_audit_receipt.json`) 검증**:
     - 타겟 크기: 모든 클릭/터치 타겟 >= 24x24 CSS px (WCAG 2.2 SC 2.5.8), 모바일 >= 44x44 CSS px 권장.
     - 실제 렌더링 명도 대비: 알파 합성 계산 대비율 >= 4.5:1 (일반 텍스트) 및 >= 3.0:1 (대형 텍스트).
     - 가로 오버플로우: 데스크톱/모바일 뷰포트에서 불필요한 가로 스크롤 없음(`scrollWidth <= clientWidth`).
     - **자가 치유(Self-Healing)**: `ERROR` 발생 시 완료 보고를 중단하고, 토큰(`.design/tokens/colors.json`) 또는 패딩/레이아웃 코드를 즉시 교정하여 재캡처(최대 3회)한다.
3. **UX 휴리스틱 & 시각 자가진단 (Heuristic & Persona Critique)**:
   - 영수증 검증 통과 후, `templates/root/REVIEW_CHECKLIST.md` 섹션 2의 5대 시각 질문과 UX 휴리스틱(인지 부하, 오류 복구, 사용자 제어) 및 도메인 매핑 페르소나(Alex, Sam, Jordan, Riley, Casey) Red Flag를 스스로 점검한다.
4. **진단 기반 피드백 반영 원칙 (Diagnose Before Prescribing)**:
   - 사용자가 "AI스럽다", "어색하다" 등의 피드백을 주면 다이얼 숫자를 바꾸거나 비대칭·장식 요소를 바로 추가하지 않는다.
   - 먼저 화면에서 어색함의 원인(평평한 위계, 반복된 카드·배지, 무의미한 강조색, 균일한 간격 등)을 구체적으로 진단하고 가장 적은 수정으로 해결한다.
   - **스타일 조정 (색상, 간격, 폰트)**: `.design/tokens/*.json`을 수정한 뒤 CSS 브리지를 재생성(`python scripts/adapter.py --bridge-only`)한다.
   - **구조/위계 조정 (불필요한 카드/배지 제거, 영역 비율 조정, DOM 변경)**: 프레임워크 컴포넌트 코드를 직접 수정한다.

---

## 4. Companion Bridges & Tools

- `scripts/adapter.py`: Scaffolds `.design/` architecture, generates CSS/Tailwind bridges, and runs `--verify-spec` hard-guard.
- `scripts/lint_ui.py`: Fast offline anti-pattern & accessibility detector with dynamic token recommendation.
- `scripts/capture_ui.py`: Playwright headless screenshot, deterministic DOM UX auditor (WCAG 2.2 target size, computed contrast, overflow), and receipt issuer (`ux_audit_receipt.json`).
- `scripts/sync_figma.py`: Synchronizes remote Figma Variables directly into `.design/tokens/*.json`.
- `scripts/verify_repo.py`: Repository self-integrity, architecture decoupling, and hard-guard test suite.
