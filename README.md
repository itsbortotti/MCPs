# MCPs

Configuração do Cursor para desenvolver com spec-driven: os servidores MCP ficam neste repositório, e cada persona sabe o que fazer quando o comando dela é chamado.

São duas partes.

**Servidores.** O `mcp.json` é a lista do que o Cursor pode consultar (Azure, Azure DevOps, Jira, Postman, GitHub e o restante). O `scripts/apply-to-cursor.sh` copia essa lista para `~/.cursor/mcp.json`, troca cada `${VAR}` pelo valor do `.env` e não mexe em servidor de plugin que só exista no Cursor. Segredo não entra no git: copie `.env.example` para `.env` e preencha. O `.env` está no `.gitignore`.

**Personas.** Os arquivos em `.cursor/rules/` dizem como a IA trabalha. O `sdd-personas.mdc` fica sempre ativo e só guarda a cadeia. O procedimento de cada personagem entra quando o comando dele é usado.

Abra esta pasta no workspace do Cursor para as personas valerem. Numa janela só com outro repositório, a cadeia não entra.

## Cadeia

`/drdestino` escreve o plano → `/ironman` implementa só esse plano → `/visao` corrige o diff → `/viuvanegra` prova os critérios de aceite, com Semgrep e Strix no diff → `/mariahill` abre a pull request e devolve o link.

Cada uma lê o plano, a entrega da anterior e as rules do repositório em que o comando rodou. Não faz o papel da próxima.

| Comando | Personagem | Faz |
| --- | --- | --- |
| `/drdestino` | Dr. Destino | Planeja num `PLANO-IMPLEMENTACAO.md`, com critério de aceite, antes de código |
| `/ironman` | Iron Man | Implementa só o plano, no padrão do repo |
| `/visao` | Visão | Revisa o diff e corrige até uma passagem limpa |
| `/viuvanegra` | Viúva Negra | Prova o aceite e procura falha no diff |
| `/mariahill` | Maria Hill | Abre a PR do incremento e devolve o link |
| `/capitao` | Capitão América | Comenta na PR do link, no arquivo e na linha, e só publica depois de um "pode mandar" |
| `/formiga` | Homem-Formiga | Publica só o DEV que a skill daquele repo descreve |
| `/heimdall` | Heimdall | Roda o smoke daquele repo, com dado real e evidência |
| `/jarvis` | Jarvis | Prepara o repo na primeira vez |

`/capitao`, `/formiga`, `/heimdall` e `/jarvis` ficam fora da cadeia de implementação. O Capitão só roda quando chega o link. Formiga e Heimdall só executam a skill que o Jarvis gravou naquele repo.

## Primeira vez num repositório

O `/jarvis` cria `.cursor/` na raiz daquele repo e deixa a pasta só na máquina (entra no `.gitignore`). Lá nascem as rules de arquitetura, comando e CI que o código já mostra, as skills de deploy e de smoke, o Graphify, o Strix e o Semgrep. Detalhe de ambiente, fila, tenant e pipeline não fica nas personas: fica nesse `.cursor/` local.

Sem esse preparo, as outras personas param e pedem o `/jarvis`. O `/capitao` ainda consegue ler o diff da PR.

## Servidores

| Server | Uso |
| --- | --- |
| `azure-integration` | Azure em leitura, inclusive documentação Microsoft |
| `ado` | Azure DevOps, pela sessão da Azure CLI |
| `jira-totvs` | Card no Jira |
| `postman` | Collection no Postman, com login OAuth |
| `github` | GitHub, pela imagem oficial, com login no navegador |
| `gitmcp` | Docs de repositório público no GitHub |
| `deepwiki` | Pergunta sobre repositório público no GitHub |
| `stripe`, `asaas`, `asaas-docs` | Pagamento |
| `render` | Render |
| `n8n-mcp` | Instância n8n |

`scripts/azure-login.sh` abre o `az login` e lista as subscriptions. Quem escolhe a subscription ativa é o `az account set`.

## Aplicar no Cursor

```bash
cp .env.example .env
./scripts/apply-to-cursor.sh
```

Recarregue a janela (Cmd+Shift+P, Reload Window). Postman e GitHub pedem login no primeiro uso.
