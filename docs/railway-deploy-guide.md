# Railway Deploy Guide

## Objetivo

Este guia cobre o deploy final do backend no Railway usando:

- plano `Free`
- deploy pela UI do Railway
- repositorio GitHub atual
- sem Docker
- volume persistente para o arquivo SQLite

## Por Que Railway

O backend deste projeto precisa de:

- URL publica estavel para o Dify
- deploy simples de uma aplicacao Python
- persistencia leve para `SQLite`

O Railway atende esse caso com menos atrito do que alternativas equivalentes para este projeto.

Decisao adotada:

- plataforma: `Railway`
- builder: padrao do Railway
- sem Dockerfile
- volume montado em `/data`

## Pre-Requisitos

Antes de iniciar no Railway:

- o repositorio precisa estar no GitHub com a branch `develop` atualizada
- o backend local precisa continuar verde em `pytest backend/tests -q`
- o checkpoint DSL do Studio pode continuar apontando para a URL temporaria; a troca para a URL final acontece depois do deploy

## Configuracao Do Servico

Criar um projeto novo no Railway e conectar o repositorio GitHub deste projeto.

No servico do backend, usar:

- source: repositorio GitHub atual
- root directory: raiz do repositrio
- custom start command:

```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

Adicionar estas configuracoes:

- healthcheck path: `/health`
- volume: `1` volume
- mount path do volume: `/data`

Variavel de ambiente obrigatoria:

```text
SUPPORT_ASSISTANT_DB_PATH=/data/support-assistant.db
```

Observacao importante:

- o `TicketRepository` ja le `SUPPORT_ASSISTANT_DB_PATH` automaticamente
- nao e necessario mudar o codigo para usar esse path no Railway

## Ordem Recomendada No Railway

1. criar o projeto
2. adicionar o repositorio GitHub
3. abrir o servico gerado para o backend
4. configurar o `Start Command`
5. adicionar a variavel `SUPPORT_ASSISTANT_DB_PATH`
6. criar e anexar o volume em `/data`
7. configurar o healthcheck em `/health`
8. aguardar o deploy completar
9. abrir a URL publica `.railway.app`
10. validar `GET /health`

## Validacao Depois Do Deploy

Validacoes minimas:

```bash
curl https://SUA-URL.railway.app/health
```

Esperado:

```json
{"status":"ok"}
```

Depois disso:

- trocar no Dify as duas URLs `trycloudflare` pela URL final do Railway
- retestar lookup e criacao no `Preview`
- publicar o app no Studio
- exportar o DSL final

## Limites Do Plano Free

O Railway Free e suficiente para esta entrega, mas com limites pequenos.

Pontos principais:

- `0.5 GB` de volume
- `1` volume por projeto
- menos folga de recursos do que o plano Hobby

Para esta API pequena com `SQLite`, isso deve ser suficiente para a demo final.
