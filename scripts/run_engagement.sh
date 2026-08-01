#!/usr/bin/env sh
# =============================================================================
# Vedha — operator engagement runner + pipeline troubleshooter
#
# Confirms a probe is online → creates a scoped engagement → runs discovery then
# a full assessment (polling each job) → summarizes findings. On any failure it
# reports the EXACT stage + HTTP code + manager error, and if findings come back
# empty it walks the pipeline to tell you where it broke:
#     auth → probe-online → COLLECTION (probe) → INGEST (api) → DETECTION (worker)
#
#   scripts/run_engagement.sh <manager> <authorized-cidr> [options]
#
#   scripts/run_engagement.sh http://localhost:18080 192.168.1.0/24 --targets 192.168.1.70 --insecure
#   scripts/run_engagement.sh vedha.example.com 10.0.0.0/24 --targets 10.0.0.10
#   scripts/run_engagement.sh vedha.example.com 10.0.0.0/24 --debug          # trace every HTTP call
#
# Only scan CIDRs you are authorized to test.
# =============================================================================
set -eu

# ── args ─────────────────────────────────────────────────────────────────────
[ $# -ge 2 ] || { sed -n '2,20p' "$0"; exit 2; }
MANAGER="$1"; CIDR="$2"; shift 2
TARGETS=""; USE_CASE="uc_full_assessment"; NAME=""; EMAIL=""; EXCLUDED=""
DISCOVERY_FIRST="yes"; INSECURE=""; DEBUG=""
TIMEOUT="${TIMEOUT:-1800}"
while [ $# -gt 0 ]; do
  case "$1" in
    --targets) TARGETS="$2"; shift 2 ;;   --use-case) USE_CASE="$2"; shift 2 ;;
    --name) NAME="$2"; shift 2 ;;         --email) EMAIL="$2"; shift 2 ;;
    --excluded) EXCLUDED="$2"; shift 2 ;; --timeout) TIMEOUT="$2"; shift 2 ;;
    --ssh-user|--ssh-key|--win-user)
      echo "Credentialed Manager jobs are disabled until an ephemeral secret broker is configured." >&2
      exit 2 ;;
    --no-discovery) DISCOVERY_FIRST="no"; shift ;; --insecure) INSECURE="yes"; shift ;;
    --debug) DEBUG="yes"; shift ;;        -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done
command -v curl >/dev/null 2>&1 || { echo "curl is required." >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "python3 is required." >&2; exit 1; }

case "$MANAGER" in http://*|https://*) BASE="$MANAGER" ;; *) BASE="https://$MANAGER" ;; esac
BASE="${BASE%/}"
case "$BASE" in http://*) [ -n "$INSECURE" ] || { echo "Refusing plain http without --insecure." >&2; exit 1; } ;; esac
[ -n "$TARGETS" ] || TARGETS="$CIDR"
[ -n "$NAME" ] || NAME="$CIDR — $(date +%Y-%m-%d)"
CURL_K=""; [ -n "$INSECURE" ] && CURL_K="-k"
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
envval() { [ -f "$ROOT/.env" ] && grep -E "^$1=" "$ROOT/.env" 2>/dev/null | head -1 | cut -d= -f2- || true; }
[ -n "$EMAIL" ] || EMAIL="${OPERATOR_EMAIL:-${ADMIN_EMAIL:-}}"
[ -n "$EMAIL" ] || EMAIL="$(envval SEED_ADMIN_EMAIL)"; [ -n "$EMAIL" ] || EMAIL="admin@vedha.io"

# ── temp files + python helper (all JSON handled here → no shell quote-escaping)
RESP="$(mktemp)"; ERRF="$(mktemp)"; REQ="$(mktemp)"; CFG="$(mktemp)"; PYH="$(mktemp)"
chmod 600 "$CFG"; trap 'rm -f "$RESP" "$ERRF" "$REQ" "$CFG" "$PYH"' EXIT
cat > "$PYH" <<'PY'
import sys, json
def load(p):
    with open(p) as f: return json.load(f)
def items(d): return d.get("items", d if isinstance(d, list) else []) if isinstance(d,(dict,list)) else []
def result(d):
    r = (d or {}).get("result") or {}
    if isinstance(r, str):
        try: r = json.loads(r)
        except Exception: r = {}
    return r if isinstance(r, dict) else {}
cmd = sys.argv[1]
try:
    if cmd == "get":
        print(load(sys.argv[2]).get(sys.argv[3], "") or "")
    elif cmd == "len":
        print(len(items(load(sys.argv[2]))))
    elif cmd == "agents-online":
        print(",".join(x.get("name","?") for x in load(sys.argv[2]) if x.get("online")))
    elif cmd == "agents-detail":
        a = load(sys.argv[2])
        if not a: print("    (no agents registered at all)")
        for x in a:
            print(f"    - {x.get('name')}: online={x.get('online')} status={x.get('status')} "
                  f"last_heartbeat={x.get('last_heartbeat')} segments={x.get('network_segments')}")
    elif cmd == "eng-body":
        name, cidrs, excl = sys.argv[2], sys.argv[3], sys.argv[4]
        b = {"name": name, "scope_cidrs": [c.strip() for c in cidrs.split(",") if c.strip()]}
        ex = [c.strip() for c in excl.split(",") if c.strip()]
        if ex: b["excluded_cidrs"] = ex
        print(json.dumps(b))
    elif cmd == "job-body":
        eid, uc, targets, scope = sys.argv[2:6]
        p = {"targets": [t.strip() for t in targets.split(",") if t.strip()],
             "scope_cidrs": [c.strip() for c in scope.split(",") if c.strip()]}
        print(json.dumps({"engagement_id": eid, "use_case_id": uc, "params": p}))
    elif cmd == "job-status":
        d = load(sys.argv[2]); print((d or {}).get("status", "?") if isinstance(d, dict) else "?")
    elif cmd == "job-facts":
        r = result(load(sys.argv[2]))
        print(int(len(r.get("facts") or []) or (r.get("service_count") or 0) or (r.get("host_count") or 0)))
    elif cmd == "job-diag":
        d = load(sys.argv[2]); r = result(d)
        print("    status     :", (d or {}).get("status"))
        print("    outcome    :", r.get("outcome"))
        print("    host_count :", r.get("host_count"), " service_count:", r.get("service_count"),
              " finding_count:", r.get("finding_count"), " facts:", len(r.get("facts") or []))
        for s in (r.get("scanner_runs") or [])[:20]:
            print(f"      scanner {s.get('id')}: {s.get('status')} facts={s.get('fact_count')} err={s.get('error_count')}")
        for i in (r.get("issues") or [])[:10]:
            print(f"      issue {i.get('code')} scanner={i.get('scanner')} target={i.get('target')} retryable={i.get('retryable')}")
        if not r: print("    (no result payload on the job record yet)")
    elif cmd == "findings-summary":
        it = items(load(sys.argv[2])); print("  total:", len(it))
        if it:
            from collections import Counter
            order = {"CRITICAL":0,"HIGH":1,"MEDIUM":2,"LOW":3,"INFO":4}
            sev = Counter((x.get("severity") or "INFO").upper() for x in it)
            print("  by severity:", {k: sev[k] for k in sorted(sev, key=lambda s: order.get(s,9))})
            it.sort(key=lambda x: -(float(x.get("risk_score") or 0)))
            for x in it[:10]:
                print(f"    [{(x.get('severity') or '').upper():>8}] risk={x.get('risk_score')} "
                      f"{x.get('title')}  {x.get('cve_ids') or ''}")
    else:
        print(f"unknown helper cmd: {cmd}", file=sys.stderr); sys.exit(3)
except Exception as e:
    print(f"[helper error in '{cmd}': {e}]", file=sys.stderr); sys.exit(4)
PY
py() { python3 "$PYH" "$@"; }

# ── HTTP wrapper: captures code + body; --debug traces every call ────────────
CODE=""
call() { # METHOD URL [JSON_BODY]
  m="$1"; u="$2"; d="${3:-}"
  if [ -n "$d" ]; then printf '%s' "$d" > "$REQ"
    CODE="$(curl $CURL_K --config "$CFG" -sS -o "$RESP" -w '%{http_code}' -X "$m" "$u" \
      -H 'Content-Type: application/json' -d @"$REQ" 2>"$ERRF" || echo 000)"
  else
    CODE="$(curl $CURL_K --config "$CFG" -sS -o "$RESP" -w '%{http_code}' -X "$m" "$u" 2>"$ERRF" || echo 000)"
  fi
  [ -n "$DEBUG" ] && { echo "  [debug] $m $u -> HTTP $CODE" >&2; echo "  [debug] body: $(head -c 300 "$RESP" 2>/dev/null)" >&2; }
  return 0
}
ok() { case "$CODE" in 2*) return 0 ;; *) return 1 ;; esac; }
die_stage() { # STAGE
  echo "" >&2
  echo "✗ FAILED at stage: $1   (HTTP $CODE)" >&2
  b="$(head -c 500 "$RESP" 2>/dev/null)"; [ -n "$b" ] && echo "  manager said: $b" >&2
  [ -s "$ERRF" ] && echo "  curl: $(head -c 200 "$ERRF")" >&2
  case "$CODE" in
    000) echo "  → manager unreachable. Check: curl -s $BASE/health  ;  docker compose ps" >&2 ;;
    401|403) echo "  → auth/scope rejected: wrong password, expired token, or out-of-scope target." >&2 ;;
    404) echo "  → not found: bad id or endpoint path." >&2 ;;
    422) echo "  → invalid request body: check CIDR/target format ($b)." >&2 ;;
    5*)  echo "  → manager-side error. Inspect: docker compose logs --tail 60 api worker" >&2 ;;
  esac
  exit 1
}

echo "=============================================================="
echo " Vedha engagement runner   manager=$BASE  scope=$CIDR  targets=$TARGETS"
echo "=============================================================="

# ── 0) preflight: is the manager even up? ────────────────────────────────────
call GET "$BASE/health"; ok || die_stage "preflight /health (manager down or wrong URL)"
echo "✓ manager reachable"

# ── 1) auth (token never on the command line) ────────────────────────────────
PASSWORD="${ADMIN_PASSWORD:-${OPERATOR_PASSWORD:-}}"
if [ -z "$PASSWORD" ]; then
  if [ -t 0 ]; then printf 'Password for %s: ' "$EMAIL" >&2; stty -echo 2>/dev/null||true; read PASSWORD; stty echo 2>/dev/null||true; printf '\n' >&2
  else echo "Set ADMIN_PASSWORD (non-interactive)." >&2; exit 1; fi
fi
lbody="$(EMAIL="$EMAIL" PASSWORD="$PASSWORD" python3 -c 'import json,os;print(json.dumps({"email":os.environ["EMAIL"],"password":os.environ["PASSWORD"]}))')"
CODE="$(printf '%s' "$lbody" | curl $CURL_K -sS -o "$RESP" -w '%{http_code}' -X POST "$BASE/auth/login" -H 'Content-Type: application/json' -d @- 2>"$ERRF" || echo 000)"
ok || die_stage "login (check email/password)"
JWT="$(py get "$RESP" access_token)"; [ -n "$JWT" ] || die_stage "login (no access_token in response)"
{ printf 'silent\nshow-error\n'; printf 'header = "Authorization: Bearer %s"\n' "$JWT"; } > "$CFG"
echo "✓ authenticated as $EMAIL"

# ── 2) probe online? ─────────────────────────────────────────────────────────
call GET "$BASE/agents"; ok || die_stage "list agents"
ONLINE="$(py agents-online "$RESP")"
if [ -z "$ONLINE" ]; then
  echo "✗ no probe is ONLINE — the scan cannot run." >&2
  echo "  registered agents:" >&2; py agents-detail "$RESP" >&2
  echo "  → start the probe, and check its log for 'Registered / Waiting for jobs'." >&2
  exit 1
fi
echo "✓ probe online: $ONLINE"

# ── 3) engagement ────────────────────────────────────────────────────────────
call POST "$BASE/engagements" "$(py eng-body "$NAME" "$CIDR" "$EXCLUDED")"; ok || die_stage "create engagement"
EID="$(py get "$RESP" id)"; [ -n "$EID" ] || die_stage "create engagement (no id)"
echo "✓ engagement: $EID"

# ── 4) run a job (enqueue + poll) ────────────────────────────────────────────
LAST_JID=""
run_job() { # use_case_id  label
  call POST "$BASE/agents/jobs" "$(py job-body "$EID" "$1" "$TARGETS" "$CIDR" "$SSH_USER" "$SSH_KEY")"
  ok || die_stage "enqueue $2"
  LAST_JID="$(py get "$RESP" job_id)"; [ -n "$LAST_JID" ] || die_stage "enqueue $2 (no job_id)"
  echo "  → $2 job $LAST_JID"
  waited=0
  while [ "$waited" -lt "$TIMEOUT" ]; do
    call GET "$BASE/agents/jobs/$LAST_JID"; ok || die_stage "poll $2"
    st="$(py job-status "$RESP")"
    printf '\r    %s: %s (%ss)        ' "$2" "$st" "$waited"
    case "$st" in done|completed) printf '\n'; return 0 ;; failed|error) printf '\n'; return 1 ;; esac
    sleep 5; waited=$((waited + 5))
  done
  printf '\n'; return 2
}
echo "── scanning ──"
if [ "$DISCOVERY_FIRST" = "yes" ]; then run_job uc_discovery_only "Discovery" || echo "  (discovery not done — continuing)"; fi
run_job "$USE_CASE" "Assessment"; ASSESS_RC=$?
ASSESS_JID="$LAST_JID"
[ "$ASSESS_RC" = 0 ] || echo "  (assessment ended rc=$ASSESS_RC — see diagnostics below)"

# ── 5) findings + pipeline breakpoint diagnosis ──────────────────────────────
echo ""
echo "── findings ──"
call GET "$BASE/findings?engagement_id=$EID&page_size=100"; ok || die_stage "list findings"
FINDINGS="$(py len "$RESP")"
py findings-summary "$RESP"

if [ "$FINDINGS" = "0" ]; then
  echo ""
  echo "── pipeline diagnostics (findings=0) ──"
  # a) probe still online (submit needs it up)?
  call GET "$BASE/agents"; STILL="$(py agents-online "$RESP" || echo '')"
  echo "  probe online now : ${STILL:-NONE}"
  # b) COLLECTION: what did the probe report on the job?
  call GET "$BASE/agents/jobs/$ASSESS_JID"
  echo "  job result:"; py job-diag "$RESP"
  FACTS="$(py job-facts "$RESP" 2>/dev/null || echo 0)"
  # c) INGEST: did facts become assets?
  call GET "$BASE/engagements/$EID/assets"; ASSETS="$(py len "$RESP" 2>/dev/null || echo 0)"
  echo "  assets ingested  : $ASSETS"
  echo ""
  echo "  DIAGNOSIS:"
  if [ "${ASSETS:-0}" -gt 0 ] 2>/dev/null; then
    echo "   → DETECTION stage. Probe collected + ingested ($ASSETS asset(s)) but 0 CVEs matched."
    echo "     Unauthenticated evidence may be version-poor, or this may be a genuinely quiet scope."
    echo "     Verify banners/configuration manually; credentialed Manager jobs require a future secret broker."
  elif [ "${FACTS:-0}" -gt 0 ] 2>/dev/null; then
    echo "   → INGEST stage. Probe collected facts ($FACTS) but they did not persist as assets."
    echo "     The api/worker likely errored or restarted at submit-time."
    echo "     Check: docker compose logs --tail 80 api worker   (look for tracebacks / OOM / 500)."
  else
    echo "   → COLLECTION stage. The probe collected nothing (or couldn't submit)."
    echo "     Likely: target down/unreachable, out-of-scope, the probe can't route to the target"
    echo "     (on macOS a *containerised* probe can't reach the LAN — run the probe natively),"
    echo "     or the result is stuck in the probe's spool because the manager was unreachable."
    echo "     Check: the probe terminal/log, its RESULT_SPOOL_DIR, and 'scanner_runs/issues' above."
    [ -z "$STILL" ] && echo "     NOTE: no probe is online now — the submit connection was likely lost."
  fi
fi

echo ""
echo "Engagement $EID complete.  Findings: $BASE/findings?engagement_id=$EID"
