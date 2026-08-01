#!/usr/bin/env sh
# =============================================================================
# Vedha — facts → real VA (import through the manager's detection pipeline)
#
# Runs a probe scan export (.jsonl / .json) through the SAME detection pipeline
# a live probe result takes: ingest → assets → CVE match (OSV-Debian) → enrich
# (CVSS/KEV/EPSS) → persist → dashboard. Then prints a VA report.
#
#   scripts/detect-va.sh                      # DEMO: generates a vulnerable
#                                             # Debian host and shows real findings
#   scripts/detect-va.sh --facts scan.jsonl --name "ClientX Q3"
#   scripts/detect-va.sh --manager https://vedha.example.com --facts export.jsonl
#
# The detection engine matches DEBIAN package versions (OSV Debian:12). Real
# findings need authenticated package inventory (ssh_inventory dpkg_packages) or
# banners of covered products (openssh/nginx/openssl/curl/samba/vsftpd/...).
# =============================================================================
set -eu

MANAGER="${MANAGER:-http://localhost:18080}"; FACTS=""; NAME=""; EMAIL=""; NO_BRINGUP=""
while [ $# -gt 0 ]; do
  case "$1" in
    --manager) MANAGER="$2"; shift 2 ;;   --facts) FACTS="$2"; shift 2 ;;
    --name) NAME="$2"; shift 2 ;;         --email) EMAIL="$2"; shift 2 ;;
    --no-bringup) NO_BRINGUP="yes"; shift ;;
    -h|--help) sed -n '2,19p' "$0"; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done
command -v curl >/dev/null 2>&1    || { echo "curl required" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "python3 required" >&2; exit 1; }
case "$MANAGER" in http://*|https://*) BASE="$MANAGER" ;; *) BASE="https://$MANAGER" ;; esac
BASE="${BASE%/}"
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
envval() { [ -f "$ROOT/.env" ] && grep -E "^$1=" "$ROOT/.env" 2>/dev/null | head -1 | cut -d= -f2- || true; }
[ -n "$EMAIL" ] || EMAIL="${ADMIN_EMAIL:-$(envval SEED_ADMIN_EMAIL)}"; [ -n "$EMAIL" ] || EMAIL="admin@vedha.io"
PASSWORD="${ADMIN_PASSWORD:-$(envval SEED_ADMIN_PASSWORD)}"; [ -n "$PASSWORD" ] || PASSWORD="ChangeMe123!"

# ── demo facts (guaranteed findings): a Debian host with old packages ────────
GEN="$(mktemp).jsonl"; trap 'rm -f "$GEN"' EXIT
if [ -z "$FACTS" ]; then
  cat > "$GEN" <<'JSONL'
{"scanner":"ssh_inventory","target":"10.0.0.50","timestamp":"2026-01-01T00:00:00Z","status":"open","port":22,"data":{"inventory":{"hostname":"vuln-debian","dpkg_packages":"openssh-server 1:6.6p1-4\nopenssl 1.0.1e-2\nnginx 1.6.2-5\nvsftpd 2.3.4-1\nsamba 3.6.0-1\ncurl 7.20.0-1\nbind9 9.8.0-1\napache2 2.4.7-1\nredis-server 3.0.6-1\n"}}}
JSONL
  FACTS="$GEN"; [ -n "$NAME" ] || NAME="DEMO — vulnerable Debian host"
fi
[ -f "$FACTS" ] || { echo "facts file not found: $FACTS" >&2; exit 1; }
[ -n "$NAME" ] || NAME="VA import $(date +%F)"

# ── helper: fresh token each call (login JWTs expire fast) ────────────────────
login() { curl -sS -X POST "$BASE/auth/login" -H 'Content-Type: application/json' \
  -d "$(EMAIL="$EMAIL" PASSWORD="$PASSWORD" python3 -c 'import json,os;print(json.dumps({"email":os.environ["EMAIL"],"password":os.environ["PASSWORD"]}))')" \
  | python3 -c 'import sys,json;print(json.load(sys.stdin).get("access_token",""))' 2>/dev/null; }

echo "=============================================================="
echo " Vedha detect-va   manager=$BASE   facts=$FACTS"
echo "=============================================================="

# ── 0) manager up ────────────────────────────────────────────────────────────
health() { curl -s -o /dev/null -w '%{http_code}' "$BASE/health" 2>/dev/null || echo 000; }
if [ "$(health)" != "200" ]; then
  case "$BASE" in *localhost*|*127.0.0.1*)
    [ -z "$NO_BRINGUP" ] || { echo "✗ manager down (--no-bringup set)" >&2; exit 1; }
    echo "• manager down — make up ..."; ( cd "$ROOT" && make up >/tmp/vedha-detectva-up.log 2>&1 ) || { echo "✗ make up failed (/tmp/vedha-detectva-up.log)" >&2; exit 1; }
    n=0; while [ "$(health)" != "200" ] && [ "$n" -lt 150 ]; do sleep 3; n=$((n+3)); done ;;
  *) echo "✗ remote manager unreachable (HTTP $(health))" >&2; exit 1 ;;
  esac
fi
[ "$(health)" = "200" ] || { echo "✗ manager /health not 200" >&2; exit 1; }
echo "✓ manager up"

TOKEN="$(login)"; [ -n "$TOKEN" ] || { echo "✗ login failed (check ADMIN_PASSWORD)" >&2; exit 1; }
echo "✓ authenticated ($EMAIL)"

# ── 1) engagement ────────────────────────────────────────────────────────────
EID="$(curl -sS -X POST "$BASE/engagements" -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d "$(NAME="$NAME" python3 -c 'import json,os;print(json.dumps({"name":os.environ["NAME"],"scope_cidrs":["10.0.0.0/24"]}))')" \
  | python3 -c 'import sys,json;print(json.load(sys.stdin).get("id",""))')"
[ -n "$EID" ] || { echo "✗ engagement create failed" >&2; exit 1; }
echo "✓ engagement: $EID"

# ── 2) import facts → real detection pipeline ────────────────────────────────
imp="$(curl -sS -X POST "$BASE/engagements/$EID/scans/import-facts" -H "Authorization: Bearer $TOKEN" -F "file=@$FACTS")"
echo "  import: $imp"
echo "$imp" | python3 -c 'import sys,json
try: d=json.load(sys.stdin); assert d.get("imported"); print("✓ facts ingested:", d.get("fact_count"), "| assets:", d.get("assets_promoted"))
except Exception: print("✗ import failed — see above", file=sys.stderr); sys.exit(1)' || exit 1

# ── 3) poll detection (background job) ───────────────────────────────────────
printf "  detecting"; T="$(login)"; total=0
for i in $(seq 1 25); do
  total="$(curl -s "$BASE/findings/summary?engagement_id=$EID" -H "Authorization: Bearer $T" | python3 -c 'import sys,json
try: print(json.load(sys.stdin).get("total",0))
except: print(0)' 2>/dev/null)"
  [ "${total:-0}" -gt 0 ] 2>/dev/null && break
  printf "."; sleep 2
done
printf "\n"

# ── 4) VA report (temp files + heredoc → no shell quote-escaping) ────────────
T="$(login)"; SUMF="$(mktemp)"; TOPF="$(mktemp)"
curl -s "$BASE/findings/summary?engagement_id=$EID" -H "Authorization: Bearer $T" > "$SUMF" 2>/dev/null || true
curl -s "$BASE/findings?engagement_id=$EID&page_size=100&sort=risk" -H "Authorization: Bearer $T" > "$TOPF" 2>/dev/null || true
echo ""; echo "── VA REPORT ──"
python3 - "$SUMF" "$TOPF" <<'PY'
import json, sys
def load(p):
    try: return json.load(open(p))
    except Exception: return {}
s = load(sys.argv[1]); top = load(sys.argv[2]).get("items", [])
print("  total findings :", s.get("total"), "   average_risk:", s.get("average_risk"))
print("  CRITICAL %s · HIGH %s · MEDIUM %s · LOW %s · INFO %s" % (
    s.get("critical_open"), s.get("high_open"), s.get("medium_open"), s.get("low_open"), s.get("info_open")))
print("  exploit-validated %s · detection-blind %s" % (s.get("validated"), s.get("blind")))
print("  top by risk:")
for x in top[:15]:
    cve = (x.get("cve_ids") or [""])[0]
    print("     [%8s] cvss=%4s %-18s %s" % (
        (x.get("severity") or "").upper(), str(x.get("cvss_score") or "-"), cve, (x.get("title") or "")[:46]))
PY
rm -f "$SUMF" "$TOPF"
echo ""
echo "Engagement $EID"
echo "Dashboard : $BASE  → Findings (this engagement) → click Explain (Ask Vedha)"
echo "API       : $BASE/findings?engagement_id=$EID&page_size=100"
