---
name: linear-list-project-labels
description: List project labels in the Linear workspace.
---

# List Linear Project Labels

Lists project labels in the workspace.

## How to Run

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($first: Int, $after: String) { projectLabels(first: $first, after: $after) { nodes { id name color description } pageInfo { hasNextPage endCursor } } }' \
  --variables '{"first": 50}' \
  --paginate projectLabels
```

## Display Results

| Name | Color | Description |
