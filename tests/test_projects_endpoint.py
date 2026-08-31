from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps" / "api" / "src"))

from fastapi.testclient import TestClient

from app.main import app


def test_projects_endpoint_returns_list_of_projects() -> None:
    client = TestClient(app)

    response = client.get("/projects")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["name"] == "Phoenix Hub"

    ai_projects = [project for project in response.json() if project["category"] == "ai"]

    assert {project["name"] for project in ai_projects} == {"CortexOps", "TIATESTER", "REQORA"}
    assert all(project["repository_url"].startswith("https://github.com/") for project in ai_projects)
