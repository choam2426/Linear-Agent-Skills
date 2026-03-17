---
name: linear-list-projects
description: List projects in the Linear workspace. Filter by team, state, label, etc.
---

# List Linear Projects

Searches and filters projects in the workspace.

## Filter Construction

Analyze the user's request and build a GraphQL filter object:

- Name: `name: { containsIgnoreCase: "search_term" }`
- State: `state: { eq: "planned" }` (planned, started, paused, completed, canceled)
- Team: `accessibleTeams: { name: { eq: "TeamName" } }`
- Lead: `lead: { name: { containsIgnoreCase: "Name" } }`

## How to Run

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($first: Int, $after: String, $filter: ProjectFilter) { projects(first: $first, after: $after, filter: $filter, orderBy: updatedAt) { nodes { id name slugId description icon color state startDate targetDate progress lead { name } teams { nodes { name key } } } pageInfo { hasNextPage endCursor } } }' \
  --variables '{"first": 50, "filter": {}}' \
  --paginate projects
```

Replace `"filter": {}` with the constructed filter object when filtering.

## Display Results

| Name | State | Lead | Team | Progress | Target Date |
