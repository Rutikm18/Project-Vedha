#!/usr/bin/env sh
# =============================================================================
# Vedha — one-command automated vulnerability assessment
#
#   scripts/assess.sh <scope-cidr> [options]
#
# Give it a scope and it self-provisions the whole pipeline:
#   • brings the manager up if it's down          (make up)
#   • auto-launches a native probe if none online (mints a PAT itself)
#   • runs discovery + full assessment
#   • prints a DEBUG report: funnel accountability, per-scanner telemetry,
#     an independent ground-truth accuracy cross-check, and the exact
#     point-of-failure stage (collection / ingest / detection).
#
#   scripts/assess.sh 192.168.1.0/24 --targets 192.168.1.70
#   scripts/assess.sh 127.0.0.0/8 --targets 127.0.0.1 --verify
#   scripts/assess.sh 10.0.0.0/24 --manager https://vedha.example.com --targets 10.0.0.10
#
# Only scan what you are authorized to. Auto-provisioning targets a LOCAL manager
# (http://localhost:18080) by default; pass --manager for a remote one.
# =============================================================================
set -eu

# ── args ─────────────────────────────────────────────────────────────────────
[ $# -ge 1 ] || { sed -n '2,20p' "$0"; exit 2; }
SCOPE="$1"; shift
MANAGER="${MANAGER:-http://localhost:18080}"
TARGETS=""; USE_CASE="uc_full_assessment"; EMAIL=""
VERIFY=""; NO_BRINGUP=""; KEEP_PROBE=""; DEBUG=""; INSECURE="yes"; TIMEOUT="${TIMEOUT:-1800}"
while [ $# -gt 0 ]; do
  case "$1" in
    --scope) SCOPE="$2"; shift 2 ;;            --targets) TARGETS="$2"; shift 2 ;;
    --manager) MANAGER="$2"; shift 2 ;;        --use-case) USE_CASE="$2"; shift 2 ;;
    --email) EMAIL="$2"; shift 2 ;;            --timeout) TIMEOUT="$2"; shift 2 ;;
    --ssh-user|--ssh-key|--win-user)
      echo "Credentialed Manager jobs are disabled until an ephemeral secret broker is configured." >&2
      exit 2 ;;
    --verify) VERIFY="yes"; shift ;;           --no-bringup) NO_BRINGUP="yes"; shift ;;
    --keep-probe) KEEP_PROBE="yes"; shift ;;   --debug) DEBUG="yes"; shift ;;
    --secure) INSECURE=""; shift ;;            -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done
command -v curl >/dev/null 2>&1    || { echo "curl required" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "python3 required" >&2; exit 1; }

case "$MANAGER" in http://*|https://*) BASE="$MANAGER" ;; *) BASE="https://$MANAGER" ;; esac
BASE="${BASE%/}"
[ -n "$TARGETS" ] || TARGETS="$SCOPE"
CURL_K=""; case "$BASE" in http://*) [ -n "$INSECURE" ] && CURL_K="" ;; esac
case "$BASE" in https://*) : ;; http://*) [ -n "$INSECURE" ] || { echo "http needs implicit insecure; ok for localhost" >&2; } ;; esac
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
envval() { [ -f "$ROOT/.env" ] && grep -E "^$1=" "$ROOT/.env" 2>/dev/null | head -1 | cut -d= -f2- || true; }
[ -n "$EMAIL" ] || EMAIL="${ADMIN_EMAIL:-$(envval SEED_ADMIN_EMAIL)}"; [ -n "$EMAIL" ] || EMAIL="admin@vedha.io"
PASSWORD="${ADMIN_PASSWORD:-$(envval SEED_ADMIN_PASSWORD)}"; [ -n "$PASSWORD" ] || PASSWORD="ChangeMe123!"

# ── temp files + python helper (all JSON logic here → no shell quoting bugs) ──
RESP="$(mktemp)"; ERRF="$(mktemp)"; REQ="$(mktemp)"; CFG="$(mktemp)"; PYH="$(mktemp)"
JOBF="$(mktemp)"; FINDF="$(mktemp)"; INDF="$(mktemp)"; PROBE_LOG="/tmp/vedha-assess-probe.log"
AUTO_PROBE_PID=""
cleanup() {
  [ -n "$AUTO_PROBE_PID" ] && [ -z "$KEEP_PROBE" ] && kill "$AUTO_PROBE_PID" 2>/dev/null && echo "[cleanup] stopped auto-probe (pid $AUTO_PROBE_PID)" >&2 || true
  rm -f "$RESP" "$ERRF" "$REQ" "$CFG" "$PYH" "$JOBF" "$FINDF" "$INDF"
}
trap cleanup EXIT
cat > "$PYH" <<'PY'
import sys, json, socket
def load(p):
    try: return json.load(open(p))
    except Exception as e: return {"_err": str(e)}
def items(d):
    if isinstance(d, list): return d
    if isinstance(d, dict): return d.get("items", [])
    return []
def result(d):
    r = (d or {}).get("result") or {}
    if isinstance(r, str):
        try: r = json.loads(r)
        except Exception: r = {}
    return r if isinstance(r, dict) else {}
GT_PORTS = [21,22,23,25,53,80,110,111,135,139,143,161,443,445,993,995,1433,1521,
            2049,3306,3389,5000,5432,5900,6379,6443,7001,8000,8080,8443,9200,27017]
cmd = sys.argv[1]
try:
    if cmd == "get":
        print(load(sys.argv[2]).get(sys.argv[3], "") or "")
    elif cmd == "len":
        print(len(items(load(sys.argv[2]))))
    elif cmd == "agents-online":
        print(",".join(x.get("name","?") for x in load(sys.argv[2]) if x.get("online")))
    elif cmd == "job-status":
        d = load(sys.argv[2]); print((d or {}).get("status","?") if isinstance(d,dict) else "?")
    elif cmd == "metric":                       # job.json KEY -> number
        print(int(result(load(sys.argv[2])).get(sys.argv[3]) or 0))
    elif cmd == "portscan":                      # target -> {"target","open_ports"}
        t = sys.argv[2]; op = []
        for p in GT_PORTS:
            s = socket.socket(); s.settimeout(0.6)
            if s.connect_ex((t, p)) == 0: op.append(p)
            s.close()
        print(json.dumps({"target": t, "open_ports": op}))
    elif cmd == "eng-body":
        name, cidrs = sys.argv[2], sys.argv[3]
        print(json.dumps({"name": name, "scope_cidrs":[c.strip() for c in cidrs.split(",") if c.strip()]}))
    elif cmd == "job-body":
        eid, uc, targets, scope = sys.argv[2:6]
        p = {"targets":[t.strip() for t in targets.split(",") if t.strip()],
             "scope_cidrs":[c.strip() for c in scope.split(",") if c.strip()]}
        print(json.dumps({"engagement_id": eid, "use_case_id": uc, "params": p}))
    elif cmd == "pat-body":
        print(json.dumps({"name": sys.argv[2], "expires_in_days": 30}))
    elif cmd == "funnel":                        # job.json -> funnel + scanner table
        d = load(sys.argv[2]); r = result(d)
        print(f"  job status : {(d or {}).get('status')}   outcome: {r.get('outcome')}")
        print(f"  funnel     : hosts_alive={r.get('host_count')}  services={r.get('service_count')}  "
              f"probe_findings={r.get('finding_count')}")
        runs = r.get("scanner_runs") or []
        if runs:
            print("  scanners   :")
            for s in runs[:20]:
                print(f"     {s.get('id'):<20} {s.get('status'):<10} facts={s.get('fact_count')} err={s.get('error_count')}")
        for i in (r.get("issues") or [])[:10]:
            print(f"     ! issue {i.get('code')} scanner={i.get('scanner')} target={i.get('target')} retryable={i.get('retryable')}")
        if not r: print("  (no result payload on the job record — status only)")
    elif cmd == "findings-audit":                # detection accuracy per finding
        it = items(load(sys.argv[2]))
        if not it: print("  (no findings to audit)"); sys.exit(0)
        with_ev = sum(1 for x in it if x.get("evidence"))
        val = sum(1 for x in it if x.get("exploit_validated"))
        from collections import Counter
        ds = Counter((x.get("detection_status") or "?") for x in it)
        print(f"  findings={len(it)}  with_evidence={with_ev}  exploit_validated={val}  detection_status={dict(ds)}")
        for x in sorted(it, key=lambda z:-(float(z.get('risk_score') or 0)))[:8]:
            print(f"     [{(x.get('severity') or '').upper():>8}] risk={x.get('risk_score')} "
                  f"det={x.get('detection_status')} ev={'Y' if x.get('evidence') else 'n'} "
                  f"{x.get('title')} {x.get('cve_ids') or ''}")
    elif cmd == "diagnose":                       # job.json indep.json ASSETS FINDINGS
        r = result(load(sys.argv[2])); ind = load(sys.argv[3])
        assets = int(sys.argv[4]); findings = int(sys.argv[5])
        gt = sum(len(t.get("open_ports") or []) for t in items(ind)) if ind and not ind.get("_err") else -1
        hc = int(r.get("host_count") or 0); sc = int(r.get("service_count") or 0)
        print("  ── accuracy cross-check ──")
        if gt < 0:
            print("     ground-truth: (skipped — pass --verify with single-IP targets)")
        else:
            print(f"     ground-truth open ports (independent) : {gt}")
            print(f"     probe services reported               : {sc}")
            if gt > 0 and sc == 0:
                print("     ⚠ ACCURACY GAP: independent scan sees open ports but the probe reported 0 services.")
                print("       → vantage/routing (probe host can't reach target the way this script can),")
                print("         timing/rate-limit, or a degraded scanner (see the scanner table above).")
            elif gt == 0 and sc == 0:
                print("     ✓ consistent: no open ports from either side (nothing to find here).")
            elif gt == 0 and sc > 0:
                print(f"     ✓ probe observed {sc} service(s) from its network vantage; the coordinator saw none.")
                print("       This is not a contradiction when the probe is inside Docker/a remote segment;")
                print("       validate the probe evidence from the same vantage before judging accuracy.")
            elif sc >= gt and gt > 0:
                print(f"     ✓ probe saw ≥ ground truth ({sc} ≥ {gt}) — coverage looks good.")
            else:
                print(f"     ~ probe {sc} vs ground-truth {gt}: partial coverage; check the scanner table.")
        print("  ── point of failure ──")
        if findings > 0:
            print(f"     ✓ COMPLETE: {findings} finding(s) produced through the full pipeline.")
        elif assets > 0:
            print(f"     → DETECTION stage: {assets} asset(s) ingested but 0 CVEs matched.")
            print("       Unauthenticated evidence may be version-poor; verify banners/configuration manually.")
            print("       Credentialed Manager jobs stay disabled until the secret-broker design is implemented.")
        elif hc > 0 or sc > 0:
            print("     → INGEST stage: probe collected data but it did not persist as assets.")
            print("       Check: docker compose logs --tail 80 api worker  (tracebacks / OOM / 500).")
        else:
            print("     → COLLECTION stage: the probe collected nothing.")
            print("       Target down/unreachable/out-of-scope, wrong probe vantage, or result stuck in spool.")
    else:
        print(f"unknown cmd {cmd}", file=sys.stderr); sys.exit(3)
except Exception as e:
    print(f"[helper error in '{cmd}': {e}]", file=sys.stderr); sys.exit(4)
PY
py() { python3 "$PYH" "$@"; }

# ── HTTP wrapper (auth header via config file; --debug traces) ────────────────
CODE=""
call() { m="$1"; u="$2"; d="${3:-}"
  if [ -n "$d" ]; then printf '%s' "$d" > "$REQ"
    CODE="$(curl $CURL_K --config "$CFG" -sS -o "$RESP" -w '%{http_code}' -X "$m" "$u" -H 'Content-Type: application/json' -d @"$REQ" 2>"$ERRF" || echo 000)"
  else
    CODE="$(curl $CURL_K --config "$CFG" -sS -o "$RESP" -w '%{http_code}' -X "$m" "$u" 2>"$ERRF" || echo 000)"
  fi
  [ -n "$DEBUG" ] && echo "  [debug] $m $u -> $CODE  $(head -c 200 "$RESP" 2>/dev/null)" >&2 || true
}
ok() { case "$CODE" in 2*) return 0 ;; *) return 1 ;; esac; }
die() { echo "" >&2; echo "✗ FAILED: $1 (HTTP $CODE)" >&2; head -c 400 "$RESP" >&2; echo "" >&2
  case "$CODE" in 000) echo "  → manager unreachable" >&2 ;; 401|403) echo "  → auth/scope" >&2 ;;
  422) echo "  → bad request body" >&2 ;; 5*) echo "  → server error: docker compose logs api worker" >&2 ;; esac; exit 1; }

echo "=============================================================="
echo " Vedha automated assessment   manager=$BASE  scope=$SCOPE  targets=$TARGETS"
echo "=============================================================="

# ── 0) ensure manager is up ──────────────────────────────────────────────────
health() { curl $CURL_K -s -o /dev/null -w '%{http_code}' "$BASE/health" 2>/dev/null || echo 000; }
if [ "$(health)" != "200" ]; then
  case "$BASE" in *localhost*|*127.0.0.1*)
    [ -z "$NO_BRINGUP" ] || { echo "✗ manager down and --no-bringup set" >&2; exit 1; }
    echo "• manager down — bringing it up (make up) ..."; ( cd "$ROOT" && make up >/tmp/vedha-assess-up.log 2>&1 ) || { echo "✗ make up failed (see /tmp/vedha-assess-up.log)" >&2; exit 1; }
    n=0; while [ "$(health)" != "200" ] && [ "$n" -lt 120 ]; do sleep 3; n=$((n+3)); done ;;
  *) echo "✗ remote manager $BASE not reachable (HTTP $(health))" >&2; exit 1 ;;
  esac
fi
[ "$(health)" = "200" ] || die "manager /health"
echo "✓ manager up"

# ── 1) auth ──────────────────────────────────────────────────────────────────
lbody="$(EMAIL="$EMAIL" PASSWORD="$PASSWORD" python3 -c 'import json,os;print(json.dumps({"email":os.environ["EMAIL"],"password":os.environ["PASSWORD"]}))')"
CODE="$(printf '%s' "$lbody" | curl $CURL_K -sS -o "$RESP" -w '%{http_code}' -X POST "$BASE/auth/login" -H 'Content-Type: application/json' -d @- 2>"$ERRF" || echo 000)"
ok || die "login"
JWT="$(py get "$RESP" access_token)"; [ -n "$JWT" ] || die "login (no token)"
{ printf 'silent\nshow-error\n'; printf 'header = "Authorization: Bearer %s"\n' "$JWT"; } > "$CFG"; chmod 600 "$CFG"
echo "✓ authenticated ($EMAIL)"

# ── 2) ensure a probe is online (auto-launch native probe if not) ────────────
call GET "$BASE/agents"; ok || die "list agents"
ONLINE="$(py agents-online "$RESP")"
if [ -z "$ONLINE" ]; then
  case "$BASE" in *localhost*|*127.0.0.1*) : ;; *) echo "✗ no probe online on remote manager — deploy one first." >&2; exit 1 ;; esac
  echo "• no probe online — provisioning a native probe ..."
  call POST "$BASE/auth/personal-access-tokens" "$(py pat-body "assess-$(date +%s)")"; ok || die "mint PAT"
  VPAT="$(py get "$RESP" token)"; [ -n "$VPAT" ] || die "mint PAT (no token)"
  ( cd "$ROOT/probe" && { [ -x .venv/bin/python ] && .venv/bin/python -c 'import httpx' 2>/dev/null; } \
      || { python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt; } ) || { echo "✗ probe venv setup failed" >&2; exit 1; }
  mkdir -p /tmp/vedha-assess-spool
  ( cd "$ROOT/probe" && PLATFORM_URL="$BASE" OPERATOR_TOKEN="$VPAT" PROBE_NAME="assess-probe" \
      PROBE_NETWORK_SEGMENTS="127.0.0.0/8,$SCOPE" LICENSE_ENFORCED=false \
      STATE_FILE=/tmp/vedha-assess-state.json RESULT_SPOOL_DIR=/tmp/vedha-assess-spool \
      nohup .venv/bin/python -m agent.agent > "$PROBE_LOG" 2>&1 & echo $! > /tmp/vedha-assess-probe.pid )
  AUTO_PROBE_PID="$(cat /tmp/vedha-assess-probe.pid)"
  n=0; while [ "$n" -lt 60 ]; do call GET "$BASE/agents"; ONLINE="$(py agents-online "$RESP")"; [ -n "$ONLINE" ] && break; sleep 2; n=$((n+2)); done
  [ -n "$ONLINE" ] || { echo "✗ probe did not register — log:" >&2; tail -15 "$PROBE_LOG" >&2; exit 1; }
fi
echo "✓ probe online: $ONLINE"

# ── 3) engagement + scan (discovery then assessment) ─────────────────────────
call POST "$BASE/engagements" "$(py eng-body "assess $SCOPE $(date +%F)" "$SCOPE")"; ok || die "create engagement"
EID="$(py get "$RESP" id)"; [ -n "$EID" ] || die "engagement (no id)"
echo "✓ engagement: $EID"

run_job() {  # use_case label -> sets JID
  call POST "$BASE/agents/jobs" "$(py job-body "$EID" "$1" "$TARGETS" "$SCOPE")"; ok || die "enqueue $2"
  JID="$(py get "$RESP" job_id)"; [ -n "$JID" ] || die "enqueue $2 (no job_id)"
  echo "  → $2 job $JID"
  w=0; while [ "$w" -lt "$TIMEOUT" ]; do call GET "$BASE/agents/jobs/$JID"; ok || die "poll $2"
    st="$(py job-status "$RESP")"; printf '\r    %s: %s (%ss)      ' "$2" "$st" "$w"
    case "$st" in done|completed) printf '\n'; return 0 ;; failed|error) printf '\n'; return 1 ;; esac
    sleep 5; w=$((w+5)); done; printf '\n'; return 2
}
echo "── scanning ──"
run_job uc_discovery_only "Discovery" || echo "  (discovery not done — continuing)"
run_job "$USE_CASE" "Assessment" || echo "  (assessment ended non-clean — diagnosing below)"
cp "$RESP" "$JOBF"                       # keep the assessment job object for diagnostics

# ── 4) results + accuracy + failure-point debug report ───────────────────────
echo ""
echo "── findings ──"
call GET "$BASE/findings?engagement_id=$EID&page_size=100"; ok || die "list findings"; cp "$RESP" "$FINDF"
FINDINGS="$(py len "$FINDF")"; echo "  total findings: $FINDINGS"

# independent ground truth (only for single-IP targets, with --verify)
echo '{"items":[]}' > "$INDF"
if [ -n "$VERIFY" ]; then
  echo "  running independent ground-truth port scan (this host's vantage) ..."
  first=1; printf '{"items":[' > "$INDF"
  for t in $(printf '%s' "$TARGETS" | tr ',' ' '); do
    case "$t" in */*) continue ;; esac    # skip CIDRs
    [ "$first" = 1 ] || printf ',' >> "$INDF"; py portscan "$t" >> "$INDF"; first=0
  done
  printf ']}' >> "$INDF"
fi

echo ""
echo "── DEBUG REPORT ──"
py funnel "$JOBF"
call GET "$BASE/engagements/$EID/assets"; ASSETS="$(py len "$RESP")"; echo "  assets ingested: $ASSETS"
echo "  detection audit:"; py findings-audit "$FINDF"
py diagnose "$JOBF" "$INDF" "$ASSETS" "$FINDINGS"

echo ""
echo "Engagement $EID · findings: $BASE/findings?engagement_id=$EID"
[ -n "$AUTO_PROBE_PID" ] && echo "(auto-probe pid $AUTO_PROBE_PID; log $PROBE_LOG$([ -n "$KEEP_PROBE" ] && echo ' — kept' || echo ' — stopping'))" || true
