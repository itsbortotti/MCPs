# Manual — cole no chat e siga

Guia prático: cola um comando → espera gravar arquivos → confere → cola o próximo.

Duas filas neste manual: **negócio** (ideia, preço, mensagem) e **dev** (plano + código). Cada ticket tem **número + nome** e pasta `MCPs/chamados/<NUMERO>-<slug>/`. Não pule pro `/ironman` sem `SPEC.md` / plano / lista de tarefas — e sem `Status: ok` da etapa anterior.

**Vídeo / MiniMax:** terceira cadeia — [MANUAL-MIDIA.md](MANUAL-MIDIA.md) (`/diretor` … `/camera` … `/distribuidor`).

Personas: [README.md](README.md).

---

## 1. Antes de começar

- Workspace: **MCPs** + repo do **produto** (ex.: GarageFlow).
- Uma vez no produto: `/jarvis` (prepara o `.cursor/` local).
- Todo ticket: **número + nome** → pasta `MCPs/chamados/<NUMERO>-<slug>/`.
- Chamados reais ficam na máquina; no git só o `_template`.
- Um comando por mensagem. Só avance com `Status: ok`.
- Ticket no MCPs; código no produto.

> **Dica:** `Status: ok` = pode ir. Outra coisa = parado.

---

## 2. Simulação A — negócio → dev

Primeiro “compra” a ideia no negócio. Depois, no **mesmo ticket**, planeja e implementa. Negócio → `PLANO-NEGOCIO.md` + `negocio/handoff/`. Dev → `SPEC.md`, `PLANO-IMPLEMENTACAO.md`, `TASKS.md` + `sdd/handoff/`. Código no produto.

| Fila | Ordem | Arquivos |
|------|--------|----------|
| Negócio | Fury → Pepper → Banner+Hope → (Ultron) | `PLANO-NEGOCIO.md`, `negocio/handoff/` |
| Dev | Destino → Iron Man → Visão → (Falcão) → Viúva → Maria Hill → Capitão | SPEC / plano / tasks, `sdd/handoff/` |

**Ticket:** `4242` · `Assinatura mensal oficina`  
**Pasta:** `chamados/4242-assinatura-mensal-oficina/`  
**Ideia:** no Painel Master a oficina assina plano mensal (preço, cobrança, status ativo/atrasado). Tela web **e** app.

### Negócio

**`/fury`** — ouve a dor e grava `discovery.md`.

```
/fury 4242 Assinatura mensal oficina

Quero entender se oficinas pagariam mensalidade por painel com cobrança e status. Foque dor de atraso e preço.
```

**Confere:** `negocio/handoff/discovery.md` → `Status: ok`.

Exemplo do que aparece (`negocio/handoff/discovery.md`):

```markdown
# Discovery — 4242 Assinatura mensal oficina

Status: ok

## Dor
Dono de oficina não sabe se a mensalidade do sistema está em dia.
Atraso vira surpresa no fim do mês.

## Hipótese
Pagaria R$ 99–149/mês se vir preço claro, cobrança e status
(ativo / atrasado) no Painel Master — web e app.

## Fora desta conversa
API, telas e tasks de código — isso é depois, no Destino.
```

**`/pepper`** — vira isso em plano de negócio (ainda sem código).

```
/pepper 4242 Assinatura mensal oficina

Com base no discovery, escreve o PLANO-NEGOCIO: ICP oficina, oferta mensal no Painel Master, fora de escopo. Sem lista de código.
```

**Confere:** `PLANO-NEGOCIO.md` legível, sem endpoints nem tasks.

Exemplo do que aparece (`PLANO-NEGOCIO.md`):

```markdown
# Plano de negócio — 4242 Assinatura mensal oficina

## Oferta
Plano mensal no Painel Master: preço visível, gera cobrança,
status ativo ou atrasado.

## Quem compra
Dono de oficina (1–3 usuários) que já usa o painel no dia a dia.

## Fora de escopo
App de pagamento próprio, NF, integração com banco.
Isso fica para outro ticket.

## Sucesso
Oficina vê status da assinatura em menos de 10 segundos
depois do login no Painel.
```

**Banner + Hope** — um precifica, o outro escreve a mensagem. Paralelo ok (duas mensagens).

```
/banner 4242 Assinatura mensal oficina

Precifica o plano mensal e cenários conservador/base/otimista. Hipótese de atraso e churn.
```

```
/hope 4242 Assinatura mensal oficina

Mensagem de lançamento para dono de oficina: preço claro, cobrança e status no Painel.
```

**Confere:** `financeiro.md` e `gtm.md` → `Status: ok`.

**(Opcional)** `/ultron` — stress-test da oferta.

```
/ultron 4242 Assinatura mensal oficina

Painel: dono de oficina que atrasa pagamento e o que mata a oferta.
```

**Confere:** `painel.md` — se for seguir, ok; senão, reforça com Pepper.

### Dev (mesmo ticket)

**`/drdestino`** — escreve `SPEC.md` (o que precisa funcionar), plano e lista de tarefas.

```
/drdestino 4242 Assinatura mensal oficina

Quero que a oficina possa assinar um plano mensal pelo Painel Master: ver preço, gerar cobrança e ver status ativo/atrasado. Web e mobile.
```

**Confere:** os três arquivos existem; o aceite dá pra testar; fala de web **e** app.

Exemplo do que aparece (`SPEC.md`):

```markdown
# SPEC — 4242 Assinatura mensal oficina

## Objetivo
No Painel Master, a oficina assina plano mensal:
vê preço, gera cobrança e vê status ativo/atrasado.

## Aceite
1. Admin Master abre Assinatura e vê preço do plano.
2. Gera cobrança; status fica ativo ou atrasado.
3. Mesmo fluxo na tela web e no app.

## Fora
NF, gateway novo, landing pública.
```

Exemplo do que aparece (`TASKS.md` — trecho):

```markdown
# TASKS — 4242

- [ ] T1 Backend: modelo assinatura + status
- [ ] T2 API: criar cobrança e consultar status
- [ ] T3 Web: tela Assinatura no Painel Master
- [ ] T4 App: mesma tela no mobile
- [ ] T5 Testes do fluxo ativo/atrasado
```

**`/ironman`** — só agora mexe no código. Resumo da entrega no MCPs.

```
/ironman 4242 Assinatura mensal oficina

Implementa as tasks do chamado. Código no repo do produto; handoff de entrega no MCPs.
```

**Confere:** diff no produto + `sdd/handoff/entrega.md` → `Status: ok`; tasks `[x]`.

Exemplo do que aparece (`sdd/handoff/entrega.md`):

```markdown
# Entrega — 4242 Assinatura mensal oficina

Status: ok

## Feito
- T1–T5 concluídas
- Backend: `backend/app/features/assinatura/`
- Web: `frontend/src/features/assinatura/pages/`
- App: `mobile/lib/features/assinatura/screens/`

## Obs
Cobrança mock em DEV; gateway real fica fora deste ticket.
```

**`/visao`** — revisa o que mudou (e a tela, se tiver).

```
/visao 4242 Assinatura mensal oficina
```

**Confere:** `revisao.md` → `Status: ok`.

**`/falcao`** — neste exemplo tem web **e** app. Depois do Visão, **antes** da Viúva. Sem `paridade.md` ok, Maria Hill trava.

> **Pular Falcão:** só uma tela (ex. só web) → não chama `/falcao`.

```
/falcao 4242 Assinatura mensal oficina

Paridade web ↔ mobile do fluxo de assinatura mensal no Painel Master.
```

**Confere:** `paridade.md` → `Status: ok`.

Exemplo do que aparece (`sdd/handoff/paridade.md`):

```markdown
# Paridade — 4242

Status: ok

| Fluxo              | Web | App |
|--------------------|-----|-----|
| Ver preço          | ok  | ok  |
| Gerar cobrança     | ok  | ok  |
| Status ativo/atras.| ok  | ok  |
```

**`/viuvanegra`** — testa se o `SPEC.md` realmente funciona.

```
/viuvanegra 4242 Assinatura mensal oficina
```

**Confere:** `prova.md` → `Status: ok`.

Exemplo do que aparece (`sdd/handoff/prova.md`):

```markdown
# Prova — 4242 Assinatura mensal oficina

Status: ok

## Aceite
1. Preço visível no Painel — ok
2. Cobrança + status ativo/atrasado — ok
3. Web e app — ok

## Checks
Semgrep e Strix no diff: sem bloqueio.
```

**(Opcional)** na raiz do MCPs — Maria Hill já roda isso antes da PR:

```bash
./scripts/check-chamado-harness.sh --before-pr chamados/4242-assinatura-mensal-oficina
```

Exemplo do que aparece no terminal:

```text
OK  pasta do chamado
OK  SPEC + PLANO + TASKS
OK  sdd/handoff (entrega, revisao, paridade, prova)
OK  pronto para PR
```

**`/mariahill`** — abre a PR.

```
/mariahill 4242 Assinatura mensal oficina
```

**Espera** o link. Se faltar `paridade.md` ok (quando web+app for obrigatório), ela para.

**`/capitao`** — valida a PR pelo link.

```
/capitao

https://github.com/ORG/REPO/pull/NNN
```

No fim: `PLANO-NEGOCIO.md`, SPEC / plano / tasks, `negocio/handoff/*`, `sdd/handoff/{entrega,revisao,paridade,prova}.md`.

### O que você leva

- Ticket = número + nome → uma pasta; negócio e dev juntos, arquivos separados.
- Negócio não manda API; dev não começa no Iron Man.
- `Status: ok` → cola o próximo.
- Web + app → `/falcao` entre Visão e Viúva; Maria Hill exige `paridade.md` ok.
- Código no produto; planos no MCPs. PR só depois da prova.

---

## 3. Simulação B — task pequena (só dev)

Mesmo ritmo, sem negócio. **Só web** → não chama Falcão.

**Ticket:** `9910` · `Fix timeout lista OS` → `chamados/9910-fix-timeout-lista-os/`

```
/drdestino 9910 Fix timeout lista OS

A lista de OS no web demora e estoura timeout em oficina com muitas ordens. Quero paginação ou limite seguro no backend e a tela não travar. Só web nesta fatia.
```

**Confere** SPEC / plano / tasks. Exemplo do `SPEC.md`:

```markdown
# SPEC — 9910 Fix timeout lista OS

## Aceite
1. Lista de OS no web carrega sem timeout com 5k+ ordens.
2. Backend pagina ou limita o retorno.
3. Só web nesta fatia (sem app).
```

```
/ironman 9910 Fix timeout lista OS
```

→ `entrega.md` ok → `/visao` → `revisao.md` ok → **não** `/falcao` → `/viuvanegra` → `prova.md` ok → `/mariahill` → `/capitao` + link da PR.

> **Dica:** “só web nesta fatia” no Destino = pode pular Falcão.

---

## 4. Se der erro

- Sem número + nome → para; manda de novo com os dois.
- `Status` ≠ `ok` → não avance; leia o bloqueio.
- Comando “não pega” → falta **MCPs** no workspace.
- Pede bootstrap → `/jarvis` no produto.
- Maria Hill pede Falcão → `/falcao`, depois `/mariahill` de novo.
- API/código no `PLANO-NEGOCIO.md` → errado; isso vai no SPEC / plano / tasks.

---

## 5. Cola rápida

**Negócio:** `/fury` → `/pepper` → `/banner`+`/hope` → (`/ultron`) → Destino.  
**Dev:** `/drdestino` → `/ironman` → `/visao` → (`/falcao` se web+app) → `/viuvanegra` → `/mariahill` → `/capitao`+PR.

`/jarvis` · `/fury`…`/ultron` · `/drdestino` · `/ironman` · `/visao` · `/falcao` · `/viuvanegra` · `/mariahill` · `/capitao` · `/loki`/`/shuri` · `/formiga`/`/heimdall`

```bash
./scripts/check-chamado-harness.sh chamados/<pasta>
./scripts/check-chamado-harness.sh --before-pr chamados/<pasta>
```
