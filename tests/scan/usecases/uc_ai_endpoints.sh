#!/usr/bin/env bash
# UC10 — AI / MCP Endpoint Sweep (probe use_case: uc_ai_endpoint_sweep)
# Discover exposed AI inference endpoints and MCP servers (Ollama 11434,
# text-gen 7860, LM Studio 1234, generic 8000/5000/3000...). Unauth AI = finding.
#
#   ./uc_ai_endpoints.sh 192.168.1.10
set -u
. "$(dirname "$0")/_uc_lib.sh"
uc_init "${1:-}"

uc_run "AI/MCP endpoint discovery" mcp_ai_scanner -p "$UC_AI_PORTS"
"$PY" - "$UC_LAST" <<'PY'
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
if not rows: print("   (no AI/MCP endpoints responded)"); raise SystemExit
for r in sorted(rows, key=lambda x: x.get("port") or 0):
    d = r.get("data") or {}
    print(f"   port {str(r.get('port')):<6} {r.get('status'):<8} {r.get('evidence')}")
    for k in ("service", "model", "models", "framework", "unauth"):
        if k in d: print(f"      {k}: {d[k]}")
PY
echo
