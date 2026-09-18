"""Testes automatizados — rastreiam diretamente os casos de teste do SPEC.md
(seção 6). Rodar com: pytest test_gerar_criterios.py -v
"""

import re
from pathlib import Path

import pytest

import gerar_criterios as gc


REQUISITO_EXEMPLO = (
    "Na tela de cadastro de cliente, o usuário deve poder salvar o cadastro "
    "somente depois de preencher nome e e-mail."
)


# 1. test_monta_prompt_inclui_requisito
def test_monta_prompt_inclui_requisito():
    prompt = gc.montar_prompt(REQUISITO_EXEMPLO)
    assert REQUISITO_EXEMPLO in prompt
    # o prompt precisa pedir explicitamente as três seções da spec
    assert "User Story" in prompt
    assert "Critérios de Aceite" in prompt
    assert "Casos de Teste" in prompt


# 2. test_formata_saida_com_secoes_esperadas
def test_formata_saida_com_secoes_esperadas():
    resposta_ia_simulada = (
        "## User Story\n"
        "Como usuário, quero salvar o cadastro, para que meus dados fiquem registrados.\n\n"
        "## Critérios de Aceite (Gherkin)\n"
        "```gherkin\n"
        "Feature: Cadastro de cliente\n"
        "  Scenario: Salvar com campos obrigatórios preenchidos\n"
        "    Given que preenchi nome e e-mail\n"
        "    When eu salvo o cadastro\n"
        "    Then o cadastro é salvo com sucesso\n"
        "```\n\n"
        "## Casos de Teste\n"
        "1. Salvar com nome e e-mail preenchidos (happy path)\n"
        "2. Tentar salvar sem e-mail (caso de borda)\n"
    )

    documento = gc.formatar_saida(resposta_ia_simulada, REQUISITO_EXEMPLO)

    assert "## User Story" in documento
    assert "## Critérios de Aceite" in documento
    assert "## Casos de Teste" in documento
    assert REQUISITO_EXEMPLO in documento


# 3. test_erro_sem_api_key
def test_erro_sem_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(gc.ErroConfiguracao):
        gc.obter_api_key()


# 4. test_le_entrada_de_arquivo
def test_le_entrada_de_arquivo(tmp_path: Path):
    arquivo = tmp_path / "requisito.md"
    arquivo.write_text(REQUISITO_EXEMPLO, encoding="utf-8")

    conteudo = gc.ler_requisito(str(arquivo))

    assert conteudo == REQUISITO_EXEMPLO


def test_le_entrada_como_texto_direto():
    # quando a "fonte" não é um arquivo existente, é tratada como texto puro
    conteudo = gc.ler_requisito(REQUISITO_EXEMPLO)
    assert conteudo == REQUISITO_EXEMPLO


# 5. test_sem_segredo_no_codigo
def test_sem_segredo_no_codigo():
    codigo_fonte = Path(__file__).with_name("gerar_criterios.py").read_text(encoding="utf-8")
    padroes_de_segredo = [
        r"sk-ant-[A-Za-z0-9\-_]+",
        r"sk-[A-Za-z0-9]{20,}",
        r"api_key\s*=\s*[\"'][^\"']+[\"']",
    ]
    for padrao in padroes_de_segredo:
        assert re.search(padrao, codigo_fonte) is None, f"Padrão suspeito encontrado: {padrao}"

    # a única forma permitida de obter a chave é via variável de ambiente
    assert "os.environ.get(\"ANTHROPIC_API_KEY\")" in codigo_fonte


# --- Novos testes v2 (Semana 8 — discovery: requisitos chegam em lote, com ID RF-XX) ---


# 6. test_divide_requisito_unico_sem_id
def test_divide_requisito_unico_sem_id():
    resultado = gc.dividir_requisitos(REQUISITO_EXEMPLO)
    assert resultado == [{"id": None, "texto": REQUISITO_EXEMPLO}]


# 7. test_divide_multiplos_requisitos_por_id
def test_divide_multiplos_requisitos_por_id():
    texto = (
        "RF-01: Permitir cadastro de cliente com nome e e-mail obrigatórios.\n\n"
        "RF-02: Permitir edição do cadastro de cliente já existente."
    )

    resultado = gc.dividir_requisitos(texto)

    assert len(resultado) == 2
    assert resultado[0]["id"] == "RF-01"
    assert "cadastro de cliente com nome e e-mail" in resultado[0]["texto"]
    assert resultado[1]["id"] == "RF-02"
    assert "edição do cadastro" in resultado[1]["texto"]


# 8. test_formata_documento_unico_mantem_formato_anterior
def test_formata_documento_unico_mantem_formato_anterior():
    resposta_ia_simulada = "## User Story\nConteúdo qualquer.\n"

    documento_v2 = gc.formatar_documento(
        [{"id": None, "requisito": REQUISITO_EXEMPLO, "resposta_ia": resposta_ia_simulada}]
    )
    documento_v1 = gc.formatar_saida(resposta_ia_simulada, REQUISITO_EXEMPLO)

    assert documento_v2 == documento_v1
    assert "| Requisito | Resumo |" not in documento_v2  # tabela-resumo não deve aparecer


# 9. test_formata_documento_lote_inclui_resumo_e_ids
def test_formata_documento_lote_inclui_resumo_e_ids():
    resultados = [
        {"id": "RF-01", "requisito": "Cadastro de cliente.", "resposta_ia": "## User Story\nA\n"},
        {"id": "RF-02", "requisito": "Edição de cadastro.", "resposta_ia": "## User Story\nB\n"},
    ]

    documento = gc.formatar_documento(resultados)

    assert "| Requisito | Resumo |" in documento
    assert "RF-01" in documento
    assert "RF-02" in documento
    assert "## RF-01" in documento
    assert "## RF-02" in documento
