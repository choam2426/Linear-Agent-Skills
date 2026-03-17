---
name: linear-get-attachment
description: Retrieve a Linear attachment by ID.
---

# Get Linear Attachment

Retrieves attachment details by ID.

## How to Run

Replace `ATTACHMENT_ID` with the user-provided attachment ID:

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($id: String!) { attachment(id: $id) { id title subtitle url sourceType createdAt updatedAt issue { id identifier title } } }' \
  --variables '{"id": "ATTACHMENT_ID"}'
```

## Display Results

- Title, URL, source type
- Linked issue identifier and title
- Created date, updated date
