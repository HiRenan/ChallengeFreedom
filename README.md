# ChallengeFreedom

Assistente de suporte corporativo, combinando:

- `Dify Studio` com `Chatflow`
- `Knowledge Retrieval` para perguntas documentais
- backend proprio em `Python + FastAPI`
- persistencia simples com `SQLite`

## O Que O Projeto Faz

O assistente consegue:

- responder perguntas usando a base de conhecimento
- consultar um ticket por ID no formato `TKT-1234`
- abrir um novo ticket
- pedir dados faltantes antes de criar o ticket
- retornar mensagens curtas e claras para `400`, `404` e `422`

## Arquitetura

O projeto foi desenhado em tres partes:

1. `knowledge/`
Conteudo curto e curado para FAQ, politica de abertura de ticket, tipos de solicitacao e fluxo de atendimento.

2. `backend/`
API REST em FastAPI com:
- `GET /health`
- `GET /tickets/{ticket_id}`
- `POST /tickets`

3. `Dify Studio`
Chatflow com separacao explicita entre:
- caminho de conhecimento
- lookup de ticket
- criacao de ticket
- esclarecimento de intencao ambigua

## Como Rodar O Backend Localmente

Pre-requisitos:

- Python 3.10+

Instalacao:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Variaveis de ambiente:

Use o arquivo `.env.example` como referencia.

Valores atuais:

- `SUPPORT_ASSISTANT_DB_PATH=artifacts/runtime/support-assistant.db`
- `SUPPORT_ASSISTANT_API_BASE_URL=http://127.0.0.1:8000`

Execucao local:

```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Rodando os testes:

```bash
pytest backend/tests -q
```

## Endpoints Principais

### `GET /health`

Resposta:

```json
{"status":"ok"}
```

### `GET /tickets/{ticket_id}`

Exemplo:

```bash
curl http://127.0.0.1:8000/tickets/TKT-1001
```

Sucesso:

```json
{
  "id": "TKT-1001",
  "requester_name": "Marina Costa",
  "requester_email": "marina.costa@example.com",
  "subject": "VPN access blocked",
  "description": "I cannot connect to the company VPN since this morning.",
  "status": "open"
}
```

Erros esperados:

- `400` para ID invalido
- `404` para ticket nao encontrado

### `POST /tickets`

Campos minimos obrigatorios:

- `requester_name`
- `requester_email`
- `subject`
- `description`

Exemplo:

```bash
curl -X POST http://127.0.0.1:8000/tickets ^
  -H "Content-Type: application/json" ^
  -d "{\"requester_name\":\"Renan\",\"requester_email\":\"renan@example.com\",\"subject\":\"VPN issue\",\"description\":\"I cannot connect to the VPN.\"}"
```

Erros esperados:

- `422` para dados ausentes ou invalidos

## Como O Studio Se Conecta Ao Backend

No Dify Studio, o Chatflow usa:

- `Knowledge Retrieval` para perguntas documentais
- `HTTP Request` para `GET /tickets/{ticket_id}`
- `HTTP Request` para `POST /tickets`

Na integracao validada ate agora, o Chatflow ja foi testado com:

- pergunta documental
- lookup de ticket existente
- lookup de ticket inexistente
- criacao com dados faltantes
- criacao com dados completos

O deploy final com URL estavel ainda sera concluido em uma etapa posterior.

## Capacidades Implementadas

Hoje o projeto ja cobre:

- resposta via base de conhecimento
- consulta de ticket por ID
- criacao de ticket com coleta de dados faltantes
- validacao no backend
- tratamento de `400`, `404` e `422`
- testes automatizados do backend

## Estrutura Do Repositorio

- `backend/` - API FastAPI e testes
- `knowledge/` - arquivos-fonte da base de conhecimento
- `docs/` - documentacao complementar
- `artifacts/` - artefatos finais e runtime local

## Documentacao Complementar

- `docs/architecture-and-decisions.md` - decisoes de arquitetura, simplificacoes e limites do estado atual
- `docs/studio-export-guide.md` - passo a passo do checkpoint DSL e estado atual do Chatflow
- `docs/demo-script.md` - roteiro literal da demo e prompts de gravacao

## Artefatos Finais

Ainda faltam estes artefatos para a entrega final:

- export final do Chatflow
- video curto de demonstracao
- deploy final estavel do backend

## Estado Atual

Situacao atual do projeto:

- backend local funcional
- suite do backend verde
- base de conhecimento pronta
- Chatflow configurado e integrado em ambiente temporario
- seed principal da demo: `TKT-1001` com cenario de `VPN`
