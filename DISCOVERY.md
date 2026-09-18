# Discovery — Gerador de Critérios de Aceite (v2)

**Entrega:** AI First Tracker · Fase 10 (Adoção Guiada) · Semana 8
**Objetivo desta etapa:** antes de tocar em código, entender o contexto real de uso
da feature entregue na Semana 7, para decidir o que evoluir. Esse discovery é o
insumo que alimenta o `SPEC.md` atualizado.

## 1. Time e contexto

- Time: analistas/devs que produzem documentação de requisitos para clientes
  (ex.: fluxo usado no projeto MP Radar), hoje escrevendo critérios de aceite à
  mão a partir do backlog.
- A entrada real de trabalho **não chega um requisito de cada vez** — chega como
  um **lote de RFs do backlog**, cada um já identificado com um código
  (`RF-01`, `RF-02`, ...), no mesmo padrão usado depois pelo agente que converte
  requisitos em diagramas UML.
- O fluxo de documentação já segue uma regra de time: o documento formal
  (docx) só é gerado depois de uma etapa de rascunho/validação — a saída em
  Markdown desta ferramenta é exatamente esse rascunho.

## 2. Problema observado (o que a v1 não resolvia)

A v1 (Semana 7) só aceitava **um requisito por execução**. Na prática, isso
significa rodar a ferramenta manualmente RF por RF quando o insumo real é um
backlog inteiro — o mesmo problema manual que a ferramenta deveria eliminar,
só que em escala menor.

## 3. Stakeholders consultados (discovery)

| Papel | O que precisa |
|---|---|
| Analista de requisitos | Colar o backlog inteiro de uma vez e sair com um único documento revisável, não um arquivo por RF |
| Dev que vai puxar caso de teste | Cada critério de aceite precisa manter o ID do RF (`RF-01`) para rastrear de volta ao backlog |
| Quem usa o RF-to-UML depois | O ID do requisito não pode se perder no meio do processo — é a chave que conecta as duas ferramentas |

## 4. Restrições que continuam valendo

- Chave de API só por variável de ambiente (nenhuma mudança aqui).
- Nenhum dado sigiloso de cliente deve ir para o prompt — o discovery não
  identificou necessidade de mudar isso.

## 5. Decisão tomada a partir do discovery

Evoluir a feature para aceitar **um ou vários requisitos na mesma execução**,
identificados por um prefixo `RF-XX` no início da linha:

- Se a entrada tiver um ou mais blocos `RF-XX`, a ferramenta trata cada bloco
  como um requisito separado, gera a spec de cada um e devolve **um único
  documento** com um resumo no topo (tabela com todos os RFs processados) e
  uma seção por RF, preservando o ID.
- Se a entrada não tiver esse padrão (uso simples, como na v1), o
  comportamento anterior é mantido exatamente igual — ninguém que já usa a
  ferramenta hoje quebra.

Essa decisão está refletida nos novos requisitos funcionais do `SPEC.md`
(RF08–RF10) e nos testes novos em `test_gerar_criterios.py`.
