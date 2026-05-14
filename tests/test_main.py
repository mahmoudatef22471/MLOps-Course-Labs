"""
Tests for the Churn Prediction API.

Run with:
    pytest tests/ -v
    pytest tests/ -v --cov=app --cov=main --cov-report=term-missing
"""

from litestar.testing import TestClient

from app.model_utils import predict_churn
from main import app


# ---------------------------------------------------------------------------
# Function Tests
# ---------------------------------------------------------------------------


def test_predict_churn_returns_binary():
    """Test that predict_churn() returns 0 or 1."""
    sample = [619, "France", "Female", 42, 2, 0, 1, 1, 1, 101348.88]
    prediction = predict_churn(sample)
    assert prediction in (0, 1), f"Prediction should be 0 or 1, got {prediction}"


def test_predict_churn_with_edge_cases():
    """Bonus: Test predict_churn with edge-case inputs."""
    edge_cases = [
        [1, "Germany", "Male", 25, 0, 0.0, 1, 0, 0, 0.0],
        [850, "Spain", "Female", 65, 10, 250000.0, 3, 1, 1, 200000.0],
    ]
    for edge_case in edge_cases:
        prediction = predict_churn(edge_case)
        assert prediction in (0, 1), f"Prediction should be 0 or 1, got {prediction}"


# ---------------------------------------------------------------------------
# Endpoint Tests
# ---------------------------------------------------------------------------


def test_post_predict_valid_request():
    """Test POST /predict with valid JSON and check status and response."""
    with TestClient(app=app) as client:
        payload = {
            "CreditScore": 619,
            "geography": "France",
            "gender": "Female",
            "age": 42,
            "tenure": 2,
            "balance": 0,
            "num_of_products": 1,
            "has_cr_card": 1,
            "is_active_member": 1,
            "estimated_salary": 101348.88,
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "prediction" in data, "Response should contain 'prediction' field"
        assert data["prediction"] in (0, 1), "Prediction should be 0 or 1"


def test_get_health():
    """Test GET /health endpoint."""
    with TestClient(app=app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


def test_get_home():
    """Test GET / endpoint."""
    with TestClient(app=app) as client:
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Welcome" in data["message"]


def test_post_predict_invalid_input():
    """Bonus: Test that invalid input returns status 400."""
    with TestClient(app=app) as client:
        invalid_payload = {
            "CreditScore": "not_an_int",  # Invalid type
            "geography": "France",
            "gender": "Female",
            "age": 42,
            "tenure": 2,
            "balance": 0,
            "num_of_products": 1,
            "has_cr_card": 1,
            "is_active_member": 1,
            "estimated_salary": 101348.88,
        }
        response = client.post("/predict", json=invalid_payload)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict), "Response body should be a JSON object"
        assert "detail" in data or "errors" in data, (
            "Validation error response should include details"
        )
