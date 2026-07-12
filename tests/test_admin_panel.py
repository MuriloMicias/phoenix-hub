from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps" / "api" / "src"))

from fastapi.testclient import TestClient

from app.main import app


def test_admin_panel_update_profile_requires_token() -> None:
    client = TestClient(app)

    response = client.put(
        "/admin/profile",
        json={"name": "Phoenix Hub", "mission": "Updated mission"},
        headers={"Authorization": "Bearer demo-token"},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "profile updated"}
