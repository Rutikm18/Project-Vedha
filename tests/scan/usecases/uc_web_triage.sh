#!/usr/bin/env bash
# UC3 — Web + TLS Triage (probe use_case: uc_external_web_triage / uc_web_app_triage)
# Web-layer fingerprint + cert/protocol facts. Finds missing security headers,
# dangerous HTTP methods, tech disclosure, weak/expired TLS.
#
#   ./uc_web_triage.sh 192.168.1.10
set -u
. "$(dirname "$0")/_uc_lib.sh"
uc_init "${1:-}"

uc_run "Web fingerprint (HTTP methods, headers, tech)" web_scanner -p "$UC_WEB_PORTS"
"$PY" - "$UC_LAST" <<'PY'
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
if not rows: print("   (no web services responded)"); raise SystemExit
for r in rows:
    d = r.get("data") or {}
    print(f"   {d.get('url')}  HTTP {d.get('status')}  title={d.get('title')!r}")
    print(f"      server={d.get('server')}  tech={d.get('tech_hints')}")
    print(f"      sec-headers MISSING: {d.get('security_headers_missing')}")
    if d.get('dangerous_methods'):
        print(f"      DANGEROUS METHODS: {d.get('dangerous_methods')}")
PY
echo

uc_run "TLS/cert audit (protocol, cipher, cert)" tls_scanner -p "$UC_TLS_PORTS"
"$PY" - "$UC_LAST" <<'PY'
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
if not rows: print("   (no TLS services)"); raise SystemExit
for r in rows:
    d = r.get("data") or {}
    print(f"   port {r.get('port')}: {r.get('evidence')}")
    for k in ("protocol", "cipher", "cert_subject", "cert_not_after", "self_signed", "expired"):
        if k in d: print(f"      {k}: {d[k]}")
PY
echo
