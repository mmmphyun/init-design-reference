# Layout Guidelines

## 1. General Grid & Breakpoints (Consumer / Editorial)
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
- **Zero Dead-Space Mandate (수직 뷰포트 완전 흡수 및 Adaptive Budgeting)**:
  - 1440x900 등 단일 고정 뷰포트 기준, 하단에 100px 이상의 빈 공간(Dead Space)을 방치하지 않는다.
  - 스크롤 0px을 달성하더라도 콘텐츠가 조기에 끊겨 대량의 빈 공간이 생기면, 테이블 행 높이(60~72px)와 패딩, 폰트 크기로 수직 공간을 비례 환원하여 가독성과 공간 활용을 극대화한다.
- **Compact Vertical Rhythm**:
  - 글로벌/섹션 헤더: `py-2.5 px-4` (높이 70px 이내)
  - 요약/필터 바: `py-1.5 px-3` (높이 35px 이내)
  - 요약 메트릭 카드: `p-3.5` (높이 120px 이내)
  - 컴포넌트 간 간격: `gap-2.5` ~ `gap-3` (Section py-16 금지)
- **Table Row Sizing & Padding**:
  - 고밀도 테이블 행 높이는 60px ~ 72px 사이로 설정하여 복합 수납(Primary + Indicator + Secondary Context)이 시각적으로 겹치지 않고 선명하게 노출되도록 한다.
