# API

Backend do Phoenix Hub para o sprint PHX-002.

## Executar localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r apps/api/requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Verificar saúde

```bash
curl http://localhost:8000/health
```

Resposta esperada:

```json
{
  "status": "healthy",
  "project": "phoenix-hub",
  "version": "0.1.0"
}
```

