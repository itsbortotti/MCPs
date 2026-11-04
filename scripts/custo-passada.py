#!/usr/bin/env python3
"""Registra uma passada de chamado e reescreve custos.md.

Na primeira passada do dia, atualiza a tabela de preços antes de gravar.

Uso:
  python3 scripts/custo-passada.py --referencia
  python3 scripts/custo-passada.py <pasta> --persona /ironman --modelo grok-4.7 --fez "implementou T1"
  python3 scripts/custo-passada.py <pasta> --persona /ironman --modelo grok-4.7 --fez "implementou T1" --entrada 100000 --saida 20000

Sem --entrada e --saida a passada entra com contagem n/d. Não estime token.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from atualizar_precos import garantir  # noqa: E402
from precos_ia import FONTES, achar, custo, estado, tabela  # noqa: E402

CENARIOS = [
    ("120k entrada", 120_000, 0),
    ("120k saída", 0, 120_000),
    ("100k entrada + 20k saída", 100_000, 20_000),
]


def dinheiro(valor):
    if valor is None:
        return "n/d"
    quantizado = valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"${quantizado}"


def resolver(alvo):
    caminho = Path(alvo)
    if caminho.is_dir():
        return caminho.resolve()
    for candidato in (ROOT / alvo, ROOT / "chamados" / alvo):
        if candidato.is_dir():
            return candidato.resolve()
    sys.exit(f"pasta do chamado não encontrada: {alvo}")


def carregar(pasta):
    arquivo = pasta / "custos.json"
    if not arquivo.exists():
        return []
    return json.loads(arquivo.read_text(encoding="utf-8")).get("passadas", [])


def gravar_json(pasta, passadas):
    (pasta / "custos.json").write_text(
        json.dumps({"passadas": passadas}, indent=2) + "\n",
        encoding="utf-8",
    )


def linha_preco(modelo, entrada, saida):
    return dinheiro(custo(modelo, entrada, saida))


def bloco_comparativo(titulo, entrada, saida):
    linhas = [f"### {titulo}", ""]
    if entrada is None or saida is None:
        linhas.append("Sem contagem de token nesta passada. O comparativo de 120k está em `chamados/_precos-ia.md`.")
        linhas.append("")
        return linhas
    linhas.append(f"Volume: {entrada} entrada + {saida} saída.")
    linhas.append("")
    linhas.append("| IA | Custo |")
    linhas.append("| --- | --- |")
    for linha in tabela():
        linhas.append(f"| {linha['nome']} | {linha_preco(linha['id'], entrada, saida)} |")
    linhas.append("")
    return linhas


def nome_modelo(ident):
    if not ident:
        return "n/d"
    linha = achar(ident)
    return linha["nome"] if linha else ident


def tokens_texto(entrada, saida):
    if entrada is None or saida is None:
        return "n/d"
    return f"{entrada} entrada + {saida} saída ({entrada + saida} no total)"


def render_md(passadas):
    atual = estado()
    consultado = atual.get("consultado") or "ainda não"
    linhas = [
        "# Custos",
        "",
        f"Preço de lista da API em USD, contexto curto, sem cache. Tabela consultada em {consultado}.",
        "O plano do Cursor pode cobrar outro valor. Sem contagem informada, token e custo ficam `n/d`.",
        "",
        "## Passadas",
        "",
    ]
    if not passadas:
        linhas.append("Nenhuma passada ainda.")
        linhas.append("")
    for indice, item in enumerate(passadas, start=1):
        entrada = item.get("entrada")
        saida = item.get("saida")
        linhas.extend(
            [
                f"### {indice} — {item.get('data', '')} — {item.get('persona', '')}",
                "",
                f"- O que fez: {item.get('fez') or 'n/d'}",
                f"- IA: {nome_modelo(item.get('modelo'))}",
                f"- Tokens: {tokens_texto(entrada, saida)}",
                f"- Custo: {linha_preco(item.get('modelo'), entrada, saida)}",
                "",
            ]
        )

    linhas.extend(["## Consolidado do chamado", ""])
    linhas.append(f"- Passadas: {len(passadas)}")
    contadas = [p for p in passadas if p.get("entrada") is not None and p.get("saida") is not None]
    if not contadas:
        linhas.append("- Tokens: n/d")
        linhas.append("- Custo: n/d")
        linhas.append(f"- Passadas sem contagem: {len(passadas)}")
        linhas.append("")
    else:
        total_e = sum(p["entrada"] for p in contadas)
        total_s = sum(p["saida"] for p in contadas)
        custos = []
        for item in contadas:
            valor = custo(item.get("modelo"), item["entrada"], item["saida"])
            if valor is not None:
                custos.append(valor)
        soma = sum(custos, Decimal(0)) if custos else None
        linhas.append(f"- Tokens: {tokens_texto(total_e, total_s)}")
        linhas.append(f"- Custo das IAs usadas: {dinheiro(soma)}")
        linhas.append(f"- Passadas sem contagem: {len(passadas) - len(contadas)}")
        linhas.append("")
        linhas.extend(bloco_comparativo("O mesmo volume em cada IA", total_e, total_s))
    linhas.append("Tabela de 120k e preços do dia: `chamados/_precos-ia.md`.")
    linhas.append("")
    return "\n".join(linhas)


def render_referencia():
    atual = estado()
    consultado = atual.get("consultado") or "ainda não"
    aviso = atual.get("aviso") or ""
    linhas = [
        "# Preços de lista — IA",
        "",
        f"Consultado em {consultado}. USD por 1 milhão de tokens. Contexto curto, sem cache e sem batch.",
        "A primeira passada de cada dia tenta atualizar esta tabela nas fontes oficiais.",
        "Isto não é a fatura do Cursor.",
        "",
    ]
    if aviso:
        linhas.extend([aviso, ""])
    linhas.extend(
        [
            "## Por milhão de tokens",
            "",
            "| IA | Entrada | Saída | Nota |",
            "| --- | --- | --- | --- |",
        ]
    )
    for linha in tabela():
        nota = linha["nota"] or "—"
        linhas.append(
            f"| {linha['nome']} | ${linha['entrada']} | ${linha['saida']} | {nota} |"
        )
    linhas.extend(["", "## 120 mil tokens", ""])
    linhas.append("O mesmo volume em cada IA. Entrada e saída têm preço diferente, então 120k não é um número só.")
    linhas.append("")
    cabecalho = "| IA | " + " | ".join(nome for nome, _, _ in CENARIOS) + " |"
    linhas.append(cabecalho)
    linhas.append("| --- | " + " | ".join("---" for _ in CENARIOS) + " |")
    for linha in tabela():
        celulas = [
            linha_preco(linha["id"], entrada, saida) for _, entrada, saida in CENARIOS
        ]
        linhas.append(f"| {linha['nome']} | " + " | ".join(celulas) + " |")
    linhas.extend(["", "## Fontes", ""])
    for url in FONTES:
        linhas.append(f"- {url}")
    linhas.append("")
    return "\n".join(linhas)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pasta", nargs="?")
    parser.add_argument("--referencia", action="store_true")
    parser.add_argument("--persona")
    parser.add_argument("--modelo")
    parser.add_argument("--fez")
    parser.add_argument("--data")
    parser.add_argument("--entrada", type=int)
    parser.add_argument("--saida", type=int)
    args = parser.parse_args()

    garantir()

    if args.referencia:
        destino = ROOT / "chamados" / "_precos-ia.md"
        destino.write_text(render_referencia(), encoding="utf-8")
        print(destino)
        return

    if not args.pasta or not args.persona or not args.fez:
        parser.error("informe a pasta, --persona e --fez, ou use --referencia")
    if (args.entrada is None) ^ (args.saida is None):
        parser.error("--entrada e --saida vêm juntos")
    if args.entrada is not None and (args.entrada < 0 or args.saida < 0):
        parser.error("token negativo não entra")
    if args.data and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.data):
        parser.error("--data no formato AAAA-MM-DD")

    pasta = resolver(args.pasta)
    passadas = carregar(pasta)
    passadas.append(
        {
            "data": args.data or date.today().isoformat(),
            "persona": args.persona,
            "modelo": args.modelo,
            "fez": args.fez,
            "entrada": args.entrada,
            "saida": args.saida,
        }
    )
    gravar_json(pasta, passadas)
    (pasta / "custos.md").write_text(render_md(passadas), encoding="utf-8")
    print(pasta / "custos.md")


if __name__ == "__main__":
    main()
