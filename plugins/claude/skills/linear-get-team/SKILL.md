---
name: linear-get-team
description: Get Linear team details. Search by team name, key, or UUID.
---

# Get Linear Team Details

Retrieves team details by ID, key, or name.

## How to Run

### By ID/Key

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($id: String!) { team(id: $id) { id name key icon description members { nodes { id name email } } states { nodes { id name type position color } } labels { nodes { id name color } } cycles { nodes { id number name startsAt endsAt } } } }' \
  --variables '{"id": "TEAM_ID_OR_KEY"}'
```

### By Name

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($filter: TeamFilter) { teams(filter: $filter) { nodes { id name key icon description members { nodes { id name email } } states { nodes { id name type position color } } } } }' \
  --variables '{"filter": {"name": {"eq": "TeamName"}}}'
```

## Display Results

- Team name, key, icon, description
- Members list
- Workflow states list
- Labels list
- Cycles list
