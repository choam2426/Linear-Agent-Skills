"""Linear GraphQL API helper — auto-loads .env, supports pagination."""

import argparse
import io
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

# Prevent Windows cp949 encoding issues
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

API_URL = "https://api.linear.app/graphql"


def load_dotenv():
    """Load environment variables from the project root .env file. Does not overwrite existing variables."""
    path = Path(__file__).resolve().parent
    while path != path.parent:
        env_path = path / ".env"
        if env_path.is_file():
            with open(env_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip("\"'")
                    if key not in os.environ:
                        os.environ[key] = value
            return
        path = path.parent


def get_api_key():
    load_dotenv()
    key = os.environ.get("LINEAR_API_KEY", "")
    if not key:
        print(
            "ERROR: LINEAR_API_KEY is not set.\n"
            "\n"
            "Create a .env file in the project root and add:\n"
            "  LINEAR_API_KEY=lin_api_...\n"
            "\n"
            "You can generate an API key at Linear > Settings > API > Personal API keys.",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def graphql_request(query, variables, api_key):
    payload = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": api_key,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def paginate(query, variables, field, api_key):
    all_nodes = []
    variables = dict(variables)
    while True:
        result = graphql_request(query, variables, api_key)
        if "errors" in result:
            print(json.dumps(result["errors"], indent=2), file=sys.stderr)
            sys.exit(1)

        data = result["data"][field]
        nodes = data.get("nodes", [])
        all_nodes.extend(nodes)

        page_info = data.get("pageInfo", {})
        if not page_info.get("hasNextPage", False):
            break
        variables["after"] = page_info["endCursor"]

    return all_nodes


def main():
    parser = argparse.ArgumentParser(description="Linear GraphQL API helper")
    parser.add_argument("--query", required=True, help="GraphQL query string")
    parser.add_argument("--variables", default="{}", help="JSON variables")
    parser.add_argument(
        "--paginate",
        default=None,
        help="Top-level field name to paginate (expects nodes/pageInfo)",
    )
    args = parser.parse_args()

    api_key = get_api_key()
    variables = json.loads(args.variables)

    if args.paginate:
        nodes = paginate(args.query, variables, args.paginate, api_key)
        print(json.dumps(nodes, indent=2, ensure_ascii=False))
    else:
        result = graphql_request(args.query, variables, api_key)
        if "errors" in result:
            print(json.dumps(result["errors"], indent=2), file=sys.stderr)
            sys.exit(1)
        print(json.dumps(result["data"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
