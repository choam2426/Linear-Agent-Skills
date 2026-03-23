---
name: linear-cli
description: Linear workspace CLI — issues, projects, documents, teams, users, comments, labels, cycles, milestones, attachments.
---

SKILL_DIR: This skill directory

## Usage
- Windows: `python ${SKILL_DIR}$/scripts/linear_cli.py <cmd> [flags]`
- macOS/Linux: `python3 ${SKILL_DIR}$/scripts/linear_cli.py <cmd> [flags]`

## Commands

### Issues
get-issue --id ID              # ID = identifier (e.g. PRJ-42) or UUID
list-issues [--team NAME] [--state NAME] [--assignee NAME] [--label NAME] [--project NAME] [--priority INT] [--parent-id ID] [--filter JSON]
create-issue --title STR --team-id UUID [--description MD] [--priority 0-4] [--assignee-id UUID] [--label-ids csv] [--state-id UUID] [--estimate INT] [--due-date YYYY-MM-DD] [--project-id UUID] [--cycle-id UUID] [--parent-id UUID]
update-issue --id ID --input JSON   # e.g. --input '{"title":"New","priority":2,"stateId":"...","assigneeId":"..."}'
list-sub-issues --id ID                          # list child issues of a parent issue
add-sub-issue --parent-id ID --issue-id ID       # link existing issue as sub-issue
remove-sub-issue --issue-id ID                   # unlink sub-issue from parent

### Documents
get-document --id ID
list-documents
create-document --title STR --content MD (--project-id UUID|--issue-id UUID|--team-id UUID)
update-document --id ID --input JSON   # e.g. --input '{"title":"New","content":"..."}'

### Projects
get-project (--id ID|--name STR)
list-projects [--team NAME] [--state STATE] [--lead NAME] [--filter JSON]
save-project --input JSON [--id UUID]   # e.g. --input '{"name":"P","teamIds":["UUID"]}'

### Teams
get-team (--id ID|--name STR)
list-teams

### Users
get-user (--id UUID|--name STR|--email STR|--me)
list-users [--name STR] [--email STR]

### Comments
list-comments --issue-id ID
save-comment --input JSON [--id UUID]   # create: '{"issueId":"...","body":"..."}' / update: '{"body":"..."}'
delete-comment --id UUID

### Labels
list-issue-labels [--team NAME]
create-issue-label --name STR [--color HEX] [--team-id UUID] [--description STR]
list-project-labels

### Workflow
get-issue-status (--id UUID|--team NAME)
list-issue-statuses (--team UUID|--name NAME)  # --team expects UUID, --name expects team name
save-issue-status --input JSON [--id UUID]   # create: '{"name":"Review","teamId":"UUID","type":"started","color":"#f0ad4e"}' / update: '{"name":"Renamed"}'
delete-issue-status --id UUID                # archives the workflow state
list-cycles (--team UUID|--name NAME)

### Milestones
get-milestone (--id UUID|--project NAME)
list-milestones (--project UUID|--name NAME)   # --project expects UUID, --name expects project name
save-milestone --input JSON [--id UUID]   # e.g. --input '{"name":"M1","projectId":"UUID"}'

### Attachments
get-attachment --id UUID
create-attachment --issue-id UUID --url URL [--title STR] [--subtitle STR]
delete-attachment --id UUID
upload-file --file PATH               # upload local file, returns assetUrl for use in descriptions/comments
download-file --url URL [--output PATH]  # download files uploaded in descriptions/comments (uploads.linear.app)

## Notes
- save-* with --id updates, without --id creates.
- --input/--filter follows Linear GraphQL schema (IssueUpdateInput, ProjectFilter, etc.).
- --filter example: `--filter '{"team":{"name":{"eq":"Backend"}},"priority":{"gte":2}}'`
- Sub-issues: use --parent-id on create-issue, or add-sub-issue to link/create. get-issue returns parent and children fields.
- Priority: 0=None 1=Urgent 2=High 3=Normal 4=Low
- Project state: planned|started|paused|completed|canceled
- Workflow state type: backlog|unstarted|started|completed|canceled
- Errors: JSON to stderr `{"error":"...","details":...}`
- Workflow: first call list-teams to get team IDs/names, then use them in other commands.
