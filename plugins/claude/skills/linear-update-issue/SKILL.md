---
name: linear-update-issue
description: Update a Linear issue. Change state, assignee, labels, priority, etc.
---

# Update Linear Issue

Applies changes to an issue identified by the user.

## Required Information

- **Issue identifier** (required): e.g., SCE-1, SSA-5, or UUID
- **Changes**: state, assignee, priority, labels, description, etc.

## How to Run

### Step 1: Get Current Issue State

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($id: String!) { issue(id: $id) { id identifier title state { name } assignee { name } team { id name states { nodes { id name type } } } } }' \
  --variables '{"id": "ISSUE_IDENTIFIER"}'
```

### Step 2: Resolve Field IDs

- State change → find the target state ID from team's states, set `stateId`
- Assignee change → query user, set `assigneeId`
- Priority change → set `priority` value directly

### Step 3: Run Update

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'mutation($id: String!, $input: IssueUpdateInput!) { issueUpdate(id: $id, input: $input) { success issue { id identifier title state { name } assignee { name } priority url } } }' \
  --variables '{"id": "ISSUE_UUID", "input": {"stateId": "STATE_UUID"}}'
```

## Display Results

Show a before/after comparison of the changes.
