# System Design Principles

## Taste Configuration (1-10 Scale)
<!-- Architecture derived from leonxlnx/taste-skill (MIT License, Copyright (c) 2025 Leon Linz) -->
<!-- Tune these knobs to govern visual output without ambiguous prose -->
- `DESIGN_VARIANCE`: 5   # 1 (Strict/Symmetric) ~ 10 (Asymmetric/Experimental)
- `VISUAL_DENSITY`: 9    # 1 (Airy/Minimalist) ~ 10 (Information-Dense Cockpit - Data Preservation Mandate)
- `MOTION_INTENSITY`: 4  # 1 (Static/Subtle) ~ 10 (Cinematic Spring Physics)

## 1. Single Source of Truth
- All visual values (colors, spacing, typography, radii) MUST be derived from `reference/tokens/`.
- Do NOT inject arbitrary hex codes or ad-hoc pixel values into component source code.

## 2. Aesthetic Constraints
- Read `reference/notes/do-not-copy.md` before initiating any frontend work.
- Strict avoidance of generic AI aesthetics (overly rounded cards, ambient neon glows, unsemantic step markers).
- Focus boldness in a single signature feature per page.

## 3. Data Preservation Mandate (High-Density Cockpit: Density >= 8)
- **정의**: "정보 생략 금지 + 단위 면적당 텔레메트리 수용 극대화"
- **미니멀리즘 오해 금지**: 고밀도(Density >= 8)는 정보 생략이나 여백 확장이 아니다. 24/7 관제 도구로서 Load average(1m/5m/15m), Swap margin, Rx/Tx split, 스파크라인 등 핵심 커널/인프라 텔레메트리 생략을 전면 금지한다.
- **복합 셀 수납 (Multi-Metric Cell)**: 단일 셀/카드 내에 Primary Metric + Slim Gauge + Secondary Metric(Load avg, Swap, Rx/Tx)을 압축 수납하여 정보 손실 없이 공간을 극대화한다.
- **전폭 레이아웃 확장**: B2B 관제 화면에서 `max-w-7xl`, `max-w-6xl` 등 인위적 컨테이너 폭 제한을 금지하고 `w-full` 전폭을 활용하여 좌우 공백 방치를 방지한다.
- **수치 우측 정렬 (Numeric Alignment)**: 모든 정량적 수치 데이터(헤더 및 셀)는 반드시 우측 정렬(`text-right`)을 적용하여 자릿수 가독성을 보장한다.
- **심각도 우선 정렬 (Severity-First)**: 장애 인지 시간 단축을 위해 인프라 노드는 상태 심각도순(Critical -> Warning -> Normal -> Offline)으로 우선 정렬한다.
