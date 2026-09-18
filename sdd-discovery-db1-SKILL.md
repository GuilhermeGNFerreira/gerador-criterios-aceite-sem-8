---
name: sdd-discovery-db1
description: 'Use esta skill sempre que for desenvolver uma feature nova ou uma mudança não trivial em um projeto de cliente da DB1 — antes de escrever qualquer código. Ela conduz a etapa de discovery (entender o problema real e o contexto do time) e depois o SDD (Specification-Driven Development — especificar e validar antes de implementar), já adaptado às convenções da casa: IDs de requisito no formato RF-XX, a regra de "docx primeiro" para validação com cliente, e compatibilidade com o agente RF-to-UML. Acione em pedidos como "preciso desenvolver uma feature nova", "vamos especificar isso antes de codar", "documentar esse requisito pro cliente", "montar a spec dessa funcionalidade", ou sempre que alguém começar a tocar em uma funcionalidade nova de um projeto de cliente. NÃO force o processo completo em quickshot, correção de bug simples ou ajuste pontual — a seção "Quando pular" explica como decidir isso.'
---

# SDD + Discovery — adaptado ao time

Esta skill existe porque, na prática dos projetos de cliente (MP Radar, PM Portal e
outros), boa parte do retrabalho não vem de bug de código — vem de especificar em
cima de um entendimento errado do problema. Discovery e SDD, nessa ordem, resolvem
isso: primeiro entender de verdade o que está sendo pedido e por quê, depois
especificar e só então codar.

## Quando pular

Nem toda tarefa merece o processo completo. Não force discovery + spec formal em:

- Quickshots e provas de conceito descartáveis.
- Correções de bug com causa e comportamento esperado já claros.
- Ajustes pontuais que não mudam comportamento observável (refactor, texto, estilo).

Use o processo completo quando a feature tem impacto real em um cliente ou no time
— múltiplos stakeholders, comportamento novo, ou algo que vai virar requisito
documentado no backlog. Na dúvida, um discovery de 10 minutos é mais barato que uma
spec errada.

## Passo 1 — Discovery

Antes de especificar, responda (ou pergunte ao usuário, se você é Claude conduzindo
isso):

1. **Time e contexto**: quem vai usar essa feature, e em qual fluxo de trabalho ela
   entra? (Ex.: time de documentação de requisitos, time de dev de um app cliente.)
2. **Problema real**: o que hoje é feito manualmente, de forma inconsistente, ou não
   é feito? Evite pular direto para "a solução é X" sem nomear o problema.
3. **Stakeholders**: quem depende do resultado, e o que cada um precisa dele? (Ex.:
   analista que escreve o requisito, dev que implementa, cliente que valida, outra
   ferramenta/agente que consome a saída.)
4. **Restrições que já existem**: convenções do time, regras de segurança
   (`devsec-db1`), formatos que outra ferramenta downstream espera.

Registre isso em um `DISCOVERY.md` curto — não precisa ser longo, precisa ser
específico o suficiente para alguém de fora entender por que a feature existe.

## Passo 2 — Spec (SDD)

Com o discovery em mãos, escreva a especificação **antes de qualquer código**, num
`SPEC.md`:

- User story ("Como / Quero / Para que").
- Requisitos funcionais numerados (RF01, RF02, ...) — se a feature nasce de um
  requisito de backlog, **preserve o ID original no formato `RF-XX`** em vez de
  renumerar; é esse ID que o agente RF-to-UML usa para conectar o requisito ao
  diagrama gerado depois.
- Critérios de aceite em Gherkin (`Feature` / `Scenario` / `Given` / `When` /
  `Then`) — são o que vira teste automatizado no passo 5.
- Casos de teste (happy path + pelo menos um caso de borda/erro).
- Fora de escopo, explícito — evita que a spec cresça por conta própria.

## Passo 3 — Validar antes de codar

Este é o ponto que separa SDD de "documentar depois". Mostre a spec para quem pediu
a feature (ou para o time) e confirme escopo e decisões **antes** de implementar.
Se a feature vai gerar um documento formal para o cliente, siga a regra de "docx
primeiro" (o `.md`/rascunho serve para validação interna; o `.docx` é o que vai para
o cliente, e só depois disso o `.md` final é gerado, exceto quando for uma peça que
só formaliza algo já validado em outro lugar).

## Passo 4 — Implementar com segurança

Sem exceção, siga a skill `devsec-db1` ao escrever o código: nada de segredo
chumbado (chave de API, senha, string de conexão — sempre variável de ambiente),
sem `shell=True`/`eval`/`exec` sobre entrada externa, dado que vem de fora nunca
vira comando ou query montada por concatenação. Se a feature for um portal, app ou
API, a skill `devsec-db1` também cobre SSO, checagem de dono por requisição e
rate limit.

## Passo 5 — Testes ligados à spec

Escreva um teste automatizado por critério de aceite/caso de teste do `SPEC.md` —
não testes genéricos "por cobertura", mas testes que, lendo o nome, mostram qual
critério da spec estão validando. Isso faz da spec um contrato vivo: se o
comportamento muda, o teste (ou a spec) precisa mudar junto, nunca os dois
silenciosamente divergirem.

## Checklist rápido (para colar num PR ou numa entrega)

- [ ] Discovery documentado (time, problema real, stakeholders, restrições)
- [ ] Spec escrita e validada com quem pediu, antes do código
- [ ] IDs de requisito (`RF-XX`) preservados do backlog até a spec
- [ ] Código sem segredo chumbado, seguindo `devsec-db1`
- [ ] Um teste automatizado por critério de aceite da spec
- [ ] Fora de escopo explícito na spec, para não crescer sem controle
