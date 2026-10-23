#!/usr/bin/env bash
# Confere se as vars do Strix estão disponíveis após carregar o .env.
# Uso: ./scripts/strix-env-check.sh
# Saída: só SET/UNSET (nunca o valor).

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck disable=SC1091
source "${ROOT}/scripts/load-env.sh"

ok=0
for name in STRIX_LLM LLM_API_KEY OPENAI_API_KEY; do
  if [[ -n "${!name:-}" ]]; then
    echo "${name}=SET"
  else
    echo "${name}=UNSET"
    # LLM_API_KEY ou OPENAI_API_KEY: basta um dos dois
    if [[ "${name}" == "STRIX_LLM" ]]; then
      ok=1
    fi
  fi
done

if [[ -z "${LLM_API_KEY:-}" && -z "${OPENAI_API_KEY:-}" ]]; then
  echo "strix-env-check: falta LLM_API_KEY ou OPENAI_API_KEY no .env" >&2
  exit 1
fi

if [[ -z "${STRIX_LLM:-}" ]]; then
  echo "strix-env-check: falta STRIX_LLM no .env" >&2
  exit 1
fi

echo "strix-env-check: ok (vars carregadas do .env)"
exit 0
