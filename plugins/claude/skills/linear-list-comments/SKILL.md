---
name: linear-list-comments
description: List comments on a Linear issue. Filter by issue identifier.
---

# List Linear Issue Comments

Retrieves comments for a specific issue.

## How to Run

Replace `ISSUE_ID` with the user-provided issue identifier:

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($id: String!) { issue(id: $id) { id identifier title comments(orderBy: createdAt) { nodes { id body createdAt updatedAt user { name email } parent { id } } } } }' \
  --variables '{"id": "ISSUE_ID"}'
```

## Display Results

Show in table or thread format:

- Author, date
- Comment content (markdown)
- If a reply, indicate parent comment
