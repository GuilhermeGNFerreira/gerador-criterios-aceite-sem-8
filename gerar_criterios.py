#!/usr/bin/env python3
"""
Gerador de Critérios de Aceite
==============================

Recebe a descrição de um requisito funcional (texto direto ou arquivo .txt/.md)
e gera um documento Markdown com:
  - User Story
  - Critérios de Aceite em Gherkin
  - Casos de Teste sugeridos

A chave de acesso à API é sempre lida da variável de ambiente ANTHROPIC_API_KEY —
nunca fica escrita neste arquivo. Veja SPEC.md para a especificação completa e
README.md para instruções de uso.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

PADRAO_ID_RF = re.compile(r"^(RF-\d+)\b[:\-]?\s*", flags=re.MULTILINE)


class ErroConfiguracao(Exception):
    """Erro de configuração do ambiente (ex.: chave de API ausente)."""


def ler_requisito(fonte: str) -> str:
    """Lê o requisito funcional a partir de um arquivo, se `fonte` for um
    caminho existente; caso contrário, trata `fonte` como o próprio texto."""
    caminho = Path(fonte)
    if caminho.is_file():
        return caminho.read_text(encoding="utf-8")
    return fonte


def dividir_requisitos(texto: str) -> list[dict]:
    """Divide o texto de entrada em um ou mais requisitos.

    Se o texto contiver um ou mais blocos que começam com um identificador
    "RF-XX" (formato usado no backlog do time — descoberto no discovery da
    Semana 8), cada bloco vira um requisito separado, com o ID preservado.
    Caso contrário, o texto inteiro é tratado como um único requisito sem ID
    (comportamento idêntico ao da v1 — RF10).
    """
    texto = texto.strip()
    marcadores = list(PADRAO_ID_RF.finditer(texto))

    if not marcadores:
        return [{"id": None, "texto": texto}]

    requisitos = []
    for indice, marcador in enumerate(marcadores):
        inicio_corpo = marcador.end()
        fim_bloco = marcadores[indice + 1].start() if indice + 1 < len(marcadores) else len(texto)
        corpo = texto[inicio_corpo:fim_bloco].strip()
        rf_id = marcador.group(1)
        requisitos.append({"id": rf_id, "texto": corpo})
    return requisitos


def montar_prompt(requisito: str) -> str:
    """Monta o prompt enviado à IA, pedindo explicitamente as três seções
    exigidas pela spec (User Story, Critérios de Aceite, Casos de Teste)."""
    return f"""Você é um analista de requisitos experiente.

Dado o requisito funcional abaixo, gere uma resposta em Markdown com exatamente
estas três seções, nesta ordem:

## User Story
(formato "Como <papel>, quero <ação>, para que <benefício>")

## Critérios de Aceite (Gherkin)
(um ou mais blocos ```gherkin``` com Feature/Scenario/Given/When/Then)

## Casos de Teste
(lista numerada com pelo menos um caminho feliz e um caso de borda/erro)

Requisito funcional:
\"\"\"
{requisito.strip()}
\"\"\"
"""


def obter_api_key() -> str:
    """Lê a chave de API da variável de ambiente. Nunca aceita a chave como
    argumento de linha de comando ou valor no código (regra de segurança)."""
    chave = os.environ.get("ANTHROPIC_API_KEY")
    if not chave:
        raise ErroConfiguracao(
            "ANTHROPIC_API_KEY não está definida. Configure a variável de "
            "ambiente antes de rodar a ferramenta (veja .env.example / "
            "README.md). Nenhuma chamada de rede foi feita."
        )
    return chave


def chamar_ia(prompt: str, api_key: str, modelo: str = "claude-sonnet-4-5") -> str:
    """Chama a API da Anthropic e devolve o texto da resposta."""
    import anthropic  # import local: só é necessário quando de fato chamamos a IA

    cliente = anthropic.Anthropic(api_key=api_key)
    resposta = cliente.messages.create(
        model=modelo,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    return resposta.content[0].text


def formatar_saida(resposta_ia: str, requisito: str) -> str:
    """Monta o documento Markdown final, com o requisito original no topo."""
    cabecalho = (
        "# Especificação gerada — Gerador de Critérios de Aceite\n\n"
        "**Requisito de entrada:**\n\n"
        f"> {requisito.strip()}\n\n"
        "---\n\n"
    )
    return cabecalho + resposta_ia.strip() + "\n"


def formatar_documento(resultados: list[dict]) -> str:
    """Monta o documento final a partir de 1..N requisitos já processados pela IA.

    `resultados`: lista de {"id": str | None, "requisito": str, "resposta_ia": str}.

    Com um único requisito sem ID, o formato é idêntico ao da v1 (RF10). Com dois
    ou mais requisitos (ou um requisito com ID RF-XX), o documento ganha uma
    tabela-resumo no topo e uma seção por requisito, com o ID preservado (RF09).
    """
    if len(resultados) == 1 and resultados[0]["id"] is None:
        return formatar_saida(resultados[0]["resposta_ia"], resultados[0]["requisito"])

    linhas_resumo = ["| Requisito | Resumo |", "|---|---|"]
    secoes = []
    for resultado in resultados:
        rotulo = resultado["id"] or "Requisito único"
        primeira_linha = resultado["requisito"].strip().splitlines()[0][:80]
        linhas_resumo.append(f"| {rotulo} | {primeira_linha} |")

        secoes.append(
            f"## {rotulo}\n\n"
            "**Requisito de entrada:**\n\n"
            f"> {resultado['requisito'].strip()}\n\n"
            f"{resultado['resposta_ia'].strip()}"
        )

    cabecalho = (
        "# Especificação gerada — Gerador de Critérios de Aceite\n\n"
        f"Processados **{len(resultados)}** requisitos nesta rodada.\n\n"
        + "\n".join(linhas_resumo)
        + "\n\n---\n\n"
    )
    return cabecalho + "\n\n---\n\n".join(secoes) + "\n"


def gerar(requisito_fonte: str, saida: str | None = None) -> str:
    """Orquestra o fluxo completo: ler -> dividir -> montar prompt -> chamar IA
    (para cada requisito) -> formatar -> salvar."""
    texto = ler_requisito(requisito_fonte)
    requisitos = dividir_requisitos(texto)

    # a chave é validada uma única vez, antes de qualquer chamada de rede —
    # nenhum requisito do lote é processado se ela estiver ausente
    api_key = obter_api_key()

    resultados = []
    for requisito in requisitos:
        prompt = montar_prompt(requisito["texto"])
        resposta = chamar_ia(prompt, api_key)
        resultados.append(
            {"id": requisito["id"], "requisito": requisito["texto"], "resposta_ia": resposta}
        )

    documento = formatar_documento(resultados)

    caminho_saida = Path(saida) if saida else Path("criterios-aceite.md")
    caminho_saida.write_text(documento, encoding="utf-8")
    return str(caminho_saida)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Gera user story + critérios de aceite (Gherkin) + casos de "
        "teste a partir de um requisito funcional."
    )
    parser.add_argument(
        "requisito",
        help="Texto do requisito funcional, ou caminho para um arquivo .txt/.md",
    )
    parser.add_argument(
        "-o",
        "--saida",
        help="Caminho do arquivo Markdown de saída (padrão: criterios-aceite.md)",
        default=None,
    )
    args = parser.parse_args(argv)

    try:
        caminho = gerar(args.requisito, args.saida)
    except ErroConfiguracao as erro:
        print(f"Erro de configuração: {erro}", file=sys.stderr)
        return 1
    except Exception as erro:  # noqa: BLE001 - CLI: erro amigável, sem stack trace bruto
        print(f"Não foi possível gerar o documento: {erro}", file=sys.stderr)
        return 1

    print(f"Documento gerado em: {caminho}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
