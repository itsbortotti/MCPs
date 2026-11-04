# Custos

Nenhuma passada ainda.

Cada passada registra o que fez, a IA, os tokens e o custo. O consolidado fica no fim do arquivo.

```bash
python3 scripts/custo-passada.py <pasta-do-chamado> --persona /ironman --modelo grok-4.7 --fez "o que esta passada fez" --entrada 100000 --saida 20000
```

A primeira passada do dia atualiza `chamados/_precos-ia.md`. Sem a contagem, omita `--entrada` e `--saida`.
