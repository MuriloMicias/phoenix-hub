from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps" / "api" / "src"))

from fastapi.testclient import TestClient

from app.main import app


def test_about_endpoint_returns_project_summary() -> None:
    client = TestClient(app)

    response = client.get("/about")

    assert response.status_code == 200
    assert response.json()["name"] == "Phoenix Hub"
    assert response.json()["mission"] == "Engineering platform for portfolio and technical excellence"
