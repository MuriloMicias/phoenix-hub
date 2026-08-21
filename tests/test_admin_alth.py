import os

# Ensure dev token/creds are present for tests
os.environ.setdefault("DEV_USER", "admin")
os.environ.setdefault("DEV_PASSWORD", "admin123")
os.environ.setdefault("DEV_TOKEN", "demo-token")

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_admin_no_header_returns_401():
    r = client.put("/admin/profile", json={"name": "X", "mission": "Y"})
    assert r.status_code == 401


def test_admin_malformed_header_returns_401():
    r = client.put("/admin/profile", headers={"Authorization": "Token wrong"}, json={"name": "X", "mission": "Y"})
    assert r.status_code == 401


def test_admin_invalid_token_returns_401():
    r = client.put("/admin/profile", headers={"Authorization": "Bearer wrong-token"}, json={"name": "X", "mission": "Y"})
    assert r.status_code == 401


def test_admin_valid_token_returns_200():
    token = os.environ["DEV_TOKEN"]
    r = client.put("/admin/profile", headers={"Authorization": f"Bearer {token}"}, json={"name": "X", "mission": "Y"})
    assert r.status_code == 200
    assert r.json().get("message") == "profile updated"
