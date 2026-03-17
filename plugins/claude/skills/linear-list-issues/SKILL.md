---
name: linear-list-issues
description: Search and filter Linear issues. Filter by team, state, assignee, label, etc.
---

# List Linear Issues

Searches issues based on user-provided conditions.

## Filter Construction

Analyze the user's request and build a GraphQL filter object. Supported filters:

- Team: `team: { name: { eq: "TeamName" } }`
- State: `state: { name: { eq: "StateName" } }` or `state: { type: { eq: "started" } }`
- Assignee: `assignee: { name: { containsIgnoreCase: "Name" } }`
- Label: `labels: { name: { eq: "LabelName" } }`
- Project: `project: { name: { eq: "ProjectName" } }`
- Priority: `priority: { eq: 1 }` (1=Urgent, 2=High, 3=Normal, 4=Low)

## How to Run

Insert the constructed filter and run:

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($filter: IssueFilter, $first: Int, $after: String) { issues(filter: $filter, first: $first, after: $after, orderBy: updatedAt) { nodes { id identifier title state { name } assignee { name } priority priorityLabel team { key } updatedAt } pageInfo { hasNextPage endCursor } } }' \
  --variables '{"filter": {constructed_filter}, "first": 50}' \
  --paginate issues
```

## Display Results

Show in table format:

| ID | Title | State | Assignee | Priority | Team |
