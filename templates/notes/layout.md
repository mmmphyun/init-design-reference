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

## 2. High-Density Enterprise Cockpit Layout (B2B / Density >= 8)
*미션 크리티컬 24/7 관제 화면에서는 B2C 랜딩 페이지의 중앙 정렬 컨테이너와 과도한 여백 규칙이 엄격히 금지됩니다.*

- **Full-Bleed Viewport Utilization (`w-full`)**:
  - `max-w-1200px`, `max-w-7xl`, `max-w-6xl` 등 인위적 가로폭 제한을 전면 금지한다.
  - 가로폭을 `w-full px-4` 또는 `px-6`로 100% 확장하여 좌우 160px 공백 방치를 원천 차단한다.
- **Zero Dead-Space Mandate (수직 뷰포트 완전 흡수)**:
  - 1440x900 단일 뷰포트 기준, 하단에 100px 이상의 빈 공간(Dead Space)을 방치하지 않는다.
  - 스크롤 0px을 달성하더라도 콘텐츠가 y≈715px에서 끊겨 20%의 빈 공간이 생기면, 테이블 행 높이(57px -> 66~72px)와 패딩, 폰트 크기로 수직 공간을 비례 환원하여 가독성을 극대화한다.
- **Compact Vertical Rhythm**:
  - 헤더: `py-2.5 px-4` (높이 70px 이내)
  - 클러스터 요약 바: `py-1.5 px-3` (높이 35px 이내)
  - 메트릭 카드: `p-3.5` (높이 120px 이내)
  - 컴포넌트 간 간격: `gap-2.5` ~ `gap-3` (Section py-16 금지)
- **Table Row Sizing & Padding**:
  - 관제 테이블 행 높이는 60px ~ 72px 사이로 설정하여 3단 복합 수납(Primary + Gauge + Secondary)이 숨 막히지 않고 선명하게 노출되도록 한다.
