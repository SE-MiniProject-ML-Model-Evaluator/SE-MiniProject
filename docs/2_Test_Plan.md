# Test Plan
## Web Based ML Model Evaluator

| **Team** | 
|*[Shreya Shahapur , PES1UG24CS442]* |
|*[Sneha Anil , PES1UG24CS460]* |
|*[Sukhmeet Kaur , PES1UG24CS479]* |
| Software Engineering Mini-Project, Phase1 |
---

## 1. Introduction

### 1.1 Purpose
This plan defines the scope, approach, resources, schedule and test cases used to verify that the **Web Based ML Model Evaluator (MLME)** meets the requirements in SRS-MLME-001, including functional, non-functional and security requirements.

### 1.2 Scope
Testing covers the web UI, REST API, data pipeline, model selector, training/testing engine, reporting, administration and security controls. Every test case is traceable to at least one SRS requirement ID (Section 8).

### 1.3 Terms and Thier Definations

| Term | Meaning |
|---|---|
| TC | Test Case |
| RTM | Requirements Traceability Matrix |
| SUT | System Under Test |
| UAT | User Acceptance Testing |

### 1.4 References
1. SRS-MLME-001, Software Requirements Specification
2. IEEE Std 829, Software Test Documentation
3. OWASP Web Security Testing Guide

---

## 2. Test Plan Identifier and Test Levels

**Identifier:** TP-MLME-001, version 1.0.

| Level | Description | Owner |
|---|---|---|
| Unit | Individual functions (validators, metric computation, split logic) using `pytest`/Django `TestCase` | Developers |
| Integration | API endpoints with database and ML engine | Developers |
| System | End-to-end user workflows through the UI | Testers |
| Acceptance | Walkthrough of SRS requirements against the running system | Whole team |

---

## 3. Test Items

The following items are under test (build version 1.0):

| # | Item | Description |
|---|---|---|
| 3.1 | Web UI | Login/Register, Dashboard, Upload, Configure, Results, Compare, History, Admin pages |
| 3.2 | REST API | Authentication, dataset, model, training, results, report and admin endpoints |
| 3.3 | Data pipeline | File validation, parsing, missing-value handling, train/test split |
| 3.4 | Model selector and ML engine | Model catalogue, hyperparameter handling, training and metric computation |
| 3.5 | Reporting module | PDF/CSV export and history |
| 3.6 | Administration and audit module | User management and audit log |
| 3.7 | Security controls | Authentication, RBAC, input validation, session and rate limiting |

---

## 4. Features to be Tested

### 4.1 Features to be Tested

| Feature area | SRS requirements |
|---|---|
| Account management and authentication | FR-01, FR-02 |
| Dataset upload, validation, preview | FR-03, FR-04, FR-05 |
| Data configuration (target, features, missing values, split) | FR-06, FR-07, FR-08 |
| Model selection and hyperparameters | FR-09, FR-10 |
| Training and evaluation | FR-11, FR-12, FR-13 |
| Model comparison, export, history | FR-14, FR-15, FR-16 |
| Administration and audit log | FR-17, FR-18 |
| Performance, scalability, usability, compatibility, reliability | NFR-01 to NFR-06 |
| Maintainability and portability | NFR-07, NFR-08 |
| Security | SR-01 to SR-08 |

### 4.2 Features Not to be Tested

| Feature | Reason |
|---|---|
| Internal correctness of scikit-learn algorithms | Third-party library, assumed verified by its maintainers |
| Django framework internals | Third-party framework |
| Load above 20 concurrent users | Outside SRS scope (NFR-03) |
| Non-CSV file formats, deep learning models | Excluded in SRS scope |
| Physical infrastructure/hosting security | Outside project scope |

---

## 5. Test Approach

| Type | Approach | Tools |
|---|---|---|
| Functional | Black-box tests from requirements: equivalence partitioning, boundary value analysis (e.g. 50 MB limit, 10-50% split), negative testing | Manual, Django test client, Selenium (optional) |
| Performance | Measure page load and training time on reference datasets | Locust/JMeter, browser dev tools |
| Usability | Timed walkthrough with first-time users | Stopwatch, observation checklist |
| Compatibility | Execute smoke workflow on Chrome, Firefox and Edge | Manual, BrowserStack (optional) |
| Reliability | Fault injection: invalid data and forced training failure | Manual, pytest |
| Regression | Re-run all TCs after each fix | pytest, checklist |
| Static/Analysis | Coverage and dependency inspection | `coverage.py`, `pip-audit`/`bandit` |

### 5.1 Security Validation

**Objective:** verify the security objectives SO-1 to SO-4 and requirements SR-01 to SR-08 defined in the SRS.

| Security area | Method | Tools | Test cases |
|---|---|---|---|
| Authentication and password storage (SR-01) | Inspect DB for salted hashes; verify no plaintext in logs | DB client, log review | TC-17 |
| Authorisation / RBAC (SR-02, SO-1) | Attempt cross-user access (IDOR) and non-admin access to admin URLs | Browser, Postman | TC-18 |
| Malicious file upload (SR-03, SO-2) | Upload executables renamed `.csv`, oversized files, malformed CSV, formula-injection payloads | Postman, crafted files | TC-05 |
| Transport security (SR-04) | Verify HTTPS redirect and TLS version | Browser, `openssl`/SSL Labs | TC-22 |
| Session and brute-force protection (SR-05, SO-3) | Idle timeout; repeated failed logins | Browser, script | TC-19 |
| Rate limiting (SR-06, SO-3) | Send more than 100 requests per minute | Locust/curl loop | TC-20 |
| Injection and web attacks (SR-07) | XSS payloads in text fields/filenames, SQLi strings, missing CSRF token | OWASP ZAP, manual | TC-21 |
| Audit trail (SR-08, SO-4) | Check log entries after login, upload, run, admin action | Admin UI, DB | TC-12 |

**Security pass criteria:** no high or medium severity finding remains open; all SR test cases pass.

---

## 6. Item Pass/Fail Criteria

- A test case **passes** when the actual result matches the expected result with no unhandled error.
- The release **passes** when: 100% of High-priority TCs pass, at least 95% of all TCs pass, and no open Critical/High defects exist.

## 7. Suspension and Resumption Criteria

- **Suspend** if the application cannot start, login is unavailable, or more than 30% of a test cycle fails from a single blocking defect.
- **Resume** after the blocking defect is fixed and a smoke test (TC-03, TC-04) passes.

---

## 8. Test Cases

Priority: H = High, M = Medium. Type: F = Functional, NF = Non-Functional, S = Security.

### 8.1 Test Case Specifications

| ID | Title | Req. | Type | Pri. | Preconditions | Steps and test data | Expected result |
|---|---|---|---|---|---|---|---|
| **TC-01** | Register with valid details | FR-01 | F | H | App running; email not registered | 1. Open Register page. 2. Enter `user1@test.com`, password `Str0ngPass!`. 3. Submit. | Account created; user redirected to login/dashboard; success message shown. |
| **TC-02** | Register with invalid details | FR-01 | F | M | User `user1@test.com` exists | 1. Register with same email. 2. Register new email with password `abc12` (5 chars). | Duplicate email rejected with clear message; short password rejected (minimum 8); no account created in both cases. |
| **TC-03** | Login and logout | FR-02 | F | H | Registered user exists | 1. Log in with valid credentials. 2. Click Logout. 3. Press browser Back. | Dashboard shown after login; after logout session ends and protected pages redirect to login. Invalid password shows an error. |
| **TC-04** | Upload valid CSV and preview | FR-03, FR-04, FR-05 | F | H | Logged in; `iris.csv` (150 rows, 5 cols, 5 KB) | 1. Go to Upload. 2. Select `iris.csv`. 3. Submit. | Upload succeeds; first 20 rows and detected column types shown in 3 s or less. |
| **TC-05** | Reject invalid uploads | FR-04, SR-03 | F/S | H | Logged in | Upload: (a) `malware.exe` renamed `data.csv`; (b) 51 MB CSV; (c) CSV with 1 column; (d) CSV with 10 rows; (e) file with `=cmd()` cell payload. | Each of (a)-(d) rejected with a specific error and nothing stored; (e) cell content handled as text, never executed. |
| **TC-06** | Configure target, features, missing values and split | FR-06, FR-07, FR-08 | F | H | `iris.csv` uploaded; dataset variant with blanks | 1. Select target `species`, features (4 cols). 2. Choose "mean imputation". 3. Set test size 25%, seed 42. 4. Try test size 5% and 60%. | Config saved; imputation applied; split is 75/25 and reproducible with same seed; 5% and 60% rejected with range message (10-50%). |
| **TC-07** | Train and evaluate classification models | FR-09, FR-10, FR-11, FR-12 | F | H | Dataset configured (TC-06) | 1. Select Logistic Regression and Random Forest. 2. Change 2 hyperparameters on Random Forest (`n_estimators=50`, `max_depth=5`). 3. Click Train. | Status moves queued → running → completed; accuracy, precision, recall, F1 and confusion matrix shown for each model; values between 0 and 1. |
| **TC-08** | Regression evaluation | FR-09, FR-13 | F | H | `housing.csv` (numeric target) uploaded and configured | 1. Select Linear Regression. 2. Train. | MAE, MSE and R² displayed; classification-only metrics not shown. |
| **TC-09** | Compare multiple models | FR-14 | F | M | At least 2 completed evaluations | 1. Open Compare. 2. Select two models. | Side-by-side table and bar chart appear with matching metric values; selecting only 1 model shows a prompt. |
| **TC-10** | Export report | FR-15 | F | M | Completed evaluation | 1. Click Export PDF. 2. Click Export CSV. | Downloaded files open correctly and contain dataset name, model, hyperparameters and all metrics. |
| **TC-11** | Evaluation history | FR-16 | F | M | User has 3 past evaluations | 1. Open History. 2. Open one entry. 3. Delete another. | All own evaluations listed; details open; deleted entry disappears and cannot be retrieved. |
| **TC-12** | Admin user management and audit log | FR-17, FR-18, SR-08 | F/S | M | Admin logged in; regular user exists | 1. Deactivate the regular user. 2. Regular user tries to log in. 3. Open Audit Log. | Deactivated user cannot log in; audit log shows login, upload, run and admin actions with timestamp and user ID. |
| **TC-13** | Performance: page load and training time | NFR-01, NFR-02, NFR-03 | NF | H | Test dataset 10,000 rows × 20 features; load script | 1. Measure 100 page loads. 2. Train each catalogue model once. 3. Run 20 concurrent users for 5 minutes. | 95th percentile page load is 3 s or less; each model completes in 60 s or less; error rate is 1% or less at 20 users. |
| **TC-14** | Usability: first-time user workflow | NFR-04 | NF | M | 3 first-time users, no training | Ask each user to upload, configure, train and view results while timing them. | Each user completes the workflow within 5 minutes without external help. |
| **TC-15** | Cross-browser compatibility | NFR-05 | NF | M | Latest two versions of Chrome, Firefox, Edge | Run TC-03, TC-04, TC-07 on each browser. | Layout renders correctly and all steps pass on every browser. |
| **TC-16** | Reliability: failed training handling | NFR-06 | NF | H | Dataset with non-numeric feature column left unencoded | 1. Train Logistic Regression. 2. Immediately run another valid training. | First job reports "failed" with readable error; server stays up; second job completes normally. |
| **TC-17** | Password storage | SR-01 | S | H | New user registered | 1. Inspect user table. 2. Search application logs for the password. | Password stored as salted hash (e.g. `pbkdf2_sha256$…`); plaintext is not found in DB or logs. |
| **TC-18** | Access control (IDOR and admin pages) | SR-02 | S | H | Users A and B, each with a dataset; admin exists | 1. As B, request A's dataset/result URL and API ID. 2. As a regular user, open `/admin/` and admin API routes. | Both requests are denied (403/404); no data from A is exposed; admin routes blocked. |
| **TC-19** | Session timeout and account lockout | SR-05 | S | H | Registered user | 1. Enter wrong password 5 times. 2. Try correct password immediately. 3. Log in later and stay idle 30 min. | Account locked for 15 min after 5 failures; correct password rejected during lock; idle session expires and requires re-login. |
| **TC-20** | Rate limiting | SR-06 | S | M | Logged in; script ready | Send 150 API requests within 60 seconds. | First 100 succeed; further requests return HTTP 429. |
| **TC-21** | Injection and CSRF protection | SR-07 | S | H | Logged in | 1. Enter `<script>alert(1)</script>` as dataset name. 2. Enter `' OR '1'='1` in login. 3. Submit a POST without CSRF token. | Script is escaped and not executed; login fails safely; POST without token is rejected (403). |
| **TC-22** | Transport security | SR-04 | S | H | Deployment with TLS enabled | 1. Open the site over `http://`. 2. Check certificate and protocol. | Redirected to HTTPS; TLS 1.2 or higher in use; no mixed-content warnings. |
| **TC-23** | Portability: fresh deployment | NFR-08 | NF | M | Clean machine/VM; README steps | Follow documented install (or Docker) steps and time them. | Application runs and TC-03 passes within 15 minutes. |
| **TC-24** | Maintainability: unit-test coverage | NFR-07 | NF | M | Unit tests written | Run `coverage run -m pytest` and `coverage report` on the ML and data modules. | Coverage is 70% or higher; modules are separated per architecture. |

**Total: 24 test cases** (14 functional/mixed, 6 security, 6 non-functional including mixed types).

---

## 9. Traceability Matrix (SRS to Test Cases)

| Requirement | Summary | Test case(s) |
|---|---|---|
| FR-01 | Register | TC-01, TC-02 |
| FR-02 | Login/logout | TC-03 |
| FR-03 | Upload CSV up to 50 MB | TC-04, TC-05 |
| FR-04 | Upload validation | TC-04, TC-05 |
| FR-05 | Dataset preview | TC-04 |
| FR-06 | Target/feature selection | TC-06 |
| FR-07 | Missing value handling | TC-06 |
| FR-08 | Train/test split settings | TC-06 |
| FR-09 | Model catalogue | TC-07, TC-08 |
| FR-10 | Hyperparameters | TC-07 |
| FR-11 | Training and status | TC-07 |
| FR-12 | Classification metrics | TC-07 |
| FR-13 | Regression metrics | TC-08 |
| FR-14 | Model comparison | TC-09 |
| FR-15 | Report export | TC-10 |
| FR-16 | History | TC-11 |
| FR-17 | Admin user management | TC-12 |
| FR-18 | Audit log view | TC-12 |
| NFR-01 | Page load time | TC-13 |
| NFR-02 | Training time | TC-13 |
| NFR-03 | 20 concurrent users | TC-13 |
| NFR-04 | Usability | TC-14 |
| NFR-05 | Browser compatibility | TC-15 |
| NFR-06 | Reliability | TC-16 |
| NFR-07 | Maintainability | TC-24 |
| NFR-08 | Portability | TC-23 |
| SR-01 | Password hashing | TC-17 |
| SR-02 | RBAC | TC-18 |
| SR-03 | Upload validation | TC-05 |
| SR-04 | HTTPS | TC-22 |
| SR-05 | Session timeout/lockout | TC-19 |
| SR-06 | Rate limiting | TC-20 |
| SR-07 | XSS/CSRF/SQLi protection | TC-21 |
| SR-08 | Audit logging | TC-12 |

**Coverage:** all 18 FRs, 8 NFRs and 8 SRs are covered by at least one test case. Security objectives are covered as follows: SO-1 by TC-17, TC-18, TC-22; SO-2 by TC-05, TC-21; SO-3 by TC-19, TC-20; SO-4 by TC-12.

---

## 10. Test Deliverables

Test plan, test case specifications (Section 8), test execution log (pass/fail per TC), defect reports, coverage report, and a final test summary report.

## 11. Environmental Needs

| Item | Specification |
|---|---|
| Hardware | Laptop/VM with 8 GB RAM, 4 cores |
| Software | Python 3.10+, Django 4.x, scikit-learn, pandas, SQLite/PostgreSQL |
| Browsers | Latest two versions of Chrome, Firefox, Edge |
| Test tools | pytest, coverage.py, Postman, Locust, OWASP ZAP |
| Test data | `iris.csv`, `housing.csv`, 10k-row synthetic dataset, malformed and oversized files |

## 12. Responsibilities (not yet decided)

| Role | Responsibility |
|---|---|
| Test lead | Plan, schedule, final report | 
| Developers | Unit and integration tests, defect fixes |
| Testers | System, performance, security and usability testing |

## 13. Schedule

| Activity | Timing |
|---|---|
| Test plan and case design | Part 1 (this deliverable) |
| Unit and integration testing | During implementation |
| System, security and performance testing | After feature freeze |
| Regression and final report | Before final submission |

## 14. Risks and Contingencies

| Risk | Mitigation |
|---|---|
| Large datasets slow the demo machine | Restrict test data to 10k rows; use timeouts |
| Insufficient time for security testing | Prioritise High-priority security TCs (TC-05, 17, 18, 19, 21) |
| Browser inconsistencies | Test early on all three browsers |

