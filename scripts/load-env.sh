#!/usr/bin/env bash
# Carrega MCPs/.env no shell atual (exporta variáveis).
# Uso:  source "$(dirname "$0")/load-env.sh"
#   ou: source /caminho/para/MCPs/scripts/load-env.sh
#
# Não imprime valores. Idempotente se chamado mais de uma vez.

_mcps_load_env() {
  local root env_file
  root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
  env_file="${root}/.env"

  if [[ ! -f "${env_file}" ]]; then
    echo "load-env: ${env_file} não encontrado (copie .env.example → .env)" >&2
    return 1
  fi

  set -a
  # shellcheck disable=SC1090
  source "${env_file}"
  set +a
  return 0
}

_mcps_load_env
unset -f _mcps_load_env
