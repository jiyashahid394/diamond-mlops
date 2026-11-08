from fastapi.testclient import TestClient

from app import app

client = TestClient(app)
GOOD = {"carat": 0.7, "depth": 61.5, "table": 57}


def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_predict_returns_positive_price():
    r = client.post("/predict", json=GOOD)
    assert r.status_code == 200
    assert r.json()["price_usd"] > 0


def test_bad_input_gives_422():
    bad = {"carat": "five", "depth": 61.5, "table": 57}
    assert client.post("/predict", json=bad).status_code == 422
    zero = {"carat": 0, "depth": 61.5, "table": 57}
    assert client.post("/predict", json=zero).status_code == 422


def test_metrics_endpoint():
    client.post("/predict", json=GOOD)
    r = client.get("/metrics")
    assert r.status_code == 200 and "predictions_total" in r.text
