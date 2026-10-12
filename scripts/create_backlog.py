#!/usr/bin/env python3
"""
Create the MLME product backlog on GitHub from backlog/backlog.csv.

What it does (idempotent: safe to re-run, existing issues are skipped):
  1. Creates labels (type, priority, sprint)
  2. Creates milestones "Sprint 1" (19-23 Oct) and "Sprint 2" (26-30 Oct)
  3. Creates (or reuses) a GitHub Project and links it to the repo
  4. Adds custom Project fields: Story Points (number), Sprint (single select),
     Requirement (text), Item ID (text)
  5. Creates one issue per backlog row, assigns it, adds it to the Project and
     fills Story Points / Sprint / Requirement / Item ID

Prerequisites:
  - GitHub CLI installed:  https://cli.github.com
  - Logged in with project scope:   gh auth login   then   gh auth refresh -s project
  - All three teammates added as collaborators on the repo (otherwise assigning fails)

Usage (run from the repo root):
  python scripts/create_backlog.py \
      --repo <owner>/<repo> \
      --users "Shreya=<gh-username>,Sneha=<gh-username>,Sukhmeet=<gh-username>" \
      [--project-number N]   # reuse an existing Project instead of creating one
      [--dry-run]            # print the gh commands without running them
"""
import argparse
import csv
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "backlog" / "backlog.csv"
PROJECT_TITLE = "MLME - Web Based ML Model Evaluator"

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

DRY = False


def run(args, capture=True, check=True):
    """Run a gh command; in dry-run mode only print it."""
    printable = " ".join(f'"{a}"' if " " in a else a for a in args)
    if DRY:
        print("[dry-run]", printable)
        return ""
    res = subprocess.run(args, capture_output=capture, text=True)
    if check and res.returncode != 0:
        sys.exit(f"Command failed: {printable}\n{res.stderr}")
    return res.stdout.strip() if capture else ""


def issue_body(row):
    criteria = "\n".join(f"- [ ] {c.strip()}" for c in row["Acceptance Criteria"].split("|"))
    return f"""**Backlog ID:** {row['ID']}
**Requirement(s):** {row['Requirements']}
**Story points:** {row['Story Points']}  |  **Priority:** {row['Priority']}  |  **Sprint:** {row['Sprint']}
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
        print(f"  created project #{number}")
    run(["gh", "project", "link", str(number), "--owner", owner, "--repo", repo], check=False)
    project_id = ""
    if not DRY:
        project_id = json.loads(run(["gh", "project", "view", str(number), "--owner", owner, "--format", "json"]))["id"]
    return number, project_id


def ensure_fields(owner, number):
    wanted = {
        "Story Points": ["--data-type", "NUMBER"],
        "Sprint": ["--data-type", "SINGLE_SELECT", "--single-select-options", "Sprint 1,Sprint 2"],
        "Requirement": ["--data-type", "TEXT"],
        "Item ID": ["--data-type", "TEXT"],
    }
    existing = {}
    if not DRY:
        existing = {f["name"]: f for f in json.loads(run(
            ["gh", "project", "field-list", str(number), "--owner", owner, "--format", "json"]))["fields"]}
    for name, extra in wanted.items():
        if name not in existing:
            run(["gh", "project", "field-create", str(number), "--owner", owner, "--name", name] + extra)
    if DRY:
        return {}
    return {f["name"]: f for f in json.loads(run(
        ["gh", "project", "field-list", str(number), "--owner", owner, "--format", "json"]))["fields"]}


def main():
    global DRY
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True, help="owner/repo")
    ap.add_argument("--users", required=True,
                    help='Map team names to GitHub usernames: "Shreya=abc,Sneha=def,Sukhmeet=ghi"')
    ap.add_argument("--project-number", type=int, help="Existing GitHub Project number to reuse")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    DRY = a.dry_run

    users = dict(pair.split("=", 1) for pair in a.users.split(","))
    owner = a.repo.split("/")[0]
    rows = list(csv.DictReader(open(CSV_PATH, newline="", encoding="utf-8")))
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
        run(base + ["--field-id", fields["Story Points"]["id"], "--number", r["Story Points"]])
        run(base + ["--field-id", fields["Requirement"]["id"], "--text", r["Requirements"]])
        run(base + ["--field-id", fields["Item ID"]["id"], "--text", r["ID"]])
        opt = next(o["id"] for o in fields["Sprint"]["options"] if o["name"] == r["Sprint"])
        run(base + ["--field-id", fields["Sprint"]["id"], "--single-select-option-id", opt])

    print("\nDone. Open the project board and add a Board view grouped by Status, "
          "and a Table view grouped by Sprint showing Story Points + Assignees.")


if __name__ == "__main__":
    main()
