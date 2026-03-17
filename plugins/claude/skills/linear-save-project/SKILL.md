---
name: linear-save-project
description: Create or update a Linear project.
---

# Create/Update Linear Project

Creates a new project or updates an existing one.

## Required Information

### New Project
- **name** (required): Project name
- **teamIds** (required): Array of team UUIDs
- **description** (optional): Markdown description
- **icon** (optional): Icon emoji
- **color** (optional): Hex color
- **leadId** (optional): Lead user UUID
- **startDate** (optional): Start date (ISO format)
- **targetDate** (optional): Target date (ISO format)
- **priority** (optional): 0=None, 1=Urgent, 2=High, 3=Medium, 4=Low

### Update Project
- **id** (required): Project UUID
- Fields to change

## How to Run

### Get Team IDs

```bash
python skills/linear-api/scripts/linear_api.py \
  --query '{ teams { nodes { id name key } } }'
```

### Create New Project

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'mutation($input: ProjectCreateInput!) { projectCreate(input: $input) { success project { id name slugId url } } }' \
  --variables '{"input": {"name": "ProjectName", "teamIds": ["TEAM_UUID"], "description": "Description"}}'
```

### Update Existing Project

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'mutation($id: String!, $input: ProjectUpdateInput!) { projectUpdate(id: $id, input: $input) { success project { id name state url } } }' \
  --variables '{"id": "PROJECT_UUID", "input": {"name": "NewName", "state": "started"}}'
```

Project states: planned, started, paused, completed, canceled

## Display Results

Show the created/updated project's name, state, and URL.
