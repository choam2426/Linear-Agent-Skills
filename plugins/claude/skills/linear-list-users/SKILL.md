---
name: linear-list-users
description: List users in the Linear workspace. Search by name or email.
---

# List Linear Users

Lists users in the workspace.

## How to Run

### All Users

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($first: Int, $after: String) { users(first: $first, after: $after, orderBy: updatedAt) { nodes { id name email displayName active admin teams { nodes { name key } } } pageInfo { hasNextPage endCursor } } }' \
  --variables '{"first": 50}' \
  --paginate users
```

### Search by Name/Email

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($filter: UserFilter) { users(filter: $filter) { nodes { id name email displayName active admin teams { nodes { name key } } } } }' \
  --variables '{"filter": {"name": {"containsIgnoreCase": "search_term"}}}'
```

For email search: `{"filter": {"email": {"containsIgnoreCase": "search_term"}}}`

## Display Results

| Name | Email | Active | Admin | Teams |
