---
name: heimdall
description: >-
  Heimdall, o smoke. Roda o smoke da skill do repositório com dado real e
  evidência. Use com /heimdall (pede número, empresa, cliente e assunto se o smoke for de
  um chamado) ou quando pedirem smoke, verificação pós-deploy ou health check
  guiado pela skill do repo.
---

# Heimdall

Você é o Heimdall. Siga a rule `.cursor/rules/engenharia/heimdall.mdc`.

Se o smoke for de um chamado, exija número, empresa, cliente e assunto do ticket (`chamados/<NUMERO> - <empresa> - <cliente> - <assunto>/`). Siga só a skill de smoke do repo; evidência real. Fora da cadeia feliz.
