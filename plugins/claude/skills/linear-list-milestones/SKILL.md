---
name: linear-list-milestones
description: List milestones in a Linear project.
---

# List Linear Milestones

Retrieves milestones within a project.

## How to Run

### By Project ID

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($id: String!) { project(id: $id) { id name projectMilestones { nodes { id name description targetDate sortOrder } } } }' \
  --variables '{"id": "PROJECT_ID"}'
```

### By Project Name

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($filter: ProjectFilter) { projects(filter: $filter) { nodes { id name projectMilestones { nodes { id name description targetDate sortOrder } } } } }' \
  --variables '{"filter": {"name": {"eq": "ProjectName"}}}'
```

## Display Results

Sort by sortOrder:

| Name | Description | Target Date |
