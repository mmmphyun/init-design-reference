# System Design Principles

## Requirement Recording Dials (보조 기록값, 1-10 Scale)
<!-- Architecture derived from leonxlnx/taste-skill (MIT License, Copyright (c) 2025 Leon Linz) -->
<!-- 주의: 아래 숫자는 합의된 요구사항을 요약하는 보조 기록값이다. 숫자를 색상·모서리·비대칭·애니메이션에 기계적으로 대응시키거나 화면을 숫자에 억지로 맞추지 마라. 사용자 목표, 기존 제품 패턴, 콘텐츠 구조, 시각 레퍼런스가 항상 우선한다. -->
- `DESIGN_VARIANCE`: 5   # 보조 메모: 기본 그리드 안정성을 유지하되 콘텐츠 성격에 맞춰 레이아웃 선택
- `VISUAL_DENSITY`: 7    # 보조 메모: 정보량과 여백의 균형 유지 (8 이상일 때만 고밀도 데이터 보존 규칙 활성화)
- `MOTION_INTENSITY`: 4  # 보조 메모: 상태 피드백 중심의 절제된 전환 유지

---

## 1. Hard Constraints (하드 제약 — 모든 화면에서 위반 금지)
- **Brand & Reference Precedence**: 사용자의 명시적 시각 요구사항, 레퍼런스, 기존 브랜드 가이드는 모든 기본값과 클리셰 휴리스틱보다 우선한다.
- **Single Source of Truth (Token Adherence)**: 색상, 간격, 타이포그래피, 반경은 `.design/tokens/`(또는 `reference/tokens/`)에서 참조하며, 컴포넌트 코드에 임의의 하드코딩 hex나 미정의 픽셀값을 주입하지 않는다.
- **Accessibility & Reduced Motion**: 본문 텍스트 대비 4.5:1 이상(WCAG 2.1 AA), 키보드 `:focus-visible` 링 노출, `@media (prefers-reduced-motion: reduce)` 대체 동작을 필수 보장한다.
- **Critical Data & Identifier Preservation**: 고유 ID, 계좌·주문 번호, 호스트·IP, 표준 측정 단위(`GiB`, `ms`, `USD` 등) 등 핵심 도메인 데이터를 임의로 생략하거나 `truncate`로 잘라내지 않는다.
- **Async 4-State Handling**: 원격 데이터를 조회하는 비동기 컴포넌트는 `Loading`, `Empty`, `Error`, `Populated` 상태를 누락 없이 처리한다.

---

## 2. Contextual Design Defaults (상황별 디자인 기본값 — 조건부 조정 가능)
아래 항목은 출발점 기본값이며, 화면의 콘텐츠 구조와 맥락에 맞지 않을 때는 예외 조건에 따라 조정한다.

- **간격 및 타이포그래피 스케일**:
  - **기본값**: `spacing.json`의 4px(0.25rem) 배수 간격과 컴포넌트당 3단계 이내의 글자 크기 위계를 사용한다.
  - **적용 예외 조건**: 데이터 테이블 내부의 조밀한 셀, 뱃지 내부 미세 정렬, 또는 에디토리얼/복합 문서 화면에서 정보 계층을 구분하기 위해 추가 타이포그래피 단계가 필요한 경우에는 화면 가독성에 맞춰 유연하게 조정한다.
- **카드 표면(Card Surface) 구분**:
  - **기본값**: 서로 다른 정보 그룹이나 독립 위젯을 분리할 때 `bg-surface` 카드를 사용한다.
  - **적용 예외 조건**: 동일 위계의 목록이나 단순 텍스트 섹션을 습관적으로 개별 카드로 쪼개지 않는다. 여백이나 단일 구분선(`divide-y`, `border-b`)만으로 그룹 구분이 충분하면 카드 래퍼를 제거한다.
- **수치 정렬 (Numeric Alignment)**:
  - **기본값**: 다중 행에서 자릿수와 크기를 세로로 비교해야 하는 정량 데이터 열(가격, 사용량, 비율 등)은 우측 정렬(`text-right`)을 적용한다.
  - **적용 예외 조건**: 단일 요약 지표, 텍스트와 결합된 문장형 수치, 또는 버전·코드·날짜처럼 크기 비교 대상이 아닌 숫자는 좌측 또는 맥락 정렬을 허용한다.
- **고밀도 데이터 화면 기본값 (`VISUAL_DENSITY >= 8` 또는 관제·트레이딩·어드민 뷰)**:
  - **기본값**: 핵심 보조 지표를 생략하지 않고 복합 수납하며, 전폭 레이아웃(`w-full`)과 위험도 우선 정렬(Critical -> Warning -> Normal)을 지원한다.
  - **적용 예외 조건**: 폼 입력 화면, 설정 페이지, 문서 열람 뷰처럼 가로 줄 길이가 길어지면 가독성이 떨어지는 화면에서는 `VISUAL_DENSITY`가 높더라도 적절한 최대 폭(`max-w-*`)을 유지한다.
