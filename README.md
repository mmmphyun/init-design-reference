# init-design-reference

[English](README.en.md) | 한국어

AI 코딩 에이전트(Google Antigravity, Claude Code, Cursor 등)의 UI 스타일 드리프트를 방지하는 디자인 레퍼런스 및 토큰 구조 스캐폴더.

## 1. 개발 배경 및 문제의식

### AI가 만드는 화면이 항상 똑같은 이유
LLM 에이전트에게 프론트엔드 UI 코드를 맡기면 예외 없이 익숙한 클리셰로 수렴합니다.
- 보라색·인디고 계열의 천편일률적인 그라디언트
- 둥근 모서리와 흐릿한 회색 그림자가 똑같이 적용된 SaaS 카드 나열
- 섹션 제목 위에 습관적으로 붙는 영문 대문자(`ALL-CAPS`) 트래킹 라벨
- 순서와 무관한 장식용 스텝 번호(`01`, `02`, `03`)
- 본문 텍스트 내 단일 단어 강조 및 접미 화살표(`→`) 남발

### 프롬프트 지시의 한계와 물리적 제약
프롬프트에 "깔끔하게 만들어줘", "모던한 느낌으로", "보라색 쓰지 마" 같은 정성적 지시를 아무리 적어도, 대화가 길어지거나 서브에이전트로 분기되는 순간 지침은 증발합니다. 결국 에이전트는 학습 데이터의 통계적 기본값으로 회귀합니다.

`init-design-reference`는 프로젝트 루트에 `/reference` 디렉토리를 구축해 **파일 시스템 기반 단일 진실 공급원(SSOT)**을 박제합니다.
- **금지 패턴 헌법 (`notes/do-not-copy.md`)**: Anthropic 공식 `frontend-design` 가이드라인의 안티패턴을 명문화하여 에이전트의 스타일 드리프트를 파일 시스템 수준에서 차단합니다.
- **디자인 토큰 (`tokens/*.json`)**: 색상, 간격, 타이포그래피, 모션을 구조화하여 에이전트가 임의의 hex 코드나 px 값을 하드코딩하지 못하도록 강제합니다.

### 이 토큰은 빌드 도구가 아닙니다
`tokens/*.json`은 CSS로 자동 변환되는 트랜스파일러나 빌드 플러그인이 아닙니다.
**에이전트가 컴포넌트를 작성할 때 임의의 값을 하드코딩하지 않고 읽어서 준수해야 하는 규격서**입니다.

## 2. 주요 기능 및 디렉토리 구조

- **완전 분리형 아키텍처**: 스크립트 내부 하드코딩 문자열 제로. 모든 템플릿은 순수 Markdown과 JSON으로 보존되어 읽기 쉽고 프로젝트별 커스텀이 자유롭습니다.
- **Anthropic 최신 클리셰 회피 규칙 반영**: SaaS 카드 키트, 유사 블랙 남용, 히어로 통계 기본값, 모노스페이스 오용 등 최신 안티패턴 방어 규칙 번들링.
- **한/영 혼용 타이포그래피 스택**: Pretendard, Space Grotesk, JetBrains Mono 및 시스템 폰트 폴백을 기본 지원하여 기준선 왜곡과 폰트 깨짐을 방지합니다.
- **안전한 멱등성**: 이미 존재하는 사용자 커스텀 파일은 건드리지 않습니다 (`--force` 지정 시에만 덮어쓰기).
- **Git 바이너리 오염 방지**: 고화질 스크린샷과 웹폰트 바이너리가 레포에 커밋되지 않도록 `.gitignore` 규칙을 자동 설정합니다.
- **스타일 엔진 감지**: 프로젝트의 `package.json`을 분석하여 Tailwind v3/v4 및 CSS 연동 가이드를 출력합니다.

```
reference/
  screenshots/          # UI 목표 캡처 보관소 (.gitignore 적용)
  notes/
    do-not-copy.md      # AI 클리셰 금지 헌법 (SaaS 카드, ALL-CAPS 라벨 등 차단)
    layout.md           # 반응형 중단점 및 여백 리듬
    interaction.md      # 트랜지션 타이밍 및 모달 포커스 트랩 규칙
    visual-direction.md # 표면 계층 및 시그니처 시각 요소 원칙
    accessibility.md    # WCAG 2.1 AA 명도 대비 준수 기준
  tokens/
    colors.json         # 표면, 텍스트, 액센트 16진수 색상값
    spacing.json        # rem 기반 4px/8px 수직·수평 여백 리듬
    typography.json     # 한/영 혼용 폰트 스택 및 역할별 타이포 스케일
    radii.json          # 모서리 곡률 토큰
    shadows.json        # 표면 깊이 토큰
    motion.json         # 애니메이션 지속 시간 및 easing 곡선
  fonts/
    README.md           # 로컬 웹폰트 배치 및 최적화 가이드
    font-license.md     # 상업적 이용 및 라이선스 고지
    preview.html        # 한/영 폰트 렌더링 검증용 인터랙티브 테스트 페이지
  DESIGN.md             # 코어 디자인 시스템 헌법
  COMPONENTS.md         # 컴포넌트 4대 상태(Loading, Empty, Error, Populated) 필수 구현 규약
  REVIEW_CHECKLIST.md   # 커밋 전 UI 자가 검증 체크리스트
```

## 3. 설치 및 에이전트 등록

Git Clone 없이 터미널에서 한 줄 명령어로 즉시 사용자의 에이전트 전역 스킬 디렉토리에 설치할 수 있습니다.

### Windows (PowerShell)
```powershell
# 기본 설치: Google Antigravity ($env:USERPROFILE/.gemini/config/skills/init-design-reference)
irm https://raw.githubusercontent.com/mmmphyun/init-design-reference/main/install.ps1 | iex

# Claude Code 또는 Cursor에 설치 시
.\install.ps1 -Agent claude
.\install.ps1 -Agent cursor

# 사용자 지정 디렉토리에 설치 시
.\install.ps1 -TargetDir "C:/path/to/skills/init-design-reference" -Force
```

### macOS / Linux (Bash)
```bash
# 기본 설치: Google Antigravity (~/.gemini/config/skills/init-design-reference)
curl -fsSL https://raw.githubusercontent.com/mmmphyun/init-design-reference/main/install.sh | bash

# Claude Code 또는 Cursor에 설치 시
curl -fsSL https://raw.githubusercontent.com/mmmphyun/init-design-reference/main/install.sh | bash -s -- --agent claude
curl -fsSL https://raw.githubusercontent.com/mmmphyun/init-design-reference/main/install.sh | bash -s -- --agent cursor
```

### 에이전트별 기본 설치 경로 안내

| 에이전트 | OS | 설치 경로 |
| :--- | :--- | :--- |
| **Google Antigravity** | Windows | `$env:USERPROFILE/.gemini/config/skills/init-design-reference` |
| **Google Antigravity** | Linux/macOS | `~/.gemini/config/skills/init-design-reference` |
| **Claude Code** | Windows | `$env:USERPROFILE/.claude/skills/init-design-reference` |
| **Claude Code** | Linux/macOS | `~/.claude/skills/init-design-reference` |
| **Cursor** | All | `~/.cursor/skills/init-design-reference` (또는 프로젝트 로컬) |

## 4. 사용 방법 (실행 트리거)

복잡한 설정 없이 에이전트 대화창에서 자연어로 요청하면 됩니다.

### 에이전트 대화창
프로젝트 루트에서 에이전트에게 다음과 같이 지시하세요:
> "UI 디자인 레퍼런스 초기화해줘"
> "디자인 토큰과 금지 규칙 구조 잡아줘"
> "/init-design-reference"

에이전트가 스킬을 인식하고 `adapter.py`를 호출하여 프로젝트 루트에 `/reference` 구조를 자동으로 스캐폴딩합니다.

### 수동 CLI 실행
에이전트 없이 터미널에서 직접 파일 구조를 생성하고 싶을 때:
```powershell
# 기본 reference 디렉토리에 생성
python "scripts/adapter.py" "reference"

# 기존 파일 강제 덮어쓰기
python "scripts/adapter.py" "reference" --force
```

## 5. 권장 개발 워크플로우

1. **스캐폴딩**: 에이전트에게 요청하여 프로젝트 루트에 `/reference` 뼈대와 기본 금지 규칙(`notes/do-not-copy.md`)을 생성합니다.
2. **토큰 구체화**: `frontend-design` 스킬을 함께 활용하여 본 프로젝트의 성격에 맞게 `tokens/colors.json`과 타이포그래피 역할을 조율합니다.
3. **UI 구현**: 컴포넌트를 작성할 때 에이전트에게 반드시 `/reference`를 SSOT로 참조하여 코딩하도록 지시합니다.
4. **검증**: Git 커밋 전 `reference/REVIEW_CHECKLIST.md` 항목을 점검하여 클리셰나 접근성 위반이 없는지 확인합니다.

## 기여 안내

버그 제보, 신규 AI 클리셰 제안, 프레임워크 감지 확장 등 기여 방법은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참고하세요.

## 라이선스

[MIT License](LICENSE).
