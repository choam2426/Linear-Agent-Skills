---
name: linear-get-issue-status
description: Retrieve a Linear issue status (workflow state). Search by team and status name.
---

# Get Linear Issue Status

Retrieves a team's workflow state details.

## How to Run

### By State ID

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($id: String!) { workflowState(id: $id) { id name type position color description team { name key } } }' \
  --variables '{"id": "STATE_ID"}'
```

### By Team Name (list all states, then filter)

If you know the team name or key, query all states and filter by name:

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($filter: TeamFilter) { teams(filter: $filter) { nodes { id name key states { nodes { id name type position color description } } } } }' \
  --variables '{"filter": {"name": {"eq": "TeamName"}}}'
```

## Display Results

- State name, type (triage/backlog/unstarted/started/completed/canceled)
- Color, position, description
- Parent team
