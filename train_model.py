import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("churn_data.csv")

encoder = LabelEncoder()
df['contract_type'] = encoder.fit_transform(df['contract_type'])

X = df.drop('churn', axis=1)
y = df['churn']

model = LogisticRegression()
model.fit(X, y)

joblib.dump(model, "model.pkl")
joblib.dump(encoder, "encoder.pkl")

print("Model and encoder saved successfully")

