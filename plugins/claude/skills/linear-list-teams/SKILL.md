---
name: linear-list-teams
description: List teams and their workflow states in the Linear workspace.
---

# List Linear Teams

Lists all teams and their workflow states in the workspace.

## How to Run

```bash
python skills/linear-api/scripts/linear_api.py \
  --query '{ teams { nodes { id name key icon states { nodes { id name type position color } } } } }'
```

## Display Results

Parse the response JSON and organize by team:

- **Team name** (key) — icon
- Workflow states: name, type (triage/backlog/unstarted/started/completed/canceled), color

Show in a table or structured format.
