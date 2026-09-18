# Ideia de Funcionalidade com IA Embarcada — MP Radar

**Entrega:** AI First Tracker · Fase 12 (Escala, Consolidação e Geração de Valor
para Clientes) · Semana 12 — Ideação e Levantamento
**Cliente:** Minhas Proteções · **Produto:** MP Radar

## Pergunta de partida

"O que a IA consegue resolver para o meu cliente?" — não uso interno do time, e
sim algo que o usuário final do MP Radar sente diretamente.

## Problema hoje

No fluxo atual, depois que o PGR (Programa de Gerenciamento de Riscos) e as
Pesquisas Psicossociais são preenchidos, é o Especialista quem cruza manualmente
os riscos identificados com os resultados da pesquisa para montar o **Plano de
Ação** — decidir o que priorizar, redigir cada ação, prazo e responsável. É
trabalho manual, repetitivo entre empresas parecidas, e o tempo do Especialista
(recurso mais caro e mais escasso do serviço) vai para redação em vez de para
julgamento técnico.

## Ideia: Plano de Ação assistido por IA, embarcado no módulo

Embarcar uma IA **dentro do módulo Plano de Ação** do MP Radar (não um chat à
parte) que:

1. Lê os riscos já cadastrados no PGR/AEP e os resultados da Pesquisa
   Psicossocial daquela empresa.
2. Gera um **rascunho** de Plano de Ação: itens priorizados por risco/gravidade,
   com sugestão de ação, prazo e responsável — no mesmo formato que o
   Especialista já usa hoje.
3. O Especialista revisa, edita e aprova o rascunho — a IA nunca publica nada
   sozinha; ela elimina a página em branco, não a decisão técnica.

Isso reaproveita exatamente o mecanismo já validado no Gerador de Critérios de
Aceite (entrada estruturada → IA → documento estruturado e revisável, com
critério humano no fim do processo) — só que embarcado no produto do cliente
em vez de ser uma ferramenta interna do time.

## Valor para o cliente

- Especialista gasta tempo revisando/ajustando prioridades, não escrevendo do
  zero — plano de ação sai mais rápido depois que PGR + pesquisa são
  concluídos.
- Padronização: planos de ação de empresas com perfis de risco parecidos ficam
  mais consistentes entre si.
- Abre espaço para o Especialista atender mais empresas no mesmo tempo (ganho
  de escala, tema central da Fase 12).

## Riscos / pontos de atenção

- Nenhum dado sensível do trabalhador (saúde, resultado individual da pesquisa
  psicossocial) pode ir para fora do ambiente controlado — só dados já
  agregados/anonimizados no prompt, seguindo a regra de dado sigiloso da
  `devsec-db1`.
- IA sugere, Especialista aprova — sem isso, o risco de responsabilidade técnica
  fica mal distribuído.
- Precisa de amostra real de Planos de Ação já aprovados para validar se o
  formato gerado bate com o que o Especialista espera.

## Próximos passos (fora do escopo desta semana)

- Validar a ideia com quem toca o MP Radar hoje (e, se possível, com um
  Especialista real) antes de virar discovery formal.
- Se aprovada, tratar como uma feature nova normal: discovery → spec (SDD) →
  implementação segura → testes — mesmo processo da skill `sdd-discovery-db1`
  já entregue nas semanas anteriores.
