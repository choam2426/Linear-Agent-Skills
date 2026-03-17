---
name: linear-save-comment
description: Create or update a comment on a Linear issue.
---

# Create/Update Linear Comment

Creates a new comment on an issue or updates an existing comment.

## Required Information

### New Comment
- **issueId** (required): Issue identifier (e.g., SCE-1) or UUID
- **body** (required): Comment content (markdown)
- **parentId** (optional): Parent comment UUID (for replies)

### Update Comment
- **id** (required): Comment UUID to update
- **body** (required): New comment content

## How to Run

### Create New Comment

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'mutation($input: CommentCreateInput!) { commentCreate(input: $input) { success comment { id body createdAt url user { name } } } }' \
  --variables '{"input": {"issueId": "ISSUE_IDENTIFIER", "body": "Comment content"}}'
```

For replies, add `"parentId": "PARENT_COMMENT_UUID"`.

### Update Existing Comment

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'mutation($id: String!, $input: CommentUpdateInput!) { commentUpdate(id: $id, input: $input) { success comment { id body updatedAt } } }' \
  --variables '{"id": "COMMENT_UUID", "input": {"body": "Updated content"}}'
```

## Display Results

- New comment: URL, author, content summary
- Update: confirm the changes
