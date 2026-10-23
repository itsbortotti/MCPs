#!/usr/bin/env bash
# Smoke do harness SDD: estrutura do template + gate --before-pr.
# Dependência: bash + grep/sed/awk (stdlib do check-chamado-harness.sh).
# Uso (raiz do MCPs): ./scripts/eval-harness-smoke.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHECK="$ROOT/scripts/check-chamado-harness.sh"
TS="$(date +%Y%m%d%H%M%S)"
TMPDIR_EVAL="$(mktemp -d "${TMPDIR:-/tmp}/mcps-harness-eval.XXXXXX")"
# Também cria um dir ignorado no repo para provar o padrão _eval-*
REPO_EVAL="$ROOT/chamados/_eval-smoke-$TS"
CLEANED=0

cleanup() {
  if [[ "$CLEANED" -eq 1 ]]; then
    return
  fi
  CLEANED=1
  rm -rf "$TMPDIR_EVAL"
  rm -rf "$REPO_EVAL"
}
trap cleanup EXIT

echo "== eval-harness-smoke =="
echo "ROOT=$ROOT"

if [[ ! -x "$CHECK" ]]; then
  chmod +x "$CHECK"
fi

TEMPLATE="$ROOT/chamados/_template"
if [[ ! -d "$TEMPLATE" ]]; then
  echo "FAIL: falta chamados/_template" >&2
  exit 1
fi

echo "-- 1) estrutura no _template deve passar"
"$CHECK" "$TEMPLATE"

echo "-- 2) --before-pr no _template deve falhar (prova pendente)"
set +e
"$CHECK" --before-pr "$TEMPLATE"
rc=$?
set -e
if [[ "$rc" -eq 0 ]]; then
  echo "FAIL: esperava falha --before-pr no template (prova pendente)" >&2
  exit 1
fi
echo "OK: --before-pr falhou como esperado (rc=$rc)"

echo "-- 3) cópia temp com prova ok (sem superfície dupla) deve passar --before-pr"
cp -R "$TEMPLATE" "$TMPDIR_EVAL/chamado"
# Garante Superfícies = n/a e prova ok; paridade fica pendente (não exige)
cat >"$TMPDIR_EVAL/chamado/SPEC.md" <<'EOF'
# Spec — eval smoke

- Ticket: 0

## O quê / porquê

smoke

## Não-objetivos

## Critérios de aceite

- harness passa

## Superfícies

n/a
EOF

cat >"$TMPDIR_EVAL/chamado/PLANO-IMPLEMENTACAO.md" <<'EOF'
# Plano — eval smoke

- Ticket: 0
- Spec: SPEC.md
- Tasks: TASKS.md

## Objetivo

smoke

## Como no repo (arquitetura)

n/a

## Situação atual

## Decisões

## Etapas

## Superfícies

n/a

## Fora de escopo

## Checklist

## Definição de pronto
EOF

# TASKS já existe na cópia
sed -i.bak 's/^Status: pendente/Status: ok/' "$TMPDIR_EVAL/chamado/sdd/handoff/prova.md"
rm -f "$TMPDIR_EVAL/chamado/sdd/handoff/prova.md.bak"

"$CHECK" --before-pr "$TMPDIR_EVAL/chamado"
echo "OK: temp com prova ok passou --before-pr"

echo "-- 4) com superfície dupla e paridade pendente deve falhar"
cp -R "$TEMPLATE" "$TMPDIR_EVAL/dual"
cat >"$TMPDIR_EVAL/dual/SPEC.md" <<'EOF'
# Spec — dual

- Ticket: 0

## Critérios de aceite

- x

## Superfícies

web+mobile
EOF
sed -i.bak 's/^Status: pendente/Status: ok/' "$TMPDIR_EVAL/dual/sdd/handoff/prova.md"
rm -f "$TMPDIR_EVAL/dual/sdd/handoff/prova.md.bak"
# paridade permanece pendente
set +e
"$CHECK" --before-pr "$TMPDIR_EVAL/dual"
rc=$?
set -e
if [[ "$rc" -eq 0 ]]; then
  echo "FAIL: esperava falha com web+mobile e paridade pendente" >&2
  exit 1
fi
echo "OK: dual sem paridade ok falhou como esperado"

echo "-- 5) dual + prova ok + paridade ok deve passar"
sed -i.bak 's/^Status: pendente/Status: ok/' "$TMPDIR_EVAL/dual/sdd/handoff/paridade.md"
rm -f "$TMPDIR_EVAL/dual/sdd/handoff/paridade.md.bak"
"$CHECK" --before-pr "$TMPDIR_EVAL/dual"
echo "OK: dual completo passou"

echo "-- 6) padrão chamados/_eval-* (cria e remove)"
mkdir -p "$REPO_EVAL"
echo "probe" >"$REPO_EVAL/.probe"
[[ -d "$REPO_EVAL" ]] || { echo "FAIL: não criou $REPO_EVAL" >&2; exit 1; }
rm -rf "$REPO_EVAL"
echo "OK: cleanup _eval-smoke"

echo "== eval-harness-smoke: verde =="
