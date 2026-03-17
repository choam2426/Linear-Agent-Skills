---
name: linear-list-cycles
description: List cycles (sprints) for a Linear team.
---

# List Linear Cycles

Retrieves cycles (sprints) for a team.

## How to Run

### By Team ID/Key

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($id: String!) { team(id: $id) { id name cycles(orderBy: startsAt) { nodes { id number name startsAt endsAt completedAt progress { completedScopeCount scopeCount } } } } }' \
  --variables '{"id": "TEAM_ID_OR_KEY"}'
```

### By Team Name

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($filter: TeamFilter) { teams(filter: $filter) { nodes { id name cycles(orderBy: startsAt) { nodes { id number name startsAt endsAt completedAt progress { completedScopeCount scopeCount } } } } } }' \
  --variables '{"filter": {"name": {"eq": "TeamName"}}}'
```

## Filtering

If the user only wants current/previous/next cycles, filter results by date:
- **current**: `startsAt <= today <= endsAt`
- **previous**: most recent where `endsAt < today`
- **next**: earliest where `startsAt > today`

## Display Results

| Number | Name | Start | End | Progress |
