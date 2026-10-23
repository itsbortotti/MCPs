#!/usr/bin/env bash
# Roda um comando com MCPs/.env já exportado (STRIX_LLM, LLM_API_KEY, etc.).
# Uso:  ./scripts/with-env.sh <comando> [args...]
# Ex.:  ./scripts/with-env.sh strix --help
#       ./scripts/with-env.sh env | grep -E '^(STRIX_LLM|LLM_API_KEY|OPENAI_API_KEY)='
#
# Não imprime segredos. Exit code do comando filho é preservado.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck disable=SC1091
source "${ROOT}/scripts/load-env.sh"

if [[ $# -lt 1 ]]; then
  echo "uso: $0 <comando> [args...]" >&2
  exit 2
fi

exec "$@"
