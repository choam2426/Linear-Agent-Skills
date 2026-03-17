---
name: linear-delete-comment
description: Delete a comment from a Linear issue.
---

# Delete Linear Comment

Deletes a comment by ID.

## Required Information

- **id** (required): Comment UUID

## How to Run

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'mutation($id: String!) { commentDelete(id: $id) { success } }' \
  --variables '{"id": "COMMENT_ID"}'
```

## Caution

- Deletion is irreversible.
- Always confirm with the user before deleting.

## Display Results

Show whether the deletion succeeded.
