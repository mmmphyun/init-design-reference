# Prohibited Patterns (Do Not Copy)

Source: Derived from Anthropic frontend-design guidelines & Production Standards.

## 1. AI Cliché Aesthetics
- **No SaaS Card Kit**: Do NOT chop content into identical rounded cards with uniform border-radius and soft grey drop-shadows (`rgba(0, 0, 0, 0.1)`).
- **No Warm-Clay Defaults**: Do NOT use warm cream (`#F4F1EA`) paired with high-contrast serif display and terracotta/warm-clay accents (`#D97757`) unless explicitly requested.
- **No Neon Monotones**: Do NOT use near-black backgrounds accented solely by a single bright acid-green or vermilion element.
- **No Broadsheet Mimicry**: Do NOT use dense hairline newspaper layouts with zero border-radius unless fitting the editorial brief.
- **No Tinted Near-Black**: Do NOT substitute pure black with tinted near-black (`#0B0B0B`, `#111`) as a generic default.
- **No Decorative Gradient Washes**: Gradients must encode state or depth, never purely arbitrary background fills.
- **No Hero Stats Default**: Do NOT default to a big number + small label + supporting stats + gradient accent layout unless justified by the brief.

## 2. Template Chrome & Typography Tells
- **No Tracked-Out Eyebrows**: Do NOT place small uppercase labels with wide letter-spacing (`ALL-CAPS`) directly above every single heading.
- **No Redundant Typographic Labels**: Do NOT prepend decorative category labels above content when context is already self-evident.
- **No Monospace Data Labels**: Do NOT reach for monospace fonts for small UI labels, badges, or meta tags unless displaying actual code or tabular numbers.
- **No Middle-Dot Meta Strings**: Avoid repetitive `Item A · Item B · Item C` meta strings across cards.
- **No Spaced Em Dash Labels**: Avoid labels structured as `CATEGORY — description`.
- **No Suffix Arrows**: Do NOT append `→` or `->` to every link and button.
- **No Single-Word Color Highlights**: Do NOT accent just a single word in a headline with italic, bold, or accent color.
- **Line Length Constraints**: Keep body text lines strictly under 80 characters for optimal readability.

## 3. Structural & Motion Tells
- **No Decorative Step Numbers**: Do NOT place numbered markers (`01`, `02`, `03`) next to content unless it is a genuinely ordered process or timeline.
- **No Universal Scroll Entrances**: Avoid cascading fade-and-slide-up animations across every section; use motion only for direct user interactions.
- **Respect Reduced Motion**: Always provide `@media (prefers-reduced-motion: reduce)` fallbacks.

## 4. UI Copywriting & State Rules
- **Active Voice CTAs**: Name buttons by immediate outcome ("Save changes", "Create project"), not vague system commands ("Submit").
- **Directional Errors**: Explain precisely what went wrong and provide an actionable fix without emotional apologies.
- **Actionable Empty States**: An empty screen must guide the user to their first action, never remain dead space.

## 5. Mission-Critical Telemetry & Cockpit Tells (B2B 관제 안티패턴)
- **No Infrastructure Truncation (Zero-Truncation Policy)**: 인프라 식별자(가용영역 AZ, 데이터센터 위치, 호스트명, 내부 IP)에 `truncate` 클래스나 고정폭(`max-w-[140px]`)을 적용하여 `(부산 D...)`처럼 말줄임표로 자르는 행위를 엄격히 금지한다. 재해복구(DR) 및 망 분리 장애 시 물리적 위치 오판은 치명적 장애로 직결된다. 툴팁 호버를 요구하지 말고 전문을 온전하게 노출하라.
- **No Anemic Slender Gauges (Preattentive Alert Failures)**: 24/7 관제 게이지/프로그레스 바를 1-2px 수준(`h-0.5`, `h-1`)의 극세선으로 축소하지 마라. 심야 온콜 및 4K 월 모니터 관제 시 주변 시야(Peripheral vision)로 임계치(적색)/주의(황색)를 0.1초 만에 감지할 수 있도록 최소 6px(`h-1.5` 이상) 두께와 뚜렷한 색상 대비를 보장하라.
- **No Informal Unit Abbreviations**: 메모리 및 스토리지 규격 단위(`GiB`, `코어`)를 `G`, `C` 등으로 임의 축약하지 마라. OOM(Out of Memory) 한계 계산 시 10진수(GB)와 2진수(GiB) 간 혼선을 방지하기 위해 정식 표준 단위(`GiB`, `MiB`, `cores`)를 명기하라.
- **No Repetitive Decorative Glyphs**: 테이블 행마다 동일한 장식용 아이콘(서버 랙 아이콘 7회 반복 등)을 기계적으로 복제하지 마라. 인지 부하만 가중시키는 시각 노이즈다.
- **No Production Canvas Demo Clutter**: 디자인 리뷰/개발용 4-State 시뮬레이션 토글 버튼을 프로덕션 관제 헤더에 상시 노출하지 마라. 온콜 엔지니어의 시야와 뷰포트를 잠식하며 오조작 위험을 유발한다.
- **No Neglected Critical Prominence**: 임계(Critical) 상태에 도달한 노드를 일반 정상 행과 동일한 시각적 무게로 방치하지 마라. 좌측 굵은 강조선(`border-l-2 border-status-error`) 또는 미세한 배경 틴트를 부여하여 첫 시선 스캔에서 1순위로 포착되도록 하라.
