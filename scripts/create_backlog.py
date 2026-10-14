#!/usr/bin/env python3
"""
Fill a GitHub Project (created from the "Iterative development" template) with the
MLME product backlog from backlog/backlog.csv.

Recommended flow (matches the class demo):
  1. On GitHub create a Project from the "Iterative development" template, fill in its
     name, default repository, short description and README in Project settings, and set
     the Iteration field so Iteration 1 starts on 19 Oct and Iteration 2 on 26 Oct
     (duration 1 week). Note the project number from its URL (.../projects/<N>).
  2. Run this script with --project-number <N>.

For every backlog row the script creates an issue in the repo (title, user story,
acceptance criteria, labels, milestone, assignee), adds it to the Project and sets the
template fields:
  Status    -> Backlog
  Priority  -> P0 (High) / P1 (Medium) / P2 (Low)
  Size      -> XS (1 SP) / S (2) / M (3) / L (5) / XL (8)
  Estimate  -> story points
  Iteration -> the iteration containing 19 Oct (Sprint 1) or 26 Oct (Sprint 2)
It also adds a text field "Requirement" (FR/NFR/SR IDs). Re-running is safe: issues whose
title already exists are skipped.

If no --project-number is given, a blank project is created instead and the missing
fields (Priority, Size, Estimate, and a "Sprint" select in place of Iteration) are added.

Prerequisites:
  - GitHub CLI: https://cli.github.com   then:  gh auth login   and   gh auth refresh -s project
  - People you assign must be collaborators on the repo (or map every name to your own username)

Usage (from the repo root):
  python scripts/create_backlog.py --repo <owner>/<repo> --project-number <N> \
      --users "Shreya=<gh-user>,Sneha=<gh-user>,Sukhmeet=<gh-user>" [--dry-run]
"""
import argparse
import csv
import datetime as dt
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "backlog" / "backlog.csv"
PROJECT_TITLE = "Web Based ML Model Evaluator"

SPRINT_DATES = {"Sprint 1": dt.date(2026, 10, 19), "Sprint 2": dt.date(2026, 10, 26)}
PRIORITY_MAP = {"High": "P0", "Medium": "P1", "Low": "P2"}
SIZE_MAP = {1: "XS", 2: "S", 3: "M", 5: "L", 8: "XL"}

MILESTONES = {
    "Sprint 1": ("2026-10-23T23:59:59Z",
                 "Working product: register, upload, configure, train, view metrics (19-23 Oct)"),
    "Sprint 2": ("2026-10-30T23:59:59Z",
                 "Compare, export, history, admin/audit, security hardening, NFR testing, docs (26-30 Oct)"),
}

LABELS = {
    "type:story": ("1d76db", "User story derived from a functional requirement"),
    "type:task": ("5319e7", "Technical / process task"),
    "type:security": ("b60205", "Security requirement (SR-xx)"),
    "type:nfr": ("fbca04", "Non-functional requirement (NFR-xx)"),
    "priority:high": ("d93f0b", "High priority"),
    "priority:medium": ("fef2c0", "Medium priority"),
    "priority:low": ("c2e0c6", "Low priority"),
    "sprint-1": ("0e8a16", "Planned for Sprint 1 (19-23 Oct)"),
    "sprint-2": ("006b75", "Planned for Sprint 2 (26-30 Oct)"),
}

ITERATION_QUERY = """
query($id: ID!) {
  node(id: $id) {
    ... on ProjectV2IterationField {
      configuration {
        iterations { id title startDate duration }
        completedIterations { id title startDate duration }
      }
    }
  }
}"""

DRY = False


def run(args, check=True):
    """Run a gh command (or print it in dry-run mode) and return stdout."""
    printable = " ".join(f'"{a}"' if " " in a else a for a in args)
    if DRY:
        print("[dry-run]", printable[:200] + ("..." if len(printable) > 200 else ""))
        return ""
    res = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    if check and res.returncode != 0:
        sys.exit(f"Command failed: {printable[:300]}\n{res.stderr}")
    return res.stdout.strip()


def issue_body(row):
    criteria = "\n".join(f"- [ ] {c.strip()}" for c in row["Acceptance Criteria"].split("|"))
    return f"""**Backlog ID:** {row['ID']}
**Requirement(s):** {row['Requirements']}
**Story points (Estimate):** {row['Story Points']}  |  **Priority:** {row['Priority']}  |  **Sprint:** {row['Sprint']}
**Design components:** {row['Components']}
**Test cases (Test Plan Section 8):** {row['Test Cases']}
**Depends on:** {row['Depends On'] or '-'}

### User story
{row['User Story']}

### Acceptance criteria
{criteria}

### Definition of Done
- [ ] Code on a feature branch `feature/{row['ID'].lower()}-...`, PR raised by the assignee with `Closes #<this issue>`
- [ ] CI (lint + tests) green
- [ ] Unit tests added/updated for new logic
- [ ] PR reviewed and merged by the repo owner
- [ ] Any deviation from SRS/SAD/Test Plan noted in `docs/6_Deviations_Log.md`
"""


def ensure_labels(repo):
    for name, (color, desc) in LABELS.items():
        run(["gh", "label", "create", name, "--repo", repo, "--color", color,
             "--description", desc, "--force"])


def ensure_milestones(repo):
    existing = set()
    if not DRY:
        out = run(["gh", "api", f"repos/{repo}/milestones?state=all&per_page=100"])
        existing = {m["title"] for m in json.loads(out or "[]")}
    for title, (due, desc) in MILESTONES.items():
        if title in existing:
            print(f"  milestone exists: {title}")
            continue
        run(["gh", "api", f"repos/{repo}/milestones", "-f", f"title={title}",
             "-f", f"due_on={due}", "-f", f"description={desc}"])


def ensure_project(owner, repo, number):
    if number is None:
        out = run(["gh", "project", "create", "--owner", owner, "--title", PROJECT_TITLE, "--format", "json"])
        number = json.loads(out)["number"] if out else 0
        print(f"  created blank project #{number} (tip: the 'Iterative development' template matches the demo)")
    run(["gh", "project", "link", str(number), "--owner", owner, "--repo", repo], check=False)
    project_id = ""
    if not DRY:
        project_id = json.loads(run(["gh", "project", "view", str(number), "--owner", owner,
                                     "--format", "json"]))["id"]
    return number, project_id


def list_fields(owner, number):
    if DRY:
        return {}
    data = json.loads(run(["gh", "project", "field-list", str(number), "--owner", owner,
                           "--format", "json", "--limit", "100"]))
    return {f["name"]: f for f in data["fields"]}


def ensure_fields(owner, number):
    fields = list_fields(owner, number)
    wanted = {
        "Priority": ["--data-type", "SINGLE_SELECT", "--single-select-options", "P0,P1,P2"],
        "Size": ["--data-type", "SINGLE_SELECT", "--single-select-options", "XS,S,M,L,XL"],
        "Estimate": ["--data-type", "NUMBER"],
        "Requirement": ["--data-type", "TEXT"],
    }
    if "Iteration" not in fields:
        wanted["Sprint"] = ["--data-type", "SINGLE_SELECT", "--single-select-options", "Sprint 1,Sprint 2"]
    for name, extra in wanted.items():
        if name not in fields:
            run(["gh", "project", "field-create", str(number), "--owner", owner, "--name", name] + extra)
            print(f"  added field: {name}")
    return list_fields(owner, number)


def option_id(field, name):
    for o in field.get("options", []):
        if o["name"].lower() == name.lower():
            return o["id"]
    return None


def iteration_ids(field):
    """Map 'Sprint 1'/'Sprint 2' to the iteration whose date range contains its start date."""
    out = run(["gh", "api", "graphql", "-f", f"query={ITERATION_QUERY}", "-f", f"id={field['id']}"])
    conf = json.loads(out)["data"]["node"]["configuration"]
    iters = conf["iterations"] + conf["completedIterations"]
    result = {}
    for sprint, day in SPRINT_DATES.items():
        for it in iters:
            start = dt.date.fromisoformat(it["startDate"])
            if start <= day < start + dt.timedelta(days=it["duration"]):
                result[sprint] = it["id"]
                print(f"  {sprint} -> iteration '{it['title']}' (starts {it['startDate']}, {it['duration']} days)")
                break
        else:
            print(f"  WARNING: no iteration covers {day} for {sprint}. Edit the Iteration field in Project "
                  f"settings (start 19 Oct, 1 week) and re-run, or set it on the board by hand.")
    return result


def main():
    global DRY
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True, help="owner/repo")
    ap.add_argument("--users", required=True,
                    help='Map team names to GitHub usernames: "Shreya=abc,Sneha=def,Sukhmeet=ghi"')
    ap.add_argument("--project-number", type=int, help="Number of the Project created from the template")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    DRY = a.dry_run

    users = dict(pair.strip().split("=", 1) for pair in a.users.split(","))
    owner = a.repo.split("/")[0]
    rows = list(csv.DictReader(open(CSV_PATH, newline="", encoding="utf-8-sig")))
    missing = {r["Assignee"] for r in rows} - users.keys()
    if missing:
        sys.exit(f"--users is missing GitHub usernames for: {', '.join(sorted(missing))}")

    print("1/5 labels")
    ensure_labels(a.repo)
    print("2/5 milestones")
    ensure_milestones(a.repo)
    print("3/5 project")
    number, project_id = ensure_project(owner, a.repo, a.project_number)
    print("4/5 fields")
    fields = ensure_fields(owner, number)
    iters = iteration_ids(fields["Iteration"]) if "Iteration" in fields else {}

    existing_titles = set()
    if not DRY:
        existing_titles = {i["title"] for i in json.loads(run(
            ["gh", "issue", "list", "--repo", a.repo, "--state", "all", "--limit", "500", "--json", "title"]))}

    print(f"5/5 issues ({len(rows)})")
    for r in rows:
        title = f"[{r['ID']}] {r['Title']}"
        if title in existing_titles:
            print(f"  skip (exists): {title}")
            continue
        labels = [f"type:{r['Type'].lower()}", f"priority:{r['Priority'].lower()}",
                  "sprint-1" if r["Sprint"] == "Sprint 1" else "sprint-2"]
        url = run(["gh", "issue", "create", "--repo", a.repo, "--title", title,
                   "--body", issue_body(r), "--label", ",".join(labels),
                   "--assignee", users[r["Assignee"]], "--milestone", r["Sprint"]])
        print(f"  created: {title} {url}")
        item = run(["gh", "project", "item-add", str(number), "--owner", owner,
                    "--url", url or "<url>", "--format", "json"])
        if DRY:
            continue
        item_id = json.loads(item)["id"]
        base = ["gh", "project", "item-edit", "--id", item_id, "--project-id", project_id]
        sp = int(r["Story Points"])

        status = fields.get("Status")
        if status:
            opt = option_id(status, "Backlog") or option_id(status, "Todo")
            if opt:
                run(base + ["--field-id", status["id"], "--single-select-option-id", opt])
        for fname, value in (("Priority", PRIORITY_MAP[r["Priority"]]), ("Size", SIZE_MAP.get(sp, "M"))):
            f = fields.get(fname)
            opt = option_id(f, value) if f else None
            if opt:
                run(base + ["--field-id", f["id"], "--single-select-option-id", opt])
        run(base + ["--field-id", fields["Estimate"]["id"], "--number", str(sp)])
        run(base + ["--field-id", fields["Requirement"]["id"], "--text", r["Requirements"]])
        if r["Sprint"] in iters:
            run(base + ["--field-id", fields["Iteration"]["id"], "--iteration-id", iters[r["Sprint"]]])
        elif "Sprint" in fields:
            opt = option_id(fields["Sprint"], r["Sprint"])
            run(base + ["--field-id", fields["Sprint"]["id"], "--single-select-option-id", opt])

    print("\nDone. Open the Project: items are in the Backlog column with Priority, Size, Estimate "
          "and Iteration filled in.")


if __name__ == "__main__":
    main()
