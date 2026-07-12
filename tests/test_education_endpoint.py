from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps" / "api" / "src"))

from fastapi.testclient import TestClient

from app.main import app


def test_education_endpoint_returns_list_of_education_items() -> None:
    client = TestClient(app)

    response = client.get("/education")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["institution"] == "University"
