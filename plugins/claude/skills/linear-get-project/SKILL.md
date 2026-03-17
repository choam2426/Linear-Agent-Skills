---
name: linear-get-project
description: Get Linear project details. Search by project name, ID, or slug.
---

# Get Linear Project Details

Retrieves project details by ID or name.

## How to Run

### By ID

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($id: String!) { project(id: $id) { id name slugId description icon color state startDate targetDate progress lead { name email } teams { nodes { name key } } members { nodes { name email } } projectMilestones { nodes { id name targetDate } } documents { nodes { id title } } } }' \
  --variables '{"id": "PROJECT_ID"}'
```

### By Name

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($filter: ProjectFilter) { projects(filter: $filter) { nodes { id name slugId description icon color state startDate targetDate progress lead { name email } teams { nodes { name key } } } } }' \
  --variables '{"filter": {"name": {"eq": "ProjectName"}}}'
```

## Options

Include additional fields when requested by the user:
- Members: `members { nodes { name email } }`
- Milestones: `projectMilestones { nodes { id name targetDate } }`
- Resources (documents, etc.): `documents { nodes { id title } }`

## Display Results

- Name, description, icon, color
- State, start date, target date, progress
- Lead, team list
- (On request) Members, milestones, documents
