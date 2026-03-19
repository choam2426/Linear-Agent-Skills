# Linear Agent Skills

An agent-optimized CLI that wraps the entire Linear API into a single Python script — no OAuth, no MCP, no dependencies.

Works with any AI coding agent: [Claude Code](https://claude.com/claude-code), [Cursor](https://cursor.com), [Gemini CLI](https://github.com/google-gemini/gemini-cli), [Windsurf](https://windsurf.com), or any tool that can run shell commands.

## Why use this instead of the Linear MCP server?

- **No OAuth flow** — works with a simple API key
- **No MCP dependency** — runs as a single Python script, no extra servers
- **Works with any AI agent** — not locked to a specific tool. Any agent that can run a shell command can use this.
- **Token efficient** — SKILL.md puts all 32 commands in context at once (~500 tokens), and outputs compact JSON by default.
- **File upload & download** — upload local files and download files from issue descriptions/comments. The Linear MCP server has no file handling capabilities.
- **Cross-platform** — works on Windows/macOS/Linux

### Comparison with Linear MCP server

| | Linear MCP server | This plugin |
|---|---|---|
| Setup | OAuth flow + MCP server process | API key in `.env` |
| Token cost (10 calls, 5 tools) | ~4,150 tok | ~2,300 tok (~45% less) |
| File upload | Not supported | `upload-file` → returns asset URL |
| File download | Not supported | `download-file` from descriptions/comments |
| Output format | Verbose JSON | Compact JSON (~40% smaller) |
| Dependencies | MCP runtime | Python standard library only |

## Installation

### Option 1: Install from marketplace (recommended)

First, register the marketplace:

```
/plugin marketplace add choam2426/claude-linear-skills
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

### Option 2: Run locally (Claude Code)

Clone the repo and point Claude Code to the plugin directory:

```bash
git clone https://github.com/choam2426/Linear-Agent-Skills.git
claude --plugin-dir ./Linear-Agent-Skills
```

### Option 3: Manual copy (works with any AI agent)

Copy the skills directory into your project. Any AI agent that can run shell commands can use it directly:

```bash
git clone https://github.com/choam2426/Linear-Agent-Skills.git
cp -r Linear-Agent-Skills/plugins/claude/skills/ /path/to/your/project/.claude/skills/
```

For **Cursor / Windsurf**, add the CLI path and SKILL.md reference to your rules file.
For **Gemini CLI**, include the SKILL.md content in your system instructions or GEMINI.md.

The CLI itself is a standalone Python script — just run:
```bash
python scripts/linear_cli.py <command> [flags]
```

### Set up your API key

Create a `.env` file in your project root:

```
LINEAR_API_KEY=lin_api_your_key_here
```

Generate a key at **Linear > Settings > API > Personal API keys**.

### Verify installation

Once installed, your AI agent will discover the CLI. Try asking:

- "List my Linear teams"
- "Show issues assigned to me"
- "Create an issue in the Backend team"

## Requirements

- Python 3.7+
- No external dependencies (uses only Python standard library)

## CLI Reference

### Issues

| Command | Description |
|---------|-------------|
| `get-issue` | Get issue details by identifier (e.g., PRJ-42) or UUID |
| `list-issues` | Search/filter issues by team, state, assignee, label, project, priority |
| `create-issue` | Create a new issue |
| `update-issue` | Update an existing issue |

### Documents

| Command | Description |
|---------|-------------|
| `get-document` | Get document details by ID |
| `list-documents` | List all documents |
| `create-document` | Create a new document (requires project, issue, or team ID) |
| `update-document` | Update an existing document |

### Projects

| Command | Description |
|---------|-------------|
| `get-project` | Get project details by name or ID |
| `list-projects` | List/filter projects by team, state, lead |
| `save-project` | Create or update a project |

### Teams

| Command | Description |
|---------|-------------|
| `get-team` | Get team details with members, states, labels |
| `list-teams` | List all teams and their workflow states |

### Users

| Command | Description |
|---------|-------------|
| `get-user` | Get user details by name, email, ID, or `--me` |
| `list-users` | List workspace users, search by name/email |

### Comments

| Command | Description |
|---------|-------------|
| `list-comments` | List comments on an issue |
| `save-comment` | Create or update a comment |
| `delete-comment` | Delete a comment |

### Labels

| Command | Description |
|---------|-------------|
| `list-issue-labels` | List issue labels (workspace or team) |
| `create-issue-label` | Create a new issue label |
| `list-project-labels` | List project labels |

### Workflow

| Command | Description |
|---------|-------------|
| `get-issue-status` | Get a workflow state by ID or team |
| `list-issue-statuses` | List all workflow states for a team |
| `list-cycles` | List cycles (sprints) for a team |

### Milestones

| Command | Description |
|---------|-------------|
| `get-milestone` | Get a milestone by ID or project |
| `list-milestones` | List milestones in a project |
| `save-milestone` | Create or update a milestone |

### Attachments & Files

| Command | Description |
|---------|-------------|
| `get-attachment` | Get attachment details by ID |
| `create-attachment` | Add a URL attachment to an issue |
| `delete-attachment` | Delete an attachment |
| `upload-file` | Upload a local file, returns asset URL for use in descriptions/comments |
| `download-file` | Download files uploaded in descriptions/comments (uploads.linear.app) |

## Project Structure

```
plugins/claude/skills/
└── linear-cli/
    ├── SKILL.md          # CLI reference for Claude Code
    └── scripts/
        └── linear_cli.py # CLI implementation
```

## License

MIT
