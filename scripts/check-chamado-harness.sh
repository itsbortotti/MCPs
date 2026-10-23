#!/usr/bin/env bash
# Gate de estrutura / prontidão de PR para um chamado SDD.
# Uso:
#   ./scripts/check-chamado-harness.sh [--before-pr] <pasta-ou-NUMERO-slug>
# Exit 0 = ok; ≠ 0 = falha (mensagens em stderr).

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BEFORE_PR=0
TARGET=""

usage() {
  cat <<'EOF' >&2
Uso: ./scripts/check-chamado-harness.sh [--before-pr] <pasta-ou-NUMERO-slug>

  (padrão)     exige SPEC.md, PLANO-IMPLEMENTACAO.md e TASKS.md
  --before-pr  + prova.md com Status: ok; + paridade Status: ok se superfície
               dupla for indicada no SPEC/PLANO/TASKS, ou se paridade.md
               tiver Status diferente de pendente

Exemplos:
  ./scripts/check-chamado-harness.sh chamados/_template
  ./scripts/check-chamado-harness.sh --before-pr 1234-busca-estabelecimentos
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --before-pr) BEFORE_PR=1; shift ;;
    -h|--help) usage; exit 0 ;;
    -*)
      echo "flag desconhecida: $1" >&2
      usage
      exit 2
      ;;
    *)
      if [[ -n "$TARGET" ]]; then
        echo "apenas um alvo permitido" >&2
        usage
        exit 2
      fi
      TARGET="$1"
      shift
      ;;
  esac
done

if [[ -z "$TARGET" ]]; then
  usage
  exit 2
fi

resolve_dir() {
  local t="$1"
  if [[ -d "$t" ]]; then
    cd "$t" && pwd
    return
  fi
  if [[ -d "$ROOT/$t" ]]; then
    cd "$ROOT/$t" && pwd
    return
  fi
  if [[ -d "$ROOT/chamados/$t" ]]; then
    cd "$ROOT/chamados/$t" && pwd
    return
  fi
  echo "pasta do chamado não encontrada: $t" >&2
  exit 2
}

DIR="$(resolve_dir "$TARGET")"
FAILS=0

fail() {
  echo "FAIL: $*" >&2
  FAILS=$((FAILS + 1))
}

ok() {
  echo "OK: $*"
}

# Status: na primeira linha útil após o título (ou qualquer linha Status: no topo)
get_status() {
  local f="$1"
  if [[ ! -f "$f" ]]; then
    echo ""
    return
  fi
  # Primeira ocorrência de linha que começa com Status:
  grep -E '^Status:[[:space:]]*' "$f" | head -n1 | sed -E 's/^Status:[[:space:]]*//' | awk '{print tolower($1)}' | tr -d '\r'
}

# Remove comentários HTML de linha (placeholders do _template) para não falso-positivo
strip_html_comments() {
  sed -E 's/<!--.*-->//g'
}

has_dual_surface() {
  local hay=""
  local f body
  for f in "$DIR/SPEC.md" "$DIR/PLANO-IMPLEMENTACAO.md" "$DIR/TASKS.md"; do
    [[ -f "$f" ]] || continue
    body="$(strip_html_comments <"$f" | tr '[:upper:]' '[:lower:]')"
    hay+=" $body"
  done
  # Indicadores explícitos (fora de comentário)
  if echo "$hay" | grep -Eq 'web\+mobile|web↔mobile|web<->mobile|superfície dupla|superficie dupla|paridade (web|mobile)|web e mobile|web[[:space:]]*\+[[:space:]]*mobile'; then
    return 0
  fi
  # Seção Superfícies: valor real (não só n/a)
  local block
  block="$(
    for f in "$DIR/SPEC.md" "$DIR/PLANO-IMPLEMENTACAO.md"; do
      [[ -f "$f" ]] || continue
      strip_html_comments <"$f" | awk '
        BEGIN{IGNORECASE=1}
        /^##[[:space:]]*Superf/ {p=1; next}
        p && /^##[[:space:]]/ {exit}
        p {print}
      '
    done | tr '[:upper:]' '[:lower:]'
  )"
  # linhas úteis sem n/a isolado
  if echo "$block" | grep -Eq '[[:alnum:]]' \
    && echo "$block" | grep -Eq 'web|mobile|ios|android|flutter' \
    && ! echo "$block" | grep -Eq '^[[:space:]]*n/?a[[:space:]]*$'; then
    # se a seção só tem "n/a" em alguma linha e nada mais forte, ignore
    if echo "$block" | grep -Eq 'web\+mobile|web e mobile|flutter|ios|android|mobile'; then
      # "n/a" sozinho em todas as linhas de conteúdo → não dual
      local meaningful
      meaningful="$(echo "$block" | grep -Ev '^[[:space:]]*(n/?a|—|-)?[[:space:]]*$' || true)"
      if [[ -n "$meaningful" ]] && echo "$meaningful" | grep -Eq 'web|mobile|ios|android|flutter'; then
        return 0
      fi
    fi
  fi
  return 1
}

echo "check-chamado-harness: $DIR"
[[ "$BEFORE_PR" -eq 1 ]] && echo "modo: --before-pr" || echo "modo: estrutura"

for req in SPEC.md PLANO-IMPLEMENTACAO.md TASKS.md; do
  if [[ -f "$DIR/$req" ]]; then
    ok "$req"
  else
    fail "falta $req"
  fi
done

if [[ "$BEFORE_PR" -eq 1 ]]; then
  PROVA="$DIR/sdd/handoff/prova.md"
  if [[ ! -f "$PROVA" ]]; then
    fail "falta sdd/handoff/prova.md (rode /viuvanegra)"
  else
    st="$(get_status "$PROVA")"
    if [[ "$st" == "ok" ]]; then
      ok "prova.md Status: ok"
    else
      fail "prova.md Status deve ser ok (achado: '${st:-<vazio>}')"
    fi
  fi

  PARIDADE="$DIR/sdd/handoff/paridade.md"
  NEED_PAR=0
  if has_dual_surface; then
    NEED_PAR=1
    echo "info: superfície dupla indicada em SPEC/PLANO/TASKS"
  fi
  if [[ -f "$PARIDADE" ]]; then
    pst="$(get_status "$PARIDADE")"
    if [[ -n "$pst" && "$pst" != "pendente" ]]; then
      NEED_PAR=1
      echo "info: paridade.md com Status=$pst (não é stub pendente)"
    fi
  fi

  if [[ "$NEED_PAR" -eq 1 ]]; then
    if [[ ! -f "$PARIDADE" ]]; then
      fail "superfície dupla / paridade exigida: falta sdd/handoff/paridade.md (rode /falcao)"
    else
      pst="$(get_status "$PARIDADE")"
      if [[ "$pst" == "ok" ]]; then
        ok "paridade.md Status: ok"
      else
        fail "paridade.md Status deve ser ok (achado: '${pst:-<vazio>}') — peça /falcao"
      fi
    fi
  else
    ok "paridade não exigida (sem superfície dupla; stub pendente ok)"
  fi
fi

if [[ "$FAILS" -gt 0 ]]; then
  echo "resultado: $FAILS falha(s)" >&2
  exit 1
fi
echo "resultado: ok"
exit 0
