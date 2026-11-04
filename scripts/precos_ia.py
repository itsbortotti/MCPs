"""Preço de lista da API, USD por 1 milhão de tokens.

Contexto curto, sem cache, sem batch.
A tabela viva fica em chamados/_precos-ia.json e é lida a cada consulta.
Quando `limiar` existe e a entrada passa dele, a requisição inteira usa a faixa longa.
"""

import json
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ARQUIVO = RAIZ / "chamados" / "_precos-ia.json"

FONTES = [
    "https://platform.claude.com/docs/en/about-claude/pricing",
    "https://developers.openai.com/api/docs/pricing",
    "https://docs.x.ai/developers/pricing",
    "https://ai.google.dev/gemini-api/docs/pricing",
]

# id, nome, entrada, saída, limiar ou None, entrada longa, saída longa, nota
PRECOS = [
    ("claude-opus-5.5", "Claude Opus 5.5", "4", "20", None, None, None, ""),
    ("claude-sonnet-5.5", "Claude Sonnet 5.5", "2", "10", None, None, None, ""),
    (
        "claude-haiku-5.5",
        "Claude Haiku 5.5",
        "0.10",
        "0.50",
        100_000,
        "0.50",
        "2.50",
        "Acima de 100k de entrada, a requisição inteira usa a faixa maior.",
    ),
    (
        "gpt-5.4",
        "GPT-5.4",
        "2.50",
        "15",
        272_000,
        "5",
        "22.50",
        "Faixa longa acima de 272k de entrada.",
    ),
    (
        "grok-4.7",
        "Grok 4.7",
        "2",
        "6",
        200_000,
        "4",
        "12",
        "Faixa longa a partir de 200k de entrada. No Cursor, a variante Fast cobra outro múltiplo, fora desta tabela.",
    ),
    (
        "gemini-4-argon",
        "Gemini 4 Argon",
        "2",
        "10",
        None,
        None,
        None,
        "Preço introdutório até 30 nov 2026. A partir de 1 dez 2026 a lista passa a $4 / $20.",
    ),
    (
        "gemini-3.8-flash",
        "Gemini 3.8 Flash",
        "0.75",
        "3.75",
        None,
        None,
        None,
        "Preço introdutório até 31 dez 2026. A partir de 1 jan 2027 a lista passa a $1.50 / $7.50.",
    ),
]


def semente():
    linhas = []
    for item in PRECOS:
        ident, nome, entrada, saida, limiar, entrada_longa, saida_longa, nota = item
        linhas.append(
            {
                "id": ident,
                "nome": nome,
                "entrada": entrada,
                "saida": saida,
                "limiar": limiar,
                "entrada_longa": entrada_longa,
                "saida_longa": saida_longa,
                "nota": nota,
            }
        )
    return linhas


def estado():
    if ARQUIVO.exists():
        return json.loads(ARQUIVO.read_text(encoding="utf-8"))
    return {
        "consultado": None,
        "tentativa": None,
        "aviso": "",
        "fontes": FONTES,
        "modelos": semente(),
    }


def tabela():
    linhas = []
    for item in estado().get("modelos", semente()):
        linhas.append(
            {
                "id": item["id"],
                "nome": item["nome"],
                "entrada": Decimal(item["entrada"]),
                "saida": Decimal(item["saida"]),
                "limiar": item.get("limiar"),
                "entrada_longa": Decimal(item["entrada_longa"]) if item.get("entrada_longa") else None,
                "saida_longa": Decimal(item["saida_longa"]) if item.get("saida_longa") else None,
                "nota": item.get("nota") or "",
            }
        )
    return linhas


def achar(modelo):
    for linha in tabela():
        if linha["id"] == modelo:
            return linha
    return None


def custo(modelo, entrada, saida):
    linha = achar(modelo)
    if linha is None or entrada is None or saida is None:
        return None
    pin, pout = linha["entrada"], linha["saida"]
    if linha["limiar"] is not None and entrada > linha["limiar"]:
        pin, pout = linha["entrada_longa"], linha["saida_longa"]
    return (Decimal(entrada) / Decimal(1_000_000)) * pin + (
        Decimal(saida) / Decimal(1_000_000)
    ) * pout
