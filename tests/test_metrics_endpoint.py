from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps" / "api" / "src"))

from fastapi.testclient import TestClient

from app.main import app


def test_metrics_endpoint_returns_basic_observability_payload() -> None:
    client = TestClient(app)

    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "phoenix-hub-api"
