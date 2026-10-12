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
- `b2b-dense`: High-density data views & telemetry (Variance 3, Density 9, Motion 2) — **Data Preservation Mandate**: "핵심 데이터 무단 생략 금지 + 단위 면적당 유효 정보 수용 극대화", 주요 보조 지표 및 상태값 필수 수납, `max-w-7xl` 인위적 폭 제한 지양 및 `w-full` 전폭 확장, 수치 우측 정렬(`text-right`), 위험도/우선순위(Severity/Priority-first) 정렬
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
【Gate 0: Smart Alignment Deep Probe】 (High-Touch Dialog)
  - Turn-Budgeted Probe (최대 2~3턴, 턴당 1~2개 질문)
  - 6-Decision Matrix Tracking (확인 / 프로젝트 추출 / 미정 / 가정)
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
  - Phase 3 (Critique)  : lint_ui.py self-healing loop (Max 3 retries, a11y & token errors only)
  - Phase 4 (Harden)    : 4-State completeness, dev server mount & capture_ui.py
     │
     ▼ (Rendered Viewport Capture Delivered)
[User Visual Feedback] ──(Token & Structure Separation)──► Style -> tokens/*.json / Structure -> Component TSX
```

### Gate 0: Deep Listening & Dynamic Theme Synthesis (High-Touch Probe)

1. **7-Decision Matrix & Existing Project Inspection**:
   - 에이전트는 기존 프로젝트가 있을 경우 먼저 정체성을 파악한다:
     - 검사 대상: `AGENTS.md`, `.design/DESIGN.md`, `tokens/*.json`, `tailwind.config.*`, 전역 CSS, 대표 페이지 TSX.
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

2. **Adaptive Deep Probe (설문지형 일괄 질문 엄격 금지)**:
   - 턴당 **최대 1~2개의 핵심 질문**만 제시하며, 결과를 실질적으로 바꿀 **[미정]** 항목에 대해서만 질문한다.
   - 최초 요청이나 기존 프로젝트에서 이미 확인된 항목은 질문하지 않고 요약하여 확인한다.
   - 기본 권장 대화 예산은 **2~3턴**이며, 핵심 결정 사항에 [미정]이 남아 있다면 사용자의 선택권을 위해 필요한 만큼 확인을 지속할 수 있다(단일 주제 꼬리질문은 최대 1회).
   - 중립적 감각 표현을 사용한다:
     - 시각 스타일/톤: "절제되고 차분한 고대비 다크 테마 vs 편안한 종이 질감의 웜톤 라이트 테마 vs 선명한 원색 포인트의 미니멀 테마"
     - 상호작용 피드백: "지체 없이 절제된 즉각 반응 vs 부드럽고 탄성 있는 유기적 반응"
     - 정보 밀도: "보조 수치와 지표가 한눈에 모이는 고밀도 구성 vs 여백과 타이포그래피 리듬 중심의 여유로운 구성"

3. **Dynamic Theme Synthesis (동적 테마 합성)**:
   - 기성 프리셋은 출발 베이스라인으로만 활용하며, 사용자와 합의된 3대 Taste 다이얼(`DESIGN_VARIANCE`, `VISUAL_DENSITY`, `MOTION_INTENSITY`)을 1~10 범위로 동적 합성한다.
   - 인터뷰를 통해 합의된 고유 브랜드 컬러, 폰트 스택, 인터랙션 원칙을 명세화한다.

4. **Synthesis Briefing & User Approval Gate**:
   - 도출된 다이얼 수치, 합의된 시그니처 색상/폰트, 그리고 미처 논의되지 않아 채운 **[에이전트 가정]** 사항을 브리핑하고 최종 확인을 구한다.
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
- Semantic DOM 계층 구조(`header`, `main`, `aside`, `table`, `article`) 구축.
- **장식용 스타일/색상 배제**. 구조적 계층, 반응형 Flex/Grid, Radix/ARIA 접근성 역할(`role="table"`, `aria-expanded`)에 집중.
- **고밀도 화면 규칙 (사용자가 확정한 Density >= 8)**: 사용자가 고밀도 구성을 선택한 경우에 한하여 전폭(`w-full`) 레이아웃을 사용하고 불필요한 공백 방치를 지양한다. 여유로운 밀도를 선택한 일반 뷰에서는 적절한 최대 폭(`max-w-*`)을 유지한다.
- **Zero-Truncation Policy**: 핵심 도메인 식별자(ID, 코드, 식별 번호 등)에 무분별한 `truncate`를 걸어 식별을 방해하는 행위를 지양한다.

#### Phase 2: Token & Surface Binding (Bind)
- 시맨틱 CSS 토큰(`bg-surface`, `text-foreground`, `border-border-default` 등)으로 스타일 바인딩.
- **Surface 계층 구조**: Level 0 Canvas(`bg-background`)와 Level 1 Surface(`bg-surface`) 간의 대비를 보장한다.
- **Font & CSS Bridge Rule**: 토큰 브리지 import(`@import "../.design/tokens/theme.css";` 또는 해당 CSS 파일 위치 기준 상대 경로)가 전역 CSS 최상단(Line 1)에 위치하도록 보장한다. Monospace 폰트 스택에는 한글 폴백(`Pretendard`, `D2Coding`)을 필수로 포함한다.
- **데이터 정렬 및 인디케이터 표준**: 다중 행 수치 비교가 필요한 데이터 표(Table)의 수치 열은 우측 정렬(`text-right`)을 적용한다.
- **Strict Rule**: 하드코딩된 hex 코드(`#6366f1`) 또는 임의의 Tailwind 기본 색상(`bg-slate-900`) 직접 사용 금지.

#### Phase 3: Deterministic Lint & Self-Healing Loop (Critique)
- 정적 린터 실행:
   ```powershell
   python scripts/lint_ui.py src/
   ```
- **Self-Healing Loop**: 접근성(a11y) 결함 및 하드코딩된 토큰 등 객관적 `[ERROR]` 발생 시 라인 번호를 파싱하여 자동 교정 후 재검사(최대 3회). 디자인 권고사항(`[WARN]`)은 임의로 레이아웃을 깨뜨리지 않고 존중한다.

#### Phase 4: Completeness & Vision Verification (Harden)
1. **조건부 4-State 커버리지**: 원격 비동기 데이터 패칭이나 컬렉션 조회가 발생하는 비동기 데이터 뷰에 한하여 `Loading`(스켈레톤), `Empty`(CTA), `Error`(재시도), `Populated` 4상태를 구현한다. 순수 정적/레이아웃 컴포넌트는 해당되지 않는다.
2. **Mount & Headless Capture**:
   - 로컬 개발 서버 확인 및 컴포넌트 마운트.
   - 헤드리스 감사 실행:
     ```powershell
     python scripts/capture_ui.py
     ```
3. **폐루프 시각 피드백 원칙 (Token & Structure Separation)**:
   - 캡처된 뷰포트 스크린샷을 사용자에게 제시한다.
   - **스타일 피드백 (색상, 간격, 폰트)**: TSX를 건드리지 않고 `.design/tokens/*.json`을 수정한 뒤 CSS 브리지를 재생성(`python scripts/adapter.py --bridge-only`)하여 전역 일관성을 유지한다.
   - **구조적 피드백 (컴포넌트 배치, 정보 구조, DOM 변경)**: 컴포넌트 TSX 코드를 직접 수정하여 사용자 요구를 충실히 반영한다.

---

## 4. Companion Bridges & Tools

- `scripts/adapter.py`: Scaffolds `.design/` architecture, generates CSS/Tailwind bridges, and runs `--verify-spec` hard-guard.
- `scripts/lint_ui.py`: Fast offline anti-pattern & accessibility detector with dynamic token recommendation.
- `scripts/capture_ui.py`: Playwright headless screenshot & console error auditor with automatic port discovery.
- `scripts/sync_figma.py`: Synchronizes remote Figma Variables directly into `.design/tokens/*.json`.
- `scripts/verify_repo.py`: Repository self-integrity, architecture decoupling, and hard-guard test suite.
