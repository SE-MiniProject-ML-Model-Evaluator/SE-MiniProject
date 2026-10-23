# Web Based ML Model Evaluator

Software Engineering Mini-Project: **Part 1** (requirements, test planning, architecture & design) and **Part 2** (backlog, sprints, implementation)

A web application that lets users upload a tabular dataset, choose machine learning models, train and test them, and compare their performance using standard metrics.

## Team

|*[Shreya Shahapur , PES1UG24CS442]* |
|*[Sneha Anil , PES1UG24CS460]* |
|*[Sukhmeet Kaur , PES1UG24CS479]* |
| Software Engineering Mini-Project, Phase1 |

**Course:** Software Engineering  

## Project Summary

| Item | Details |
|---|---|
| Topic | Web Based ML Model Evaluator |
| Key modules | Web Interface, Data Pipeline, Model Selector, Training and Testing |
| Planned stack | Python (Django), scikit-learn, pandas, HTML/JavaScript, PostgreSQL/SQLite |
| Architecture | Three-tier layered client-server (Django MVT with a service layer) |

## Deliverables (Part 1)

| # | Deliverable | Standard | File |
|---|---|---|---|
| 1 | Software Requirements Specification (FRs, NFRs, use case diagram, security section) | IEEE 830 / 29148 | [`docs/1_SRS.md`](docs/1_SRS.md) |
| 2 | Test Plan (sections 3, 4, 5, 5.1 security validation, 24 test cases, traceability matrix) | IEEE 829 | [`docs/2_Test_Plan.md`](docs/2_Test_Plan.md) |
| 3 | Software Architecture & Design Specification (component diagram, pattern, security architecture, sequence diagrams, API design, error handling) | IEEE 1016 | [`docs/3_Architecture_Design_Spec.md`](docs/3_Architecture_Design_Spec.md) |
| 4 | Test cases update for the Test Plan | | Section 8 of [`docs/2_Test_Plan.md`](docs/2_Test_Plan.md) |

## Deliverables (Part 2)

| # | Deliverable | Due | File / location |
|---|---|---|---|
| 1 | Product backlog from FRs/NFRs/SRs, story points, assignees | 12 Oct | GitHub Project · [`docs/4_Product_Backlog.md`](docs/4_Product_Backlog.md) · [`backlog/backlog.csv`](backlog/backlog.csv) |
| 2 | Sprint plan (dry run 12-16 Oct, Sprint 1, Sprint 2) | 12 Oct | [`docs/5_Sprint_Plan.md`](docs/5_Sprint_Plan.md) |
| 3 | GitHub Actions (CI + PR checks) | Sprint 1 | [`.github/workflows/`](.github/workflows/) |
| 4 | Sprint 1 working product + 1-minute video | 23 Oct | `demo/sprint1_demo.mp4` |
| 5 | Sprint 2 working product + 2-minute video, final docs | 30 Oct | `demo/sprint2_demo.mp4` |
| 6 | Deviations from submitted documents | ongoing | [`docs/6_Deviations_Log.md`](docs/6_Deviations_Log.md) |

Workflow rules (branches, PRs, reviews) are in [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Requirement ID Conventions

- **FR-xx**: Functional requirements (FR-01 to FR-18)
- **NFR-xx**: Non-functional requirements (NFR-01 to NFR-08)
- **SO-x / SR-xx**: Security objectives and requirements
- **TC-xx**: Test cases (traceability matrix in the Test Plan, Section 9)
- **C1 to C12**: Architecture components (traceability in the Design Specification, Section 2.4)
- **US-xx / T-xx**: Backlog items (user stories / technical tasks)

## Repository Structure

```
.
├── README.md
├── CONTRIBUTING.md
├── requirements.txt
├── .github/
│   ├── workflows/ci.yml          # lint + tests + coverage on PRs and main
│   ├── workflows/pr-checks.yml   # issue link, title format, auto-assign, labels
│   ├── labeler.yml
│   ├── pull_request_template.md
│   ├── ISSUE_TEMPLATE/
│   └── CODEOWNERS
├── manage.py, mlme/              # Django project
├── accounts/ datasets/ mlengine/ reports/ audit/   # application components
├── templates/ static/            # shared web UI
├── sample_data/                  # demo CSV files
├── backlog/backlog.csv           # backlog source of truth
├── scripts/create_backlog.py     # creates GitHub Project + issues from the CSV
├── demo/                         # sprint demo videos
└── docs/
    ├── 1_SRS.md
    ├── 2_Test_Plan.md
    ├── 3_Architecture_Design_Spec.md
    ├── 4_Product_Backlog.md
    ├── 5_Sprint_Plan.md
    └── 6_Deviations_Log.md
```

## Running the Application Locally

Requires **Python 3.10 or newer** and Git.

**Windows (PowerShell)**
```powershell
git clone https://github.com/SE-MiniProject-ML-Model-Evaluator/SE-MiniProject.git
cd SE-MiniProject
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py manage.py migrate
py manage.py runserver
```

**macOS / Linux**
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000>, register an account and upload one of the files in [`sample_data/`](sample_data/).

| Task | Command |
|---|---|
| Run all tests | `pytest` |
| Tests with coverage | `coverage run -m pytest` then `coverage report` |
| Lint | `flake8 .` |
| Django admin user (optional) | `py manage.py createsuperuser`, then open `/django-admin/` |

If PowerShell blocks `Activate.ps1`, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once.

### Code layout

| Folder | Component (Design Spec 2.3) |
|---|---|
| `mlme/` | Project settings, URL routing, standard API error format (C2) |
| `accounts/` | C3 Auth and access control: register, login/logout, owner-only checks |
| `datasets/` | C4 Dataset service + C12 file storage: upload, validation, preview, configuration |
| `mlengine/` | C5 data pipeline, C6 model selector, C7 ML engine (metrics), C8 job manager (background training) |
| `reports/`, `audit/` | C9 reporting and C10 audit (Sprint 2) |
| `templates/`, `static/` | C1 web UI shared layout and styles |

## Viewing the Diagrams

UML use case, component, ER and sequence diagrams are written in [Mermaid](https://mermaid.js.org/) and render automatically when the Markdown files are viewed on GitHub or GitLab. To export images, paste a diagram block into <https://mermaid.live>.

## Status

- Part 1 (documentation): complete
- Part 2: backlog and sprint plan ready; Sprint 1 starts 19 Oct
