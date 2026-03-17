---
name: linear-create-issue-label
description: Create a new issue label in Linear. Specify name, color, and team.
---

# Create Linear Issue Label

Creates a new issue label.

## Required Information

- **name** (required): Label name
- **color** (optional): Hex color code (e.g., #FF0000)
- **description** (optional): Label description
- **teamId** (optional): Team UUID. If omitted, creates a workspace-level label
- **parentId** (optional): Parent label group UUID

## How to Run

### Get Team ID (for team-scoped labels)

```bash
python skills/linear-api/scripts/linear_api.py \
  --query '{ teams { nodes { id name key } } }'
```

### Create Label

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'mutation($input: IssueLabelCreateInput!) { issueLabelCreate(input: $input) { success issueLabel { id name color } } }' \
  --variables '{"input": {"name": "LabelName", "color": "#FF0000", "teamId": "TEAM_UUID"}}'
```

Omit `teamId` for workspace-level labels.

## Display Results

Show the created label's name and color.
