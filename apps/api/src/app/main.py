from pathlib import Path

from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.core.settings import get_settings
from app.auth import get_token

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version, debug=settings.debug)

STATIC_DIR = Path("src/static")
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Response / Request models
class ProjectOut(BaseModel):
    name: str
    description: str
    stack: str

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str

class ProfileUpdateRequest(BaseModel):
    name: str
    mission: str

class ArticleCreateRequest(BaseModel):
    title: str
    slug: str
    content: str
    category: str

class ArticleOut(BaseModel):
    title: str
    slug: str
    category: str
    content: str

@app.get('/health')
def health_check() -> dict[str, str]:
    return {
        'status': 'healthy',
        'project': settings.app_name,
        'version': settings.app_version,
    }

# Serve SPA index.html at root
@app.get('/', response_class=HTMLResponse)
def root():
    index_path = "src/static/index.html"
    try:
        return FileResponse(index_path)
    except Exception:
        # fallback to a JSON response if file not found (during local dev before build)
        return {
            'status': 'ok',
            'project': settings.app_name,
            'version': settings.app_version,
            'message': 'Welcome to Phoenix Hub'
        }

@app.get('/favicon.ico')
def favicon():
    # If a favicon exists in static, this will be served automatically at /static/favicon.ico
    # Keep this for backward compatibility
    return FileResponse('src/static/favicon.ico') if False else HTMLResponse(status_code=204)

@app.get('/projects', response_model=list[ProjectOut])
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

@app.post('/auth/login', response_model=LoginResponse)
def login(payload: LoginRequest) -> dict[str, str]:
    # simple dev authentication: compare with settings dev_user/dev_password
    if payload.username == settings.dev_user and payload.password == settings.dev_password:
        return {'token': settings.dev_token}
    from fastapi import HTTPException, status

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

@app.put('/admin/profile', dependencies=[Depends(get_token)])
def update_profile(payload: ProfileUpdateRequest) -> dict[str, str]:
    return {'message': 'profile updated'}

@app.get('/articles', response_model=list[ArticleOut])
def list_articles() -> list[dict[str, str]]:
    return [
        {
            'title': 'Knowledge Center Introduction',
            'slug': 'knowledge-center-introduction',
            'category': 'Engineering',
            'content': 'A simple introduction to the knowledge center module.',
        }
    ]

@app.get('/admin/summary')
def admin_summary() -> dict[str, int | str]:
    return {
        'projects': len(list_projects()),
        'articles': len(list_articles()),
        'status': 'ok',
    }

@app.post('/admin/articles', dependencies=[Depends(get_token)], response_model=ArticleOut)
def create_article(payload: ArticleCreateRequest) -> dict[str, str]:
    return {
        'title': payload.title,
        'slug': payload.slug,
        'category': payload.category,
        'content': payload.content,
    }

HTML_CONTENT = """
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
"""

@app.get('/admin', include_in_schema=False, response_class=HTMLResponse)
def admin_dashboard() -> HTMLResponse:
    index_path = "src/static/index.html"
    try:
        return FileResponse(index_path)
    except Exception:
        return HTMLResponse(content=HTML_CONTENT)
