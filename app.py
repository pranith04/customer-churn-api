from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import joblib
import time
from sqlalchemy.exc import OperationalError

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/churn_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

model = joblib.load("model.pkl")
encoder = joblib.load("encoder.pkl")

# -------------------- DATABASE MODELS --------------------

class PredictionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_data = db.Column(db.JSON)
    churn_probability = db.Column(db.Float)
    prediction = db.Column(db.Boolean)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    tenure = db.Column(db.Integer)
    monthly_charges = db.Column(db.Float)
    total_charges = db.Column(db.Float)
    contract_type = db.Column(db.String(50))

# -------------------- ROUTES --------------------

@app.route('/')
def home():
    return {"message": "Customer Churn Prediction API running"}

# predict churn
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        # Validate contract_type
        if data['contract_type'] not in encoder.classes_:
            return jsonify({
                "error": "Invalid contract_type",
                "allowed_values": list(encoder.classes_)
            }), 400

        contract_encoded = encoder.transform([data['contract_type']])[0]

        features = [[
            data['age'],
            data['tenure'],
            data['monthly_charges'],
            data['total_charges'],
            contract_encoded
        ]]

        prob = float(model.predict_proba(features)[0][1])
        prediction = bool(prob > 0.5)


        log = PredictionLog(
            request_data=data,
            churn_probability=prob,
            prediction=prediction
        )

        db.session.add(log)
        db.session.commit()

        return jsonify({
            "churn_probability": round(prob, 3),
            "churn_prediction": prediction
        })

    except Exception as e:
        return jsonify({
            "error": "Internal error during prediction",
            "details": str(e)
        }), 500


# customer data
@app.route('/insert', methods=['POST'])
def insert_customer():
    data = request.json

    customer = Customer(
        age=data['age'],
        tenure=data['tenure'],
        monthly_charges=data['monthly_charges'],
        total_charges=data['total_charges'],
        contract_type=data['contract_type']
    )

    db.session.add(customer)
    db.session.commit()

    return jsonify({
        "message": "Customer data inserted successfully"
    })

# -------------------- APP STARTUP --------------------

if __name__ == "__main__":
    for i in range(10):
        try:
            with app.app_context():
                db.create_all()
            print("Database connected successfully")
            break
        except OperationalError:
            print("Database not ready, retrying...")
            time.sleep(3)

    app.run(host="0.0.0.0", port=5000)
