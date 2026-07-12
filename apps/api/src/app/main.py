from fastapi import FastAPI, Header
from pydantic import BaseModel

from app.core.settings import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version, debug=settings.debug)


class LoginRequest(BaseModel):
    username: str
    password: str


class ProfileUpdateRequest(BaseModel):
    name: str
    mission: str


class ArticleCreateRequest(BaseModel):
    title: str
    slug: str
    content: str
    category: str


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


@app.post('/auth/login')
def login(payload: LoginRequest) -> dict[str, str]:
    if payload.username == 'admin' and payload.password == 'admin123':
        return {'token': 'demo-token'}
    return {'detail': 'invalid credentials'}


@app.put('/admin/profile')
def update_profile(payload: ProfileUpdateRequest, authorization: str | None = Header(default=None, alias='Authorization')) -> dict[str, str]:
    if authorization != 'Bearer demo-token':
        return {'detail': 'unauthorized'}

    return {'message': 'profile updated'}


@app.get('/articles')
def list_articles() -> list[dict[str, str]]:
    return [
        {
            'title': 'Knowledge Center Introduction',
            'slug': 'knowledge-center-introduction',
            'category': 'Engineering',
            'content': 'A simple introduction to the knowledge center module.',
        }
    ]


@app.post('/admin/articles')
def create_article(payload: ArticleCreateRequest, authorization: str | None = Header(default=None, alias='Authorization')) -> dict[str, str]:
    if authorization != 'Bearer demo-token':
        return {'detail': 'unauthorized'}

    return {
        'title': payload.title,
        'slug': payload.slug,
        'category': payload.category,
        'content': payload.content,
    }


@app.get('/admin', include_in_schema=False)
def admin_dashboard() -> str:
    return '''
    <html>
      <head><title>Admin Dashboard</title></head>
      <body>
        <h1>Admin Dashboard</h1>
        <p>Manage content</p>
        <ul>
          <li><a href='/docs'>API Docs</a></li>
          <li><a href='/articles'>View articles</a></li>
        </ul>
      </body>
    </html>
    '''
