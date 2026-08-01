#!/usr/bin/env sh
# =============================================================================
# Vedha — live probe scan in one command (real probe → facts → findings)
#
#   scripts/probe-lab.sh                        # LAB: stand up a vulnerable Debian
#                                               # target + scan it → guaranteed findings
#   scripts/probe-lab.sh --target 192.168.1.78     # scan a REAL LAN host (native probe)
#   scripts/probe-lab.sh --target 192.168.1.78 --cidr 192.168.1.0/24
#
# LAB mode uses the compose probe + a Debian container on the manager network.
# --target uses a NATIVE probe on this host (real LAN reachability; a container
# probe can't reach the LAN on macOS). Selects/launches a probe whose advertised
# segment COVERS the target's CIDR. Unauthenticated only (the manager rejects
# credentials in job params) → findings come from exposed service banners
# (openssh / nginx / apache / mariadb / postgres / redis).
#
# Only scan hosts you are authorized to test.
# =============================================================================
set -eu

MANAGER="${MANAGER:-http://localhost:18080}"; TARGET=""; CIDR=""; KEEP=""; EMAIL=""; TIMEOUT="${TIMEOUT:-300}"
while [ $# -gt 0 ]; do
  case "$1" in
    --target) TARGET="$2"; shift 2 ;;  --cidr) CIDR="$2"; shift 2 ;;
    --manager) MANAGER="$2"; shift 2 ;; --email) EMAIL="$2"; shift 2 ;;
    --keep) KEEP="yes"; shift ;;        --timeout) TIMEOUT="$2"; shift 2 ;;
    -h|--help) sed -n '2,19p' "$0"; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done
command -v curl >/dev/null 2>&1    || { echo "curl required" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "python3 required" >&2; exit 1; }
command -v docker >/dev/null 2>&1  || { echo "docker required" >&2; exit 1; }
case "$MANAGER" in http://*|https://*) BASE="$MANAGER" ;; *) BASE="https://$MANAGER" ;; esac
BASE="${BASE%/}"
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
envval() { [ -f "$ROOT/.env" ] && grep -E "^$1=" "$ROOT/.env" 2>/dev/null | head -1 | cut -d= -f2- || true; }
[ -n "$EMAIL" ] || EMAIL="${ADMIN_EMAIL:-$(envval SEED_ADMIN_EMAIL)}"; [ -n "$EMAIL" ] || EMAIL="admin@vedha.io"
PASSWORD="${ADMIN_PASSWORD:-$(envval SEED_ADMIN_PASSWORD)}"; [ -n "$PASSWORD" ] || PASSWORD="ChangeMe123!"
MODE="lab"; [ -n "$TARGET" ] && MODE="target"
if [ "$MODE" = "target" ] && [ -z "$CIDR" ]; then CIDR="$(printf '%s' "$TARGET" | sed 's/\.[0-9]*$/.0\/24/')"; fi

RESP="$(mktemp)"; ERRF="$(mktemp)"; REQ="$(mktemp)"; CFG="$(mktemp)"; PROBE_LOG="/tmp/vedha-lab-probe.log"
AUTO_PROBE_PID=""; STARTED_TARGET=""
cleanup() {
  [ -z "$KEEP" ] && [ -n "$AUTO_PROBE_PID" ] && kill "$AUTO_PROBE_PID" 2>/dev/null && echo "[cleanup] stopped native probe" >&2 || true
  [ -z "$KEEP" ] && [ -n "$STARTED_TARGET" ] && docker rm -f vedha-lab-target >/dev/null 2>&1 && echo "[cleanup] removed lab target" >&2 || true
  rm -f "$RESP" "$ERRF" "$REQ" "$CFG"
}
trap cleanup EXIT

login() { curl -sS -X POST "$BASE/auth/login" -H 'Content-Type: application/json' \
  -d "$(EMAIL="$EMAIL" PASSWORD="$PASSWORD" python3 -c 'import json,os;print(json.dumps({"email":os.environ["EMAIL"],"password":os.environ["PASSWORD"]}))')" \
  | python3 -c 'import sys,json;print(json.load(sys.stdin).get("access_token",""))' 2>/dev/null; }
CODE=""
call() { m="$1"; u="$2"; d="${3:-}"
  if [ -n "$d" ]; then printf '%s' "$d" > "$REQ"
    CODE="$(curl --config "$CFG" -sS -o "$RESP" -w '%{http_code}' -X "$m" "$u" -H 'Content-Type: application/json' -d @"$REQ" 2>"$ERRF" || echo 000)"
  else CODE="$(curl --config "$CFG" -sS -o "$RESP" -w '%{http_code}' -X "$m" "$u" 2>"$ERRF" || echo 000)"; fi
}
jget() { python3 -c 'import sys,json;print(json.load(open(sys.argv[1])).get(sys.argv[2],"") or "")' "$RESP" "$1"; }
# covering CIDR RESPFILE -> name of an ONLINE probe whose segment covers CIDR (or empty)
covering() { python3 -c 'import sys,json,ipaddress
try: agents=json.load(open(sys.argv[2]))
except Exception: sys.exit(0)
try: cidr=ipaddress.ip_network(sys.argv[1],strict=False)
except Exception: sys.exit(0)
def cov(segs):
    for s in (segs or []):
        try:
            n=ipaddress.ip_network(s,strict=False)
            if cidr.subnet_of(n) or n.overlaps(cidr): return True
        except Exception: pass
    return False
for a in agents:
    if a.get("online") and cov(a.get("network_segments")): print(a.get("name")); break' "$1" "$2"; }

echo "=============================================================="
echo " Vedha probe-lab   mode=$MODE   manager=$BASE"
echo "=============================================================="

# ── 0) manager up ────────────────────────────────────────────────────────────
health() { curl -s -o /dev/null -w '%{http_code}' "$BASE/health" 2>/dev/null || echo 000; }
if [ "$(health)" != "200" ]; then
  echo "• manager down — make up ..."; ( cd "$ROOT" && make up >/tmp/vedha-lab-up.log 2>&1 ) || { echo "✗ make up failed (/tmp/vedha-lab-up.log)" >&2; exit 1; }
  n=0; while [ "$(health)" != "200" ] && [ "$n" -lt 150 ]; do sleep 3; n=$((n+3)); done
fi
[ "$(health)" = "200" ] || { echo "✗ manager /health not 200" >&2; exit 1; }
echo "✓ manager up"
TOKEN="$(login)"; [ -n "$TOKEN" ] || { echo "✗ login failed" >&2; exit 1; }
{ printf 'silent\nshow-error\n'; printf 'header = "Authorization: Bearer %s"\n' "$TOKEN"; } > "$CFG"; chmod 600 "$CFG"
echo "✓ authenticated"

# ── 1) provision probe + target ──────────────────────────────────────────────
if [ "$MODE" = "lab" ]; then
  NET="$(docker network ls --format '{{.Name}}' | grep -i vedha | head -1)"; NET="${NET:-vedha_default}"
  SUBNET="$(docker network inspect "$NET" --format '{{range .IPAM.Config}}{{.Subnet}}{{end}}' 2>/dev/null)"; SUBNET="${SUBNET:-172.18.0.0/16}"
  echo "• lab target on $NET ($SUBNET) ..."
  docker rm -f vedha-lab-target >/dev/null 2>&1 || true
  docker run -d --name vedha-lab-target --network "$NET" --hostname deb-vuln debian:11 bash -c \
    "apt-get update -qq && apt-get install -y openssh-server nginx >/dev/null 2>&1; mkdir -p /run/sshd; nginx; echo READY>/tmp/r; /usr/sbin/sshd -D" >/dev/null
  STARTED_TARGET="yes"
  n=0; while [ "$n" -lt 90 ]; do [ "$(docker exec vedha-lab-target cat /tmp/r 2>/dev/null)" = "READY" ] && break; sleep 3; n=$((n+3)); done
  TARGET="$(docker inspect vedha-lab-target --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')"; CIDR="$SUBNET"
  echo "  target up: $TARGET (openssh + nginx)"
  echo "• compose probe on $NET (segment $SUBNET) ..."
  ( cd "$ROOT" && PROBE_NETWORK_SEGMENTS="$SUBNET" docker compose --profile probe up -d probe >/dev/null 2>&1 ) || true
else
  echo "• target mode: need a probe covering $CIDR (native — real LAN reachability)"
  call GET "$BASE/agents"
  if [ -z "$(covering "$CIDR" "$RESP")" ]; then
    echo "  launching a native probe scoped to $CIDR ..."
    call POST "$BASE/auth/personal-access-tokens" "$(python3 -c 'import json,sys;print(json.dumps({"name":"lab-"+sys.argv[1],"expires_in_days":7}))' "$(date +%s)")"
    VPAT="$(jget token)"; [ -n "$VPAT" ] || { echo "✗ PAT mint failed (HTTP $CODE): $(cat "$RESP")" >&2; exit 1; }
    ( cd "$ROOT/probe" && { [ -x .venv/bin/python ] && .venv/bin/python -c 'import httpx' 2>/dev/null; } || { python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt; } ) || { echo "✗ probe venv failed" >&2; exit 1; }
    SDIR="$ROOT/probe/.lab-run"; mkdir -p "$SDIR/spool"
    ( cd "$ROOT/probe" && TMPDIR="$SDIR" PLATFORM_URL="$BASE" OPERATOR_TOKEN="$VPAT" PROBE_NAME="lab-native-probe" \
        PROBE_NETWORK_SEGMENTS="127.0.0.0/8,$CIDR" LICENSE_ENFORCED=false \
        STATE_FILE="$SDIR/state.json" RESULT_SPOOL_DIR="$SDIR/spool" \
        nohup .venv/bin/python -m agent.agent >"$PROBE_LOG" 2>&1 & echo $! >/tmp/vedha-lab-probe.pid )
    AUTO_PROBE_PID="$(cat /tmp/vedha-lab-probe.pid)"
  else
    echo "  reusing an online probe that already covers $CIDR"
  fi
fi

# wait for a probe COVERING the scope (not just any online probe)
printf '  waiting for a probe covering %s' "$CIDR"
n=0; PN=""
while [ "$n" -lt 90 ]; do
  call GET "$BASE/agents"; PN="$(covering "$CIDR" "$RESP")"
  [ -n "$PN" ] && break; printf '.'; sleep 3; n=$((n+3))
done
printf '\n'
[ -n "$PN" ] || { echo "✗ no probe covering $CIDR came online"; [ -f "$PROBE_LOG" ] && tail -12 "$PROBE_LOG"; exit 1; }
echo "✓ probe online (covers $CIDR): $PN"
echo "  target=$TARGET  scope=$CIDR"

# ── 2) engagement + unauthenticated assessment ───────────────────────────────
call POST "$BASE/engagements" "$(NAME="probe-lab $TARGET" CIDR="$CIDR" python3 -c 'import json,os;print(json.dumps({"name":os.environ["NAME"],"scope_cidrs":[os.environ["CIDR"]]}))')"
EID="$(jget id)"; [ -n "$EID" ] || { echo "✗ engagement failed (HTTP $CODE): $(cat "$RESP")" >&2; exit 1; }
echo "✓ engagement: $EID"
call POST "$BASE/agents/jobs" "$(EID="$EID" T="$TARGET" C="$CIDR" python3 -c 'import json,os;print(json.dumps({"engagement_id":os.environ["EID"],"use_case_id":"uc_full_assessment","params":{"targets":[os.environ["T"]],"scope_cidrs":[os.environ["C"]]}}))')"
JID="$(jget job_id)"; [ -n "$JID" ] || { echo "✗ enqueue failed (HTTP $CODE): $(cat "$RESP")" >&2; exit 1; }
echo "  → job $JID"
w=0; st="?"; while [ "$w" -lt "$TIMEOUT" ]; do
  call GET "$BASE/agents/jobs/$JID"; st="$(python3 -c 'import sys,json
try: print((json.load(open(sys.argv[1])) or {}).get("status","?"))
except: print("?")' "$RESP")"
  printf '\r  scan: %s (%ss)   ' "$st" "$w"
  case "$st" in done|completed|failed|error) printf '\n'; break ;; esac; sleep 4; w=$((w+4))
done
cp "$RESP" /tmp/vedha-lab-job.json

# detection runs asynchronously after the probe submits facts — wait for it
printf '  detecting'
n=0; while [ "$n" -lt 45 ]; do
  T="$(login)"; { printf 'silent\nshow-error\n'; printf 'header = "Authorization: Bearer %s"\n' "$T"; } > "$CFG"
  call GET "$BASE/findings/summary?engagement_id=$EID"
  tot="$(python3 -c 'import sys,json
try: print(json.load(open(sys.argv[1])).get("total",0))
except: print(0)' "$RESP")"
  [ "${tot:-0}" -gt 0 ] 2>/dev/null && break
  printf '.'; sleep 3; n=$((n+3))
done
printf '\n'

# ── 3) VA report ─────────────────────────────────────────────────────────────
T="$(login)"; { printf 'silent\nshow-error\n'; printf 'header = "Authorization: Bearer %s"\n' "$T"; } > "$CFG"
call GET "$BASE/findings/summary?engagement_id=$EID"; cp "$RESP" /tmp/vedha-lab-sum.json
call GET "$BASE/findings?engagement_id=$EID&page_size=100&sort=risk"; cp "$RESP" /tmp/vedha-lab-top.json
echo ""; echo "── VA REPORT ──"
python3 - /tmp/vedha-lab-job.json /tmp/vedha-lab-sum.json /tmp/vedha-lab-top.json <<'PY'
import json, sys
def load(p):
    try: return json.load(open(p))
    except Exception: return {}
job, summ, top = load(sys.argv[1]), load(sys.argv[2]), load(sys.argv[3])
r = job.get("result") or {}
if isinstance(r, str):
    try: r = json.loads(r)
    except Exception: r = {}
print("  probe funnel  : host_alive=%s services=%s (probe emits facts, not CVEs)" % (r.get("host_count"), r.get("service_count")))
for s in (r.get("scanner_runs") or []):
    if (s.get("fact_count") or 0) > 0 or s.get("status") in ("degraded","failed"):
        print("     %-16s %-10s facts=%s err=%s" % (s.get("id"), s.get("status"), s.get("fact_count"), s.get("error_count")))
tot = summ.get("total", 0)
print("  findings      : %s   (C%s H%s M%s L%s I%s)  avg_risk=%s" % (
    tot, summ.get("critical_open"), summ.get("high_open"), summ.get("medium_open"),
    summ.get("low_open"), summ.get("info_open"), summ.get("average_risk")))
items = top.get("items", [])
if items:
    print("  top by risk:")
    for x in items[:15]:
        cve = (x.get("cve_ids") or [""])[0]
        print("     [%8s] cvss=%4s %-18s %s" % (
            (x.get("severity") or "").upper(), str(x.get("cvss_score") or "-"), cve, (x.get("title") or "")[:46]))
else:
    print("  (no CVE findings — the target exposed no service the OSV-Debian DB covers.")
    print("   Enumeration above is real. For CVE findings, scan a host running")
    print("   openssh/nginx/apache/mariadb/postgres/redis — or run without --target for the lab.)")
PY
echo ""
echo "Engagement $EID · Dashboard $BASE  (Findings → Explain / Ask Vedha)"
echo "API: $BASE/findings?engagement_id=$EID&page_size=100"
