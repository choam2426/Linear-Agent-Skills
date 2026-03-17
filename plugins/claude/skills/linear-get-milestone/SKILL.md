---
name: linear-get-milestone
description: Retrieve a Linear project milestone. Search by project name and milestone name/ID.
---

# Get Linear Milestone

Retrieves a specific milestone within a project.

## How to Run

### By Milestone ID

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($id: String!) { projectMilestone(id: $id) { id name description targetDate sortOrder project { id name } } }' \
  --variables '{"id": "MILESTONE_ID"}'
```

### By Project Name (list milestones, then filter)

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($filter: ProjectFilter) { projects(filter: $filter) { nodes { id name projectMilestones { nodes { id name description targetDate sortOrder } } } } }' \
  --variables '{"filter": {"name": {"eq": "ProjectName"}}}'
```

## Display Results

- Milestone name, description
- Target date
- Parent project
