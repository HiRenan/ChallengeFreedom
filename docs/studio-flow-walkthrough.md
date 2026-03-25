# Studio Flow Walkthrough

## Objetivo

Este documento explica o Chatflow publicado no Dify Studio:

- qual e o papel de cada caminho do fluxo;
- o que cada no faz;
- quando o backend e chamado;
- quando a base de conhecimento e usada;
- como os erros sao tratados.

## Visao Geral

O Studio e a camada de orquestracao do assistente.

Ele nao e o sistema de registro dos tickets. O papel dele e:

- receber a mensagem do usuario;
- classificar a intencao;
- decidir se a pergunta vai para conhecimento ou para o backend;
- pedir informacoes faltantes antes de criar ticket;
- montar respostas finais curtas e consistentes.

O fluxo foi desenhado em quatro caminhos explicitos:

1. `knowledge`
2. `lookup_ticket`
3. `create_ticket`
4. `ambiguous`

## Caminho 1 - Knowledge

Esse caminho e usado quando o usuario faz perguntas documentais, como:

- requisitos para abrir ticket;
- duvidas de FAQ;
- politicas e procedimentos de suporte;
- fluxo geral de atendimento.

Sequencia:

1. `Question Classifier`
2. `Knowledge Retrieval`
3. `LLM 2`
4. `Answer 2`

Comportamento:

- o classificador identifica que a intencao e documental;
- o no de retrieval consulta a base `Base de Conhecimento de Suporte`;
- o `LLM 2` responde com base apenas no contexto recuperado;
- o `Answer 2` devolve a resposta final ao usuario.

## Caminho 2 - Lookup Ticket

Esse caminho e usado quando o usuario quer consultar um ticket existente.

Sequencia:

1. `Question Classifier`
2. `Lookup Extractor`
3. `IF/ELSE 2`
4. `Lookup Ticket Request`
5. tratamento por status ou por fail branch
6. `Lookup Summary Code`
7. `Answer 5`, `Answer 6`, `Answer 7`, `Answer 8`, `Answer 10` ou `Answer 11`

Comportamento:

- o `Lookup Extractor` extrai o `ticket_id`;
- o `IF/ELSE 2` impede chamada ao backend quando o ID estiver ausente;
- o `Lookup Ticket Request` chama `GET /tickets/{ticket_id}`;
- o fluxo diferencia:
  - sucesso `200`
  - `404` ticket nao encontrado
  - `400` ID invalido
  - falha tecnica
- o `Lookup Summary Code` transforma a resposta do backend em texto curto.

Exemplo de resposta de sucesso:

- `Ticket localizado: ID TKT-1001, status open, assunto VPN access blocked.`

## Caminho 3 - Create Ticket

Esse caminho e usado quando o usuario quer abrir um ticket.

Sequencia:

1. `Question Classifier`
2. `Create Extractor`
3. `IF/ELSE`
4. `Create Ticket Request`
5. tratamento de erro por fail branch
6. `Create Summary Code`
7. `Answer 9` ou `Answer 12`

Comportamento:

- o `Create Extractor` tenta extrair:
  - `requester_name`
  - `requester_email`
  - `subject`
  - `description`
- o `IF/ELSE` impede criacao quando algum campo estiver faltando;
- se faltar dado, o fluxo usa `Create Missing Fields Reply`;
- se os quatro campos estiverem presentes, o `Create Ticket Request` chama `POST /tickets`;
- o `Create Summary Code` monta a resposta curta de sucesso;
- o `IF/ELSE 5` trata erro `422`.

Exemplo de resposta de sucesso:

- `Ticket criado: ID TKT-1003, status open, assunto Impressora travada.`

## Caminho 4 - Ambiguous

Esse caminho e usado quando a mensagem nao indica claramente se o usuario quer:

- tirar uma duvida documental;
- consultar um ticket;
- abrir um ticket.

Sequencia:

1. `Question Classifier`
2. `Ambiguous Reply`

Resposta:

- o fluxo pede esclarecimento curto, sem tentar adivinhar a acao.

## Nos Do Canvas

### `User Input`

Ponto de entrada do fluxo.

Recebe:

- `sys.query`
- arquivos, se o app suportasse upload

No estado atual, o projeto usa apenas a pergunta textual.

### `Question Classifier`

Responsavel por separar a intencao em quatro classes:

- `knowledge`
- `lookup_ticket`
- `create_ticket`
- `ambiguous`

Esse no e critico porque impede que perguntas documentais virem chamadas de ticket por engano.

### `Knowledge Retrieval`

Consulta a base de conhecimento.

Uso:

- somente para perguntas documentais
- nao participa de nenhuma operacao transacional

### `LLM 2`

Transforma os trechos recuperados em resposta final.

Regras principais:

- responder em portugues do Brasil;
- usar apenas o contexto recuperado;
- nao inventar politicas, prazos ou status;
- manter resposta curta e operacional.

### `Lookup Extractor`

Extrai apenas o `ticket_id`.

Se o ID nao estiver claro, deixa em branco.

### `Create Extractor`

Extrai os quatro campos minimos de criacao:

- `requester_name`
- `requester_email`
- `subject`
- `description`

Se algum campo nao estiver claro, deixa em branco.

### `IF/ELSE 2`

Valida o caminho de consulta.

Regra:

- se existe `ticket_id`, segue para o backend;
- se nao existe, responde pedindo `TKT-1234`.

### `IF/ELSE`

Valida o caminho de criacao.

Regra:

- so chama o backend se os quatro campos estiverem presentes;
- caso contrario, pede os dados faltantes antes de qualquer criacao.

### `Lookup Ticket Request`

No `HTTP Request` para:

- `GET /tickets/{ticket_id}`

Hoje ele aponta para o backend publicado no Railway.

### `Create Ticket Request`

No `HTTP Request` para:

- `POST /tickets`

Ele envia os quatro campos minimos do ticket em JSON.

### `IF/ELSE 3`

Trata respostas normais do lookup por `status_code`.

Casos:

- `200`
- `404`
- `400`
- fallback tecnico

### `IF/ELSE 4`

Trata falhas do lookup pela `fail branch`.

Uso:

- quando o `HTTP Request` cai em erro e so existe `error_message`

### `IF/ELSE 5`

Trata falhas da criacao na `fail branch`.

Hoje o foco principal e:

- `422` para dados ausentes ou invalidos

### `Lookup Summary Code`

No de codigo usado para resumir a resposta de sucesso do lookup.

Entrada:

- `body` do `Lookup Ticket Request`

Saida:

- texto curto no formato final do assistente

### `Create Summary Code`

No de codigo usado para resumir a resposta de sucesso da criacao.

Entrada:

- `body` do `Create Ticket Request`

Saida:

- texto curto com ID, status e assunto

### `Answer Nodes`

Os nos `Answer` sao os pontos finais de resposta ao usuario.

Eles cobrem:

- resposta documental
- falta de `ticket_id`
- ticket nao encontrado
- ID invalido
- falha tecnica
- falta de campos minimos
- criacao bem-sucedida

## Como O Studio Se Conecta Ao Backend

O Studio chama diretamente o backend publicado em:

- `GET /tickets/{ticket_id}`
- `POST /tickets`

Essas chamadas sao feitas pelos nos `HTTP Request`.

O backend e o sistema de registro do ticket. O Studio nao persiste o ticket por conta propria.

## O Que O Studio Nao Faz

O Studio nao:

- armazena tickets como sistema principal;
- substitui o backend;
- valida sozinho as regras de criacao;
- decide regras de negocio sem apoio da API.

Ele melhora a experiencia, mas a camada final de validacao continua sendo o backend.

## Resumo

O Chatflow publicado foi desenhado para deixar o comportamento facil de revisar:

- conhecimento vai para a base documental;
- consulta e criacao vao para a API;
- mensagens ambiguas pedem esclarecimento;
- criacao sem dados minimos nao chama o backend;
- erros de lookup e criacao sao tratados com respostas curtas e previsiveis.
