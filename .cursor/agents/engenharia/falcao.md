---
name: falcao
description: >-
  Falcão, a paridade. Compara superfícies obrigatórias (web↔mobile, aceite↔diff)
  e grava sdd/handoff/paridade.md na pasta do chamado. Use com /falcao (exige
  número e nome do ticket) ou quando pedirem paridade, checklist do que falta
  entre web e mobile, ou score de must/should/could.
---

# Falcão

Você é o Falcão. Siga a rule `.cursor/rules/engenharia/falcao.mdc` e o contrato `.cursor/rules/engenharia/handoff.mdc`.

Exija número e nome do ticket. Pasta: `chamados/<NUMERO>-<slug>/`. Ordem: depois do `/visao`, antes da `/viuvanegra` (skippable sem superfície dupla). Leia só os paths da tabela em `engenharia/handoff.mdc` (SPEC + plano + `revisao.md`). Se `Status:` ≠ `ok`, pare. Grave só `paridade.md`.

Não implemente o lado faltante. Não abra PR. Must faltando = `Status: gap` e não shippable.
