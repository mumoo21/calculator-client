
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Tests for POST /calculate

def test_basic_division():
    response = client.post(
        "/calculate",
        json={"expr": "30/4"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["result"] == 7.5
    assert data["expr"] == "30/4"
    assert data["error"] == ""


def test_percent_subtraction():
    response = client.post(
        "/calculate",
        json={"expr": "100 - 6%"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert abs(data["result"] - 94.0) < 1e-9


def test_standalone_percent():
    response = client.post(
        "/calculate",
        json={"expr": "6%"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.06) < 1e-9


def test_invalid_expr_returns_ok_false():
    response = client.post(
        "/calculate",
        json={"expr": "2**(3"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is False
    assert data["error"] != ""


def test_calculate_rejects_missing_expr():
    response = client.post("/calculate", json={})
    assert response.status_code == 422


def test_calculate_rejects_missing_json_body():
    response = client.post("/calculate")
    assert response.status_code == 422


# Tests for GET /history

def test_history_returns_list():
    response = client.get("/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_history_record_contains_required_fields():
    response = client.post(
        "/calculate",
        json={"expr": "10 + 5"},
    )
    assert response.status_code == 200
    assert response.json()["ok"] is True

    history_response = client.get("/history")
    assert history_response.status_code == 200

    records = history_response.json()
    record = next(
        item for item in records
        if item["expr"] == "10 + 5"
    )

    assert record["result"] == 15
    assert "timestamp" in record
    assert record["timestamp"] != ""


def test_history_response_schema():
    schema = app.openapi()
    history_schema = schema["paths"]["/history"]["get"]["responses"]["200"]
    response_schema = history_schema["content"]["application/json"]["schema"]

    assert response_schema["type"] == "array"
    assert response_schema["items"]["$ref"].endswith("/CalculatorLog")
