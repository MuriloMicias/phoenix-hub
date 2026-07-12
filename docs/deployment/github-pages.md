# Publicação com GitHub Pages

## Visão geral
O projeto já possui uma API FastAPI funcional e um painel administrativo simples. Para publicar o site de forma simples e gratuita, o caminho mais direto é:

1. Publicar o frontend estático no GitHub Pages.
2. Manter a API no mesmo repositório ou em um serviço separado como Render, Railway ou Azure Container Apps.
3. Usar um domínio personalizado no futuro.

## O que já existe
- API FastAPI com endpoints públicos e administrativos.
- Estrutura Docker para rodar a API localmente.
- Repositório GitHub com fluxo de branches e tags.

## O que falta para publicar
- Criar a pasta do frontend estático ou um build do site.
- Adicionar workflow de GitHub Actions para publicar os arquivos estáticos.
- Definir se a API ficará no mesmo repositório ou em um serviço externo.
- Configurar variáveis de ambiente e domínio se necessário.

## Recomendações
- Para a primeira publicação, usar GitHub Pages com um site estático simples.
- Para a API, usar Render ou Azure Container Apps, já que o projeto já está preparado para FastAPI.
- Separar frontend e backend em deploys diferentes para deixar a operação mais limpa.
