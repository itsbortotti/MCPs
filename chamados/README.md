# Chamados

Cada ticket vive em `chamados/<NUMERO>-<slug-do-nome>/` (slug: minúsculas, sem acento, espaços → hífen).

Copie `chamados/_template/` ou crie a pasta e os stubs abaixo. Não use plano na raiz do MCPs.

## Engenharia

```
chamados/<NUMERO>-<slug>/
  PLANO-IMPLEMENTACAO.md          # /drdestino
  sdd/handoff/
    entrega.md                    # /ironman
    revisao.md                    # /visao
    paridade.md                   # /falcao (se superfície dupla)
    prova.md                      # /viuvanegra
    duelo.md                      # /loki (opcional)
    recon.md                      # /shuri (opcional)
```

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

Engenharia e negócio podem coexistir no mesmo chamado. Contrato de leitura: `.cursor/rules/engenharia/handoff.mdc` e `.cursor/rules/negocio/handoff-negocio.mdc`.
