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

## Login de administrador no Render

O login usa as variáveis `DEV_USER`, `DEV_PASSWORD` e `DEV_TOKEN`. Para não
perder acesso à senha, `DEV_PASSWORD` não é gerada automaticamente no
Blueprint. Antes de publicar, abra o serviço no Render em **Environment** e
defina uma senha forte para `DEV_PASSWORD`; mantenha `DEV_USER=admin` ou
escolha outro usuário e atualize a variável também. Salve as alterações e faça
um redeploy. `DEV_TOKEN` pode continuar como valor gerado pelo Render, pois é
entregue pela API somente depois da autenticação.

Não use as credenciais de exemplo (`admin` / `admin123`) em produção.
