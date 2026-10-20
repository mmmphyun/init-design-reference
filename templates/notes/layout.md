# Layout Guidelines

> **원칙**: 아래 수치는 레이아웃 설계를 위한 **디자인 기본값(Contextual Defaults)**이다. 기존 제품의 레이아웃 체계나 사용자 레퍼런스가 있으면 그것을 우선하며, 콘텐츠의 실제 길이와 구조에 따라 간격과 폭을 조정한다.

## 1. General Grid & Breakpoints (Consumer / Content Views)
- **Mobile First**: Design starts from mobile viewport (`375px`).
- **Breakpoints**:
  - `sm`: `640px` (Tablets / Large phones)
  - `md`: `768px` (Tablets landscape)
  - `lg`: `1024px` (Small laptops)
  - `xl`: `1280px` (Standard desktop)
- **Container Max Width**: `1200px` centered with variable horizontal padding (`1rem` on mobile, `2rem` on desktop).
- **Section vertical spacing**: `4rem` to `6rem` (`py-16` to `py-24`).
- **Card internal padding**: `1.25rem` to `1.5rem` (`p-5` to `p-6`).

---

## 2. High-Density Data Layouts (Density >= 8)
*전문가용 고밀도 인터페이스(어드민, 대시보드, 데이터 뷰 등)에서는 소비재 랜딩 페이지의 중앙 고정폭 컨테이너와 과도한 여백 규칙을 지양합니다.*

- **Full-Bleed Viewport Utilization (`w-full`)**:
  - `max-w-1200px`, `max-w-7xl`, `max-w-6xl` 등 인위적 가로폭 제한을 지양한다.
  - 가로폭을 `w-full px-4` 또는 `px-6`로 100% 확장하여 좌우 불필요한 공백 방치를 차단한다.
- **Viewport Utilization & Vertical Balance (수직 공간 균형 — 조건부 기본값)**:
  - 고정 뷰포트 대시보드에서 상단 요약과 하단 테이블이 배치될 때, 테이블 영역이 지나치게 좁아지거나 불필요한 이중 스크롤이 생기지 않도록 수직 비율을 배분한다.
  - **적용 예외 조건**: 데이터 행 수가 적거나(예: 1-3건) 단일 설정·조회 화면인 경우, 빈 공간을 메우기 위해 행 높이나 패딩을 인위적으로 늘리지 않는다.
- **Compact Vertical Rhythm**:
  - 글로벌/섹션 헤더: `py-2.5 px-4` (높이 70px 이내)
  - 요약/필터 바: `py-1.5 px-3` (높이 35px 이내)
  - 요약 메트릭 카드: `p-3.5` (높이 120px 이내)
  - 컴포넌트 간 간격: `gap-2.5` ~ `gap-3` (Section py-16 금지)
- **Table Row Sizing & Padding**:
  - 고밀도 테이블 행 높이는 60px ~ 72px 사이로 설정하여 복합 수납(Primary + Indicator + Secondary Context)이 시각적으로 겹치지 않고 선명하게 노출되도록 한다.
