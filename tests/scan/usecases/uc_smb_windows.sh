#!/usr/bin/env bash
# UC6 — Windows / SMB Estate (probe use_case: uc_windows_estate)
# SMB dialect + signing detection. Finds SMBv1 enabled (WannaCry/EternalBlue
# surface) and SMB signing NOT required (relay surface).
#
#   ./uc_smb_windows.sh 192.168.1.10
set -u
. "$(dirname "$0")/_uc_lib.sh"
uc_init "${1:-}"

uc_run "SMB dialect + signing" smb_scanner --port 445
"$PY" - "$UC_LAST" <<'PY'
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
if not rows: print("   (no SMB response on 445)"); raise SystemExit
for r in rows:
    d = r.get("data") or {}
    print(f"   {r.get('target')} :445  {r.get('status')}  {r.get('evidence')}")
    for k in ("dialect", "smbv1", "signing_required", "signing", "os", "domain"):
        if k in d: print(f"      {k}: {d[k]}")
    if d.get("smbv1") is True:
        print("      *** SMBv1 ENABLED — legacy/vulnerable (EternalBlue surface) ***")
    if d.get("signing_required") is False:
        print("      *** SMB signing NOT required — NTLM relay surface ***")
PY
echo
