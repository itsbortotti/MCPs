#!/usr/bin/env bash
# Roda o Strix com CWD = pasta do chamado, para o CLI gravar ./strix_runs/ lá
# (não na raiz do MCPs). Carrega .env via with-env.
#
# Uso:
#   ./scripts/strix-in-chamado.sh <pasta-ou-NUMERO-slug> -- <args do strix>
# Ex.:
#   ./scripts/strix-in-chamado.sh "DINTCT-1629 - NDD vale pedagio VPO" -- \
#     -n -t /tmp/dintct-1629-vp-diff --scan-mode quick --max-budget 10

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

usage() {
  cat <<'EOF' >&2
Uso: ./scripts/strix-in-chamado.sh <pasta-ou-NUMERO-slug> -- <args do strix>

O Strix sempre escreve em ./strix_runs/ relativo ao CWD. Este script entra na
pasta do chamado, cria strix_runs/ se faltar, e executa o CLI com o .env carregado.

Exemplos:
  ./scripts/strix-in-chamado.sh chamados/_template -- strix --help
  ./scripts/strix-in-chamado.sh 1234-busca -- -n -t /tmp/diff --scan-mode quick
EOF
}

if [[ $# -lt 1 ]]; then
  usage
  exit 2
fi

TARGET="$1"
shift

if [[ "${1:-}" == "--" ]]; then
  shift
fi

if [[ $# -lt 1 ]]; then
  echo "faltam args do strix (depois de --)" >&2
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
mkdir -p "${DIR}/strix_runs"

# Se o primeiro arg for "strix", remove (aceita ambos os estilos).
if [[ "$1" == "strix" ]]; then
  shift
fi

cd "$DIR"
exec "${ROOT}/scripts/with-env.sh" strix "$@"
