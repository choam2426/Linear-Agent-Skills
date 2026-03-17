---
name: linear-get-issue
description: Get Linear issue details. Pass an issue identifier (e.g., SCE-1) or UUID as argument.
---

# Get Linear Issue Details

Retrieves issue details by identifier (e.g., SCE-1) or UUID.

## How to Run

Replace `ISSUE_ID` with the user-provided issue identifier:

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($id: String!) { issue(id: $id) { id identifier title description state { name type } assignee { name email } labels { nodes { name color } } priority priorityLabel project { name } team { name key } createdAt updatedAt dueDate estimate url attachments { nodes { id title url sourceType } } } }' \
  --variables '{"id": "ISSUE_ID"}'
```

## Display Results

- Identifier, title, URL
- State, assignee, priority
- Labels, project, team
- Description (summarize if long)
- Attachments/resources list
