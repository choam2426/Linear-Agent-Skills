---
name: linear-get-user
description: Get Linear user details. Search by name, email, ID, or "me".
---

# Get Linear User Details

Retrieves user details by ID, name, or email.

## How to Run

### By ID

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($id: String!) { user(id: $id) { id name email displayName avatarUrl active admin createdAt teams { nodes { name key } } } }' \
  --variables '{"id": "USER_ID"}'
```

### Current User (me)

```bash
python skills/linear-api/scripts/linear_api.py \
  --query '{ viewer { id name email displayName avatarUrl active admin createdAt teams { nodes { name key } } } }'
```

### Search by Name/Email

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($filter: UserFilter) { users(filter: $filter) { nodes { id name email displayName active admin teams { nodes { name key } } } } }' \
  --variables '{"filter": {"name": {"containsIgnoreCase": "search_term"}}}'
```

## Display Results

- Name, email, display name
- Active status, admin status
- Team memberships
