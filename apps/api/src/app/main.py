import logging
import secrets
from pathlib import Path

from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.core.settings import get_settings
from app.auth import get_token

settings = get_settings()
is_production = settings.environment.lower() == "production"
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    docs_url=None if is_production else "/docs",
    redoc_url=None if is_production else "/redoc",
    openapi_url=None if is_production else "/openapi.json",
)
logger = logging.getLogger("phoenix_hub.auth")

STATIC_DIR = Path("src/static")
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

PROJECTS = [
    {
        'name': 'Phoenix Hub',
        'description': 'Engineering platform for portfolio and technical projects',
        'stack': 'FastAPI, Docker, Python',
    }
]

ARTICLES = [
    {
        'title': 'Knowledge Center Introduction',
        'slug': 'knowledge-center-introduction',
        'category': 'Engineering',
        'content': 'A simple introduction to the knowledge center module.',
    }
]

PROFILE = {
    'name': 'Phoenix Hub',
    'mission': 'Engineering platform',
}

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
        'project': 'phoenix-hub',
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
    return PROJECTS

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
    # Keep comparisons timing-safe and do not log credentials. The diagnostic
    # fields below are sufficient to troubleshoot production configuration
    # without exposing the username/password values.
    configured_user = settings.dev_user or ""
    configured_password = settings.dev_password or ""
    username_matches = secrets.compare_digest(payload.username, configured_user)
    password_matches = secrets.compare_digest(payload.password, configured_password)

    if username_matches and password_matches:
        return {'token': settings.dev_token}

    logger.warning(
        "Login rejected: username_matches=%s submitted_password_length=%d configured_password_length=%d",
        username_matches,
        len(payload.password),
        len(configured_password),
    )
    from fastapi import HTTPException, status

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

@app.get('/admin/profile', dependencies=[Depends(get_token)])
def get_profile() -> dict[str, str]:
    return PROFILE

@app.put('/admin/profile', dependencies=[Depends(get_token)])
def update_profile(payload: ProfileUpdateRequest) -> dict[str, str]:
    PROFILE['name'] = payload.name
    PROFILE['mission'] = payload.mission
    return {'message': 'profile updated'}

@app.get('/articles', response_model=list[ArticleOut])
def list_articles() -> list[dict[str, str]]:
    return ARTICLES

@app.get('/admin/summary')
def admin_summary() -> dict[str, int | str]:
    return {
        'projects': len(PROJECTS),
        'articles': len(ARTICLES),
        'status': 'ok',
    }

@app.post('/admin/articles', dependencies=[Depends(get_token)], response_model=ArticleOut)
def create_article(payload: ArticleCreateRequest) -> dict[str, str]:
    new_article = {
        'title': payload.title,
        'slug': payload.slug,
        'category': payload.category,
        'content': payload.content,
    }
    ARTICLES.insert(0, new_article)
    return new_article

@app.delete('/admin/articles/{slug}', dependencies=[Depends(get_token)])
def delete_article(slug: str) -> dict[str, str]:
    for index, article in enumerate(ARTICLES):
        if article['slug'] == slug:
            del ARTICLES[index]
            return {'message': f'Article {slug} deleted'}

    from fastapi import HTTPException, status
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Article not found')

HTML_CONTENT = """
<html>
  <head><title>Admin Dashboard</title></head>
  <body>
    <h1>Admin Dashboard</h1>
    <p>Manage content</p>
    <a href='/articles'>View articles</a>
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
