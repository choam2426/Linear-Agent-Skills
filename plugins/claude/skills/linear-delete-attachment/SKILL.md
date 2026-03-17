---
name: linear-delete-attachment
description: Delete a Linear attachment by ID.
---

# Delete Linear Attachment

Deletes an attachment by ID.

## Required Information

- **id** (required): Attachment UUID

## How to Run

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'mutation($id: String!) { attachmentDelete(id: $id) { success } }' \
  --variables '{"id": "ATTACHMENT_ID"}'
```

## Caution

- Deletion is irreversible.
- Always confirm with the user before deleting.

## Display Results

Show whether the deletion succeeded.
