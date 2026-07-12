# Versionamento e Tags

## Estratégia

O projeto utiliza Semantic Versioning (SemVer 2.0.0) no formato MAJOR.MINOR.PATCH.

- MAJOR: mudanças incompatíveis, marcos importantes ou lançamento oficial
- MINOR: novas funcionalidades compatíveis com versões anteriores
- PATCH: correções de bugs, documentação e pequenas melhorias sem alterar compatibilidade

### Exemplos

- 1.2.3
- 0.2.1 para correções
- 0.3.0 para novas funcionalidades
- 1.0.0 para lançamento oficial

## Tags Git

As tags devem seguir o padrão:

- v0.1.0 - Foundation
- v0.2.0 - Backend API
- v0.3.0 - Frontend
- v0.4.0 - Portfolio
- v0.5.0 - Blog
- v0.6.0 - CMS
- v0.7.0 - Observability
- v0.8.0 - CI/CD
- v0.9.0 - Cloud Ready
- v1.0.0 - First Production Release

## Regras de versionamento

- Commits devem seguir Conventional Commits
- Tags devem ser criadas apenas para marcos importantes do projeto
- Toda tag publicada deve ter uma GitHub Release associada
- O CHANGELOG deve ser atualizado em cada release
- A branch main deve conter apenas versões estáveis
- A branch develop concentra desenvolvimento contínuo
- Funcionalidades devem ser desenvolvidas em branches feature/*

## Fluxo de publicação

1. Criar branch de funcionalidade a partir de develop
2. Implementar e validar mudanças
3. Abrir pull request para develop
4. Validar e integrar
5. Merge para main
6. Criar tag semântica vX.Y.Z
7. Publicar GitHub Release
8. Atualizar CHANGELOG

## Exemplo

```bash
git checkout develop
git checkout -b feature/nova-funcionalidade
git commit -m "feat(api): add new endpoint"
git push origin feature/nova-funcionalidade
# abrir PR para develop
# após merge

git checkout main
git pull origin main
git tag v0.3.0
git push origin v0.3.0
```
