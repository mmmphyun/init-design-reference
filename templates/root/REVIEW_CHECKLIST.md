# UI Review & Verification Checklist
<!-- Derived from Superfuture/design-review (MIT License), addyosmani/web-quality-skills (MIT License), plugin87/ux-ui-agent-skills (MIT License), pbakaus/impeccable (Apache-2.0), and vercel-labs/web-interface-guidelines (MIT License) -->

Complete this checklist prior to submitting or committing UI code changes.

---

## 1. Pre-Commit Verification Checklist

- [ ] **Token Adherence**: Colors, spacing, and typography conform strictly to `.design/tokens/` (or `reference/tokens/`).
- [ ] **Anti-Cliché Audit**: Verified absence of prohibited patterns in `.design/notes/do-not-copy.md`.
- [ ] **Deterministic Lint**: `python scripts/lint_ui.py <src>` returns 0 errors (covers hardcoded hex, unsemantic clickables, missing icon button labels, paste-blocking, unlabeled form controls, zoom disable).
- [ ] **Deterministic DOM UX Audit**: `python scripts/capture_ui.py` returns 0 runtime errors and 0 deterministic UX errors in `.design/screenshots/audit/ux_audit_receipt.json`:
  - [ ] Target size: all interactive targets >= 24x24 CSS px (WCAG 2.2 SC 2.5.8), mobile touch targets >= 44x44 CSS px recommended.
  - [ ] Rendered contrast: computed alpha-composited contrast >= 4.5:1 (normal text) and >= 3.0:1 (large text).
  - [ ] Reflow & overflow: no horizontal scrollbar or content overflow at 1440px or 375px (`scrollWidth <= clientWidth`).
- [ ] **Responsive Breakpoints**: Verified visual integrity at `375px` (mobile) and `1440px` (desktop).
- [ ] **Multilingual Typography**: Korean and English mixed strings render without baseline distortion or font clipping.
- [ ] **Hobson 4-State Completeness**: Verified `Loading`, `Empty`, `Error`, and `Populated` states on all dynamic data components.
- [ ] **Performance & Motion**: Spatial transitions restricted to GPU-accelerated properties (`transform`, `opacity`, `filter`); state transitions restricted to targeted paint properties (`color`, `background-color`, `border-color`, `box-shadow`); micro-interaction duration <= 350ms; strict `prefers-reduced-motion` compliance.
- [ ] **Critical Data Integrity & Functional Visibility (High-Density / Enterprise)**:
  - [ ] Zero truncation on critical domain identities (ID, Code, Key, Host/IP, Account fully visible).
  - [ ] Functional indicator/gauge bar height >= 6px (`h-1.5`) with high-contrast alert states.
  - [ ] Standard units enforced (e.g., `GiB`, `cores`, `ms`, `USD`, `Mbps`), no informal abbreviations.
  - [ ] Adaptive vertical budget: no dead space > 100px on fixed viewports; rows vertically balanced.
  - [ ] Critical state rows have elevated prominence (left border indicator or tint).
  - [ ] Production view isolated from development state-simulation controls.

---

## 2. Contextual Visual & UX Heuristic Review (캡처 기반 맥락·위계·사용성 자가진단)

> **주의**: 정적 린트(`lint_ui.py`) 0 에러나 영수증 통과를 디자인 완성으로 간주하지 마라. Gate 4에서 캡처된 실제 렌더링 화면을 보고 아래 5대 시각 질문과 UX 휴리스틱·페르소나 Red Flag를 스스로 점검한다.

### 2-1. 5대 시각 위계 점검 질문
1. **초점과 핵심 작업 (Focal Point & Primary Task)**:
   - 화면을 열었을 때 첫 시선이 사용자의 핵심 작업이나 가장 중요한 데이터로 즉시 향하는가, 아니면 주변 장식·배지·보조 카드에 분산되는가?
2. **콘텐츠 기반 위계 (Content-Driven Hierarchy)**:
   - 실제 콘텐츠의 양과 중요도 차이가 영역 크기, 여백, 타이포그래피 대비에 반영되었는가, 아니면 중요도가 다른 항목들이 모두 똑같은 크기의 박스 안에 평평하게 나열되어 있는가?
3. **반복 패턴 억제 (Unjustified Repetition)**:
   - 동일한 모양의 카드, 상단 작은 라벨(Eyebrow), 상태 배지, 아이콘이 정보 구분에 실질적 도움 없이 관성적으로 반복되고 있지 않은가?
4. **색상과 장식의 정보성 (Functional Color & Ornament)**:
   - 강조색(Accent)과 테두리·배경 처리가 상태나 중요도를 전달하는가, 아니면 빈약한 구조를 가리기 위해 화면을 꾸미기만 하는가?
5. **도메인 및 사용자 적합성 (Product & User Fit)**:
   - 이 화면의 밀도, 톤, 조작 방식이 해당 제품과 실제 사용 환경에 자연스러운가, 아니면 다른 장르의 템플릿을 억지로 이식한 느낌인가?

### 2-2. UX 휴리스틱 & 인지 부하 (Nielsen & Cognitive Load)
1. **인지 부하 (Cognitive Load)**:
   - 단일 화면이나 카드 안에 비그룹화된 선택지·버튼이 4개 이상 경쟁하여 결정을 지연시키고 있지 않은가?
2. **오류 방지 및 복구 (Error Prevention & Recovery)**:
   - 파괴적 작업(삭제, 취소, 초기화)에 확인 모달이나 실행 취소(Undo) 창이 존재하는가?
   - 에러 상태 메시지가 단순 문제 고발에 그치지 않고 구체적인 복구 액션(재시도 버튼, 입력 수정 안내)을 제시하는가?
3. **사용자 제어 및 탈출 (User Control & Escape)**:
   - 열린 모달, 드로어, 팝오버를 ESC 키나 명확한 닫기/취소 버튼으로 즉시 벗어날 수 있는가?

### 2-3. 도메인 매핑 가상 페르소나 Red Flag 점검 (Impeccable Personas)
- **대시보드 / 어드민 / 분석 뷰 (`Alex` 파워 유저 & `Sam` 접근성 사용자)**:
  - 마우스 호버에만 의존해 중요한 데이터나 액션이 숨겨져 있지 않은가?
  - 키보드 Tab 키만으로 데이터 테이블 및 필터 조작이 논리적 순서로 동작하는가?
- **랜딩 / 쇼케이스 / 온보딩 (`Jordan` 첫 방문자 & `Casey` 모바일 사용자)**:
  - 3초 이내에 제품의 핵심 가치와 가장 먼저 눌러야 할 주 액션(Primary CTA)이 한눈에 들어오는가?
  - 모바일 뷰포트에서 주요 조작부가 하단 엄지 영역(Thumb Zone)에 배치되었는가?
- **폼 / 결제 / 데이터 입력 (`Riley` 엣지케이스 테스터 & `Casey` 모바일 사용자)**:
  - 0건(Empty) 또는 수천 건의 데이터, 극단적으로 긴 텍스트 입력 시 레이아웃이 깨지지 않는가?
  - 모바일에서 입력 폼 터치 시 불필요한 확대나 가로 스크롤 흔들림이 발생하지 않는가?

---

## 3. Diagnostic Feedback & Self-Correction Protocol (자가 진단 및 개선 가이드)
*(결함 발생 시 다이얼 숫자를 기계적으로 올리거나 레이아웃을 즉시 뒤엎지 말고, 캡처 화면과 영수증에서 원인을 먼저 진단한 뒤 가장 적은 수정으로 해결한다)*

| 진단 항목 / 결함 유형 | 선행 진단 항목 (확인할 원인) | 최소 수정 및 자가 개선 처방 |
| :--- | :--- | :--- |
| **`ux_audit_receipt.json` FAIL (Target Size)** | - 인터랙티브 요소 패딩 부족 또는 인라인 축소 | - 요소 패딩(`py-2 px-3`) 또는 `min-h-[36px]` (모바일 `min-h-[44px]`) 부여 |
| **`ux_audit_receipt.json` FAIL (Contrast)** | - 배경과 텍스트 간 명도 대비 미달 (4.5:1 미만) | - `.design/tokens/colors.json` 명도 조정 후 `python scripts/adapter.py --bridge-only` 재생성 |
| **`ux_audit_receipt.json` FAIL (Overflow)** | - 전폭 레이아웃에서 고정 너비(`w-[600px]`) 또는 음수 마진 | - `max-w-full`, `overflow-x-hidden`, `min-w-0` 적용 및 플렉스 랩(`flex-wrap`) 처리 |
| **"지루하고 AI가 만든 것 같아"** | 1. 모든 섹션이 동일한 둥근 카드·배지·상단 영문 라벨로 반복되는가?<br>2. 중요도가 다른 정보가 같은 크기와 균일한 간격으로 평평하게 나열되었는가?<br>3. 맥락 없는 기본 강조색이나 장식 요소가 들어갔는가? | - **금지**: 원인 진단 없이 비대칭 그리드, 큰 색상 블록, 애니메이션, 인위적 시그니처 요소를 추가하지 마라.<br>- **처방**: 불필요한 카드 테두리와 반복 배지·라벨을 걷어내고, 핵심 영역과 보조 영역의 크기·대비 차이를 벌려 정보 위계를 세운다. |
| **"너무 휑하고 빈약해 보여"** | 1. 사용자가 판단에 필요한 보조 지표나 컨텍스트가 생략되었는가?<br>2. 콘텐츠 양에 비해 컨테이너나 카드 내부 패딩이 과도한가? | - 빈자리를 장식 아이콘으로 채우지 말고, 실제 업무에 필요한 보조 데이터·상태 맥락을 노출하거나 불필요한 외곽 여백을 줄인다. |
| **"너무 장난감 같아 / 가벼워 보여"** | 1. 도메인 성격에 비해 모서리 곡률(`radii`)이나 그림자가 과장되었는가?<br>2. 포인트 색상이 너무 많은 영역에 남발되었는가? | - 모서리 반경을 줄이고(`radii.json`), 강조색을 핵심 액션과 임계 상태에만 남긴 뒤 나머지는 무채색 표면 대비로 정리한다. |
| **"글자가 눈에 안 들어와 / 가독성 불량"** | 1. 배경과 텍스트 명도 대비가 부족하거나 줄 길이가 너무 긴가?<br>2. 제목·본문·보조 텍스트의 크기와 굵기 차이가 모호한가? | - `colors.json`의 텍스트-표면 대비를 높이고, 불필요한 대문자 자간 확장(`uppercase tracking-widest`)을 제거하며 본문 줄 길이를 조정한다. |
| **"너무 어지럽고 복잡해"** | 1. 카드 안에 카드가 중첩되어 테두리 선이 겹쳐 보이는가?<br>2. 한 화면에 너무 많은 글자 크기와 색상이 경쟁하는가? | - 내부 중첩 테두리를 제거하고 배경 톤 차이(`bg-background` vs `bg-surface`)로만 구분하며, 부차적 액션은 보조 메뉴로 정리한다. |
