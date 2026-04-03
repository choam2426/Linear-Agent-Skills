# Linear-CLI

Linear API 전체를 하나의 Python 스크립트로 래핑한, AI Agent에 최적화된 CLI입니다. OAuth, MCP, 외부 의존성 없이 동작합니다.

모든 AI 코딩 에이전트에서 사용 가능: [Claude Code](https://claude.com/claude-code), [Cursor](https://cursor.com), [Gemini CLI](https://github.com/google-gemini/gemini-cli), [Windsurf](https://windsurf.com), 또는 셸 명령을 실행할 수 있는 어떤 도구든.

## Linear MCP 서버 대신 이걸 쓰는 이유

- **OAuth 불필요** — 간단한 API 키만으로 동작
- **MCP 의존성 없음** — 단일 Python 스크립트로 실행, 별도 서버 불필요
- **어떤 AI Agent에서든 동작** — 특정 도구에 종속되지 않음. 셸 명령을 실행할 수 있는 Agent라면 바로 사용 가능.
- **토큰 효율적** — SKILL.md가 37개 커맨드를 ~500 토큰으로 한번에 제공하고, 기본 출력이 compact JSON.
- **파일 업로드 & 다운로드** — 로컬 파일 업로드 및 이슈 설명/댓글의 파일 다운로드 가능. Linear MCP 서버에는 파일 처리 기능이 없음.
- **크로스플랫폼** — Windows/macOS/Linux 지원

### Linear MCP 서버와 비교

| | Linear MCP 서버 | 이 플러그인 |
|---|---|---|
| 설정 | OAuth flow + MCP 서버 프로세스 | `.env`에 API 키 |
| 토큰 비용 (10회 호출, 5개 tool) | ~4,150 tok | ~2,300 tok (~45% 절감) |
| 파일 업로드 | 미지원 | `upload-file` → asset URL 반환 |
| 파일 다운로드 | 미지원 | `download-file`로 설명/댓글 파일 다운로드 |
| 출력 형식 | Verbose JSON | Compact JSON (~40% 절감) |
| 의존성 | MCP 런타임 | Python 표준 라이브러리만 |

## 설치

### 방법 1: 마켓플레이스에서 설치 (권장)

먼저 마켓플레이스를 등록합니다:

```
/plugin marketplace add choam2426/Linear-CLI
```

그런 다음 플러그인을 설치합니다:

```
/plugin install Linear-CLI@Linear-CLI
```

설치 범위를 지정할 수도 있습니다:

```bash
# 사용자 범위 (기본값, 모든 프로젝트에서 사용)
claude plugin install Linear-CLI@Linear-CLI

# 프로젝트 범위 (팀원과 공유, 버전 관리에 포함)
claude plugin install Linear-CLI@Linear-CLI --scope project

# 로컬 범위 (gitignore 처리, 나만 사용)
claude plugin install Linear-CLI@Linear-CLI --scope local
```

### 방법 2: 로컬에서 직접 실행 (Claude Code)

저장소를 클론한 뒤 플러그인 디렉토리를 지정하여 실행합니다:

```bash
git clone https://github.com/choam2426/Linear-CLI.git
claude --plugin-dir ./Linear-CLI
```

### 방법 3: 수동 복사 (모든 AI Agent에서 사용 가능)

스킬 디렉토리를 프로젝트에 복사합니다. 셸 명령을 실행할 수 있는 AI Agent라면 바로 사용 가능합니다:

```bash
git clone https://github.com/choam2426/Linear-CLI.git
cp -r Linear-CLI/plugins/claude/skills/ /path/to/your/project/.claude/skills/
```

**Cursor / Windsurf**의 경우, rules 파일에 CLI 경로와 SKILL.md 참조를 추가하세요.
**Gemini CLI**의 경우, 시스템 지시사항이나 GEMINI.md에 SKILL.md 내용을 포함하세요.

CLI 자체는 독립 실행 가능한 Python 스크립트입니다:
```bash
python scripts/linear_cli.py <command> [flags]
```

### API 키 설정

프로젝트 루트에 `.env` 파일을 생성하세요:

```
LINEAR_API_KEY=lin_api_your_key_here
```

키는 **Linear > Settings > API > Personal API keys**에서 발급할 수 있습니다.

### 설치 확인

설치가 완료되면 AI Agent가 CLI를 인식합니다. 다음과 같이 사용해 보세요:

- "Linear 팀 목록 보여줘"
- "나에게 할당된 이슈 보여줘"
- "Backend 팀에 이슈 만들어줘"

## 요구 사항

- Python 3.7+
- 외부 의존성 없음 (Python 표준 라이브러리만 사용)

## CLI 레퍼런스

### 이슈

| 커맨드 | 설명 |
|--------|------|
| `get-issue` | 식별자(예: PRJ-42) 또는 UUID로 이슈 상세 조회 |
| `list-issues` | 팀, 상태, 담당자, 라벨, 프로젝트, 우선순위로 이슈 검색/필터 |
| `create-issue` | 새 이슈 생성 |
| `update-issue` | 기존 이슈 수정 |
| `list-sub-issues` | 부모 이슈의 하위 이슈 목록 조회 |
| `add-sub-issue` | 기존 이슈를 하위 이슈로 연결 |
| `remove-sub-issue` | 하위 이슈 연결 해제 |

### 문서

| 커맨드 | 설명 |
|--------|------|
| `get-document` | ID로 문서 상세 조회 |
| `list-documents` | 전체 문서 목록 조회 |
| `create-document` | 새 문서 생성 (프로젝트, 이슈, 또는 팀 ID 필수) |
| `update-document` | 기존 문서 수정 |

### 프로젝트

| 커맨드 | 설명 |
|--------|------|
| `get-project` | 이름 또는 ID로 프로젝트 상세 조회 |
| `list-projects` | 팀, 상태, 리드로 프로젝트 목록/필터 |
| `save-project` | 프로젝트 생성 또는 수정 |

### 팀

| 커맨드 | 설명 |
|--------|------|
| `get-team` | 멤버, 상태, 라벨 포함 팀 상세 조회 |
| `list-teams` | 전체 팀 및 워크플로 상태 목록 조회 |

### 사용자

| 커맨드 | 설명 |
|--------|------|
| `get-user` | 이름, 이메일, ID, `--me`로 사용자 상세 조회 |
| `list-users` | 워크스페이스 사용자 목록 조회 (이름/이메일 검색) |

### 댓글

| 커맨드 | 설명 |
|--------|------|
| `list-comments` | 이슈의 댓글 목록 조회 |
| `save-comment` | 댓글 생성 또는 수정 |
| `delete-comment` | 댓글 삭제 |

### 라벨

| 커맨드 | 설명 |
|--------|------|
| `list-issue-labels` | 이슈 라벨 목록 조회 (워크스페이스 또는 팀) |
| `create-issue-label` | 새 이슈 라벨 생성 |
| `list-project-labels` | 프로젝트 라벨 목록 조회 |

### 워크플로

| 커맨드 | 설명 |
|--------|------|
| `get-issue-status` | ID 또는 팀으로 워크플로 상태 조회 |
| `list-issue-statuses` | 팀의 전체 워크플로 상태 목록 조회 |
| `save-issue-status` | 워크플로 상태 생성 또는 수정 |
| `delete-issue-status` | 워크플로 상태 아카이브 |
| `list-cycles` | 팀의 사이클(스프린트) 목록 조회 |

### 마일스톤

| 커맨드 | 설명 |
|--------|------|
| `get-milestone` | ID 또는 프로젝트로 마일스톤 조회 |
| `list-milestones` | 프로젝트의 마일스톤 목록 조회 |
| `save-milestone` | 마일스톤 생성 또는 수정 |

### 첨부파일 & 파일

| 커맨드 | 설명 |
|--------|------|
| `get-attachment` | ID로 첨부파일 상세 조회 |
| `create-attachment` | 이슈에 URL 첨부파일 추가 |
| `delete-attachment` | 첨부파일 삭제 |
| `upload-file` | 로컬 파일 업로드, 설명/댓글에 사용할 asset URL 반환 |
| `download-file` | 이슈 설명/댓글에 업로드된 파일 다운로드 (uploads.linear.app) |

## 프로젝트 구조

```
plugins/claude/skills/
└── linear-cli/
    ├── SKILL.md          # Claude Code용 CLI 레퍼런스
    └── scripts/
        └── linear_cli.py # CLI 구현
```

## 라이선스

MIT
