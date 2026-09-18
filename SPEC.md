# SPEC — Gerador de Critérios de Aceite

**Entrega:** AI First Tracker · Fase 10 (Adoção Guiada) · Semana 7 (v1) e Semana 8 (v2)
**Metodologia:** SDD (Specification-Driven Development) — a especificação abaixo é
escrita e validada **antes** de qualquer linha de código de implementação.

> **v2 (Semana 8):** os requisitos RF08–RF10 foram adicionados depois do discovery
> documentado em `DISCOVERY.md` — leia-o primeiro para entender o "porquê" das
> mudanças abaixo.

## 1. Contexto e problema

No dia a dia de levantamento de requisitos (ex.: MP Radar, PM Portal), o requisito
funcional costuma chegar em texto livre (print de tela, frase do cliente, item de
backlog). Transformar isso em user story + critérios de aceite testáveis é manual e
inconsistente entre pessoas/times.

## 2. User story

> Como analista/dev que documenta requisitos,
> quero colar a descrição livre de um requisito funcional e receber uma user story
> formatada com critérios de aceite em Gherkin e uma lista de casos de teste,
> para que a especificação saia pronta para revisão e para virar teste automatizado.

## 3. Requisitos funcionais (RF)

- **RF01** — A ferramenta recebe um requisito funcional em texto livre (arquivo `.txt`/`.md`
  ou texto via linha de comando).
- **RF02** — A ferramenta gera uma **user story** no formato "Como / Quero / Para que".
- **RF03** — A ferramenta gera de 1 a N **cenários de aceite em Gherkin**
  (`Feature` / `Scenario` / `Given` / `When` / `Then`).
- **RF04** — A ferramenta gera uma lista de **casos de teste sugeridos** (happy path +
  pelo menos um caso de borda/erro).
- **RF05** — A saída é salva como um arquivo Markdown (`.md`), pronta para anexar à
  documentação do requisito.
- **RF06** — A chave de acesso à API de IA é lida de variável de ambiente
  (`ANTHROPIC_API_KEY`); nunca fica no código.
- **RF07** — Se a chamada à IA falhar (sem chave, sem rede, erro da API), a ferramenta
  informa o erro de forma clara, sem vazar segredo ou stack trace bruto.

## 3.1 Requisitos funcionais novos (v2 — a partir do discovery)

- **RF08** — Se a entrada contiver um ou mais blocos identificados por um prefixo
  `RF-XX` no início da linha (ex.: `RF-01`, `RF-02`), a ferramenta trata cada bloco
  como um requisito independente.
- **RF09** — Quando houver mais de um requisito, a saída é **um único documento**
  Markdown contendo: uma tabela-resumo no topo (RF + resumo de uma linha) e, na
  sequência, uma seção por RF, cada uma com o ID preservado no título.
- **RF10** — Quando a entrada não tiver nenhum bloco `RF-XX` (uso simples), o
  comportamento da v1 é mantido sem nenhuma diferença perceptível — a evolução é
  aditiva, não substitui o caso de uso original.

## 4. Fora de escopo (explícito)

- Interface gráfica/web (fica para uma iteração futura, se fizer sentido publicar em
  `apps.db1group.com`).
- Integração direta com VSTS/Mandala ou qualquer sistema de tracking.
- Tradução automática de idioma do requisito.

## 5. Critérios de aceite (Gherkin)

```gherkin
Feature: Gerar critérios de aceite a partir de um requisito funcional

  Scenario: Gerar a partir de texto direto
    Given um requisito funcional descrito em texto livre
    When eu executo a ferramenta passando esse texto
    Then recebo uma user story no formato "Como/Quero/Para que"
    And recebo pelo menos um cenário em Gherkin (Given/When/Then)
    And recebo pelo menos dois casos de teste sugeridos (um happy path e um de borda)

  Scenario: Gerar a partir de um arquivo
    Given um arquivo .txt ou .md contendo um requisito funcional
    When eu executo a ferramenta apontando para esse arquivo
    Then o conteúdo do arquivo é usado como entrada
    And o resultado é salvo em um novo arquivo .md

  Scenario: Chave de API ausente
    Given a variável de ambiente ANTHROPIC_API_KEY não está definida
    When eu executo a ferramenta
    Then recebo uma mensagem de erro clara explicando como configurar a chave
    And nenhuma chamada de rede é tentada

  Scenario: Nenhum segredo no código-fonte
    Given o código-fonte da ferramenta
    When eu procuro por chaves de API ou credenciais chumbadas
    Then não encontro nenhuma — apenas leitura de variável de ambiente

  Scenario: Lote de requisitos identificados por RF-XX
    Given um texto contendo vários blocos que começam com "RF-01", "RF-02" etc.
    When eu executo a ferramenta passando esse texto
    Then recebo um único documento Markdown
    And o documento tem uma tabela-resumo listando cada RF processado
    And cada RF aparece em sua própria seção, com o ID preservado no título

  Scenario: Requisito único continua funcionando como na v1
    Given um texto sem nenhum prefixo "RF-XX"
    When eu executo a ferramenta passando esse texto
    Then o documento gerado é idêntico ao formato da v1 (sem tabela-resumo)
```

## 6. Casos de teste (para a suíte automatizada)

1. `test_monta_prompt_inclui_requisito` — o prompt enviado à IA contém o texto do
   requisito de entrada.
2. `test_formata_saida_com_secoes_esperadas` — a saída formatada contém as seções
   "User Story", "Critérios de Aceite" e "Casos de Teste".
3. `test_erro_sem_api_key` — sem `ANTHROPIC_API_KEY`, a função levanta um erro
   tratado com mensagem orientando a configuração, sem chamar a rede.
4. `test_le_entrada_de_arquivo` — dado um arquivo `.md` de entrada, o conteúdo lido
   é o mesmo do arquivo.
5. `test_sem_segredo_no_codigo` — varredura simples no arquivo-fonte não encontra
   padrões de chave (`sk-`, `Bearer `, etc.) fora de comentários/exemplos.
6. `test_divide_requisito_unico_sem_id` — texto sem prefixo `RF-XX` volta como um
   único requisito sem ID.
7. `test_divide_multiplos_requisitos_por_id` — texto com `RF-01`/`RF-02` é dividido
   corretamente em dois requisitos, cada um com seu ID e texto.
8. `test_formata_documento_unico_mantem_formato_anterior` — documento de um único
   requisito sem ID é idêntico ao formato da v1 (sem tabela-resumo).
9. `test_formata_documento_lote_inclui_resumo_e_ids` — documento com múltiplos RFs
   inclui a tabela-resumo e o ID de cada RF em sua seção.

## 7. Requisitos não funcionais

- Código em Python 3, dependência mínima (`anthropic` + biblioteca padrão).
- Sem `shell=True`, sem `eval`/`exec` sobre a entrada do usuário.
- Sem dado sigiloso (CPF, e-mail real, etc.) em exemplos ou logs.

## 8. Artefato final esperado

- `DISCOVERY.md` — contexto de discovery do time (v2).
- `gerar_criterios.py` — CLI.
- `test_gerar_criterios.py` — testes automatizados.
- `README.md` — como instalar, configurar a chave e usar.
- `.env.example` — placeholder da variável de ambiente.
- Este `SPEC.md`.
