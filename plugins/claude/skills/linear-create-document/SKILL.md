---
name: linear-create-document
description: Create a new Linear document. Can attach to an issue as a resource or link to a project.
---

# Create Linear Document

Extracts document information from the user's request and creates it.

## Required Information

- **title** (required): Document title
- **content** (required): Markdown body
- **parent** (required, choose one): A document must be linked to one of the following:
  - `projectId` — link to a project (recommended, visible under Project > Resources in Linear UI)
  - `issueId` — attach as a resource to an issue (visible in issue details)
  - `teamId`, `cycleId`, `initiativeId`, `releaseId` are also possible but harder to find in the UI
- **icon** (optional): Icon emoji

If the user doesn't specify a parent, ask whether to link to a project or issue.

## How to Run

### Look Up Issue/Project ID (if needed)

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($id: String!) { issue(id: $id) { id identifier title } }' \
  --variables '{"id": "ISSUE_IDENTIFIER"}'
```

### Create Document

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'mutation($input: DocumentCreateInput!) { documentCreate(input: $input) { success document { id title url } } }' \
  --variables '{"input": {"title": "Title", "content": "Markdown body", "projectId": "PROJECT_UUID"}}'
```

- For issue attachment: use `"issueId": "ISSUE_UUID"` instead of `projectId`
- For team attachment: use `"teamId": "TEAM_UUID"` instead of `projectId` (hard to find in UI)

## Display Results

Show the created document's title, URL, and linked issue/project.
