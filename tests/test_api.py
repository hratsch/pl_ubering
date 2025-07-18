import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # Add root to path for 'app' import

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "1.0.0"}

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

# Add for expenses
def test_create_expense():
    login = client.post("/api/auth/login", json={"password": "test"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/expenses/", json={"date": "2025-07-14", "category": "maintenance", "amount": 50.0}, headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()