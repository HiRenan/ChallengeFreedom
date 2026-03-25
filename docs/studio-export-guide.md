# Studio Export Guide

## Estado Atual Do Chatflow

- o canvas do Chatflow esta completo
- nao ha nos desconectados visiveis
- o draft esta salvo com status `Auto-Saved`
- o app segue `Unpublished`
- os nos `HTTP Request` ainda apontam para a URL temporaria do `trycloudflare`

Resumo do comportamento atual do draft:

- perguntas documentais seguem para `Knowledge Retrieval`
- lookup exige `ticket_id`
- criacao exige `requester_name`, `requester_email`, `subject` e `description`
- entradas ambiguas caem em esclarecimento
- lookup e create ja retornam respostas finais curtas

## Checkpoint Do Studio

O objetivo deste checkpoint e salvar o estado atual do fluxo antes do deploy estavel da versao final.

Arquivo recomendado:

- `artifacts/studio/assistente-de-suporte-checkpoint.dsl.yml`

Arquivo final depois do deploy estavel:

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
5. salvar o arquivo com o nome `assistente-de-suporte-checkpoint.dsl.yml`
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

Antes de considerar o checkpoint pronto:

- confirmar que o export saiu do draft mais recente
- manter um print ou nota do status `Unpublished`, porque ainda nao existe versao publicada
- nao tratar esse DSL como artefato final da submissao
- repetir o export depois do deploy estavel e do publish final
