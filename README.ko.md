# Claude Linear Skills

Linear MCP 서버를 네이티브 GraphQL API 호출로 대체하는 [Claude Code](https://claude.com/claude-code) 스킬 모음입니다. OAuth나 MCP 설정 없이 Linear API 키만 있으면 됩니다.

## Linear MCP 서버 대신 이걸 쓰는 이유

- **OAuth 불필요** — 간단한 API 키만으로 동작
- **MCP 의존성 없음** — 순수 Python으로 실행, 별도 서버 불필요
- **완전한 커버리지** — Linear MCP 도구 전체를 대체하는 30개 스킬
- **커스터마이징 가능** — 워크플로에 맞게 GraphQL 쿼리를 자유롭게 수정

## 설치

### 방법 1: 마켓플레이스에서 설치 (권장)

먼저 마켓플레이스를 등록합니다:

```
/plugin marketplace add choam/claude-linear-skills
```

그런 다음 플러그인을 설치합니다:

```
/plugin install claude-linear-skills@claude-linear-skills
```

설치 범위를 지정할 수도 있습니다:

```bash
# 사용자 범위 (기본값, 모든 프로젝트에서 사용)
claude plugin install claude-linear-skills@claude-linear-skills

# 프로젝트 범위 (팀원과 공유, 버전 관리에 포함)
claude plugin install claude-linear-skills@claude-linear-skills --scope project

# 로컬 범위 (gitignore 처리, 나만 사용)
claude plugin install claude-linear-skills@claude-linear-skills --scope local
```

### 방법 2: 로컬에서 직접 실행

저장소를 클론한 뒤 플러그인 디렉토리를 지정하여 실행합니다:

```bash
git clone https://github.com/choam/claude-linear-skills.git
claude --plugin-dir ./claude-linear-skills
```

### 방법 3: 수동 복사

스킬 디렉토리를 프로젝트에 직접 복사합니다:

```bash
cp -r skills/ /path/to/your/project/skills/
```

### API 키 설정

설치 방법과 관계없이 Linear API 키가 필요합니다. 프로젝트 루트에 `.env` 파일을 생성하세요:

```
LINEAR_API_KEY=lin_api_your_key_here
```

키는 **Linear > Settings > API > Personal API keys**에서 발급할 수 있습니다.

### 설치 확인

설치가 완료되면 Claude Code가 자동으로 스킬을 인식합니다. 다음과 같이 사용해 보세요:

- "Linear 팀 목록 보여줘"
- "나에게 할당된 이슈 보여줘"
- "Backend 팀에 이슈 만들어줘"

## 요구 사항

- Python 3.7+
- 외부 의존성 없음 (Python 표준 라이브러리만 사용)

## 스킬 레퍼런스

### 기본 도구

| 스킬 | 설명 |
|------|------|
| `linear-api` | 기본 GraphQL API 도구. 다른 모든 스킬이 이 스크립트를 사용합니다. |

### 이슈

| 스킬 | 설명 |
|------|------|
| `linear-get-issue` | 식별자(예: SCE-1) 또는 UUID로 이슈 상세 조회 |
| `linear-list-issues` | 팀, 상태, 담당자, 라벨 등으로 이슈 검색/필터 |
| `linear-create-issue` | 새 이슈 생성 |
| `linear-update-issue` | 기존 이슈 수정 |

### 문서

| 스킬 | 설명 |
|------|------|
| `linear-get-document` | ID 또는 슬러그로 문서 상세 조회 |
| `linear-list-documents` | 문서 목록 조회 (프로젝트별 필터 가능) |
| `linear-create-document` | 새 문서 생성 |
| `linear-update-document` | 기존 문서 수정 |

### 프로젝트

| 스킬 | 설명 |
|------|------|
| `linear-get-project` | 이름, ID, 슬러그로 프로젝트 상세 조회 |
| `linear-list-projects` | 팀, 상태, 라벨 등으로 프로젝트 목록/필터 |
| `linear-save-project` | 프로젝트 생성 또는 수정 |

### 팀

| 스킬 | 설명 |
|------|------|
| `linear-get-team` | 이름, 키, UUID로 팀 상세 조회 |
| `linear-list-teams` | 전체 팀 및 워크플로 상태 목록 조회 |

### 사용자

| 스킬 | 설명 |
|------|------|
| `linear-get-user` | 이름, 이메일, ID, "me"로 사용자 상세 조회 |
| `linear-list-users` | 워크스페이스 사용자 목록 조회 (이름/이메일 검색) |

### 댓글

| 스킬 | 설명 |
|------|------|
| `linear-list-comments` | 이슈의 댓글 목록 조회 |
| `linear-save-comment` | 댓글 생성 또는 수정 |
| `linear-delete-comment` | 댓글 삭제 |

### 라벨

| 스킬 | 설명 |
|------|------|
| `linear-list-issue-labels` | 이슈 라벨 목록 조회 (워크스페이스 또는 팀) |
| `linear-create-issue-label` | 새 이슈 라벨 생성 |
| `linear-list-project-labels` | 프로젝트 라벨 목록 조회 |

### 워크플로

| 스킬 | 설명 |
|------|------|
| `linear-get-issue-status` | ID 또는 팀으로 워크플로 상태 조회 |
| `linear-list-issue-statuses` | 팀의 전체 워크플로 상태 목록 조회 |
| `linear-list-cycles` | 팀의 사이클(스프린트) 목록 조회 |

### 마일스톤

| 스킬 | 설명 |
|------|------|
| `linear-get-milestone` | ID 또는 프로젝트로 마일스톤 조회 |
| `linear-list-milestones` | 프로젝트의 마일스톤 목록 조회 |
| `linear-save-milestone` | 마일스톤 생성 또는 수정 |

### 첨부파일

| 스킬 | 설명 |
|------|------|
| `linear-get-attachment` | ID로 첨부파일 상세 조회 |
| `linear-create-attachment` | 이슈에 URL 첨부파일 추가 |
| `linear-delete-attachment` | 첨부파일 삭제 |

## 프로젝트 구조

```
skills/
├── linear-api/          # 기본 도구 (GraphQL API 스크립트)
│   ├── SKILL.md
│   └── scripts/
│       └── linear_api.py
├── linear-get-issue/    # 각 스킬은 고유 디렉토리를 가짐
│   └── SKILL.md
├── linear-list-issues/
│   └── SKILL.md
└── ...                  # 30개 이상의 스킬
```

## 라이선스

MIT
