from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps" / "api" / "src"))

from fastapi.testclient import TestClient

from app.main import app


def test_contact_endpoint_returns_contact_information() -> None:
    client = TestClient(app)

    response = client.get("/contact")

    assert response.status_code == 200
    assert response.json()["email"] == "murilo@phoenixhub.dev"
    assert response.json()["location"] == "Brazil"
