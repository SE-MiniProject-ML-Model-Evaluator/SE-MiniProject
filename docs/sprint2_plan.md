# Sprint 2 – Plan and Deviations

## 1. Sprint Overview
The objective of Sprint 2 was to complete the Web-Based ML Model Evaluator, improve its functionality, implement secure deployment and perform application testing.

## 2. Planned Features
The following features were planned for Sprint 2:

- Implement CSV dataset upload and validation.
- Allow users to select target columns and input features.
- Implement missing-value handling and train-test splitting.
- Integrate machine learning algorithms.
- Display model evaluation metrics such as Accuracy, Precision, Recall and F1-score.
- Generate confusion matrices.
- Provide downloadable PDF reports and CSV results.
- Implement user registration and login functionality.
- Configure HTTPS deployment using Nginx and Docker.

## 3. Completed Features

The following features were implemented:

- CSV dataset upload and processing.
- Machine learning model training using Logistic Regression and Random Forest.
- Display of model evaluation metrics.
- Confusion matrix visualization.
- PDF report and CSV result download functionality.
- User authentication functionality.
- Docker-based application deployment.
- Nginx configuration for HTTPS.
- HTTP to HTTPS redirection.
- Security headers and upload-size configuration.

## 4. Changes from Original Plan

- Docker Compose was used to manage the application and Nginx containers.
- Nginx was configured as a reverse proxy for the Django application.
- HTTPS configuration was added for secure communication.
- Application testing was performed using sample CSV datasets.

## 5. Challenges Encountered

- Configuring Docker containers and ensuring services started correctly.
- Resolving user authentication and administrator login issues.
- Configuring SSL certificates and HTTPS redirection.
- Testing CSV uploads and machine learning model execution.
- Verifying application responses through HTTPS.
- Managing application data and database backups.

## 6. Final Implementation Status

The Web-Based ML Model Evaluator was successfully implemented with CSV upload, machine learning model training, evaluation metrics, result downloads and user authentication.

The application was deployed using Docker Compose with Nginx handling HTTPS traffic.

The application was tested using sample datasets, and deployment verification was performed.
