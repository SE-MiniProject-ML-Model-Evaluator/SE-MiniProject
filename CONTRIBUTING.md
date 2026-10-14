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
5. **Create the GitHub Project (same as the class demo):**
   - Repo > **Projects** tab > **New project** > template **Iterative development** > **Create project**.
   - Project **... > Settings**: set *Project name* `Web Based ML Model Evaluator`, *Default repository* this repo,
     *Short description* and *README* (text in `docs/5_Sprint_Plan.md`, section 9). **Save changes**.
   - Settings > **Iteration** field: start date **19 Oct 2026**, duration **1 week**, so Iteration 1 = Sprint 1
     (19-25 Oct) and Iteration 2 = Sprint 2 (26 Oct-1 Nov). Save.
   - Note the project number from the URL: `github.com/users/<you>/projects/<N>`.
6. **Fill the backlog** (creates 30 issues in the Backlog column with Assignee, Priority, Size, Estimate = story points, Iteration):
   ```bash
   gh auth login
   gh auth refresh -s project
   python scripts/create_backlog.py --repo <owner>/<repo> --project-number <N> \
     --users "Shreya=<gh-user>,Sneha=<gh-user>,Sukhmeet=<gh-user>" --dry-run   # preview
   python scripts/create_backlog.py --repo <owner>/<repo> --project-number <N> \
     --users "Shreya=<gh-user>,Sneha=<gh-user>,Sukhmeet=<gh-user>"
   ```
7. In the Project: **Workflows** > enable *Item closed > Done* and *Pull request merged > Done*.
   The template already has the board (*Current iteration*), *Prioritized backlog* and *Roadmap* views.

## Running checks locally
```bash
pip install -r requirements.txt
flake8 .
pytest
coverage run -m pytest && coverage report
```
