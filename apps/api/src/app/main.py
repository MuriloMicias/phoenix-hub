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
        'category': 'platform',
        'repository_url': 'https://github.com/MuriloMicias/phoenix-hub',
    },
    {
        'name': 'CortexOps',
        'description': (
            'Plataforma de IA para DevOps, SRE e Operações, voltada à análise '
            'de ambientes, observabilidade, automação e apoio à tomada de decisões '
            'sobre infraestrutura e aplicações.'
        ),
        'stack': 'AI, DevOps, SRE, Observability',
        'category': 'ai',
        'repository_url': 'https://github.com/projects-techuser/CortexOps',
    },
    {
        'name': 'TIATESTER',
        'description': (
            'Plataforma de IA para Qualidade e Testes de Software, capaz de analisar '
            'sistemas, requisitos e código para apoiar a criação, execução, cobertura '
            'e análise de testes.'
        ),
        'stack': 'AI, Quality Engineering, Testing',
        'category': 'ai',
        'repository_url': 'https://github.com/projects-techuser/TIATESTER',
    },
    {
        'name': 'REQORA',
        'description': (
            'Plataforma de IA para Engenharia de Requisitos, focada na análise, '
            'organização, rastreabilidade e relacionamento de requisitos, com '
            'identificação de conflitos, impactos, riscos e apoio à tomada de decisões.'
        ),
        'stack': 'AI, Requirements Engineering, Traceability',
        'category': 'ai',
        'repository_url': 'https://github.com/projects-techuser/REQORA',
    },
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
    category: str
    repository_url: str

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

def curriculum_semester(
    semester: int, *courses: tuple[str, int | None]
) -> dict[str, object]:
    return {
        'semester': semester,
        'courses': [
            {'name': name, 'hours': hours}
            for name, hours in courses
        ],
    }


@app.get('/education')
def education() -> list[dict[str, object]]:
    return [
        {
            'institution': 'Universidade Braz Cubas',
            'degree': 'Análise e Desenvolvimento de Sistemas',
            'period': '06/2016 - 12/2018',
            'curriculum': [
                curriculum_semester(
                    1,
                    ('Algoritmos e Pensamento Computacional', 90),
                    ('Desenvolvimento Front-end para Web', 90),
                    ('Design Profissional', 90),
                    ('Meio Ambiente e Cuidados de Saúde', 40),
                    ('Modelagem de Banco de Dados', 90),
                ),
                curriculum_semester(
                    2,
                    ('Engenharia de Prompt e Aplicações em IA', 90),
                    ('Humanidades e a População Brasileira', 40),
                    ('Interface e Jornada do Usuário', 90),
                    ('Programação de Computadores', 90),
                    ('Prototipagem de Sistemas Computacionais', 90),
                ),
                curriculum_semester(
                    3,
                    ('Competências Abertas', 90),
                    ('Desenvolvimento Back-end', 90),
                    ('Desenvolvimento de Aplicativos Móveis', 90),
                    ('Projeto de Software', 120),
                    ('Optativa', 40),
                    ('Competências Abertas', 90),
                ),
                curriculum_semester(
                    4,
                    ('Desenvolvimento de Banco de Dados', 90),
                    ('Desenvolvimento de Sistemas de Informação', 90),
                    ('Economia Sustentável', 100),
                    ('Competências Abertas', 90),
                    ('Optativa', 40),
                    ('Competências Abertas', 90),
                ),
            ],
        },
        {
            'institution': 'UNIVESP',
            'degree': 'Bacharelado em Engenharia da Computação',
            'period': '01/2020 - 01/2025',
            'curriculum': [
                curriculum_semester(
                    1,
                    ('Pensamento Computacional', 80),
                    ('Leitura e Produção de Textos', 80),
                    ('Ética, Cidadania e Sociedade', 40),
                    ('Matemática Básica', 80),
                    ('Inglês', 80),
                    ('Metodologia Científica', 40),
                ),
                curriculum_semester(
                    2,
                    ('Algoritmos e Programação de Computadores I', 80),
                    ('Cálculo I', 80),
                    ('Introdução a Conceitos de Computação', 40),
                    ('Algoritmos e Programação de Computadores II', 80),
                    ('Fundamentos Matemáticos para Computação', 80),
                    ('Fundamentos de Web', 40),
                ),
                curriculum_semester(
                    3,
                    ('Sistemas Computacionais', 80),
                    ('Estruturas de Dados', 80),
                    ('Formação Profissional em Computação', 40),
                    ('Estatística e Probabilidade', 80),
                    ('Programação Orientada a Objetos', 80),
                    ('Gestão da Inovação e Desenvolvimento de Produtos', 40),
                ),
                curriculum_semester(
                    4,
                    ('Projeto Integrador I', None),
                    ('Banco de Dados', 80),
                    ('Cálculo II', 80),
                    ('Física do Movimento', 80),
                    ('Circuitos Digitais', 80),
                ),
                curriculum_semester(
                    5,
                    ('Projeto Integrador II', None),
                    ('Engenharia de Software', 80),
                    ('Sistemas Embarcados', 80),
                    ('Protocolos de Comunicação IoT', 80),
                    ('Geometria Analítica e Álgebra Linear', 80),
                ),
                curriculum_semester(
                    6,
                    ('Projeto Integrador III', None),
                    ('Infraestrutura para Sistemas de Software', 80),
                    ('Plataforma de Análise e Desenvolvimento de Sistemas', 80),
                    ('Desenvolvimento Web', 80),
                    ('Interface Humano-Computador', 80),
                ),
                curriculum_semester(
                    7,
                    ('Projeto Integrador IV', None),
                    ('Mecânica dos Sólidos e dos Fluidos', 80),
                    ('Projeto e Análise de Algoritmos', 80),
                    ('Processamento Digital de Sinais', 80),
                    ('Desenvolvimento para Dispositivos Móveis', 80),
                ),
                curriculum_semester(
                    8,
                    ('Projeto Integrador V', None),
                    ('Química Tecnológica e Ambiental', 80),
                    ('Controle e Automação', 80),
                    ('Planejamento Estratégico de Negócios', 80),
                    ('Computação Escalável', 80),
                ),
                curriculum_semester(
                    9,
                    ('Projeto Integrador VI', None),
                    ('Impactos da Computação na Sociedade', 80),
                    ('Eletiva', 80),
                    ('Compiladores', 80),
                    ('Eletiva', 80),
                ),
                curriculum_semester(
                    10,
                    ('TCC', 80),
                    ('Cidades Inteligentes', 80),
                    ('Eletiva', 80),
                    ('Legislação e Responsabilidade Profissional', 80),
                    ('Eletiva', 80),
                ),
            ],
        },
        {
            'institution': 'UNIVESP',
            'degree': 'Bacharelado em Tecnologia da Informação — ênfase em IoT',
            'period': '06/2021 - 06/2024',
            'curriculum': [
                curriculum_semester(
                    1,
                    ('Pensamento Computacional', 80),
                    ('Leitura e Produção de Textos', 80),
                    ('Ética, Cidadania e Sociedade', 40),
                    ('Matemática Básica', 80),
                    ('Inglês', 80),
                    ('Projetos e Métodos para a Produção do Conhecimento', 40),
                ),
                curriculum_semester(
                    2,
                    ('Algoritmos e Programação de Computadores I', 80),
                    ('Cálculo I', 80),
                    ('Introdução a Conceitos de Computação', 40),
                    ('Algoritmos e Programação de Computadores II', 80),
                    ('Fundamentos Matemáticos para Computação', 80),
                    ('Fundamentos de Internet e Web', 40),
                ),
                curriculum_semester(
                    3,
                    ('Sistemas Computacionais', 80),
                    ('Estruturas de Dados', 80),
                    ('Formação Profissional em Computação', 40),
                    ('Estatística e Probabilidade', 80),
                    ('Programação Orientada a Objetos', 80),
                    ('Gestão da Inovação e Desenvolvimento de Produtos', 40),
                ),
                curriculum_semester(
                    4,
                    ('Projeto Integrador I', None),
                    ('Banco de Dados', 80),
                    ('Infraestrutura para Sistemas de Software', 80),
                    ('Desenvolvimento Web', 80),
                    ('Interface Humano-Computador', 80),
                ),
                curriculum_semester(
                    5,
                    ('Projeto Integrador II', None),
                    ('Engenharia de Software', 80),
                    ('Segurança da Informação', 80),
                    ('Aplicações em Aprendizado de Máquina', 80),
                    ('Desenvolvimento para Dispositivos Móveis', 80),
                ),
                curriculum_semester(
                    6,
                    ('Projeto Integrador III', None),
                    ('Gerência da Qualidade de Software', 80),
                    ('Sistemas de Informação', 80),
                    ('Computação Escalável', 80),
                    ('Planejamento Estratégico de Negócios', 80),
                ),
            ],
        },
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
