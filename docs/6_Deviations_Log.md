# Deviations Log
## Web Based ML Model Evaluator

Part-2 requirement: *"Deviations from the submitted document should be documented and explained during the final demo."*
Record every place where the implementation differs from the SRS (`1_SRS.md`), Architecture & Design Specification (`3_Architecture_Design_Spec.md`) or Test Plan (`2_Test_Plan.md`). Add a row when the change is made, not at the end.

| # | Date | Sprint | Document & section | Planned (as submitted) | Actual (as implemented) | Reason | Impact on requirements / tests | Backlog item / PR | Raised by |
|---|---|---|---|---|---|---|---|---|---|
| D-01 | 23 Oct | 1 | SAD 2.7, 5.4 (C7/C8 job timeout) | Training jobs have a hard 120 s limit | Jobs run in a thread pool; duration is recorded and a warning is logged above the 60 s target, but a running job is not forcibly stopped | Python threads cannot be killed safely; a process-based worker is needed for a hard stop | NFR-02 still measured (TC-13); hard limit to be revisited in Sprint 2 (US-25) | US-12 | Shreya |
| D-02 | 23 Oct | 1 | SAD 2.6 Data Design (USER) | USER has `role`, `failed_logins`, `locked_until` columns | Django's built-in user model is used, with the email stored as the username; lockout and role fields are not added yet | Built-in model gives secure hashing and sessions for free; lockout and admin roles are Sprint 2 stories | No change to FR-01/FR-02; SR-05 (TC-19) and FR-17 (TC-12) delivered in Sprint 2 | US-01, US-21, US-19 | Sneha |
| D-03 | 23 Oct | 1 | SAD 2.6 Data Design (DATASET, DATASET_CONFIG) | DATASET has `stored_path`; config has no task type | DATASET stores a random `stored_name` plus column names/types (JSON); DATASET_CONFIG also stores the detected `task_type` | Random names keep user file names out of the file system (SR-03); storing column types avoids re-reading the file for every page | None | US-05, US-08 | Sukhmeet |
| D-04 | 23 Oct | 1 | SRS FR-12 / SAD 4.2 metrics | Accuracy, precision, recall, F1, confusion matrix | Same metrics; precision/recall/F1 use **weighted** averaging so multi-class datasets get one value each | The SRS does not specify the averaging method for multi-class data | TC-07 expected values computed with weighted averaging | US-13 | Sneha |
| D-05 | 23 Oct | 1 | SRS FR-13 | MAE, MSE, R² | Same, plus **RMSE** | RMSE is in the target's units and easier to interpret | Additive only; TC-08 unchanged | US-14 | Sukhmeet |
| D-06 | 23 Oct | 1 | SAD 2.3 C5 Data Pipeline | Missing-value options apply before training | Rows with an empty **target** value are always dropped (the chosen option applies to features); categorical features are one-hot encoded; Logistic Regression, KNN and SVM get standard scaling | A missing target cannot be imputed; encoding and scaling are needed for the models to train correctly | TC-06 unchanged | US-09 | Shreya |
| D-07 | 23 Oct | 1 | SRS FR-06 (task type) | Task type implied by the target column | Detected automatically: text/boolean target, or a whole-number target with 15 or fewer distinct values = classification; otherwise regression | Needed to show only matching models (FR-09) | Shown to the user on the configure and train pages | US-08 | Sukhmeet |
| D-08 | 23 Oct | 1 | SAD 4.1 API Design | REST endpoints only | REST endpoints exist as designed, plus server-rendered pages (`/datasets/`, `/evaluations/`) that use them; the train page starts several models at once, grouped as one "batch" | Faster to build and test for Sprint 1; the API contract is unchanged | None | US-05 to US-12 | Shreya |
| D-09 | 23 Oct | 1 | SRS FR-10 | Edit at least 2 hyperparameters per model | Catalogue defines editable hyperparameters with defaults and validation, and the API accepts them; the **UI form** for editing them is Sprint 2 | Planned split between US-11 (Sprint 1) and US-15 (Sprint 2) | TC-07 step 2 runs via the API in Sprint 1, via the UI in Sprint 2 | US-11, US-15 | Shreya |

### Categories to watch
- **Scope:** a requirement dropped, reduced or postponed (e.g. low-priority FR-18 viewer simplified).
- **Technology:** a library or tool replaced (e.g. thread pool instead of Celery, Chart.js vs Matplotlib).
- **Design:** API endpoint, data model or component boundary changed.
- **Testing:** a test case changed, merged or not executed, with reason.
- **Process:** sprint scope moved between Sprint 1 and Sprint 2.
