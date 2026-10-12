# Contributing Guide

## Branches
- `main` is protected: no direct pushes, PR + 1 approval + green CI required.
- Branch names: `feature/<id>-<short-name>`, `fix/<id>-<short-name>`, `docs/<short-name>`
  e.g. `feature/us-06-upload-validation`

## Commits
`<ID>: <imperative summary> (#<issue>)`, e.g. `US-06: reject files under 20 rows (#8)`

## Pull requests
- Raised **by the issue's assignee**.
- Title: `[US-06] Validate uploaded files`. Description must contain `Closes #<issue>` (checked by GitHub Actions).
- Fill in the PR template checklist.
- Reviewed and merged by the **repo owner**; the owner's own PRs are reviewed by another teammate.
- Use **Squash and merge** so each backlog item is one commit on `main`.

## One-time repository setup (repo owner)
1. **Settings → Collaborators:** add all three members (write access).
2. **Settings → Branches → Add rule** for `main`: require a pull request, 1 approval, review from Code Owners, status checks `lint-and-test` and `pr-hygiene`.
3. **Settings → Actions → General:** allow GitHub Actions; workflow permissions **Read and write**.
4. Replace `REPO_OWNER_USERNAME` in `.github/CODEOWNERS`.
5. Create the backlog:
   ```bash
   gh auth login
   gh auth refresh -s project
   python scripts/create_backlog.py --repo <owner>/<repo> \
     --users "Shreya=<gh-user>,Sneha=<gh-user>,Sukhmeet=<gh-user>" --dry-run   # preview
   python scripts/create_backlog.py --repo <owner>/<repo> \
     --users "Shreya=<gh-user>,Sneha=<gh-user>,Sukhmeet=<gh-user>"
   ```
6. In the Project: **Workflows** → enable *Item added to project → Todo*, *Item closed → Done*, *Pull request merged → Done*, and *Auto-add to project* (filter `is:issue,pr`).
7. Add views: **Board** (group by Status), **Sprint table** (group by Sprint, show Story Points, Assignees; sum of Story Points visible in the group header).

## Running checks locally
```bash
pip install -r requirements.txt
flake8 .
pytest
coverage run -m pytest && coverage report
```
