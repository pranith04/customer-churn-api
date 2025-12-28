# Customer Churn Prediction API

## Overview
This project implements a Flask-based REST API to predict customer churn probability using a machine learning model.  
The application is containerized using Docker and uses PostgreSQL to store prediction requests and results for auditing.

The project demonstrates an end-to-end ML deployment workflow including model training, API development, database integration, and containerized deployment.

---

## Technologies Used
- Python
- Flask
- scikit-learn
- PostgreSQL
- SQLAlchemy
- Docker
- Docker Compose

---

## System Architecture
- Flask API container for serving predictions
- PostgreSQL container for storing prediction logs
- Machine learning model trained using Logistic Regression
- SQLAlchemy ORM for database interactions

---

## API Endpoints

### Health Check
**GET /**

Response:
```json
{
  "message": "Customer Churn Prediction API running"
}

