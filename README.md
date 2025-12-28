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
...

## API Endpoints

### Predict Customer Churn
**POST /predict**

#### Request Body
```json
{
  "age": 35,
  "tenure": 12,
  "monthly_charges": 75.5,
  "total_charges": 905.5,
  "contract_type": "month-to-month"
}

Response
{
  "churn_probability": 1.0,
  "churn_prediction": true
}
Database Auditing

All prediction requests and results are logged in PostgreSQL, including:

Input request data (JSON)

Churn probability

Prediction result

This ensures traceability and auditing of model predictions.

Running the Application
Prerequisites

Docker

Docker Compose

Run Commands
docker-compose build --no-cache
docker-compose up


The API will be available at:

http://localhost:5000
