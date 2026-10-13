#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${ROOT}/mcp.json"
DEST="${HOME}/.cursor/mcp.json"
ENV_FILE="${ROOT}/.env"

mkdir -p "${HOME}/.cursor"

if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  set -a
  # shellcheck disable=SC1091
  source "${ENV_FILE}"
  set +a
fi

python3 - <<'PY' "${SRC}" "${DEST}"
import json, os, re, sys
src, dest = sys.argv[1], sys.argv[2]
template = json.load(open(src, encoding="utf-8"))
current = {"mcpServers": {}}
if os.path.exists(dest):
    current = json.load(open(dest, encoding="utf-8"))
    current.setdefault("mcpServers", {})

placeholder = re.compile(r"\$\{([A-Z0-9_]+)\}")

def resolve(value):
    if isinstance(value, str):
        def repl(m):
            val = os.environ.get(m.group(1))
            if val is None or val == "":
                return m.group(0)
            return val
        return placeholder.sub(repl, value)
    if isinstance(value, list):
        return [resolve(item) for item in value]
    if isinstance(value, dict):
        return {key: resolve(item) for key, item in value.items()}
    return value

retired = ["azure-full", "n8n-instance-http"]
removed = []
for name in retired:
    if name in current["mcpServers"]:
        del current["mcpServers"][name]
        removed.append(name)

kept = []
updated = []
for name, config in template.get("mcpServers", {}).items():
    rendered = resolve(config)
    raw = json.dumps(rendered)
    if placeholder.search(raw) and name in current["mcpServers"]:
        kept.append(name)
        continue
    current["mcpServers"][name] = rendered
    updated.append(name)

open(dest, "w", encoding="utf-8").write(json.dumps(current, indent=2) + "\n")
print(f"Merged: {src} -> {dest}")
print("Updated: " + (", ".join(updated) if updated else "(none)"))
if removed:
    print("Removed: " + ", ".join(removed))
if kept:
    print("Kept existing (missing .env value): " + ", ".join(kept))
print("Plugin servers outside mcp.json were left in place.")
print("Reload Cursor (Cmd+Shift+P → Reload Window) to pick up MCP servers.")
PY
