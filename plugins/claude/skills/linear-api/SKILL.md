---
name: linear-api
description: Linear GraphQL API calling tool. Other Linear skills use this skill's script to make API calls.
---

# Linear GraphQL API Tool

Base tool for calling the Linear GraphQL API. All other Linear skills use this skill's script.

## Script Location

`skills/linear-api/scripts/linear_api.py`

## Usage

### Basic Query

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'GraphQL query' \
  --variables '{"key": "value"}'
```

### Paginated Query

Used for list queries with `nodes`/`pageInfo` pattern. Automatically traverses all pages.

```bash
python skills/linear-api/scripts/linear_api.py \
  --query 'query($first: Int, $after: String) { issues(first: $first, after: $after) { nodes { id title } pageInfo { hasNextPage endCursor } } }' \
  --variables '{"first": 50}' \
  --paginate issues
```

## Authentication

- Automatically loads `LINEAR_API_KEY` from the `.env` file in the project root.
- Displays setup instructions if the API key is missing.
- Keys can be generated at Linear > Settings > API > Personal API keys.

## Output

- Basic query: outputs `result.data` as JSON
- Paginated query: outputs all `nodes` merged into a single JSON array
- On error: outputs error JSON to stderr and exits with code 1

## Notes

- GraphQL API endpoint: `https://api.linear.app/graphql`
- Ensures UTF-8 output on Windows.
