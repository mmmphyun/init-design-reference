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

## 5. Critical Data Integrity & Functional Visibility (고밀도·전문가 인터페이스 안티패턴)
- **No Critical Identifier Truncation (Zero-Truncation Policy)**: 핵심 도메인 식별자(고유 ID, 계좌/주문/트랜잭션 식별자, 호스트/IP, 코드, 모델명 등)에 `truncate` 클래스나 임의 고정폭을 적용하여 말줄임표(`...`)로 자르는 행위를 엄격히 금지한다. 전문 식별자 절단은 운영·거래·관제 중 식별 오류와 치명적 사고로 직결된다. 호버 툴팁에 의존하지 말고 전문을 온전하게 노출하거나 자연스러운 줄바꿈/동적 폭을 보장하라.
- **No Ineffective Slender Indicators (Preattentive Visibility Failures)**: 상태·진행률·소비량·잔여량을 나타내는 기능성 인디케이터/프로그레스 바를 1-2px 수준(`h-0.5`, `h-1`)의 극세선으로 축소하지 마라. 미니멀리즘을 핑계로 지표의 가시성을 훼손해서는 안 되며, 주변 시야(Peripheral vision)로도 위험/정상 상태를 즉시 감지할 수 있도록 유효 두께(최소 6px, `h-1.5` 이상)와 뚜렷한 색상 대비를 보장하라.
- **No Non-standard Metric Abbreviations**: 측정 단위나 통화·수량 단위를 임의로 단일 알파벳으로 축약하지 마라. 계산 오차와 단위 혼선을 방지하기 위해 정식 표준 규격 단위(`GiB`, `GB`, `ms`, `USD`, `EA` 등)를 명기하라.
- **No Repetitive Decorative Glyphs**: 테이블 행이나 반복 리스트마다 문맥 정보가 없는 동일한 장식용 아이콘을 기계적으로 복제 배치하지 마라. 정보 밀도를 떨어뜨리고 시각 노이즈를 유발한다.
- **No Production Canvas Demo Clutter**: 개발/디자인 검증용 목업 상태 전환 컨트롤(State simulation pills 등)을 실제 인터페이스 헤더나 운영 뷰포트에 방치하지 마라. 유효 작업 공간을 잠식하고 실제 인터랙션과 혼선을 유발한다.
- **No Neglected Critical State Prominence**: 임계(Critical)·에러·경고 상태에 도달한 항목을 정상(Normal) 항목과 동일한 시각적 무게로 방치하지 마라. 시각적 인지 위계(좌측 강조선, 배경 틴트, 배지 등)를 부여하여 단일 스캔에서 즉시 포착되도록 하라.
