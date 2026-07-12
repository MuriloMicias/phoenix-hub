from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps" / "api" / "src"))

from fastapi.testclient import TestClient

from app.main import app


def test_resume_endpoint_returns_summary() -> None:
    client = TestClient(app)

    response = client.get("/resume")

    assert response.status_code == 200
    assert response.json()["role"] == "Cloud and Platform Engineer"
    assert response.json()["location"] == "Brazil"
