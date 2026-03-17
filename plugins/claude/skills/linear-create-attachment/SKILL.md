---
name: linear-create-attachment
description: Add a URL attachment to a Linear issue.
---

# Create Linear Attachment

Adds a URL-based attachment (link) to an issue.

## Required Information

- **issue** (required): Issue identifier (e.g., SCE-1) or UUID
- **url** (required): URL to attach
- **title** (optional): Attachment title
- **subtitle** (optional): Subtitle

## How to Run

### Step 1: Get Issue UUID

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($id: String!) { issue(id: $id) { id identifier title } }' \
  --variables '{"id": "ISSUE_IDENTIFIER"}'
```

### Step 2: Create Attachment

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'mutation($input: AttachmentCreateInput!) { attachmentCreate(input: $input) { success attachment { id title url } } }' \
  --variables '{"input": {"issueId": "ISSUE_UUID", "url": "ATTACHMENT_URL", "title": "Title"}}'
```

## Notes

- This skill supports URL-based attachments (links).
- File uploads require a separate upload flow.

## Display Results

Show the created attachment's title and URL.
