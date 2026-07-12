from fastapi import FastAPI

from app.core.settings import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version, debug=settings.debug)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "project": settings.project_name,
        "version": settings.app_version,
    }


@app.get("/projects")
def list_projects() -> list[dict[str, str]]:
    return [
        {
            "name": "Phoenix Hub",
            "description": "Engineering platform for portfolio and technical projects",
            "stack": "FastAPI, Docker, Python",
        }
    ]
