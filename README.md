# MCPs

Configuração do Cursor para desenvolver com spec-driven: os servidores MCP ficam neste repositório, e cada persona sabe o que fazer quando o comando dela é chamado.

São duas partes.

**Servidores.** O `mcp.json` é a lista do que o Cursor pode consultar (Azure, Azure DevOps, Jira, Postman, GitHub e o restante). O `scripts/apply-to-cursor.sh` copia essa lista para `~/.cursor/mcp.json`, troca cada `${VAR}` pelo valor do `.env` e não mexe em servidor de plugin que só exista no Cursor. Segredo não entra no git: copie `.env.example` para `.env` e preencha. O `.env` está no `.gitignore`.

**Personas.** Os arquivos em `.cursor/rules/` dizem como a IA trabalha. O `sdd-personas.mdc` fica sempre ativo e só guarda a cadeia. O procedimento de cada personagem entra quando o comando dele é usado.

Abra esta pasta no workspace do Cursor para as personas valerem. Numa janela só com outro repositório, a cadeia não entra.

## Cadeia

`/drdestino` escreve o plano → `/ironman` implementa só esse plano → `/visao` corrige o diff e, se houver tela, audita com `web-design-guidelines` → `/viuvanegra` prova os critérios de aceite, o caminho visível com `playwright-cli` quando há tela, e Semgrep e Strix no diff → `/mariahill` abre a pull request e devolve o link.

Cada uma lê o plano, a entrega da anterior e as rules do repositório em que o comando rodou. Não faz o papel da próxima. Se uma rule do repo exige outra superfície na mesma tarefa, o plano inclui essa superfície ou a exceção que a rule permite. O Visão não fecha a passagem com ela faltando.

| Comando | Personagem | Faz |
| --- | --- | --- |
| `/drdestino` | Dr. Destino | Planeja num `PLANO-IMPLEMENTACAO.md`, com critério de aceite, antes de código |
| `/ironman` | Iron Man | Implementa só o plano, no padrão do repo |
| `/visao` | Visão | Revisa o diff, corrige até uma passagem limpa e, em tela, audita com `web-design-guidelines` |
| `/viuvanegra` | Viúva Negra | Prova o aceite, o caminho visível com `playwright-cli` quando há tela, e procura falha no diff |
| `/mariahill` | Maria Hill | Abre a PR do incremento e devolve o link |
| `/capitao` | Capitão América | Lê os checks da PR, comenta no arquivo e na linha, e só publica depois de um "pode mandar" |
| `/formiga` | Homem-Formiga | Publica só o DEV que a skill daquele repo descreve |
| `/heimdall` | Heimdall | Roda o smoke daquele repo, com dado real e evidência |
| `/jarvis` | Jarvis | Prepara o repo na primeira vez |

`/capitao`, `/formiga`, `/heimdall` e `/jarvis` ficam fora da cadeia de implementação. O Capitão só roda quando chega o link. Formiga e Heimdall só executam a skill que o Jarvis gravou naquele repo.

## Primeira vez num repositório

O `/jarvis` cria `.cursor/` na raiz daquele repo e deixa a pasta só na máquina (entra no `.gitignore`). Lá nascem as rules de arquitetura, comando e CI que o código já mostra, as skills de deploy e de smoke, o Graphify, o Strix e o Semgrep. Se o repo tem interface web, também entram `playwright-cli` e `web-design-guidelines`. Detalhe de ambiente, fila, tenant e pipeline não fica nas personas: fica nesse `.cursor/` local.

Sem esse preparo, as outras personas param e pedem o `/jarvis`. O `/capitao` ainda consegue ler o diff da PR.

## Terceiros

O que o fluxo usa de fora do nosso código. O `/jarvis` instala no repo o que for ferramenta de código (Graphify, Strix, Semgrep e, se houver tela, Playwright e as guidelines). Os servidores MCP ficam neste repositório e entram no Cursor pelo `scripts/apply-to-cursor.sh`.

### Ferramentas do fluxo

| Nome | O que é | Para que serve | Como ajuda | Quem usa | Acesso |
| --- | --- | --- | --- | --- | --- |
| Graphify (`graphifyy`) | Grafo local do código | Achar ligação entre arquivos antes de abrir o repo | Mostra dependência que a busca por texto não vê. Atualiza no commit, no checkout e no pull, em segundo plano | Quem explora o código. O `/jarvis` instala | Nenhum. O parse fica na máquina. O grafo não sobe |
| Strix (`usestrix/strix`) | Skills de pentest no diff | Achar vulnerabilidade no que a tarefa mudou | Prova a falha no código e no fluxo do diff, com teto de custo. Não varre o repositório inteiro e não usa a cloud do Strix | `/viuvanegra` | Chave de LLM no shell (`OPENAI_API_KEY` ou `LLM_API_KEY`, modelo em `STRIX_LLM`). O `apply-to-cursor.sh` não copia essas variáveis |
| Semgrep | Análise estática | Achar bug e padrão inseguro no diff | Roda `semgrep scan --config auto` só nos arquivos do diff. Não envia resultado para a nuvem | `/viuvanegra`. O MCP `semgrep` nasce no `.cursor/mcp.json` daquele repo, não neste `mcp.json` | Nenhum. Sem `semgrep login` e sem `semgrep ci` |
| `playwright-cli` | Browser por linha de comando. Skill em `~/.agents/skills/playwright-cli` | Abrir a tela local, clicar e tirar snapshot | Prova o critério visual sem carregar a árvore inteira da página no contexto | `/ironman` confere a rota. `/viuvanegra` prova o aceite. `/heimdall` só se o smoke abrir interface | Nenhum. O Chromium baixa da CDN da Microsoft na primeira prova |
| `web-design-guidelines` (Vercel) | Skill em `~/.agents/skills/web-design-guidelines` | Auditar a interface do diff | Aponta contraste, foco, formulário e estado vazio em `arquivo:linha`, contra o guia público | `/visao` corrige. `/capitao` comenta o que ainda estiver na PR | Nenhum. Na auditoria, baixa o guia no GitHub |

Ficam de fora: taste-skill, awesome-design-md e image-to-code (trocam o visual do repositório) e o servidor MCP `@playwright/mcp` (repete o CLI e gasta mais contexto).

### Servidores MCP

| Server | O que é | Para que serve | Como ajuda | Acesso |
| --- | --- | --- | --- | --- |
| `azure-integration` | `@azure/mcp`, só leitura | Documentação Microsoft e recurso Azure (função, fila, monitor, banco, cofre, storage) | Consulta o que está na subscription sem escrever na conta | `az login`. `scripts/azure-login.sh` abre o login e lista as subscriptions. A subscription ativa é `az account set` |
| `ado` | `@azure-devops/mcp`, org `totvstfs` | Work item, repositório e pull request no Azure DevOps | A Maria Hill abre a PR e o Capitão comenta quando o host é o Azure DevOps | Sessão da Azure CLI |
| `jira-totvs` | `mcp-atlassian` | Card no Jira de produção da TOTVS | O plano nasce do card de verdade, com tipo e campo reais | `JIRA_PERSONAL_TOKEN` |
| `postman` | MCP oficial, modo minimal | Collection e environment | O Heimdall dispara o request de smoke quando a skill daquele repo aponta o Postman | OAuth no Cursor. A API key não entra no repo |
| `github` | `github-mcp-server`, imagem oficial no Docker | Issue, arquivo e pull request no GitHub | A Maria Hill abre a PR e o Capitão comenta quando o host é o GitHub | OAuth no navegador, callback na porta `8085` |
| `gitmcp` | gitmcp.io | Documentação de repositório público | Tira dúvida de biblioteca sem clonar o repo | Nenhum |
| `deepwiki` | mcp.deepwiki.com | Wiki gerada de repositório público | Explica um código que a gente não mantém | Nenhum |
| `stripe` | mcp.stripe.com | Conta Stripe | Consulta cliente, pagamento e assinatura | OAuth Stripe |
| `asaas` | `asaas-mcp` | API Asaas | Cria e consulta cobrança, cliente e assinatura na conta | `ASAAS_API_KEY` |
| `asaas-docs` | docs.asaas.com/mcp | Documentação da Asaas | Confere o endpoint antes de chamar a API | Nenhum |
| `meta-ads` | MCP de anúncios da Meta | Gerenciador de Anúncios | Consulta e opera campanha na conta ligada | OAuth Meta |
| `meta-instagram` | MCP de Instagram da Meta | Publicação no Instagram | Consulta e publica na conta ligada | OAuth Meta |
| `render` | mcp.render.com | Serviço, deploy e log no Render | Vê o que está no ar e o que o deploy fez | `RENDER_API_KEY` |
| `n8n-mcp` | `n8n-mcp` | Instância n8n | Lê e altera workflow nessa instância | `N8N_API_URL` e `N8N_API_KEY` |

## Aplicar no Cursor

```bash
cp .env.example .env
./scripts/apply-to-cursor.sh
```

Recarregue a janela (Cmd+Shift+P, Reload Window). Postman e GitHub pedem login no primeiro uso.
