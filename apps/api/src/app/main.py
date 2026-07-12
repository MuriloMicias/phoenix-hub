from fastapi import FastAPI

from app.core.settings import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version, debug=settings.debug)


@app.get('/health')
def health_check() -> dict[str, str]:
    return {
        'status': 'healthy',
        'project': settings.project_name,
        'version': settings.app_version,
    }


@app.get('/projects')
def list_projects() -> list[dict[str, str]]:
    return [
        {
            'name': 'Phoenix Hub',
            'description': 'Engineering platform for portfolio and technical projects',
            'stack': 'FastAPI, Docker, Python',
        }
    ]


@app.get('/metrics')
def metrics() -> dict[str, str]:
    return {
        'status': 'ok',
        'service': settings.service_name,
    }


@app.get('/about')
def about() -> dict[str, str]:
    return {
        'name': 'Phoenix Hub',
        'mission': 'Engineering platform for portfolio and technical excellence',
    }


@app.get('/contact')
def contact() -> dict[str, str]:
    return {
        'email': 'murilo@phoenixhub.dev',
        'location': 'Brazil',
    }


@app.get('/resume')
def resume() -> dict[str, str]:
    return {
        'role': 'Cloud and Platform Engineer',
        'location': 'Brazil',
    }


@app.get('/skills')
def skills() -> list[dict[str, str]]:
    return [
        {'name': 'Python', 'category': 'Backend'},
        {'name': 'Docker', 'category': 'Infrastructure'},
    ]


@app.get('/experience')
def experience() -> list[dict[str, str]]:
    return [
        {
            'title': 'Platform Engineer',
            'company': 'Phoenix Hub',
            'period': '2024 - Present',
        }
    ]


@app.get('/education')
def education() -> list[dict[str, str]]:
    return [
        {
            'institution': 'University',
            'degree': 'Computer Science',
            'period': '2020 - 2024',
        }
    ]


@app.get('/certifications')
def certifications() -> list[dict[str, str]]:
    return [
        {
            'name': 'Azure Fundamentals',
            'issuer': 'Microsoft',
            'issued_at': '2024-01',
            'image_url': '/assets/certificates/azure-fundamentals.png',
        }
    ]
