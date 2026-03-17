---
name: linear-create-issue
description: Create a new Linear issue. Specify title, team, description, priority, labels, etc.
---

# Create Linear Issue

Extracts issue information from the user's request and creates a new issue.

## Required Information

- **title** (required): Issue title
- **team** (required): Team name or key. If not specified, query the team list and ask the user to choose
- **description** (optional): Markdown description
- **priority** (optional): 0=None, 1=Urgent, 2=High, 3=Normal, 4=Low
- **labels** (optional): Array of label names
- **assignee** (optional): Assignee name or email

## How to Run

### Step 1: Get Team ID

```bash
python skills/linear-api/scripts/linear_api.py \
  --query '{ teams { nodes { id name key } } }'
```

### Step 2: Create Issue

After confirming the team ID, run the mutation:

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'mutation($input: IssueCreateInput!) { issueCreate(input: $input) { success issue { id identifier title url } } }' \
  --variables '{"input": {"title": "Title", "teamId": "TEAM_UUID", "description": "Description", "priority": 3}}'
```

- If labels are specified, add `labelIds` with an array of label UUIDs (query labels separately if needed)
- If assignee is specified, add `assigneeId`

## Display Results

Show the created issue's identifier, title, and URL.
