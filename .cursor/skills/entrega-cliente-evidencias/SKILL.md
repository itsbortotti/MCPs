---
name: entrega-cliente-evidencias
description: >-
  Roteiro do /uatu: testar o chamado num ambiente (local|dev|hml|prd) e montar
  o PDF de entrega com evidências para o cliente. Use quando a persona Uatu
  estiver ativa ou quando pedirem documento de entrega com screenshots.
---

# Entrega ao cliente com evidências

## Quando usar

Depois de implementar (e, se aplicável, publicar) um chamado: provar no **ambiente indicado** e gerar PDF + PNGs para envio ao cliente.

Persona: `/uatu` (rule `engenharia/uatu.mdc`).

## Pré-requisitos

- Pasta do chamado com `SPEC.md` (critérios).
- Ambiente explícito: `local` | `dev` | `hml` | `prd`.
- Stack acessível (health OK). Credenciais: seed local da doc do repo, ou fornecidas pelo utilizador (nunca inventar).
- `playwright-cli` no PATH.
- Helper: `scripts/montar-pdf-entrega-cliente.py` (raiz do MCPs).

## Passos

1. Ler `SPEC.md` (+ `PLANO-IMPLEMENTACAO.md`; opcional `prova.md` / `DOC-APROVACAO.md`).
2. Confirmar URL do ambiente (skill/docs do repo de produto ou pedido).
3. Criar `evidencia/entrega-<ambiente>/`.
4. Para cada critério com UI: `playwright-cli` → ações → PNG com nome estável (`a1-…`, `a2-…`).
5. Escrever `evidencia/entrega-<ambiente>/manifest.json` (ver schema abaixo).
6. Gerar PDF:

```bash
python3 scripts/montar-pdf-entrega-cliente.py \
  --chamado "chamados/<NUMERO> - <empresa> - <cliente> - <assunto>" \
  --ambiente <local|dev|hml|prd> \
  --manifest evidencia/entrega-<ambiente>/manifest.json
```

Schema de exemplo:

```bash
python3 scripts/montar-pdf-entrega-cliente.py --schema
```

7. Gravar `sdd/handoff/documento.md` (`Status: ok` só se os must do SPEC passaram no ambiente).
8. `python3 scripts/custo-passada.py <pasta> --persona uatu --modelo <id> --fez "…"`.

## Manifesto (campos úteis)

| Campo | Uso |
| --- | --- |
| `titulo`, `subtitulo`, `cliente`, `produto`, `chamado`, `ambiente`, `url_base` | Capa |
| `entregas[]` | Tabela id / título / status |
| `resumo_intro`, `contexto[]`, `nao_mudou[]` | Texto inicial |
| `secoes[]` | `titulo`, `pedido`, `como_ficou`, `evidencia_nota`, `figura`, `legenda` |
| `resumo_cliente[]`, `referencias[]`, `rodape` | Fecho |

`figura` é o **nome do ficheiro** dentro da mesma pasta do `manifest.json`.

## Saídas

- `evidencia/entrega-<ambiente>/*.png` + `manifest.json`
- `<Assunto>-Entrega-<AMBIENTE>.pdf` na raiz do chamado
- `sdd/handoff/documento.md`

## Não fazer

- Escolher ambiente sozinho.
- Colocar senhas no PDF ou no manifesto.
- Substituir `/viuvanegra` ou fazer deploy.
