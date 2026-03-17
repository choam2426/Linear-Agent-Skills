---
name: linear-get-document
description: Get Linear document details. Pass a document ID or slug as argument.
---

# Get Linear Document Details

Retrieves a document by ID or slug.

## How to Run

Replace `DOC_ID` with the user-provided document ID:

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($id: String!) { document(id: $id) { id title icon color content project { name } creator { name } createdAt updatedAt } }' \
  --variables '{"id": "DOC_ID"}'
```

## Display Results

- Title, project, author
- Content (markdown)
- Created date, updated date
