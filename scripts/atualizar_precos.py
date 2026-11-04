"""Atualiza chamados/_precos-ia.json na primeira passada do dia.

Uma tentativa por dia. Se a página não entregar o preço, o valor anterior fica
e o aviso explica. Não inventa número novo.
"""

from __future__ import annotations

import json
import re
import urllib.request
from datetime import date

from precos_ia import ARQUIVO, FONTES, estado

PAGINAS = {
    "claude": "https://platform.claude.com/docs/en/about-claude/pricing",
    "openai": "https://developers.openai.com/api/docs/pricing",
    "xai": "https://docs.x.ai/developers/pricing",
    "gemini": "https://ai.google.dev/gemini-api/docs/pricing",
}


def baixar(url):
    pedido = urllib.request.Request(
        url,
        headers={
            "User-Agent": "GarageFlow-custos/1.0",
            "Accept": "text/markdown, text/plain;q=0.9, text/html;q=0.5",
        },
    )
    with urllib.request.urlopen(pedido, timeout=25) as resposta:
        return resposta.read().decode("utf-8", errors="replace")


def colunas(linha):
    return [parte.strip() for parte in linha.strip().strip("|").split("|")]


def dolar(texto):
    achado = re.search(r"\$([0-9]+(?:\.[0-9]+)?)", texto or "")
    return achado.group(1) if achado else None


def linha_que_comeca(texto, prefixo):
    for linha in texto.splitlines():
        if not linha.startswith("|"):
            continue
        nome = colunas(linha)[0]
        if nome.startswith(prefixo):
            return colunas(linha)
    return None


def aplicar_claude(texto, modelos):
    mapa = {
        "claude-opus-5.5": "Claude Opus 5.5",
        "claude-sonnet-5.5": "Claude Sonnet 5.5",
    }
    achou = []
    for ident, prefixo in mapa.items():
        cols = linha_que_comeca(texto, prefixo)
        if not cols or len(cols) < 6:
            continue
        entrada, saida = dolar(cols[1]), dolar(cols[-1])
        if entrada and saida:
            _por_id(modelos, ident, entrada, saida)
            achou.append(ident)
    curta = linha_que_comeca(texto, "Claude Haiku 5.5 (for prompts up to")
    longa = linha_que_comeca(texto, "Claude Haiku 5.5 (for prompts over")
    if curta and longa and len(curta) >= 6 and len(longa) >= 6:
        entrada, saida = dolar(curta[1]), dolar(curta[-1])
        entrada_longa, saida_longa = dolar(longa[1]), dolar(longa[-1])
        if all((entrada, saida, entrada_longa, saida_longa)):
            item = _por_id(modelos, "claude-haiku-5.5", entrada, saida)
            item["entrada_longa"] = entrada_longa
            item["saida_longa"] = saida_longa
            item["limiar"] = 100_000
            achou.append("claude-haiku-5.5")
    return achou


def aplicar_openai(texto, modelos):
    for linha in texto.splitlines():
        if "gpt-5.4 (<272K" not in linha or not linha.startswith("|"):
            continue
        cols = colunas(linha)
        if len(cols) < 8:
            return []
        entrada, saida = dolar(cols[1]), dolar(cols[2])
        entrada_longa, saida_longa = dolar(cols[6]), dolar(cols[7])
        if not all((entrada, saida, entrada_longa, saida_longa)):
            return []
        item = _por_id(modelos, "gpt-5.4", entrada, saida)
        item["entrada_longa"] = entrada_longa
        item["saida_longa"] = saida_longa
        item["limiar"] = 272_000
        return ["gpt-5.4"]
    return []


def aplicar_xai(texto, modelos):
    curta = linha_que_comeca(texto, "grok-4.7 (<")
    longa = linha_que_comeca(texto, "grok-4.7 (≥")
    if not curta or not longa or len(curta) < 5 or len(longa) < 5:
        return []
    entrada, saida = dolar(curta[2]), dolar(curta[4])
    entrada_longa, saida_longa = dolar(longa[2]), dolar(longa[4])
    if not all((entrada, saida, entrada_longa, saida_longa)):
        return []
    item = _por_id(modelos, "grok-4.7", entrada, saida)
    item["entrada_longa"] = entrada_longa
    item["saida_longa"] = saida_longa
    item["limiar"] = 200_000
    return ["grok-4.7"]


def secao(texto, titulo):
    inicio = texto.find(titulo)
    if inicio < 0:
        return ""
    fim = texto.find("\n## ", inicio + len(titulo))
    return texto[inicio:] if fim < 0 else texto[inicio:fim]


def preco_vigente(trecho, marcador, hoje):
    inicio = trecho.find(marcador)
    if inicio < 0:
        return None
    janela = trecho[inicio : inicio + 500]
    vigente = None
    for valor, dia in re.findall(r"\$([0-9]+(?:\.[0-9]+)?) through ([A-Za-z]+ \d+, \d{4})", janela):
        limite = date_texto(dia)
        if limite and hoje <= limite:
            vigente = valor
    for valor, dia in re.findall(r"\$([0-9]+(?:\.[0-9]+)?) starting ([A-Za-z]+ \d+, \d{4})", janela):
        limite = date_texto(dia)
        if limite and hoje >= limite:
            vigente = valor
    if vigente:
        return vigente
    achado = re.search(r"\$([0-9]+(?:\.[0-9]+)?)", janela)
    return achado.group(1) if achado else None


def date_texto(texto):
    from datetime import datetime

    try:
        return datetime.strptime(texto, "%B %d, %Y").date()
    except ValueError:
        return None


def aplicar_gemini(texto, modelos):
    from datetime import date

    hoje = date.today()
    achou = []
    pares = (
        ("gemini-4-argon", "## Gemini 4 Argon"),
        ("gemini-3.8-flash", "## Gemini 3.8 Flash"),
    )
    for ident, titulo in pares:
        bloco = secao(texto, titulo)
        entrada = preco_vigente(bloco, "Input price", hoje)
        saida = preco_vigente(bloco, "Output price", hoje)
        if entrada and saida:
            _por_id(modelos, ident, entrada, saida)
            achou.append(ident)
    return achou


def _por_id(modelos, ident, entrada, saida):
    for item in modelos:
        if item["id"] == ident:
            item["entrada"] = entrada
            item["saida"] = saida
            return item
    raise KeyError(ident)


def garantir():
    hoje = date.today().isoformat()
    atual = estado()
    if atual.get("consultado") == hoje or atual.get("tentativa") == hoje:
        return atual
    atual["tentativa"] = hoje
    atual["fontes"] = FONTES
    _salvar(atual)

    textos = {}
    erros = []
    for nome, url in PAGINAS.items():
        try:
            textos[nome] = baixar(url)
        except Exception as erro:
            erros.append(f"{nome}: {erro.__class__.__name__}")

    modelos = atual.get("modelos") or []
    achados = []
    if "claude" in textos:
        achados += aplicar_claude(textos["claude"], modelos)
    if "openai" in textos:
        achados += aplicar_openai(textos["openai"], modelos)
    if "xai" in textos:
        achados += aplicar_xai(textos["xai"], modelos)
    if "gemini" in textos:
        achados += aplicar_gemini(textos["gemini"], modelos)

    if achados:
        atual["consultado"] = hoje
        atual["modelos"] = modelos
        faltou = erros
        atual["aviso"] = (
            "Atualizado: " + ", ".join(achados) + (". Falhou: " + "; ".join(faltou) if faltou else ".")
        )
    else:
        atual["aviso"] = "A tabela do dia não mudou. " + "; ".join(erros)
    _salvar(atual)
    return atual


def _salvar(atual):
    ARQUIVO.parent.mkdir(parents=True, exist_ok=True)
    ARQUIVO.write_text(json.dumps(atual, indent=2) + "\n", encoding="utf-8")
