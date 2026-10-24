# Manual — Mídia (vídeo com MiniMax)

Guia exclusivo da **terceira cadeia** do MCPs: ofício + artefatos no chamado + MiniMax só no fim.

Personas de engenharia/negócio: [MANUAL.md](MANUAL.md) e [README.md](README.md).  
Contrato: `.cursor/rules/midia/handoff-midia.mdc`.

---

## 1. Ideia em uma frase

Prepare **tudo no papel** (brief → roteiro → storyboard → pacote de jobs). Só então a **`/camera`** chama o MiniMax — como o `/ironman` só roda depois do SPEC/PLANO/TASKS.

| Fase | Quem | Gera mídia? |
|------|------|-------------|
| Papel | `/diretor` … `/produtor` | Não |
| Runtime | `/camera` | **Sim** (só MiniMax) |
| Acabamento | `/montador` → `/critico` → `/distribuidor` | Não |

Ninguém publica rede social. O `/distribuidor` só escreve o pacote; você sobe o vídeo.

---

## 2. Antes de começar

- Workspace com a pasta **MCPs** aberta (personas carregam daqui).
- MCP **MiniMax Design** disponível no Cursor (`user-minimax-design`).
- Todo ticket: **número + nome** → `chamados/<NUMERO>-<slug>/`.
- Um comando por mensagem. Só avance com `Status: ok` no handoff da etapa.
- Custo MiniMax: quando a `/camera` pedir confirmação, responda **sim** / **go** (ou recuse). Ela não confirma sozinha.

> **Dica:** `Status: ok` = pode ir. `pendente` / `gap` / `bloqueado` = parado.

---

## 3. Pasta e arquivos

```
chamados/<NUMERO>-<slug>/
  BRIEF-VIDEO.md                 ← /diretor
  midia/handoff/
    roteiro.md                   ← /roteirista
    storyboard.md                ← /story
    pacote-minimax.md            ← /produtor  (jobs, sem API)
    producao.md                  ← /camera    (única geração)
    montagem.md                  ← /montador
    qa.md                        ← /critico
    pacote.md                    ← /distribuidor (não publica)
```

Stubs: `chamados/_template/BRIEF-VIDEO.md` e `chamados/_template/midia/handoff/`.

Pode coexistir no **mesmo chamado** com `PLANO-NEGOCIO.md` / `SPEC.md` — pastas de handoff separadas (`negocio/`, `sdd/`, `midia/`).

---

## 4. Comandos (ofício)

| Comando | Papel | Escreve |
|---------|--------|---------|
| `/diretor` | Brief mestre | `BRIEF-VIDEO.md` |
| `/roteirista` | Hooks + roteiro falado | `roteiro.md` |
| `/story` | Shot list + prompts | `storyboard.md` |
| `/produtor` | Jobs MiniMax no papel | `pacote-minimax.md` |
| `/camera` | Executa MiniMax | `producao.md` |
| `/montador` | Timeline / sync | `montagem.md` |
| `/critico` | QA vs brief | `qa.md` |
| `/distribuidor` | Título, thumb, caption | `pacote.md` |

Rules: `.cursor/rules/midia/`. Agents: `.cursor/agents/midia/`.  
Skill da câmera: `.cursor/skills/midia-minimax/SKILL.md`.

---

## 5. Simulação — um Reel curto

**Ticket:** `9001` · `Reel GarageFlow OS`  
**Pasta:** `chamados/9001-reel-garageflow-os/`  
**Ideia:** Reel 20–30s mostrando ordem de serviço no app, CTA “agende na oficina”.

### 5.1 Papel (sem MiniMax)

**`/diretor`**

```
/diretor 9001 Reel GarageFlow OS

Brief para Instagram Reels, 20–30s, vertical 9:16, tom direto de oficina.
CTA: agende pelo link. Critérios: hook nos 3s, OS legível, sem jargão de dev.
```

**Confere:** `BRIEF-VIDEO.md` com critérios de aceite.

**`/roteirista`**

```
/roteirista 9001 Reel GarageFlow OS
```

**Confere:** `midia/handoff/roteiro.md` → `Status: ok`.

**`/story`**

```
/story 9001 Reel GarageFlow OS
```

**Confere:** shot list + prompts em `storyboard.md`.

**`/produtor`**

```
/produtor 9001 Reel GarageFlow OS

Monte o pacote MiniMax: VO + clips + (se precisar) imagem de apoio.
Não execute. Liste custos que a câmera vai pedir confirmação.
```

**Confere:** `pacote-minimax.md` com jobs numeradas e capability ids.

### 5.2 Runtime (MiniMax)

**`/camera`**

```
/camera 9001 Reel GarageFlow OS
```

A persona abre o projeto MiniMax, roda as jobs do pacote, **para no custo** e espera seu “sim”.  
**Confere:** `producao.md` com taskIds / resourceIds / paths.

### 5.3 Acabamento

```
/montador 9001 Reel GarageFlow OS
```

```
/critico 9001 Reel GarageFlow OS
```

Se veredito `segue`:

```
/distribuidor 9001 Reel GarageFlow OS
```

**Confere:** `pacote.md` (título + caption). Publique você no Instagram.

---

## 6. Analogia com engenharia

| Engenharia | Mídia |
|------------|--------|
| `/drdestino` → SPEC + PLANO + TASKS | `/diretor` … `/produtor` → brief + roteiro + storyboard + pacote |
| `/ironman` no repo | `/camera` no MiniMax |
| `/visao` / `/viuvanegra` | `/montador` / `/critico` |
| `/mariahill` abre PR | `/distribuidor` só texto — humano publica |

---

## 7. Ligação com negócio

Se o vídeo nasceu de GTM:

1. `/hope` (ou plano) no mesmo ticket → `gtm.md` / `PLANO-NEGOCIO.md`
2. `/diretor …` citando esse arquivo no pedido (leitura opcional **um** path)
3. Cadeia de mídia segue

Não misture critérios de código no `BRIEF-VIDEO.md`.

---

## 8. Regras que quebram a cadeia

- Chamar MiniMax antes do `/camera` (ou fora do `pacote-minimax.md`).
- `/camera` confirmar custo sem o usuário.
- Avançar com `Status` ≠ `ok`.
- Pedir `/montador` sem `producao.md`.
- Esperar que `/distribuidor` poste sozinho.
- Usar Runway / fal / HeyGen / OpenMontage nesta cadeia (v1 = só MiniMax).

---

## 9. Checklist rápido

- [ ] Ticket com número e nome  
- [ ] `BRIEF-VIDEO.md`  
- [ ] `roteiro` → `storyboard` → `pacote-minimax` com `ok`  
- [ ] `/camera` + confirmação de custo  
- [ ] `montagem` → `qa` veredito `segue`  
- [ ] `pacote.md` → publicação humana  

---

## 10. Onde está o quê

| Peça | Path |
|------|------|
| Índice das 3 cadeias | `.cursor/rules/sdd-personas.mdc` |
| Handoff mídia | `.cursor/rules/midia/handoff-midia.mdc` |
| Personas | `.cursor/rules/midia/*.mdc` |
| Agents Cursor | `.cursor/agents/midia/` |
| Skill MiniMax | `.cursor/skills/midia-minimax/SKILL.md` |
| Template | `chamados/_template/BRIEF-VIDEO.md`, `…/midia/handoff/` |
| Este manual | `MANUAL-MIDIA.md` |
