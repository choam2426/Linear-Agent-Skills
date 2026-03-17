---
name: linear-save-milestone
description: Create or update a milestone in a Linear project.
---

# Create/Update Linear Milestone

Creates a new milestone in a project or updates an existing one.

## Required Information

### New Milestone
- **projectId** (required): Project UUID
- **name** (required): Milestone name
- **description** (optional): Description
- **targetDate** (optional): Target date (ISO format, e.g., 2026-04-01)

### Update Milestone
- **id** (required): Milestone UUID
- **name/description/targetDate**: Fields to change

## How to Run

### Look Up Project ID

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($filter: ProjectFilter) { projects(filter: $filter) { nodes { id name } } }' \
  --variables '{"filter": {"name": {"eq": "ProjectName"}}}'
```

### Create New Milestone

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'mutation($input: ProjectMilestoneCreateInput!) { projectMilestoneCreate(input: $input) { success projectMilestone { id name description targetDate } } }' \
  --variables '{"input": {"projectId": "PROJECT_UUID", "name": "MilestoneName", "targetDate": "2026-04-01"}}'
```

### Update Existing Milestone

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'mutation($id: String!, $input: ProjectMilestoneUpdateInput!) { projectMilestoneUpdate(id: $id, input: $input) { success projectMilestone { id name description targetDate } } }' \
  --variables '{"id": "MILESTONE_UUID", "input": {"name": "NewName", "targetDate": "2026-05-01"}}'
```

To remove target date: `"targetDate": null`

## Display Results

Show the created/updated milestone's name and target date.
