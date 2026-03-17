---
name: linear-list-issue-labels
description: List issue labels in the Linear workspace or a specific team.
---

# List Linear Issue Labels

Lists issue labels for the entire workspace or a specific team.

## How to Run

### All Labels

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($first: Int, $after: String) { issueLabels(first: $first, after: $after, orderBy: updatedAt) { nodes { id name color description isGroup parent { id name } team { name key } } pageInfo { hasNextPage endCursor } } }' \
  --variables '{"first": 50}' \
  --paginate issueLabels
```

### Filter by Team

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($first: Int, $after: String, $filter: IssueLabelFilter) { issueLabels(first: $first, after: $after, filter: $filter, orderBy: updatedAt) { nodes { id name color description isGroup parent { id name } team { name key } } pageInfo { hasNextPage endCursor } } }' \
  --variables '{"first": 50, "filter": {"team": {"name": {"eq": "TeamName"}}}}' \
  --paginate issueLabels
```

## Display Results

| Name | Color | Group | Team | Description |
