# Status e Fluxo de Atendimento

Este documento resume o fluxo básico de atendimento usado neste projeto.

## Como o fluxo funciona

O assistente separa dois tipos de interação:

- perguntas documentais, respondidas pela base de conhecimento
- ações de suporte, como consultar ou abrir ticket

## Fluxo para consulta de ticket

Para consultar um ticket, é necessário informar o ID completo no formato `TKT-<número>`.

Se o formato estiver incorreto, o assistente informará o padrão esperado.

Se o formato estiver correto, mas o ticket não existir, o retorno será de ticket não encontrado.

## Fluxo para abertura de ticket

Ao pedir a abertura de um ticket, o assistente verifica se existem dados mínimos suficientes.

Se faltar alguma informação, ele faz perguntas de follow-up antes de criar o ticket.

## Status inicial do ticket

Neste projeto, tickets novos são registrados com status `open`.

Esse status indica que a solicitação foi aberta e está disponível para acompanhamento.

## O que esperar da resposta

As respostas do assistente devem ser curtas, claras e operacionais.

O objetivo é orientar rapidamente o próximo passo, sem explicações longas.

## Boa prática de uso

Se a sua dúvida puder ser resolvida com documentação, consulte a base antes de abrir um ticket.
