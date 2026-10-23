# MCPs

Configuração do Cursor para desenvolver com **Spec-Driven Design próprio** (personas Marvel + `chamados/`): os servidores MCP ficam neste repositório, e cada persona sabe o que fazer quando o comando dela é chamado. Harness = guides + tools + sensors + gates + artefatos (ver seção abaixo).

**[Como usar](MANUAL.md)** — playbook: cole no chat, confira o disco, próximo comando (simulações negócio→dev e task pequena).

São duas partes.

**Servidores.** O `mcp.json` é a lista do que o Cursor pode consultar (Azure, Azure DevOps, Jira, Postman, GitHub e o restante). O `scripts/apply-to-cursor.sh` copia essa lista para `~/.cursor/mcp.json`, troca cada `${VAR}` pelo valor do `.env` e não mexe em servidor de plugin que só exista no Cursor. Segredo não entra no git: copie `.env.example` para `.env` e preencha. O `.env` está no `.gitignore`.

**Personas.** Os arquivos em `.cursor/rules/` dizem como a IA trabalha. O `sdd-personas.mdc` fica na raiz de `.cursor/rules/` com `alwaysApply: true` e é o índice das duas cadeias (engenharia e negócio). O procedimento de cada personagem entra quando o comando dele é usado.

Abra esta pasta no workspace do Cursor para as personas valerem. Numa janela só com outro repositório, a cadeia não entra.

## Layout das pastas

Cursor carrega rules em subpastas de `.cursor/rules/` (documentação oficial). O índice que vale o tempo todo fica na raiz; o resto é por domínio.

```
.cursor/
  rules/
    sdd-personas.mdc          # alwaysApply — índice Engenharia | Negócio
    engenharia/               # cadeia SDD + facilitadores técnicos
      handoff.mdc             # contrato SDD engenharia
      jarvis.mdc
      drdestino.mdc …
    negocio/                  # mini-cadeia de produto/negócio
      handoff-negocio.mdc
      fury.mdc
      pepper.mdc …
  agents/
    engenharia/               # ver inventário de agents abaixo
    negocio/                  # fury, pepper, banner, hope, ultron
```

### Agents Cursor (existem neste repo)

| Pasta | Agents |
| --- | --- |
| `.cursor/agents/engenharia/` | `drdestino`, `ironman`, `visao`, `falcao`, `viuvanegra`, `mariahill`, `capitao`, `jarvis`, `formiga`, `heimdall`, `wong`, `demolidor`, `loki`, `shuri` |
| `.cursor/agents/negocio/` | `fury`, `pepper`, `banner`, `hope`, `ultron` |

Cada agent aponta para a rule correspondente; o procedimento completo fica em `.cursor/rules/`.

| Domínio | Rules | Agents | Artefatos no chamado |
| --- | --- | --- | --- |
| Engenharia | `.cursor/rules/engenharia/` | `.cursor/agents/engenharia/` | `SPEC.md`, `PLANO-IMPLEMENTACAO.md`, `TASKS.md`, `sdd/handoff/` |
| Negócio | `.cursor/rules/negocio/` | `.cursor/agents/negocio/` | `PLANO-NEGOCIO.md`, `negocio/handoff/` |

## Spec-Driven + Harness (completo)

**SDD próprio** com personas Marvel em `chamados/`. Alinhado ao espírito do [Spec Kit](https://github.com/github/spec-kit) (`specify → plan → tasks → implement → verify`), **sem** substituir o fluxo pelo Spec Kit CLI.

| Camada | O que é neste repo |
| --- | --- |
| Guides | Rules e agents em `.cursor/` (personas + `handoff.mdc`) |
| Tools | MCP (`mcp.json`), skills do `/jarvis`, scripts em `scripts/` |
| Sensors | `/visao`, `/viuvanegra` (grader = testes de aceite commitados), `/falcao`, Semgrep, Strix |
| Gates | `Status:` nos handoffs + `scripts/check-chamado-harness.sh` (`--before-pr` na Maria Hill) |
| Artifacts | Pasta local `chamados/<id>-<slug>/` (só `_template` no git) |
| Bootstrap | `/jarvis` no repo de produto |
| Eval (opcional) | `scripts/eval-harness-smoke.sh` |

Fluxo de arquivos:

```text
SPEC.md  →  PLANO-IMPLEMENTACAO.md  →  TASKS.md
                ↓
         sdd/handoff/entrega.md  →  revisao.md  →  [paridade.md]
                ↓
              prova.md  →  check --before-pr  →  PR
```

Anti reward-hacking: a Viúva committa os testes de aceite com a prova; o Iron Man **não** os enfraquece para ficar verde — lacuna de plano → `/drdestino`.

```bash
# estrutura (SPEC + PLANO + TASKS)
./scripts/check-chamado-harness.sh chamados/<NUMERO>-<slug>

# prontidão de PR (prova ok; paridade se superfície dupla)
./scripts/check-chamado-harness.sh --before-pr chamados/<NUMERO>-<slug>

# smoke do harness (deve ficar verde)
./scripts/eval-harness-smoke.sh
```

## Chamados (tickets)

Chamados reais ficam só na máquina; só `_template` vai pro git.

Planos e handoffs **não** ficam na raiz. Cada ticket tem uma pasta:

```
chamados/<NUMERO>-<slug-do-nome>/
  SPEC.md                     # engenharia — o quê / aceite (/drdestino)
  PLANO-IMPLEMENTACAO.md      # engenharia — como no repo (/drdestino → /ironman)
  TASKS.md                    # engenharia — checklist ordenado (/drdestino → /ironman)
  PLANO-NEGOCIO.md            # negócio (/pepper)
  sdd/handoff/...             # engenharia
  negocio/handoff/...         # negócio
```

Slug: minúsculas, sem acento, espaços → hífen. Ex.: `1234` + `Busca estabelecimentos` → `chamados/1234-busca-estabelecimentos/`.

**Como invocar** (número e nome obrigatórios na cadeia de engenharia, na de negócio, e em `/falcao`, `/loki`, `/shuri`):

```text
/drdestino 1234 Busca estabelecimentos
/pepper 1234 Plano de assinatura
/fury 1234 Plano de assinatura
```

Ou no corpo: `Ticket: 1234` e `Nome: …`.

Exceções sem ticket: `/jarvis` (bootstrap), `/capitao` (só link da PR), `/wong`, `/demolidor`. `/formiga` e `/heimdall` pedem ticket quando o trabalho é de um chamado.

Plano legado migrado: `chamados/001-migrado-busca-estabelecimentos/` (só PLANO — ver README lá). Chamados novos: `chamados/_template/`. Não há contrato na raiz do MCPs.

## Cadeia — Engenharia

`/drdestino` cria a pasta e escreve `SPEC.md` + `PLANO-IMPLEMENTACAO.md` + `TASKS.md` → `/ironman` implementa por id de task e grava `sdd/handoff/entrega.md` → `/visao` corrige o diff, grava `revisao.md` e, se houver tela, audita com `web-design-guidelines` → `/falcao` (depois do `/visao`, **antes** da `/viuvanegra`, quando a rule ou o SPEC/plano pede outra superfície; sem superfície dupla, skippable) grava `paridade.md` → `/viuvanegra` prova o aceite do **SPEC**, grava `prova.md`, e no diff roda Semgrep e Strix → `/mariahill` roda `check-chamado-harness.sh --before-pr` e abre a pull request. Se superfície dupla for obrigatória e não houver `paridade.md` com `Status: ok`, Maria Hill para e pede `/falcao`.

**Contexto mínimo — uma etapa atrás.** Cada persona lê só os paths da tabela em `.cursor/rules/engenharia/handoff.mdc` (SPEC/PLANO/TASKS conforme a tabela + handoff da etapa anterior; no máximo um opcional). Não abre a pasta `sdd/handoff/` inteira. Se `Status:` da anterior ≠ `ok`, para. Rules do repo de produto entram à parte. Não faz o papel da próxima.

Esqueleto de pasta: `chamados/README.md` e `chamados/_template/`.

| Comando | Personagem | Faz |
| --- | --- | --- |
| `/drdestino` | Dr. Destino | Cria `chamados/<NUMERO>-<slug>/` e escreve SPEC + PLANO + TASKS antes de código |
| `/ironman` | Iron Man | Implementa PLANO + TASKS e grava `sdd/handoff/entrega.md` |
| `/visao` | Visão | Revisa o diff, corrige até uma passagem limpa e, em tela, audita com `web-design-guidelines` |
| `/falcao` | Falcão | Matriz e score de paridade entre superfícies (ex.: web↔mobile); grava `paridade.md` |
| `/viuvanegra` | Viúva Negra | Prova o aceite do SPEC, o caminho visível com `playwright-cli` quando há tela, e procura falha no diff |
| `/mariahill` | Maria Hill | Gate harness `--before-pr`, abre a PR e devolve o link |
| `/capitao` | Capitão América | Lê os checks da PR, comenta no arquivo e na linha, e só publica depois de um "pode mandar" |
| `/formiga` | Homem-Formiga | Publica só o DEV que a skill daquele repo descreve |
| `/heimdall` | Heimdall | Roda o smoke daquele repo, com dado real e evidência |
| `/jarvis` | Jarvis | Prepara o repo na primeira vez; **instala** o tooling obrigatório |
| `/wong` | Wong | Organiza a árvore inteira e parte arquivo grande quando a leitura pede |
| `/demolidor` | Demolidor | Lê o texto da norma no acervo público [ctresb/leis](https://github.com/ctresb/leis) |
| `/loki` | Loki | Duelo adversarial leve ao plano ou à solução; grava `duelo.md` (fora do fluxo feliz) |
| `/shuri` | Shuri | Reverse engineering com [REA](https://github.com/morluto/rea); grava `recon.md` para o plano |

`/capitao`, `/formiga`, `/heimdall`, `/jarvis`, `/wong`, `/demolidor`, `/loki` e `/shuri` ficam fora da cadeia feliz. O Falcão entra na cadeia feliz só quando há superfície dupla obrigatória (posição fixa: após `/visao`, antes de `/viuvanegra`). O Loki só sob pedido. A Shuri só com alvo concreto e REA instalado (`npx rea-agents setup`).

### Handoff tipado (engenharia)

Dentro de `chamados/<NUMERO>-<slug>/`:

| Arquivo | Quem escreve |
| --- | --- |
| `SPEC.md` | `/drdestino` |
| `PLANO-IMPLEMENTACAO.md` | `/drdestino` |
| `TASKS.md` | `/drdestino` (cria); `/ironman` marca ids |
| `sdd/handoff/entrega.md` | `/ironman` |
| `sdd/handoff/revisao.md` | `/visao` |
| `sdd/handoff/prova.md` | `/viuvanegra` |
| `sdd/handoff/paridade.md` | `/falcao` |
| `sdd/handoff/duelo.md` | `/loki` |
| `sdd/handoff/recon.md` | `/shuri` |

Seções fixas na rule `.cursor/rules/engenharia/handoff.mdc`. Stubs com `Status: pendente` em `chamados/_template/`.

**Por que vários arquivos (e não um `HANDOFF.md` único):** cada persona lê só o handoff nomeado da anterior; `Status:` na primeira linha útil é o gate; caps de tamanho e “sem dump de log” mantêm o arquivo pequeno. Sem índice `STATUS.md` extra — a tabela de leitura + `check-chamado-harness.sh` bastam. Detalhe na rule `engenharia/handoff.mdc`.

## Cadeia — Negócio / produto

Mini-cadeia separada da SDD de código. Mesmo ticket e mesma pasta `chamados/`; artefatos em `PLANO-NEGOCIO.md` e `negocio/handoff/`.

Fluxo sugerido: `/fury` → `/pepper` → `/banner` e `/hope` (podem em paralelo após o plano v1) → `/ultron` → Pepper reforça se o painel pedir.

| Comando | Personagem | Faz |
| --- | --- | --- |
| `/fury` | Nick Fury | Discovery e voz do cliente → `negocio/handoff/discovery.md` |
| `/pepper` | Pepper Potts | Único `PLANO-NEGOCIO.md` (ops / orquestração) |
| `/banner` | Banner | Pricing, unit economics, risco → `negocio/handoff/financeiro.md` |
| `/hope` | Hope van Dyne | GTM, launch, messaging → `negocio/handoff/gtm.md` |
| `/ultron` | Ultron | Painel leve de compradores (3–5) → `negocio/handoff/painel.md` |

Exemplo:

```text
/fury 5678 Oferta mensal oficinas
/pepper 5678 Oferta mensal oficinas
/banner 5678 Oferta mensal oficinas
/hope 5678 Oferta mensal oficinas
/ultron 5678 Oferta mensal oficinas
```

Seções fixas e tabela de leitura estrita na rule `negocio/handoff-negocio.mdc` (contexto mínimo — uma etapa atrás). Se depois houver implementação, use o mesmo número e nome com `/drdestino` e `SPEC` / `PLANO` / `TASKS`.

## Primeira vez num repositório

O `/jarvis` cria `.cursor/` na raiz daquele repo e deixa a pasta só na máquina (entra no `.gitignore`). Lá nascem as rules de arquitetura, comando e CI que o código já mostra, as skills de deploy e de smoke, e o tooling:

1. **Instala** Graphify, Strix e Semgrep (não só reporta).
2. Se o repo tem interface web, instala `playwright-cli` e `web-design-guidelines`.
3. **Verifica alternativas** ao stack; mantém o padrão salvo troca drop-in claramente melhor; documenta o que foi considerado.

Detalhe de ambiente, fila, tenant e pipeline não fica nas personas do MCPs: fica nesse `.cursor/` local. Personas e pasta `chamados/` **não** são copiadas para o repo de produto.

Sem esse preparo, as outras personas de engenharia param e pedem o `/jarvis`. O `/capitao` ainda consegue ler o diff da PR.

## Inventário — repositórios e ferramentas externas

Só o que este fluxo já referencia. Não é catálogo genérico.

### Repositórios / projetos GitHub

| Nome | URL | Uso no fluxo |
| --- | --- | --- |
| Graphify (`graphifyy`) | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) / PyPI `graphifyy` | Grafo local do código; `/jarvis` instala; quem explora consulta o grafo |
| Strix | [usestrix/strix](https://github.com/usestrix/strix) | Skills de pentest no diff; `/viuvanegra` |
| Semgrep | [semgrep/semgrep](https://github.com/semgrep/semgrep) | SAST no diff; MCP `semgrep` no `.cursor/mcp.json` do **repo de produto** |
| playwright-cli | Pacote npm `@playwright/cli` | Prova visual local; skill em `.agents/skills` ou `~/.agents/skills` |
| web-design-guidelines | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) (+ guia [web-interface-guidelines](https://github.com/vercel-labs/web-interface-guidelines)) | Auditoria de UI; `/visao`, `/capitao` |
| ctresb/leis | [ctresb/leis](https://github.com/ctresb/leis) | Acervo de normas; `/demolidor` + `scripts/extrair-trecho-lei.py` |
| REA | [morluto/rea](https://github.com/morluto/rea) | Reverse engineering; `/shuri` (`npx rea-agents setup`) |

Ficam de fora do install padrão: taste-skill, awesome-design-md, image-to-code e o servidor MCP `@playwright/mcp`.

### CLIs e bibliotecas (install)

| Ferramenta | Como instalar | Onde fica |
| --- | --- | --- |
| Graphify | `uv tool install graphifyy` → `graphify install --project --platform cursor` | CLI no PATH; rule em `.cursor/rules/graphify.mdc` do repo |
| Strix skills | `npx skills add usestrix/strix -a cursor` | `.cursor/skills/` do repo |
| Semgrep | `brew install semgrep` ou `uv tool install semgrep` | CLI; MCP no `.cursor/mcp.json` do repo |
| playwright-cli | `npm install -g @playwright/cli@latest` + `playwright-cli install --skills=agents` | global + `.agents/skills/playwright-cli` |
| web-design-guidelines | `npx skills add vercel-labs/agent-skills --skill web-design-guidelines --global --agent cursor -y` | `~/.agents/skills/` |
| REA (Shuri) | `npx rea-agents setup` | skill/MCP conforme o setup do REA |
| uv / uvx | instalador oficial do Astral | usado por Graphify, Semgrep (opção) e MCP `jira-totvs` (`uvx mcp-atlassian`) |
| Azure CLI (`az`) | instalador Microsoft | `azure-integration`, `ado`, `scripts/azure-login.sh` |
| Docker | Docker Desktop / Engine | server `github` (imagem `ghcr.io/github/github-mcp-server`) |
| Node / npm / npx | LTS | vários MCPs stdio e skills |
| Python 3 | sistema ou pyenv | `scripts/extrair-trecho-lei.py` (stdlib + rede) |
| GitHub CLI (`gh`) | `brew install gh` | `/demolidor` e fluxos que leem API GitHub |

Variáveis de exemplo (não commitadas): ver `.env.example` — `ASAAS_API_KEY`, `JIRA_PERSONAL_TOKEN`, `RENDER_API_KEY`, `N8N_API_URL`, `N8N_API_KEY`, e para Strix no shell `OPENAI_API_KEY` / `LLM_API_KEY` / `STRIX_LLM`.

### Ferramentas do fluxo (resumo)

| Nome | O que é | Para que serve | Quem usa | Acesso |
| --- | --- | --- | --- | --- |
| Graphify (`graphifyy`) | Grafo local do código | Ligação entre arquivos antes de abrir o repo | Exploração; `/jarvis` instala | Nenhum. Parse local |
| Strix (`usestrix/strix`) | Skills de pentest no diff | Falha no que a tarefa mudou | `/viuvanegra` | Chave de LLM no shell (`OPENAI_API_KEY` ou `LLM_API_KEY`, modelo em `STRIX_LLM`) |
| Semgrep | Análise estática | Bug/padrão inseguro no diff | `/viuvanegra` | Nenhum. Sem `semgrep login` / `semgrep ci` no bootstrap |
| `playwright-cli` | Browser por CLI | Prova visual | `/ironman`, `/viuvanegra`, `/heimdall` | Nenhum. Chromium na 1ª prova |
| `web-design-guidelines` | Skill Vercel | Auditoria de UI | `/visao`, `/capitao` | Nenhum. Guia público no GitHub |
| REA | Reverse engineering | Comportamento sem fonte | `/shuri` | Setup local do REA |
| ctresb/leis | Acervo Markdown | Texto de norma | `/demolidor` | API GitHub pública (`gh`) |

### Servidores MCP (`mcp.json`)

| Server | O que é | Para que serve | Acesso |
| --- | --- | --- | --- |
| `azure-integration` | `@azure/mcp`, só leitura | Docs Microsoft e recurso Azure | `az login` |
| `ado` | `@azure-devops/mcp`, org `totvstfs` | Work item, repo e PR no Azure DevOps | Sessão Azure CLI |
| `jira-totvs` | `mcp-atlassian` via `uvx` | Card no Jira de produção da TOTVS | `JIRA_PERSONAL_TOKEN` |
| `postman` | MCP oficial, modo minimal | Collection e environment | OAuth no Cursor |
| `github` | `github-mcp-server` (Docker) | Issue, arquivo e PR no GitHub | OAuth, callback porta `8085` |
| `gitmcp` | gitmcp.io | Documentação de repo público | Nenhum |
| `deepwiki` | mcp.deepwiki.com | Wiki gerada de repo público | Nenhum |
| `stripe` | mcp.stripe.com | Conta Stripe | OAuth Stripe |
| `asaas` | `asaas-mcp` | API Asaas | `ASAAS_API_KEY` |
| `asaas-docs` | docs.asaas.com/mcp | Documentação Asaas | Nenhum |
| `meta-ads` | MCP de anúncios da Meta | Gerenciador de Anúncios | OAuth Meta |
| `meta-instagram` | MCP de Instagram da Meta | Publicação no Instagram | OAuth Meta |
| `render` | mcp.render.com | Serviço, deploy e log no Render | `RENDER_API_KEY` |
| `n8n-mcp` | `n8n-mcp` | Instância n8n | `N8N_API_URL` e `N8N_API_KEY` |

O Semgrep MCP **não** está neste `mcp.json`: o `/jarvis` grava no `.cursor/mcp.json` de cada repo de produto.

### Scripts locais (`scripts/`)

| Script | Função |
| --- | --- |
| `scripts/apply-to-cursor.sh` | Copia `mcp.json` → `~/.cursor/mcp.json` substituindo `${VAR}` pelo `.env` |
| `scripts/load-env.sh` | `source` — exporta o `.env` no shell atual (Strix / LLM) |
| `scripts/with-env.sh` | Roda um comando já com o `.env` exportado |
| `scripts/strix-env-check.sh` | Confere `STRIX_LLM` + chave LLM (só SET/UNSET) |
| `scripts/azure-login.sh` | Abre `az login` e lista subscriptions |
| `scripts/extrair-trecho-lei.py` | Baixa um Markdown do acervo ctresb/leis e imprime cabeçalho/artigo (usado pelo `/demolidor`) |
| `scripts/check-chamado-harness.sh` | Gate de chamado: estrutura (SPEC/PLANO/TASKS) e `--before-pr` (prova/paridade) |
| `scripts/eval-harness-smoke.sh` | Smoke do harness (template + cenários temp); deve ficar verde |

## Aplicar no Cursor

```bash
cp .env.example .env
./scripts/apply-to-cursor.sh
```

Recarregue a janela (Cmd+Shift+P, Reload Window). Postman e GitHub pedem login no primeiro uso.
