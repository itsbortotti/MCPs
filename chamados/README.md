# Chamados

Chamados reais ficam só na máquina; só `_template` vai pro git.

Cada ticket vive em `chamados/<NUMERO>-<slug-do-nome>/` (slug: minúsculas, sem acento, espaços → hífen).

Copie `chamados/_template/` ou deixe o `/drdestino` criar a pasta. Não use plano na raiz do MCPs.

Fluxo de artefatos (espírito Spec Kit; SDD próprio — personas Marvel):

`SPEC.md` → `PLANO-IMPLEMENTACAO.md` → `TASKS.md` → `sdd/handoff/*` → PR

## Engenharia

```
chamados/<NUMERO>-<slug>/
  SPEC.md                         # /drdestino — o quê / aceite
  PLANO-IMPLEMENTACAO.md          # /drdestino — como no repo (/ironman)
  TASKS.md                        # /drdestino — checklist ordenado (ids)
  sdd/handoff/
    entrega.md                    # /ironman
    revisao.md                    # /visao
    paridade.md                   # /falcao (se superfície dupla)
    prova.md                      # /viuvanegra
    duelo.md                      # /loki (opcional)
    recon.md                      # /shuri (opcional)
```

Stubs do `_template` já vêm com `Status: pendente` e seções vazias.

## Negócio

```
chamados/<NUMERO>-<slug>/
  PLANO-NEGOCIO.md                # /pepper
  negocio/handoff/
    discovery.md                  # /fury
    financeiro.md                 # /banner
    gtm.md                        # /hope
    painel.md                     # /ultron
```

## Gate (harness)

```bash
# só estrutura (SPEC + PLANO + TASKS)
./scripts/check-chamado-harness.sh chamados/<NUMERO>-<slug>

# prontidão de PR (prova ok; paridade se superfície dupla)
./scripts/check-chamado-harness.sh --before-pr chamados/<NUMERO>-<slug>

# smoke do harness
./scripts/eval-harness-smoke.sh
```

Maria Hill roda `--before-pr` antes de abrir a PR.

## Exemplo legado

`001-migrado-busca-estabelecimentos/` tem só o plano antigo. Chamados novos usam o `_template` completo (SPEC + PLANO + TASKS + stubs). Para reabrir esse exemplo na cadeia atual, rode `/drdestino` no mesmo ticket e regenere os três artefatos.

Engenharia e negócio podem coexistir no mesmo chamado. Contrato de leitura: `.cursor/rules/engenharia/handoff.mdc` e `.cursor/rules/negocio/handoff-negocio.mdc`.
