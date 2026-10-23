# Plano — busca de estabelecimentos no Brasil

- Card: não há número original. Migrado para `chamados/001-migrado-busca-estabelecimentos/` (sem ticket formal). Pedido nesta conversa: a busca é um recurso genérico, para qualquer sistema. No GarageFlow ela entra como aba nova do Painel Master.
- Repo do plano: MCPs. Este arquivo fica na pasta do chamado e viaja com as personas. Não copiar o plano para cada produto.
- Hospedeiro desta passagem: GarageFlow, branch atual `main`. Branch de trabalho ainda não existe. O Iron Man abre `feat/busca-estabelecimentos` a partir de `main` e não commita em `main`.
- Lacuna: outro sistema não tem path neste plano. O Iron Man só implementa o núcleo e a tela nova. A gravação dos escolhidos espera o encaixe daquele repo, preenchido no formato da etapa 5.

## Objetivo

Qualquer sistema ganha uma tela própria de busca. A pessoa informa cidade, UF e uma categoria fechada. O sistema consulta o mapa público só no Brasil, mostra os estabelecimentos e devolve os marcados para o hospedeiro gravar onde ele já grava gente. A busca não envia mensagem.

No GarageFlow essa tela é uma aba nova do Painel Master, ao lado do CRM. Ela não entra dentro do funil.

## O que o recurso é

Três peças, iguais em todo sistema. O hospedeiro não reescreve a consulta ao mapa.

1. **Função.** Recebe cidade, UF e categoria. Devolve no máximo 40 estabelecimentos, já normalizados.
2. **Tela nova.** Formulário, lista, vazio, erro e confirmação. Não é diálogo dentro de outra tela.
3. **Encaixe.** O hospedeiro diz quem pode abrir a tela e o que acontece ao confirmar. A função de busca não conhece lead, cliente, aluno nem tenant.

O mapa é o Nominatim e o Overpass. Não se importa o Harvey nem se usa fonte paga.

## Contrato

Validado na borda. Dali para dentro só estes tipos. Nenhum campo é dicionário livre.

`Uf`: `AC` `AL` `AP` `AM` `BA` `CE` `DF` `ES` `GO` `MA` `MT` `MS` `MG` `PA` `PB` `PR` `PE` `PI` `RJ` `RN` `RS` `RO` `RR` `SC` `SP` `SE` `TO`.

`CategoriaEstabelecimento` e a tag OSM (a tela não envia a tag):

| Valor | Rótulo | Tag |
| --- | --- | --- |
| `oficina` | Oficina mecânica | `shop=car_repair` |
| `autopecas` | Autopeças | `shop=car_parts` |
| `borracharia` | Borracharia | `shop=tyres` |
| `lava_jato` | Lava-jato | `shop=car_wash` |
| `posto` | Posto de combustível | `amenity=fuel` |
| `academia` | Academia | `leisure=fitness_centre` |
| `clinica` | Clínica | `amenity=clinic` |
| `farmacia` | Farmácia | `amenity=pharmacy` |
| `restaurante` | Restaurante | `amenity=restaurant` |
| `escritorio` | Escritório | `office=company` |

O hospedeiro pode mostrar um subconjunto. Não pode acrescentar valor fora da tabela.

`BuscaPedido`: `cidade` (texto, 2 a 80), `uf` (`Uf`), `categoria` (`CategoriaEstabelecimento`).

`Endereco`: `logradouro`, `numero`, `bairro`, `cep` (8 dígitos ou nulo), `cidade` (texto), `uf` (`Uf`).

`Estabelecimento`: `osm_tipo` (`node` | `way` | `relation`), `osm_id` (inteiro positivo), `nome` (texto), `telefone` (só dígitos ou nulo), `site` (texto ou nulo), `endereco` (`Endereco`).

`BuscaResposta`: `itens` (lista de `Estabelecimento`), `truncado` (booleano).

`ConfirmacaoPedido`: `itens` (lista de `Estabelecimento`, de 1 a 40). O hospedeiro pode acrescentar um campo de destino já existente nele (no GarageFlow, `stage_id`). Esse campo não entra no núcleo.

`ConfirmacaoResposta`: `criados` (lista de ids do registro do hospedeiro), `ignorados` (lista de textos `osm_tipo/osm_id`).

Chave estável de um estabelecimento: `"{osm_tipo}/{osm_id}"`. O hospedeiro guarda essa chave no registro que ele já tem. Não se cria tabela de mapa.

## Regras da busca

- Geocode em `https://nominatim.openstreetmap.org/search` com `q` = `"{cidade}, {uf}, Brasil"`, `countrycodes=br`, `format=jsonv2`, `limit=1`, `addressdetails=1`. Sem resultado naquela UF, o erro é "Não encontrei essa cidade neste estado." e o Overpass não é chamado.
- Overpass em `https://overpass-api.de/api/interpreter`, só a tag da categoria. Área: a bounding box do Nominatim. Se o lado maior passar de 25 km, raio de 12 km a partir do centro.
- Nome: `name` ou `name:pt`. Sem nome, o item sai da lista.
- Telefone: `phone` ou `contact:phone`, o primeiro número. Só dígitos. Com 10 ou 11, prefixa `55`. Com 12 ou 13 começando em `55`, mantém. Fora isso, telefone nulo e o item continua.
- Site: `website` ou `contact:website`.
- Endereço: `addr:street`, `addr:housenumber`, `addr:suburb`, `addr:postcode`.
- Teto de 40. Acima disso, `truncado` verdadeiro.
- User-Agent: `"{nome do sistema}-busca/1.0"`. Um pedido de mapa por vez, timeout de 25 s. Sem chave e sem variável de ambiente nova.

## Tela

A busca é uma área nova do sistema, com nome visível "Buscar clientes". Não é botão dentro de uma lista que já existe.

Campos: cidade, UF (27 siglas), categoria (rótulos da tabela), botão "Buscar".

Lista, por item: nome, telefone formatado ou "Sem telefone", cidade/UF, site ou "Sem site", e um marcado. Item que o hospedeiro já guardou aparece desmarcado e não pode ser marcado de novo.

Textos que a pessoa vê:

- Buscando: "Buscando estabelecimentos…"
- Vazio: "Nenhum estabelecimento encontrado nesta cidade para esta categoria."
- Cidade: "Não encontrei essa cidade neste estado."
- Mapa: "A consulta ao mapa falhou. Tente de novo."
- Nada marcado: "Marque ao menos um estabelecimento."
- Antes de confirmar: "A busca não envia mensagem. Ao confirmar, os escolhidos são gravados neste sistema."

Quem não tem permissão de usar a busca não vê a área.

## Critérios de aceite do núcleo

- Categoria fora da tabela responde 422. O pedido não aceita tag OSM.
- Cidade inválida não chama o Overpass e a tela mostra o texto de cidade.
- Lista vazia mostra o texto de vazio. Falha de rede mostra o texto de mapa.
- Oficina em cidade válida só devolve `shop=car_repair`.
- Confirmar sem marcado não grava.
- A mesma chave `osm_tipo/osm_id` não gera dois registros. A segunda vez entra em `ignorados`.
- Nenhum pedido da busca envia WhatsApp, e-mail ou outra mensagem.

## Etapas do núcleo

Modo de pasta: o do hospedeiro, um só. No GarageFlow é fatia por assunto. Noutro repo, o modo que a rule daquele repo marcar. Se a rule não marcar, fatia por assunto.

### 1. Função

Arquivo novo na pasta do fluxo, não num utilitário genérico. Nome: `busca_estabelecimentos`.

`buscar(pedido: BuscaPedido, nome_sistema: str) -> BuscaResposta`, com as regras acima. `nome_sistema` só entra no User-Agent.

Critério: os critérios de aceite do núcleo, menos a gravação.

### 2. Tela nova

Depende da etapa 1. Peça nova na pasta de telas do fluxo. A tela chama a função e, ao confirmar, chama o encaixe do hospedeiro. Não coloca a lista dentro de uma tela que já lista outra coisa.

Critério: os textos da seção Tela, na rota que o encaixe nomear.

### 3. Encaixe do hospedeiro

Depende da etapa 2. O hospedeiro implementa `gravar(pedido: ConfirmacaoPedido) -> ConfirmacaoResposta` em cima do criar-registro que ele já tem. A chave estável fica num campo que esse registro já aceite. Quem já tem a chave volta em `ignorados`.

Se o criar-registro desse sistema dispara mensagem, a frase de confirmação ganha uma segunda linha dizendo isso. A busca em si continua sem enviar.

Critério: duas confirmações da mesma chave criam um registro só.

## Encaixe GarageFlow

Esta é a passagem atual. A aba é nova. O funil não muda.

Situação que o código já mostra:

- Web: uma rota só, `/master`, em `frontend/src/App.jsx`. As seções são abas de `frontend/src/features/master/pages/MasterPanel.jsx`. CRM é `activeTab === 'crm'`, botão "CRM" no menu lateral (`MasterSidebarNavButton`, por volta da linha 4329). O funil é `MasterCrmKanban.jsx`.
- Criar lead: `POST /master/crm/leads`, `crm_lead_create` em `backend/app/features/crm/controllers/crm_master_router.py`. O corpo está em `CrmLeadCreateBody` (`backend/app/schemas.py`). `source` gravado é o usuário do Master (`_crm_manual_lead_source`), não o `source` do corpo. Depois chama `trigger_crm_ai_for_lead`. O agente só age se a coluna estiver na configuração dele.
- Mobile: o menu do Master está em `mobile/lib/features/master/screens/master_screens.dart`. CRM é a rota `/master/crm` em `mobile/lib/app.dart` (`_MasterCrmScreen`, só lista). A rule `garageflow.mdc` pede a mesma aba no app.

O que entra:

- Aba web `busca`, rótulo "Buscar clientes", no menu lateral depois de "CRM", visível com `see_crm`. `MasterPanel.jsx` só ganha o botão, o `activeTab` e a renderização da peça nova. A peça é `frontend/src/features/master/components/MasterCrmBuscaClientes.jsx`. Layout da aba: o mesmo de `crm-ai` (`gf-master-page-inner--list`).
- API nova, sem mexer em `crm_master_router.py` nem em `schemas.py`. Contrato em `backend/app/features/crm/controllers/crm_busca_contrato.py`. Rotas em `backend/app/features/crm/controllers/crm_busca_router.py`, montadas no `master_app` de `backend/app/main.py` com prefixo `/crm`: `POST /master/crm/busca-clientes` (`see_crm`) e `POST /master/crm/busca-clientes/confirmar` (`edit_crm`).
- Função em `backend/app/features/crm/services/busca_estabelecimentos.py`, com `nome_sistema` `GarageFlow`.
- Confirmar chama `crm_lead_create` com `name`, `phone`, `stage_id` (a coluna que a pessoa escolhe na aba) e `extra.busca_osm_id`, `extra.busca_categoria`, `extra.busca_site`, `extra.busca_cidade`, `extra.busca_uf`. E-mail nulo. `source` continua o usuário do Master.
- A frase de confirmação nesta aba tem a segunda linha: "Se a coluna escolhida dispara o agente de IA, a cadência de WhatsApp ou e-mail pode começar."
- Mobile: rota `/master/busca` em `mobile/lib/app.dart` e item "Buscar clientes" no menu, depois de CRM. Tela `mobile/lib/features/master/screens/master_busca_clientes_screen.dart`. Model `mobile/lib/features/master/models/estabelecimento_busca.dart`. Os dois métodos HTTP entram em `MasterRepository`, que já está em `master_screens.dart`.

Critério desta aba: em `/master`, o menu mostra "Buscar clientes". A aba abre com os campos e, sem busca, sem lista. Os textos da seção Tela aparecem. Um estabelecimento confirmado surge no funil, na coluna escolhida, com `extra.busca_osm_id`. No app, o menu do Master abre a mesma busca em `/master/busca`.

## Fora de escopo

- Harvey, DataForSEO, CNPJ, Receita Federal e visita ao site para marcar "sem site".
- Mensagem nova. No GarageFlow, o único disparo é o que `crm_lead_create` já faz.
- Alterar o funil, `_crm_manual_lead_source`, as colunas ou o agente de IA.
- Partir `MasterPanel.jsx`, `MasterCrmKanban.jsx`, `schemas.py` ou `master_screens.dart`.
- Implementar outro produto nesta passagem.

## Checklist

1. Função de busca, igual para qualquer sistema, com os tipos do contrato.
2. Tela nova, com os textos fixos, fora da lista que o sistema já tinha.
3. Encaixe: gravar pela função de criar que o sistema já tem, deduplicando pela chave do mapa.
4. GarageFlow: aba "Buscar clientes" no Painel Master, web e mobile, gravando lead na coluna escolhida.

## Definição de pronto

No GarageFlow, a aba nova cumpre o critério do encaixe, na branch `feat/busca-estabelecimentos`. O núcleo permanece o deste arquivo, para o próximo sistema repetir a função e a tela e só trocar o `gravar`.
