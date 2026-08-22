from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "Okay"}

def test_model_endpoint_reports_v2():
    response = client.get("/model")
    assert response.status_code == 200
    assert response.json()["version"] == "v2"

def test_predict():
    response = client.post("/predict", json={
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    })
    assert response.status_code == 200
    body = response.json()
    assert "class_id" in body
    assert len(body["probabilities"]) == 3
    assert body["model_version"] == "v2"

def test_invalid_predict():
    response = client.post("/predict", json={
        "sepal_length": -5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    })
    assert response.status_code == 422

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "iris_api_requests_total" in response.text