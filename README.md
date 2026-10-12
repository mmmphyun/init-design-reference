# init-design-reference

[English](README.en.md) | 한국어

AI 코딩 에이전트(Google Antigravity, Claude Code, Cursor 등)의 UI 스타일 드리프트를 방지하고, 텍스트 프롬프트를 넘어 **결정론적 안티슬롭(Anti-Slop) 린터**와 **시각 피드백 폐루프(Closed-Loop Vision Verification)**를 제공하는 차세대 디자인 엔지니어링 프레임워크.

---

## 1. 실측 엔지니어링 증거 (Real-World Proof)

### ① TSX 0-diff 토큰 역추적 시각 변경 실측 (Next.js 15 App Router)
컴포넌트 TSX 코드를 단 1줄도 수정하지 않고(0-diff), `.design/tokens/colors.json` 수정 및 CSS 브리지 재생성만으로 실제 프로덕션 렌더링이 변경됨을 헤드리스 Playwright로 실측 검증했습니다.

| 기준 렌더링 (`assets/baseline.png`) | 토큰 갱신 렌더링 (`assets/updated.png`) |
|:---:|:---:|
| ![Baseline](assets/baseline.png) | ![Updated](assets/updated.png) |
| `--surface`: `#12151c` (Cockpit Carbon)<br>`--accent`: `#10b981` (Phosphor Emerald) | `--surface`: `#171717` (Terminal Panel)<br>`--accent`: `#f59e0b` (Amber Phosphor CRT) |

```console
$ git diff --stat app/components/MetricCard.tsx
# 0 files changed, 0 insertions(+), 0 deletions(-) -> 완전한 0-diff 달성
```

---

### ② 결정론적 정적 린터 & 자가 치유(Self-Healing) 실측
정규식 기반의 경량 정적 린터(`scripts/lint_ui.py`)로 접근성 결함과 하드코딩된 토큰을 감지하고, 에이전트가 코드를 스스로 수정하여 `0 errors`로 수렴합니다.

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

# -> 에이전트 자가 치유(Self-Healing) 루프 1회 통과 후:
$ python scripts/lint_ui.py app/components/MetricCard.tsx
Scan complete: 1 files inspected. Findings: 0 errors, 2 warnings.
Lint PASSED.
```

---

### ③ 디자인 스펙 정적 하드가드 (`--verify-spec`)
Taste 3대 다이얼 설정(1-10 범위) 및 필수 핵심 색상 토큰(`background.surface`, `background.primary`, `accent.primary`, `border.default`)의 존재와 유효 hex 포맷을 정적으로 검증하여 스펙 오류 전파를 차단합니다. 에이전트의 사용자 승인 완료 후 코드 생성 직전에 실행되어 설정 무결성을 보장합니다.


```console
$ python scripts/adapter.py --verify-spec
[HARD-GUARD FAIL] .design\DESIGN.md is missing one of DESIGN_VARIANCE, VISUAL_DENSITY, MOTION_INTENSITY.
# -> 스펙 불일치 시 0이 아닌 종료 코드를 반환하여 에이전트가 설정을 정상화하도록 유도
```

---

## 2. 개발 배경 및 핵심 메커니즘

### AI가 만드는 화면이 항상 똑같은 이유 (Attention Drift & Prior 회귀)
LLM에게 프론트엔드 코딩을 맡기면 보라색·인디고 그라디언트, 둥근 SaaS 카드 나열, 습관적인 `tracking-widest uppercase` 라벨로 수렴합니다. 정성적 지시("예쁘게 해줘", "모던하게")는 대화가 길어질수록 Attention 가중치가 희석되어 사전 학습 데이터의 통계적 기본값(Slop)으로 회귀하기 때문입니다.

`init-design-reference`는 이 문제를 **4대 핵심 엔지니어링 레이어**로 원천 차단합니다:
1. **토큰 & 3대 Taste 다이얼 (`DESIGN.md`, `.design/tokens/*.json`)**: `leonxlnx/taste-skill`의 3대 정량 다이얼(`DESIGN_VARIANCE`, `VISUAL_DENSITY`, `MOTION_INTENSITY`)을 수치(1~10)로 통제.
2. **검증된 컴포넌트 레시피 (`.design/patterns/*.md`)**: React/TSX + Tailwind 기반의 표준 레이아웃, 데이터 테이블, 폼, 스프링 마이크로 인터랙션 제공.
3. **결정론적 정적 린터 (`scripts/lint_ui.py`)**: `pbakaus/impeccable`의 패턴 검출 철학을 정규식 기반으로 구현하여 접근성 결함(WCAG)과 하드코딩된 토큰을 `[ERROR]`로 기계적 차단하고, 일반 AI 클리셰 및 모션 결함은 논블로킹 `[WARN]`으로 감지.
4. **시각 피드백 폐루프 (`scripts/capture_ui.py`)**: Playwright 기반으로 뷰포트 캡처 및 콘솔 런타임 에러를 수집하여 모델이 시각적으로 자가 교정하도록 유도.

---

### 프레임워크 지원 범위 & 아키텍처 중립성
- **1차 우선 지원 스택**: React / Next.js, Vue / Nuxt, Svelte / SvelteKit, 일반 CSS (Vanilla CSS).
- **빌드 도구 분리**: Vite는 번들러/빌드 도구로 분류되며, 프레임워크와 혼동하지 않고 프로젝트의 실제 프레임워크 관례를 따릅니다.
- **핵심 원칙 전면 지원 vs 패턴 예시 범위**:
  - **프레임워크 중립 코어 (전면 지원)**: 시맨틱 DOM, ARIA 접근성 규약, 3-Dial Taste 체계, 4-State 생명주기 및 모션 물리는 모든 스택에서 100% 동일한 규약으로 동작합니다.
  - **코드 패턴 예시 범위**: React/TSX를 기본 기준선 레시피로 전 패턴에 제공하며, Vue 3 및 Svelte 5는 문법과 상태 바인딩이 차별화되는 핵심 패턴(`micro-interactions.md`, `forms-inputs.md`)의 구체적 구현을 제공합니다. 타 패턴은 `COMPONENTS.md`의 헤드리스 합성 규약(Radix Vue, Bits UI 등)을 준수하여 작성합니다.
- **스타일 브리지 지원 범위**:
  - 자동 생성: Tailwind v4 (`theme.css` via `@theme`), Tailwind v3 (`tailwind.preset.js` via `presets` & `tokens.css`), Vanilla CSS (`tokens.css` via `:root`).
  - 미지원 런타임 엔진 (CSS-in-JS: Styled Components, Emotion, Panda CSS): `tokens.css`의 `:root` CSS 변수를 수동 참조하여 연동합니다.

---

## 3. 디렉토리 구조 (.design 골디락스 아키텍처)

```
.design/                # 프로젝트 런타임 디자인 저장소 (레거시 reference/ 투명 폴백 지원)
  screenshots/          # UI 목표 캡처 및 런타임 감사 스크린샷 (.gitignore 적용)
    audit/              # scripts/capture_ui.py 결과물 보관소
  tokens/               # 프로젝트 런타임에 직접 보존되는 디자인 토큰
    colors.json         # 표면, 텍스트, 액센트 16진수 색상값
    spacing.json        # rem 기반 4px/8px 수직·수평 여백 리듬
    typography.json     # 한/영 혼용 폰트 스택 및 공식 CDN 링크
    radii.json          # 모서리 곡률 토큰
    shadows.json        # 표면 깊이 토큰 (Meng To 앰비언트 오클루전)
    motion.json         # 애니메이션 지속 시간 및 Emil Kowalski 스프링 물리 계수
    theme.css           # 런타임 CSS 브리지 (Tailwind v4 / Vanilla CSS)
    tailwind.preset.js  # 런타임 프리셋 브리지 (Tailwind v3)
  patterns/             # 프로덕션 컴포넌트 패턴 (React/TSX, Vue 3, Svelte 5)
    layout-shells.md    # 고밀도 B2B 콕핏 및 비대칭 에디토리얼 그리드
    data-display.md     # 4대 상태(Loading/Empty/Error/Populated) 완비 데이터 테이블
    forms-inputs.md     # 키보드 접근성 폼 필드 및 필터 툴바
    micro-interactions.md # scale(0.98) 누름 피드백 및 스프링 물리학
  DESIGN.md             # 코어 디자인 헌법 및 3-Dial Taste 설정
```

> **Zero Repo Pollution**: 정적 가이드라인 문서(`notes/*.md`, `REVIEW_CHECKLIST.md` 등)는 전역 스킬 내부에 격리 보존되어 레포지토리를 오염시키지 않으며, 에이전트가 JIT 방식으로 참조합니다.

---

## 4. 설치 및 프리셋 스캐폴딩

### 설치 (에이전트 전역 등록)
```powershell
# Windows (PowerShell)
irm https://raw.githubusercontent.com/mmmphyun/init-design-reference/main/install.ps1 | iex

# macOS / Linux (Bash)
curl -fsSL https://raw.githubusercontent.com/mmmphyun/init-design-reference/main/install.sh | bash
```

### 도메인 프리셋 선택 스캐폴딩 (`--preset`)
```powershell
# 기본 SaaS baseline (Variance: 5, Density: 7, Motion: 4)
python "scripts/adapter.py"

# 고밀도 B2B 데이터 콕핏 & 텔레메트리 (Variance: 3, Density: 9, Motion: 2)
python "scripts/adapter.py" --preset b2b-dense

# 다중 앱 워크스페이스 모노레포 타겟팅 (--app)
python "scripts/adapter.py" --preset b2b-dense --app apps/web

# 사용자 지정 CSS 진입 파일 명시 (--css)
python "scripts/adapter.py" --css src/styles/main.css

# 비대칭 에디토리얼 쇼케이스 & 랜딩 (Variance: 8, Density: 3, Motion: 5)
python "scripts/adapter.py" --preset editorial-minimal

# 터미널 / 개발자 도구 테크니컬 모노 (Variance: 4, Density: 8, Motion: 1)
python "scripts/adapter.py" --preset technical-mono

# 유체 스프링 모션 & 햅틱 피드백 (Variance: 6, Density: 5, Motion: 9)
python "scripts/adapter.py" --preset apple-fluid
```

---

## 5. 자율 주행 5-Gate 오케스트레이션 루프

에이전트는 프론트엔드 작업 시 다음 게이트 파이프라인을 기계적으로 준수합니다:

1. **Gate 0: Smart Alignment (High-Touch Dialog & Hard-Guard)**:
   - 기존 프로젝트 정체성 파악 및 7-Decision Matrix 추적 (확인 / 프로젝트 추출 / 미정 / 가정).
   - 다중 앱 모노레포 및 다중 CSS 진입점 후보의 모호성을 선제 확인하고 해소.
   - Adaptive Deep Probe를 통해 합의된 Taste 3-다이얼(1~10) 및 브랜드 토큰 동적 합성.
   - **사용자 승인 락(Strict Lock)**: 사용자 명시 승인 전까지 파일 작성 및 `adapter.py` 실행 금지.
   - `python scripts/adapter.py --verify-spec` 하드가드 통과 검증 (다이얼 범위 1~10 및 필수 토큰 유효성).
2. **Phase 1: Semantic Skeleton (Craft)**: 색상이나 장식 없이 시맨틱 DOM 트리, 접근성(ARIA) 구조, 반응형 그리드 구축 (React, Vue, Svelte, HTML 공통).
3. **Phase 2: Token & Surface Binding (Bind)**: `.design/tokens/*.json` 시맨틱 유틸리티 클래스 및 CSS 변수 매핑 (하드코딩 hex 및 임의 Tailwind 색상 금지).
4. **Phase 3: Deterministic Lint & Self-Healing (Critique)**:
   ```powershell
   python scripts/lint_ui.py src/
   ```
   객관적 오류(`[ERROR]`, A11y 및 토큰 누락) 발생 시 에이전트가 코드를 스스로 수정하여 3회 이내 `0 errors` 달성.
5. **Phase 4: Completeness & Vision Verification (Harden)**:
   - 비동기 데이터 뷰에 한하여 빈 데이터(Empty), 로딩(Skeleton), 에러(Error), 정상(Populated) 4-State 구현.
   - Playwright 기반 시각 검증 실행 및 캡처:
     ```powershell
     python scripts/capture_ui.py
     ```
   - 사용자 피드백 시 스타일(색상·간격·폰트)은 `tokens/*.json`으로 역추적하고, 컴포넌트 구조 변경은 프레임워크 컴포넌트 코드(TSX / Vue / Svelte / HTML)를 수정하여 정밀 반영.

---

## 라이선스 및 크레딧

- 본 프로젝트는 [MIT License](LICENSE)로 배포됩니다.
- 본 프로젝트의 룰셋, 모션 파라미터 및 다이얼 아키텍처는 아래 오픈소스 선구자들의 뛰어난 연구에 기반합니다:
  - **Emil Kowalski** ([emilkowalski/skills](https://github.com/emilkowalski/skills), MIT) - 마이크로 모션 & 스프링 물리
  - **Paul Bakaus** ([pbakaus/impeccable](https://github.com/pbakaus/impeccable), Apache 2.0) - 결정론적 안티패턴 룰셋 & 라이프사이클
  - **Leon Linz** ([leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill), MIT) - 3대 Taste 다이얼 체계
  - **Addy Osmani** - 접근성 및 시맨틱 웹 표준 규약

각 저작물의 원본 라이선스 전문 및 고지 사항은 [NOTICE.md](NOTICE.md)에서 확인하실 수 있습니다.
