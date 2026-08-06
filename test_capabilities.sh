#!/usr/bin/env sh
# =============================================================================
# Vedha probe — standalone CAPABILITY self-test (no manager required)
#
# Runs the probe's scanners directly against a target and reports which of the
# advertised capabilities actually produced facts. This is the fastest way to
# prove the probe works, independent of the manager/agent transport.
#
#   sh probe/test_capabilities.sh                 # scan this host (127.0.0.1)
#   sh probe/test_capabilities.sh 192.168.1.10    # scan one target
#   sh probe/test_capabilities.sh 192.168.1.0/24  # scan a CIDR
#   MODE=triage sh probe/test_capabilities.sh     # lighter/faster mode
#
# Only scan hosts you are authorized to test.
# =============================================================================
set -eu

HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$HERE"

TARGET="${1:-${TARGET:-127.0.0.1}}"
MODE="${MODE:-assessment}"            # triage | assessment | service-specific | re-scan
PROFILE="${PROFILE:-it}"             # it | iot | ot
OUT="${OUT:-/tmp/vedha-probe-captest.json}"

SCOPE_FILE="$(mktemp)"
trap 'rm -f "$SCOPE_FILE"' EXIT

# Derive an authorizing scope that contains the target.
case "$TARGET" in
  127.*)  echo "127.0.0.0/8"        > "$SCOPE_FILE" ;;   # loopback
  */*)    echo "$TARGET"            > "$SCOPE_FILE" ;;   # a CIDR is its own scope
  *)      echo "${TARGET%.*}.0/24"  > "$SCOPE_FILE" ;;   # single IP -> its /24
esac

echo "=============================================================="
echo " Vedha probe — capability self-test"
echo "   target : $TARGET"
echo "   mode   : $MODE    profile: $PROFILE"
echo "   scope  : $(cat "$SCOPE_FILE")"
echo "=============================================================="

# --- 0) Python venv (core scanners are stdlib; venv covers transport imports) -
PY="$HERE/.venv/bin/python"
if [ ! -x "$PY" ]; then
  echo "[setup] creating probe venv (first run only) ..."
  python3 -m venv .venv
  ./.venv/bin/pip install -q -U pip
  ./.venv/bin/pip install -q -r requirements.txt \
    || echo "[warn] some optional deps failed to install; stdlib scanners still work"
fi

# --- 1) Advertised capabilities + use-case library --------------------------
echo ""
echo "── Advertised capabilities ──"
"$PY" - <<'PY'
from agent.engine import CAPABILITIES
from agent.use_cases import USE_CASES
print("scanners  :", ", ".join(CAPABILITIES))
print("use-cases :", ", ".join(sorted(USE_CASES)))
PY

# --- 2) Built-in self-test (startup gauntlet) -------------------------------
echo ""
echo "── Probe self-test ──"
LICENSE_ENFORCED=false "$PY" -m agent.agent self-test 2>&1 | tail -5 \
  || echo "[warn] self-test returned non-zero (continuing)"

# --- 3) Live scan — this is what exercises the scanners ---------------------
echo ""
echo "── Live scan (summary) ──"
"$PY" -m workflow.cli -t "$TARGET" -s "$SCOPE_FILE" --mode "$MODE" --profile "$PROFILE" -o "$OUT"

# --- 4) Per-capability breakdown from the asset report ----------------------
echo ""
echo "── Capabilities exercised (✓ = produced facts) ──"
"$PY" - "$OUT" <<'PY'
import json, sys
data = json.load(open(sys.argv[1]))
if not data:
    print("  (no hosts scanned — target unreachable or out of scope)"); sys.exit(0)

def count(x): return len(x) if isinstance(x, (list, dict)) else (1 if x else 0)

for host, a in data.items():
    open_ports = sorted(int(p) for p, f in (a.get("open_ports") or {}).items()
                        if (f or {}).get("status") == "open")
    snmp = a.get("snmp_state") or {}
    snmp_hit = any((v or {}).get("responded") for v in snmp.values()) if isinstance(snmp, dict) else False
    rows = [
        ("host_discovery + port_scan", len(open_ports) > 0, f"{len(open_ports)} open: {open_ports}"),
        ("service_fingerprint",        count(a.get("services")) > 0, f"{count(a.get('services'))} banner(s)"),
        ("tls_scan",                   count(a.get("tls_facts")) > 0, f"ports {list((a.get('tls_facts') or {}).keys())}"),
        ("web_scan",                   count(a.get("web_facts")) > 0, f"ports {list((a.get('web_facts') or {}).keys())}"),
        ("smb_enum",                   bool(a.get("smb_state")), "responded" if a.get("smb_state") else "no SMB"),
        ("snmp_scan",                  snmp_hit, f"{count(snmp)} probe(s)" + (", responded" if snmp_hit else "")),
        ("db_fingerprint",             count(a.get("db_facts")) > 0, f"{count(a.get('db_facts'))} db"),
        ("ai_service_discovery",       count(a.get("ai_facts")) > 0, f"{count(a.get('ai_facts'))} ai"),
        ("credentialed_inventory",     bool(a.get("cred_collected")), "collected" if a.get("cred_collected") else "not run (no creds)"),
    ]
    alive = "alive" if a.get("last_seen_alive") else "no-response"
    print(f"\n  host {host}  [{alive}]")
    for cap, hit, detail in rows:
        print(f"    {'✓' if hit else '·'}  {cap:<28} {detail}")
PY

echo ""
echo "Full asset report → $OUT"
echo "Done."
