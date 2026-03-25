# Demo Script

## Setup Antes De Gravar

Para o ensaio atual:

- abrir o app `Assistente de Suporte` no `Preview`
- garantir que o backend esteja respondendo
- usar `Restart` entre cenarios independentes
- manter o mesmo roteiro e os mesmos prompts da gravacao oficial

Para a gravacao oficial:

- repetir este roteiro ja com a URL final estavel
- exportar o DSL final depois do publish definitivo

## Ordem Da Demo

1. abertura curta
2. pergunta documental
3. lookup de ticket existente
4. tentativa de criacao sem dados minimos
5. criacao com dados completos
6. lookup de ticket inexistente

## Prompts Exatos

### 1. Pergunta documental

```text
Quais dados preciso informar para abrir um ticket?
```

### 2. Lookup existente

```text
Quero consultar o ticket TKT-1001
```

### 3. Criacao incompleta

```text
Quero abrir um ticket
```

### 4. Criacao completa

```text
Nome: Renan. Email: renan@example.com. Assunto: Impressora travada. Descricao: A impressora nao imprime desde ontem.
```

### 5. Lookup inexistente

```text
Quero consultar o ticket TKT-9999
```

## Roteiro Literal

### Abertura

```text
Este projeto entrega um assistente de suporte corporativo com tres responsabilidades bem separadas. Perguntas documentais vao para a base de conhecimento, acoes de ticket vao para um backend FastAPI, e o Chatflow no Dify faz a orquestracao entre esses caminhos. Agora eu vou demonstrar os fluxos principais.
```

### Pergunta documental

```text
Primeiro, eu vou fazer uma pergunta de conhecimento. Aqui a ideia e mostrar que o assistente responde usando a base de conhecimento, sem transformar tudo em acao transacional.
```

Digite o prompt da secao `1. Pergunta documental`.

```text
Nesse caso, o fluxo classificou a intencao como pergunta documental, consultou a knowledge base e respondeu de forma direta.
```

### Lookup de ticket existente

```text
Agora eu vou consultar um ticket existente pelo ID. Esse fluxo vai para o backend e retorna uma resposta curta com o identificador, o status e o assunto.
```

Digite o prompt da secao `2. Lookup existente`.

```text
Aqui o assistente encontrou o ticket TKT-1001 e devolveu um resumo objetivo do registro.
```

### Criacao incompleta

```text
Agora eu vou tentar abrir um ticket sem enviar os dados minimos. O comportamento esperado e nao criar nada e pedir exatamente as informacoes que faltam.
```

Digite o prompt da secao `3. Criacao incompleta`.

```text
O assistente nao chamou o backend para criar o ticket. Primeiro ele pediu nome, email, assunto e descricao do problema.
```

### Criacao completa

```text
Na mesma conversa, eu envio agora os dados completos em uma unica mensagem para concluir a abertura do ticket.
```

Digite o prompt da secao `4. Criacao completa`.

```text
Com os dados minimos completos, o backend cria o ticket e o fluxo retorna o novo ID com status e assunto.
```

### Lookup inexistente

```text
Por fim, eu vou consultar um ticket que nao existe para mostrar o tratamento de erro.
```

Digite o prompt da secao `5. Lookup inexistente`.

```text
Nesse caso, o backend retorna ticket nao encontrado e o assistente responde com uma mensagem curta e clara.
```

### Fechamento

```text
Com isso, o projeto cobre os comportamentos principais do assistente: resposta por conhecimento, consulta por ID, follow-up para criacao incompleta, criacao bem-sucedida e tratamento de erro para ticket inexistente.
```

## Checklist Rapido Da Gravacao

- usar `Restart` antes do passo documental
- usar `Restart` antes do lookup existente
- manter criacao incompleta e criacao completa na mesma conversa
- usar `Restart` antes do lookup inexistente
- evitar abrir menus ou editar nos durante a demo
