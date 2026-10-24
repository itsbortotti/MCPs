---
name: midia-minimax
description: >-
  Protocolo MiniMax Design para a persona /camera da cadeia midia. Use ao
  executar pacote-minimax.md: projetos, capabilities, execute, task_wait,
  confirm_cost e get_output.
---

# Mídia — protocolo MiniMax

Só a persona **`/camera`** usa esta skill para gerar. As demais preparam artefatos.

Namespace MCP: `user-minimax-design`.

## Fluxo obrigatório

1. Ler `midia/handoff/pacote-minimax.md` com `Status: ok`.
2. `list_projects` → escolher ou criar contexto → `open_project` com `projectId` e descrição curta da tarefa.
3. Para cada job do pacote (ordem + `depends_on`):
   - Se o capability id não estiver claro: `capability_list` / `capability_get`.
   - `execute` com os params do pacote.
   - `task_wait` com o mesmo `taskId` até settle. **Não** resubmeter enquanto espera.
4. Se a resposta trouxer `waiting_user` / confirmação de custo:
   - Mostrar o valor ao usuário.
   - Só chamar `confirm_cost` após **sim** / **go** explícito.
   - Se recusar: `task_resolve` com stop (ou equivalente) e gravar `Status: bloqueado` em `producao.md`.
5. Coletar saídas com `get_output` / `deliver` conforme a API.
6. Escrever `midia/handoff/producao.md` (projectId, taskIds, resourceIds, paths/URLs, custos). Sem log bruto.

## Defaults (salvo o pacote pedir outro)

| Uso | Capability típico |
| --- | --- |
| Vídeo curto geral | `generate_video:MiniMax-H3` |
| Drama / multi-shot (só se pedido) | `generate_video:seedance2.5` |
| Narração | `generate_speech:seed-audio-1.0` |
| Música instrumental | `generate_music:music-3.0` ou ElevenLabs Music se o pacote citar |
| Imagem de apoio | default de imagem da sessão (`capability_list`) |

## Proibições

- Confirmar custo sem o usuário.
- Gerar job que não está no `pacote-minimax.md`.
- Usar outro provider (Runway, fal, HeyGen) nesta cadeia.
- Deixar a `/camera` fazer papel de `/montador` ou `/critico`.
