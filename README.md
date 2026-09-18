# Gerador de Critérios de Aceite

Entrega da Semana 7 (Fase 10 · Adoção Guiada) do AI First Tracker —
"Desenvolver 1 feature utilizando SDD por time" — evoluída na Semana 8 com
"SDD + contexto de discovery por time" (ver `DISCOVERY.md`).

Recebe a descrição de um requisito funcional (texto livre ou arquivo `.txt`/`.md`) e
gera um documento Markdown com **user story**, **critérios de aceite em Gherkin** e
**casos de teste sugeridos** — pronto para colar na documentação do requisito ou virar
teste automatizado.

Feito seguindo **SDD (Specification-Driven Development)**: a especificação
(`SPEC.md`) foi escrita e validada antes de qualquer código; a implementação e os
testes seguem exatamente os requisitos e critérios de aceite descritos lá.

## Arquivos

| Arquivo | O que é |
|---|---|
| `DISCOVERY.md` | Discovery do time (v2): contexto, problema, stakeholders e decisão que levou aos requisitos RF08–RF10 |
| `SPEC.md` | Especificação (user story, requisitos, critérios de aceite em Gherkin, casos de teste) — escrita **antes** do código |
| `gerar_criterios.py` | CLI da feature |
| `test_gerar_criterios.py` | Testes automatizados, um por caso de teste do SPEC.md |
| `.env.example` | Modelo da variável de ambiente da chave de API |
| `requirements.txt` | Dependências |

## Instalação

```bash
pip install -r requirements.txt
cp .env.example .env
# edite o .env e coloque sua chave real da Anthropic em ANTHROPIC_API_KEY
export $(cat .env | xargs)   # ou use um gerenciador como direnv/python-dotenv
```

A chave **nunca** vai no código — só em variável de ambiente, conforme a regra de
segurança da DB1 (skill `devsec-db1`).

## Uso

```bash
# passando o requisito direto como texto
python3 gerar_criterios.py "Na tela de cadastro de cliente, o usuário só pode salvar depois de preencher nome e e-mail."

# passando um arquivo com o requisito
python3 gerar_criterios.py requisito.md -o criterios-cadastro-cliente.md
```

O resultado é salvo em `criterios-aceite.md` (ou no caminho passado em `-o`).

### Modo lote (v2)

Se o texto (ou arquivo) tiver vários requisitos, cada um começando com um
identificador `RF-XX` no início da linha, a ferramenta processa todos numa
única execução e gera um documento com uma tabela-resumo no topo:

```bash
python3 gerar_criterios.py backlog.md -o criterios-sprint-10.md
```

```text
RF-01: Permitir cadastro de cliente com nome e e-mail obrigatórios.

RF-02: Permitir edição do cadastro de cliente já existente.
```

Sem esse padrão no texto, o comportamento é o mesmo da v1 (um único requisito,
sem tabela-resumo).

## Rodando os testes

```bash
pytest test_gerar_criterios.py -v
```

Os testes não fazem chamada real à IA (não precisam de chave configurada) — eles
validam a montagem do prompt, a formatação da saída, a leitura de arquivo, o
tratamento de erro sem chave e a ausência de segredos no código-fonte.

## Publicar / linkar como artefato da entrega

Para preencher o campo **"Link do artefato"** da entrega no AI First Tracker, basta
subir esta pasta num repositório (ex.: GitHub) e usar a URL do repositório. Sugestão
de passos:

```bash
git init
git add .
git commit -m "Gerador de critérios de aceite (SDD) — entrega semana 7 AI First"
git remote add origin <url-do-seu-repo>
git push -u origin main
```

## Próximos passos (fora do escopo desta entrega)

- Interface web publicada em `apps.db1group.com` (ver skill `apps-db1`), se fizer
  sentido o time todo usar sem instalar nada localmente.
- Registrar as chamadas de IA no LangFuse para acompanhar custo e qualidade.
