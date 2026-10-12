# Product Backlog
## Web Based ML Model Evaluator

| **Team** |
|*[Shreya Shahapur , PES1UG24CS442]* |
|*[Sneha Anil , PES1UG24CS460]* |
|*[Sukhmeet Kaur , PES1UG24CS479]* |
| Software Engineering Mini-Project, Part 2 |

---

## 1. Purpose

This backlog turns every functional, non-functional and security requirement in the SRS (`1_SRS.md`) into estimated, assigned GitHub issues. The machine-readable source is [`backlog/backlog.csv`](../backlog/backlog.csv); [`scripts/create_backlog.py`](../scripts/create_backlog.py) creates the GitHub Project and issues from it.

## 2. Conventions

| Item | Convention |
|---|---|
| Item IDs | **US-xx** user/security/NFR stories, **T-xx** technical/process tasks |
| Story points | Fibonacci scale **1, 2, 3, 5, 8**: relative effort, complexity and uncertainty (1 = a few hours; 5 = most of a sprint day for one person; 8 = should be split) |
| Priority | High / Medium / Low, carried over from the SRS priority column |
| Labels | `type:story`, `type:task`, `type:security`, `type:nfr`, `priority:*`, `sprint-1`, `sprint-2` |
| Sprints | GitHub milestones **Sprint 1** (19-23 Oct) and **Sprint 2** (26-30 Oct), plus the Project field *Sprint* |
| Project fields | Status (Todo / In Progress / In Review / Done), Story Points, Sprint, Requirement, Item ID |

### Story point reference

| Points | Reference item | Why |
|---|---|---|
| 1 | T-03 Sprint 1 demo video | Recording + notes, no code |
| 2 | US-10 Train/test split | One form field set and a library call |
| 3 | US-01 Registration | API + page + validation + tests |
| 5 | US-06 Upload validation | Six checks, error codes, security cases, tests |
| 8 | none | Anything this large is split before planning |

## 3. Backlog Items

| ID | Title | Type | Requirement(s) | SP | Priority | Sprint | Assignee | Test cases |
|---|---|---|---|---|---|---|---|---|
| **T-01** | Set up Django + DRF project skeleton with layered app structure | Task | NFR-07 | 3 | High | Sprint 1 | Shreya | TC-23 (partial), TC-24 |
| **T-02** | Enable GitHub Actions CI for pushes and pull requests | Task | NFR-07 | 2 | High | Sprint 1 | Sukhmeet | TC-24 |
| **US-01** | User registration with unique email and secure password storage | Story | FR-01, SR-01 | 3 | High | Sprint 1 | Sneha | TC-01, TC-02, TC-17 |
| **US-02** | Login and logout | Story | FR-02 | 3 | High | Sprint 1 | Sneha | TC-03 |
| **US-03** | Owner-only access control on datasets and evaluations | Security | SR-02 | 3 | High | Sprint 1 | Sneha | TC-18 |
| **US-04** | CSRF, XSS and SQL-injection baseline protections | Security | SR-07 | 2 | High | Sprint 1 | Sneha | TC-21 |
| **US-05** | Upload a CSV dataset (up to 50 MB) | Story | FR-03 | 3 | High | Sprint 1 | Sukhmeet | TC-04 |
| **US-06** | Validate uploaded files and reject invalid ones | Story | FR-04, SR-03 | 5 | High | Sprint 1 | Sukhmeet | TC-05 |
| **US-07** | Preview first 20 rows with detected column types | Story | FR-05 | 3 | Medium | Sprint 1 | Sukhmeet | TC-04 |
| **US-08** | Select target and feature columns | Story | FR-06 | 2 | High | Sprint 1 | Sukhmeet | TC-06 |
| **US-09** | Handle missing values (drop / mean-mode impute / none) | Story | FR-07 | 3 | Medium | Sprint 1 | Shreya | TC-06 |
| **US-10** | Configure train/test split size and random seed | Story | FR-08 | 2 | High | Sprint 1 | Shreya | TC-06 |
| **US-11** | Model catalogue for classification and regression | Story | FR-09 | 3 | High | Sprint 1 | Shreya | TC-07, TC-08 |
| **US-12** | Train selected models asynchronously with status tracking | Story | FR-11, NFR-06 | 5 | High | Sprint 1 | Shreya | TC-07, TC-16 |
| **US-13** | Classification metrics and confusion matrix | Story | FR-12 | 5 | High | Sprint 1 | Sneha | TC-07 |
| **US-14** | Regression metrics (MAE, MSE, R²) | Story | FR-13 | 2 | High | Sprint 1 | Sukhmeet | TC-08 |
| **T-03** | Sprint 1 demo video, deviation notes and sprint review | Task | - | 1 | High | Sprint 1 | Sneha | - |
| **US-15** | Edit model hyperparameters | Story | FR-10 | 3 | Medium | Sprint 2 | Shreya | TC-07 |
| **US-16** | Side-by-side comparison table and bar chart | Story | FR-14 | 5 | Medium | Sprint 2 | Sukhmeet | TC-09 |
| **US-17** | Export evaluation report as PDF and CSV | Story | FR-15 | 5 | Medium | Sprint 2 | Sukhmeet | TC-10 |
| **US-18** | Evaluation history: view and delete | Story | FR-16 | 3 | Medium | Sprint 2 | Sneha | TC-11 |
| **US-19** | Admin: view, deactivate and delete users | Story | FR-17 | 3 | Medium | Sprint 2 | Sneha | TC-12, TC-18 |
| **US-20** | Audit logging and admin audit-log viewer | Security | FR-18, SR-08 | 5 | Low | Sprint 2 | Sneha | TC-12 |
| **US-21** | Session timeout and account lockout | Security | SR-05 | 3 | High | Sprint 2 | Shreya | TC-19 |
| **US-22** | API rate limiting (100 requests/min per user) | Security | SR-06 | 2 | Medium | Sprint 2 | Shreya | TC-20 |
| **US-23** | Docker deployment with HTTPS (Nginx + Gunicorn) | NFR | NFR-08, SR-04 | 3 | Medium | Sprint 2 | Sukhmeet | TC-22, TC-23 |
| **US-24** | Reach 70% unit-test coverage on ML and data modules | NFR | NFR-07 | 3 | Medium | Sprint 2 | Shreya | TC-24 |
| **US-25** | Performance and load testing | NFR | NFR-01, NFR-02, NFR-03 | 3 | Medium | Sprint 2 | Shreya | TC-13 |
| **US-26** | Usability and cross-browser testing | NFR | NFR-04, NFR-05 | 2 | Medium | Sprint 2 | Sneha | TC-14, TC-15 |
| **T-04** | Final documentation, Sprint 2 demo video and code freeze | Task | - | 2 | High | Sprint 2 | Sukhmeet | - |

## 4. Story Points per Member

| Member | Sprint 1 | Sprint 2 | Total |
|---|---|---|---|
| Shreya | 16 | 14 | 30 |
| Sneha | 17 | 13 | 30 |
| Sukhmeet | 17 | 15 | 32 |
| **Total** | **50** | **42** | **92** |

## 5. Requirement Coverage

Every SRS requirement maps to at least one backlog item.

| Requirement | Backlog item(s) |
|---|---|
| FR-01 | US-01 |
| FR-02 | US-02 |
| FR-03 | US-05 |
| FR-04 | US-06 |
| FR-05 | US-07 |
| FR-06 | US-08 |
| FR-07 | US-09 |
| FR-08 | US-10 |
| FR-09 | US-11 |
| FR-10 | US-15 |
| FR-11 | US-12 |
| FR-12 | US-13 |
| FR-13 | US-14 |
| FR-14 | US-16 |
| FR-15 | US-17 |
| FR-16 | US-18 |
| FR-17 | US-19 |
| FR-18 | US-20 |
| NFR-01 | US-25 |
| NFR-02 | US-25 |
| NFR-03 | US-25 |
| NFR-04 | US-26 |
| NFR-05 | US-26 |
| NFR-06 | US-12 |
| NFR-07 | T-01, T-02, US-24 |
| NFR-08 | US-23 |
| SR-01 | US-01 |
| SR-02 | US-03 |
| SR-03 | US-06 |
| SR-04 | US-23 |
| SR-05 | US-21 |
| SR-06 | US-22 |
| SR-07 | US-04 |
| SR-08 | US-20 |

## 6. Detailed Backlog Items

Each section below is the body of the matching GitHub issue.

### T-01: Set up Django + DRF project skeleton with layered app structure

**Requirement(s):** NFR-07 · **SP:** 3 · **Priority:** High · **Sprint:** Sprint 1 · **Assignee:** Shreya · **Components:** C2, C11 · **Depends on:** - · **Test cases:** TC-23 (partial), TC-24

*As a developer, I want a Django/DRF project split into the layers from the design spec so that every team member can build their component independently.*

**Acceptance criteria**

- Django 4.x project `mlme` created with apps: accounts (C3), datasets (C4/C5/C12), mlengine (C6/C7/C8), reports (C9), audit (C10)
- requirements.txt pins Django, djangorestframework, pandas, scikit-learn, numpy, reportlab, pytest, pytest-django, coverage, flake8
- SQLite configured for dev; settings read SECRET_KEY/DEBUG from environment
- `python manage.py runserver` starts and `/api/health` returns 200
- README has local setup steps

### T-02: Enable GitHub Actions CI for pushes and pull requests

**Requirement(s):** NFR-07 · **SP:** 2 · **Priority:** High · **Sprint:** Sprint 1 · **Assignee:** Sukhmeet · **Components:** DevOps · **Depends on:** T-01 · **Test cases:** TC-24

*As a team, we want every PR automatically linted and tested so that broken code never reaches main.*

**Acceptance criteria**

- `.github/workflows/ci.yml` runs flake8 and pytest with coverage on every PR and push to main
- `.github/workflows/pr-checks.yml` fails a PR that does not reference an issue (Closes #N)
- Branch protection on main: PR required, 1 approving review, CI must pass
- Coverage report uploaded as a workflow artifact

### US-01: User registration with unique email and secure password storage

**Requirement(s):** FR-01, SR-01 · **SP:** 3 · **Priority:** High · **Sprint:** Sprint 1 · **Assignee:** Sneha · **Components:** C1, C3 · **Depends on:** T-01 · **Test cases:** TC-01, TC-02, TC-17

*As a guest, I want to register with my email and a password so that I can use the evaluator.*

**Acceptance criteria**

- POST /api/auth/register creates a user for a unique email and password of 8+ characters
- Duplicate email returns 409/400 with a clear message; password under 8 characters rejected
- Password stored only as a salted PBKDF2 hash (Django default); never logged
- Register page in the UI with inline error messages

### US-02: Login and logout

**Requirement(s):** FR-02 · **SP:** 3 · **Priority:** High · **Sprint:** Sprint 1 · **Assignee:** Sneha · **Components:** C1, C3 · **Depends on:** US-01 · **Test cases:** TC-03

*As a registered user, I want to log in and log out so that my work is tied to my account and my session ends when I leave.*

**Acceptance criteria**

- POST /api/auth/login starts a session for valid credentials; invalid credentials show an error
- POST /api/auth/logout ends the session immediately
- After logout, protected pages redirect to login (browser Back does not show data)
- Login page and a dashboard landing page exist

### US-03: Owner-only access control on datasets and evaluations

**Requirement(s):** SR-02 · **SP:** 3 · **Priority:** High · **Sprint:** Sprint 1 · **Assignee:** Sneha · **Components:** C2, C3 · **Depends on:** US-02 · **Test cases:** TC-18

*As a user, I want only me to see my datasets and results so that my data stays confidential.*

**Acceptance criteria**

- All dataset/evaluation querysets are filtered by request.user
- Requesting another user's dataset or evaluation ID returns 404/403
- Admin-only routes return 403 for regular users
- Unit tests cover the IDOR cases

### US-04: CSRF, XSS and SQL-injection baseline protections

**Requirement(s):** SR-07 · **SP:** 2 · **Priority:** High · **Sprint:** Sprint 1 · **Assignee:** Sneha · **Components:** C1, C2 · **Depends on:** T-01 · **Test cases:** TC-21

*As the system owner, I want framework protections switched on so that common web attacks fail.*

**Acceptance criteria**

- CSRF middleware active; state-changing POST without token returns 403
- All templates use auto-escaping; no `
- safe` on user content
- Only ORM queries used (no raw SQL with string formatting)
- Test proves `<script>` in a dataset name is rendered escaped

### US-05: Upload a CSV dataset (up to 50 MB)

**Requirement(s):** FR-03 · **SP:** 3 · **Priority:** High · **Sprint:** Sprint 1 · **Assignee:** Sukhmeet · **Components:** C1, C4, C12 · **Depends on:** US-02 · **Test cases:** TC-04

*As a user, I want to upload a CSV file so that I can evaluate models on my own data.*

**Acceptance criteria**

- POST /api/datasets accepts multipart field `file` from an authenticated user
- File saved to file storage (C12) under a generated name, metadata row saved in DB
- GET /api/datasets lists only the user's own datasets
- Upload page in the UI shows progress and success/error message

### US-06: Validate uploaded files and reject invalid ones

**Requirement(s):** FR-04, SR-03 · **SP:** 5 · **Priority:** High · **Sprint:** Sprint 1 · **Assignee:** Sukhmeet · **Components:** C4 · **Depends on:** US-05 · **Test cases:** TC-05

*As a user, I want invalid files rejected with a specific reason so that I know what to fix.*

**Acceptance criteria**

- Checks: .csv extension, text/csv MIME, size <= 50 MB, header row, >= 2 columns, >= 20 rows
- Each failure returns a specific error code/message (400/413/415) and nothing is stored
- File is parsed with pandas only; never executed or unpickled
- Formula-like cells (e.g. `=cmd()`) treated as plain text
- Unit tests for each rejection case

### US-07: Preview first 20 rows with detected column types

**Requirement(s):** FR-05 · **SP:** 3 · **Priority:** Medium · **Sprint:** Sprint 1 · **Assignee:** Sukhmeet · **Components:** C1, C4 · **Depends on:** US-06 · **Test cases:** TC-04

*As a user, I want to preview my dataset so that I can check it uploaded correctly before training.*

**Acceptance criteria**

- GET /api/datasets/{id}/preview returns first 20 rows and a dtype per column
- Preview table rendered in the UI within 3 seconds for a 5 KB file
- Owner-only access enforced

### US-08: Select target and feature columns

**Requirement(s):** FR-06 · **SP:** 2 · **Priority:** High · **Sprint:** Sprint 1 · **Assignee:** Sukhmeet · **Components:** C1, C4 · **Depends on:** US-07 · **Test cases:** TC-06

*As a user, I want to choose the target column and feature columns so that the model learns what I care about.*

**Acceptance criteria**

- Configure page lists columns; exactly one target and one or more features required
- Target cannot also be a feature
- Task type (classification/regression) inferred from target dtype and shown to the user
- Saved through PUT /api/datasets/{id}/config

### US-09: Handle missing values (drop / mean-mode impute / none)

**Requirement(s):** FR-07 · **SP:** 3 · **Priority:** Medium · **Sprint:** Sprint 1 · **Assignee:** Shreya · **Components:** C5 · **Depends on:** US-08 · **Test cases:** TC-06

*As a user, I want to pick how missing values are handled so that training does not fail on incomplete data.*

**Acceptance criteria**

- Options: drop rows, mean (numeric) / mode (categorical) imputation, none
- Chosen strategy stored in dataset config and applied in the data pipeline before training
- Categorical features one-hot encoded in the pipeline
- Unit tests for each strategy

### US-10: Configure train/test split size and random seed

**Requirement(s):** FR-08 · **SP:** 2 · **Priority:** High · **Sprint:** Sprint 1 · **Assignee:** Shreya · **Components:** C5 · **Depends on:** US-08 · **Test cases:** TC-06

*As a user, I want to set the test size and seed so that my results are reproducible.*

**Acceptance criteria**

- Test size accepted between 10% and 50%, default 20%; out-of-range values rejected with a range message
- Random seed field (default 42); same seed gives the same split
- Stratified split used for classification targets

### US-11: Model catalogue for classification and regression

**Requirement(s):** FR-09 · **SP:** 3 · **Priority:** High · **Sprint:** Sprint 1 · **Assignee:** Shreya · **Components:** C6 · **Depends on:** T-01 · **Test cases:** TC-07, TC-08

*As a user, I want to choose from a list of standard models so that I can compare algorithms.*

**Acceptance criteria**

- GET /api/models returns: Logistic Regression, Decision Tree, Random Forest, KNN, SVM (classification); Linear Regression, Decision Tree Regressor, Random Forest Regressor (regression)
- Each entry lists its editable hyperparameters with defaults
- UI shows only models matching the dataset's task type; multiple can be selected

### US-12: Train selected models asynchronously with status tracking

**Requirement(s):** FR-11, NFR-06 · **SP:** 5 · **Priority:** High · **Sprint:** Sprint 1 · **Assignee:** Shreya · **Components:** C7, C8 · **Depends on:** US-09, US-10, US-11 · **Test cases:** TC-07, TC-16

*As a user, I want training to run in the background with a visible status so that the page stays responsive and failures are clear.*

**Acceptance criteria**

- POST /api/evaluations creates one job per selected model with status queued
- Job manager (thread pool) moves status queued -> running -> completed/failed
- UI polls GET /api/evaluations/{id} and shows the status
- A failing job stores a readable error_message and does not crash the server; the next job still runs
- Hard timeout of 120 s per job

### US-13: Classification metrics and confusion matrix

**Requirement(s):** FR-12 · **SP:** 5 · **Priority:** High · **Sprint:** Sprint 1 · **Assignee:** Sneha · **Components:** C1, C7 · **Depends on:** US-12 · **Test cases:** TC-07

*As a user, I want accuracy, precision, recall, F1 and a confusion matrix so that I can judge a classifier.*

**Acceptance criteria**

- Metrics computed on the test split and stored with the evaluation
- Weighted averaging for multi-class precision/recall/F1
- Results page shows the four metrics (0 to 1) and a confusion-matrix heatmap/table
- Unit tests compare against scikit-learn on a fixed dataset

### US-14: Regression metrics (MAE, MSE, R²)

**Requirement(s):** FR-13 · **SP:** 2 · **Priority:** High · **Sprint:** Sprint 1 · **Assignee:** Sukhmeet · **Components:** C1, C7 · **Depends on:** US-12 · **Test cases:** TC-08

*As a user, I want MAE, MSE and R² so that I can judge a regression model.*

**Acceptance criteria**

- Metrics computed on the test split and stored with the evaluation
- Results page shows MAE, MSE, R² and hides classification-only metrics
- Unit test with a known regression dataset

### T-03: Sprint 1 demo video, deviation notes and sprint review

**Requirement(s):** - · **SP:** 1 · **Priority:** High · **Sprint:** Sprint 1 · **Assignee:** Sneha · **Components:** Docs · **Depends on:** US-13, US-14 · **Test cases:** -

*As a team, we want a recorded demo of the working Sprint 1 product so that progress is evidenced in the repo.*

**Acceptance criteria**

- 1-minute screen recording: register -> login -> upload -> configure -> train -> view metrics
- Video uploaded to `demo/sprint1_demo.mp4` (or linked in README if too large)
- Any changes from SRS/SAD/Test Plan recorded in docs/6_Deviations_Log.md
- Unfinished Sprint 1 items moved to Sprint 2 on the board

### US-15: Edit model hyperparameters

**Requirement(s):** FR-10 · **SP:** 3 · **Priority:** Medium · **Sprint:** Sprint 2 · **Assignee:** Shreya · **Components:** C1, C6 · **Depends on:** US-11 · **Test cases:** TC-07

*As a user, I want to change at least two hyperparameters per model so that I can tune performance.*

**Acceptance criteria**

- Hyperparameter form per selected model, pre-filled with defaults
- Values validated against allowed type/range before the job starts; invalid values rejected with a message
- Hyperparameters used are stored with the evaluation and shown on the results page

### US-16: Side-by-side comparison table and bar chart

**Requirement(s):** FR-14 · **SP:** 5 · **Priority:** Medium · **Sprint:** Sprint 2 · **Assignee:** Sukhmeet · **Components:** C1, C9 · **Depends on:** US-13, US-14 · **Test cases:** TC-09

*As a user, I want to compare two or more evaluated models so that I can pick the best one.*

**Acceptance criteria**

- GET /api/evaluations/compare?ids=... returns metrics for the user's own evaluations
- Compare page shows a table and a Chart.js bar chart with matching values
- Selecting fewer than 2 evaluations shows a prompt; mixing classification and regression is blocked

### US-17: Export evaluation report as PDF and CSV

**Requirement(s):** FR-15 · **SP:** 5 · **Priority:** Medium · **Sprint:** Sprint 2 · **Assignee:** Sukhmeet · **Components:** C9 · **Depends on:** US-13, US-14 · **Test cases:** TC-10

*As a user, I want to download a report so that I can share or submit my results.*

**Acceptance criteria**

- GET /api/evaluations/{id}/report?format=pdf
- csv returns a downloadable file
- Report contains dataset name, model, hyperparameters, split settings and all metrics
- PDF built with ReportLab; if PDF fails, CSV still works (500 INTERNAL_ERROR for PDF only)

### US-18: Evaluation history: view and delete

**Requirement(s):** FR-16 · **SP:** 3 · **Priority:** Medium · **Sprint:** Sprint 2 · **Assignee:** Sneha · **Components:** C1, C9 · **Depends on:** US-13 · **Test cases:** TC-11

*As a user, I want to see and delete my past evaluations so that I can manage my work.*

**Acceptance criteria**

- History page lists the user's evaluations (date, dataset, model, key metric, status)
- Opening an entry shows its full results
- DELETE /api/evaluations/{id} and DELETE /api/datasets/{id} remove records and stored files
- Deleted items cannot be retrieved afterwards

### US-19: Admin: view, deactivate and delete users

**Requirement(s):** FR-17 · **SP:** 3 · **Priority:** Medium · **Sprint:** Sprint 2 · **Assignee:** Sneha · **Components:** C1, C3, C10 · **Depends on:** US-03 · **Test cases:** TC-12, TC-18

*As an administrator, I want to manage user accounts so that I can remove misuse.*

**Acceptance criteria**

- GET /api/admin/users, PATCH /api/admin/users/{id} (activate/deactivate), DELETE /api/admin/users/{id}
- Deactivated users cannot log in
- Deleting a user removes their datasets and evaluations
- Admin UI page; regular users get 403

### US-20: Audit logging and admin audit-log viewer

**Requirement(s):** FR-18, SR-08 · **SP:** 5 · **Priority:** Low · **Sprint:** Sprint 2 · **Assignee:** Sneha · **Components:** C10 · **Depends on:** US-19 · **Test cases:** TC-12

*As an administrator, I want an audit log of logins, uploads, runs and admin actions so that actions are traceable.*

**Acceptance criteria**

- AuditLog model records timestamp, user ID, action, target and IP for: login success/failure, upload, evaluation run, admin action
- GET /api/admin/audit-log with filters by user and date range
- Audit-log page for admins; no passwords or dataset contents logged

### US-21: Session timeout and account lockout

**Requirement(s):** SR-05 · **SP:** 3 · **Priority:** High · **Sprint:** Sprint 2 · **Assignee:** Shreya · **Components:** C3 · **Depends on:** US-02 · **Test cases:** TC-19

*As the system owner, I want idle sessions to expire and brute-force logins to be locked out so that accounts are protected.*

**Acceptance criteria**

- Session expires after 30 minutes of inactivity
- 5 consecutive failed logins lock the account for 15 minutes; correct password rejected during lock
- Lockout events written to the audit log

### US-22: API rate limiting (100 requests/min per user)

**Requirement(s):** SR-06 · **SP:** 2 · **Priority:** Medium · **Sprint:** Sprint 2 · **Assignee:** Shreya · **Components:** C2 · **Depends on:** T-01 · **Test cases:** TC-20

*As the system owner, I want per-user rate limits so that the server is not overloaded.*

**Acceptance criteria**

- DRF throttling: 100 requests/minute per authenticated user
- Excess requests return HTTP 429 in the standard error format
- Test sends 150 requests and asserts 429 after the 100th

### US-23: Docker deployment with HTTPS (Nginx + Gunicorn)

**Requirement(s):** NFR-08, SR-04 · **SP:** 3 · **Priority:** Medium · **Sprint:** Sprint 2 · **Assignee:** Sukhmeet · **Components:** DevOps · **Depends on:** T-01 · **Test cases:** TC-22, TC-23

*As an evaluator, I want to run the app on a fresh machine quickly and securely so that the demo is reliable.*

**Acceptance criteria**

- Dockerfile + docker-compose.yml (app, Nginx); `docker compose up` starts the app
- Nginx redirects HTTP to HTTPS with TLS 1.2+ (self-signed cert for demo)
- SECURE_* Django settings enabled in production mode
- Fresh-machine setup timed at 15 minutes or less and documented in README

### US-24: Reach 70% unit-test coverage on ML and data modules

**Requirement(s):** NFR-07 · **SP:** 3 · **Priority:** Medium · **Sprint:** Sprint 2 · **Assignee:** Shreya · **Components:** C5, C6, C7 · **Depends on:** US-12 · **Test cases:** TC-24

*As a team, we want solid unit-test coverage so that the core logic is trustworthy and maintainable.*

**Acceptance criteria**

- pytest tests for data pipeline, model selector, ML engine and dataset validation
- `coverage report` shows >= 70% for datasets and mlengine apps
- CI fails if coverage drops below 70% on these modules

### US-25: Performance and load testing

**Requirement(s):** NFR-01, NFR-02, NFR-03 · **SP:** 3 · **Priority:** Medium · **Sprint:** Sprint 2 · **Assignee:** Shreya · **Components:** Testing · **Depends on:** US-12 · **Test cases:** TC-13

*As a team, we want measured performance so that we can show the NFR targets are met.*

**Acceptance criteria**

- Locust (or similar) script: 20 concurrent users for 5 minutes, error rate <= 1%
- 95th-percentile page load <= 3 s recorded
- Each catalogue model trains on a 10,000 x 20 dataset in <= 60 s
- Results written to docs/test_results/performance.md

### US-26: Usability and cross-browser testing

**Requirement(s):** NFR-04, NFR-05 · **SP:** 2 · **Priority:** Medium · **Sprint:** Sprint 2 · **Assignee:** Sneha · **Components:** Testing · **Depends on:** US-16 · **Test cases:** TC-14, TC-15

*As a team, we want to confirm first-time users and all supported browsers work so that the demo goes smoothly.*

**Acceptance criteria**

- 3 first-time users complete upload -> evaluate in <= 5 minutes (timings recorded)
- TC-03, TC-04, TC-07 pass on latest Chrome, Firefox and Edge
- Results written to docs/test_results/usability_browser.md

### T-04: Final documentation, Sprint 2 demo video and code freeze

**Requirement(s):** - · **SP:** 2 · **Priority:** High · **Sprint:** Sprint 2 · **Assignee:** Sukhmeet · **Components:** Docs · **Depends on:** US-16, US-17, US-23 · **Test cases:** -

*As a team, we want complete documentation and a recorded final demo so that the project can be evaluated.*

**Acceptance criteria**

- 2-minute Sprint 2 demo video uploaded to `demo/sprint2_demo.mp4` (or linked)
- README: features, setup (local + Docker), screenshots, team, test results
- Traceability matrix updated with test results; deviations log complete
- Release tag v1.0 created; development frozen
