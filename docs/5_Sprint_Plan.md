# Sprint Plan
## Web Based ML Model Evaluator

| **Team** |
|*[Shreya Shahapur , PES1UG24CS442]* |
|*[Sneha Anil , PES1UG24CS460]* |
|*[Sukhmeet Kaur , PES1UG24CS479]* |
| Software Engineering Mini-Project, Part 2 |

---

## 1. Timeline

| Phase | Dates | Goal | Output |
|---|---|---|---|
| Backlog creation | by 12 Oct | Project created and linked, backlog with story points and assignees | GitHub Project, 30 issues, `docs/4_Product_Backlog.md` |
| Sprint 0 (dry run) | 12-16 Oct | Practise the workflow: branch, PR, CI, review, merge, board update | T-01 and T-02 done (project skeleton + CI) |
| Backlog refinement | 19 Oct | Final changes to estimates, assignees or scope before Sprint 1 starts | Updated issues |
| **Sprint 1** | **19-23 Oct** | **Working product:** register, log in, upload, validate, preview, configure, train, view metrics | 1-minute demo video in `demo/` |
| **Sprint 2** | **26-30 Oct** | Comparison, export, history, admin and audit, security hardening, NFR testing, Docker, docs | 2-minute demo video, final docs, `v1.0` tag, code freeze |

## 2. Team Capacity and Velocity

- 3 members × 5 working days per sprint.
- Planned load: about 15-17 story points per member per sprint.
- Sprint 1 is planned at **50 SP**, Sprint 2 at **42 SP** (Sprint 2 is lighter to leave room for carry-over, testing and documentation).
- Velocity after Sprint 1 = SP of issues closed by 23 Oct. If it is below 42, lowest-priority Sprint 2 items (US-20, US-26) are de-scoped first and the change is logged in the deviations log.

## 3. Sprint 0: Dry Run (12-16 Oct)

Purpose: rehearse the process on low-risk setup work so Sprint 1 starts with a working pipeline.

| Item | Owner | Done when |
|---|---|---|
| T-01 Django + DRF skeleton | Shreya | `runserver` works, `/api/health` returns 200, PR merged |
| T-02 GitHub Actions CI | Sukhmeet | CI runs on a PR; branch protection on `main` enabled |
| Each member raises one practice PR (e.g. README section) | All | PR title/issue-link checks pass, owner reviews and merges |

Items finished in the dry run count toward Sprint 1.

## 4. Sprint 1 Backlog (19-23 Oct): 50 SP

**Sprint goal:** a user can register, log in, upload a CSV, configure it, train one or more models and see correct metrics. This is the end-to-end flow shown in the 1-minute video.

| ID | Item | Req. | SP | Assignee |
|---|---|---|---|---|
| T-01 | Django + DRF skeleton | NFR-07 | 3 | Shreya |
| T-02 | GitHub Actions CI | NFR-07 | 2 | Sukhmeet |
| US-01 | Registration + password hashing | FR-01, SR-01 | 3 | Sneha |
| US-02 | Login / logout | FR-02 | 3 | Sneha |
| US-03 | Owner-only access control | SR-02 | 3 | Sneha |
| US-04 | CSRF / XSS / SQLi protections | SR-07 | 2 | Sneha |
| US-05 | Upload CSV | FR-03 | 3 | Sukhmeet |
| US-06 | Validate uploads | FR-04, SR-03 | 5 | Sukhmeet |
| US-07 | Preview 20 rows + types | FR-05 | 3 | Sukhmeet |
| US-08 | Select target and features | FR-06 | 2 | Sukhmeet |
| US-09 | Missing-value handling | FR-07 | 3 | Shreya |
| US-10 | Train/test split + seed | FR-08 | 2 | Shreya |
| US-11 | Model catalogue | FR-09 | 3 | Shreya |
| US-12 | Async training + status | FR-11, NFR-06 | 5 | Shreya |
| US-13 | Classification metrics + confusion matrix | FR-12 | 5 | Sneha |
| US-14 | Regression metrics | FR-13 | 2 | Sukhmeet |
| T-03 | Sprint 1 video + deviation notes | - | 1 | Sneha |

**Per member:** Shreya 16 · Sneha 17 · Sukhmeet 17

### Suggested day-by-day order

| Day | Focus |
|---|---|
| Mon 19 | Refine backlog; US-01, US-05, US-11 start (no inter-dependencies) |
| Tue 20 | US-02, US-06, US-09, US-10 |
| Wed 21 | US-03, US-04, US-07, US-08, US-12 |
| Thu 22 | US-13, US-14; integrate the end-to-end flow |
| Fri 23 | Bug fixing, merge freeze at noon, record video (T-03), sprint review and retrospective |

## 5. Sprint 2 Backlog (26-30 Oct): 42 SP

**Sprint goal:** complete all remaining FRs, harden security, prove the NFRs with tests, and ship documented, Docker-deployable v1.0.

| ID | Item | Req. | SP | Assignee |
|---|---|---|---|---|
| US-15 | Edit hyperparameters | FR-10 | 3 | Shreya |
| US-16 | Compare table + bar chart | FR-14 | 5 | Sukhmeet |
| US-17 | Export PDF / CSV | FR-15 | 5 | Sukhmeet |
| US-18 | Evaluation history | FR-16 | 3 | Sneha |
| US-19 | Admin user management | FR-17 | 3 | Sneha |
| US-20 | Audit logging + viewer | FR-18, SR-08 | 5 | Sneha |
| US-21 | Session timeout + lockout | SR-05 | 3 | Shreya |
| US-22 | Rate limiting | SR-06 | 2 | Shreya |
| US-23 | Docker + HTTPS | NFR-08, SR-04 | 3 | Sukhmeet |
| US-24 | 70% unit-test coverage | NFR-07 | 3 | Shreya |
| US-25 | Performance / load tests | NFR-01..03 | 3 | Shreya |
| US-26 | Usability + cross-browser tests | NFR-04, NFR-05 | 2 | Sneha |
| T-04 | Final docs, video, code freeze | - | 2 | Sukhmeet |

**Per member:** Shreya 14 · Sneha 13 · Sukhmeet 15

## 6. Ceremonies

| Ceremony | When | Length | Output |
|---|---|---|---|
| Sprint planning | Monday 10:00 | 30 min | Sprint items moved to *Todo*, owners confirmed |
| Daily stand-up | Each day | 10 min | Done yesterday / doing today / blockers (WhatsApp or in person) |
| Sprint review | Friday | 20 min | Demo of the working product, video recorded |
| Retrospective | Friday | 15 min | 1 thing to keep, 1 to change, noted in section 8 |

## 7. Workflow per Backlog Item

1. Assignee moves the issue to **In Progress** on the Project board.
2. Create a branch: `feature/us-05-upload-csv` (or `fix/...`, `docs/...`).
3. Commit with the issue reference: `US-05: add upload endpoint (#7)`.
4. Push and open a PR titled `[US-05] Upload CSV dataset` with `Closes #7` in the description. **The assignee raises the PR.**
5. GitHub Actions runs CI (lint + tests) and PR checks (issue link, title format, labels).
6. Move the issue to **In Review**. The **repo owner reviews and merges**; PRs raised by the owner are reviewed by another teammate.
7. Merging closes the issue automatically and the board moves it to **Done**.

## 8. Sprint Review and Retrospective Notes

### Sprint 1 (fill in on 23 Oct)
- Planned SP: 50 · Completed SP: __ · Velocity: __
- Demo video: `demo/sprint1_demo.mp4`
- Carried over to Sprint 2:
- Keep doing:
- Change:

### Sprint 2 (fill in on 30 Oct)
- Planned SP: 42 · Completed SP: __
- Demo video: `demo/sprint2_demo.mp4`
- Keep doing:
- Change:

## 9. GitHub Project Setup Text

Project created from the **Iterative development** template. Field mapping: **Estimate** = story points, **Iteration 1** = Sprint 1 (19-23 Oct), **Iteration 2** = Sprint 2 (26-30 Oct), **Priority** P0 = High, P1 = Medium, P2 = Low, **Size** XS = 1 SP, S = 2, M = 3, L = 5, XL = 8.

**Short description**

> A web application that lets users upload a tabular CSV dataset, choose machine learning models, train and test them, and compare their performance using standard metrics.

**README**

> This project is about a web-based ML model evaluator. The product allows:
> 1. Users to register, log in and log out securely
> 2. Upload a CSV dataset, validate it and preview the first 20 rows
> 3. Select target and feature columns, handle missing values and set the train/test split
> 4. Choose classification or regression models and edit their hyperparameters
> 5. Train models in the background and view metrics (accuracy, precision, recall, F1, confusion matrix, MAE, MSE, R²)
> 6. Compare models side by side, export reports as PDF/CSV and manage evaluation history
> 7. Admins manage users and view the audit log
>
> Sprint 1 (19-23 Oct): working upload-to-metrics flow. Sprint 2 (26-30 Oct): comparison, export, admin, security hardening, testing and documentation.
