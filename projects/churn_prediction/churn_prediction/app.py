from typing import Any, Dict
from fastapi import FastAPI
from pydantic import BaseModel
from churn_prediction.train import get_trained_model

app = FastAPI(title="Customer Churn Prediction API")
model = get_trained_model()


class CustomerPayload(BaseModel):
    monthly_charges: float
    tenure_months: int
    contract_type: int


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "healthy"}


@app.post("/predict")
def predict_churn(customer: CustomerPayload) -> Dict[str, Any]:
    features = [
        [customer.monthly_charges, customer.tenure_months, customer.contract_type]
    ]
    prediction = int(model.predict(features)[0])
    prob = float(model.predict_proba(features)[0][1])
    return {
        "churn_prediction": prediction,
        "churn_probability": round(prob, 4),
    }
