from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_and_login():
    # Register new user
    register_data = {
        "username": "testuser",
        "password": "pass123",
        "role": "user"
    }
    r = client.post("/register", json=register_data)
    assert r.status_code == 200
    assert r.json()["username"] == "testuser"

    # Login with same user
    login_data = {
        "username": "testuser",
        "password": "pass123"
    }
    r = client.post("/token", data=login_data)
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
