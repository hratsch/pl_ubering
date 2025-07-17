from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_login():
    response = client.post("/api/auth/login", json={"password": "test"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_trip():
    login = client.post("/api/auth/login", json={"password": "test"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/trips/", json={"date": "2025-07-14", "gross_earnings": 100.0}, headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()

# Add for expenses, get/update/delete