# Sprint 2 – Test Summary

## 1. Overview
This document summarizes the testing performed for the SE Mini-Project – Web-Based ML Model Evaluator.

## 2. Functional Testing

| Test | Description | Result |
|---|---|---|
| CSV Upload | Upload a student performance CSV dataset | Passed |
| Model Training | Train Logistic Regression | Passed |
| Model Training | Train Random Forest | Passed |
| Model Evaluation | Display accuracy, precision, recall and F1-score | Passed |
| Confusion Matrix | Display actual vs predicted classes | Passed |
| PDF Report | Download model evaluation report | Verified if download succeeds |
| CSV Export | Download evaluation results | Verified if download succeeds |

## 3. Deployment Testing

### TC-22: HTTPS Application Test
- Started the application using Docker Compose.
- Configured Nginx to redirect HTTP traffic to HTTPS.
- Verified HTTP redirection using curl.
- Verified HTTPS response using curl.
- HTTPS returned HTTP 200 OK.

**Result: PASS**

### TC-23: GitHub CI Checks
- Checked the GitHub repository Actions/Checks section.
- Verified the CI workflow status.

**Result: Update according to the actual GitHub CI status.**

## 4. ML Model Evaluation
Tested the application using student_performance_sample.csv.

Models tested:
- Logistic Regression
- Random Forest

Both models achieved 100% accuracy on the displayed test results.

## 5. Conclusion
The application successfully demonstrated CSV uploading, machine learning model training, evaluation metrics and HTTPS deployment.