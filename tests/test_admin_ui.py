from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps" / "api" / "src"))

from fastapi.testclient import TestClient

from app.main import app


def test_admin_dashboard_endpoint_returns_html() -> None:
    client = TestClient(app)

    response = client.get("/admin")

    assert response.status_code == 200
    assert "Admin Dashboard" in response.text
    assert "Manage content" in response.text
