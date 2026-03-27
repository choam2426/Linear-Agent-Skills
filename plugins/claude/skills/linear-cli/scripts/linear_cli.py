"""Linear CLI — agent-optimized CLI for the Linear GraphQL API."""

import argparse
import io
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path
from urllib.parse import urlparse, unquote

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

API_URL = "https://api.linear.app/graphql"


# --- Infrastructure ---

def load_dotenv():
    path = Path.cwd()
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


def error_exit(message, details=None):
    err = {"error": message}
    if details:
        err["details"] = details
    print(json.dumps(err, ensure_ascii=False), file=sys.stderr)
    sys.exit(1)


def get_api_key():
    load_dotenv()
    key = os.environ.get("LINEAR_API_KEY", "")
    if not key:
        error_exit("LINEAR_API_KEY not set")
    return key


def graphql_request(query, variables, api_key):
    payload = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={"Authorization": api_key, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            details = json.loads(body)
        except json.JSONDecodeError:
            details = body
        error_exit(f"HTTP {e.code}", details)


def paginate(query, variables, field, api_key):
    all_nodes = []
    variables = dict(variables)
    while True:
        result = graphql_request(query, variables, api_key)
        if "errors" in result:
            error_exit("GraphQL error", result["errors"])
        data = result["data"][field]
        all_nodes.extend(data.get("nodes", []))
        page_info = data.get("pageInfo", {})
        if not page_info.get("hasNextPage", False):
            break
        variables["after"] = page_info["endCursor"]
    return all_nodes


def parse_json(text, label="--input"):
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        error_exit(f"Invalid JSON in {label}: {e.msg} at pos {e.pos}")


def out(data):
    print(json.dumps(data, ensure_ascii=False))


def handle(result):
    if "errors" in result:
        error_exit("GraphQL error", result["errors"])
    out(result["data"])


# --- Issues ---

def cmd_get_issue(args, api_key):
    query = """query($id: String!) {
      issue(id: $id) {
        id identifier title description
        state { name type }
        assignee { name email }
        labels { nodes { name } }
        priority
        project { name }
        team { name key }
        updatedAt dueDate estimate url
        attachments { nodes { id title url } }
        parent { id identifier title }
        children { nodes { id identifier title state { name } priority } }
      }
    }"""
    handle(graphql_request(query, {"id": args.id}, api_key))


def cmd_list_issues(args, api_key):
    filt = parse_json(args.filter, "--filter") if args.filter else {}
    if args.team:
        filt["team"] = {"name": {"eq": args.team}}
    if args.state:
        filt["state"] = {"name": {"eq": args.state}}
    if args.assignee:
        filt["assignee"] = {"name": {"containsIgnoreCase": args.assignee}}
    if args.label:
        filt["labels"] = {"name": {"eq": args.label}}
    if args.project:
        filt["project"] = {"name": {"eq": args.project}}
    if args.priority is not None:
        filt["priority"] = {"eq": args.priority}
    if args.parent_id:
        filt["parent"] = {"id": {"eq": args.parent_id}}

    query = """query($filter: IssueFilter, $first: Int, $after: String) {
      issues(filter: $filter, first: $first, after: $after, orderBy: updatedAt) {
        nodes {
          id identifier title
          state { name } assignee { name }
          priority team { key } updatedAt
        }
        pageInfo { hasNextPage endCursor }
      }
    }"""
    out(paginate(query, {"filter": filt, "first": 50}, "issues", api_key))


def cmd_create_issue(args, api_key):
    inp = {"title": args.title, "teamId": args.team_id}
    if args.description:
        inp["description"] = args.description
    if args.priority is not None:
        inp["priority"] = args.priority
    if args.assignee_id:
        inp["assigneeId"] = args.assignee_id
    if args.label_ids:
        inp["labelIds"] = args.label_ids.split(",")
    if args.state_id:
        inp["stateId"] = args.state_id
    if args.estimate is not None:
        inp["estimate"] = args.estimate
    if args.due_date:
        inp["dueDate"] = args.due_date
    if args.project_id:
        inp["projectId"] = args.project_id
    if args.cycle_id:
        inp["cycleId"] = args.cycle_id
    if args.parent_id:
        inp["parentId"] = args.parent_id

    query = """mutation($input: IssueCreateInput!) {
      issueCreate(input: $input) {
        success
        issue { id identifier title url }
      }
    }"""
    handle(graphql_request(query, {"input": inp}, api_key))


def cmd_update_issue(args, api_key):
    query = """mutation($id: String!, $input: IssueUpdateInput!) {
      issueUpdate(id: $id, input: $input) {
        success
        issue { id identifier title state { name } assignee { name } priority url }
      }
    }"""
    handle(graphql_request(query, {"id": args.id, "input": parse_json(args.input)}, api_key))


def cmd_list_sub_issues(args, api_key):
    query = """query($id: String!) {
      issue(id: $id) {
        id identifier title
        children {
          nodes {
            id identifier title
            state { name } assignee { name }
            priority team { key } updatedAt
          }
        }
      }
    }"""
    handle(graphql_request(query, {"id": args.id}, api_key))


def cmd_add_sub_issue(args, api_key):
    query = """mutation($id: String!, $input: IssueUpdateInput!) {
      issueUpdate(id: $id, input: $input) {
        success
        issue { id identifier title parent { id identifier title } url }
      }
    }"""
    handle(graphql_request(query, {"id": args.issue_id, "input": {"parentId": args.parent_id}}, api_key))


def cmd_remove_sub_issue(args, api_key):
    query = """mutation($id: String!, $input: IssueUpdateInput!) {
      issueUpdate(id: $id, input: $input) {
        success
        issue { id identifier title url }
      }
    }"""
    handle(graphql_request(query, {"id": args.issue_id, "input": {"parentId": None}}, api_key))


# --- Documents ---

def cmd_get_document(args, api_key):
    query = """query($id: String!) {
      document(id: $id) {
        id title content
        project { name }
        creator { name }
        updatedAt
      }
    }"""
    handle(graphql_request(query, {"id": args.id}, api_key))


def cmd_list_documents(args, api_key):
    query = """query($first: Int, $after: String) {
      documents(first: $first, after: $after, orderBy: updatedAt) {
        nodes {
          id title
          project { name }
          creator { name }
          updatedAt
        }
        pageInfo { hasNextPage endCursor }
      }
    }"""
    out(paginate(query, {"first": 50}, "documents", api_key))


def cmd_create_document(args, api_key):
    inp = {"title": args.title, "content": args.content}
    if args.project_id:
        inp["projectId"] = args.project_id
    if args.issue_id:
        inp["issueId"] = args.issue_id
    if args.team_id:
        inp["teamId"] = args.team_id
    if not any(k in inp for k in ("projectId", "issueId", "teamId")):
        error_exit("Missing required: one of --project-id, --issue-id, or --team-id")

    query = """mutation($input: DocumentCreateInput!) {
      documentCreate(input: $input) {
        success
        document { id title url }
      }
    }"""
    handle(graphql_request(query, {"input": inp}, api_key))


def cmd_update_document(args, api_key):
    query = """mutation($id: String!, $input: DocumentUpdateInput!) {
      documentUpdate(id: $id, input: $input) {
        success
        document { id title url updatedAt }
      }
    }"""
    handle(graphql_request(query, {"id": args.id, "input": parse_json(args.input)}, api_key))


# --- Projects ---

def cmd_get_project(args, api_key):
    if args.name:
        query = """query($filter: ProjectFilter) {
          projects(filter: $filter, first: 1) {
            nodes {
              id name description state
              startDate targetDate progress
              lead { name email }
              teams(first: 10) { nodes { name key } }
              members(first: 10) { nodes { name email } }
              projectMilestones(first: 20) { nodes { id name targetDate } }
              documents(first: 20) { nodes { id title } }
            }
          }
        }"""
        handle(graphql_request(query, {"filter": {"name": {"eq": args.name}}}, api_key))
    else:
        query = """query($id: String!) {
          project(id: $id) {
            id name description state
            startDate targetDate progress
            lead { name email }
            teams(first: 10) { nodes { name key } }
            members(first: 50) { nodes { name email } }
            projectMilestones(first: 50) { nodes { id name targetDate } }
            documents(first: 50) { nodes { id title } }
          }
        }"""
        handle(graphql_request(query, {"id": args.id}, api_key))


def cmd_list_projects(args, api_key):
    filt = parse_json(args.filter, "--filter") if args.filter else {}
    if args.team:
        filt["accessibleTeams"] = {"some": {"name": {"eq": args.team}}}
    if args.state:
        filt["state"] = {"eq": args.state}
    if args.lead:
        filt["lead"] = {"name": {"containsIgnoreCase": args.lead}}

    query = """query($first: Int, $after: String, $filter: ProjectFilter) {
      projects(first: $first, after: $after, filter: $filter, orderBy: updatedAt) {
        nodes {
          id name description state
          startDate targetDate progress
          lead { name }
          teams { nodes { name key } }
        }
        pageInfo { hasNextPage endCursor }
      }
    }"""
    out(paginate(query, {"first": 50, "filter": filt}, "projects", api_key))


def cmd_save_project(args, api_key):
    inp = parse_json(args.input)
    if args.id:
        query = """mutation($id: String!, $input: ProjectUpdateInput!) {
          projectUpdate(id: $id, input: $input) {
            success
            project { id name state url }
          }
        }"""
        handle(graphql_request(query, {"id": args.id, "input": inp}, api_key))
    else:
        query = """mutation($input: ProjectCreateInput!) {
          projectCreate(input: $input) {
            success
            project { id name url }
          }
        }"""
        handle(graphql_request(query, {"input": inp}, api_key))


# --- Teams ---

def cmd_get_team(args, api_key):
    if args.name:
        query = """query($filter: TeamFilter) {
          teams(filter: $filter) {
            nodes {
              id name key description
              members(first: 20) { nodes { id name email } }
              states { nodes { id name type } }
              labels(first: 20) { nodes { id name } }
            }
          }
        }"""
        handle(graphql_request(query, {"filter": {"name": {"eq": args.name}}}, api_key))
    else:
        query = """query($id: String!) {
          team(id: $id) {
            id name key description
            members(first: 20) { nodes { id name email } }
            states { nodes { id name type } }
            labels(first: 20) { nodes { id name } }
          }
        }"""
        handle(graphql_request(query, {"id": args.id}, api_key))


def cmd_list_teams(args, api_key):
    query = """{ teams {
      nodes {
        id name key
        states { nodes { id name type } }
      }
    } }"""
    handle(graphql_request(query, {}, api_key))


# --- Users ---

def cmd_get_user(args, api_key):
    if args.me:
        query = """{ viewer {
          id name email active admin
          teams { nodes { name key } }
        } }"""
        handle(graphql_request(query, {}, api_key))
    elif args.name:
        query = """query($filter: UserFilter) {
          users(filter: $filter) {
            nodes { id name email active admin teams { nodes { name key } } }
          }
        }"""
        handle(graphql_request(query, {"filter": {"name": {"containsIgnoreCase": args.name}}}, api_key))
    elif args.email:
        query = """query($filter: UserFilter) {
          users(filter: $filter) {
            nodes { id name email active admin teams { nodes { name key } } }
          }
        }"""
        handle(graphql_request(query, {"filter": {"email": {"containsIgnoreCase": args.email}}}, api_key))
    else:
        query = """query($id: String!) {
          user(id: $id) {
            id name email active admin
            teams { nodes { name key } }
          }
        }"""
        handle(graphql_request(query, {"id": args.id}, api_key))


def cmd_list_users(args, api_key):
    if args.name or args.email:
        filt = {}
        if args.name:
            filt["name"] = {"containsIgnoreCase": args.name}
        if args.email:
            filt["email"] = {"containsIgnoreCase": args.email}
        query = """query($filter: UserFilter) {
          users(filter: $filter) {
            nodes { id name email active admin teams { nodes { name key } } }
          }
        }"""
        handle(graphql_request(query, {"filter": filt}, api_key))
    else:
        query = """query($first: Int, $after: String) {
          users(first: $first, after: $after, orderBy: updatedAt) {
            nodes { id name email active admin teams { nodes { name key } } }
            pageInfo { hasNextPage endCursor }
          }
        }"""
        out(paginate(query, {"first": 50}, "users", api_key))


# --- Comments ---

def cmd_list_comments(args, api_key):
    query = """query($id: String!) {
      issue(id: $id) {
        id identifier title
        comments(orderBy: createdAt) {
          nodes {
            id body createdAt updatedAt
            user { name }
            parent { id }
          }
        }
      }
    }"""
    handle(graphql_request(query, {"id": args.issue_id}, api_key))


def cmd_save_comment(args, api_key):
    inp = parse_json(args.input)
    if args.id:
        query = """mutation($id: String!, $input: CommentUpdateInput!) {
          commentUpdate(id: $id, input: $input) {
            success
            comment { id body updatedAt }
          }
        }"""
        handle(graphql_request(query, {"id": args.id, "input": inp}, api_key))
    else:
        query = """mutation($input: CommentCreateInput!) {
          commentCreate(input: $input) {
            success
            comment { id body createdAt url user { name } }
          }
        }"""
        handle(graphql_request(query, {"input": inp}, api_key))


def cmd_delete_comment(args, api_key):
    query = """mutation($id: String!) {
      commentDelete(id: $id) { success }
    }"""
    handle(graphql_request(query, {"id": args.id}, api_key))


# --- Labels ---

def cmd_list_issue_labels(args, api_key):
    filt_arg = {"first": 50}
    if args.team:
        filt_arg["filter"] = {"team": {"name": {"eq": args.team}}}
    query = """query($first: Int, $after: String, $filter: IssueLabelFilter) {
      issueLabels(first: $first, after: $after, filter: $filter, orderBy: updatedAt) {
        nodes {
          id name
          parent { id name }
          team { name key }
        }
        pageInfo { hasNextPage endCursor }
      }
    }"""
    out(paginate(query, filt_arg, "issueLabels", api_key))


def cmd_create_issue_label(args, api_key):
    inp = {"name": args.name}
    if args.color:
        inp["color"] = args.color
    if args.team_id:
        inp["teamId"] = args.team_id
    if args.description:
        inp["description"] = args.description

    query = """mutation($input: IssueLabelCreateInput!) {
      issueLabelCreate(input: $input) {
        success
        issueLabel { id name }
      }
    }"""
    handle(graphql_request(query, {"input": inp}, api_key))


def cmd_list_project_labels(args, api_key):
    query = """query($first: Int, $after: String) {
      projectLabels(first: $first, after: $after) {
        nodes { id name }
        pageInfo { hasNextPage endCursor }
      }
    }"""
    out(paginate(query, {"first": 50}, "projectLabels", api_key))


# --- Workflow ---

def cmd_get_issue_status(args, api_key):
    if args.team:
        query = """query($filter: TeamFilter) {
          teams(filter: $filter) {
            nodes {
              id name key
              states { nodes { id name type } }
            }
          }
        }"""
        handle(graphql_request(query, {"filter": {"name": {"eq": args.team}}}, api_key))
    else:
        query = """query($id: String!) {
          workflowState(id: $id) {
            id name type
            team { name key }
          }
        }"""
        handle(graphql_request(query, {"id": args.id}, api_key))


def cmd_list_issue_statuses(args, api_key):
    if args.name:
        query = """query($filter: TeamFilter) {
          teams(filter: $filter) {
            nodes {
              id name key
              states { nodes { id name type } }
            }
          }
        }"""
        handle(graphql_request(query, {"filter": {"name": {"eq": args.name}}}, api_key))
    else:
        query = """query($id: String!) {
          team(id: $id) {
            id name key
            states { nodes { id name type } }
          }
        }"""
        handle(graphql_request(query, {"id": args.team}, api_key))


def cmd_save_issue_status(args, api_key):
    inp = parse_json(args.input)
    if args.id:
        query = """mutation($id: String!, $input: WorkflowStateUpdateInput!) {
          workflowStateUpdate(id: $id, input: $input) {
            success
            workflowState { id name type color position description team { name key } }
          }
        }"""
        handle(graphql_request(query, {"id": args.id, "input": inp}, api_key))
    else:
        query = """mutation($input: WorkflowStateCreateInput!) {
          workflowStateCreate(input: $input) {
            success
            workflowState { id name type color position description team { name key } }
          }
        }"""
        handle(graphql_request(query, {"input": inp}, api_key))


def cmd_delete_issue_status(args, api_key):
    query = """mutation($id: String!) {
      workflowStateArchive(id: $id) { success }
    }"""
    handle(graphql_request(query, {"id": args.id}, api_key))


def cmd_list_cycles(args, api_key):
    if args.name:
        query = """query($filter: TeamFilter) {
          teams(filter: $filter) {
            nodes {
              id name
              cycles { nodes { id number name startsAt endsAt completedAt progress } }
            }
          }
        }"""
        handle(graphql_request(query, {"filter": {"name": {"eq": args.name}}}, api_key))
    else:
        query = """query($id: String!) {
          team(id: $id) {
            id name
            cycles { nodes { id number name startsAt endsAt completedAt progress } }
          }
        }"""
        handle(graphql_request(query, {"id": args.team}, api_key))


# --- Milestones ---

def cmd_get_milestone(args, api_key):
    if args.project:
        query = """query($filter: ProjectFilter) {
          projects(filter: $filter) {
            nodes {
              id name
              projectMilestones { nodes { id name description targetDate sortOrder } }
            }
          }
        }"""
        handle(graphql_request(query, {"filter": {"name": {"eq": args.project}}}, api_key))
    else:
        query = """query($id: String!) {
          projectMilestone(id: $id) {
            id name description targetDate sortOrder
            project { id name }
          }
        }"""
        handle(graphql_request(query, {"id": args.id}, api_key))


def cmd_list_milestones(args, api_key):
    if args.name:
        query = """query($filter: ProjectFilter) {
          projects(filter: $filter) {
            nodes {
              id name
              projectMilestones { nodes { id name description targetDate sortOrder } }
            }
          }
        }"""
        handle(graphql_request(query, {"filter": {"name": {"eq": args.name}}}, api_key))
    else:
        query = """query($id: String!) {
          project(id: $id) {
            id name
            projectMilestones { nodes { id name description targetDate sortOrder } }
          }
        }"""
        handle(graphql_request(query, {"id": args.project}, api_key))


def cmd_save_milestone(args, api_key):
    inp = parse_json(args.input)
    if args.id:
        query = """mutation($id: String!, $input: ProjectMilestoneUpdateInput!) {
          projectMilestoneUpdate(id: $id, input: $input) {
            success
            projectMilestone { id name description targetDate }
          }
        }"""
        handle(graphql_request(query, {"id": args.id, "input": inp}, api_key))
    else:
        query = """mutation($input: ProjectMilestoneCreateInput!) {
          projectMilestoneCreate(input: $input) {
            success
            projectMilestone { id name description targetDate }
          }
        }"""
        handle(graphql_request(query, {"input": inp}, api_key))


# --- Attachments ---

def cmd_get_attachment(args, api_key):
    query = """query($id: String!) {
      attachment(id: $id) {
        id title subtitle url
        updatedAt
        issue { id identifier title }
      }
    }"""
    handle(graphql_request(query, {"id": args.id}, api_key))


def cmd_create_attachment(args, api_key):
    inp = {"issueId": args.issue_id, "url": args.url}
    if args.title:
        inp["title"] = args.title
    if args.subtitle:
        inp["subtitle"] = args.subtitle

    query = """mutation($input: AttachmentCreateInput!) {
      attachmentCreate(input: $input) {
        success
        attachment { id title url }
      }
    }"""
    handle(graphql_request(query, {"input": inp}, api_key))


def cmd_delete_attachment(args, api_key):
    query = """mutation($id: String!) {
      attachmentDelete(id: $id) { success }
    }"""
    handle(graphql_request(query, {"id": args.id}, api_key))


MIME_TYPES = {
    ".txt": "text/plain", ".md": "text/markdown", ".csv": "text/csv",
    ".json": "application/json", ".xml": "application/xml",
    ".pdf": "application/pdf", ".zip": "application/zip",
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".gif": "image/gif", ".svg": "image/svg+xml", ".webp": "image/webp",
    ".mp4": "video/mp4", ".webm": "video/webm",
    ".html": "text/html", ".css": "text/css", ".js": "application/javascript",
    ".py": "text/x-python", ".log": "text/plain",
}


def cmd_upload_file(args, api_key):
    file_path = Path(args.file)
    if not file_path.is_file():
        error_exit(f"File not found: {file_path}")

    file_size = file_path.stat().st_size
    content_type = MIME_TYPES.get(file_path.suffix.lower(), "application/octet-stream")
    filename = file_path.name

    # Step 1: Request presigned upload URL
    query = """mutation($size: Int!, $contentType: String!, $filename: String!) {
      fileUpload(size: $size, contentType: $contentType, filename: $filename) {
        success
        uploadFile { uploadUrl assetUrl headers { key value } }
      }
    }"""
    result = graphql_request(query, {
        "size": file_size, "contentType": content_type, "filename": filename,
    }, api_key)
    if "errors" in result:
        error_exit("GraphQL error", result["errors"])

    upload_info = result["data"]["fileUpload"]["uploadFile"]
    upload_url = upload_info["uploadUrl"]
    asset_url = upload_info["assetUrl"]
    headers = {h["key"]: h["value"] for h in upload_info["headers"]}
    headers["Content-Type"] = content_type

    # Step 2: PUT file to presigned URL
    file_data = file_path.read_bytes()
    req = urllib.request.Request(upload_url, data=file_data, method="PUT")
    for k, v in headers.items():
        req.add_header(k, v)
    try:
        urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        error_exit(f"Upload failed: HTTP {e.code}")

    out({"success": True, "assetUrl": asset_url, "filename": filename, "size": file_size})


def _download_to(url, output_path, api_key):
    """Download a URL, trying with auth first then without."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"Authorization": api_key})
    try:
        with urllib.request.urlopen(req) as resp:
            with open(output_path, "wb") as f:
                while True:
                    chunk = resp.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
    except urllib.error.HTTPError:
        req = urllib.request.Request(url)
        try:
            with urllib.request.urlopen(req) as resp:
                with open(output_path, "wb") as f:
                    while True:
                        chunk = resp.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)
        except urllib.error.HTTPError as e:
            error_exit(f"Download failed: HTTP {e.code}")
    return output_path


def cmd_download_file(args, api_key):
    url = args.url
    if args.output:
        output_path = Path(args.output)
    else:
        parsed = urlparse(url)
        filename = unquote(Path(parsed.path).name) or "download"
        output_path = Path.cwd() / filename

    result_path = _download_to(url, output_path, api_key)
    out({"success": True, "path": str(result_path.resolve()), "size": result_path.stat().st_size})



# --- Argparse ---

def build_parser():
    parser = argparse.ArgumentParser(prog="linear-cli")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("get-issue")
    p.add_argument("--id", required=True)

    p = sub.add_parser("list-issues")
    p.add_argument("--filter")
    p.add_argument("--team")
    p.add_argument("--state")
    p.add_argument("--assignee")
    p.add_argument("--label")
    p.add_argument("--project")
    p.add_argument("--priority", type=int)
    p.add_argument("--parent-id")

    p = sub.add_parser("create-issue")
    p.add_argument("--title", required=True)
    p.add_argument("--team-id", required=True)
    p.add_argument("--description")
    p.add_argument("--priority", type=int)
    p.add_argument("--assignee-id")
    p.add_argument("--label-ids")
    p.add_argument("--state-id")
    p.add_argument("--estimate", type=int)
    p.add_argument("--due-date")
    p.add_argument("--project-id")
    p.add_argument("--cycle-id")
    p.add_argument("--parent-id")

    p = sub.add_parser("update-issue")
    p.add_argument("--id", required=True)
    p.add_argument("--input", required=True)

    p = sub.add_parser("list-sub-issues")
    p.add_argument("--id", required=True)

    p = sub.add_parser("add-sub-issue")
    p.add_argument("--parent-id", required=True)
    p.add_argument("--issue-id", required=True)

    p = sub.add_parser("remove-sub-issue")
    p.add_argument("--issue-id", required=True)

    p = sub.add_parser("get-document")
    p.add_argument("--id", required=True)

    sub.add_parser("list-documents")

    p = sub.add_parser("create-document")
    p.add_argument("--title", required=True)
    p.add_argument("--content", required=True)
    p.add_argument("--project-id")
    p.add_argument("--issue-id")
    p.add_argument("--team-id")

    p = sub.add_parser("update-document")
    p.add_argument("--id", required=True)
    p.add_argument("--input", required=True)

    p = sub.add_parser("get-project")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--id")
    g.add_argument("--name")

    p = sub.add_parser("list-projects")
    p.add_argument("--filter")
    p.add_argument("--team")
    p.add_argument("--state")
    p.add_argument("--lead")

    p = sub.add_parser("save-project")
    p.add_argument("--id")
    p.add_argument("--input", required=True)

    p = sub.add_parser("get-team")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--id")
    g.add_argument("--name")

    sub.add_parser("list-teams")

    p = sub.add_parser("get-user")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--id")
    g.add_argument("--name")
    g.add_argument("--email")
    g.add_argument("--me", action="store_true")

    p = sub.add_parser("list-users")
    p.add_argument("--name")
    p.add_argument("--email")

    p = sub.add_parser("list-comments")
    p.add_argument("--issue-id", required=True)

    p = sub.add_parser("save-comment")
    p.add_argument("--id")
    p.add_argument("--input", required=True)

    p = sub.add_parser("delete-comment")
    p.add_argument("--id", required=True)

    p = sub.add_parser("list-issue-labels")
    p.add_argument("--team")

    p = sub.add_parser("create-issue-label")
    p.add_argument("--name", required=True)
    p.add_argument("--color")
    p.add_argument("--team-id")
    p.add_argument("--description")

    sub.add_parser("list-project-labels")

    p = sub.add_parser("get-issue-status")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--id")
    g.add_argument("--team")

    p = sub.add_parser("list-issue-statuses")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--team")
    g.add_argument("--name")

    p = sub.add_parser("save-issue-status")
    p.add_argument("--id")
    p.add_argument("--input", required=True)

    p = sub.add_parser("delete-issue-status")
    p.add_argument("--id", required=True)

    p = sub.add_parser("list-cycles")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--team")
    g.add_argument("--name")

    p = sub.add_parser("get-milestone")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--id")
    g.add_argument("--project")

    p = sub.add_parser("list-milestones")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--project")
    g.add_argument("--name")

    p = sub.add_parser("save-milestone")
    p.add_argument("--id")
    p.add_argument("--input", required=True)

    p = sub.add_parser("get-attachment")
    p.add_argument("--id", required=True)

    p = sub.add_parser("create-attachment")
    p.add_argument("--issue-id", required=True)
    p.add_argument("--url", required=True)
    p.add_argument("--title")
    p.add_argument("--subtitle")

    p = sub.add_parser("delete-attachment")
    p.add_argument("--id", required=True)

    p = sub.add_parser("upload-file")
    p.add_argument("--file", required=True)

    p = sub.add_parser("download-file")
    p.add_argument("--url", required=True)
    p.add_argument("--output")

    return parser


COMMAND_MAP = {
    "get-issue": cmd_get_issue,
    "list-issues": cmd_list_issues,
    "create-issue": cmd_create_issue,
    "update-issue": cmd_update_issue,
    "list-sub-issues": cmd_list_sub_issues,
    "add-sub-issue": cmd_add_sub_issue,
    "remove-sub-issue": cmd_remove_sub_issue,
    "get-document": cmd_get_document,
    "list-documents": cmd_list_documents,
    "create-document": cmd_create_document,
    "update-document": cmd_update_document,
    "get-project": cmd_get_project,
    "list-projects": cmd_list_projects,
    "save-project": cmd_save_project,
    "get-team": cmd_get_team,
    "list-teams": cmd_list_teams,
    "get-user": cmd_get_user,
    "list-users": cmd_list_users,
    "list-comments": cmd_list_comments,
    "save-comment": cmd_save_comment,
    "delete-comment": cmd_delete_comment,
    "list-issue-labels": cmd_list_issue_labels,
    "create-issue-label": cmd_create_issue_label,
    "list-project-labels": cmd_list_project_labels,
    "get-issue-status": cmd_get_issue_status,
    "list-issue-statuses": cmd_list_issue_statuses,
    "save-issue-status": cmd_save_issue_status,
    "delete-issue-status": cmd_delete_issue_status,
    "list-cycles": cmd_list_cycles,
    "get-milestone": cmd_get_milestone,
    "list-milestones": cmd_list_milestones,
    "save-milestone": cmd_save_milestone,
    "get-attachment": cmd_get_attachment,
    "create-attachment": cmd_create_attachment,
    "delete-attachment": cmd_delete_attachment,
    "upload-file": cmd_upload_file,
    "download-file": cmd_download_file,
}


def main():
    parser = build_parser()
    args = parser.parse_args()
    api_key = get_api_key()
    COMMAND_MAP[args.command](args, api_key)


if __name__ == "__main__":
    main()
