# Visual Direction & Aesthetic Framework
<!-- Derived from jakubkrehel/skills (MIT License) & frontend-design -->

Synthesizes Jakub Krehel's design brief extraction protocol with deterministic token execution and curated palette libraries.

---

## 1. Gate 0: Alignment Protocol & Decision Matrix Tracking

Before touching layout or code, the agent extracts requirements using a structured **7-Decision Matrix**:

### 7-Decision Matrix Tracking
1. **Target User & Context**: Internal operators vs consumers / casual users.
2. **Hero Action & Screen**: The single most critical operation or viewport.
3. **Visual Direction & References**: Tonal mood, surface brightness (dark vs light vs warm neutral), typographic character (sans vs serif vs mono), benchmark aesthetics.
4. **Interaction & Motion Vibe**: Immediate/understated reaction vs organic/spring feedback.
5. **Visual Density**: Information-dense multi-metric cockpit vs airy typographical rhythm.
6. **Device Scope**: Desktop workspace vs mobile-first responsive.
7. **Brand Constraints & Accessibility**: Specific brand colors, contrast targets, compliance.

### Reference-First & Observable Alignment Protocol
- **우선순위 원칙 (Reference Precedence)**: 사용자가 레퍼런스 화면, 기존 제품 코드, 브랜드 가이드, 피하고 싶은 사례를 제공하면 모든 프리셋과 참고 팔레트보다 최우선으로 분석하여 반영한다.
- **레퍼런스 부재 시 제안 규칙**: 레퍼런스가 없으면 도메인별 고정 미감을 자동 적용하지 말고, 제품 목적과 콘텐츠 구조에 적합한 시각 방향과 그 근거를 먼저 제안한다.
- **관찰 가능한 선택으로 합의 (Observable Choices)**: "차분한", "유기적인", "실험적인" 같은 추상적 형용사 대신 아래 관찰 가능한 기준으로 합의한다:
  - 표면 대비: 배경과 카드 표면 간 명도 차이를 둘지, 1px 테두리로 구분할지
  - 콘텐츠 폭: 고정 최대 폭(`max-w-5xl` 등)을 쓸지, 뷰포트 전폭(`w-full`)을 쓸지
  - 제목·본문 위계: 제목과 본문 크기 차이를 크게 둘지, 조밀한 실무형 스케일을 쓸지
  - 강조색 위치: 핵심 CTA 버튼에만 제한할지, 상태 지표와 선택 행에도 부여할지
  - 정보 밀도: 한 화면에 보조 지표를 함께 노출할지, 핵심 요약만 남기고 상세 화면으로 분리할지
- **Approval Gate**: 제안한 시각 방향, 보조 다이얼 기록값, 에이전트 가정 사항을 브리핑하고 **사용자 명시 승인 후에 Phase 1-4를 실행한다.**

---

## 2. Contextual Palette Case Studies (참고 사례 — 자동 기본값 사용 금지)

아래 팔레트는 정답이나 도메인 기본값이 아닌 참고 사례다. 분야 이름만 보고 팔레트를 자동 선택하지 마라. 기존 브랜드나 사용자 시각 방향이 있으면 항상 그것을 우선하며, 아래 사례를 참고할 때는 **"이 색 조합이 대상 사용자·콘텐츠·사용 환경에 왜 적합한가"**를 먼저 검증해야 한다.

### 사례 A. 저조도 장시간 모니터링 환경 (Low-Glare Dark Surface)
- **적합 근거**: 야간 관제실·통합 모니터링처럼 장시간 화면을 주시하여 눈부심 억제가 필수이고, 정상 상태는 무채색으로 억제하되 이상 징후(경고·에러)만 색상으로 분리해야 하는 경우.
- **부적합 조건**: 일반 소비자용 금융 앱이나 주간 업무용 백오피스처럼 밝은 환경에서 긴 텍스트를 읽는 화면에는 적용하지 않는다.
- **토큰 예시**: Surface `#0F141C` / `#161D27`, Foreground `#F1F5F9` / `#94A3B8`, Primary Accent `#3B82F6` (단일 네온 그린 남용 금지), Border `#222C3A`

### 사례 B. 고조도 실무 문서 및 임상·행정 포털 (High-Clarity Light Surface)
- **적합 근거**: 밝은 실내 조명 아래에서 다량의 텍스트·폼·표 데이터를 장시간 대조해야 하며, 종이 문서 및 표준 서식과의 시각적 연속성이 필요한 경우.
- **부적합 조건**: 미디어 쇼케이스나 야간 다크 모드 전용 환경에는 적용하지 않는다.
- **토큰 예시**: Surface `#F8FAFC` / `#FFFFFF`, Foreground `#0F172A` / `#475569`, Primary Accent `#0284C7`, Border `#E2E8F0`

### 사례 C. 장문 독서 및 아카이브 출판물 (Long-Form Reading Surface)
- **적합 근거**: 3,000자 이상의 장문 아티클이나 에세이처럼 순백색(`#FFFFFF`)의 눈 피로를 줄여야 하는 텍스트 중심 출판 콘텐츠인 경우.
- **부적합 조건**: 일반 SaaS 랜딩 페이지나 대시보드에 "고급스러운 느낌"을 내기 위한 클리셰로 따뜻한 종이색+세리프+테라코타 조합을 기계적으로 차용하지 않는다.
- **토큰 예시**: Surface `#F6F5F2` / `#FFFFFF`, Foreground `#18181B` / `#52525B`, Primary Accent `#1D2A44` (차분한 네이비; 기계적 버밀리언/테라코타 배제), Border `#E4E2DD`

---

## 3. External MCP & Tool Integration Guidelines

When external Color or Palette MCPs (e.g., `color-palette-mcp`, Coolors MCP, Color Hunt MCP) are available in the agent harness:

### A. Recommended Tooling: `color-palette-mcp` (ppower-dev)
When the user specifies an explicit brand color (e.g. `#0A84FF`), domain-specific aesthetic (e.g. `ecommerce`, `dashboard`, `webrtc`), or natural language visual intent, invoke `color-palette-mcp` to generate dynamic 50~900 scales rather than falling back to static preset defaults:
- `generate_palette`: Generates base 50~900 scales and semantic colors from a single hex input.
- `extend_palette_for_project`: Tailors complementary palettes for domain types (`ecommerce`, `dashboard`, `webrtc`, `blog`).
- `generate_dynamic_colors`: Synthesizes project-tailored color tokens from natural language descriptions.
- `validate_accessibility`: Verifies WCAG AA/AAA contrast ratios between text and surface pairs.

### B. Deterministic Semantic Token Mapping
Map the 50~900 numeric palette output into `.design/tokens/colors.json` semantic slots:
- **Dark Theme Mapping (다크 모드 합의 시)**:
  - Canvas & Surfaces: `background.primary` = 950 (Canvas), `background.surface` = 900 (Surface Plate), `background.secondary` = 850 (Card Elevated).
  - Typography: `text.primary` = 50 (High contrast), `text.secondary` = 400 (Readable metadata), `text.muted` = 500 (Subtle hints).
  - Accent Affordance: `accent.primary` = 500 (Brand focal), `accent.hover` = 600 (Interactive active).
  - Structural Borders: `border.subtle` = 850, `border.default` = 800, `border.strong` = 700.
  - Status Indicators: Preserve standard semantic signals (`status.success`, `warning`, `error`, `info`).
- **Light Theme Mapping (라이트 모드 합의 시)**:
  - Canvas & Surfaces: `background.primary` = 50, `background.surface` = 100, `background.secondary` = 200.
  - Typography: `text.primary` = 900, `text.secondary` = 700, `text.muted` = 500.

### C. Validation & Hard-Guard Check
1. Verify body text contrast meets WCAG 2.1 AA (>= 4.5:1 against adjacent surface).
2. Directly populate `.design/tokens/colors.json`.
3. Run `python scripts/adapter.py --verify-spec` to ensure all required core token slots and hex formats pass validation.

