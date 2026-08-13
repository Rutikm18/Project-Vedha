#!/usr/bin/env bash
# UC5 — Database Exposure (probe use_case: uc_db_exposure)
# Protocol-handshake fingerprint of DB ports. Finds exposed / unauthenticated
# databases (Redis no-auth, Mongo no-auth, MySQL/Postgres/MSSQL/Oracle reachable).
#
#   ./uc_db_exposure.sh 192.168.1.10
set -u
. "$(dirname "$0")/_uc_lib.sh"
uc_init "${1:-}"

uc_run "Database fingerprint" db_scanner -p "$UC_DB_PORTS"
"$PY" - "$UC_LAST" <<'PY'
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
if not rows: print("   (no database ports responded)"); raise SystemExit
for r in sorted(rows, key=lambda x: x.get("port") or 0):
    d = r.get("data") or {}
    flag = ""
    if d.get("unauth") or d.get("no_auth") or d.get("unauthenticated"):
        flag = "  *** UNAUTHENTICATED ACCESS ***"
    print(f"   port {str(r.get('port')):<6} {r.get('status'):<8} {r.get('evidence')}{flag}")
    if d: print(f"      {d}")
PY
echo
