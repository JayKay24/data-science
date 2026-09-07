import httpx  # noqa: F401
from fastapi.testclient import TestClient
from churn_prediction.app import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_predict() -> None:
    payload = {
        "monthly_charges": 85.5,
        "tenure_months": 3,
        "contract_type": 0,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "churn_prediction" in data
    assert "churn_probability" in data
