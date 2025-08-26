#!/usr/bin/env python3
import os, sys, json, subprocess, tempfile
from pathlib import Path
import yaml

REPO = os.environ.get("REPO")
if not REPO:
    print("Set REPO=owner/repo", file=sys.stderr); sys.exit(1)

PROJECT_OWNER = os.environ.get("PROJECT_OWNER")
PROJECT_NUMBER = os.environ.get("PROJECT_NUMBER")

def gh_api(args, input_json=None, input_file=None):
    cmd = ["gh","api"] + args
    if input_json is not None:
        p = subprocess.run(cmd, input=json.dumps(input_json).encode(), capture_output=True, check=True)
    elif input_file is not None:
        p = subprocess.run(cmd + ["--input", input_file], capture_output=True, check=True)
    else:
        p = subprocess.run(cmd, capture_output=True, check=True)
    return json.loads(p.stdout.decode() or "{}")

def create_issue(title, body, labels):
    args = ["-X","POST", f"/repos/{REPO}/issues", "-F", f"title={title}"]
    with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
        tf.write(body or "")
        tf.flush()
        for lab in labels or []:
            args += ["-F", f"labels[]={lab}"]
        data = gh_api(args, input_file=tf.name)
    return {"number": data["number"], "url": data["html_url"]}

def edit_issue(number, body):
    with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
        tf.write(body or "")
        tf.flush()
        gh_api(["-X","PATCH", f"/repos/{REPO}/issues/{number}"], input_file=tf.name)

def add_to_project(issue_url):
    if not (PROJECT_OWNER and PROJECT_NUMBER):
        return
    subprocess.run(["gh","project","item-add","--owner",PROJECT_OWNER,"--project",PROJECT_NUMBER,"--url",issue_url], check=True)

def main(yaml_path):
    data = yaml.safe_load(Path(yaml_path).read_text())
    epic_id_to_num = {}
    children = []

    for epic in data.get("epics", []):
        res = create_issue(epic["title"], epic.get("body",""), epic.get("labels",[]))
        epic_id_to_num[epic["id"]] = res["number"]
        add_to_project(res["url"])
        print(f"[EPIC] #{res['number']} {epic['title']}")

    for it in data.get("issues", []):
        res = create_issue(it["title"], it.get("body",""), it.get("labels",[]))
        add_to_project(res["url"])
        parent = it.get("parent")
        children.append((epic_id_to_num.get(parent), res["number"], it["title"]))
        print(f"[ISSUE] #{res['number']} {it['title']} (parent: {parent})")

    # Update epic bodies with checklists
    per_epic = {}
    for parent_num, child_num, title in children:
        if not parent_num: continue
        per_epic.setdefault(parent_num, []).append((child_num, title))
    for epic_num, kids in per_epic.items():
        epic_json = gh_api([f"/repos/{REPO}/issues/{epic_num}"])
        body = (epic_json.get("body") or "") + "\n\n## Scope\n"
        for num, title in sorted(kids):
            body += f"- [ ] #{num} {title}\n"
        edit_issue(epic_num, body)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/create_issues_from_yaml.py backlog.yml", file=sys.stderr); sys.exit(1)
    main(sys.argv[1])
