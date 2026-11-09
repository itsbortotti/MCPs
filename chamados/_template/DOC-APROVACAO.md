# <ASSUNTO EM UMA LINHA>

<!-- Obrigatório em todo chamado de engenharia (/drdestino). Texto legível para o
     aprovador antes de codar: regra, ordem dos cards e trechos de referência
     (legado / contrato). Não substitui SPEC/PLANO/TASKS. Nome canónico: DOC-APROVACAO.md.
     Tom/estrutura: DOC-APROVACAO-REPOM.md no chamado DINTCT-1686.
     Copiar de chamados/_template/ ao abrir o chamado; preencher placeholders. -->

**Épico / card:** [<CHAVE> — <título>](<url-jira>)  
**Objetivo deste texto:** explicar o que vamos fazer, a regra de negócio e **os trechos de código de referência**, para aprovar antes de começarmos a codar.

---

## Em uma frase

<!-- Uma frase: o que muda para o usuário/produto, sem jargão de implementação. -->

<frase>

---

## O problema

<!-- Por que isso existe agora; o que falta sem o trabalho. -->

<problema>

---

## O que NÃO muda × o que muda

| Não muda | Muda |
| --- | --- |
| <regra / contrato que permanece> | <onde o código / fluxo muda> |
| | |

---

## Fluxo (visão simples)

```
1. <passo>
2. <passo>
3. <passo>
```

---

## Ordem dos chamados

<!-- Só se houver épico com vários cards. Se for card único, deixe uma linha. -->

| Ordem | Chamado | Em português |
| --- | --- | --- |
| 1 | [<CHAVE>](<url>) | <o quê> |
| 2 | | |

---

## Premissas (precisam do ok)

1. <premissa>
2. <premissa>

---

# Detalhe de cada chamado + trechos de referência

<!-- Repo / pasta de origem dos trechos. -->

Os trechos abaixo são de `<path-legado-ou-contrato>`. É **isso** que vamos reaproveitar / migrar.

---

## 1) <CHAVE> — <título curto>

### Para que serve

<uma ou duas frases>

### Regra

> <regra em uma linha>

#### Trecho — <nome do trecho>

Arquivo: `<path-relativo>`

```typescript
// trecho real, enxuto — sem inventar comportamento
```

---

## Fora do escopo

- <item>
- <item>

---

## Ambiente

<!-- URLs, cofres, secrets por *nome* (não colar senha no chat público).
     Credenciais de QA: se necessário no doc interno, apontar também segredos-locais.md. -->

- Host:
- Token / auth:
- Segredo (nome + cofre):
- Help / swagger:

---

## Checklist de aprovação

- [ ] Ordem / card inicial
- [ ] Premissas
- [ ] Regras e trechos de referência
- [ ] Fora de escopo
- [ ] Ambiente ok para validar depois

**Pedido:** confirme o que está ok e o que precisa ajustar. Com o ok, partimos para o primeiro card / implementação.
