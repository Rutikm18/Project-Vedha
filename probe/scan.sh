#!/usr/bin/env bash
#
# scan.sh — real assessment runner for the Agentic VA Scanner probe.
#
# Point it at a real target and it performs an actual scan, then prints a clean,
# consolidated per-host findings report. It uses the best available engine under
# the hood for accuracy — battle-tested open-source scanners when present — and
# keeps all raw tool output in a hidden .logs/ dir so the console stays clean.
#
# USAGE:
#   ./scan.sh <target> [ports]
#     target : IP, CIDR, hostname, or range (e.g. 192.168.1.10, 10.0.0.0/24)
#     ports  : optional TCP port spec (e.g. "1-1000" or "22,80,443,3306")
#              default: nmap's top ports (or 1-1000 for the fallback engine)
#
# EXAMPLES:
#   ./scan.sh 127.0.0.1
#   ./scan.sh 192.168.1.10 1-65535
#   ./scan.sh 10.0.0.0/24 22,80,443,445,3389
#
# NOTE: only scan systems you are authorized to. The target you pass becomes the
# authorization scope; the scanners refuse anything outside it.
#
set -uo pipefail

# ── args ────────────────────────────────────────────────────────────────────
if [ $# -lt 1 ]; then
  echo "usage: $0 <target> [ports]"; exit 2
fi
TARGET="$1"
PORTS="${2:-}"

c_blue='\033[1;34m'; c_grn='\033[1;32m'; c_yel='\033[1;33m'; c_dim='\033[2m'; c_rst='\033[0m'
say()  { echo -e "${c_blue}[*]${c_rst} $*"; }
good() { echo -e "${c_grn}[+]${c_rst} $*"; }
note() { echo -e "${c_yel}[!]${c_rst} $*"; }

SAFE=$(echo "$TARGET" | tr '/.:' '___')
TS=$(date +%Y%m%d_%H%M%S)
OUTDIR="./scan_${SAFE}_${TS}"
LOGDIR="$OUTDIR/.logs"                 # hidden: raw tool/scanner output lives here
mkdir -p "$LOGDIR"
SCOPE="$OUTDIR/.scope"                 # authorization = the target you named
printf '%s\n' "$TARGET" > "$SCOPE"

# ── engine detection (silent — we don't advertise tool names on the console) ──
HAVE_NMAP=0;    command -v nmap    >/dev/null 2>&1 && HAVE_NMAP=1
HAVE_MASSCAN=0; command -v masscan >/dev/null 2>&1 && HAVE_MASSCAN=1
HAVE_NUCLEI=0;  command -v nuclei  >/dev/null 2>&1 && HAVE_NUCLEI=1

echo -e "${c_dim}────────────────────────────────────────────────────────${c_rst}"
say "Target : $TARGET"
say "Scope  : $TARGET (authorized)"
[ -n "$PORTS" ] && say "Ports  : $PORTS"
echo -e "${c_dim}────────────────────────────────────────────────────────${c_rst}"

run() { # logfile, command...   (captures stdout->logfile.jsonl, stderr->logfile.log)
  local base="$1"; shift
  "$@" > "$LOGDIR/${base}.jsonl" 2> "$LOGDIR/${base}.log"
}

# ── STAGE 1 — hosts, ports & service/version detection ───────────────────────
say "[1/3] Discovering hosts, ports & services…"

# Prefer nmap for authoritative service/version (-sV). Fall back to a fast
# mass sweep, then the pure engine — whichever is available. All hidden.
DISC_ENGINE="builtin"
if [ "$HAVE_NMAP" = "1" ]; then
  DISC_ENGINE="nmap"
  if [ -n "$PORTS" ]; then
    run 1_discovery python3 -m scanner.nmap_wrapper -t "$TARGET" -s "$SCOPE" --profile version -p "$PORTS"
  else
    run 1_discovery python3 -m scanner.nmap_wrapper -t "$TARGET" -s "$SCOPE" --profile version
  fi
elif [ "$HAVE_MASSCAN" = "1" ] || true; then
  DISC_ENGINE="mass"
  MP="${PORTS:-1-1000}"
  # real masscan if present, else pure-Python sweep (both via this wrapper)
  if [ "$HAVE_MASSCAN" = "1" ]; then
    run 1_discovery python3 -m scanner.mass_scan -t "$TARGET" -s "$SCOPE" -p "$MP"
  else
    run 1_discovery python3 -m scanner.mass_scan -t "$TARGET" -s "$SCOPE" -p "$MP" --fallback
  fi
fi

# extract the OPEN tcp ports found, per the discovery JSONL
OPEN_TCP=$(python3 - "$LOGDIR/1_discovery.jsonl" <<'PY'
import json, sys
ports = set()
try:
    for line in open(sys.argv[1]):
        line = line.strip()
        if not line.startswith("{"):
            continue
        o = json.loads(line)
        if o.get("proto") == "tcp" and o.get("status") == "open" and o.get("port"):
            ports.add(int(o["port"]))
except FileNotFoundError:
    pass
print(",".join(str(p) for p in sorted(ports)))
PY
)

if [ -z "$OPEN_TCP" ]; then
  note "No open TCP ports found on $TARGET (host may be down/filtered or out of scope)."
else
  good "Open TCP ports: $OPEN_TCP"
fi

# ── STAGE 2 — deep fingerprinting on the open services ───────────────────────
say "[2/3] Deep fingerprinting open services…"
if [ -n "$OPEN_TCP" ]; then
  # banner/version enrichment (client-first for HTTP, read-first for others)
  run 2_service python3 -m scanner.service_banner -t "$TARGET" -s "$SCOPE" -p "$OPEN_TCP"
  # TLS posture (returns nothing on non-TLS ports — safe to point at all open)
  run 2_tls     python3 -m scanner.tls_scanner    -t "$TARGET" -s "$SCOPE" -p "$OPEN_TCP"
  # HTTP(S) fingerprint (title / server / security headers)
  run 2_web     python3 -m scanner.web_scanner    -t "$TARGET" -s "$SCOPE" -p "$OPEN_TCP"
  # DB protocol handshake (mysql/postgres/mssql/…)
  run 2_db      python3 -m scanner.db_scanner     -t "$TARGET" -s "$SCOPE"
  # SMB dialects (only meaningful if 445 is open)
  case ",$OPEN_TCP," in *,445,*) run 2_smb python3 -m scanner.smb_scanner -t "$TARGET" -s "$SCOPE" ;; esac
  # AI/MCP endpoint discovery (unauth model servers)
  run 2_ai      python3 -m scanner.mcp_ai_scanner -t "$TARGET" -s "$SCOPE"
fi
# UDP services (DNS/NTP/SNMP/NetBIOS) — independent of TCP results
run 2_udp  python3 -m scanner.udp_scanner  -t "$TARGET" -s "$SCOPE"
run 2_snmp python3 -m scanner.snmp_scanner -t "$TARGET" -s "$SCOPE"

# Deep vulnerability checks against discovered web services (single-host targets).
# Auto-activates only when a template-based checker is present; runs hidden.
if [ "$HAVE_NUCLEI" = "1" ] && [ -n "$OPEN_TCP" ] && [[ "$TARGET" != */* ]]; then
  say "Running deep vulnerability checks…"
  : > "$LOGDIR/.vtargets"
  for p in ${OPEN_TCP//,/ }; do
    printf 'http://%s:%s\n'  "$TARGET" "$p" >> "$LOGDIR/.vtargets"
    printf 'https://%s:%s\n' "$TARGET" "$p" >> "$LOGDIR/.vtargets"
  done
  nuclei -l "$LOGDIR/.vtargets" -jsonl -silent -o "$LOGDIR/3_vuln.jsonl" \
    >/dev/null 2> "$LOGDIR/3_vuln.log" || true
fi

# ── STAGE 3 — consolidate every fact into one per-host report ────────────────
say "[3/3] Consolidating findings…"
python3 - "$LOGDIR" "$OUTDIR/findings.json" "$OUTDIR/report.txt" <<'PY'
import glob, json, os, sys

logdir, findings_json, report_txt = sys.argv[1], sys.argv[2], sys.argv[3]

# host -> "tcp/8080" -> merged fact dict ; plus udp singletons
hosts = {}
def slot(host, proto, port):
    return hosts.setdefault(host, {}).setdefault(f"{proto}/{port}", {
        "port": port, "proto": proto, "state": "open",
        "service": None, "product": None, "version": None,
        "banner": None, "tls": None, "http": None, "db": None, "smb": None, "ai": None,
    })

findings = []  # notable, human-review-worthy observations

for path in sorted(glob.glob(os.path.join(logdir, "*.jsonl"))):
    for line in open(path, errors="replace"):
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            o = json.loads(line)
        except Exception:
            continue

        # Template-based vuln checker output (different schema). Parse into a
        # neutral finding — the checker's identity is never carried through.
        if o.get("template-id") or o.get("templateID") or o.get("matched-at"):
            import re as _re
            info = o.get("info") or {}
            sev = str(info.get("severity") or "info").upper()
            name = info.get("name") or o.get("template-id") or o.get("templateID") or "issue"
            at = o.get("matched-at") or o.get("matched_at") or o.get("host") or o.get("ip") or ""
            m = _re.search(r"https?://([^/:]+):?(\d+)?", str(at))
            vh = (m.group(1) if m else (o.get("host") or o.get("ip"))) or "?"
            vp = (m.group(2) if (m and m.group(2)) else "")
            vwhere = f"tcp/{vp}" if vp else "-"
            detail = str(name)
            if at and str(at) not in detail:
                detail += f" @ {at}"
            findings.append((vh, vwhere, f"VULN-{sev}", detail))
            continue

        host = o.get("target"); scanner = o.get("scanner") or ""; data = o.get("data") or {}
        port = o.get("port"); proto = o.get("proto") or "tcp"
        if not host:
            continue

        if scanner.startswith("nmap") or scanner in ("mass_scan", "port_scan"):
            if o.get("status") == "open" and port:
                s = slot(host, proto, port)
                s["service"] = data.get("service") or s["service"]
                s["product"] = data.get("product") or s["product"]
                s["version"] = data.get("version") or s["version"]
        elif scanner == "service_banner" and port:
            s = slot(host, proto, port)
            s["banner"] = (data.get("first_line") or data.get("banner") or "")[:80] or s["banner"]
        elif scanner == "tls_scan" and port:
            s = slot(host, proto, port)
            cert = data.get("certificate") or {}
            s["tls"] = {
                "versions": data.get("accepted_versions") or [],
                "subject": cert.get("subject"),
                "self_signed": cert.get("self_signed"),
                "expired": cert.get("expired"),
            }
            vers = s["tls"]["versions"]
            if any(v in ("TLSv1_0", "TLSv1_1") for v in vers):
                findings.append((host, f"{proto}/{port}", "WEAK-TLS",
                                 f"accepts deprecated {','.join(v for v in vers if v in ('TLSv1_0','TLSv1_1'))}"))
            if cert.get("expired"):
                findings.append((host, f"{proto}/{port}", "TLS-CERT", "certificate expired"))
            if cert.get("self_signed"):
                findings.append((host, f"{proto}/{port}", "TLS-CERT", "self-signed certificate"))
        elif scanner == "web_scan" and port:
            s = slot(host, proto, port)
            s["http"] = {
                "status": data.get("status"), "title": data.get("title"),
                "server": data.get("server"),
                "redirect_location": data.get("redirect_location"),
                "missing_sec": data.get("security_headers_missing") or [],
                "tech": data.get("tech_hints") or [],
            }
            missing = data.get("security_headers_missing") or []
            if len(missing) >= 3:
                findings.append((host, f"{proto}/{port}", "MISSING-HEADERS",
                                 f"{len(missing)} security headers absent ({', '.join(missing[:3])}, ...)"))
        elif scanner == "db_scan" and port:
            s = slot(host, proto, port)
            s["db"] = {"engine": data.get("engine"), "version": data.get("server_version")}
            findings.append((host, f"{proto}/{port}", "DB-EXPOSED",
                             f"{data.get('engine')} {data.get('server_version') or ''} reachable"))
        elif scanner == "smb_scan" and port:
            s = slot(host, proto, port)
            s["smb"] = {"v1": data.get("smbv1_enabled"), "v2": data.get("smb2_supported")}
            if data.get("smbv1_enabled"):
                findings.append((host, f"{proto}/{port}", "SMBv1", "legacy SMBv1 enabled"))
        elif scanner == "mcp_ai_scan" and port:
            s = slot(host, proto, port)
            s["ai"] = {"kind": data.get("kind"), "unauth": data.get("unauthenticated_access")}
            if data.get("unauthenticated_access"):
                findings.append((host, f"{proto}/{port}", "AI-NOAUTH",
                                 f"{data.get('kind')} endpoint without auth"))
        elif scanner in ("udp_scan", "snmp_scan") and port and o.get("status") == "open":
            s = slot(host, proto or "udp", port)
            s["service"] = s["service"] or data.get("service") or data.get("service_guess")
            if scanner == "snmp_scan" and data.get("community"):
                findings.append((host, f"udp/{port}", "SNMP",
                                 f"responds to community '{data.get('community')}'"))

# ── render ───────────────────────────────────────────────────────────────────
def one_line(s):
    svc = s["service"] or "?"
    # Real HTTP probe beats nmap's port-number-based service guess
    if s.get("http"):
        svc = "http"
    ver = " ".join(x for x in (s.get("product"), s.get("version")) if x)
    extra = []
    if s.get("db"):
        extra.append(f"db={s['db'].get('engine')} {s['db'].get('version') or ''}".strip())
    if s.get("tls"):
        extra.append("tls=" + ",".join(s["tls"]["versions"]))
    if s.get("http"):
        h = s["http"]
        if h.get("server"):
            extra.append(f"server={h['server']}")
        if h.get("title"):
            extra.append(f"title={h['title']!r}")
        elif h.get("status"):
            st = f"HTTP {h['status']}"
            if h.get("redirect_location"):
                st += f" -> {h['redirect_location']}"
            extra.append(st)
    if s.get("smb"):
        extra.append(f"smbv1={'on' if s['smb'].get('v1') else 'off'}")
    if s.get("ai"):
        extra.append(f"ai={s['ai'].get('kind')} unauth={s['ai'].get('unauth')}")
    if not extra and s.get("banner"):
        extra.append(s["banner"])
    return f"  {str(s['port'])+'/'+s['proto']:<11} {svc:<12} {ver:<22} {'  '.join(extra)}".rstrip()

lines = []
total_ports = 0
for host in sorted(hosts):
    lines.append(f"\nHOST {host}")
    for key in sorted(hosts[host], key=lambda k: (k.split('/')[0], int(k.split('/')[1]))):
        lines.append(one_line(hosts[host][key]))
        total_ports += 1
report = "VEDHA — Assessment Report" + ("\n" + "\n".join(lines) if lines else "\n(no open services found)")

if findings:
    report += "\n\nNOTABLE FINDINGS"
    seen = set()
    for host, where, tag, msg in findings:
        k = (host, where, tag, msg)
        if k in seen: continue
        seen.add(k)
        report += f"\n  [{tag}] {host} {where} — {msg}"

open(report_txt, "w").write(report + "\n")
json.dump({"engine": "vedha-probe", "hosts": hosts,
           "findings": [{"host": h, "where": w, "tag": t, "detail": m}
                        for (h, w, t, m) in dict.fromkeys(findings)]},
          open(findings_json, "w"), indent=2, default=str)

print(report)
print(f"\n[summary] {len(hosts)} host(s), {total_ports} open service(s), {len(set(findings))} notable finding(s)")
PY

echo -e "${c_dim}────────────────────────────────────────────────────────${c_rst}"
good "Report : $OUTDIR/report.txt"
good "JSON   : $OUTDIR/findings.json"
echo -e "${c_dim}Raw tool output (hidden): $LOGDIR/${c_rst}"
