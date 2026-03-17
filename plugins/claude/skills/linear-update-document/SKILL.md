---
name: linear-update-document
description: Update a Linear document. Change title, content, project link, etc.
---

# Update Linear Document

Updates an existing document's title, content, project link, etc.

## Required Information

- **id** (required): Document UUID or slug
- Fields to change:
  - **title**: New title
  - **content**: New markdown body
  - **icon**: Icon emoji
  - **color**: Hex color
  - **projectId**: Project UUID to link

## How to Run

### Step 1: Get Current Document

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($id: String!) { document(id: $id) { id title content project { id name } } }' \
  --variables '{"id": "DOC_ID"}'
```

### Step 2: Update Document

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'mutation($id: String!, $input: DocumentUpdateInput!) { documentUpdate(id: $id, input: $input) { success document { id title url updatedAt } } }' \
  --variables '{"id": "DOC_ID", "input": {"title": "New Title", "content": "New content"}}'
```

To change project: add `"projectId": "PROJECT_UUID"` to the input.

## Display Results

Show the updated document's title, URL, and updated date.
