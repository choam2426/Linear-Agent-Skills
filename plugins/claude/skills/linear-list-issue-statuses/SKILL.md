---
name: linear-list-issue-statuses
description: List issue statuses (workflow states) for a Linear team.
---

# List Linear Issue Statuses

Retrieves workflow states for a specific team.

## How to Run

### By Team ID/Key

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($id: String!) { team(id: $id) { id name key states { nodes { id name type position color description } } } }' \
  --variables '{"id": "TEAM_ID_OR_KEY"}'
```

### By Team Name

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($filter: TeamFilter) { teams(filter: $filter) { nodes { id name key states { nodes { id name type position color description } } } } }' \
  --variables '{"filter": {"name": {"eq": "TeamName"}}}'
```

## Display Results

Sort by position and show:

| Name | Type | Color | Description |

Types: triage, backlog, unstarted, started, completed, canceled
