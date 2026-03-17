---
name: linear-list-documents
description: List documents in the Linear workspace. Can filter by project.
---

# List Linear Documents

Searches documents based on user-provided conditions. Lists all documents if no conditions are specified.

## How to Run

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($first: Int, $after: String) { documents(first: $first, after: $after, orderBy: updatedAt) { nodes { id title icon color project { name } creator { name } createdAt updatedAt } pageInfo { hasNextPage endCursor } } }' \
  --variables '{"first": 50}' \
  --paginate documents
```

## Display Results

Show in table format:

| Title | Project | Author | Updated |
