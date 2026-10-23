#!/usr/bin/env python3
"""Extrai cabeçalho e um trecho de norma em Markdown do acervo ctresb/leis.

Não clona o repositório. Baixa um arquivo cru e imprime só o que foi pedido.
"""

import argparse
import re
import sys
import urllib.request

ARTIGO = re.compile(r"(?m)^\*{0,2}Art\.\s+(\d+)\s*[º°o\.]?\*{0,2}")
TITULO = re.compile(r"(?m)^(#{1,6})\s+(.+?)\s*$")
MAX_LINHAS = 400


def baixar(url):
    pedido = urllib.request.Request(url, headers={"User-Agent": "mcps-consulta-leis"})
    with urllib.request.urlopen(pedido, timeout=60) as resposta:
        return resposta.read().decode("utf-8", "replace")


def partir(texto):
    if texto.startswith("---\n"):
        fim = texto.find("\n---\n", 4)
        if fim != -1:
            meta = {}
            for linha in texto[4:fim].splitlines():
                if ":" not in linha:
                    continue
                chave, valor = linha.split(":", 1)
                meta[chave.strip()] = valor.strip().strip('"')
            return meta, texto[fim + 5 :]
    return {}, texto


def imprimir_meta(meta, corpo):
    if meta:
        for chave in (
            "titulo",
            "tipo",
            "numero",
            "data",
            "ementa",
            "situacao",
            "revogada",
            "versao_texto",
            "fonte",
            "urn",
        ):
            if chave in meta:
                print(f"{chave}: {meta[chave]}")
        return
    primeira = ""
    for linha in corpo.splitlines():
        if linha.startswith("# "):
            primeira = linha[2:].strip()
            break
    if primeira:
        print(f"titulo: {primeira}")
    print("cabecalho: sem YAML (documento único de topo, como a Constituição)")


def sem_titulo_final(trecho):
    linhas = trecho.strip().splitlines()
    while linhas and TITULO.match(linhas[-1]):
        linhas.pop()
    return "\n".join(linhas).strip()


def cortar(trecho):
    linhas = trecho.splitlines()
    if len(linhas) <= MAX_LINHAS:
        return trecho
    return "\n".join(linhas[:MAX_LINHAS]) + f"\n\n[cortado em {MAX_LINHAS} linhas; o artigo continua no arquivo]"


def artigo(corpo, numero):
    achados = list(ARTIGO.finditer(corpo))
    for indice, marca in enumerate(achados):
        if int(marca.group(1)) != numero:
            continue
        inicio = marca.start()
        fim = achados[indice + 1].start() if indice + 1 < len(achados) else len(corpo)
        return cortar(sem_titulo_final(corpo[inicio:fim]))
    return None


def faixa(corpo, inicio, fim):
    partes = []
    for numero in range(inicio, fim + 1):
        trecho = artigo(corpo, numero)
        if trecho:
            partes.append(trecho)
    return "\n\n".join(partes) if partes else None


def estrutura(corpo):
    linhas = []
    for marca in TITULO.finditer(corpo):
        linhas.append(f"{marca.group(1)} {marca.group(2)}")
        if len(linhas) == 80:
            linhas.append("[estrutura cortada em 80 títulos]")
            break
    return "\n".join(linhas)


def main():
    parser = argparse.ArgumentParser(description="Extrai um trecho de norma do acervo ctresb/leis")
    origem = parser.add_mutually_exclusive_group(required=True)
    origem.add_argument("--url", help="URL crua do .md (raw.githubusercontent.com)")
    origem.add_argument("--arquivo", help="Arquivo .md já baixado")
    parser.add_argument("--artigo", type=int, help="Número do artigo")
    parser.add_argument("--ate", type=int, help="Último artigo, inclusive, quando se quer uma faixa")
    args = parser.parse_args()

    texto = baixar(args.url) if args.url else open(args.arquivo, encoding="utf-8").read()
    meta, corpo = partir(texto)
    imprimir_meta(meta, corpo)
    print("---")

    if args.artigo is None:
        print(estrutura(corpo))
        return

    fim = args.ate if args.ate is not None else args.artigo
    if fim < args.artigo:
        print("faixa inválida: --ate é menor que --artigo", file=sys.stderr)
        sys.exit(2)

    trecho = artigo(corpo, args.artigo) if fim == args.artigo else faixa(corpo, args.artigo, fim)
    if not trecho:
        print(f"artigo {args.artigo} não aparece neste arquivo", file=sys.stderr)
        sys.exit(2)
    print(trecho)


if __name__ == "__main__":
    main()
