# Claude Linear Skills

A collection of [Claude Code](https://claude.com/claude-code) skills that replace the Linear MCP server with native GraphQL API calls. No OAuth or MCP configuration required — just a Linear API key.

## Why use this instead of the Linear MCP server?

- **No OAuth flow** — works with a simple API key
- **No MCP dependency** — runs as plain Python, no extra servers
- **Full coverage** — 30 skills covering all Linear MCP tools
- **Customizable** — edit any skill's GraphQL query to fit your workflow

## Installation

### Option 1: Install from marketplace (recommended)

First, register the marketplace:

```
/plugin marketplace add choam/claude-linear-skills
```

Then install the plugin:

```
/plugin install claude-linear-skills@claude-linear-skills
```

You can also specify the installation scope:

```bash
# User scope (default, available across all projects)
claude plugin install claude-linear-skills@claude-linear-skills

# Project scope (shared with team, included in version control)
claude plugin install claude-linear-skills@claude-linear-skills --scope project

# Local scope (gitignored, only for you)
claude plugin install claude-linear-skills@claude-linear-skills --scope local
```

### Option 2: Run locally

Clone the repo and point Claude Code to the plugin directory:

```bash
git clone https://github.com/choam/claude-linear-skills.git
claude --plugin-dir ./claude-linear-skills
```

### Option 3: Manual copy

Copy the skills directory directly into your project:

```bash
cp -r skills/ /path/to/your/project/skills/
```

### Set up your API key

Regardless of installation method, you need a Linear API key. Create a `.env` file in your project root:

```
LINEAR_API_KEY=lin_api_your_key_here
```

You can generate a key at **Linear > Settings > API > Personal API keys**.

### Verify installation

Once installed, Claude Code will automatically discover the skills. Try asking:

- "List my Linear teams"
- "Show issues assigned to me"
- "Create an issue in the Backend team"

## Requirements

- Python 3.7+
- No external dependencies (uses only Python standard library)

## Skills Reference

### Base Tool

| Skill | Description |
|-------|-------------|
| `linear-api` | Base GraphQL API tool. All other skills use this script. |

### Issues

| Skill | Description |
|-------|-------------|
| `linear-get-issue` | Get issue details by identifier (e.g., SCE-1) or UUID |
| `linear-list-issues` | Search/filter issues by team, state, assignee, label, etc. |
| `linear-create-issue` | Create a new issue |
| `linear-update-issue` | Update an existing issue |

### Documents

| Skill | Description |
|-------|-------------|
| `linear-get-document` | Get document details by ID or slug |
| `linear-list-documents` | List documents, optionally filtered by project |
| `linear-create-document` | Create a new document |
| `linear-update-document` | Update an existing document |

### Projects

| Skill | Description |
|-------|-------------|
| `linear-get-project` | Get project details by name, ID, or slug |
| `linear-list-projects` | List/filter projects by team, state, label, etc. |
| `linear-save-project` | Create or update a project |

### Teams

| Skill | Description |
|-------|-------------|
| `linear-get-team` | Get team details by name, key, or UUID |
| `linear-list-teams` | List all teams and their workflow states |

### Users

| Skill | Description |
|-------|-------------|
| `linear-get-user` | Get user details by name, email, ID, or "me" |
| `linear-list-users` | List workspace users, search by name/email |

### Comments

| Skill | Description |
|-------|-------------|
| `linear-list-comments` | List comments on an issue |
| `linear-save-comment` | Create or update a comment |
| `linear-delete-comment` | Delete a comment |

### Labels

| Skill | Description |
|-------|-------------|
| `linear-list-issue-labels` | List issue labels (workspace or team) |
| `linear-create-issue-label` | Create a new issue label |
| `linear-list-project-labels` | List project labels |

### Workflow

| Skill | Description |
|-------|-------------|
| `linear-get-issue-status` | Get a workflow state by ID or team |
| `linear-list-issue-statuses` | List all workflow states for a team |
| `linear-list-cycles` | List cycles (sprints) for a team |

### Milestones

| Skill | Description |
|-------|-------------|
| `linear-get-milestone` | Get a milestone by ID or project |
| `linear-list-milestones` | List milestones in a project |
| `linear-save-milestone` | Create or update a milestone |

### Attachments

| Skill | Description |
|-------|-------------|
| `linear-get-attachment` | Get attachment details by ID |
| `linear-create-attachment` | Add a URL attachment to an issue |
| `linear-delete-attachment` | Delete an attachment |

## Project Structure

```
skills/
├── linear-api/          # Base tool (GraphQL API script)
│   ├── SKILL.md
│   └── scripts/
│       └── linear_api.py
├── linear-get-issue/    # Each skill has its own directory
│   └── SKILL.md
├── linear-list-issues/
│   └── SKILL.md
└── ...                  # 30 more skills
```

## License

MIT
