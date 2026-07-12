from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps" / "api" / "src"))

from fastapi.testclient import TestClient

from app.main import app


def test_articles_endpoint_returns_seed_content() -> None:
    client = TestClient(app)

    response = client.get("/articles")

    assert response.status_code == 200
    assert response.json()[0]["slug"] == "knowledge-center-introduction"


def test_admin_can_create_article() -> None:
    client = TestClient(app)

    response = client.post(
        "/admin/articles",
        json={
            "title": "New Article",
            "slug": "new-article",
            "content": "This is a new article.",
            "category": "Engineering",
        },
        headers={"Authorization": "Bearer demo-token"},
    )

    assert response.status_code == 200
    assert response.json()["slug"] == "new-article"
