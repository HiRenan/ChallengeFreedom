# Studio Export Guide

## Estado Atual Do Chatflow

- o canvas do Chatflow esta completo
- nao ha nos desconectados visiveis
- o draft esta salvo com status `Auto-Saved`
- o app ja foi publicado
- os nos `HTTP Request` apontam para a URL final do Railway

Resumo do comportamento atual:

- perguntas documentais seguem para `Knowledge Retrieval`
- lookup exige `ticket_id`
- criacao exige `requester_name`, `requester_email`, `subject` e `description`
- entradas ambiguas caem em esclarecimento
- lookup e create ja retornam respostas finais curtas
- o export final do Studio ja existe em `artifacts/studio/assistente-de-suporte-final.dsl.yml`

## Arquivos Do Studio

- checkpoint intermediario:
  - `artifacts/studio/assistente-de-suporte-checkpoint.dsl.yml`
- export final publicado:
  - `artifacts/studio/assistente-de-suporte-final.dsl.yml`

## Como Exportar O DSL

Use uma destas duas entradas da interface:

1. na pagina do app no Studio, abrir o menu de acoes do app e clicar em `Export DSL`
2. na tela de orquestracao, usar a opcao `Export DSL` disponivel no menu do app

Passo a passo:

1. abrir o app `Assistente de Suporte`
2. confirmar que o topo mostra `Auto-Saved`
3. abrir a acao `Export DSL`
4. se houver pergunta sobre variaveis secretas, nao incluir segredos no arquivo exportado
5. salvar o arquivo com o nome adequado ao momento:
   - `assistente-de-suporte-checkpoint.dsl.yml` para snapshot intermediario
   - `assistente-de-suporte-final.dsl.yml` para a versao final publicada
6. mover ou salvar o arquivo em `artifacts/studio/`
7. confirmar com `git status --short` que o arquivo apareceu como novo

## O Que O Export Leva

Pelas docs do Dify, o export leva:

- configuracao do app
- metadata do app
- orquestracao do workflow e configuracao dos nos
- parametros de modelo e prompts
- conexoes com bases de conhecimento

O export nao leva:

- conteudo real da base de conhecimento
- credenciais de terceiros
- logs de uso

## Verificacoes Antes Do Fechamento Final

Antes de considerar o export final pronto:

- confirmar que o export saiu da versao mais recente publicada
- confirmar que os nos `HTTP Request` apontam para a URL final do backend
- manter o checkpoint anterior apenas como referencia
- tratar o arquivo final como o artefato principal do Studio para a submissao
