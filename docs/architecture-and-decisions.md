# Architecture And Decisions

## Objetivo

Este projeto foi mantido propositalmente pequeno para ser facil de revisar, explicar e demonstrar.

## Decisoes Principais

- `FastAPI`
API pequena, explicita e rapida de entender.

- `SQLite`
Persistencia simples e suficiente para a demo, sem overhead de banco mais pesado.

- `Chatflow` no Dify Studio
Fluxo visual adequado para separar conhecimento, lookup e criacao de ticket.

- `Knowledge Retrieval`
Usado apenas para perguntas documentais.

- `HTTP Request`
Escolhido como integracao mais direta e mais facil de explicar para acoes transacionais.

## Simplificacoes Intencionais

- sem autenticacao
- sem banco externo
- sem plugin customizado
- sem observabilidade avancada
- sem interface administrativa

Essas simplificacoes foram deliberadas para manter o escopo compativel com o teste tecnico.

## Separacao De Responsabilidades

- `knowledge/` responde duvidas documentais
- `backend/` e o sistema de registro para tickets
- `Studio` orquestra intencao, follow-up e chamadas HTTP

## Limites Do Estado Atual

O projeto ja esta funcional em execucao local e integracao temporaria, mas ainda faltam artefatos de entrega final:

- export final do Studio
- video curto da demo
- deploy final estavel

Esses pontos ficam explicitamente para os blocos `L` e `M`.
