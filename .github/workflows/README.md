# Phoenix Hub

Este repositório contém o backend (FastAPI) e um frontend SPA (Vite + React) integrados para rodar dentro de uma única imagem Docker.

Resumo
- Backend: apps/api (FastAPI, Python)
- Frontend: apps/web (Vite + React)
- Docker: apps/api/Dockerfile usa multi-stage build para compilar o frontend e copiar o build para `src/static` do backend.
- CI: .github/workflows/ci.yml — constrói frontend, executa testes backend e testa build do Docker.

Como desenvolver localmente

Pré-requisitos
- Node.js 18 (recomendado)
- Python 3.12
- Docker (opcional, para rodar a imagem localmente)

Frontend (apps/web)

1. Entrar na pasta:

```bash
cd apps/web
