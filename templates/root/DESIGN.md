# System Design Principles

## Taste Configuration (1-10 Scale)
<!-- Architecture derived from leonxlnx/taste-skill (MIT License, Copyright (c) 2025 Leon Linz) -->
<!-- Tune these knobs to govern visual output without ambiguous prose -->
- `DESIGN_VARIANCE`: 5   # 1 (Strict/Symmetric) ~ 10 (Asymmetric/Experimental)
- `VISUAL_DENSITY`: 9    # 1 (Airy/Minimalist) ~ 10 (High-Density Views - Data Preservation Mandate)
- `MOTION_INTENSITY`: 4  # 1 (Static/Subtle) ~ 10 (Cinematic Spring Physics)

## 1. Single Source of Truth
- All visual values (colors, spacing, typography, radii) MUST be derived from `reference/tokens/`.
- Do NOT inject arbitrary hex codes or ad-hoc pixel values into component source code.

## 2. Aesthetic Constraints
- Read `reference/notes/do-not-copy.md` before initiating any frontend work.
- Strict avoidance of generic AI aesthetics (overly rounded cards, ambient neon glows, unsemantic step markers).
- Focus boldness in a single signature feature per page.

## 3. Data Preservation Mandate (High-Density Views: Density >= 8)
- **정의**: "핵심 데이터 무단 생략 금지 + 단위 면적당 유효 정보 수용 극대화"
- **미니멀리즘 오해 금지**: 고밀도(Density >= 8) 설정은 시각적 단순화를 위해 핵심 수치나 보조 메트릭을 임의로 생략하는 미니멀리즘이 아니다. 전문가용 도구(대시보드, 어드민, 트레이딩, 관제)에서 업무 판단에 직결되는 주요 지표(세부 분할 수치, 보조 상태값, 추세 인디케이터 등)의 임의 거세를 전면 금지한다.
- **복합 셀 수납 (Multi-Metric Compression)**: 단일 셀/카드 내에 Primary Metric + Visual Indicator + Secondary Context를 계층적으로 압축 수납하여 정보 손실 없이 공간을 극대화한다.
- **전폭 레이아웃 확장**: 고밀도 데이터 화면에서 `max-w-7xl`, `max-w-6xl` 등 인위적 컨테이너 폭 제한을 지양하고 `w-full` 전폭을 활용하여 좌우 공백 방치를 방지한다.
- **수치 우측 정렬 (Numeric Alignment)**: 모든 정량적 수치 데이터(헤더 및 셀)는 반드시 우측 정렬(`text-right`)을 적용하여 자릿수 가독성을 보장한다.
- **심각도/우선순위 우선 정렬 (Severity/Priority-First)**: 신속한 인지를 위해 목록 엔티티는 상태 위험도나 업무 우선순위(Critical -> Warning -> Normal 등)에 따른 정렬을 기본으로 지원한다.
